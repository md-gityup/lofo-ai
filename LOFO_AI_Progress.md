# LOFO.AI — Build Progress & Context
*Last updated: March 5, 2026 (Phase 9a complete — finder-owned secret detail with Claude fuzzy verification)*

---

## What LOFO.AI Is

A lost and found app built almost entirely by AI. Radically simple. A finder snaps a photo of something they found. A loser describes what they lost. AI matches them, verifies ownership, coordinates the return, and prompts a tip at the moment of reunion. Ten seconds of user effort. Everything else is the engine.

Full concept doc: `LOFO.pdf`
Full architecture doc: `LOFO_AI_Architecture.md`
UI prototype: `LOFO_MVP.html`

---

## The Bigger Picture

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
| 9b — SMS Verification | ← Next | Real OTP via Twilio, replace fake verify screens |
| 10 — Realtime Matching | Planned | Polling/Supabase realtime on Waiting screen |
| 11 — Stripe Connect Payouts | Planned | Finder bank account, direct tip transfers |

---

## Current Status: Phases 1–7 Complete & Deployed ✓

### What's running

| Thing | URL |
|---|---|
| **Live API (Railway)** | `https://lofo-ai-production.up.railway.app` |
| **Live app (GitHub Pages)** | `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html` |
| **API docs** | `https://lofo-ai-production.up.railway.app/docs` |
| **Local API** | `http://localhost:8000` (only when uvicorn running) |
| **Database** | Supabase (PostgreSQL + pgvector) |
| **Project folder** | `~/Desktop/lofo-ai` |
| **Git repo** | `https://github.com/md-gityup/lofo-ai` |

### Backend endpoints

| Endpoint | What it does |
|---|---|
| `GET /` | Serves LOFO_MVP.html (the app UI) |
| `POST /items` | Submit a structured item manually |
| `POST /items/from-photo` | Upload photo → Claude Vision extracts profile → stored with embedding |
| `POST /items/from-text` | Submit text description → Claude extracts profile → stored with embedding |
| `GET /items/{id}` | Retrieve an item by UUID |
| `POST /match` | Find top matching finder items for a loser item (cosine similarity) |
| `POST /verify` | Verify ownership via secret detail (Argon2id, 3-attempt lockout) |
| `POST /handoff/validate` | Validate single-use JWT handoff token |
| `PATCH /items/{id}/finder-email` | Store finder's payout email after item creation |
| `POST /tip/create-payment-intent` | Create Stripe PaymentIntent, record pending tip |
| `POST /stripe/webhook` | Mark tip completed on `payment_intent.succeeded` |

### Database schema

**Table: `items`**
| Column | Type | Notes |
|---|---|---|
| id | UUID | Auto-generated |
| type | varchar | 'finder' or 'loser' |
| item_type | varchar | e.g. 'handbag' |
| color | text[] | e.g. ['brown'] |
| material | varchar | e.g. 'leather' |
| size | varchar | 'small' / 'medium' / 'large' |
| features | text[] | e.g. ['gold clasp'] |
| embedding | vector(1024) | Voyage AI, used for cosine matching |
| finder_email | varchar | Optional — finder's payout email (Phase 7) |
| latitude | numeric(9,6) | Optional — GPS latitude at submission (Phase 8) |
| longitude | numeric(9,6) | Optional — GPS longitude at submission (Phase 8) |
| status | varchar | Default 'active' |
| expires_at | timestamptz | Default 30 days from creation |
| created_at | timestamptz | Auto-set |

**Table: `secret_verifications`**
| Column | Type | Notes |
|---|---|---|
| id | UUID | Auto-generated |
| item_id | UUID | References items(id) |
| secret_hash | varchar | Argon2id hash |
| attempt_count | integer | Brute-force counter |
| locked | boolean | True after 3 failed attempts |
| verified_at | timestamptz | Set on successful verification |

**Table: `used_tokens`**
| Column | Type | Notes |
|---|---|---|
| jti | varchar | JWT ID — unique, prevents replay |
| item_id | UUID | References items(id) |
| used_at | timestamptz | When token was first used |
| expires_at | timestamptz | Token expiry |

**Table: `tips`** *(Phase 7 — new)*
| Column | Type | Notes |
|---|---|---|
| id | UUID | Auto-generated |
| finder_item_id | UUID | References items(id) |
| loser_item_id | UUID | References items(id) |
| amount_cents | integer | e.g. 1000 = $10 |
| stripe_payment_intent_id | varchar | Stripe PI ID, unique |
| status | varchar | 'pending' → 'completed' via webhook |
| created_at | timestamptz | Auto-set |

### Key files

| File | What it does |
|---|---|
| `main.py` | FastAPI app — all 11 endpoints + CORS + serves HTML |
| `database.py` | Supabase connection pool + API key loading |
| `schema.sql` | PostgreSQL table definitions (all 4 tables) |
| `requirements.txt` | Python dependencies (includes stripe) |
| `LOFO_MVP.html` | Fully wired 13-screen app — real API calls, Stripe.js, real data |
| `security.py` | Argon2id hashing + JWT handoff token logic |
| `.env` | API keys — never share, never commit |

### Key credentials & locations

| Thing | Where |
|---|---|
| Supabase project | supabase.com → LOFO → LOFO-AI |
| Railway project | railway.app → lofo-ai |
| GitHub repo | github.com/md-gityup/lofo-ai |
| Stripe dashboard | dashboard.stripe.com |
| All API keys | `.env` file on local machine only |

**Railway environment variables (must match .env):**
`DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`

**Important:** Never share, paste, or commit your `.env` file.

---

## Session Summary — March 5, 2026 (Phase 8 session)

### What we did

1. **Ran schema migration** — `ALTER TABLE items ADD COLUMN latitude NUMERIC(9,6)` and `longitude`. Confirmed via psycopg2 — both columns now live on Supabase.

2. **Updated all item creation endpoints** — `/items`, `/items/from-text`, `/items/from-photo` all accept optional `latitude` / `longitude`. The photo endpoint takes them as `Form` fields alongside the file upload.

3. **Haversine proximity filter in `/match`** — SQL now computes distance in miles using the pure-SQL Haversine formula (no PostGIS). Results are filtered to a 10-mile radius when both items have coordinates; if either item has no location, embedding-only matching is used as fallback. `MatchResponse` now includes `distance_miles` (null when coordinates absent).

4. **Frontend geolocation** — new `getLocation()` helper calls `navigator.geolocation.getCurrentPosition` with a 6-second timeout. Called in both the finder photo upload handler and `submitLost()`. Coordinates stored in `state.latitude` / `state.longitude` and sent on every item creation request.

5. **Real waiting screen pills** — replaced hardcoded "Lincoln Park / Today 1–4 PM" copy. Now shows "Within 10 mi of your location" (or "Searching all nearby finds" if GPS was denied) and the actual submission time.

6. **Match card distance** — match screen meta now appends "· X.X mi away" when `distance_miles` is returned from the API.

7. **Pushed and deployed** — committed and pushed to `main`; Railway auto-redeploys.

### Issues hit and how they were resolved

None — clean build.

---

## Phase 8 — What Was Built

### Backend (`main.py`)

- `ItemCreate`, `TextItemCreate` schemas: added `latitude: Optional[float]` and `longitude: Optional[float]`
- `create_item_from_photo`: added `latitude: Optional[float] = Form(None)` and `longitude: Optional[float] = Form(None)`
- `_INSERT_SQL`: updated to always include `latitude, longitude` columns (pass `None` when absent)
- `_MATCH_SQL`: Haversine formula computes `distance_miles`; `AND (...)` clause filters to 10-mile radius or falls back to embedding-only when no coords
- `MatchResponse`: new `distance_miles: Optional[float] = None` field

### Database (`schema.sql` / Supabase)

- `ALTER TABLE items ADD COLUMN IF NOT EXISTS latitude NUMERIC(9,6)` ✅
- `ALTER TABLE items ADD COLUMN IF NOT EXISTS longitude NUMERIC(9,6)` ✅

### Frontend (`LOFO_MVP.html`)

- `state` now tracks `latitude` and `longitude`
- `getLocation()` — Promise wrapper around `navigator.geolocation.getCurrentPosition`; resolves null on error/denial/timeout
- Finder photo upload: calls `getLocation()` before fetch, appends `latitude`/`longitude` to FormData when available
- `submitLost()`: calls `getLocation()` before fetch, spreads coords into JSON body when available
- `updateWaitingPills()`: sets location pill ("Within 10 mi" or fallback) and time pill (real HH:MM AM/PM)
- Waiting screen HTML: replaced hardcoded pills with `id="waiting-location-text"` / `id="waiting-time-text"` spans
- Match screen: `item-meta` now appends distance string when `m.distance_miles != null`

### Known intentional placeholders (updated)

| Artifact | Where | Status |
|---|---|---|
| "DEMO: CHOOSE OUTCOME" + two branch buttons | `screen-verify` | Phase 9 |
| Hardcoded OTP boxes | `screen-verify` | Phase 9 |
| "Simulate match found →" button | `screen-waiting` | Phase 10 |
| Location/time pills | `screen-waiting` | ✅ Fixed Phase 8 |

---

---

## Session Summary — March 5, 2026 (Phase 9a session)

### What we built

**New ownership verification model:** The finder optionally adds a secret physical observation about the item they found (inscription, sticker, what's inside, unique mark). If they do, the loser must describe that detail before the handoff proceeds. Claude judges whether the descriptions match — semantically, not word-for-word.

**Why this is better than the old model:**
- Old: loser had to invent a secret at submission time, remember it later, and match it exactly (Argon2id hash)
- New: finder is the independent witness — they have the item in hand and can note objective details. Loser just describes what they know about their own item. Claude handles fuzzy matching.

**Backend (`main.py`):**
- `ALTER TABLE items ADD COLUMN IF NOT EXISTS secret_detail TEXT` — run on Supabase
- `ItemCreate` / `TextItemCreate`: accept optional `secret_detail` (stored on finder items only)
- `ItemResponse` + `MatchResponse`: new `has_secret: bool` field
- `_INSERT_SQL`: +`secret_detail` column; RETURNING `(secret_detail IS NOT NULL) AS has_secret`
- `_MATCH_SQL`: `(f.secret_detail IS NOT NULL) AS has_secret` in SELECT
- `create_item_from_photo`: accepts `secret_detail: Optional[str] = Form(None)`
- `create_item_from_text`: stores `secret_detail` for finder items; removed old `secret_verifications` INSERT
- `PATCH /items/{id}/finder-info`: new endpoint replaces `/finder-email`; accepts both `finder_email` and `secret_detail`; old URL kept as silent alias
- `POST /verify`: complete rewrite — fetches finder item's `secret_detail`, calls Claude to fuzzy-match against `loser_claim`, returns `{verified, reason}`; skips Claude call if no secret was set

**Frontend (`LOFO_MVP.html`):**
- Lost-prompt: removed secret detail field + required validation — loser flow is now two fields (description + location)
- Finder-done: added optional "🔐 Add a secret detail" input below the email field
- `finderDoneContinue()`: PATCHes `/finder-info` with email + secret_detail if provided
- Match screen CTA: routes to `ownership-verify` only when `state.matchedItem.has_secret === true`; skips straight to handoff otherwise
- Ownership-verify screen: new copy ("One quick check." / "The finder noted something specific…"); removed attempt-dot UI
- `submitOwnershipVerify()`: sends `{finder_item_id, loser_claim}`; shows Claude's human-readable `reason` on failure
- Removed dead `.att-dot` CSS

### Known intentional placeholders

| Artifact | Where | Status |
|---|---|---|
| Fake SMS OTP boxes | `screen-verify` | Phase 9b |
| "DEMO: CHOOSE OUTCOME" buttons | `screen-verify` | Phase 9b |
| "Simulate match found →" button | `screen-waiting` | Phase 10 |

---

## Session Summary — March 5, 2026 (Phase 8.5 session)

### What we did

Six UX & flow bugs identified and fixed in `LOFO_MVP.html`:

1. **Broken `.desktop-hint` CSS** — the comment block was malformed (missing closing `*/` and the selector itself). The "Tap through the full LOFO.AI user journey" hint below the phone shell had no styles at all. Fixed.

2. **Camera geo-row hardcoded** — `"Lincoln Park · Chicago"` was still in the HTML from before Phase 8. Phase 8 fixed the Waiting screen pills but missed the camera screen. Now shows `"Acquiring location…"` on entry and updates to `"Location acquired"` or `"Location unavailable"` once GPS resolves.

3. **GPS pre-fetch on camera entry** — Previously `getLocation()` was only called when the shutter was pressed. Now it's called immediately in `onScreenEnter('finder-camera')`, so the OS permission prompt fires while the user is composing the shot. By the time they tap the shutter, GPS is already resolved.

4. **Live clock** — All status bars showed frozen `"9:41"`. Added `updateClock()` that reads `new Date()` and writes the real time to every `.status-time` element. Runs on load and every 30 seconds.

5. **Phone number not carried forward** — User typed their number on screen-phone but `screen-verify` subtitle and `screen-allset` card still showed hardcoded `(555) 000-0000`. The "Send code →" button now calls `sendCode()` which captures the input value, writes it to both downstream screens, then navigates.

6. **Handoff screen hardcoded distance** — `"0.3 miles away · Lincoln Park"` was static HTML. `onScreenEnter('handoff')` now reads `state.matchedItem.distance_miles` and writes the real value (or `"Coordinate the return"` if no distance data).

7. **Content overflow/clipping** — `finder-done`, `lost-prompt`, and `ownership-verify` content areas had `overflow: hidden` (inherited from `.content`). Added `overflow-y: auto; -webkit-overflow-scrolling: touch` to those three screens so content scrolls instead of being clipped.

### Issues hit

None — clean build.

---

## What's Next: Phase 9 — SMS Verification

Replace the fake SMS/OTP verify screens with real Twilio-based phone verification.

---

## Session Summary — March 5, 2026 (Phase 7 session)

### What we did

1. **Debugged GitHub Pages → Railway connection** — the `API` URL detection was wrong. The old logic only handled `file://` vs same-origin. GitHub Pages uses `https:` so `API` resolved to `''`, pointing all fetches at GitHub Pages instead of Railway. Fixed by checking `window.location.hostname` instead of `window.location.protocol`.

2. **Fixed duplicate JWT_SECRET in `.env`** — two lines, python-dotenv loads first, Railway had a different value. Removed the duplicate locally, matched to Railway's value.

3. **Built Phase 7 — Stripe tip flow** — full implementation across backend and frontend (see below).

4. **Fixed demo mode error** — "Missing item info" error appeared when tapping to Reunion screen directly (no real API state). Fixed: `sendTip()` now detects demo mode (no `state.matchedItem`) and still shows the card element; `confirmTip()` in demo mode simulates success after 1.2s delay. Real flow does a real Stripe charge.

5. **Pushed all changes to git** — Railway auto-redeploys from main branch. GitHub Pages serves the HTML.

### Issues hit and how they were resolved

**Issue:** GitHub Pages HTML was calling itself instead of Railway — all API calls 404'd.
**Resolution:** Changed `const API` from protocol-check to hostname-check. Now correctly points to Railway from any non-Railway host.

**Issue:** Stripe "You did not provide an API key" error on Railway.
**Resolution:** `STRIPE_SECRET_KEY` wasn't set in Railway Variables. Added it there.

**Issue:** "Missing item info — please restart the flow" when tapping directly to Reunion screen.
**Resolution:** Added demo mode to `sendTip()` — checks if real item state exists. If not, skips the PaymentIntent API call, still mounts the Stripe Card Element, and simulates success on confirm.

---

## Phase 7 — What Was Built

### Backend (`main.py`)

- `import stripe` + `stripe.api_key = _STRIPE_SECRET_KEY`
- Added `Request` to FastAPI imports (needed for webhook body reading)
- New Pydantic schemas: `FinderEmailUpdate`, `TipCreateRequest`
- **`PATCH /items/{item_id}/finder-email`** — updates `finder_email` on a finder item after creation. Only updates `type = 'finder'` rows.
- **`POST /tip/create-payment-intent`** — validates both items exist, creates Stripe PaymentIntent (`payment_method_types: ["card"]`, amount in cents, metadata with item IDs), inserts pending tip row, returns `client_secret`.
- **`POST /stripe/webhook`** — reads raw body + Stripe-Signature header, verifies with `STRIPE_WEBHOOK_SECRET` if set (skips verification if blank — dev mode), handles `payment_intent.succeeded` by marking tip 'completed'.

### Database (`schema.sql`)

- `ALTER TABLE items ADD COLUMN IF NOT EXISTS finder_email VARCHAR`
- New `tips` table (see schema above)

### Frontend (`LOFO_MVP.html`)

- **Stripe.js CDN** added to `<head>`
- **`const stripeClient = Stripe(pk_test_...)`** in script — initialized once at page load
- **Finder Done screen** — new email input field: "Get paid when your find is reunited" (optional, hint: "we'll email you when someone tips you")
- **`finderDoneContinue()`** — replaces `go('phone')` on Finder Done Continue button. If email is filled, PATCHes `/items/{finderItemId}/finder-email` (non-blocking, failure doesn't stop flow), then navigates to 'phone'.
- **Reunion screen** — "Send $X →" button calls `sendTip()` instead of `go('thanks')`. New hidden `#card-payment-panel` div below the skip button.
- **`sendTip()`** — real flow: creates PaymentIntent via API, stores `client_secret`, shows card panel, mounts Stripe Card Element with LOFO dark styling. Demo flow (no state): skips API call, shows card panel directly.
- **`confirmTip()`** — real: calls `stripe.confirmCardPayment(clientSecret, { payment_method: { card: cardElement } })`. Demo: 1.2s simulated delay then go('thanks'). Both paths set `#thanks-amount` before navigating.
- **`cancelTip()`** — unmounts card element, hides panel, restores tip send + skip buttons.
- **Thanks screen** — "You sent **$X** to the finder." — `#thanks-amount` span updated dynamically.
- **CSS additions** — `.finder-email-section`, `.finder-email-input`, `.card-payment-panel`, `.stripe-card-wrap`, `.card-error`, `.card-cancel-link`

### Known demo artifacts (intentional — do not fix yet)

| Artifact | Where | Why it's intentional |
|---|---|---|
| "DEMO: CHOOSE OUTCOME" + two branch buttons on SMS Verify screen | `screen-verify` | SMS/OTP flow unbuilt. Fix in Phase 9. |
| Hardcoded OTP boxes showing "3 7 4 ·" | `screen-verify` | Same. |
| "(555) 000-0000" in verify screen copy | `screen-verify` | Same. |
| "Simulate match found →" button on Waiting screen | `screen-waiting` | Useful for demo. Remove when realtime matching is built (Phase 10). |
| Location and time pills on Waiting screen | `screen-waiting` | ✅ Fixed in Phase 8 — real GPS + submission time. |
| Finder Connect Express onboarding | — | Tips currently held in LOFO's Stripe balance. Full finder payout in Phase 11. |

---

## Phase 6 — End-to-End Test Results (March 5, 2026)

| Test | Result |
|---|---|
| `POST /items/from-text` (finder) | Claude extracted: wallet, brown, leather, small, bifold, silver clasp ✅ |
| `POST /items/from-text` (loser + secret) | Same extraction, secret hashed and stored ✅ |
| `POST /match` | **89.7% similarity score** — correct item returned, above 0.7 threshold ✅ |
| `POST /verify` (wrong answer) | `verified: false, attempts_remaining: 2` ✅ |
| `POST /verify` (correct answer) | `verified: true` + JWT handoff token issued ✅ |
| `POST /handoff/validate` (1st use) | `valid: true` ✅ |
| `POST /handoff/validate` (2nd use) | `409 — Handoff token has already been used` ✅ |

---

## How to Resume

### Option A — Test the live deployed app
Go to: `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`
API is at: `https://lofo-ai-production.up.railway.app`

### Option B — Run locally
```bash
cd ~/Desktop/lofo-ai
source .venv/bin/activate
uvicorn main:app --reload
```
Then open `http://localhost:8000/` or `LOFO_MVP.html` directly in a browser.

### Seed test data (for match testing)
```bash
# 1. Submit a finder item
curl -X POST https://lofo-ai-production.up.railway.app/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "finder", "description": "Found a brown leather wallet near the park fountain. Small, bifold, with a silver clasp."}'

# 2. Submit a matching loser item with a secret
curl -X POST https://lofo-ai-production.up.railway.app/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "loser", "description": "Lost my brown leather wallet, bifold with silver clasp, near the fountain.", "secret_detail": "There is a photo of my dog inside the left pocket"}'

# 3. Run match (use loser item id from step 2)
curl -X POST https://lofo-ai-production.up.railway.app/match \
  -H "Content-Type: application/json" \
  -d '{"item_id": "<loser-item-id>"}'
```

### Test the Stripe tip flow
Use Stripe test card: `4242 4242 4242 4242` · exp `12/26` · CVC `123` · any ZIP.
Check Stripe Dashboard → Payments to confirm charge appears.

---

## Phase 7 — Testing Checklist (do this before Phase 8)

Work through these in order to confirm Phase 7 is fully wired end-to-end.

### Demo mode test (no API state needed)
- [ ] Go to `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`
- [ ] Tap through to the Reunion screen directly
- [ ] Tap "Send $10 thank you →" — card input should appear inline (no redirect)
- [ ] Enter test card `4242 4242 4242 4242` · `12/26` · `123`
- [ ] Tap "Pay $10 →" — should land on Thanks screen showing "You sent $10 to the finder"
- [ ] Tap "← Change amount" before paying — should restore tip buttons correctly

### Real flow test (full API)
- [ ] Submit a finder item via text (use Railway `/docs` Swagger or curl)
- [ ] Submit a matching loser item with a secret
- [ ] Go through the app: describe lost item → match found → verify ownership → handoff → reunion
- [ ] Tap a tip amount, enter test card, confirm payment
- [ ] Check **Stripe Dashboard → Payments** — $X charge should appear ✅
- [ ] Check **Supabase → tips table** — row should show `status = 'completed'` (webhook fired) ✅

### Finder email test
- [ ] Submit a finder photo or text item
- [ ] On Finder Done screen, enter an email address in "Get paid when your find is reunited"
- [ ] Tap Continue
- [ ] Check **Supabase → items table** — `finder_email` column should be populated ✅

### Webhook test
- [ ] Make a real tip payment (real flow above)
- [ ] Go to Stripe Dashboard → Developers → Webhooks → your endpoint → check "Recent deliveries"
- [ ] Should show a successful `payment_intent.succeeded` delivery ✅

### Known issues to watch for
| Issue | What to do |
|---|---|
| "Stripe error: No API key" | STRIPE_SECRET_KEY not set in Railway — check Variables tab |
| Tips table doesn't update to 'completed' | STRIPE_WEBHOOK_SECRET not set in Railway, or webhook URL wrong |
| Card panel doesn't appear | Check browser console for JS errors — likely Stripe.js failed to load |
| "Finder item not found" on tip | Make sure you went through the full loser flow, not demo tap-through |

---

## What's Next: Phase 8 — GPS & Proximity Matching

**Goal:** Capture real lat/lng from the browser at item submission. Store location on each item. Filter match results by proximity so a wallet found in Chicago never matches a wallet lost in Miami.

### What to build in Phase 8

**8a — Frontend location capture**
- Request `navigator.geolocation` permission when finder submits photo and when loser submits description
- Pass `latitude` and `longitude` as optional fields on both `/items/from-photo` and `/items/from-text`
- Replace hardcoded location pills on Waiting screen with real "Within X mi" data

**8b — Backend schema + endpoint updates**
- Add `latitude NUMERIC(9,6)` and `longitude NUMERIC(9,6)` columns to `items` table
- Update all three item creation endpoints (`/items`, `/items/from-text`, `/items/from-photo`) to accept and store optional `lat`/`lng`
- Update `/match` to filter by proximity (Haversine formula in SQL — no PostGIS needed for MVP)

**8c — Match proximity filter**
- Default radius: 10 miles
- Items with no location stored are still matchable (fall back to embedding-only matching)
- Match response includes distance in miles

**Schema change needed on Supabase:**
```sql
ALTER TABLE items ADD COLUMN IF NOT EXISTS latitude  NUMERIC(9,6);
ALTER TABLE items ADD COLUMN IF NOT EXISTS longitude NUMERIC(9,6);
```

---

## Cursor Prompt for Phase 8

When starting the Phase 8 Cursor session, paste this:

> "I'm building LOFO.AI — a lost and found matching app. The project is at ~/Desktop/lofo-ai. Read `LOFO_AI_Progress.md` first for full context. Here's the quick version:
>
> **What's complete and working:**
> Phases 1–7 fully built and deployed. Live API at `https://lofo-ai-production.up.railway.app`, frontend at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`. The full loop works: finder snaps photo → Claude Vision extracts profile → Voyage AI embedding → loser describes lost item → cosine similarity match (tested 89.7%) → Argon2id ownership verification (3-attempt lockout) → single-use JWT handoff → Stripe inline card payment (Card Element, no redirect) → Thanks screen shows amount paid.
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector (`database.py`), Stripe (`stripe`), security (`security.py`). 11 endpoints. Deployed on Railway. `.env` has: DATABASE_URL, ANTHROPIC_API_KEY, VOYAGE_API_KEY, JWT_SECRET, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET. Stripe webhook configured for `payment_intent.succeeded` → marks tips as 'completed'.
>
> **Frontend:** `LOFO_MVP.html` — 13 screens, all live API calls, Stripe.js inline card payment. Key JS: `state` object, `go()` navigation, `submitLost()`, `submitOwnershipVerify()`, `sendTip()`, `confirmTip()`, `finderDoneContinue()`, `cleanType()`.
>
> **Known intentional placeholders (do not touch):** SMS/OTP verify screens are fake (Phase 9), 'Simulate match found' button on Waiting screen (Phase 10), hardcoded location pills on Waiting screen (Phase 8 — that's what we're building now).
>
> **What's next — Phase 8: GPS & Proximity Matching**
> Capture real lat/lng from the browser Geolocation API at item submission. Store it on the items table. Update the match endpoint to filter by proximity (Haversine in SQL). Replace hardcoded location pills with real distance data.
>
> Start by reading `main.py` and `LOFO_MVP.html`. Then run the two schema changes on Supabase (in the progress doc) and begin implementation."

---

*Built with Cursor + Claude. Zero prior coding experience. March 5, 2026.*
