# LOFO.AI — Build Progress & Context
*Last updated: March 6, 2026 — Phases 1–10c + bug fixes complete and deployed*

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
| 9b — SMS Verification | ✅ Complete | Real OTP via Twilio Verify, 6-digit inputs, demo buttons removed |
| 10 — Realtime Matching | ✅ Complete | 5s polling on Waiting screen; auto-navigates to Match on hit |
| 10b — Two-sided SMS Notifications | ✅ Complete | Finder posts → SMS waiting losers; loser posts → SMS matched finders |
| 10c — Match Flow Redesign | ✅ Complete | Realistic loser flow: potential match → ownership verify → confirmed screen → broker SMS → tip |
| 10d — Flow Bug Fixes | ✅ Complete | Loser-wait screen, "Not my item" routing, finder phone save bug, CSS animation fix |
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
| `POST /items/from-photo` | Photo → Claude Vision → item profile + embedding; triggers loser SMS notifications |
| `POST /items/from-text` | Text → Claude → item profile + embedding; triggers notifications both directions |
| `GET /items/{id}` | Retrieve item by UUID |
| `POST /match` | Cosine similarity + Haversine proximity match; returns `has_secret: bool` per result |
| `POST /verify` | Claude fuzzy-matches finder's `secret_detail` against loser's `loser_claim`; returns `{verified, reason}` |
| `POST /handoff/validate` | Validate single-use JWT handoff token |
| `PATCH /items/{id}/finder-info` | Save finder's `finder_email`, `secret_detail`, and/or `phone` after item creation |
| `PATCH /items/{id}/loser-info` | Save loser's `phone` so they can receive match notifications |
| `POST /tip/create-payment-intent` | Create Stripe PaymentIntent, record pending tip |
| `POST /stripe/webhook` | Mark tip `completed` on `payment_intent.succeeded` |
| `POST /sms/send-otp` | Send 6-digit OTP via Twilio Verify |
| `POST /sms/verify-otp` | Validate submitted OTP; returns `{verified: bool}` |
| `POST /handoff/coordinate` | Save loser phone + fire intro SMS to both parties with each other's numbers |

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
| finder_email | varchar | Optional — finder's payout email |
| latitude | numeric(9,6) | Optional — GPS latitude at submission |
| longitude | numeric(9,6) | Optional — GPS longitude at submission |
| secret_detail | text | Optional — finder's physical observation for ownership verify |
| phone | varchar | Optional — contact phone for SMS notifications (both finder and loser) |
| status | varchar | Default `'active'` |
| expires_at | timestamptz | Default 30 days from creation |
| created_at | timestamptz | Auto-set |

**Table: `secret_verifications`** *(legacy — no longer written to since Phase 9a)*

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
| `LOFO_MVP.html` | 16-screen app — all live API calls, Stripe.js, GPS, Twilio OTP |
| `security.py` | Argon2id hashing + JWT handoff token logic |
| `.env` | API keys — never share, never commit |

## Key Credentials

| Thing | Where |
|---|---|
| Supabase project | supabase.com → LOFO → LOFO-AI |
| Railway project | railway.app → lofo-ai |
| GitHub repo | github.com/md-gityup/lofo-ai |
| Stripe dashboard | dashboard.stripe.com |
| Twilio console | console.twilio.com |
| All API keys | `.env` on local machine only |

**Railway environment variables:** `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_VERIFY_SID`

---

## Known Intentional Placeholders

| Artifact | Screen | Fix in |
|---|---|---|
| Finder payout (tips held in LOFO's Stripe balance) | — | Phase 11 |
| Photo not stored — confirmed screen shows item attributes instead of actual photo | Confirmed | Phase 11 or 12 |

## Known Bugs To Fix

| Bug | Details |
|---|---|
| Rejected match loops | If loser taps "Not my item" and there's only one potential match, polling finds the same match again immediately. Need to track rejected match IDs in `state` (e.g. `state.rejectedMatchIds = []`) and filter them out of `/match` results — either client-side or via a `exclude_ids` param on the backend. If multiple matches exist, serve the next one; only show "no match" if all candidates are exhausted. |

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
# 1. Submit a finder item (with phone for notifications)
curl -X POST https://lofo-ai-production.up.railway.app/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "finder", "description": "Found a brown leather wallet near the park fountain. Small, bifold, with a silver clasp.", "secret_detail": "There is a photo of a golden retriever inside the left pocket"}'

# 2. Submit a matching loser item
curl -X POST https://lofo-ai-production.up.railway.app/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "loser", "description": "Lost my brown leather wallet, bifold with silver clasp, near the fountain."}'

# 3. Run match (use loser item id from step 2)
curl -X POST https://lofo-ai-production.up.railway.app/match \
  -H "Content-Type: application/json" \
  -d '{"item_id": "<loser-item-id>"}'

# 4. Verify ownership
curl -X POST https://lofo-ai-production.up.railway.app/verify \
  -H "Content-Type: application/json" \
  -d '{"finder_item_id": "<finder-item-id>", "loser_claim": "I have a photo of my dog inside"}'
```

**Stripe test card:** `4242 4242 4242 4242` · exp `12/26` · CVC `123` · any ZIP

---

## What's Next: Phase 11 — Stripe Connect Payouts

Right now tips are collected by Stripe but sit in LOFO's Stripe balance. Finders never see the money. Phase 11 wires Stripe Connect so tips route directly to the finder's bank account.

**What to build:**
- Stripe Connect account onboarding for finders (Express or Standard)
- `POST /connect/onboard` — creates a Stripe Connect account + returns onboarding link
- `POST /connect/return` — handles post-onboarding redirect, marks finder as payout-enabled
- Store `stripe_connect_account_id` on finder items (or a separate `finders` table)
- Update `POST /tip/create-payment-intent` to route payment to finder's Connect account via `transfer_data` or `on_behalf_of`
- UI: Add "Set up payouts" step in finder flow after OTP verify (or prompt from allset screen)

---

## Cursor Prompt for Next Session

Paste this to start the next agent session:

> "I'm building LOFO.AI — a lost and found matching app. The project is at `~/Desktop/lofo-ai`. Read `LOFO_AI_Progress.md` first for full context.
>
> **What's complete and deployed (Phases 1–10d):**
> Live API at `https://lofo-ai-production.up.railway.app`, frontend at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`. Full end-to-end loop: finder snaps photo → Claude Vision → Voyage embedding → phone OTP via Twilio Verify → allset. Loser describes item → cosine similarity + proximity match → if no match, waits 10s then captures phone for SMS notification → polling auto-navigates on match → "hang tight" screen. When finder posts, backend SMSes any waiting losers whose item matches. When loser posts and matches instantly, backend SMSes the finder. Match screen shows confidence + when/where found → ownership verify (Claude fuzzy-match) → confirmed screen captures loser phone → `POST /handoff/coordinate` fires intro SMS to both parties → Stripe inline tip → thanks.
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector, Stripe, Twilio, `security.py`. Deployed on Railway. All env vars set: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_VERIFY_SID`.
>
> **Frontend:** `LOFO_MVP.html` — 16 screens, all live. Key JS: `state` object (`finderItemId`, `loserItemId`, `matchedItem`, `phone`, `loserPhone`, `loserItemType`, `latitude`, `longitude`), `go()` + `onScreenEnter()` navigation lifecycle, `submitLost()`, `submitOwnershipVerify()`, `coordinateHandoff()`, `sendTip()`, `confirmTip()`, `finderDoneContinue()`, `sendCode()`, `verifyCode()`, `saveLoserPhone()`, `startPolling()`, `rejectMatch()`, `timeAgo()`.
>
> **DB schema:** `items` table has `phone VARCHAR`, `finder_email`, `secret_detail`, GPS coords, `embedding vector(1024)`, `created_at`. `tips` table tracks Stripe payments.
>
> **Known bug to fix first:** When loser taps "Not my item" and there's only one potential match, polling finds the same match again immediately — creating a loop. Fix: track rejected match IDs in `state.rejectedMatchIds = []`, filter them out of `/match` results client-side (or add `exclude_ids` param to backend). If all candidates are exhausted, go to waiting screen normally.
>
> **Next after that — Phase 11: Stripe Connect Payouts**
> Wire Stripe Connect so tips route directly to finders. Build onboarding flow: after OTP verify on allset screen, prompt finder to connect their bank. Backend: `POST /connect/onboard` creates Stripe Connect Express account + returns onboarding URL. Store `stripe_connect_account_id` on finder items. Update `POST /tip/create-payment-intent` to use `transfer_data` to route funds to the finder's Connect account.
>
> Start by reading `main.py` and `LOFO_MVP.html`, then begin implementation."

---

## Session History

### Phase 10d — March 6, 2026

**What changed:** Four bug fixes discovered during live testing of Phase 10c flow.

**1. Loser-wait screen (dead end fix)**
After the loser entered their phone on the waiting screen and tapped "Notify me →", they were stuck — a confirmation text appeared but nothing happened. Added a new `screen-loser-wait` terminal screen (navy background, modal slide-up) that navigates to after `saveLoserPhone()` succeeds. Features a breathing orb animation (3 concentric rings staggered at -1.33s, 4s ease-in-out cycle) simulating calm breathing. Copy: "Hang tight. Think positive." / "People do good things. We'll text you the moment someone finds your [item]." Item type populated from `state.loserItemType` stored at submit time.

**2. Finder phone never saved (broker SMS broken)**
`PATCH /items/{id}/finder-info` endpoint had `FinderInfoUpdate` schema with a `phone` field, but the endpoint only processed `finder_email` and `secret_detail` — the `phone` field was silently dropped. This meant finder's phone was always `NULL` in the DB, so `POST /handoff/coordinate` could never SMS the finder or give the loser the finder's number. Added `if body.phone is not None: updates["phone"] = body.phone` to the endpoint.

**3. "Not my item" sent loser to home instead of waiting**
Ghost button on match screen had hardcoded `onclick="go('home')"`. Added `rejectMatch()` function that checks `matchContext`: if `'loser'` → `go('waiting')` (polling restarts, same session continues); if `'finder'` → `go('home')`. Clears `state.matchedItem` on reject.

**4. Backward-from-modal animation broken**
`.screen.active { transform: translateX(0) !important }` — the `!important` declaration beats a normal inline style in the CSS cascade. When `go()` set the animation start position via `element.style.transform = 'translateX(-28%)'` and then added the `active` class, the CSS `!important` immediately overrode the inline style, snapping the destination screen to position 0 before the animation could run. Removed `!important` from `.screen.active` transform — inline start positions now win during setup, RAF animates to 0, cleanup `setTimeout` removes exit classes.

**Also fixed in this session:** `_TWILIO_PHONE_NUMBER` was referenced in `_sms()` but never defined — all Phase 10b notification SMS were silently failing. Added `_TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")`.

---

### Phase 10c — March 6, 2026

**What changed:** Complete redesign of the loser post-match flow to reflect real-world reunion mechanics.

**The problem:** Old flow went Match → "How to meet" (placeholder options) → Tip. This skipped ownership verification context, had no emotional confidence-building moment, never captured the loser's phone in the happy path, and never actually connected the two parties.

**New loser flow:**
1. **Match screen** — eyebrow changed to "Good news", headline to "We may have found your [item]" (tentative, honest). Meta now shows "Found X min/hrs ago · X mi away" using `created_at` from the match response. Haptic fires on both immediate match and polling match.
2. **Ownership verify** — unchanged mechanically; skipped if no `secret_detail`.
3. **Confirmed screen** (new `screen-confirmed`) — post-verification payoff. Strong triple-pulse haptic. Shows item card (emoji + attributes). Requires loser's phone number. "Connect us →" calls `POST /handoff/coordinate`. "I'll sort it out myself" skips to tip.
4. **Broker SMS** — `POST /handoff/coordinate` saves loser phone, fetches finder phone, fires intro SMS to both parties. Loser gets finder's number; finder gets loser's number. LOFO exits the loop.
5. **Tip screen** — reached after coordination, not before. Loser is now in peak grateful state.

**Backend:** `POST /handoff/coordinate` endpoint added. `MatchResponse` now includes `created_at`. `_MATCH_SQL` updated to return `f.created_at::text`. Fixed missing `_TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")` (was referenced but never defined — silent SMS failures now fixed). `CoordinateRequest` schema added.

**Frontend:** `screen-confirmed` HTML + CSS added. `flowOrder` and `screenMap` updated. `state.loserPhone` added. `timeAgo()` helper for human-readable timestamps. `coordinateHandoff()` function. `submitOwnershipVerify()` now routes to `confirmed` on success. Match screen CTA (no secret path) now routes to `confirmed`. `saveLoserPhone()` saves to `state.loserPhone` for pre-population on confirmed screen.

---

### Phase 10b — March 6, 2026

**What changed:** Two-sided SMS notification loop — the app now actively connects finder and loser when a match exists, even if they submitted at different times.

**Backend:** Two new SQL helpers (`_NOTIFY_LOSER_SQL`, `_NOTIFY_FINDER_SQL`) run reverse and forward cosine + proximity matches after every item creation. `_sms()` helper sends plain Twilio notification messages (not Verify). `_notify_waiting_losers()` called after finder item created — SMSes any active loser items with matching embeddings and a stored phone. `_notify_matched_finder()` called after loser item created — SMSes any matching finder items with a phone. Both are fully non-blocking (exceptions swallowed, logged). `phone VARCHAR` column added to `items` (requires `ALTER TABLE items ADD COLUMN IF NOT EXISTS phone VARCHAR;` in Supabase). New `PATCH /items/{id}/loser-info` endpoint saves loser phone. `FinderInfoUpdate` extended with `phone` field so finder phone saves via existing `PATCH /items/{id}/finder-info`. Finder's verified phone saved automatically in `verifyCode()` on OTP success.

**Frontend:** Waiting screen: after ~10 seconds (2 polls) with no match, phone-capture section fades in below status pills — "Nothing nearby yet. Drop your number and we'll text you." Phone input + "Notify me →" button → calls `PATCH /items/{id}/loser-info` → shows "You're on the list" confirmation. Polling continues in background while phone section is visible, so auto-navigation to match still fires. `saveLoserPhone()` added.

---

### Phase 10 — March 6, 2026

**What changed:** The loser waiting screen now polls for real matches instead of showing a fake simulate button.

**Frontend only:** `startPolling()` / `stopPolling()` / `pollForMatch()` added. Polls `POST /match` every 5s. On match: stops polling, sets `state.matchedItem`, fires haptic, navigates to `screen-match`. After ~2 min stops. Wired into `onScreenEnter()` lifecycle. "Simulate match found →" removed.

---

### Phase 9b — March 6, 2026

**What changed:** Fake SMS verify flow replaced with real Twilio OTP end-to-end.

**Backend:** `POST /sms/send-otp` and `POST /sms/verify-otp` via Twilio Verify API (switched from basic messaging after US carrier filtering blocked delivery). `TWILIO_VERIFY_SID` env var. `twilio` added to `requirements.txt`.

**Frontend:** `screen-verify` replaced with six real digit inputs. `initOtpInputs()`, `sendCode()`, `verifyCode()`, `resendCode()`. Auto-advance, auto-submit on 6th digit. "DEMO: CHOOSE OUTCOME" buttons removed. `state.phone` added.

---

### Phase 9a — March 5, 2026

**What changed:** Ownership verification redesigned. Finder notes a physical observation; Claude fuzzy-matches loser's claim against it. No secret = no verify step.

**Backend:** `secret_detail TEXT` on `items`. `POST /verify` calls Claude. `PATCH /items/{id}/finder-info`. `has_secret: bool` on match + item responses.

---

### Phase 8.5 — March 5, 2026

Six UX fixes: `.desktop-hint` CSS; live GPS on camera screen; live clock; phone propagation; real distances on handoff; scroll fixes on finder-done / lost-prompt / ownership-verify.

---

### Phase 8 — March 5, 2026

`latitude` and `longitude` on `items`. Haversine 10-mile proximity filter in `/match`. `distance_miles` in `MatchResponse`. GPS captured on both finder and loser submission.

---

### Phase 7 — March 5, 2026

Stripe inline tip flow. `POST /tip/create-payment-intent`, webhook marks completed. Finder email capture. Demo mode.

---

### Phases 1–6 — March 5, 2026

Foundation → AI ingestion → matching engine → security → UI → API wiring. Full loop tested at 89.7% similarity.

---

*Built with Cursor + Claude. Zero prior coding experience. March 5–6, 2026.*
