# LOFO.AI — Build Progress & Context
*Last updated: March 6, 2026 — Phases 1–9b complete and deployed*

---

## What LOFO.AI Is

A lost and found app built almost entirely by AI. Radically simple. A finder snaps a photo of something they found. A loser describes what they lost. AI matches them, verifies ownership, coordinates the return, and prompts a tip at the moment of reunion. Ten seconds of user effort. Everything else is the engine.

---

## Phase Roadmap

| Phase | Status | What it is |
|---|---|---|
| 1 — Foundation | ✅ Complete | FastAPI + Supabase PostgreSQL |
| 2 — AI Ingestion | ✅ Complete | Claude Vision + text → structured item profile + Voyage embeddings |
| 3 — Matching Engine | ✅ Complete | Cosine similarity matching with confidence scoring |
| 4 — Security | ✅ Complete | Argon2id secret hashing, JWT handoff tokens, brute-force lockout |
| 5 — UI Polish | ✅ Complete | 13-screen interactive prototype, iOS animations, Dynamic Island |
| 6 — API Wiring | ✅ Complete | All screens wired to real backend with live API calls |
| 7 — Tip Flow | ✅ Complete | Stripe inline card payment, finder email capture, tips table |
| 8 — GPS & Proximity | ✅ Complete | Real location capture, proximity-filtered matching |
| 8.5 — UX & Flow Fixes | ✅ Complete | Live clock, GPS pre-fetch, phone propagation, real distances, scroll fixes |
| 9a — Ownership Verification Rethink | ✅ Complete | Finder-owned secret detail; Claude fuzzy matching; loser flow friction removed |
| 9b — SMS Verification | ✅ Complete | Real OTP via Twilio, interactive digit inputs, demo buttons removed |
| 10 — Realtime Matching | ✅ Complete | 5s polling on Waiting screen; auto-navigates to Match on hit; 2-min timeout |
| **11 — Stripe Connect Payouts** | **← Next** | Finder bank account, direct tip transfers |

---

## What's Running

| Thing | URL |
|---|---|
| **Live API (Railway)** | `https://lofo-ai-production.up.railway.app` |
| **Live app (GitHub Pages)** | `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html` |
| **API docs** | `https://lofo-ai-production.up.railway.app/docs` |
| **Local API** | `http://localhost:8000` (only when uvicorn running) |
| **Database** | Supabase (PostgreSQL + pgvector) |
| **Project folder** | `~/Desktop/lofo-ai` |
| **Git repo** | `https://github.com/md-gityup/lofo-ai` |

---

## Backend Endpoints

| Endpoint | What it does |
|---|---|
| `GET /` | Serves LOFO_MVP.html |
| `POST /items` | Submit a structured item manually |
| `POST /items/from-photo` | Photo → Claude Vision → item profile + embedding; optional `secret_detail` Form field |
| `POST /items/from-text` | Text → Claude → item profile + embedding |
| `GET /items/{id}` | Retrieve item by UUID |
| `POST /match` | Cosine similarity + Haversine proximity match; returns `has_secret: bool` per result |
| `POST /verify` | Claude fuzzy-matches finder's `secret_detail` against loser's `loser_claim`; returns `{verified, reason}` |
| `POST /handoff/validate` | Validate single-use JWT handoff token |
| `PATCH /items/{id}/finder-info` | Save finder's `finder_email` and/or `secret_detail` after item creation |
| `POST /tip/create-payment-intent` | Create Stripe PaymentIntent, record pending tip |
| `POST /stripe/webhook` | Mark tip `completed` on `payment_intent.succeeded` |
| `POST /sms/send-otp` | Generate 4-digit code, store in-memory (10 min TTL), send via Twilio SMS |
| `POST /sms/verify-otp` | Validate submitted code; returns `{verified: bool, reason?}` |

---

## Database Schema

**Table: `items`**
| Column | Type | Notes |
|---|---|---|
| id | UUID | Auto-generated |
| type | varchar | `'finder'` or `'loser'` |
| item_type | varchar | e.g. `'handbag'` |
| color | text[] | e.g. `['brown']` |
| material | varchar | e.g. `'leather'` |
| size | varchar | `'small'` / `'medium'` / `'large'` |
| features | text[] | e.g. `['gold clasp']` |
| embedding | vector(1024) | Voyage AI — used for cosine matching |
| finder_email | varchar | Optional — finder's payout email (Phase 7) |
| latitude | numeric(9,6) | Optional — GPS latitude at submission (Phase 8) |
| longitude | numeric(9,6) | Optional — GPS longitude at submission (Phase 8) |
| secret_detail | text | Optional — finder's physical observation for ownership verify (Phase 9a) |
| status | varchar | Default `'active'` |
| expires_at | timestamptz | Default 30 days from creation |
| created_at | timestamptz | Auto-set |

**Table: `secret_verifications`** *(legacy — no longer written to since Phase 9a)*
Was used for Argon2id loser-owned secrets. Replaced by `secret_detail` on `items`. Table still exists on Supabase, just unused.

**Table: `used_tokens`**
| Column | Type | Notes |
|---|---|---|
| jti | varchar | JWT ID — unique, prevents replay |
| item_id | UUID | References items(id) |
| used_at | timestamptz | When token was first used |
| expires_at | timestamptz | Token expiry |

**Table: `tips`**
| Column | Type | Notes |
|---|---|---|
| id | UUID | Auto-generated |
| finder_item_id | UUID | References items(id) |
| loser_item_id | UUID | References items(id) |
| amount_cents | integer | e.g. `1000` = $10 |
| stripe_payment_intent_id | varchar | Stripe PI ID, unique |
| status | varchar | `'pending'` → `'completed'` via webhook |
| created_at | timestamptz | Auto-set |

---

## Key Files

| File | What it does |
|---|---|
| `main.py` | FastAPI app — all endpoints + CORS + serves HTML |
| `database.py` | Supabase connection pool + API key loading |
| `schema.sql` | PostgreSQL table definitions |
| `requirements.txt` | Python dependencies |
| `LOFO_MVP.html` | 13-screen app — all live API calls, Stripe.js, GPS |
| `security.py` | Argon2id hashing + JWT handoff token logic |
| `.env` | API keys — never share, never commit |

## Key Credentials

| Thing | Where |
|---|---|
| Supabase project | supabase.com → LOFO → LOFO-AI |
| Railway project | railway.app → lofo-ai |
| GitHub repo | github.com/md-gityup/lofo-ai |
| Stripe dashboard | dashboard.stripe.com |
| All API keys | `.env` on local machine only |

**Railway environment variables:** `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_VERIFY_SID`, `TWILIO_VERIFY_SID`

---

## Known Intentional Placeholders

| Artifact | Screen | Fix in |
|---|---|---|
| Finder payout (tips held in LOFO's Stripe balance) | — | Phase 11 |

---

## How to Run Locally

```bash
cd ~/Desktop/lofo-ai
source .venv/bin/activate
uvicorn main:app --reload
# open http://localhost:8000
```

## Seed Test Data

```bash
# 1. Submit a finder item (with optional secret detail)
curl -X POST https://lofo-ai-production.up.railway.app/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "finder", "description": "Found a brown leather wallet near the park fountain. Small, bifold, with a silver clasp.", "secret_detail": "There is a photo of a golden retriever inside the left pocket"}'

# 2. Submit a matching loser item (no secret needed anymore)
curl -X POST https://lofo-ai-production.up.railway.app/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "loser", "description": "Lost my brown leather wallet, bifold with silver clasp, near the fountain."}'

# 3. Run match (use loser item id from step 2)
curl -X POST https://lofo-ai-production.up.railway.app/match \
  -H "Content-Type: application/json" \
  -d '{"item_id": "<loser-item-id>"}'

# 4. Verify ownership (loser describes what they know; Claude judges)
curl -X POST https://lofo-ai-production.up.railway.app/verify \
  -H "Content-Type: application/json" \
  -d '{"finder_item_id": "<finder-item-id>", "loser_claim": "I have a photo of my dog inside"}'
```

**Stripe test card:** `4242 4242 4242 4242` · exp `12/26` · CVC `123` · any ZIP

---

## Session History

### Phase 10 — March 6, 2026

**What changed:** The loser waiting screen now polls for real matches instead of showing a fake simulate button.

**Frontend only:** `startPolling()` / `stopPolling()` / `pollForMatch()` added. `startPolling()` is called from `onScreenEnter('waiting')` — the existing screen lifecycle hook — so it fires automatically on every transition into the waiting screen. `pollForMatch()` runs every 5 seconds: calls `POST /match` with `state.loserItemId`, and on a hit stops the interval, sets `state.matchedItem`, fires a haptic pulse (`navigator.vibrate`), and navigates to `screen-match`. After 24 polls (~2 minutes) with no result, stops and shows a calm "Still scanning — we'll text you" message. `stopPolling()` is called from `onScreenEnter` for every non-waiting screen, so the interval is always cleaned up on navigation. "Simulate match found →" button removed entirely.

---

### Phase 9b — March 6, 2026

**What changed:** Fake SMS verify flow replaced with real Twilio OTP end-to-end.

**Backend:** Two new endpoints — `POST /sms/send-otp` and `POST /sms/verify-otp`. Originally used the basic Twilio messaging API; switched mid-session to **Twilio Verify** after discovering US carriers block unregistered senders (A2P 10DLC). Verify API routes through pre-registered infrastructure — no carrier filtering, no registration required. `_normalize_phone()` strips US formatting to E.164. `TWILIO_VERIFY_SID` env var added (Verify Service SID, `VA...`). `twilio` added to `requirements.txt`.

**Frontend:** `screen-verify` hardcoded `3 7 4 ·` divs replaced with **six** real `<input type="text" inputmode="numeric">` elements (Twilio Verify sends 6-digit codes by default). `initOtpInputs()` wires each input: digit-only filter, auto-advance, backspace navigates back, auto-submits on 6th digit. `sendCode()` made async — calls `/sms/send-otp` with loading overlay. `verifyCode()` calls `/sms/verify-otp`, shows inline error on failure, navigates to `allset` on success. `resendCode()` re-fires without leaving the screen. "DEMO: CHOOSE OUTCOME" branch buttons removed entirely. `state.phone` added.

---

### Phase 9a — March 5, 2026

**What changed:** Ownership verification redesigned from the ground up. Previously the *loser* had to invent a secret at submission time and match it exactly (Argon2id hash). Now the *finder* optionally notes a physical observation while holding the item — and Claude fuzzy-matches the loser's claim against it. No secret = no verify step. With secret = Claude judges semantic match, not exact string.

**Backend:** `secret_detail TEXT` column added to `items`. `POST /verify` completely rewritten to call Claude. New `PATCH /items/{id}/finder-info` endpoint replaces `/finder-email` (accepts both). `MatchResponse` and `ItemResponse` now include `has_secret: bool`. `secret_verifications` table no longer written to.

**Frontend:** Secret detail field removed from lost-prompt. Optional "🔐 Add a secret detail" field added to finder-done. Match screen CTA skips ownership-verify when `has_secret === false`. Ownership-verify copy and submit logic updated for new API shape.

---

### Phase 8.5 — March 5, 2026

Six UX fixes: broken `.desktop-hint` CSS; camera geo-row hardcoded "Lincoln Park · Chicago" replaced with live GPS state + pre-fetch on screen entry; status bar time frozen at "9:41" replaced with live clock; phone number not carried forward to verify/allset screens; handoff screen hardcoded distance replaced with real match data; content clipping on finder-done / lost-prompt / ownership-verify fixed with `overflow-y: auto`.

---

### Phase 8 — March 5, 2026

`latitude` and `longitude` columns added to `items`. All creation endpoints accept optional coords. `/match` uses pure-SQL Haversine formula — 10-mile radius filter when both items have location, embedding-only fallback otherwise. `MatchResponse` includes `distance_miles`. Frontend `getLocation()` helper, GPS sent on both finder photo upload and loser `submitLost()`. Waiting screen pills updated with real location + submission time.

---

### Phase 7 — March 5, 2026

Full Stripe tip flow: inline Card Element on Reunion screen (no redirect), `POST /tip/create-payment-intent`, `POST /stripe/webhook` marks tips completed. Finder email capture on Finder Done screen. Demo mode for tap-through testing without real API state.

---

### Phases 1–6 — March 5, 2026

Foundation → AI ingestion → matching engine → security → UI → API wiring. Full loop tested at 89.7% match similarity. Argon2id ownership verification (now legacy), JWT single-use handoff tokens, brute-force lockout.

---

*Built with Cursor + Claude. Zero prior coding experience. March 5, 2026.*
