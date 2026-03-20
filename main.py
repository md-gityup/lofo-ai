from fastapi import FastAPI, Form, HTTPException, File, UploadFile, Request, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, Response
from pydantic import BaseModel, field_validator
import os
import re
from typing import Optional
from datetime import datetime, timezone, timedelta
import math
import uuid
import asyncio
import base64
import json

import io

import anthropic
import voyageai
import cohere
import pillow_heif
import stripe
from PIL import Image

from database import get_connection, ANTHROPIC_API_KEY, VOYAGE_API_KEY
import jwt

from security import create_handoff_token, decode_handoff_token, hash_secret, verify_secret

claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)

_COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
_cohere_client = cohere.Client(api_key=_COHERE_API_KEY) if _COHERE_API_KEY else None
if not _COHERE_API_KEY:
    print("[LOFO] COHERE_API_KEY not set — reranker disabled, using cosine-only fallback")

_STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
_STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
stripe.api_key = _STRIPE_SECRET_KEY

_TWILIO_ACCOUNT_SID  = os.getenv("TWILIO_ACCOUNT_SID", "")
_TWILIO_AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN", "")
_TWILIO_VERIFY_SID   = os.getenv("TWILIO_VERIFY_SID", "")
_TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

_CRON_SECRET = os.getenv("CRON_SECRET", "")

# Resend — school notifications (optional)
_RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
_RESEND_FROM = os.getenv("RESEND_FROM", "LOFO <onboarding@resend.dev>")
_SCHOOL_DEFAULT_NOTIFY_EMAIL = os.getenv("SCHOOL_DEFAULT_NOTIFY_EMAIL", "")
_LOFO_APP_STORE_URL = os.getenv(
    "LOFO_APP_STORE_URL",
    "https://apps.apple.com/app/lofo/id0000000000",
)

# APNs push notifications (iOS Phase F)
# Set these in Railway env vars to enable push alongside SMS.
# APNS_AUTH_KEY: full content of the .p8 file downloaded from Apple Developer Portal → Keys
# APNS_ENVIRONMENT: "production" (default) or "sandbox" (for Simulator / dev testing)
_APNS_KEY_ID    = os.getenv("APNS_KEY_ID", "")
_APNS_TEAM_ID   = os.getenv("APNS_TEAM_ID", "")
_APNS_AUTH_KEY  = os.getenv("APNS_AUTH_KEY", "")   # PEM string, newlines as \n
_APNS_BUNDLE_ID = os.getenv("APNS_BUNDLE_ID", "ai.lofo.app")
_APNS_HOST = (
    "api.sandbox.push.apple.com"
    if os.getenv("APNS_ENVIRONMENT", "production") == "sandbox"
    else "api.push.apple.com"
)

_twilio_client = None
if _TWILIO_ACCOUNT_SID and _TWILIO_AUTH_TOKEN:
    from twilio.rest import Client as TwilioClient
    _twilio_client = TwilioClient(_TWILIO_ACCOUNT_SID, _TWILIO_AUTH_TOKEN)

# Supabase Storage — prefer explicit SUPABASE_URL env var; fall back to
# parsing the project ref from DATABASE_URL (handles both pooler and direct formats)
_SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
_SUPABASE_URL = os.getenv("SUPABASE_URL", "")
if not _SUPABASE_URL:
    _db_url_str = os.getenv("DATABASE_URL", "")
    # Pooler format:  postgres.{ref}.pooler.supabase.com
    # Direct format:  db.{ref}.supabase.co
    _proj_match = re.search(r"postgres\.([a-z0-9]+)\.", _db_url_str) or \
                  re.search(r"db\.([a-z0-9]+)\.supabase", _db_url_str)
    if _proj_match:
        _SUPABASE_URL = f"https://{_proj_match.group(1)}.supabase.co"
_SUPABASE_STORAGE_BASE = f"{_SUPABASE_URL}/storage/v1" if _SUPABASE_URL else ""
_PHOTO_BUCKET = "item-photos"

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
      AND 1 - (l.embedding <=> f.embedding) >= 0.78
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
      AND 1 - (f.embedding <=> l.embedding) >= 0.78
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


def _get_device_tokens(phone: str) -> list:
    """Return all APNs device tokens registered for the given E.164 phone number."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT device_token FROM device_tokens WHERE phone = %s AND platform = 'ios'",
                    (phone,),
                )
                rows = cur.fetchall()
        return [row["device_token"] for row in rows]
    except Exception as exc:
        print(f"[LOFO APNs token lookup] {exc}")
        return []


def _push_apns(device_token: str, title: str, body: str, screen: str = "") -> None:
    """Send an APNs push notification. Non-blocking — failures are swallowed.

    Requires Railway env vars: APNS_KEY_ID, APNS_TEAM_ID, APNS_AUTH_KEY, APNS_BUNDLE_ID.
    APNS_AUTH_KEY must be the full .p8 file contents (with header/footer, newlines as \\n).
    APNS_ENVIRONMENT defaults to 'production'; set to 'sandbox' for Simulator testing.
    """
    if not (_APNS_KEY_ID and _APNS_TEAM_ID and _APNS_AUTH_KEY and _APNS_BUNDLE_ID):
        print(f"[LOFO APNs] Not configured — skipping push: {title}")
        return
    try:
        import time
        auth_token = jwt.encode(
            {"iss": _APNS_TEAM_ID, "iat": int(time.time())},
            _APNS_AUTH_KEY,
            algorithm="ES256",
            headers={"kid": _APNS_KEY_ID},
        )
        payload: dict = {
            "aps": {
                "alert": {"title": title, "body": body},
                "sound": "default",
            }
        }
        if screen:
            payload["screen"] = screen

        with httpx.Client(http2=True, timeout=10.0) as client:
            resp = client.post(
                f"https://{_APNS_HOST}/3/device/{device_token}",
                json=payload,
                headers={
                    "Authorization": f"bearer {auth_token}",
                    "apns-topic": _APNS_BUNDLE_ID,
                    "apns-push-type": "alert",
                    "apns-priority": "10",
                },
            )
            if resp.status_code != 200:
                print(f"[LOFO APNs] Delivery failed ({resp.status_code}): {resp.text[:200]}")
    except Exception as exc:
        print(f"[LOFO APNs error] {device_token[:8]}...: {exc}")


def _notify_waiting_losers(finder_item_id: uuid.UUID, finder_item_type: str) -> None:
    """After a finder item is saved, SMS + push any waiting losers whose item matches."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(_NOTIFY_LOSER_SQL, (str(finder_item_id),))
                rows = cur.fetchall()
        for row in rows:
            label = row["item_type"] or finder_item_type
            phone = row["phone"]
            sms_body = (
                f"LOFO: Your {label} may have been found nearby! "
                f"Open the app to claim it: {_APP_URL}"
            )
            _sms(phone, sms_body)
            for token in _get_device_tokens(phone):
                _push_apns(
                    token,
                    title="LOFO — possible match found",
                    body=f"Your {label} may have been found nearby. Tap to claim it.",
                    screen="waiting",
                )
    except Exception as exc:
        print(f"[LOFO notify-losers error] {exc}")


def _notify_matched_finder(loser_item_id: uuid.UUID, loser_item_type: str) -> None:
    """After a loser item is saved and a match exists, SMS + push the finder."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(_NOTIFY_FINDER_SQL, (str(loser_item_id),))
                rows = cur.fetchall()
        for row in rows:
            label = row["item_type"] or loser_item_type
            phone = row["phone"]
            sms_body = (
                f"LOFO: Someone is looking for a {label} you found! "
                f"They'll go through the app to verify ownership. "
                f"Check it out: {_APP_URL}"
            )
            _sms(phone, sms_body)
            for token in _get_device_tokens(phone):
                _push_apns(
                    token,
                    title="LOFO — someone's looking",
                    body=f"Someone is looking for a {label} you found. They'll verify ownership in the app.",
                    screen="finder",
                )
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
    'If the description mentions a specific place, extract it as "location" (human-readable name) and also '
    'provide your best estimate of "latitude" and "longitude" as decimal numbers using your world knowledge — '
    'be as precise as possible (e.g. a specific sports field, terminal, or street corner, not just the city). '
    'Respond ONLY with valid JSON matching this exact schema, no other text: '
    '{"item_type": "string", "color": ["array of colors"], "material": "string or null", '
    '"size": "small/medium/large or null", "features": ["array of distinguishing features"], '
    '"location": "string or null", "latitude": "number or null", "longitude": "number or null"}'
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


@app.get("/stats/public")
def public_stats():
    """Weekly reunion count — public, no auth required."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) AS c FROM reunions
                    WHERE created_at >= NOW() - INTERVAL '7 days'
                """)
                count = cur.fetchone()['c']
        return {"reunions_this_week": count}
    except Exception:
        return {"reunions_this_week": 0}

@app.get("/health", include_in_schema=False)
def health_check():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
    except Exception as e:
        return {"status": "degraded", "db": str(e)}
    return {"status": "ok"}


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
    where_description: Optional[str] = None   # free-text location for geocoding (loser flow)
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
    photo_url: Optional[str] = None


class TextItemResponse(ItemResponse):
    """Extended response for /items/from-text — adds location_name extracted by Claude."""
    location_name: Optional[str] = None


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
    photo_url: Optional[str] = None


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


class AttributesUpdate(BaseModel):
    item_type: Optional[str] = None
    color: Optional[list[str]] = None
    material: Optional[str] = None
    size: Optional[str] = None
    features: Optional[list[str]] = None


class RedescribeRequest(BaseModel):
    item_type: str
    details: list[str]


class CoordinateRequest(BaseModel):
    finder_item_id: uuid.UUID
    loser_item_id: uuid.UUID
    loser_phone: str
    self_outreach: bool = False  # true = loser will reach out themselves; finder still notified


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


class DeviceRegisterRequest(BaseModel):
    phone: str
    device_token: str
    platform: str = "ios"


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #

def _build_embedding_text(profile: dict) -> str:
    """
    Build the text sent to Voyage AI for embedding.

    Comma-separated attribute format with item_type as the first token.

    item_type leads the list to anchor retrieval recall — without it, a "blue knit glove"
    and a "blue knit beanie" have near-identical embeddings, flooding the retrieval pool
    with wrong-type items and pushing real matches out of LIMIT 50.
    item_type is NOT repeated (unlike the old sentence format) so it gets one token's
    weight rather than dominating. The hard gate in match_item() handles precision —
    any cross-type false positives that still score high get removed before scoring.

    Example output: "glove, small, blue, white, wool, knit, souvenir text, winter pattern"
    This string is never stored or shown to users.
    """
    parts: list[str] = []

    item_type = (profile.get("item_type") or "").strip()
    size      = (profile.get("size") or "").strip()
    colors    = [c.strip() for c in (profile.get("color") or []) if c.strip()]
    material  = (profile.get("material") or "").strip()
    features  = [f.strip() for f in (profile.get("features") or []) if f.strip()]

    if item_type:
        parts.append(item_type)
    if size:
        parts.append(size)
    parts.extend(colors)
    if material:
        parts.append(material)
    parts.extend(features)

    return ", ".join(parts)


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
    INSERT INTO items (type, item_type, color, material, size, features, latitude, longitude, secret_detail, school_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        (secret_detail IS NOT NULL) AS has_secret,
        photo_url
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
        created_at::text,
        photo_url
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
        f.photo_url,
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
      AND f.school_id IS NULL
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
    LIMIT 50
"""

# School-scoped retrieval: only finder items at the same school as the loser.
_MATCH_SQL_SCHOOL = """
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
        f.photo_url,
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
      AND l.school_id IS NOT NULL
      AND f.school_id IS NOT NULL
      AND l.school_id = %s::uuid
      AND f.school_id = %s::uuid
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
    LIMIT 50
"""


def _geocode(location_text: str) -> Optional[tuple[float, float]]:
    """
    Geocode a free-text location string via Nominatim (OpenStreetMap, no API key).
    Retries up to 3 times by progressively dropping leading terms so that
    "Beach Chalet Soccer Fields, Golden Gate Park" falls back to
    "Golden Gate Park" and then "Golden Gate Park, San Francisco" style queries.
    Returns (latitude, longitude) or None on failure / no result.
    """
    import httpx

    terms = [t.strip() for t in location_text.replace(",", " ").split() if t.strip()]
    queries: list[str] = [location_text]
    # Build fallback queries by dropping leading words (max 2 fallbacks)
    for drop in range(1, min(3, len(terms))):
        queries.append(" ".join(terms[drop:]))

    for query in queries:
        try:
            resp = httpx.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query, "format": "json", "limit": 1},
                headers={"User-Agent": "LOFO-AI/1.0 (lost-and-found-app)"},
                timeout=4.0,
            )
            resp.raise_for_status()
            results = resp.json()
            if results:
                print(f"[LOFO geocode] '{query}' → {results[0]['lat']}, {results[0]['lon']}")
                return float(results[0]["lat"]), float(results[0]["lon"])
        except Exception as exc:
            print(f"[LOFO geocode] '{query}' failed: {exc}")

    print(f"[LOFO geocode] no result for '{location_text}' after fallbacks")
    return None


async def _upload_photo(item_id: uuid.UUID, image_bytes: bytes) -> Optional[str]:
    """Upload a JPEG to Supabase Storage; return public URL or None on failure."""
    if not (_SUPABASE_STORAGE_BASE and _SUPABASE_SERVICE_ROLE_KEY):
        print("[LOFO photo] Supabase Storage not configured — skipping upload")
        return None
    path = f"{item_id}.jpg"
    upload_url = f"{_SUPABASE_STORAGE_BASE}/object/{_PHOTO_BUCKET}/{path}"
    headers = {
        "Authorization": f"Bearer {_SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "image/jpeg",
        "x-upsert": "true",
    }
    try:
        import httpx
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(upload_url, content=image_bytes, headers=headers)
            resp.raise_for_status()
        return f"{_SUPABASE_STORAGE_BASE}/object/public/{_PHOTO_BUCKET}/{path}"
    except Exception as exc:
        print(f"[LOFO photo upload error] {exc}")
        return None


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
                 item.latitude, item.longitude, item.secret_detail, None),
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


@app.post("/items/from-text", response_model=TextItemResponse, status_code=201)
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

    # Resolve coordinates: priority order —
    #   1. Explicit where_description field (geocoded via Nominatim)
    #   2. Claude's own lat/lng from its world knowledge (most precise for named places)
    #   3. Nominatim fallback on Claude's location string
    #   4. Device GPS (body.latitude / body.longitude)
    stored_lat = body.latitude
    stored_lng = body.longitude
    resolved_location_name = None

    if body.where_description:
        resolved_location_name = body.where_description
        if body.latitude is not None and body.longitude is not None:
            # Precise coords already provided (e.g. map pin-drop) — use them directly.
            # Skip Nominatim so the pin's exact coordinates are preserved.
            stored_lat, stored_lng = body.latitude, body.longitude
            print(f"[LOFO geocode] pin coords for '{body.where_description}' → {stored_lat:.4f}, {stored_lng:.4f}")
        else:
            coords = _geocode(body.where_description)
            if coords:
                stored_lat, stored_lng = coords
                print(f"[LOFO geocode] explicit '{body.where_description}' → {stored_lat:.4f}, {stored_lng:.4f}")
    elif extracted.get("location"):
        resolved_location_name = extracted["location"]
        # Try Claude's own coordinates first — far more precise for specific landmarks
        claude_lat = extracted.get("latitude")
        claude_lng = extracted.get("longitude")
        if claude_lat is not None and claude_lng is not None:
            try:
                stored_lat, stored_lng = float(claude_lat), float(claude_lng)
                print(f"[LOFO geocode] Claude coords for '{resolved_location_name}' → {stored_lat:.4f}, {stored_lng:.4f}")
            except (TypeError, ValueError):
                pass
        # Fall back to Nominatim if Claude didn't return valid coords
        if stored_lat is None or stored_lng is None:
            coords = _geocode(resolved_location_name)
            if coords:
                stored_lat, stored_lng = coords

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
                    stored_lat,
                    stored_lng,
                    stored_secret,
                    None,
                ),
            )
            row = cur.fetchone()
        conn.commit()

    item = dict(row)
    item["location_name"] = resolved_location_name
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

    # Run sync Claude SDK in a thread so it doesn't block the uvicorn event loop.
    try:
        message = await asyncio.to_thread(
            claude_client.messages.create,
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
                    None,
                ),
            )
            row = cur.fetchone()
        conn.commit()

    item = dict(row)
    # Run sync Voyage embedding in a thread (same reason as Claude above).
    await asyncio.to_thread(_store_embedding, item["id"], extracted)

    # Upload the photo and persist the public URL
    photo_url = await _upload_photo(item["id"], image_bytes)
    if photo_url:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE items SET photo_url = %s WHERE id = %s",
                    (photo_url, str(item["id"])),
                )
            conn.commit()
        item["photo_url"] = photo_url

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
                """SELECT embedding, item_type, color, material, size, features
                   FROM items WHERE id = %s AND type = 'loser'""",
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

    return _run_match_stages(dict(loser_row), [dict(r) for r in rows])


_ITEM_TYPE_SYNONYMS: list[set[str]] = [
    {"glove", "gloves", "mitten", "mittens"},
    {"hat", "beanie", "cap", "knit hat", "winter hat", "bonnet", "toque", "beret"},
    {"scarf", "scarves", "wrap", "shawl"},
    {"shoe", "shoes", "boot", "boots", "sneaker", "sneakers", "loafer", "loafers", "heel", "heels", "sandal", "sandals"},
    {"bag", "purse", "handbag", "clutch", "tote", "satchel"},
    {"backpack", "bookbag", "rucksack", "daypack"},
    {"wallet", "billfold", "card holder", "cardholder"},
    {"key", "keys", "keychain", "keyring", "key fob"},
    {"phone", "smartphone", "iphone", "android", "cell phone", "mobile"},
    {"glasses", "sunglasses", "eyeglasses", "spectacles", "shades"},
    {"headphones", "earphones", "earbuds", "airpods", "earphones"},
    {"watch", "wristwatch", "smartwatch"},
    {"ring", "wedding ring", "engagement ring", "band"},
    {"necklace", "chain", "pendant"},
    {"bracelet", "bangle", "wristband"},
    {"jacket", "coat", "parka", "puffer", "fleece", "windbreaker"},
    {"umbrella", "brolly"},
    {"luggage", "suitcase", "duffel", "duffle", "travel bag"},
    {"toy", "stuffed animal", "plush", "stuffed toy", "plushie"},
    {"laptop", "computer", "macbook", "notebook"},
    {"tablet", "ipad"},
    {"camera", "dslr", "mirrorless"},
]


def _item_types_compatible(type_a: str, type_b: str) -> bool:
    """
    Returns True if two item_type strings refer to the same kind of object.
    Allows: exact match, containment ("glove" in "winter glove"), or shared synonym group.
    If types are clearly different categories, returns False — the caller should
    exclude the candidate entirely (hard gate), not raise a threshold.
    """
    a = type_a.lower().strip()
    b = type_b.lower().strip()
    if a == b:
        return True
    # Containment: "winter glove" contains "glove"
    if a in b or b in a:
        return True
    # Shared synonym group
    for group in _ITEM_TYPE_SYNONYMS:
        a_match = any(a == s or a in s or s in a for s in group)
        b_match = any(b == s or b in s or s in b for s in group)
        if a_match and b_match:
            return True
    return False


_COLOR_GROUPS: list[set[str]] = [
    {"red", "crimson", "scarlet", "maroon", "burgundy", "rose", "pink", "coral", "salmon", "magenta"},
    {"orange", "amber", "rust", "peach", "apricot", "copper", "bronze", "terracotta"},
    {"yellow", "gold", "lemon", "cream", "beige", "tan", "khaki", "mustard"},
    {"green", "olive", "lime", "sage", "mint", "teal", "emerald", "forest", "hunter", "chartreuse"},
    {"blue", "navy", "cobalt", "sky", "azure", "cerulean", "royal", "indigo", "denim", "midnight", "dark blue", "slate blue"},
    {"purple", "violet", "lavender", "plum", "mauve", "lilac"},
    {"brown", "chocolate", "espresso", "mocha", "chestnut", "caramel", "leather", "walnut"},
    {"white", "ivory", "cream", "off-white", "eggshell"},
    {"black", "jet", "ebony", "onyx", "charcoal"},
    {"gray", "grey", "silver", "graphite", "stone", "ash"},
]
_NEUTRAL_GROUPS: set[int] = {7, 8, 9}  # white/black/gray groups — neutrals can pair with anything
_COLOR_GROUP_NAMES = ["red", "orange", "yellow", "green", "blue", "purple", "brown", "white", "black", "gray"]


def _color_group(color: str) -> int | None:
    """Return the index of the color group this color belongs to, or None."""
    c = color.lower().strip()
    for i, group in enumerate(_COLOR_GROUPS):
        if c in group or any(g in c or c in g for g in group):
            return i
    return None


def _colors_compatible(loser_colors: list[str], finder_colors: list[str]) -> bool:
    """
    Returns True if the color sets are compatible — i.e., at least one color on each
    side maps to the same color group, OR at least one side consists entirely of
    neutral colors (black/white/gray/silver) which pair with anything.
    """
    loser_groups  = {g for c in loser_colors  if (g := _color_group(c)) is not None}
    finder_groups = {g for c in finder_colors if (g := _color_group(c)) is not None}

    # If either side has no recognized colors, allow the match (don't penalise unknown colors)
    if not loser_groups or not finder_groups:
        return True

    # If either side is entirely neutral colors, allow the match
    if loser_groups <= _NEUTRAL_GROUPS or finder_groups <= _NEUTRAL_GROUPS:
        return True

    # Otherwise require at least one group in common
    return bool(loser_groups & finder_groups)


_SIDE_TOKENS_LEFT  = {"left", "l", "left hand", "left foot", "left ear"}
_SIDE_TOKENS_RIGHT = {"right", "r", "right hand", "right foot", "right ear"}
_SIDED_ITEM_TYPES  = {"glove", "gloves", "mitten", "mittens", "shoe", "shoes",
                      "boot", "boots", "sneaker", "sneakers", "earbud", "earbuds",
                      "earphone", "earphones", "airpod", "airpods", "earring", "earrings"}


def _extract_side(features: list[str]) -> Optional[str]:
    """Return 'left', 'right', or None from a feature list."""
    tokens = {f.lower().strip() for f in features}
    for t in tokens:
        if t in _SIDE_TOKENS_LEFT or any(s in t for s in ("left",)):
            return "left"
        if t in _SIDE_TOKENS_RIGHT or any(s in t for s in ("right",)):
            return "right"
    return None


def _sides_compatible(loser_features: list[str], finder_features: list[str]) -> bool:
    """
    Hard block only when both sides explicitly state conflicting sides (left vs right).
    Returns True (compatible) when either side is silent about sidedness.
    """
    loser_side  = _extract_side(loser_features)
    finder_side = _extract_side(finder_features)
    if loser_side is None or finder_side is None:
        return True
    return loser_side == finder_side


def _color_score(loser_colors: list[str], finder_colors: list[str]) -> float:
    """
    Convert color compatibility to a 0–1 signal for composite scoring.
      1.0 — both sides have colors and share a color group (positive signal)
      0.5 — one or both sides have no color info (absence of data, not a mismatch)
      0.0 — both sides have colors but share no group (confirmed incompatible)
    """
    if not loser_colors or not finder_colors:
        return 0.5

    loser_groups  = {g for c in loser_colors  if (g := _color_group(c)) is not None}
    finder_groups = {g for c in finder_colors if (g := _color_group(c)) is not None}

    if not loser_groups or not finder_groups:
        return 0.5

    if loser_groups & finder_groups:
        return 1.0

    # If either side is entirely neutral, it can pair with anything — neutral signal
    if loser_groups <= _NEUTRAL_GROUPS or finder_groups <= _NEUTRAL_GROUPS:
        return 0.5

    return 0.0


def _feature_overlap(loser_features: list[str], finder_features: list[str]) -> float:
    """
    Jaccard similarity over lowercased feature tokens.
    Returns 0.0 when either side has no features (absence of data, not a mismatch).
    """
    a = {f.lower().strip() for f in loser_features  if f.strip()}
    b = {f.lower().strip() for f in finder_features if f.strip()}
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _query_richness(loser_attributes: dict) -> str:
    """
    Classifies how much information the loser provided.
    Drives dynamic final_score threshold — sparse queries get more lenient thresholds
    because the reranker has less to work with.
    """
    filled = sum(
        1 for v in loser_attributes.values()
        if v and (not isinstance(v, list) or len(v) > 0)
    )
    if filled <= 2:
        return "sparse"
    elif filled <= 5:
        return "medium"
    return "rich"


def _build_rerank_text(
    item_type: str,
    colors: list[str],
    material: str,
    size: str,
    features: list[str],
) -> str:
    """
    Structured attribute string for Cohere Rerank input.
    Format: "type=glove; colors=blue,white; material=wool; size=small; features=souvenir text,winter pattern"
    Only includes non-empty fields so the reranker doesn't see blank slots as signal.
    """
    parts: list[str] = []
    if item_type:
        parts.append(f"type={item_type.strip()}")
    if colors:
        parts.append(f"colors={','.join(c.strip() for c in colors if c.strip())}")
    if material and material.strip():
        parts.append(f"material={material.strip()}")
    if size and size.strip():
        parts.append(f"size={size.strip()}")
    if features:
        clean = [f.strip() for f in features if f.strip()]
        if clean:
            parts.append(f"features={','.join(clean)}")
    return "; ".join(parts)


_RERANK_THRESHOLDS: dict[str, float] = {
    "sparse": 0.30,
    "medium": 0.40,
    "rich":   0.55,
}


def _run_match_stages(loser_row: dict, rows: list[dict]) -> list[dict]:
    """
    Stages A–E: hard filters, Cohere rerank (or cosine fallback), composite score.
    Shared by POST /match and school-scoped matching.
    """
    if not loser_row.get("embedding"):
        return []

    loser_item_type = (loser_row["item_type"] or "").strip()
    loser_colors = [c.lower() for c in (loser_row["color"] or [])]
    loser_features = [f.lower() for f in (loser_row["features"] or [])]
    loser_attrs = {
        "item_type": loser_row["item_type"],
        "color": loser_row["color"],
        "material": loser_row["material"],
        "size": loser_row["size"],
        "features": loser_row["features"],
    }

    candidates: list[dict] = []
    for r in rows:
        finder_item_type = (r.get("item_type") or "").strip()
        if not _item_types_compatible(loser_item_type, finder_item_type):
            continue
        finder_colors = [c.lower() for c in (r["color"] or [])]
        if not _colors_compatible(loser_colors, finder_colors):
            continue
        finder_features = [f.lower() for f in (r["features"] or [])]
        if not _sides_compatible(loser_features, finder_features):
            continue
        candidates.append(dict(r))

    if not candidates:
        return []

    richness = _query_richness(loser_attrs)
    threshold = _RERANK_THRESHOLDS[richness]

    reranker_scores = [0.0] * len(candidates)
    cohere_ok = False

    if _cohere_client:
        try:
            query_doc = _build_rerank_text(
                loser_item_type,
                loser_colors,
                loser_row["material"] or "",
                loser_row["size"] or "",
                loser_row["features"] or [],
            )
            documents = [
                _build_rerank_text(
                    c.get("item_type") or "",
                    [col.lower() for col in (c.get("color") or [])],
                    c.get("material") or "",
                    c.get("size") or "",
                    c.get("features") or [],
                )
                for c in candidates
            ]
            rerank_result = _cohere_client.rerank(
                model="rerank-english-v3.0",
                query=query_doc,
                documents=documents,
                return_documents=False,
            )
            for result in rerank_result.results:
                reranker_scores[result.index] = result.relevance_score
            cohere_ok = True
            print(f"[LOFO rerank] OK — {len(candidates)} candidates, top score={max(reranker_scores):.3f}, richness={richness}")
        except Exception as exc:
            print(f"[LOFO rerank] Cohere error: {exc} — falling back to cosine-only")

    if cohere_ok:
        scored: list[tuple[float, dict]] = []
        for i, c in enumerate(candidates):
            cosine = float(c["similarity_score"])
            reranker = reranker_scores[i]
            f_colors = [col.lower() for col in (c.get("color") or [])]
            f_feats = [f.lower() for f in (c.get("features") or [])]
            c_score = _color_score(loser_colors, f_colors)
            f_score = _feature_overlap(loser_features, f_feats)
            dist = c.get("distance_miles")
            proximity_mult = (1.0 + 0.12 * max(0.0, 1.0 - float(dist) / 10.0)) if dist is not None else 1.0
            final = (0.55 * reranker + 0.20 * cosine + 0.15 * c_score + 0.10 * f_score) * proximity_mult
            if final < threshold:
                continue
            c["similarity_score"] = round(final, 4)
            scored.append((final, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[:5]]

    cosine_thresholds = {"sparse": 0.58, "medium": 0.62, "rich": 0.68}
    floor = cosine_thresholds[richness]
    results = [c for c in candidates if float(c["similarity_score"]) >= floor]
    results.sort(key=lambda x: float(x["similarity_score"]), reverse=True)
    print(f"[LOFO rerank] cosine-only fallback — floor={floor}, richness={richness}, results={len(results)}")
    return results[:5]


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
        try:
            updates["phone"] = _normalize_phone(body.phone)
        except HTTPException:
            updates["phone"] = body.phone  # store as-is if already E.164
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
    phone = _normalize_phone(body.phone)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET phone = %s WHERE id = %s AND type = 'loser' RETURNING id",
                (phone, str(item_id)),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Loser item not found")
    return {"ok": True}


@app.patch("/items/{item_id}/attributes", status_code=200)
def update_item_attributes(item_id: uuid.UUID, body: AttributesUpdate):
    """
    Update structured attributes on any item and re-embed so the corrected profile
    is immediately used for matching. Works for both finder and loser items.
    """
    updates: dict = {}
    if body.item_type is not None:
        updates["item_type"] = body.item_type.strip()
    if body.color is not None:
        updates["color"] = [c.strip().lower() for c in body.color if c.strip()]
    if body.material is not None:
        updates["material"] = body.material.strip() or None
    if body.size is not None:
        updates["size"] = body.size.strip() or None
    if body.features is not None:
        updates["features"] = [f.strip() for f in body.features if f.strip()]

    if not updates:
        return {"ok": True}

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [str(item_id)]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE items SET {set_clause} WHERE id = %s "
                f"RETURNING id, item_type, color, material, size, features",
                values,
            )
            row = cur.fetchone()
        conn.commit()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    profile = {
        "item_type": row["item_type"],
        "color": row["color"] or [],
        "material": row["material"],
        "size": row["size"],
        "features": row["features"] or [],
    }
    _store_embedding(item_id, profile)

    return {
        "ok": True,
        "item_type": row["item_type"],
        "color": row["color"],
        "material": row["material"],
        "size": row["size"],
        "features": row["features"],
    }


@app.patch("/items/{item_id}/redescribe", status_code=200)
def redescribe_item(item_id: uuid.UUID, body: RedescribeRequest):
    """
    Re-parse a free-text item description through Claude so user edits are
    intelligently mapped to structured columns (color, material, size, features)
    instead of being stored verbatim.
    """
    description = f"Item type: {body.item_type}. Details: {', '.join(body.details)}"
    user_message = f"Re-classify this lost/found item from the user's description: {description}"

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

    updates = {
        "item_type": extracted["item_type"],
        "color": extracted.get("color", []),
        "material": extracted.get("material"),
        "size": extracted.get("size"),
        "features": extracted.get("features", []),
    }
    set_clause = ", ".join(f"{k} = %s" for k in updates)
    values = list(updates.values()) + [str(item_id)]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE items SET {set_clause} WHERE id = %s "
                f"RETURNING id, item_type, color, material, size, features",
                values,
            )
            row = cur.fetchone()
        conn.commit()

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    _store_embedding(item_id, extracted)

    return {
        "ok": True,
        "item_type": row["item_type"],
        "color": row["color"],
        "material": row["material"],
        "size": row["size"],
        "features": row["features"],
    }


@app.post("/handoff/coordinate", status_code=200)
def coordinate_handoff(body: CoordinateRequest):
    """
    Called after loser confirms ownership (both "Connect us" and "I'll reach out" paths).
    Saves the loser's phone, creates a reunion relay record, and fires confirmation
    SMS to both parties. Neither party's real number is shared — they reply to
    LOFO's number and POST /sms/inbound relays the messages between them.
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
    raw_finder_phone = finder["phone"]

    # Normalize the finder's stored phone (stored from OTP flow, may not be E.164 yet)
    finder_phone: str | None = None
    if raw_finder_phone:
        try:
            finder_phone = _normalize_phone(raw_finder_phone)
        except HTTPException:
            finder_phone = raw_finder_phone  # use as-is if already normalized

    if finder_phone:
        # Duplicate guard — skip INSERT if an active reunion for this pair already exists
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id FROM reunions
                    WHERE finder_item_id = %s
                      AND loser_item_id  = %s
                      AND status = 'active'
                      AND expires_at > NOW()
                    LIMIT 1
                    """,
                    (str(body.finder_item_id), str(body.loser_item_id)),
                )
                existing = cur.fetchone()

        if not existing:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO reunions (finder_item_id, loser_item_id, finder_phone, loser_phone)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (str(body.finder_item_id), str(body.loser_item_id), finder_phone, loser_phone),
                    )
                conn.commit()

            # Notify both parties — no raw numbers shared, relay via LOFO's number
            resolve_link = f"{_RAILWAY_URL}/resolve/{body.loser_item_id}"
            if body.self_outreach:
                _sms(
                    loser_phone,
                    f"LOFO: Your {label} is confirmed! "
                    f"The finder has been notified and is expecting your message. "
                    f"Once you've got it back, close the report (and tip if you'd like): {resolve_link}"
                )
                _sms(
                    finder_phone,
                    f"LOFO: The owner of the {label} you found has been verified! "
                    f"They'll be reaching out directly to arrange pickup."
                )
            else:
                _sms(
                    loser_phone,
                    f"LOFO: Your {label} is confirmed! "
                    f"Reply here to message the finder — we'll relay it securely. "
                    f"Once you've got it back, close the report (and tip if you'd like): {resolve_link}"
                )
                _sms(
                    finder_phone,
                    f"LOFO: Great news — the owner of the {label} you found has been verified and is ready to connect! "
                    f"Reply to this number to message them — we'll relay it securely."
                )
    else:
        # Finder has no phone on file — be honest with the loser
        _sms(
            loser_phone,
            f"LOFO: Your {label} is confirmed! "
            f"The finder didn't leave a number, but they may still have the item. "
            f"Check back in the app — we'll notify you if they make contact."
        )

    return {"ok": True}


@app.post("/sms/inbound", include_in_schema=False)
async def sms_inbound(request: Request):
    """
    Twilio inbound SMS webhook.
    When either party in an active reunion replies to LOFO's number, this endpoint
    forwards the message to the other party — acting as a secure relay so neither
    person ever sees the other's real phone number.

    Configure in Twilio console:
      Phone Numbers → your number → Messaging → Webhook URL:
      https://lofo-ai-production.up.railway.app/sms/inbound  (HTTP POST)
    """
    form        = await request.form()
    from_number = (form.get("From") or "").strip()
    body_text   = (form.get("Body") or "").strip()

    _EMPTY_TWIML = '<?xml version="1.0" encoding="UTF-8"?><Response/>'

    if not (from_number and body_text):
        return Response(content=_EMPTY_TWIML, media_type="text/xml")

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT finder_phone, loser_phone
                    FROM reunions
                    WHERE status = 'active'
                      AND expires_at > NOW()
                      AND (finder_phone = %s OR loser_phone = %s)
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (from_number, from_number),
                )
                row = cur.fetchone()

        if row:
            if from_number == row["loser_phone"]:
                _sms(row["finder_phone"], f"[Owner via LOFO] {body_text}\n\nReply to respond.")
            elif from_number == row["finder_phone"]:
                _sms(row["loser_phone"], f"[Finder via LOFO] {body_text}\n\nReply to respond.")
        else:
            # No active reunion found — send a gentle nudge
            _sms(from_number, "LOFO: No active reunion found for your number. Open the app to get started.")

    except Exception as exc:
        print(f"[LOFO inbound relay error] {exc}")

    return Response(content=_EMPTY_TWIML, media_type="text/xml")


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


@app.post("/devices/register", status_code=200)
def register_device(body: DeviceRegisterRequest):
    """
    Register an APNs device token paired with a verified phone number.

    Called by the iOS app after successful OTP verification. Upserts a row in
    device_tokens so push notifications can be sent to this device alongside SMS.

    DB migration required (run once in Supabase SQL editor):
        CREATE TABLE IF NOT EXISTS device_tokens (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            phone VARCHAR NOT NULL,
            device_token TEXT NOT NULL,
            platform VARCHAR NOT NULL DEFAULT 'ios',
            created_at TIMESTAMPTZ DEFAULT NOW(),
            UNIQUE(phone, device_token)
        );
    """
    phone = _normalize_phone(body.phone)
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO device_tokens (phone, device_token, platform)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (phone, device_token) DO NOTHING
                    """,
                    (phone, body.device_token, body.platform),
                )
                conn.commit()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not register device: {exc}") from exc
    return {"ok": True}


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


# --------------------------------------------------------------------------- #
# LOFO for Schools                                                             #
# --------------------------------------------------------------------------- #

_SCHOOL_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def _jwt_secret_for_tokens() -> str:
    return os.getenv("JWT_SECRET", "dev-secret")


def _require_valid_school_slug(slug: str) -> None:
    if not slug or not _SCHOOL_SLUG_RE.match(slug):
        raise HTTPException(status_code=404, detail="Not found")


def _get_school_public(slug: str) -> dict:
    """id, slug, name, pickup_info, admin_notify_email (email ok for admin use only)."""
    _require_valid_school_slug(slug)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, slug, name, pickup_info, admin_notify_email
                FROM schools WHERE slug = %s
                """,
                (slug,),
            )
            row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="School not found")
    return dict(row)


def _get_school_with_hash(slug: str) -> dict:
    _require_valid_school_slug(slug)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, slug, name, pickup_info, admin_notify_email, admin_passcode_hash
                FROM schools WHERE slug = %s
                """,
                (slug,),
            )
            row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="School not found")
    return dict(row)


def _require_school_admin(slug: str, authorization: Optional[str]) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="School admin authentication required")
    token = authorization[7:].strip()
    try:
        payload = jwt.decode(token, _jwt_secret_for_tokens(), algorithms=["HS256"])
        if payload.get("role") != "school_admin":
            raise HTTPException(status_code=403, detail="Not a school admin token")
        if payload.get("slug") != slug:
            raise HTTPException(status_code=403, detail="Token not valid for this school")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired — please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")


def _create_school_admin_token(school_id: str, slug: str) -> str:
    payload = {
        "role": "school_admin",
        "school_id": school_id,
        "slug": slug,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, _jwt_secret_for_tokens(), algorithm="HS256")


def _school_page_url(slug: str) -> str:
    return f"https://lofoapp.com/school/{slug}"


def _school_email_html(school_name: str, body_html: str, slug: str = "") -> str:
    """Shared HTML wrapper for all school transactional emails."""
    school_url = _school_page_url(slug) if slug else "https://lofoapp.com"
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{school_name}</title></head>
<body style="margin:0;padding:0;background:#F5F2EC;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;">
  <div style="max-width:520px;margin:0 auto;padding:32px 16px 56px;">
    <div style="background:#1A1A2E;border-radius:12px 12px 0 0;padding:24px 28px 20px;">
      <div style="font-size:10px;font-weight:700;letter-spacing:0.28em;text-transform:uppercase;color:#C17A4A;">LOFO</div>
      <div style="font-size:12px;color:rgba(255,255,255,0.42);margin-top:3px;">{school_name} &middot; Lost &amp; Found</div>
    </div>
    <div style="background:#ffffff;border:1px solid #E0DBD1;border-top:none;border-radius:0 0 12px 12px;padding:32px 28px 28px;color:#1A1A2E;line-height:1.65;">
      {body_html}
    </div>
    <p style="text-align:center;margin:20px 0 0;font-size:11px;color:#9A9488;line-height:1.6;">
      <a href="{school_url}" style="color:#9A9488;text-decoration:none;">{school_name} Lost &amp; Found</a>
      &nbsp;&middot;&nbsp;
      <a href="https://lofoapp.com" style="color:#9A9488;text-decoration:none;">lofoapp.com</a>
    </p>
  </div>
</body></html>"""


def _email_cta_btn(label: str, url: str, color: str = "#C17A4A") -> str:
    return (
        f'<a href="{url}" style="display:inline-block;background:{color};color:#ffffff;'
        f'text-decoration:none;padding:12px 26px;border-radius:8px;font-size:14px;'
        f'font-weight:600;margin-top:20px;letter-spacing:-0.1px;">{label} &rarr;</a>'
    )


def _resend_send_html(to_list: list[str], subject: str, html: str) -> None:
    to_list = [e.strip() for e in to_list if e and e.strip()]
    if not to_list:
        return
    if not _RESEND_API_KEY:
        print(f"[LOFO school email] RESEND_API_KEY not set — skip: {subject}")
        return
    try:
        import resend

        resend.api_key = _RESEND_API_KEY
        resend.Emails.send(
            {
                "from": _RESEND_FROM,
                "to": to_list[:50],
                "subject": subject,
                "html": html,
            }
        )
    except Exception as exc:
        print(f"[LOFO school email] send error: {exc}")


def _school_match_internal(loser_id: uuid.UUID, school_id: uuid.UUID) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT embedding, item_type, color, material, size, features, school_id
                   FROM items WHERE id = %s AND type = 'loser'""",
                (str(loser_id),),
            )
            loser_row = cur.fetchone()
    if not loser_row or not loser_row.get("school_id"):
        return []
    if str(loser_row["school_id"]) != str(school_id):
        return []
    if loser_row["embedding"] is None:
        return []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _MATCH_SQL_SCHOOL,
                (str(loser_id), str(school_id), str(school_id)),
            )
            rows = cur.fetchall()
    return _run_match_stages(dict(loser_row), [dict(r) for r in rows])


def _school_match_reasons(m: dict) -> list[str]:
    reasons: list[str] = []
    it = (m.get("item_type") or "").strip()
    if it:
        reasons.append(f"Looks like a {it}")
    sc = m.get("similarity_score")
    if sc is not None:
        try:
            reasons.append(f"AI confidence {int(round(float(sc) * 100))}%")
        except (TypeError, ValueError):
            pass
    cols = m.get("color") or []
    if cols:
        reasons.append("Colors: " + ", ".join(str(c) for c in cols))
    fts = m.get("features") or []
    if fts:
        reasons.append("Details: " + ", ".join(str(f) for f in fts[:3]))
    return reasons


def _school_notify_subscribers_new_item(school: dict, item: dict, extracted: dict) -> None:
    sid = str(school["id"])
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT email FROM school_subscriptions WHERE school_id = %s",
                (sid,),
            )
            rows = cur.fetchall()
    emails = [r["email"] for r in rows]
    if not emails:
        return
    slug = school.get("slug", "")
    label = (extracted.get("item_type") or "item").capitalize()
    colors = extracted.get("color") or []
    color_str = (", ".join(str(c) for c in colors)).capitalize() if colors else ""
    photo = item.get("photo_url") or ""
    school_url = _school_page_url(slug)

    photo_block = (
        f'<p><img src="{photo}" alt="{label}" style="max-width:100%;border-radius:10px;'
        f'display:block;margin:20px 0 4px;border:1px solid #E0DBD1;"/></p>'
        if photo else ""
    )
    desc_line = f"{label}{' · ' + color_str if color_str else ''}"
    body = f"""
      <p style="font-size:15px;margin:0 0 6px;font-weight:600;">{desc_line}</p>
      <p style="font-size:14px;color:#9A9488;margin:0 0 16px;">Just posted to the {school["name"]} lost &amp; found.</p>
      {photo_block}
      <p style="font-size:14px;margin:16px 0 0;">Recognize it? Browse the full gallery and submit a claim.</p>
      {_email_cta_btn("View found items", school_url)}
    """
    _resend_send_html(
        emails,
        f"New found item — {school['name']}",
        _school_email_html(school["name"], body, slug),
    )


def _school_notify_claim_admin(school: dict, claim: dict, item: dict) -> None:
    to_addr = (school.get("admin_notify_email") or "").strip() or _SCHOOL_DEFAULT_NOTIFY_EMAIL
    if not to_addr:
        print("[LOFO school] No admin_notify_email — skip claim notification")
        return
    slug = school.get("slug", "")
    item_label = (item.get("item_type") or "item").capitalize()
    child = claim.get("child_name") or "—"
    parent_name = claim.get("parent_name") or "—"
    parent_email = claim.get("parent_email") or "—"
    note = claim.get("claim_note") or "—"
    school_url = _school_page_url(slug)

    row_style = "padding:8px 0;border-bottom:1px solid #F0EDE6;font-size:14px;"
    label_style = "color:#9A9488;font-size:11px;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;display:block;margin-bottom:2px;"
    body = f"""
      <p style="font-size:15px;font-weight:600;margin:0 0 20px;">A parent submitted a claim on <em>{item_label}</em>.</p>
      <table style="width:100%;border-collapse:collapse;">
        <tr><td style="{row_style}"><span style="{label_style}">Child</span>{child}</td></tr>
        <tr><td style="{row_style}"><span style="{label_style}">Parent</span>{parent_name}</td></tr>
        <tr><td style="{row_style}"><span style="{label_style}">Parent email</span>
          <a href="mailto:{parent_email}" style="color:#C17A4A;text-decoration:none;">{parent_email}</a></td></tr>
        <tr><td style="padding:8px 0;font-size:14px;"><span style="{label_style}">Note</span>{note}</td></tr>
      </table>
      {_email_cta_btn("Open admin dashboard", school_url, "#1A1A2E")}
    """
    _resend_send_html(
        [to_addr],
        f"Claim submitted — {item_label} · {school['name']}",
        _school_email_html(school["name"], body, slug),
    )


def _school_notify_parent_possible_match(
    school: dict,
    pending: dict,
    finder_item: dict,
    score: float,
) -> None:
    slug = school.get("slug", "")
    child = pending.get("child_name") or "your child"
    pct = int(round(float(score) * 100))
    label = (finder_item.get("item_type") or "item").capitalize()
    photo = finder_item.get("photo_url") or ""
    school_url = _school_page_url(slug)

    photo_block = (
        f'<p><img src="{photo}" alt="{label}" style="max-width:100%;border-radius:10px;'
        f'display:block;margin:20px 0 4px;border:1px solid #E0DBD1;"/></p>'
        if photo else ""
    )
    body = f"""
      <p style="font-size:15px;font-weight:600;margin:0 0 8px;">We found a possible match for {child}.</p>
      <p style="font-size:14px;color:#9A9488;margin:0 0 16px;">
        Something new was just posted at <strong style="color:#1A1A2E;">{school["name"]}</strong>
        that looks like a <strong style="color:#1A1A2E;">{label}</strong>
        — AI confidence <strong style="color:#1A1A2E;">{pct}%</strong>.
      </p>
      {photo_block}
      <p style="font-size:14px;margin:16px 0 0;">Open the lost &amp; found page to view the item and submit a claim if it's yours.</p>
      {_email_cta_btn("Check it out", school_url)}
    """
    _resend_send_html(
        [pending["parent_email"]],
        f"Possible match found — {school['name']}",
        _school_email_html(school["name"], body, slug),
    )


def _school_after_new_finder_post(school: dict, item: dict, extracted: dict) -> None:
    try:
        _school_notify_subscribers_new_item(school, item, extracted)
    except Exception as exc:
        print(f"[LOFO school] subscriber notify error: {exc}")
    school_id = uuid.UUID(str(school["id"]))
    new_finder_id = uuid.UUID(str(item["id"]))
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, loser_item_id, parent_email, parent_name, child_name
                    FROM school_lost_pending WHERE school_id = %s
                    """,
                    (str(school_id),),
                )
                pending_rows = cur.fetchall()
        for p in pending_rows:
            loser_id = uuid.UUID(str(p["loser_item_id"]))
            results = _school_match_internal(loser_id, school_id)
            for r in results:
                if uuid.UUID(str(r["id"])) == new_finder_id:
                    try:
                        _school_notify_parent_possible_match(school, dict(p), item, float(r["similarity_score"]))
                    except Exception as exc:
                        print(f"[LOFO school] parent match email error: {exc}")
                    with get_connection() as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                "DELETE FROM school_lost_pending WHERE id = %s",
                                (str(p["id"]),),
                            )
                        conn.commit()
                    break
    except Exception as exc:
        print(f"[LOFO school] pending match scan error: {exc}")


class SchoolAdminLoginRequest(BaseModel):
    passcode: str


class SchoolSettingsPatch(BaseModel):
    pickup_info: Optional[str] = None
    admin_notify_email: Optional[str] = None


class SchoolSubscribeRequest(BaseModel):
    email: str
    parent_name: Optional[str] = None


class SchoolClaimRequest(BaseModel):
    item_id: uuid.UUID
    child_name: str
    parent_name: str
    parent_email: str
    claim_note: Optional[str] = None


class SchoolLostRequest(BaseModel):
    description: str
    parent_email: Optional[str] = None
    parent_name: Optional[str] = None
    child_name: Optional[str] = None


@app.get("/school/{slug}", include_in_schema=False)
def serve_school_page(slug: str):
    _get_school_public(slug)
    return FileResponse(os.path.join(os.path.dirname(__file__), "school.html"))


@app.get("/school/{slug}/data")
def school_public_data(slug: str):
    school = _get_school_public(slug)
    return {
        "slug": school["slug"],
        "name": school["name"],
        "pickup_info": school["pickup_info"] or "",
        "app_store_url": _LOFO_APP_STORE_URL,
    }


@app.get("/school/{slug}/items")
def school_list_items(slug: str, page: int = 1, search: str = ""):
    school = _get_school_public(slug)
    limit = 30
    offset = (max(1, page) - 1) * limit
    pat = f"%{search.strip()}%" if search.strip() else None
    with get_connection() as conn:
        with conn.cursor() as cur:
            if pat:
                cur.execute(
                    """
                    SELECT id, item_type, color, material, size, features, photo_url, created_at::text
                    FROM items
                    WHERE school_id = %s AND type = 'finder' AND status = 'active'
                      AND item_type ILIKE %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (str(school["id"]), pat, limit, offset),
                )
            else:
                cur.execute(
                    """
                    SELECT id, item_type, color, material, size, features, photo_url, created_at::text
                    FROM items
                    WHERE school_id = %s AND type = 'finder' AND status = 'active'
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    (str(school["id"]), limit, offset),
                )
            rows = cur.fetchall()
    return {"items": [dict(r) for r in rows]}


@app.get("/school/{slug}/admin/items")
def school_admin_items(slug: str, request: Request):
    _require_school_admin(slug, request.headers.get("Authorization"))
    school = _get_school_public(slug)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT i.id, i.item_type, i.color, i.material, i.size, i.features,
                       i.photo_url, i.created_at::text, i.status,
                       (SELECT COUNT(*)::int FROM school_claims sc
                        WHERE sc.item_id = i.id AND sc.status = 'pending') AS pending_claims
                FROM items i
                WHERE i.school_id = %s AND i.type = 'finder'
                ORDER BY i.created_at DESC
                LIMIT 200
                """,
                (str(school["id"]),),
            )
            rows = cur.fetchall()
    return {"items": [dict(r) for r in rows]}


@app.post("/school/{slug}/admin/login")
def school_admin_login(slug: str, body: SchoolAdminLoginRequest):
    row = _get_school_with_hash(slug)
    ph = row.get("admin_passcode_hash") or ""
    if not ph or not verify_secret(body.passcode, ph):
        raise HTTPException(status_code=401, detail="Invalid passcode")
    token = _create_school_admin_token(str(row["id"]), slug)
    return {"token": token, "slug": slug}


@app.patch("/school/{slug}/settings")
def school_patch_settings(slug: str, body: SchoolSettingsPatch, request: Request):
    _require_school_admin(slug, request.headers.get("Authorization"))
    school = _get_school_public(slug)
    updates: list[str] = []
    params: list = []
    if body.pickup_info is not None:
        updates.append("pickup_info = %s")
        params.append(body.pickup_info)
    if body.admin_notify_email is not None:
        updates.append("admin_notify_email = %s")
        params.append(body.admin_notify_email.strip() or None)
    if not updates:
        return {"ok": True}
    params.append(str(school["id"]))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE schools SET {', '.join(updates)} WHERE id = %s",
                params,
            )
        conn.commit()
    return {"ok": True}


@app.post("/school/{slug}/subscribe", status_code=201)
def school_subscribe(slug: str, body: SchoolSubscribeRequest):
    school = _get_school_public(slug)
    email = body.email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=422, detail="Valid email required")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO school_subscriptions (school_id, email, parent_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (school_id, email) DO UPDATE SET parent_name = EXCLUDED.parent_name
                """,
                (str(school["id"]), email, body.parent_name),
            )
        conn.commit()
    return {"ok": True}


@app.post("/school/{slug}/claim", status_code=201)
def school_claim(slug: str, body: SchoolClaimRequest, request: Request):
    school = _get_school_public(slug)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, item_type, school_id FROM items
                WHERE id = %s AND type = 'finder' AND status = 'active'
                """,
                (str(body.item_id),),
            )
            item_row = cur.fetchone()
    if not item_row or str(item_row.get("school_id")) != str(school["id"]):
        raise HTTPException(status_code=404, detail="Item not found at this school")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO school_claims
                    (item_id, school_id, child_name, parent_name, parent_email, claim_note)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    str(body.item_id),
                    str(school["id"]),
                    body.child_name.strip(),
                    body.parent_name.strip(),
                    body.parent_email.strip().lower(),
                    (body.claim_note or "").strip() or None,
                ),
            )
            cur.fetchone()
        conn.commit()
    claim_dict = {
        "child_name": body.child_name,
        "parent_name": body.parent_name,
        "parent_email": body.parent_email,
        "claim_note": body.claim_note,
    }
    try:
        _school_notify_claim_admin(school, claim_dict, dict(item_row))
    except Exception as exc:
        print(f"[LOFO school] claim email error: {exc}")
    return {"ok": True}


@app.post("/school/{slug}/lost")
def school_lost_match(slug: str, body: SchoolLostRequest):
    school = _get_school_public(slug)
    desc = body.description.strip()
    if len(desc) < 3:
        raise HTTPException(status_code=422, detail="Please describe the item")

    user_message = f"Extract item information from this description: {desc}"
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

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _INSERT_SQL,
                (
                    "loser",
                    extracted["item_type"],
                    extracted["color"],
                    extracted.get("material"),
                    extracted.get("size"),
                    extracted.get("features", []),
                    None,
                    None,
                    None,
                    str(school["id"]),
                ),
            )
            row = cur.fetchone()
        conn.commit()

    item = dict(row)
    _store_embedding(item["id"], extracted)

    matches_raw = _school_match_internal(uuid.UUID(str(item["id"])), uuid.UUID(str(school["id"])))
    matches_out: list[dict] = []
    for m in matches_raw[:5]:
        d = dict(m)
        d["match_reasons"] = _school_match_reasons(d)
        # JSON-serializable ids
        d["id"] = str(d["id"])
        matches_out.append(d)

    pending_watch = False
    if not matches_out and body.parent_email and body.parent_email.strip():
        email = body.parent_email.strip().lower()
        if "@" in email:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO school_lost_pending
                            (school_id, parent_email, parent_name, child_name, loser_item_id)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            str(school["id"]),
                            email,
                            (body.parent_name or "").strip() or None,
                            (body.child_name or "").strip() or None,
                            str(item["id"]),
                        ),
                    )
                conn.commit()
            pending_watch = True
            slug = school.get("slug", "")
            school_url = _school_page_url(slug)
            _watch_body = f"""
              <p style="font-size:15px;font-weight:600;margin:0 0 8px;">We're on the lookout.</p>
              <p style="font-size:14px;color:#9A9488;margin:0 0 16px;">
                No close match in the {school["name"]} lost &amp; found right now — but we'll
                email you the moment something similar is posted.
              </p>
              <p style="font-size:14px;margin:0 0 4px;">In the meantime, you can browse everything that's been found so far.</p>
              {_email_cta_btn("Browse found items", school_url)}
            """
            _resend_send_html(
                [email],
                f"We're watching for a match — {school['name']}",
                _school_email_html(school["name"], _watch_body, slug),
            )
    elif not matches_out:
        # No match and no watch email — remove orphan loser row
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM items WHERE id = %s", (str(item["id"]),))
            conn.commit()
        return {
            "loser_item_id": None,
            "matches": [],
            "pending_watch": False,
            "extracted_summary": {
                "item_type": extracted.get("item_type"),
                "color": extracted.get("color"),
            },
        }

    return {
        "loser_item_id": str(item["id"]),
        "matches": matches_out,
        "pending_watch": pending_watch,
        "extracted_summary": {
            "item_type": extracted.get("item_type"),
            "color": extracted.get("color"),
        },
    }


@app.post("/school/{slug}/items/from-photo", status_code=201)
async def school_create_from_photo(
    slug: str,
    request: Request,
    file: UploadFile = File(...),
):
    _require_school_admin(slug, request.headers.get("Authorization"))
    school = _get_school_public(slug)

    media_type = file.content_type or "image/jpeg"
    if media_type not in _SUPPORTED_MEDIA_TYPES | _HEIC_MEDIA_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported media type '{media_type}'.",
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
        message = await asyncio.to_thread(
            claude_client.messages.create,
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

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _INSERT_SQL,
                (
                    "finder",
                    extracted["item_type"],
                    extracted["color"],
                    extracted.get("material"),
                    extracted.get("size"),
                    extracted.get("features", []),
                    None,
                    None,
                    None,
                    str(school["id"]),
                ),
            )
            row = cur.fetchone()
        conn.commit()

    item = dict(row)
    await asyncio.to_thread(_store_embedding, item["id"], extracted)

    photo_url = await _upload_photo(item["id"], image_bytes)
    if photo_url:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE items SET photo_url = %s WHERE id = %s",
                    (photo_url, str(item["id"])),
                )
            conn.commit()
        item["photo_url"] = photo_url

    _school_after_new_finder_post(school, item, extracted)
    return item


# --------------------------------------------------------------------------- #
# Admin / Ops Dashboard                                                        #
# --------------------------------------------------------------------------- #

# Parse ADMIN_USERS env var: JSON dict of {"username": "password"}
_ADMIN_USERS: dict = {}
try:
    _ADMIN_USERS = json.loads(os.getenv("ADMIN_USERS", "{}"))
except Exception as _e:
    print(f"[LOFO admin] ADMIN_USERS parse error: {_e}")


def _create_admin_token(username: str) -> str:
    payload = {
        "sub": username,
        "role": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET", "dev-secret"), algorithm="HS256")


def _verify_admin(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Admin authentication required")
    token = auth[7:]
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET", "dev-secret"), algorithms=["HS256"])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not an admin token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired — please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")


def _admin_period_filter(period: str, col: str = "created_at") -> str:
    """Return a safe SQL snippet for time-range filtering. period is validated before call."""
    if period == "today":
        return f"AND {col} > NOW() - INTERVAL '24 hours'"
    elif period == "week":
        return f"AND {col} > NOW() - INTERVAL '7 days'"
    elif period == "month":
        return f"AND {col} > NOW() - INTERVAL '30 days'"
    return ""


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminDebugMatchRequest(BaseModel):
    item_a_id: uuid.UUID
    item_b_id: uuid.UUID


@app.get("/terms", include_in_schema=False)
def serve_terms():
    return FileResponse(os.path.join(os.path.dirname(__file__), "terms.html"))


@app.get("/privacy", include_in_schema=False)
def serve_privacy():
    return FileResponse(os.path.join(os.path.dirname(__file__), "privacy-policy.html"))


_STATS_BY_ITEMS_MAX_IDS = 100


@app.get("/stats/by-items", include_in_schema=False)
def stats_by_items(ids: str = Query("")):
    """User-level stats — counts for items the user has created (passed as comma-separated UUIDs)."""
    id_list = [x.strip().lower() for x in ids.split(",") if x.strip()][:_STATS_BY_ITEMS_MAX_IDS]
    if not id_list:
        return {"lost_count": 0, "found_count": 0, "reunited_count": 0}

    placeholders = ",".join("%s" for _ in id_list)
    params = id_list + id_list + id_list + id_list
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    (SELECT COUNT(*) FROM items WHERE id::text IN ({placeholders}) AND type='loser'  AND status='active') AS lost_count,
                    (SELECT COUNT(*) FROM items WHERE id::text IN ({placeholders}) AND type='finder' AND status='active') AS found_count,
                    (SELECT COUNT(*) FROM reunions WHERE finder_item_id::text IN ({placeholders}) OR loser_item_id::text IN ({placeholders})) AS reunited_count
            """, params)
            row = cur.fetchone()
    return dict(row)


@app.get("/admin", include_in_schema=False)
def serve_admin():
    return FileResponse(os.path.join(os.path.dirname(__file__), "admin.html"))


@app.get("/map", include_in_schema=False)
def serve_map():
    return FileResponse(os.path.join(os.path.dirname(__file__), "map.html"))


@app.get("/admin/map-pins", include_in_schema=False)
def admin_map_pins(period: str = "all", admin=Depends(_verify_admin)):
    """Return active items with GPS coords for map display, filtered by period."""
    period = period if period in ("today", "week", "month", "all") else "all"
    pf = _admin_period_filter(period)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    id, type, item_type, color, material, size, features,
                    latitude, longitude, status, created_at::text, photo_url,
                    (phone IS NOT NULL) AS has_phone
                FROM items
                WHERE status = 'active'
                  AND latitude IS NOT NULL
                  AND longitude IS NOT NULL
                  {pf}
                ORDER BY created_at DESC
            """)
            gps_rows = cur.fetchall()
            cur.execute(f"""
                SELECT COUNT(*) AS cnt FROM items
                WHERE status='active' AND (latitude IS NULL OR longitude IS NULL) {pf}
            """)
            no_gps = cur.fetchone()["cnt"]
    return {"pins": [dict(r) for r in gps_rows], "no_gps_count": int(no_gps)}


@app.get("/admin/map-pairs", include_in_schema=False)
def admin_map_pairs(period: str = "all", admin=Depends(_verify_admin)):
    """Return reunion pairs where both items have GPS, for drawing match lines on the map."""
    period = period if period in ("today", "week", "month", "all") else "all"
    pf = _admin_period_filter(period, col="r.created_at")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    r.id::text               AS reunion_id,
                    fi.id::text              AS finder_item_id,
                    fi.item_type             AS finder_item_type,
                    fi.latitude              AS finder_lat,
                    fi.longitude             AS finder_lng,
                    li.id::text              AS loser_item_id,
                    li.item_type             AS loser_item_type,
                    li.latitude              AS loser_lat,
                    li.longitude             AS loser_lng,
                    r.status,
                    r.created_at::text
                FROM reunions r
                JOIN items fi ON fi.id = r.finder_item_id
                JOIN items li ON li.id = r.loser_item_id
                WHERE fi.latitude  IS NOT NULL AND fi.longitude  IS NOT NULL
                  AND li.latitude  IS NOT NULL AND li.longitude  IS NOT NULL
                  {pf}
                ORDER BY r.created_at DESC
                LIMIT 200
            """)
            rows = cur.fetchall()
    return [dict(r) for r in rows]


@app.post("/admin/login", include_in_schema=False)
def admin_login(body: AdminLoginRequest):
    expected = _ADMIN_USERS.get(body.username)
    if not expected or body.password != expected:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = _create_admin_token(body.username)
    return {"token": token, "username": body.username}


@app.get("/admin/stats", include_in_schema=False)
def admin_stats(period: str = "all", admin=Depends(_verify_admin)):
    period = period if period in ("today", "week", "month", "all") else "all"
    pf = _admin_period_filter(period)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    (SELECT COUNT(*) FROM items WHERE type='loser'  AND status='active' AND school_id IS NULL) AS active_lost,
                    (SELECT COUNT(*) FROM items WHERE type='finder' AND status='active' AND school_id IS NULL) AS active_found,
                    (SELECT COUNT(*) FROM reunions WHERE 1=1 {pf}) AS reunions,
                    (SELECT COALESCE(SUM(amount_cents), 0) FROM tips WHERE status='completed' {pf}) AS tips_cents,
                    (SELECT COUNT(*) FROM items
                     WHERE status='active' AND expires_at BETWEEN NOW() AND NOW() + INTERVAL '7 days') AS expiring_7d
            """)
            row = cur.fetchone()
    return dict(row)


@app.get("/admin/charts", include_in_schema=False)
def admin_charts(admin=Depends(_verify_admin)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    d::date AS day,
                    COALESCE(SUM(CASE WHEN i.type = 'loser' THEN 1 ELSE 0 END), 0)::int AS lost,
                    COALESCE(SUM(CASE WHEN i.type = 'finder' THEN 1 ELSE 0 END), 0)::int AS found
                FROM generate_series(
                    DATE_TRUNC('week', NOW()),
                    DATE_TRUNC('week', NOW()) + INTERVAL '6 days',
                    INTERVAL '1 day'
                ) d
                LEFT JOIN items i ON DATE_TRUNC('day', i.created_at) = d::date
                GROUP BY d ORDER BY d
            """)
            daily_rows = cur.fetchall()

            cur.execute("""
                SELECT COALESCE(AVG(EXTRACT(EPOCH FROM (r.created_at - li.created_at)) / 86400), 0) AS avg_days
                FROM reunions r JOIN items li ON li.id = r.loser_item_id
                WHERE r.created_at >= NOW() - INTERVAL '30 days'
            """)
            avg_current = float(cur.fetchone()["avg_days"])

            cur.execute("""
                SELECT COALESCE(AVG(EXTRACT(EPOCH FROM (r.created_at - li.created_at)) / 86400), 0) AS avg_days
                FROM reunions r JOIN items li ON li.id = r.loser_item_id
                WHERE r.created_at BETWEEN NOW() - INTERVAL '60 days' AND NOW() - INTERVAL '30 days'
            """)
            avg_prev = float(cur.fetchone()["avg_days"])

            cur.execute("""
                SELECT
                    DATE_TRUNC('week', r.created_at)::date AS week_start,
                    AVG(EXTRACT(EPOCH FROM (r.created_at - li.created_at)) / 86400) AS avg_days
                FROM reunions r JOIN items li ON li.id = r.loser_item_id
                WHERE r.created_at >= NOW() - INTERVAL '35 days'
                GROUP BY week_start ORDER BY week_start
            """)
            weekly_rows = cur.fetchall()

            cur.execute("SELECT COUNT(*) AS cnt FROM reunions WHERE status = 'active' AND expires_at > NOW()")
            active = int(cur.fetchone()["cnt"])

    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    daily_items = [
        {"day": day_names[i] if i < 7 else "?", "lost": int(r["lost"]), "found": int(r["found"])}
        for i, r in enumerate(daily_rows)
    ]
    reunion_weekly = [
        {"week": f"W{i+1}", "avg_days": round(float(r["avg_days"]), 1)}
        for i, r in enumerate(weekly_rows)
    ]
    avg_cur = round(avg_current, 1)
    avg_prv = round(avg_prev, 1)
    diff = round(avg_prv - avg_cur, 1) if avg_prv > 0 else 0

    return {
        "daily_items": daily_items,
        "reunion_avg_days": avg_cur if avg_current > 0 else None,
        "reunion_diff_vs_prev": diff,
        "active_matches": active,
        "reunion_weekly": reunion_weekly,
    }


@app.get("/admin/items", include_in_schema=False)
def admin_items(type: Optional[str] = None, period: str = "all", admin=Depends(_verify_admin)):
    period = period if period in ("today", "week", "month", "all") else "all"
    pf = _admin_period_filter(period)
    type_filter = "AND type = 'loser'" if type == "loser" else ("AND type = 'finder'" if type == "finder" else "")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    id, type, item_type, color, material, size, features,
                    latitude, longitude, status,
                    expires_at::text, created_at::text,
                    phone, finder_email,
                    finder_payout_app, finder_payout_handle,
                    photo_url,
                    (secret_detail IS NOT NULL) AS has_secret
                FROM items
                WHERE status != 'archived' {type_filter} {pf}
                ORDER BY created_at DESC
                LIMIT 200
            """)
            rows = cur.fetchall()
    return [dict(r) for r in rows]


@app.get("/admin/reunions", include_in_schema=False)
def admin_reunions(period: str = "all", admin=Depends(_verify_admin)):
    period = period if period in ("today", "week", "month", "all") else "all"
    pf = _admin_period_filter(period, col="r.created_at")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    r.id, r.finder_phone, r.loser_phone, r.status,
                    r.created_at::text, r.expires_at::text,
                    fi.item_type
                FROM reunions r
                LEFT JOIN items fi ON fi.id = r.finder_item_id
                WHERE 1=1 {pf}
                ORDER BY r.created_at DESC
                LIMIT 200
            """)
            rows = cur.fetchall()
    return [dict(r) for r in rows]


@app.get("/admin/tips", include_in_schema=False)
def admin_tips(period: str = "all", admin=Depends(_verify_admin)):
    period = period if period in ("today", "week", "month", "all") else "all"
    pf = _admin_period_filter(period, col="t.created_at")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT
                    t.id, t.finder_item_id::text, t.loser_item_id::text,
                    t.amount_cents, t.status, t.created_at::text,
                    fi.item_type AS finder_item_type,
                    li.item_type AS loser_item_type
                FROM tips t
                LEFT JOIN items fi ON fi.id = t.finder_item_id
                LEFT JOIN items li ON li.id = t.loser_item_id
                WHERE 1=1 {pf}
                ORDER BY t.created_at DESC
                LIMIT 200
            """)
            rows = cur.fetchall()
    return [dict(r) for r in rows]


@app.patch("/admin/items/{item_id}/archive", include_in_schema=False)
def admin_archive_item(item_id: uuid.UUID, admin=Depends(_verify_admin)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET status = 'archived' WHERE id = %s RETURNING id",
                (str(item_id),),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}


@app.patch("/admin/items/{item_id}/deactivate", include_in_schema=False)
def admin_deactivate_item(item_id: uuid.UUID, admin=Depends(_verify_admin)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET status = 'inactive' WHERE id = %s RETURNING id",
                (str(item_id),),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}


@app.patch("/admin/items/{item_id}/extend", include_in_schema=False)
def admin_extend_item(item_id: uuid.UUID, admin=Depends(_verify_admin)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET expires_at = expires_at + INTERVAL '30 days' WHERE id = %s RETURNING id, expires_at::text",
                (str(item_id),),
            )
            row = cur.fetchone()
        conn.commit()
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True, "expires_at": row["expires_at"]}


# --------------------------------------------------------------------------- #
# Resolve / Item Lifecycle                                                     #
# --------------------------------------------------------------------------- #

@app.get("/resolve/{loser_item_id}", include_in_schema=False)
def serve_resolve(loser_item_id: uuid.UUID):
    return FileResponse(os.path.join(os.path.dirname(__file__), "resolve.html"))


@app.get("/resolve/{loser_item_id}/data", include_in_schema=False)
def resolve_data(loser_item_id: uuid.UUID):
    """Return item and finder info needed by the resolve page."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT item_type, status FROM items WHERE id = %s AND type = 'loser'",
                (str(loser_item_id),),
            )
            loser = cur.fetchone()

    if loser is None:
        raise HTTPException(status_code=404, detail="Report not found")

    if loser["status"] != "active":
        return {
            "loser_item_type": loser["item_type"],
            "finder_item_id": None,
            "finder_item_type": None,
            "finder_payout_handle": None,
            "finder_payout_app": None,
            "already_closed": True,
        }

    # Look up reunion to find the matched finder item
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT r.finder_item_id,
                       i.item_type        AS finder_item_type,
                       i.finder_payout_handle,
                       i.finder_payout_app
                FROM reunions r
                JOIN items i ON i.id = r.finder_item_id
                WHERE r.loser_item_id = %s
                  AND r.status = 'active'
                ORDER BY r.created_at DESC
                LIMIT 1
                """,
                (str(loser_item_id),),
            )
            reunion = cur.fetchone()

    return {
        "loser_item_type":     loser["item_type"],
        "finder_item_id":      str(reunion["finder_item_id"]) if reunion else None,
        "finder_item_type":    reunion["finder_item_type"]    if reunion else None,
        "finder_payout_handle": reunion["finder_payout_handle"] if reunion else None,
        "finder_payout_app":   reunion["finder_payout_app"]   if reunion else None,
        "already_closed":      False,
    }


class ResolveConfirmRequest(BaseModel):
    tip_amount_cents: Optional[int] = 0


@app.post("/resolve/{loser_item_id}/confirm", include_in_schema=False)
def resolve_confirm(loser_item_id: uuid.UUID, body: ResolveConfirmRequest = ResolveConfirmRequest()):
    """Mark the loser item (and matched finder item via reunion) as inactive."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE items SET status = 'inactive' WHERE id = %s AND type = 'loser' RETURNING id",
                (str(loser_item_id),),
            )
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Report not found")
        conn.commit()

    # Close finder item and mark reunion resolved
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT finder_item_id FROM reunions
                WHERE loser_item_id = %s AND status = 'active'
                ORDER BY created_at DESC LIMIT 1
                """,
                (str(loser_item_id),),
            )
            reunion = cur.fetchone()

    if reunion:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE items SET status = 'inactive' WHERE id = %s",
                    (str(reunion["finder_item_id"]),),
                )
                cur.execute(
                    "UPDATE reunions SET status = 'closed' WHERE loser_item_id = %s AND status = 'active'",
                    (str(loser_item_id),),
                )
            conn.commit()

    return {"ok": True}


# --------------------------------------------------------------------------- #
# Lifecycle Cron                                                               #
# --------------------------------------------------------------------------- #

@app.get("/cron/lifecycle", include_in_schema=False)
def cron_lifecycle(key: str = Query("")):
    """
    Daily lifecycle notifications for unmatched loser items.

    Day 7  — warm encouragement SMS, no action required.
    Day 28 — auto-extend expires_at 30 days + SMS with resolve link.

    If a phone has multiple items hitting the same milestone on the same run,
    only the first is messaged — the rest are picked up on the next daily run.

    Triggered by GitHub Actions (schedule: daily). Key-protected via CRON_SECRET.
    """
    if not _CRON_SECRET or key != _CRON_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    phones_messaged: set[str] = set()
    sent_week1 = 0
    sent_week2 = 0
    skipped = 0

    # --- Week-1 candidates: created 6–9 days ago, not yet notified, no active reunion ---
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, phone, item_type
                FROM items
                WHERE type = 'loser'
                  AND status = 'active'
                  AND phone IS NOT NULL
                  AND notif_week1_at IS NULL
                  AND created_at BETWEEN NOW() - INTERVAL '9 days' AND NOW() - INTERVAL '6 days'
                  AND NOT EXISTS (
                      SELECT 1 FROM reunions
                      WHERE loser_item_id = items.id AND status = 'active'
                  )
                ORDER BY created_at ASC
            """)
            week1_items = cur.fetchall()

    for item in week1_items:
        phone = item["phone"]
        if phone in phones_messaged:
            skipped += 1
            continue
        phones_messaged.add(phone)

        label = item["item_type"] or "item"
        _sms(
            phone,
            f"LOFO: Still on it. Your {label} report is active and we're watching. "
            f"Good things take time — we'll reach out the moment something turns up."
        )

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE items SET notif_week1_at = NOW() WHERE id = %s",
                    (str(item["id"]),),
                )
            conn.commit()
        sent_week1 += 1

    # --- Week-2 candidates: created 27–31 days ago, not yet notified, no active reunion ---
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, phone, item_type
                FROM items
                WHERE type = 'loser'
                  AND status = 'active'
                  AND phone IS NOT NULL
                  AND notif_week2_at IS NULL
                  AND created_at BETWEEN NOW() - INTERVAL '31 days' AND NOW() - INTERVAL '27 days'
                  AND NOT EXISTS (
                      SELECT 1 FROM reunions
                      WHERE loser_item_id = items.id AND status = 'active'
                  )
                ORDER BY created_at ASC
            """)
            week2_items = cur.fetchall()

    for item in week2_items:
        phone = item["phone"]
        if phone in phones_messaged:
            skipped += 1
            continue
        phones_messaged.add(phone)

        label = item["item_type"] or "item"
        resolve_link = f"{_RAILWAY_URL}/resolve/{item['id']}"
        _sms(
            phone,
            f"LOFO: One month in on your {label} — still no match, but we've extended "
            f"your search automatically. Miracles happen. "
            f"Got it back another way? Close your report: {resolve_link}"
        )

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE items
                    SET notif_week2_at = NOW(),
                        expires_at     = expires_at + INTERVAL '30 days'
                    WHERE id = %s
                    """,
                    (str(item["id"]),),
                )
            conn.commit()
        sent_week2 += 1

    print(f"[LOFO cron] lifecycle: sent_week1={sent_week1} sent_week2={sent_week2} skipped_multi={skipped}")
    return {"ok": True, "sent_week1": sent_week1, "sent_week2": sent_week2, "skipped_multi_item": skipped}


def _debug_pair_analysis(
    similarity: Optional[float],
    a_colors: list[str],
    b_colors: list[str],
    a_lat: Optional[float], a_lng: Optional[float],
    b_lat: Optional[float], b_lng: Optional[float],
) -> dict:
    """Shared logic for computing match debug info between any two items."""
    def _color_detail(color: str) -> dict:
        idx = _color_group(color)
        return {"color": color, "group_index": idx,
                "group_name": _COLOR_GROUP_NAMES[idx] if idx is not None else "unrecognized"}

    a_color_groups = [_color_detail(c) for c in a_colors]
    b_color_groups = [_color_detail(c) for c in b_colors]
    colors_ok = _colors_compatible(a_colors, b_colors)

    distance_miles = None
    within_radius = True
    if all(x is not None for x in [a_lat, a_lng, b_lat, b_lng]):
        dlat = math.radians(b_lat - a_lat)
        dlon = math.radians(b_lng - a_lng)
        ha = (math.sin(dlat / 2) ** 2
              + math.cos(math.radians(a_lat)) * math.cos(math.radians(b_lat))
              * math.sin(dlon / 2) ** 2)
        distance_miles = round(3958.8 * 2 * math.asin(math.sqrt(ha)), 1)
        within_radius = distance_miles <= 10

    block_reasons = []
    if similarity is None:
        block_reasons.append("One or both items have no embedding yet")
    elif similarity < 0.40:
        # Note: the live match pipeline uses a composite final_score with dynamic
        # thresholds (0.30–0.55). This debug view shows raw cosine only — use the
        # near-miss analyzer + live /match endpoint to evaluate the full pipeline.
        gap = round(0.40 - similarity, 4)
        block_reasons.append(f"Cosine {similarity:.4f} below retrieval floor 0.40 (gap: {gap})")
    if not colors_ok:
        a_str = ", ".join(c["color"] for c in a_color_groups) or "none"
        b_str = ", ".join(c["color"] for c in b_color_groups) or "none"
        block_reasons.append(f"Color mismatch — A: [{a_str}] vs B: [{b_str}]")
    if not within_radius:
        block_reasons.append(f"Distance {distance_miles} mi exceeds 10-mile radius")

    return {
        "a_color_groups": a_color_groups,
        "b_color_groups": b_color_groups,
        "colors_compatible": colors_ok,
        "distance_miles": distance_miles,
        "within_radius": within_radius,
        "would_match": len(block_reasons) == 0,
        "block_reasons": block_reasons,
    }


@app.post("/admin/debug/match", include_in_schema=False)
def admin_debug_match(body: AdminDebugMatchRequest, admin=Depends(_verify_admin)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    a.id AS a_id, a.type AS a_type, a.item_type AS a_item_type,
                    a.color AS a_color, a.material AS a_material, a.size AS a_size,
                    a.features AS a_features, a.latitude AS a_lat, a.longitude AS a_lng,
                    a.status AS a_status,
                    b.id AS b_id, b.type AS b_type, b.item_type AS b_item_type,
                    b.color AS b_color, b.material AS b_material, b.size AS b_size,
                    b.features AS b_features, b.latitude AS b_lat, b.longitude AS b_lng,
                    b.status AS b_status,
                    CASE
                        WHEN a.embedding IS NOT NULL AND b.embedding IS NOT NULL
                        THEN ROUND(CAST(1 - (a.embedding <=> b.embedding) AS NUMERIC), 4)
                        ELSE NULL
                    END AS similarity_score
                FROM items a, items b
                WHERE a.id = %s AND b.id = %s
                """,
                (str(body.item_a_id), str(body.item_b_id)),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="One or both items not found")

    similarity = float(row["similarity_score"]) if row["similarity_score"] is not None else None
    a_colors = [c.lower() for c in (row["a_color"] or [])]
    b_colors = [c.lower() for c in (row["b_color"] or [])]
    analysis = _debug_pair_analysis(
        similarity, a_colors, b_colors,
        float(row["a_lat"]) if row["a_lat"] is not None else None,
        float(row["a_lng"]) if row["a_lng"] is not None else None,
        float(row["b_lat"]) if row["b_lat"] is not None else None,
        float(row["b_lng"]) if row["b_lng"] is not None else None,
    )

    return {
        "item_a": {
            "id": str(body.item_a_id), "type": row["a_type"], "item_type": row["a_item_type"],
            "color": row["a_color"], "material": row["a_material"], "size": row["a_size"],
            "features": row["a_features"], "status": row["a_status"],
            "latitude": row["a_lat"], "longitude": row["a_lng"],
        },
        "item_b": {
            "id": str(body.item_b_id), "type": row["b_type"], "item_type": row["b_item_type"],
            "color": row["b_color"], "material": row["b_material"], "size": row["b_size"],
            "features": row["b_features"], "status": row["b_status"],
            "latitude": row["b_lat"], "longitude": row["b_lng"],
        },
        "similarity_score": similarity,
        "would_pass_cosine_floor": similarity is not None and similarity >= 0.40,
        **analysis,
    }


class AdminNearMissRequest(BaseModel):
    item_id: uuid.UUID


@app.post("/admin/debug/near-misses", include_in_schema=False)
def admin_near_misses(body: AdminNearMissRequest, admin=Depends(_verify_admin)):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, type, item_type, color, material, size, features,
                          latitude, longitude, status, created_at::text, photo_url, embedding
                   FROM items WHERE id = %s""",
                (str(body.item_id),),
            )
            q = cur.fetchone()

    if q is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if q["embedding"] is None:
        raise HTTPException(status_code=422, detail="Item has no embedding — cannot run similarity search")

    opposite_type = "finder" if q["type"] == "loser" else "loser"
    q_lat = float(q["latitude"]) if q["latitude"] is not None else None
    q_lng = float(q["longitude"]) if q["longitude"] is not None else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.id, c.type, c.item_type, c.color, c.material, c.size, c.features,
                    c.status, c.created_at::text, c.photo_url,
                    c.latitude AS c_lat, c.longitude AS c_lng,
                    ROUND(CAST(1 - (c.embedding <=> q.embedding) AS NUMERIC), 4) AS similarity_score
                FROM items c
                CROSS JOIN items q
                WHERE q.id = %s
                  AND c.type = %s
                  AND c.status != 'archived'
                  AND c.embedding IS NOT NULL
                ORDER BY c.embedding <=> q.embedding
                LIMIT 10
                """,
                (str(body.item_id), opposite_type),
            )
            rows = cur.fetchall()

    q_colors = [c.lower() for c in (q["color"] or [])]
    candidates = []
    for r in rows:
        sim = float(r["similarity_score"]) if r["similarity_score"] is not None else None
        c_colors = [c.lower() for c in (r["color"] or [])]
        c_lat = float(r["c_lat"]) if r["c_lat"] is not None else None
        c_lng = float(r["c_lng"]) if r["c_lng"] is not None else None
        analysis = _debug_pair_analysis(sim, q_colors, c_colors, q_lat, q_lng, c_lat, c_lng)
        candidates.append({
            "id": str(r["id"]),
            "type": r["type"],
            "item_type": r["item_type"],
            "color": r["color"],
            "material": r["material"],
            "size": r["size"],
            "features": r["features"],
            "status": r["status"],
            "created_at": r["created_at"],
            "photo_url": r["photo_url"],
            "similarity_score": sim,
            **analysis,
        })

    return {
        "query_item": {
            "id": str(q["id"]), "type": q["type"], "item_type": q["item_type"],
            "color": q["color"], "material": q["material"], "size": q["size"],
            "features": q["features"], "status": q["status"],
            "latitude": q["latitude"], "longitude": q["longitude"],
        },
        "candidates": candidates,
        "total": len(candidates),
        "opposite_type": opposite_type,
    }


@app.post("/admin/reembed-all", include_in_schema=False)
def admin_reembed_all(admin=Depends(_verify_admin)):
    """
    Re-embeds all non-archived items using the current _build_embedding_text format.
    Use after changing the embedding text format to bring existing items in sync.
    Batches Voyage API calls in groups of 50 to stay within rate limits.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, item_type, color, material, size, features
                   FROM items WHERE status != 'archived' ORDER BY created_at DESC"""
            )
            rows = cur.fetchall()

    if not rows:
        return {"reembedded": 0, "skipped": 0}

    BATCH_SIZE = 50
    reembedded = 0
    skipped = 0

    for batch_start in range(0, len(rows), BATCH_SIZE):
        batch = rows[batch_start : batch_start + BATCH_SIZE]
        texts = []
        valid = []
        for r in batch:
            profile = {
                "item_type": r["item_type"],
                "color":     r["color"],
                "material":  r["material"],
                "size":      r["size"],
                "features":  r["features"],
            }
            text = _build_embedding_text(profile)
            if not text.strip():
                skipped += 1
                continue
            texts.append(text)
            valid.append(r)

        if not texts:
            continue

        try:
            result = voyage_client.embed(texts, model="voyage-3", input_type="document")
        except Exception as exc:
            print(f"[reembed-all] Voyage error on batch {batch_start}: {exc}")
            skipped += len(valid)
            continue

        with get_connection() as conn:
            with conn.cursor() as cur:
                for item, embedding in zip(valid, result.embeddings):
                    emb_str = "[" + ",".join(str(x) for x in embedding) + "]"
                    cur.execute(
                        "UPDATE items SET embedding = %s::vector WHERE id = %s",
                        (emb_str, str(item["id"])),
                    )
                    reembedded += 1
            conn.commit()

    print(f"[reembed-all] Done — {reembedded} re-embedded, {skipped} skipped")
    return {"reembedded": reembedded, "skipped": skipped}
