# LOFO.AI — Build Progress & Context
*Last updated: March 12, 2026 — Phase 18: Lifecycle notifications (day-7 encouragement + day-28 auto-extend)*

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
| 5 — UI Polish | ✅ Complete | 13-screen interactive prototype, iOS animations |
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
| 12b — Phone Save Fix & SMS Polish | ✅ Complete | Finder phone now saved reliably (awaited, was fire-and-forget); E.164 normalization on PATCH; honest copy when finder has no phone; self_outreach flag differentiates button paths; duplicate reunion guard |
| 13 — Match Screen Polish & Match Quality | ✅ Complete | Match screen layout, location emphasis, smart reasons, color-aware matching |
| 14a — Photo Storage & Lightbox | ✅ Complete | Finder photos uploaded to Supabase Storage; `photo_url` on items; match card thumbnail + confirmed screen show real photo; tap-to-expand lightbox with spring animation and claim/reject CTAs |
| 14b — Attribute Correction + Loser Location | ✅ Complete | Inline attribute editor on finder-done screen; `PATCH /items/{id}/attributes` re-embeds on save; loser "Where?" field geocoded via Nominatim — no new screens, 0 extra taps in happy path |
| 15 — Loser Attribute Correction | ✅ Complete | "Looking for: wallet · brown · leather" summary line on waiting screen; "Don't like description?" expands inline edit panel; saves via `PATCH /items/{id}/attributes`, re-embeds, updates title, fires immediate re-poll |
| 16 — Admin / Ops Dashboard + Live Map | ✅ Complete | `/admin`: multi-user login (JWT, `ADMIN_USERS` env var), 4 stat cards, time filters, 5-tab table (Lost · Found · Reunions · Tips · Debug Matcher), Deactivate + Extend 30d actions, expiring-soon alert. `/map`: full-screen Leaflet dark map, blue finder pins, pulsing red loser pins, clustered markers, rich popups with photo/details. Both use DM Sans + DM Serif Display (same as app). |
| 17a — Post-Reunion Resolve Page + Tip Flow | ✅ Complete | `/resolve/{loser_item_id}`: standalone page linked from handoff SMS. States: question → tip (Stripe inline, $5/$10/$20, skip) → done/tipped. Marks both items inactive + closes reunion record on confirm. In-app tip (`screen-reunion`) restored while Twilio A2P pending — resolve page activates automatically once SMS works. |
| 17b — UI Cleanup | ✅ Complete | Dynamic Island placeholder removed (HTML, CSS, JS function + all call sites — 127 lines deleted). Green circle check icons removed from `screen-finder-done` and `screen-confirmed` — both screens now lead directly with DM Serif Display title. |
| 18 — Lifecycle Notifications | ✅ Complete | Day-7 encouragement SMS + day-28 auto-extend SMS for unmatched loser items. No expiry concept exposed to users. Items with active reunions skipped. Multi-item users stagger across daily runs (one message per phone per run). GitHub Actions cron — no external services beyond what's already running. |

---

## What's Running

| Thing | URL |
|---|---|
| **Live API (Railway)** | `https://lofo-ai-production.up.railway.app` |
| **Live app (GitHub Pages)** | `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html` |
| **Admin dashboard** | `https://lofo-ai-production.up.railway.app/admin` |
| **Live map** | `https://lofo-ai-production.up.railway.app/map` |
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
| `POST /match` | Cosine similarity + Haversine proximity match; threshold 0.78; color compatibility post-filter |
| `POST /verify` | Claude fuzzy-matches finder's `secret_detail` against loser's `loser_claim`; returns `{verified, reason}` |
| `POST /handoff/validate` | Validate single-use JWT handoff token |
| `PATCH /items/{id}/finder-info` | Save finder's `finder_email`, `secret_detail`, and/or `phone` after item creation |
| `PATCH /items/{id}/loser-info` | Save loser's `phone` so they can receive match notifications |
| `PATCH /items/{id}/attributes` | Update `item_type`, `color`, `material`, `size`, `features` + re-embed immediately; works for finder and loser items |
| `POST /tip/create-payment-intent` | Create Stripe PaymentIntent; routes via `transfer_data` to finder's Connect account if set, falls back to platform-held |
| `POST /stripe/webhook` | Mark tip `completed` on `payment_intent.succeeded` |
| `POST /sms/send-otp` | Send 6-digit OTP via Twilio Verify |
| `POST /sms/verify-otp` | Validate submitted OTP; returns `{verified: bool}` |
| `POST /handoff/coordinate` | Save loser phone + create reunion record + fire relay-style SMS to both parties (no raw numbers shared) |
| `POST /sms/inbound` | Twilio inbound webhook — relays messages between finder/loser via LOFO's number; config in Twilio console |
| `POST /connect/onboard` | Create Stripe Connect Express account for finder; return onboarding URL *(dormant — not used in UI)* |
| `GET /connect/return` | Post-onboarding redirect → back to frontend *(dormant)* |
| `GET /connect/refresh` | Re-generate expired onboarding link *(dormant)* |
| `GET /health` | Returns `{"status":"ok"}` after `SELECT 1` DB ping — used by UptimeRobot keep-alive |
| `GET /cron/lifecycle?key=` | Daily lifecycle cron — sends day-7 encouragement + day-28 auto-extend SMS to unmatched loser items; key-protected via `CRON_SECRET` env var; triggered by GitHub Actions |
| `GET /admin` | Serves `admin.html` (protected via JWT in page) |
| `POST /admin/login` | Validates username/password against `ADMIN_USERS` env var; returns 24h JWT |
| `GET /admin/stats?period=` | Stat card data: active_lost, active_found, reunions, tips_cents, expiring_7d |
| `GET /admin/items?type=&period=` | Up to 200 items with all columns (phone, payout, photo_url, etc.) |
| `GET /admin/reunions?period=` | Reunions joined with finder item for item_type |
| `GET /admin/tips?period=` | Tips joined with both items for item_type labels |
| `PATCH /admin/items/{id}/deactivate` | Sets item status = 'inactive' |
| `PATCH /admin/items/{id}/extend` | Adds 30 days to item expires_at |
| `POST /admin/debug/match` | Takes two item UUIDs; returns similarity, color groups, distance, block reasons, would_match |
| `GET /map` | Serves `map.html` (protected via JWT in page) |
| `GET /admin/map-pins` | All active items with GPS coords for map; includes no_gps_count |

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
| photo_url | varchar | Optional — public Supabase Storage URL for finder's photo (Phase 14a) |
| status | varchar | Default `'active'` |
| expires_at | timestamptz | Default 30 days from creation; auto-extended 30 days by lifecycle cron at day-28 |
| notif_week1_at | timestamptz | Set when day-7 encouragement SMS is sent; prevents re-send |
| notif_week2_at | timestamptz | Set when day-28 auto-extend SMS is sent; prevents re-send |
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
| `admin.html` | Admin/ops dashboard — login, stat cards, tables, debug matcher |
| `map.html` | Full-screen live map — Leaflet, CartoDB dark tiles, clustered pins |
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

**Railway environment variables:** `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_VERIFY_SID`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_URL`, `ADMIN_USERS`, `CRON_SECRET`

**GitHub Secret (for lifecycle cron):** `LIFECYCLE_CRON_URL` = `https://lofo-ai-production.up.railway.app/cron/lifecycle?key=YOUR_CRON_SECRET`

**`ADMIN_USERS` format** (JSON string in Railway Variables):
```
{"marc": "yourpassword", "alice": "herpassword"}
```
Add/remove users by editing this variable and redeploying. No code changes needed.

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

## What's Next: Phase 18+

**Phase 18 complete and deployed.** Lifecycle notifications live. All setup steps done.

### Pre-Launch Requirements

- **Twilio A2P 10DLC registration:** Campaign SID `CM50255157d8c0965b92369a1f90b3ab2b` — status **In progress** with TCR/carrier review as of March 12, 2026. Was already submitted previously (not lost). Approval expected within 2–3 weeks. Once approved, `+15175136672` will send to any US number without carrier filtering. No code changes needed.

> **⚠️ When A2P is approved — revisit the tip flow:**
> `resolve.html` and its backend endpoints (`GET /resolve/{id}`, `GET /resolve/{id}/data`, `POST /resolve/{id}/confirm`) are already built and deployed. The handoff SMS already includes the resolve link. Once SMS delivery works:
> 1. Test the full resolve flow end-to-end (see Phase 17a session notes for test steps)
> 2. Consider moving the in-app tip back to post-reunion (Direction 2 from the design discussion) — or keep both as a belt-and-suspenders approach (in-app tip + resolve page as second chance)
> 3. The resolve page also handles **item closure** (marks both items inactive) — this is the only way items currently get closed before their 30-day expiry, so it's worth making prominent in the SMS copy once it works

### Candidates for Phase 18+

- **Item lifecycle UI — extend** — *(Phase 18 handles this automatically via cron — no user action needed. Resolved.)*
- **Loser location post-submit correction** — `PATCH /items/{id}/location` endpoint so the loser can update where they lost the item after the fact. Small backend + small UI addition.
- **Map in app flow** — Leaflet pin-drop screen in the loser flow between `screen-lost-prompt` and submission, for users who type vague locations ("somewhere near downtown"). Would improve geocoding accuracy. Medium effort.
- **Admin map enhancements** — filter map pins by time period (matching the dashboard's time filter), draw a 10-mile radius circle around a selected pin to visualize the match zone, show a line between matched finder+loser pairs.
- **Map as admin tab** — embed the live map as a 6th tab in the admin dashboard instead of a separate page. Eliminates auth/sessionStorage issues entirely and keeps everything in one place.

### Known Intentional Limitations

- Finder payout is manual — tips land in LOFO's Stripe balance; admin must look up `finder_payout_handle` in DB and send payment manually. Stripe Connect (dormant code in `main.py`) is the long-term fix but requires business verification.
- Admin users are plaintext passwords in an env var. Fine for a personal ops tool, but should be hashed if more people get access.

---

## Cursor Prompt for Next Session

> "I'm building LOFO.AI — a lost and found matching app. The project is at `~/Desktop/lofo-ai`. Read `LOFO_AI_Progress.md` first for full context.
>
> **What's complete and deployed (Phases 1–18):**
> Live API at `https://lofo-ai-production.up.railway.app`, frontend at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`. Full end-to-end loop working. Admin dashboard at `/admin`, live map at `/map`. UptimeRobot keep-alive on GET /health every 10 min — no cold starts. Lifecycle cron running daily via GitHub Actions.
>
> **Phase 18 (last session):**
> - Lifecycle notifications fully built and deployed: `GET /cron/lifecycle?key=` endpoint, day-7 encouragement SMS + day-28 auto-extend SMS for unmatched loser items. GitHub Actions cron (`.github/workflows/lifecycle-cron.yml`, 10am ET daily). DB migration done (`notif_week1_at`, `notif_week2_at` columns on items). All env vars set. First manual test run: green ✅.
> - Twilio A2P 10DLC: campaign was already submitted (not lost). Campaign SID `CM50255157d8c0965b92369a1f90b3ab2b`, status In Progress with TCR. Awaiting carrier approval — no code changes needed when approved.
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector + Supabase Storage, Stripe, Twilio. Deployed on Railway.
>
> **Frontend:** `LOFO_MVP.html` (app), `admin.html` (ops dashboard), `map.html` (live map), `resolve.html` (post-reunion closure page).
>
> **DB schema:** `items` (includes `photo_url`, `notif_week1_at`, `notif_week2_at`), `tips`, `reunions`.
>
> **SMS:** Code-complete, pending Twilio A2P carrier approval. Read the ⚠️ block in 'Pre-Launch Requirements' for what to do when approved.
>
> **Keep-alive:** UptimeRobot pings `GET /health` every 10 min — Railway stays warm, no cold starts.
>
> **Today's goal:** [describe what you want to work on]. Read the 'What's Next: Phase 18+' section in the progress doc before starting.
>
> Start by reading `main.py` and `LOFO_AI_Progress.md`, then discuss before building."

---

## Session History

### Phase 18 — Lifecycle Notifications — March 12, 2026

**What changed:** Automated SMS lifecycle touchpoints for unmatched loser items. No expiry concept exposed to users.

**Design decisions:**
- Users never see the words "expiry" or "expires" — items just silently auto-extend
- No reply mechanic (KEEP/STOP was considered and rejected — breaks with multiple active items)
- Multi-item users: one message per phone per cron run; subsequent items picked up next day's run, naturally staggered
- Items with an active reunion record are skipped (they're already in the connected flow)
- GitHub Actions for scheduling — free, no new external services, manually triggerable from the Actions UI

**Backend (`main.py`):**
- `_CRON_SECRET = os.getenv("CRON_SECRET", "")` added to module-level env vars
- `GET /cron/lifecycle?key=` endpoint — key-protected, returns `{ok, sent_week1, sent_week2, skipped_multi_item}`
- Day-7 query: active loser items, phone set, `notif_week1_at IS NULL`, created 6–9 days ago, no active reunion
- Day-28 query: active loser items, phone set, `notif_week2_at IS NULL`, created 27–31 days ago, no active reunion
- Day-28 send also runs `UPDATE items SET expires_at = expires_at + INTERVAL '30 days'`
- `phones_messaged` set prevents same phone getting two messages in one run

**DB migration (run in Supabase SQL editor):**
```sql
ALTER TABLE items
  ADD COLUMN IF NOT EXISTS notif_week1_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS notif_week2_at TIMESTAMPTZ;
```

**GitHub Actions (`.github/workflows/lifecycle-cron.yml`):**
- Schedule: `0 14 * * *` (10am ET / 2pm UTC daily)
- `workflow_dispatch` enabled for manual test runs
- `LIFECYCLE_CRON_URL` stored as GitHub Secret (never in code)
- Non-200 response fails the run (visible in Actions tab)

**SMS copy:**
- Day 7: `"LOFO: Still on it. Your [wallet] report is active and we're watching. Good things take time — we'll reach out the moment something turns up."`
- Day 28: `"LOFO: One month in on your [wallet] — still no match, but we've extended your search automatically. Miracles happen. Got it back another way? Close your report: [resolve_link]"`

**Setup required (one-time):**
1. Run DB migration in Supabase SQL editor
2. Add `CRON_SECRET=your-random-secret` to Railway env vars + local `.env`
3. Add GitHub Secret: `LIFECYCLE_CRON_URL` = `https://lofo-ai-production.up.railway.app/cron/lifecycle?key=your-random-secret`
4. Deploy to Railway

---

### Phase 17b — UI Cleanup — March 11, 2026

**What changed:** Visual polish and dead code removal. No backend changes.

**Dynamic Island (`LOFO_MVP.html`):**
- Removed the black pill placeholder entirely — HTML element, all CSS (`.dynamic-island`, `.island-content`, `.island-dot`, `.island-text`, `@keyframes islandPip`, expanded states), `setIsland()` JS function, and all 4 call sites (`setIsland('off')` on home, every non-match screen, and `setIsland('match', pct)` + dismiss timeout on match screen). 127 lines deleted.
- Was always a design prop; no functional purpose. Will reconsider if/when a native Swift app is built.

**Green check icons (`LOFO_MVP.html`):**
- Removed `<div class="done-icon">✓</div>` from `screen-finder-done` — the green circle badge felt generic/Material Design against the cream background. DM Serif Display title ("Nice one. We've got it.") leads directly now.
- Removed `<div class="confirmed-icon">✓</div>` from `screen-confirmed` — same issue, same fix. Title ("It's yours. Confirmed.") leads directly.
- Removed `.done-icon` and `.confirmed-icon` CSS blocks.

---

### Phase 17a — Post-Reunion Resolve Page + Tip Flow — March 11, 2026

**What changed:** Moved the tip from the in-app flow (pre-physical-reunion) to a standalone resolve page (post-physical-reunion). Full item lifecycle closure.

**Design decision:** Removed in-app `screen-reunion` tip prompt — it was asking the loser to pay before they had their item in hand. Tip now lives exclusively on `/resolve/{loser_item_id}`, linked from the handoff SMS. More honest UX: you pay after the service is complete.

**Backend (`main.py`):**
- `GET /resolve/{loser_item_id}` — serves `resolve.html`
- `GET /resolve/{loser_item_id}/data` — returns loser item type + finder item info (payout handle/app) via reunion lookup; `already_closed: true` if item is inactive
- `POST /resolve/{loser_item_id}/confirm` — marks loser item inactive; finds reunion record → marks finder item inactive + reunion status = 'closed'; body accepts `tip_amount_cents` (informational)
- `POST /handoff/coordinate` — resolve link appended to loser's confirmation SMS: "Once you've got it back, close the report (and tip if you'd like): [link]"

**Frontend (`resolve.html` — new file):**
- Standalone LOFO-branded page (DM Sans + DM Serif Display, cream bg, white card)
- States: `loading` → `question` ("Did you get your [wallet] back?") → `tip` (Stripe inline, $5/$10/$20, skip link) → `done` / `tipped` / `notyet` / `closed` / `error`
- Shows finder's payout handle (Venmo/PayPal/Cash App/Zelle) in tip state if set
- Calls existing `POST /tip/create-payment-intent` + Stripe `confirmCardPayment` (same flow as before, just on a new page)
- On payment success or skip → `POST /resolve/{id}/confirm` → done state

**Frontend (`LOFO_MVP.html`):**
- `screen-reunion` repurposed: stripped Stripe/tip UI, replaced with "You're all set. We'll be in touch." terminal — body text dynamically sets item label from `state.matchedItem.item_type`
- `screen-thanks` left in DOM but unreachable from active flow (harmless dead screen)

---

### Keep-alive + Map Bug Fixes — March 11, 2026

**What changed:** Infrastructure fixes to keep Railway alive and resolve the map not loading.

**Keep-alive (`main.py`):**
- `GET /health` endpoint added — returns `{"status": "ok"}` after pinging the DB with `SELECT 1`. Used with UptimeRobot (free tier, 10-min interval) to prevent Railway cold starts.

**DB connection resilience (`database.py`):**
- TCP keepalives added to psycopg2 pool (`keepalives=1`, `keepalives_idle=30`, `keepalives_interval=5`, `keepalives_count=5`) so stale sockets after cold restarts are detected quickly.
- `_is_conn_alive()` check added to `get_connection()` — validates pooled connection with `SELECT 1` before use; replaces dead connection with a fresh one rather than hanging.

**Map cold-start UX (`map.html`):**
- Auto-retry loop: up to 4 attempts, 30s timeout each (Railway cold start measured at ~23s). Shows "Server waking up… retrying (Xs)" during retries. Manual "Try Again" button only appears after all retries exhausted.

**Map TDZ crash fix (`map.html`):**
- Root cause of map never loading: `let map`, `let clusters`, `let allPins`, `let _retryCount`, `const _MAX_RETRIES` were all declared *after* `initMap()` was called — hitting JavaScript's temporal dead zone. Safari threw `ReferenceError: Cannot access 'map' before initialization` immediately, preventing any fetch from ever running. Fixed by hoisting all `let`/`const` declarations to the top of the script block.

**UptimeRobot:** configured at `https://lofo-ai-production.up.railway.app/health`, 10-minute interval, email alerts on.

---

### Phase 16 — Admin Dashboard — March 11, 2026

**What changed:** Full admin/ops dashboard at `/admin`.

**Backend (`main.py`):**
- `import math` + `timedelta` + `Depends` added
- `_COLOR_GROUP_NAMES` list added alongside `_COLOR_GROUPS` for human-readable group names in debug output
- `ADMIN_USERS` env var (JSON dict `{"username": "password"}`) parsed at startup
- `_create_admin_token(username)` — issues a 24h JWT with `role: admin` claim, signed with existing `JWT_SECRET`
- `_verify_admin(request)` — FastAPI dependency; validates Bearer token, checks `role == admin`
- `_admin_period_filter(period, col)` — returns safe SQL INTERVAL snippet for today/week/month/all
- `GET /admin` — serves `admin.html`
- `POST /admin/login` — validates against `_ADMIN_USERS`, returns JWT + username
- `GET /admin/stats?period=` — 5 metrics: active_lost, active_found, reunions (in period), tips_cents (in period), expiring_7d
- `GET /admin/items?type=&period=` — up to 200 items with all columns inc. phone, payout, photo_url
- `GET /admin/reunions?period=` — reunions joined with finder item for item_type
- `GET /admin/tips?period=` — tips joined with both items for item_type labels
- `PATCH /admin/items/{id}/deactivate` — sets status = 'inactive'
- `PATCH /admin/items/{id}/extend` — adds 30 days to expires_at
- `POST /admin/debug/match` — takes two item UUIDs; returns similarity score (pgvector), color group breakdown, Haversine distance, block reasons, would_match verdict

**Frontend (`admin.html`):**
- Login screen: username + password → POST `/admin/login` → JWT stored in `sessionStorage`
- Header: LOFO logo + ADMIN badge, time filters, avatar initial, logout button, "🗺 Live Map" link
- Greeting with current date
- 4 stat cards (red/blue/green/yellow), all live from `/admin/stats`; clicking a card jumps to the corresponding table tab
- Orange expiring-soon alert bar (appears when expiring_7d > 0)
- 5-tab panel: Lost Items · Found Items · Reunions · Tips · Debug Matcher
- Sortable column headers (click to toggle ↑/↓) — client-side, sort state resets on tab change
- Time filters update both stat cards and table simultaneously
- Photo thumbnails (click to open full size), masked phones (+1 ••• ••• 1234)
- Deactivate: confirms, updates row in place; Extend: refreshes table
- Debug panel: UUID inputs → match verdict card + 3 metric tiles + color breakdown + block reasons + item cards
- Accent color: `#60A5FA` blue (matches app); semantic status pills (active green / inactive red) unchanged
- Fonts: DM Sans body, DM Serif Display for "LOFO" branding (same as main app)

**Live Map (`map.html`) — Phase 16 addition:**
- Full-screen Leaflet map, CartoDB Dark Matter tiles (no API key needed)
- Two marker styles: blue circle pins (finders) + pulsing red pins (losers)
- Leaflet.MarkerCluster for density management
- Popups: photo thumbnail (if present), item type badge, attributes, GPS coords, created date, item ID
- Floating header (LOFO branding + "Live Map" label), floating legend, item count badge
- Admin auth: reads JWT from `sessionStorage`, redirects to `/admin` if missing/expired
- Cold-start handling: 5s `wakeTimer` shows "Server waking up…" message; 60s `AbortController` hard timeout; on failure shows error message + "Try Again" button + "← Back to Admin" link

---

### UX Polish — March 10, 2026

**What changed:** Copy cleanup + camera location UX. No new features, no backend changes.

**Copy fixes:**
- Camera AI overlay: "Reading your photo…" → "Reviewing photo…"
- Lost item submit: two-step "Describing your item…" → "Searching for matches…" collapsed into single "Searching for your item…" for both loading states

**Camera screen location:**
- Removed the Dynamic Island "Location on · live" expansion from the camera screen — redundant with the bottom geo row
- Bottom geo row now reverse geocodes device GPS via Nominatim and shows the actual location: city, state abbreviation (extracted from `ISO3166-2-lvl4`), and zip code (e.g. "San Francisco, CA 94110") instead of the generic "Location acquired"
- Text brightens to `rgba(255,255,255,0.75)` on confirmed location
- Fallback to "Location acquired" if geocode fails

**Waiting screen attr section fixes:**
- Removed extra wrapper div — flattened structure so edit panel is full-width matching status pills
- "Don't like description?" line split into static muted text + navy underlined "Fix it →" clickable span (same pattern as finder-done screen)
- Bumped font-size to 13px, weight to 400 for readability
- Left-aligned with `padding: 0 2px` to match "Looking for:" row above
- Added `padding-top: 24px` to "Nothing nearby yet…" section for clear visual separation

---

### Phase 15 — March 10, 2026

**What changed:** Loser attribute correction on the waiting screen. Zero new screens, zero extra taps in happy path.

- `state.loserItem` added — stores the full item object returned from `/items/from-text`, used as source of truth for the edit panel (mirrors `state.finderItem` from 14b).
- `submitLost()` now saves `state.loserItem = item` after the POST response.
- `screen-waiting`: compact `"Looking for: wallet · brown · leather"` summary line added below the status pills. Always visible when a loser item is in state. "Don't like description?" link expands an inline edit panel.
- Edit panel: same chip/input pattern as finder-done. Item-type text input (pre-filled from Claude), attribute chips with × to remove, add-detail input (Enter or + adds to features), "Update description →" / Cancel.
- Save calls `PATCH /items/{loserItemId}/attributes` (same endpoint used by finder correction), re-renders the summary row, updates the waiting screen title (`"Looking for your wallet."`), closes the panel, and immediately calls `pollForMatch()` so the corrected embedding is tested right away. Toast: "Updated — re-scanning…"
- New JS: `_renderWaitingAttrSummary()`, `toggleLoserAttrEdit()`, `_renderLoserEditTagChips()`, `_removeLoserEditChip()`, `addLoserEditTag()`, `saveLoserAttrEdits()`, `_loserEditAttrs` working copy variable.
- CSS: `.waiting-attr-section`, `.waiting-attr-summary`, `.waiting-attr-summary-label`, `.waiting-attr-tags-inline`, `.waiting-attr-fix`, `.waiting-attr-edit-panel`. Reuses existing `.attr-edit-panel`, `.tag-removable`, `.tag-x`, `.attr-edit-save-btn`, `.attr-cancel-link`.

---

### Phase 14b — March 10, 2026

**What changed:** Attribute correction flow + loser location fix. Zero new screens, zero extra taps in the happy path for either feature.

**Attribute correction (finder flow):**
- `PATCH /items/{id}/attributes` endpoint: accepts `item_type`, `color`, `material`, `size`, `features` (all optional), updates DB, immediately calls `_store_embedding()` so the corrected profile is live for matching. Works for both finder and loser items.
- `state.finderItem` added — stores the full item object returned from photo/text submission, used as source of truth for the edit panel.
- `renderFinderDone()` now saves `state.finderItem = item` and resets the edit panel between submissions.
- `screen-finder-done`: "AI got it wrong? Fix it →" muted link added below the tag row. Tapping expands an inline edit panel (no new screen). Panel shows: item-type text input (pre-filled), all attribute chips with × to remove, add-detail input (Enter or + adds to features), Save + Cancel. Save calls `PATCH /items/{id}/attributes`, re-renders the card on success, collapses panel.
- New JS functions: `toggleAttrEdit()`, `_renderEditTagChips()`, `_removeEditChip(type, idx)`, `addEditTag()`, `saveAttrEdits()`.

**Loser location fix:**
- `TextItemCreate.where_description: Optional[str]` — new optional field.
- `_geocode(location_text)` helper: synchronous Nominatim (OpenStreetMap, no API key) call via httpx. Returns `(lat, lng)` or None. 4s timeout, exceptions swallowed. User-Agent header set per OSM usage policy.
- `create_item_from_text`: if `where_description` is provided, geocodes it. If geocoding succeeds, uses those coords instead of device GPS. Device GPS still passed as fallback in case geocoding fails or `where_description` is empty.
- `screen-lost-prompt`: "📍 Add location" and "🕑 Add time" placeholder chips replaced with a real optional text input: "Where did you lose it?" with placeholder "e.g. JFK Terminal 4, Central Park, 5th & Broadway…". The value is passed as `where_description` in `submitLost()`.

**Partial address enrichment (same session, follow-up):**
- `_enrichPartialAddress(text, lat, lng)` helper in frontend — runs at submit time.
- Heuristic: if `where_description` starts with digits AND has no comma AND no trailing 2-letter state code → looks like a street-only address (e.g. `"1679 45th Ave"`).
- If partial: calls Nominatim reverse geocode on device GPS coords → extracts `city` + `state` from result → appends to text: `"1679 45th Ave, San Francisco, California"`.
- Updates the input field visually so user sees the resolved address before loading begins.
- Fully silent fallback: if GPS unavailable, Nominatim fails, or heuristic doesn't fire → original text passes through unchanged.
- Generic place names (`"Central Park"`, `"JFK Terminal 4"`) bypass enrichment entirely — no leading digit, no change.

---

### Phase 14a — March 10, 2026

**What changed:** Photo storage end-to-end + tap-to-expand lightbox on match screen.

**Photo storage (backend):**
- Added `httpx` to `requirements.txt` for async uploads
- `SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_URL` added as env vars (Railway + `.env`)
- Project URL derived from `DATABASE_URL` via regex (pooler + direct formats); explicit `SUPABASE_URL` takes priority
- `_upload_photo(item_id, image_bytes)` async helper: uploads JPEG to `item-photos` Supabase Storage bucket, returns public URL or None on failure (non-blocking)
- `create_item_from_photo()`: after INSERT + embed, calls `_upload_photo()`, then `UPDATE items SET photo_url = ...`
- `photo_url: Optional[str] = None` added to `ItemResponse`, `MatchResponse`, `_INSERT_SQL` RETURNING, `_SELECT_SQL`, `_MATCH_SQL`
- DB migration applied: `ALTER TABLE items ADD COLUMN IF NOT EXISTS photo_url VARCHAR`

**Photo display (frontend):**
- **Match card**: if `photo_url` set, replaces emoji in `.item-thumb` with `<img>`; thumb gets `.tappable` class with sonar ring (hot pink, `#F441A5`, expands outward on 1.8s cycle) + pointer cursor; "Tap the photo to see it full size →" hint text below card
- **Confirmed screen**: `#confirmed-photo-wrap` full-width 190px photo preview added between subtitle and item card; shown when `photo_url` present, hidden otherwise
- **Photo lightbox**: full-screen overlay (`z-index: 800`) that slides up from bottom with spring (`cubic-bezier(0.34, 1.28, 0.64, 1)`); dark blurred backdrop; 440px photo; cream action area below with location/time eyebrow, "Is this your [item]?" headline, "That's mine →" and "Not mine" buttons; backdrop tap or ✕ dismisses; `openLightbox()` / `closeLightbox()` functions; claim button wired to ownership-verify or confirmed based on `has_secret`

---

### Phase 13 — March 9, 2026

**What changed:** Match screen layout polish + match quality improvements.

**Match screen — layout & visual (frontend):**
- Added proper `.status` bar inside the navy `.match-banner` (time + signal dots at rgba(255,255,255,0.35)) so the screen has the same top structure as all other screens. Banner no longer uses `s-item` as a whole block — the navy background appears immediately on slide-in; eyebrow (delay=0), h2 (delay=60ms), and confidence bar (delay=140ms) stagger in individually.
- Eyebrow opacity raised from 0.30 → 0.55 so "GOOD NEWS" label is readable against navy.
- `#screen-match` background changed from white (`#fff`) to `var(--cream)`, consistent with `screen-finder-done` and `screen-waiting`. Match card flips to white with a border (same treatment as item cards on other cream screens).
- New `.match-location-row` pill between the card and reasons list: "📍 X mi away · found Y ago". Distance < 0.1 mi shows "Same area." Only appears when both items had GPS coordinates (distance_miles not null). Card meta now shows physical attributes (material · size) instead of duplicating the distance.
- Dynamic Island auto-dismisses after 3.5 seconds on match screen instead of staying expanded until navigation.

**Match screen — smart reasons (frontend):**
- `state.loserDescription` added to app state. `submitLost()` stores the loser's original description text before the API call.
- On match screen entry, reasons are built with two helper functions (`_mentionedVals`, `_mentionedStr`) that check if each attribute word appears in `state.loserDescription`. For loser context: color/material/size only show as reasons if the loser explicitly typed those words. For finder context: all attributes on the finder's item are shown (since the finder physically observed them).
- Proximity (distance_miles) added as the **first** reason in the checklist ("Nearby — X mi away" / "Nearby — Same area") — always shown when GPS data is available, regardless of what the loser described, since it's captured automatically and is a strong objective signal.
- Fallback: if no specific attribute reasons match, shows `"X% AI match score"` so the list is never empty.

**Match quality — color filtering (backend):**
- Similarity threshold raised: 0.70 → 0.78 in `/match` endpoint and both `_NOTIFY_LOSER_SQL` / `_NOTIFY_FINDER_SQL` notification helpers.
- Added `_colors_compatible()` and `_COLOR_GROUPS` helper in `main.py`. Maps ~60 named colors into 10 hue families (red, orange, yellow, green, blue, purple, brown, white, black, gray). After SQL match, applies post-filter: if both items have recognized non-neutral colors that share no hue group in common, the match is rejected regardless of embedding score. Key behaviors: navy + silver → rejected (blue group vs gray group); navy + dark blue → allowed (both blue); silver + black → allowed (gray group is "neutral," pairs with anything); unrecognized/empty colors → match allowed (fail open).
- **Important:** empty `loser_colors` (loser didn't mention color) short-circuits the filter — the condition is `loser_colors AND finder_colors AND not compatible`, so empty loser colors always passes. Confirmed via live test: "portable reading light" (no color) correctly matched "portable book/reading light" (black) at 94.9%.

---

### Phase 12b — March 9, 2026

**What changed:** Finder phone save reliability fix + SMS relay polish.

**Root cause of missing phones:** `verifyCode()` saved the finder's phone via fire-and-forget `fetch().catch(() => {})`. Any failure (network blip, null `state.finderItemId`, anything) was silently swallowed. Result: every finder item in the DB had `phone = NULL`, so `coordinateHandoff` always took the no-phone branch.

**Fixes:**
- `verifyCode()` phone save is now `await`ed with a `console.warn` if it fails — no longer silent
- `PATCH /items/{id}/finder-info` now normalizes phone to E.164 (`+1XXXXXXXXXX`) on write, so DB always stores a consistent format regardless of what the user typed
- Honest SMS copy when finder has no phone: "The finder didn't leave a number, but they may still have the item" instead of the false "We've notified the finder"
- `coordinateHandoff(selfOutreach)` now takes a boolean flag: primary button passes `false` ("Notify us both"), ghost button passes `true` ("I'll reach out"). Loading spinner and SMS copy differ accordingly
- Duplicate reunion guard: checks for active reunion before INSERT so double-tapping doesn't create duplicate rows

**SMS debugging:** Traced the full SMS failure path. Twilio `messages.create()` was reaching the API but carriers were blocking delivery with error `30034` (A2P 10DLC compliance). OTP works because Twilio Verify bypasses carrier registration requirements. Regular messaging (`_sms()`) requires A2P registration. User submitted A2P 10DLC campaign registration (Brand: LOFO AI, Sole Proprietor) — pending carrier approval (2–3 weeks). No code changes needed once approved.

---

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

*Built with Cursor + Claude. Zero prior coding experience. March 5–9, 2026.*
