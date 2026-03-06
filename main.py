from fastapi import FastAPI, Form, HTTPException, File, UploadFile, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, field_validator
import os
from typing import Optional
from datetime import datetime, timezone
import uuid
import base64
import json

import io

import anthropic
import voyageai
import pillow_heif
import stripe
from PIL import Image

from database import get_connection, ANTHROPIC_API_KEY, VOYAGE_API_KEY
import jwt

from security import create_handoff_token, decode_handoff_token, hash_secret, verify_secret

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)

_STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
_STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = _STRIPE_SECRET_KEY

_TWILIO_ACCOUNT_SID  = os.getenv("TWILIO_ACCOUNT_SID", "")
_TWILIO_AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN", "")
_TWILIO_VERIFY_SID   = os.getenv("TWILIO_VERIFY_SID", "")
_TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

_twilio_client = None
if _TWILIO_ACCOUNT_SID and _TWILIO_AUTH_TOKEN:
    from twilio.rest import Client as TwilioClient
    _twilio_client = TwilioClient(_TWILIO_ACCOUNT_SID, _TWILIO_AUTH_TOKEN)

_APP_URL = "https://md-gityup.github.io/lofo-ai/LOFO_MVP.html"

_NOTIFY_LOSER_SQL = """
    SELECT l.phone, l.item_type
    FROM items l
    CROSS JOIN items f
    WHERE f.id = %s
      AND l.type = 'loser'
      AND l.status = 'active'
      AND l.phone IS NOT NULL
      AND l.embedding IS NOT NULL
      AND f.embedding IS NOT NULL
      AND 1 - (l.embedding <=> f.embedding) >= 0.7
      AND (
          f.latitude IS NULL OR l.latitude IS NULL
          OR 3958.8 * 2 * ASIN(SQRT(
              POWER(SIN(RADIANS(f.latitude - l.latitude) / 2), 2) +
              COS(RADIANS(l.latitude)) * COS(RADIANS(f.latitude)) *
              POWER(SIN(RADIANS(f.longitude - l.longitude) / 2), 2)
          )) <= 10
      )
    LIMIT 5
"""

_NOTIFY_FINDER_SQL = """
    SELECT f.phone, f.item_type
    FROM items f
    CROSS JOIN items l
    WHERE l.id = %s
      AND f.type = 'finder'
      AND f.status = 'active'
      AND f.phone IS NOT NULL
      AND f.embedding IS NOT NULL
      AND l.embedding IS NOT NULL
      AND 1 - (f.embedding <=> l.embedding) >= 0.7
      AND (
          f.latitude IS NULL OR l.latitude IS NULL
          OR 3958.8 * 2 * ASIN(SQRT(
              POWER(SIN(RADIANS(f.latitude - l.latitude) / 2), 2) +
              COS(RADIANS(l.latitude)) * COS(RADIANS(f.latitude)) *
              POWER(SIN(RADIANS(f.longitude - l.longitude) / 2), 2)
          )) <= 10
      )
    LIMIT 5
"""


def _sms(to: str, body: str) -> None:
    """Send a plain notification SMS. Non-blocking — failures are swallowed."""
    if not (_twilio_client and _TWILIO_PHONE_NUMBER):
        print(f"[LOFO SMS] {to}: {body}")
        return
    try:
        _twilio_client.messages.create(body=body, from_=_TWILIO_PHONE_NUMBER, to=to)
    except Exception as exc:
        print(f"[LOFO SMS error] {to}: {exc}")


def _notify_waiting_losers(finder_item_id: uuid.UUID, finder_item_type: str) -> None:
    """After a finder item is saved, SMS any waiting losers whose item matches."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(_NOTIFY_LOSER_SQL, (str(finder_item_id),))
                rows = cur.fetchall()
        for row in rows:
            label = row["item_type"] or finder_item_type
            _sms(row["phone"],
                 f"LOFO: Your {label} may have been found nearby! "
                 f"Open the app to claim it: {_APP_URL}")
    except Exception as exc:
        print(f"[LOFO notify-losers error] {exc}")


def _notify_matched_finder(loser_item_id: uuid.UUID, loser_item_type: str) -> None:
    """After a loser item is saved and a match exists, SMS the finder."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(_NOTIFY_FINDER_SQL, (str(loser_item_id),))
                rows = cur.fetchall()
        for row in rows:
            label = row["item_type"] or loser_item_type
            _sms(row["phone"],
                 f"LOFO: Someone is looking for a {label} you found! "
                 f"They'll go through the app to verify ownership. "
                 f"Check it out: {_APP_URL}")
    except Exception as exc:
        print(f"[LOFO notify-finder error] {exc}")

_VISION_SYSTEM_PROMPT = (
    'You are an item classifier for a lost and found app. Analyze the image and extract structured information. '
    'Respond ONLY with valid JSON matching this exact schema, no other text: '
    '{"item_type": "string", "color": ["array of colors"], "material": "string or null", '
    '"size": "small/medium/large or null", "features": ["array of distinguishing features"]}'
)

_TEXT_SYSTEM_PROMPT = (
    'You are an item classifier for a lost and found app. Extract structured information from the text description. '
    'Respond ONLY with valid JSON matching this exact schema, no other text: '
    '{"item_type": "string", "color": ["array of colors"], "material": "string or null", '
    '"size": "small/medium/large or null", "features": ["array of distinguishing features"]}'
)

_SUPPORTED_MEDIA_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
_HEIC_MEDIA_TYPES = {"image/heic", "image/heif"}

app = FastAPI(title="LOFO.AI", description="Lost and Found Matching API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def serve_ui():
    return FileResponse(os.path.join(os.path.dirname(__file__), "LOFO_MVP.html"))


# --------------------------------------------------------------------------- #
# Schemas                                                                      #
# --------------------------------------------------------------------------- #

class ItemCreate(BaseModel):
    type: str
    item_type: str
    color: list[str]
    material: Optional[str] = None
    size: Optional[str] = None
    features: Optional[list[str]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    secret_detail: Optional[str] = None  # finder items only

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("finder", "loser"):
            raise ValueError("type must be 'finder' or 'loser'")
        return v


class TextItemCreate(BaseModel):
    type: str
    description: str
    location_description: Optional[str] = None
    secret_detail: Optional[str] = None  # finder items only; ignored for loser
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("finder", "loser"):
            raise ValueError("type must be 'finder' or 'loser'")
        return v


class ItemResponse(BaseModel):
    id: uuid.UUID
    type: str
    item_type: str
    color: list[str]
    material: Optional[str]
    size: Optional[str]
    features: Optional[list[str]]
    status: str
    expires_at: str
    created_at: str
    has_secret: bool = False


class MatchRequest(BaseModel):
    item_id: uuid.UUID


class MatchResponse(BaseModel):
    id: uuid.UUID
    item_type: str
    color: list[str]
    material: Optional[str]
    size: Optional[str]
    features: Optional[list[str]]
    status: str
    similarity_score: float
    distance_miles: Optional[float] = None
    has_secret: bool = False
    created_at: Optional[str] = None


class VerifyRequest(BaseModel):
    finder_item_id: uuid.UUID  # the finder's item that holds the secret
    loser_claim: str           # the loser's description — Claude judges the match


class HandoffValidateRequest(BaseModel):
    token: str


class FinderInfoUpdate(BaseModel):
    finder_email: Optional[str] = None
    secret_detail: Optional[str] = None
    phone: Optional[str] = None
    finder_payout_app: Optional[str] = None    # e.g. 'venmo', 'paypal', 'cashapp', 'zelle'
    finder_payout_handle: Optional[str] = None  # e.g. '@username', '$cashtag', email


class LoserInfoUpdate(BaseModel):
    phone: str


class CoordinateRequest(BaseModel):
    finder_item_id: uuid.UUID
    loser_item_id: uuid.UUID
    loser_phone: str


class TipCreateRequest(BaseModel):
    finder_item_id: uuid.UUID
    loser_item_id: uuid.UUID
    amount_cents: int


class OtpSendRequest(BaseModel):
    phone: str


class OtpVerifyRequest(BaseModel):
    phone: str
    code: str


class ConnectOnboardRequest(BaseModel):
    item_id: uuid.UUID


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #

def _build_embedding_text(profile: dict) -> str:
    colors = " ".join(profile.get("color") or [])
    features = " ".join(profile.get("features") or [])
    return (
        f"item_type: {profile.get('item_type', '')} "
        f"color: {colors} "
        f"material: {profile.get('material', '')} "
        f"size: {profile.get('size', '')} "
        f"features: {features}"
    ).strip()


def _store_embedding(item_id: uuid.UUID, profile: dict) -> None:
    text = _build_embedding_text(profile)
    result = voyage_client.embed([text], model="voyage-3", input_type="document")
    embedding: list[float] = result.embeddings[0]
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET embedding = %s::vector WHERE id = %s",
                (embedding_str, str(item_id)),
            )
        conn.commit()


def _parse_claude_json(raw_text: str) -> dict:
    if raw_text.startswith("```"):
        raw_text = raw_text.removeprefix("```json").removeprefix("```").strip()
        raw_text = raw_text.removesuffix("```").strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail=f"Claude returned non-JSON output. Raw response: {raw_text[:300]}",
        )


def _validate_extracted_profile(extracted: dict) -> None:
    missing = {"item_type", "color", "features"} - set(extracted.keys())
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Claude response is missing required fields: {sorted(missing)}",
        )


_INSERT_SQL = """
    INSERT INTO items (type, item_type, color, material, size, features, latitude, longitude, secret_detail)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING
        id,
        type,
        item_type,
        color,
        material,
        size,
        features,
        status,
        expires_at::text,
        created_at::text,
        (secret_detail IS NOT NULL) AS has_secret
"""

_SELECT_SQL = """
    SELECT
        id,
        type,
        item_type,
        color,
        material,
        size,
        features,
        status,
        expires_at::text,
        created_at::text
    FROM items
    WHERE id = %s
"""

_MATCH_SQL = """
    SELECT
        f.id,
        f.item_type,
        f.color,
        f.material,
        f.size,
        f.features,
        f.status,
        1 - (f.embedding <=> l.embedding) AS similarity_score,
        (f.secret_detail IS NOT NULL) AS has_secret,
        f.created_at::text,
        CASE
            WHEN f.latitude IS NOT NULL AND l.latitude IS NOT NULL THEN
                ROUND(CAST(
                    3958.8 * 2 * ASIN(SQRT(
                        POWER(SIN(RADIANS(f.latitude  - l.latitude)  / 2), 2) +
                        COS(RADIANS(l.latitude)) * COS(RADIANS(f.latitude)) *
                        POWER(SIN(RADIANS(f.longitude - l.longitude) / 2), 2)
                    ))
                AS NUMERIC), 1)
            ELSE NULL
        END AS distance_miles
    FROM items f
    CROSS JOIN items l
    WHERE l.id = %s
      AND f.type = 'finder'
      AND f.status = 'active'
      AND f.embedding IS NOT NULL
      AND l.embedding IS NOT NULL
      AND (
          f.latitude IS NULL OR l.latitude IS NULL
          OR 3958.8 * 2 * ASIN(SQRT(
              POWER(SIN(RADIANS(f.latitude  - l.latitude)  / 2), 2) +
              COS(RADIANS(l.latitude)) * COS(RADIANS(f.latitude)) *
              POWER(SIN(RADIANS(f.longitude - l.longitude) / 2), 2)
          )) <= 10
      )
    ORDER BY f.embedding <=> l.embedding
    LIMIT 5
"""


# --------------------------------------------------------------------------- #
# Endpoints                                                                    #
# --------------------------------------------------------------------------- #

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _INSERT_SQL,
                (item.type, item.item_type, item.color, item.material, item.size, item.features,
                 item.latitude, item.longitude, item.secret_detail),
            )
            row = cur.fetchone()
        conn.commit()

    result = dict(row)
    profile = {
        "item_type": item.item_type,
        "color": item.color,
        "material": item.material,
        "size": item.size,
        "features": item.features,
    }
    _store_embedding(result["id"], profile)
    if item.type == "finder":
        _notify_waiting_losers(result["id"], item.item_type)
    else:
        _notify_matched_finder(result["id"], item.item_type)
    return result


@app.post("/items/from-text", response_model=ItemResponse, status_code=201)
def create_item_from_text(body: TextItemCreate):
    user_message = f"Extract item information from this description: {body.description}"
    if body.location_description:
        user_message += f"\nLocation context: {body.location_description}"

    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=_TEXT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc}") from exc

    extracted = _parse_claude_json(message.content[0].text.strip())
    _validate_extracted_profile(extracted)

    # Store secret_detail on finder items only
    stored_secret = body.secret_detail if body.type == "finder" else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _INSERT_SQL,
                (
                    body.type,
                    extracted["item_type"],
                    extracted["color"],
                    extracted.get("material"),
                    extracted.get("size"),
                    extracted.get("features", []),
                    body.latitude,
                    body.longitude,
                    stored_secret,
                ),
            )
            row = cur.fetchone()
        conn.commit()

    item = dict(row)
    _store_embedding(item["id"], extracted)
    if body.type == "finder":
        _notify_waiting_losers(item["id"], extracted["item_type"])
    else:
        _notify_matched_finder(item["id"], extracted["item_type"])
    return item


@app.post("/items/from-photo", response_model=ItemResponse, status_code=201)
async def create_item_from_photo(
    file: UploadFile = File(...),
    type: str = Form("finder"),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    secret_detail: Optional[str] = Form(None),
):
    if type not in ("finder", "loser"):
        raise HTTPException(status_code=422, detail="type must be 'finder' or 'loser'")

    media_type = file.content_type or "image/jpeg"
    if media_type not in _SUPPORTED_MEDIA_TYPES | _HEIC_MEDIA_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type '{media_type}'. Allowed: {sorted(_SUPPORTED_MEDIA_TYPES | _HEIC_MEDIA_TYPES)}",
        )

    image_bytes = await file.read()

    if media_type in _HEIC_MEDIA_TYPES:
        heif_image = pillow_heif.read_heif(image_bytes)
        pil_image = Image.frombytes(heif_image.mode, heif_image.size, heif_image.data)
        buf = io.BytesIO()
        pil_image.save(buf, format="JPEG")
        image_bytes = buf.getvalue()
        media_type = "image/jpeg"

    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=_VISION_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": "Analyze this image and extract the item information."},
                    ],
                }
            ],
        )
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc}") from exc

    extracted = _parse_claude_json(message.content[0].text.strip())
    _validate_extracted_profile(extracted)

    stored_secret = secret_detail if type == "finder" else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _INSERT_SQL,
                (
                    type,
                    extracted["item_type"],
                    extracted["color"],
                    extracted.get("material"),
                    extracted.get("size"),
                    extracted.get("features", []),
                    latitude,
                    longitude,
                    stored_secret,
                ),
            )
            row = cur.fetchone()
        conn.commit()

    item = dict(row)
    _store_embedding(item["id"], extracted)
    _notify_waiting_losers(item["id"], extracted["item_type"])  # type is always 'finder' here
    return item


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: uuid.UUID):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(_SELECT_SQL, (str(item_id),))
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return dict(row)


@app.post("/match", response_model=list[MatchResponse])
def match_item(body: MatchRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT embedding FROM items WHERE id = %s AND type = 'loser'",
                (str(body.item_id),),
            )
            loser_row = cur.fetchone()

    if loser_row is None:
        raise HTTPException(status_code=404, detail="Loser item not found")
    if loser_row["embedding"] is None:
        raise HTTPException(status_code=422, detail="Item has no embedding yet")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(_MATCH_SQL, (str(body.item_id),))
            rows = cur.fetchall()

    return [dict(r) for r in rows if r["similarity_score"] >= 0.7]


_VERIFY_SYSTEM_PROMPT = (
    "You are an ownership verifier for a lost and found app. "
    "A finder has noted a specific physical detail about a found item. "
    "A claimant says they own the item and provides their own description of that same detail. "
    "Determine whether the claimant's description is consistent with the finder's observation — "
    "they are describing the same real object so the details should align, even if phrased differently. "
    "Be forgiving of synonym use, abbreviation, and different phrasing. "
    "Be strict about factual contradictions (wrong color, wrong number, fundamentally different detail). "
    'Respond ONLY with valid JSON: {"match": true/false, "reason": "one sentence explanation"}'
)


@app.post("/verify")
def verify_item(body: VerifyRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT secret_detail FROM items WHERE id = %s AND type = 'finder'",
                (str(body.finder_item_id),),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Finder item not found")

    finder_secret = row["secret_detail"]
    if not finder_secret:
        # No secret set — skip verification entirely
        return {"verified": True, "reason": "No secret detail required for this item"}

    try:
        message = claude_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=_VERIFY_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": (
                    f'Finder observed: "{finder_secret}"\n'
                    f'Claimant says: "{body.loser_claim}"\n'
                    "Do these describe the same physical detail of the same item?"
                ),
            }],
        )
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Claude API error: {exc}") from exc

    result = _parse_claude_json(message.content[0].text.strip())
    matched = bool(result.get("match", False))
    reason  = result.get("reason", "")

    return {"verified": matched, "reason": reason}


@app.patch("/items/{item_id}/finder-info", status_code=200)
def update_finder_info(item_id: uuid.UUID, body: FinderInfoUpdate):
    updates: dict = {}
    if body.finder_email is not None:
        updates["finder_email"] = body.finder_email
    if body.secret_detail is not None:
        updates["secret_detail"] = body.secret_detail
    if body.phone is not None:
        updates["phone"] = body.phone
    if body.finder_payout_app is not None:
        updates["finder_payout_app"] = body.finder_payout_app
    if body.finder_payout_handle is not None:
        updates["finder_payout_handle"] = body.finder_payout_handle
    if not updates:
        return {"ok": True}
    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [str(item_id)]
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE items SET {set_clause} WHERE id = %s AND type = 'finder' RETURNING id",
                values,
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Finder item not found")
    return {"ok": True}


@app.patch("/items/{item_id}/loser-info", status_code=200)
def update_loser_info(item_id: uuid.UUID, body: LoserInfoUpdate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET phone = %s WHERE id = %s AND type = 'loser' RETURNING id",
                (body.phone, str(item_id)),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Loser item not found")
    return {"ok": True}


@app.post("/handoff/coordinate", status_code=200)
def coordinate_handoff(body: CoordinateRequest):
    """
    Called after loser confirms ownership.
    Saves the loser's phone and fires intro SMS to both parties so they can
    coordinate pickup directly — LOFO never needs to be in the loop again.
    """
    loser_phone = _normalize_phone(body.loser_phone)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET phone = %s WHERE id = %s AND type = 'loser' RETURNING id",
                (loser_phone, str(body.loser_item_id)),
            )
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Loser item not found")
        conn.commit()

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT phone, item_type FROM items WHERE id = %s AND type = 'finder'",
                (str(body.finder_item_id),),
            )
            finder = cur.fetchone()

    if finder is None:
        raise HTTPException(status_code=404, detail="Finder item not found")

    label = finder["item_type"] or "item"
    finder_phone = finder["phone"]

    if finder_phone:
        _sms(
            loser_phone,
            f"LOFO: Ownership confirmed! Your {label} is waiting for you. "
            f"The finder's number: {finder_phone}. Reach out to arrange pickup!"
        )
        _sms(
            finder_phone,
            f"LOFO: The owner of the {label} you found has been verified! "
            f"They'd like to arrange pickup — reach them at {loser_phone}."
        )
    else:
        _sms(
            loser_phone,
            f"LOFO: Ownership confirmed! Your {label} is waiting for you. "
            f"The finder will be in touch shortly to arrange the return."
        )

    return {"ok": True}


# Keep old URL alive so existing deployed HTML still works during transition
@app.patch("/items/{item_id}/finder-email", status_code=200, include_in_schema=False)
def update_finder_email_legacy(item_id: uuid.UUID, body: FinderInfoUpdate):
    return update_finder_info(item_id, body)


@app.post("/tip/create-payment-intent", status_code=201)
def create_tip_payment_intent(body: TipCreateRequest):
    if body.amount_cents < 50:
        raise HTTPException(status_code=422, detail="Minimum tip amount is $0.50")

    connect_account_id = None
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT stripe_connect_account_id FROM items WHERE id = %s AND type = 'finder'",
                (str(body.finder_item_id),),
            )
            finder_row = cur.fetchone()
            if finder_row is None:
                raise HTTPException(status_code=404, detail="Finder item not found")
            connect_account_id = finder_row["stripe_connect_account_id"]
            cur.execute(
                "SELECT id FROM items WHERE id = %s AND type = 'loser'",
                (str(body.loser_item_id),),
            )
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Loser item not found")

    intent_kwargs: dict = {
        "amount": body.amount_cents,
        "currency": "usd",
        "payment_method_types": ["card"],
        "metadata": {
            "finder_item_id": str(body.finder_item_id),
            "loser_item_id": str(body.loser_item_id),
        },
    }
    if connect_account_id:
        intent_kwargs["transfer_data"] = {"destination": connect_account_id}

    try:
        intent = stripe.PaymentIntent.create(**intent_kwargs)
    except stripe.StripeError as exc:
        if connect_account_id and intent_kwargs.get("transfer_data"):
            # Connect account not ready — fall back to platform-held payment
            del intent_kwargs["transfer_data"]
            try:
                intent = stripe.PaymentIntent.create(**intent_kwargs)
            except stripe.StripeError as exc2:
                raise HTTPException(status_code=502, detail=f"Stripe error: {exc2.user_message}") from exc2
        else:
            raise HTTPException(status_code=502, detail=f"Stripe error: {exc.user_message}") from exc

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tips (finder_item_id, loser_item_id, amount_cents, stripe_payment_intent_id)
                VALUES (%s, %s, %s, %s)
                """,
                (str(body.finder_item_id), str(body.loser_item_id), body.amount_cents, intent.id),
            )
        conn.commit()

    return {"client_secret": intent.client_secret, "payment_intent_id": intent.id}


@app.post("/stripe/webhook", status_code=200)
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if _STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, _STRIPE_WEBHOOK_SECRET)
        except stripe.SignatureVerificationError as exc:
            raise HTTPException(status_code=400, detail="Invalid webhook signature") from exc
    else:
        import json as _json
        event = _json.loads(payload)

    if event["type"] == "payment_intent.succeeded":
        pi_id = event["data"]["object"]["id"]
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE tips SET status = 'completed' WHERE stripe_payment_intent_id = %s",
                    (pi_id,),
                )
            conn.commit()

    return {"received": True}


def _normalize_phone(raw: str) -> str:
    """Strip formatting, require a 10-digit US number, return E.164 (+1XXXXXXXXXX)."""
    digits = "".join(c for c in raw if c.isdigit())
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    raise HTTPException(status_code=422, detail="Please enter a valid 10-digit US phone number.")



@app.post("/sms/send-otp", status_code=200)
def send_otp(body: OtpSendRequest):
    phone = _normalize_phone(body.phone)

    if not (_twilio_client and _TWILIO_VERIFY_SID):
        print(f"[LOFO OTP] Twilio Verify not configured — skipping SMS for {phone}")
        return {"ok": True}

    try:
        _twilio_client.verify.v2.services(_TWILIO_VERIFY_SID).verifications.create(
            to=phone,
            channel="sms",
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"SMS delivery failed: {exc}") from exc

    return {"ok": True}


@app.post("/sms/verify-otp", status_code=200)
def verify_otp(body: OtpVerifyRequest):
    phone = _normalize_phone(body.phone)

    if not (_twilio_client and _TWILIO_VERIFY_SID):
        # Dev fallback — accept any 4-digit code when Twilio isn't configured
        return {"verified": True}

    try:
        check = _twilio_client.verify.v2.services(_TWILIO_VERIFY_SID).verification_checks.create(
            to=phone,
            code=body.code.strip(),
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Verification check failed: {exc}") from exc

    if check.status == "approved":
        return {"verified": True}
    return {"verified": False, "reason": "Incorrect code. Check your messages and try again."}


_RAILWAY_URL = "https://lofo-ai-production.up.railway.app"


@app.post("/connect/onboard", status_code=200)
def connect_onboard(body: ConnectOnboardRequest):
    """
    Create (or retrieve) a Stripe Connect Express account for a finder item.
    Returns a Stripe-hosted onboarding URL the finder opens to link their bank.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT stripe_connect_account_id FROM items WHERE id = %s AND type = 'finder'",
                (str(body.item_id),),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Finder item not found")

    connect_account_id = row["stripe_connect_account_id"]

    try:
        if not connect_account_id:
            account = stripe.Account.create(type="express")
            connect_account_id = account.id
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE items SET stripe_connect_account_id = %s WHERE id = %s",
                        (connect_account_id, str(body.item_id)),
                    )
                conn.commit()

        account_link = stripe.AccountLink.create(
            account=connect_account_id,
            refresh_url=f"{_RAILWAY_URL}/connect/refresh?item_id={body.item_id}",
            return_url=f"{_RAILWAY_URL}/connect/return?item_id={body.item_id}",
            type="account_onboarding",
        )
    except stripe.StripeError as exc:
        raise HTTPException(status_code=502, detail=f"Stripe error: {exc.user_message}") from exc

    return {"url": account_link.url, "account_id": connect_account_id}


@app.get("/connect/return", include_in_schema=False)
def connect_return(item_id: Optional[str] = Query(None)):
    """Stripe redirects here after the finder completes onboarding."""
    return RedirectResponse(f"{_APP_URL}?connected=true")


@app.get("/connect/refresh", include_in_schema=False)
def connect_refresh(item_id: Optional[str] = Query(None)):
    """Stripe redirects here if the onboarding link expires — we generate a fresh one."""
    if not item_id:
        return RedirectResponse(_APP_URL)
    try:
        item_uuid = uuid.UUID(item_id)
    except ValueError:
        return RedirectResponse(_APP_URL)

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT stripe_connect_account_id FROM items WHERE id = %s AND type = 'finder'",
                    (str(item_uuid),),
                )
                row = cur.fetchone()

        if row is None or not row["stripe_connect_account_id"]:
            return RedirectResponse(_APP_URL)

        account_link = stripe.AccountLink.create(
            account=row["stripe_connect_account_id"],
            refresh_url=f"{_RAILWAY_URL}/connect/refresh?item_id={item_id}",
            return_url=f"{_RAILWAY_URL}/connect/return?item_id={item_id}",
            type="account_onboarding",
        )
        return RedirectResponse(account_link.url)
    except Exception:
        return RedirectResponse(_APP_URL)


@app.post("/handoff/validate")
def validate_handoff_token(body: HandoffValidateRequest):
    try:
        payload = decode_handoff_token(body.token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Handoff token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid handoff token")

    jti = payload["jti"]
    item_id = payload["sub"]
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO used_tokens (jti, item_id, used_at, expires_at)
                VALUES (%s, %s, now(), %s)
                ON CONFLICT (jti) DO NOTHING
                RETURNING jti
                """,
                (jti, item_id, expires_at),
            )
            inserted = cur.fetchone()
        conn.commit()

    if inserted is None:
        raise HTTPException(status_code=409, detail="Handoff token has already been used")

    return {"valid": True, "item_id": item_id}
