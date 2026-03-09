# LOFO.AI — Build Progress & Context
*Last updated: March 7, 2026 — Phases 1–12a complete and deployed*

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
| 11 — Finder Payouts | ✅ Complete | Payout handle capture (Venmo/PayPal/Cash App/Zelle); tips collected via Stripe, distributed to stored handle |
| 11c — Allset Screen Polish | ✅ Complete | Reward section redesigned: messaging on cream bg (no card), dropdown replaces pills, dual-entry confirm, larger type |
| 12a — SMS Relay & Both-Path Notify | ✅ Complete | "I'll sort it out myself" fixed — both buttons call coordinateHandoff; reunions table; POST /sms/inbound relay; no raw numbers shared |

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
| `POST /tip/create-payment-intent` | Create Stripe PaymentIntent; routes via `transfer_data` to finder's Connect account if set, falls back to platform-held |
| `POST /stripe/webhook` | Mark tip `completed` on `payment_intent.succeeded` |
| `POST /sms/send-otp` | Send 6-digit OTP via Twilio Verify |
| `POST /sms/verify-otp` | Validate submitted OTP; returns `{verified: bool}` |
| `POST /handoff/coordinate` | Save loser phone + create reunion record + fire relay-style SMS to both parties (no raw numbers shared) |
| `POST /sms/inbound` | Twilio inbound webhook — relays messages between finder/loser via LOFO's number; config in Twilio console |
| `POST /connect/onboard` | Create Stripe Connect Express account for finder; return onboarding URL *(dormant — not used in UI)* |
| `GET /connect/return` | Post-onboarding redirect → back to frontend *(dormant)* |
| `GET /connect/refresh` | Re-generate expired onboarding link *(dormant)* |

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
| stripe_connect_account_id | varchar | Optional — Stripe Connect Express account ID (dormant) |
| finder_payout_app | varchar | Optional — e.g. `'venmo'`, `'paypal'`, `'cashapp'`, `'zelle'` |
| finder_payout_handle | varchar | Optional — e.g. `'@username'`, `'$cashtag'`, email, phone |
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

**Table: `reunions`** *(Phase 12a)*
| Column | Type | Notes |
|---|---|---|
| id | UUID | Auto-generated |
| finder_item_id | UUID | References items(id) |
| loser_item_id | UUID | References items(id) |
| finder_phone | varchar | E.164 — for relay lookup |
| loser_phone | varchar | E.164 — for relay lookup |
| status | varchar | Default `'active'` |
| created_at | timestamptz | Auto-set |
| expires_at | timestamptz | 7 days from creation — relay stops after |

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

*None — all known bugs resolved.*

## Manual Setup (Phase 12a)

**Twilio inbound webhook** — required for SMS relay to work:
- Go to [console.twilio.com](https://console.twilio.com) → Phone Numbers → your LOFO number
- Messaging → "A message comes in" → set to `https://lofo-ai-production.up.railway.app/sms/inbound` (HTTP POST)

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

## What's Next: Phase 12 — Ideas

- **Phase 12a polish:** Fix misleading copy when finder has no phone ("We've notified the finder" → honest message); ghost button copy ("just notify the finder" → "notify us both"); duplicate reunion guard (UNIQUE or check before INSERT)
- **Photo storage:** store finder's photo in Supabase Storage; display on confirmed screen instead of attribute text
- **Stripe Connect application fee:** add `application_fee_amount` to `POST /tip/create-payment-intent` for a LOFO platform cut
- **Payout status:** `GET /connect/status` to check whether finder's account has completed onboarding (capabilities ready), update allset button to "✓ Connected" on re-entry if already linked
- **Web push notifications:** replace SMS-only with web push on desktop/PWA so finders get notified without leaving a tab open

---

## Cursor Prompt for Next Session

Paste this to start the next agent session:

> "I'm building LOFO.AI — a lost and found matching app. The project is at `~/Desktop/lofo-ai`. Read `LOFO_AI_Progress.md` first for full context.
>
> **What's complete and deployed (Phases 1–12a):**
> Live API at `https://lofo-ai-production.up.railway.app`, frontend at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`. Full end-to-end loop: finder snaps photo → Claude Vision → Voyage embedding → phone OTP → allset screen with payout handle capture (Venmo/PayPal/Cash App/Zelle dropdown, dual-entry confirm, format validation, stored to DB). Loser flow: describe item → cosine similarity + proximity match → if no match, polls and captures phone for SMS → match screen → ownership verify (Claude fuzzy-match) → confirmed screen → **both buttons** call `coordinateHandoff()` (Notify us both / I'll reach out — just notify the finder) → reunion relay SMS to both parties (no raw numbers shared) → Stripe tip → thanks. Rejected matches tracked in `state.rejectedMatchIds`. Tips collected via Stripe to LOFO balance; payout to finder's stored handle is manual.
>
> **Phase 12a (SMS relay):** `reunions` table stores finder_phone, loser_phone for relay. `POST /handoff/coordinate` creates reunion + fires relay-style SMS. `POST /sms/inbound` (Twilio webhook) forwards messages between parties. Twilio inbound URL must be set in console. Known polish items: misleading copy when finder has no phone; ghost button says 'just notify the finder' but both are notified; duplicate reunion guard.
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector, Stripe, Twilio, `security.py`. Deployed on Railway. All env vars set.
>
> **Frontend:** `LOFO_MVP.html` — 16 screens. Key JS: `state`, `go()`, `onScreenEnter()`, `coordinateHandoff()`, `submitOwnershipVerify()`, `sendTip()`, `confirmTip()`, `startPolling()`, `rejectMatch()`, etc.
>
> **DB schema:** `items`, `tips`, `reunions` (finder_item_id, loser_item_id, finder_phone, loser_phone, status, expires_at).
>
> See `LOFO_AI_Progress.md` for Phase 12 polish ideas and next steps.
>
> Start by reading `main.py` and `LOFO_MVP.html`, then begin."

---

## Session History

### Phase 12a — March 7, 2026

**What changed:** Fixed "I'll sort it out myself" gap + SMS relay so both parties are always notified.

**The problem:** The ghost button on `screen-confirmed` called `go('reunion')` directly, skipping `coordinateHandoff()`. The finder was never notified; the loser could tip and the finder had no idea their item was claimed.

**Fix — both paths notify:**
- Both buttons ("Notify us both →" and "I'll reach out — just notify the finder") now call `coordinateHandoff()`.
- Phone is required before either action; both parties get SMS.

**SMS relay (no raw numbers):**
- `reunions` table: `finder_item_id`, `loser_item_id`, `finder_phone`, `loser_phone`, `status`, `expires_at` (7 days).
- `POST /handoff/coordinate` creates reunion record and sends relay-style SMS to both parties: "Reply to this number to message [finder/owner] — we'll pass it along securely."
- `POST /sms/inbound` — Twilio webhook. When either party replies to LOFO's number, the endpoint looks up the active reunion and forwards the message to the other party with `[Finder via LOFO]` or `[Owner via LOFO]` prefix. Returns empty TwiML.
- If finder has no phone on file: loser gets "We've notified the finder" (copy is misleading — see Phase 12 polish).

**Manual step:** Configure Twilio Phone Numbers → Messaging → Webhook URL: `https://lofo-ai-production.up.railway.app/sms/inbound` (HTTP POST).

**Known polish:** (1) Fix copy when finder has no phone. (2) Ghost button says "just notify the finder" but both are notified. (3) Add duplicate reunion guard.

---

### Phase 11c — March 6, 2026

**What changed:** Allset screen reward section polish.

**Messaging lifted out of card:** The "Optional reward" eyebrow, title, and body text now live directly on the cream background — no white card wrapper. The white card only contains the interactive dropdown + handle fields. This separates the communication layer from the action layer visually.

**Text sizes increased:** `payout-intro-title` 14px → 18px; `payout-intro-body` 12.5px → 15px. Both noticeably more readable without competing with the main allset headline.

**Copy trimmed:** Body copy cut from ~50 words to 28: *"LOFO is free — always. If the owner wants to say thanks, we'll give them the option a few hours after reunion. Entirely up to them."* Same meaning, half the length.

**Dropdown replaces pill selectors:** Four pill buttons replaced with a native `<select>` ("Select how to get rewarded") with a custom chevron. Cleaner, less cluttered, more intentional.

**Dual-entry confirm field:** After selecting an app, two labeled inputs appear — "Your handle" and "Confirm handle". On save, both are normalized and compared (case-insensitive). If they don't match, both fields highlight red with an inline error. Prevents typo on a field that can't be verified any other way.

**CSS removed:** `.payout-apps`, `.payout-app-pill`, `.payout-section-label`, `.payout-divider` — all deleted. New classes: `.payout-dropdown`, `.payout-dropdown-label`, `.payout-handle-fields`, `.payout-handle-field-label`, `.payout-handle-input.mismatch`.

---

### Phase 11 — March 6, 2026

**What changed:** Rejected match loop bug fix + finder payout handle capture.

**Bug fix (rejected match loop):**
`state.rejectedMatchIds = []` added to app state. `rejectMatch()` pushes the current `matchedItem.id` before clearing. Both `pollForMatch()` and `submitLost()` filter `/match` results against `rejectedMatchIds` so a rejected item is never surfaced again in the same session. If all candidates are rejected, polling continues and the loser lands on the waiting/notify screen normally.

**Phase 11 — Finder Payouts:**

Stripe Connect was attempted first but abandoned — Stripe requires the platform (LOFO) to complete full business verification before any Express accounts can be created, which is the wrong experience entirely for an MVP. Even if that worked, asking a finder to submit SSN + bank details to "set up a Stripe account" is too much friction for someone who just picked up a wallet.

Replaced with a simple payout handle capture:

*Database:* Two new columns — `finder_payout_app VARCHAR` (e.g. `'venmo'`) and `finder_payout_handle VARCHAR` (e.g. `'@username'`). Migration applied. `stripe_connect_account_id` column kept but dormant.

*Backend:* `FinderInfoUpdate` extended with `finder_payout_app` and `finder_payout_handle`. The existing `PATCH /items/{id}/finder-info` endpoint handles them via its generic `updates` dict — no new endpoint needed. Connect endpoints (`/connect/onboard`, `/connect/return`, `/connect/refresh`) remain in the codebase but are not used in the UI. `POST /tip/create-payment-intent` still routes via `transfer_data` if a Connect account ID is present, but falls back gracefully.

*Frontend (`LOFO_MVP.html`):*
- "Get paid when it's returned" section on `screen-allset` replaces the Connect card.
- Four pill-style app selectors: **Venmo / PayPal / Cash App / Zelle**. Tap highlights the pill navy.
- Handle input appears below with app-specific placeholder (`@username`, `email or @username`, `$cashtag`, `phone or email`).
- Client-side format validation on save — regex per app, inline error if bad format.
- Auto-prefix: Venmo gets `@`, Cash App gets `$` if not already present.
- After save: confirmation row shows `✓ Venmo @handle` in green with an Edit link.
- Section state resets cleanly on each `screen-allset` entry.
- `showSuccess()` helper added for green success toasts.
- Tips still collected via Stripe to LOFO's balance. Payout to finder's stored handle is currently manual (pull from Supabase `items` table when tip completes).

---

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
3. **Confirmed screen** (new `screen-confirmed`) — post-verification payoff. Strong triple-pulse haptic. Shows item card (emoji + attributes). Requires loser's phone number. Both buttons call `POST /handoff/coordinate` (Phase 12a: "Notify us both" and "I'll reach out — just notify the finder").
4. **Relay SMS** — `POST /handoff/coordinate` saves loser phone, creates reunion record, fires relay-style SMS to both parties. Neither sees the other's number; they reply to LOFO's number and `POST /sms/inbound` relays messages. *(Phase 10c originally shared raw numbers; Phase 12a changed to relay.)*
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

*Built with Cursor + Claude. Zero prior coding experience. March 5–7, 2026.*
