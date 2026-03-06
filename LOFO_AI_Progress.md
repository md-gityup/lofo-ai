# LOFO.AI — Build Progress & Context
*Last updated: March 5, 2026 — Phases 1–9a complete and deployed*

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
| **9b — SMS Verification** | **← Next** | Real OTP via Twilio, replace fake verify screens |
| 10 — Realtime Matching | Planned | Polling/Supabase realtime on Waiting screen |
| 11 — Stripe Connect Payouts | Planned | Finder bank account, direct tip transfers |

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

**Railway environment variables:** `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`

---

## Known Intentional Placeholders

| Artifact | Screen | Fix in |
|---|---|---|
| Fake SMS OTP — hardcoded "3 7 4 ·" boxes | `screen-verify` | Phase 9b |
| "DEMO: CHOOSE OUTCOME" branch buttons | `screen-verify` | Phase 9b |
| "Simulate match found →" button | `screen-waiting` | Phase 10 |
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

## What's Next: Phase 9b — SMS Verification

Replace the fake phone verify flow with real Twilio OTP.

**Before starting:** Create a free Twilio account at twilio.com and add three new Railway environment variables:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER` (a Twilio-provisioned number, e.g. `+15005550006`)

**What to build:**
- New backend endpoint `POST /sms/send-otp` — generates a random 4-digit code, stores it (in-memory or a new `otp_sessions` table), sends it via Twilio SMS to the provided phone number
- New backend endpoint `POST /sms/verify-otp` — checks submitted code against stored code, returns `{verified: bool}`
- Frontend: `screen-phone` "Send code →" calls `/sms/send-otp`; replace hardcoded OTP boxes with a real interactive 4-input; submit calls `/sms/verify-otp`; on success navigate to `allset` or `match` depending on whether a match exists
- Remove the "DEMO: CHOOSE OUTCOME" branch buttons from `screen-verify`

---

## Cursor Prompt for Phase 9b

Paste this to start the next agent session:

> "I'm building LOFO.AI — a lost and found matching app. The project is at `~/Desktop/lofo-ai`. Read `LOFO_AI_Progress.md` first for full context.
>
> **What's complete and deployed (Phases 1–9a):**
> Live API at `https://lofo-ai-production.up.railway.app`, frontend at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`. Full loop: finder snaps photo → Claude Vision extracts profile → Voyage AI embedding → loser describes lost item → cosine similarity + proximity match → optional ownership verify (finder adds a secret detail; Claude fuzzy-matches loser's claim against it) → Stripe inline tip payment → Thanks screen.
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector, Stripe, `security.py`. Deployed on Railway. `.env` has: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`.
>
> **Frontend:** `LOFO_MVP.html` — 13 screens, all live API calls, Stripe.js. Key JS: `state` object, `go()` navigation, `submitLost()`, `submitOwnershipVerify()`, `sendTip()`, `confirmTip()`, `finderDoneContinue()`, `sendCode()`.
>
> **Known intentional placeholders — do not touch:**
> - `screen-verify`: fake SMS OTP with hardcoded "3 7 4 ·" boxes and two "DEMO: CHOOSE OUTCOME" branch buttons. This is exactly what Phase 9b replaces.
> - `screen-waiting`: "Simulate match found →" button. Keep until Phase 10.
>
> **What's next — Phase 9b: Real SMS Verification via Twilio**
> Replace the fake phone verify flow with real OTP. New backend endpoints: `POST /sms/send-otp` (generate + store code, send via Twilio) and `POST /sms/verify-otp` (validate submitted code). Frontend: wire `screen-phone` "Send code →" to the real endpoint, replace hardcoded OTP boxes with interactive digit inputs, verify on submit, remove demo branch buttons. Twilio credentials are already set in Railway env vars (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`).
>
> Start by reading `main.py` and `LOFO_MVP.html`, then begin implementation."

---

## Session History

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
