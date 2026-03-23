# LOFO.AI — Build Progress & Context
*Last updated: March 23, 2026 — School app: subscriber alert throttle, thinking screen iOS upgrade, admin card fixes.*

> **Two numbering systems — here's how they work:**
> - **Phases 1–26+** = the full project roadmap (backend + web + iOS). Used in the Phase Roadmap table below.
> - **iOS Phases A–G** = the iOS-only build plan. Used in the "SwiftUI iOS App" section below. Each iOS phase maps to a project phase (iOS Phases A–D = Project Phase 23; iOS Phase E = Project Phase 24, etc.)
> - When working on the **iOS app**, use the A–G labels. When talking about the **overall project**, use the 1–26 numbers.

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
| 19 — Map as Admin Tab + Enhancements | ✅ Complete | Live map embedded as 6th tab in admin dashboard. Period filter drives map pins + pairs. 10-mile radius circle on pin click. Dashed green lines connecting matched reunion pairs (toggleable). No separate page navigation — all in one auth context. Admin table rows clickable — expand inline to show full item detail (photo, all attributes, GPS, full timestamps, phone, payout, item ID). |
| 20 — In-App Menu Drawer | ✅ Complete | Gear icon (white circle) top-right of home screen. Slide-up sheet: My Usage (user-level lost/found/reunited from localStorage item IDs), Support (FAQ accordion + Contact Us email form), Information (Terms, Privacy, About, App Version). Backend: `GET /terms`, `GET /privacy`, `GET /stats/by-items`. App Store ready. |
| 21 — Bug Fixes & Hardening | ✅ Complete | 8 bugs fixed: loser phone normalization, DB pool corruption, resolve page false-success, unbounded stats IDs, JWT_SECRET crash, XSS hardening (all frontends), photo URL validation, absolute API paths in admin/map. Admin UX: minimal underline tabs, clickable geo coords zoom to item on map. |
| 22 — Admin Charts & Mobile | ✅ Complete | Two chart cards: Lost vs Found bar chart (daily, current week) + Avg Time to Reunion line chart (weekly trend, month-over-month delta, active matches). `GET /admin/charts` endpoint. Blank map fix (Leaflet `invalidateSize`). Full mobile responsive layout (900px + 540px breakpoints). |
| 23 — SwiftUI App Skeleton *(iOS Phases A–D)* | ✅ Complete | Native iOS app at `~/Desktop/LOFO/`. 28 Swift files: full design system, API client, all screens wired for both finder and loser flows. Targets iOS 17+. |
| 24 — iOS Phase E: First Build *(iOS Phase E)* | ✅ Complete | LoserWaitView (breathing orb), TipView ($5/$10/$20 + skip → backend), DM Sans + DM Serif Display fonts bundled via Core Text, compile errors fixed, BUILD SUCCEEDED on iPhone 17 Pro simulator. |
| 25 — iOS Phase F: Push Notifications + Stripe *(iOS Phase F)* | ✅ Complete | PushManager, AppDelegate, `POST /devices/register`, APNs push in notify helpers, Stripe PaymentSheet + Apple Pay wired with `#if canImport(StripePaymentSheet)` guard. |
| 26 — iOS Phase G: App Store Prep + TestFlight *(iOS Phase G)* | ✅ Complete — TestFlight Live | App icon 1024×1024, LaunchScreen.storyboard, bundle ID `ai.lofo.app`, version `1.0.0`, portrait-only. Build 1.0.0 (1) on TestFlight. Internal group active. ReunionView + TipView redesigned (Phases 26q/26r). |

---

## What's Running

| Thing | URL |
|---|---|
| **Live API (Railway)** | `https://lofo-ai-production.up.railway.app` |
| **Live app (GitHub Pages)** | `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html` |
| **Admin dashboard** | `https://lofoapp.com/admin` (proxied via Vercel → Railway) |
| **Live map** | `https://lofoapp.com/map` (proxied via Vercel → Railway) |
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
| `PATCH /items/{id}/redescribe` | Re-parse free-text details through Claude → intelligently maps natural language to structured DB columns + re-embeds. Used by iOS edit sheet so user edits are AI-parsed, not stored verbatim. |
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
| `GET /admin/map-pins?period=` | Active items with GPS coords for map, period-filtered; includes no_gps_count |
| `GET /admin/map-pairs?period=` | Reunion pairs where both items have GPS, for drawing match lines on map |
| `GET /terms` | Serves `terms.html` — Terms of Service |
| `GET /privacy` | Serves `privacy-policy.html` — Privacy Policy |
| `GET /stats/by-items?ids=` | User-level stats: `{lost_count, found_count, reunited_count}` for comma-separated item UUIDs (no auth) |

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

**Matching engine — redesigned (March 19, 2026):**
New 5-stage pipeline deployed. See Session History (March 19, 2026 — Matching Engine Redesign) for full details. Key changes: item_type is now a hard categorical gate (not a threshold raise), embeddings are attribute-only (no item_type in text), LIMIT 50 retrieval, Cohere Rerank stage C, composite final_score = 0.55·reranker + 0.20·cosine + 0.15·color + 0.10·features, dynamic threshold by query richness. **After deploying: add `COHERE_API_KEY` to Railway env vars, then hit "Re-embed All →" in admin Debug tab.**

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

## What's Next: Phase 22+

**Phases 1–22 complete and deployed.**

### Pre-Launch Requirements

- **Twilio A2P 10DLC registration:** Campaign SID `CM50255157d8c0965b92369a1f90b3ab2b` — status **In progress** with TCR/carrier review as of March 12, 2026. Approval expected within 2–3 weeks. Once approved, `+15175136672` will send to any US number without carrier filtering. No code changes needed.

> **⚠️ When A2P is approved — revisit the tip flow:**
> `resolve.html` and its backend endpoints (`GET /resolve/{id}`, `GET /resolve/{id}/data`, `POST /resolve/{id}/confirm`) are already built and deployed. The handoff SMS already includes the resolve link. Once SMS delivery works:
> 1. Test the full resolve flow end-to-end (see Phase 17a session notes for test steps)
> 2. Consider moving the in-app tip back to post-reunion (Direction 2 from the design discussion) — or keep both as a belt-and-suspenders approach (in-app tip + resolve page as second chance)
> 3. The resolve page also handles **item closure** (marks both items inactive) — this is the only way items currently get closed before their 30-day expiry, so it's worth making prominent in the SMS copy once it works

---

## SwiftUI iOS App — Active Build Plan

> **Full plan document:** `~/.cursor/plans/swiftui_native_app_transition_e4202362.plan.md`
> This plan was created in session and is the authoritative reference for the native app build. Every future session working on the iOS app should treat this plan + this progress doc as the two sources of truth.

**Project location:** `~/Desktop/LOFO/LOFO.xcodeproj`
**Target:** iOS 17+, SwiftUI, `@Observable`
**Backend:** Unchanged — same Railway API at `https://lofo-ai-production.up.railway.app`

### Architecture (from plan)

- `NavigationStack` with `AppState.path: NavigationPath` — mirrors `flowOrder` from web app. `appState.push(.screen)` = `go('screen-name')`
- `FinderFlowState.shared` + `LoserFlowState.shared` — singleton `@Observable` objects holding per-flow data across screens (equivalent to `state` object in `LOFO_MVP.html`)
- `APIClient.shared` — URLSession wrapper, all endpoints, async/await
- No third-party state libraries. No WebView.
- Admin dashboard + resolve page stay as web-only pages. Pure SwiftUI app.

### Screen Map (HTML → SwiftUI)

| HTML Screen | SwiftUI View | Notes |
|---|---|---|
| `screen-home` | `HomeView` | Root of NavigationStack |
| `screen-finder-camera` | `FinderCameraView` | Push |
| `screen-finder-done` | `FinderDoneView` | Push |
| `screen-phone` | `PhoneVerifyView` | Push |
| `screen-verify` | `OTPVerifyView` | Push |
| `screen-allset` | `AllSetView` | Push |
| `screen-lost-prompt` | `LostPromptView` | Push |
| `screen-waiting` | `WaitingView` | Push |
| `screen-loser-wait` | `LoserWaitView` | Sheet (not yet built) |
| `screen-match` | `MatchView` | Push (match flow) |
| `screen-ownership-verify` | `OwnershipVerifyView` | Push |
| `screen-confirmed` | `ConfirmedView` | Push |
| `screen-reunion` | `ReunionView` | Push |
| Menu drawer | `MenuSheet` | Sheet from HomeView |
| Photo lightbox | `PhotoLightboxView` | fullScreenCover |

### iOS Build Phases (A–G) — Current Status

> These map to overall project phases: A–D = Phase 23, E = Phase 24, F = Phase 25, G = Phase 26.
> **We are currently at iOS Phase G.**

| iOS Phase | Project Phase | Status | What |
|---|---|---|---|
| A — Foundation + Home | 23 | ✅ Done | APIClient, HomeView, MenuSheet, design system, shared components |
| B — Finder Flow | 23 | ✅ Done | FinderCameraView, FinderDoneView, PhoneVerifyView, OTPVerifyView, AllSetView |
| C — Loser Flow | 23 | ✅ Done | LostPromptView, WaitingView (5s polling) |
| D — Match + Reunion | 23 | ✅ Done | MatchView, OwnershipVerifyView, ConfirmedView, ReunionView, PhotoLightboxView |
| E — Stripe + Polish | 24 | ✅ Done | LoserWaitView (breathing orb), TipView ($5/$10/$20 + skip), DM Sans + DM Serif Display fonts, BUILD SUCCEEDED. Stripe PaymentSheet/Apple Pay deferred to Phase F. |
| **F — Push Notifications + Stripe** | **25** | **✅ Done** | PushManager, AppDelegate, `POST /devices/register`, APNs push in notify helpers, Stripe PaymentSheet + Apple Pay via `#if canImport(StripePaymentSheet)` guard, deep link tap handling |
| **G — App Store Prep** | **26** | **✅ Complete + TestFlight Live** | App icon 1024×1024, `LaunchScreen.storyboard`, bundle ID `ai.lofo.app`, version `1.0.0`, portrait-only. Build 1.0.0 (1) uploaded to TestFlight Mar 17, 2026. Internal group created. APNs key + Railway env vars configured. |

### iOS Phase G Checklist (= Project Phase 26) — ✅ COMPLETE (file changes done; manual steps remain)

**What was done by Cursor:**
1. ✅ App icon — 1024×1024 PNG generated (`LOFO` wordmark, navy bg `#1A1A2E`, cream type `#F5F2EC`, Palatino serif, dotted arc motif). Placed in `Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png`. `Contents.json` updated to reference it. Xcode auto-generates all required icon sizes from this single 1024×1024 file.
2. ✅ `LaunchScreen.storyboard` — Created in `LOFO/LaunchScreen.storyboard`. Cream background (`#F5F2EC`), `LOFO` label centered in Palatino Roman 64pt, navy color. No spinner. `PBXFileSystemSynchronizedRootGroup` auto-includes it.
3. ✅ `project.pbxproj` — Updated both Debug + Release target configs:
   - `PRODUCT_BUNDLE_IDENTIFIER`: `com.lofo.LOFO` → **`ai.lofo.app`**
   - `MARKETING_VERSION`: `1.0` → **`1.0.0`**
   - `CURRENT_PROJECT_VERSION`: `1` (unchanged — this is the build number, correct)
   - `INFOPLIST_KEY_UILaunchScreen_Generation = YES` → **`INFOPLIST_KEY_UILaunchStoryboardName = LaunchScreen`**
   - `INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone` → **`UIInterfaceOrientationPortrait`** (portrait-only; App Store requires this be intentional)

**Manual steps before archiving — complete in this order:**

**Step 1 — Supabase DB migration** (if not done from Phase F):
```sql
CREATE TABLE IF NOT EXISTS device_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    phone VARCHAR NOT NULL,
    device_token TEXT NOT NULL,
    platform VARCHAR NOT NULL DEFAULT 'ios',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(phone, device_token)
);
```

**Step 2 — Apple Developer Portal setup:**
- Go to [developer.apple.com](https://developer.apple.com) → Certificates, Identifiers & Profiles
- **App ID**: Identifiers → `+` → App ID → Bundle ID = `ai.lofo.app`. Enable: Push Notifications, Apple Pay.
- **APNs Key**: Keys → `+` → enable "Apple Push Notifications service (APNs)" → Download `.p8`. Note the 10-char Key ID. Note your 10-char Team ID (top-right of portal).
- **Merchant ID**: Identifiers → `+` → Merchant IDs → ID = `merchant.ai.lofo`.
- **Push certificate**: Not needed — backend uses token-based auth (JWT `.p8`) which is simpler and doesn't expire.

**Step 3 — Railway env vars** (for APNs):
Add to Railway → lofo-ai → Variables:
- `APNS_KEY_ID` = your 10-char key ID
- `APNS_TEAM_ID` = your 10-char team ID  
- `APNS_AUTH_KEY` = full contents of the `.p8` file (paste with literal `\n` newlines, or escape them)
- `APNS_BUNDLE_ID` = `ai.lofo.app`
- `APNS_ENVIRONMENT` = `production` (use `sandbox` only for Simulator testing)
Then redeploy Railway.

**Step 4 — Xcode: Stripe SPM + Apple Pay:**
1. Open `~/Desktop/LOFO/LOFO.xcodeproj` in Xcode 26.3
2. **Stripe**: File → Add Package Dependencies → URL: `https://github.com/stripe/stripe-ios` → Add `StripePaymentSheet` target to LOFO
3. In `LOFOApp.init()`, replace `"pk_test_YOUR_STRIPE_PUBLISHABLE_KEY"` with your Stripe live publishable key (`pk_live_...`)
4. **Apple Pay**: Target LOFO → Signing & Capabilities → `+` → Apple Pay → add `merchant.ai.lofo`
5. **Verify signing**: Signing & Capabilities → Team = your team (already in project as `45F4TH223D`). Bundle ID should auto-resolve to `ai.lofo.app`.

**Step 5 — Build & Verify:**
1. Product → Clean Build Folder
2. Select any iPhone simulator → Build (⌘B) — confirm BUILD SUCCEEDED
3. Check launch screen appears correctly on simulator start
4. Check app icon shows in simulator home screen

**Step 6 — Archive for TestFlight:**
1. Select "Any iOS Device (arm64)" as destination (not a simulator)
2. Product → Archive
3. When Organizer opens → Distribute App → App Store Connect → Upload
4. Select options: Strip Swift symbols ✓, Upload symbols ✓, Manage version and build number ✓
5. Click Upload

**Step 7 — App Store Connect listing** ([appstoreconnect.apple.com](https://appstoreconnect.apple.com)):
- My Apps → `+` → New App → Platform: iOS → Name: **LOFO** → Primary Language: English (U.S.) → Bundle ID: `ai.lofo.app` → SKU: `ai.lofo.app`
- **App Information:**
  - Subtitle: `Lost & found, reunited by AI`
  - Category: Utilities (Primary), Lifestyle (Secondary)
  - Privacy Policy URL: `https://lofo-ai-production.up.railway.app/privacy`
  - Support URL: `https://lofo-ai-production.up.railway.app`
- **Description (App Store):**
  ```
  LOFO reunites lost things with their owners using AI.

  Found something? Snap a photo. LOFO reads it in seconds.
  Lost something? Describe it. LOFO watches for a match.

  When the AI finds a connection, you both get notified instantly. Verify ownership, coordinate the return, and optionally tip the finder — all without sharing your number.

  Ten seconds of effort. Everything else is the engine.
  ```
- **Keywords** (100 chars max): `lost,found,lost and found,reunite,missing,wallet,keys,phone,AI,match`
- **What's New in This Version:** `Initial release.`
- **Screenshots** (required: 6.7" iPhone — use iPhone 15 Pro Max or 16 Plus simulator at 1290×2796):
  - Home screen (two CTAs on cream bg)
  - Finder camera / AI result screen
  - Match screen (navy banner + confidence bar)
  - Ownership verify screen
  - Confirmed screen
  - Reunion / all set screen
  - *(Optional: 6.1" — same screens at 1179×2556)*
- **App Review Information:** Demo account not required (no login needed). Add a note: "App uses camera to submit found items and AI to match lost/found pairs. Push notifications alert users to matches. Twilio OTP verifies phone numbers."
- **Build**: Select the build uploaded in Step 6
- **Pricing**: Free
- Submit for Review

**Step 8 — TestFlight (optional, do before App Store submission):**
- After upload in Step 6, the build appears in TestFlight tab in App Store Connect within ~15 min
- Add yourself as Internal Tester → install on device → smoke-test full finder + loser flows
- For External Testing: add group, export compliance (select "no encryption beyond what iOS provides"), submit for Beta App Review

### iOS Phase F Checklist (= Project Phase 25) — ✅ COMPLETE

1. ✅ `PushManager.swift` (new, `Services/`) — `@Observable` singleton. Requests push permission via `UNUserNotificationCenter`, receives APNs token via `AppDelegate`, registers `(phone, device_token)` pair with backend after phone verify. `UNUserNotificationCenterDelegate` shows banners in foreground + broadcasts `.lofoNotificationTap` on tap.
2. ✅ `AppDelegate.swift` (new) — `UIApplicationDelegate` registered via `@UIApplicationDelegateAdaptor`. Receives `didRegisterForRemoteNotificationsWithDeviceToken` → forwards to `PushManager.shared`.
3. ✅ `LOFOApp.swift` — Added `@UIApplicationDelegateAdaptor(AppDelegate.self)`, `.onAppear { PushManager.shared.requestPermission() }`, `.onReceive(.lofoNotificationTap)` deep link handler (pops to root; screen-specific routing via `screen` payload key). Also added Stripe publishable key init under `#if canImport(StripePaymentSheet)`.
4. ✅ `APIClient.swift` — Added `registerDevice(phone:deviceToken:)` → `POST /devices/register`.
5. ✅ `TipView.swift` — Full Stripe `PaymentSheet` + Apple Pay wired under `#if canImport(StripePaymentSheet)`. Uses `withCheckedContinuation` to bridge callback API into async/await. Falls back to direct navigation when Stripe SDK not linked. Merchant ID: `merchant.ai.lofo`.
6. ✅ `OTPVerifyView.swift` — Calls `PushManager.shared.registerWithServer(phone:)` after successful OTP verify (finder flow).
7. ✅ `WaitingView.swift` — Calls `PushManager.shared.registerWithServer(phone:)` after loser phone save.
8. ✅ Backend `main.py` — `DeviceRegisterRequest` schema, `POST /devices/register` endpoint (upserts `device_tokens` table), `_push_apns()` helper (httpx HTTP/2 + PyJWT ES256 auth token), `_get_device_tokens(phone)` lookup, both `_notify_waiting_losers` and `_notify_matched_finder` now send APNs push alongside SMS. APNs payload includes `screen` key for deep linking.
9. ✅ `requirements.txt` — `httpx` → `httpx[http2]` for APNs HTTP/2 transport.

**Backend setup required (one-time) before APNs pushes work:**
1. Run DB migration in Supabase SQL editor:
   ```sql
   CREATE TABLE IF NOT EXISTS device_tokens (
       id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
       phone VARCHAR NOT NULL,
       device_token TEXT NOT NULL,
       platform VARCHAR NOT NULL DEFAULT 'ios',
       created_at TIMESTAMPTZ DEFAULT NOW(),
       UNIQUE(phone, device_token)
   );
   ```
2. In Apple Developer Portal → Certificates, Identifiers & Profiles → Keys → create an APNs key (enable Apple Push Notifications). Download the `.p8` file.
3. Add Railway env vars: `APNS_KEY_ID` (10-char key ID), `APNS_TEAM_ID` (10-char team ID), `APNS_AUTH_KEY` (full `.p8` file contents — paste with `\n` newlines), `APNS_BUNDLE_ID` (e.g. `ai.lofo.app`). Optionally `APNS_ENVIRONMENT=sandbox` for testing.
4. Deploy to Railway.

**Xcode setup required before Stripe PaymentSheet activates:**
1. File → Add Package Dependencies → `https://github.com/stripe/stripe-ios` → add `StripePaymentSheet` target.
2. In `LOFOApp.init()`, replace `"pk_test_YOUR_STRIPE_PUBLISHABLE_KEY"` with your real publishable key (`pk_live_...` for production).
3. For Apple Pay: Signing & Capabilities → + → Apple Pay → add merchant ID `merchant.ai.lofo`. Register the merchant ID at developer.apple.com → Identifiers → Merchant IDs first.

### iOS Phase E Checklist (= Project Phase 24) — ✅ COMPLETE

1. ✅ Fix compile errors — `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` required removing `nonisolated` + `Sendable` from APIClient and models
2. ✅ `LoserWaitView` — breathing orb animation (3 staggered concentric rings), navy fullScreenCover, shown after phone capture in WaitingView
3. ✅ DM Sans + DM Serif Display fonts bundled — downloaded from Google Fonts CDN, placed in `LOFO/Fonts/`, registered via `CTFontManagerRegisterFontsForURL` in `LOFOApp.init()` (no Info.plist change needed)
4. ✅ `TipView` — $5/$10/$20 + skip, calls `POST /tip/create-payment-intent`, then navigates to ReunionView. Stripe PaymentSheet wiring is a TODO comment for Phase F.
5. ✅ `TipView` wired into flow: ConfirmedView → tip → reunion
6. ✅ Stripe iOS SDK — NOT added via SPM (not needed for first build since TipView calls backend directly). Add via Xcode File > Add Package Dependencies when ready to wire Apple Pay.
7. ✅ First simulator build: **BUILD SUCCEEDED** — iPhone 17 Pro, iOS 26.3.1

### Known Intentional Differences from Web App

- `TipView` activates full Stripe `PaymentSheet` + Apple Pay once `StripePaymentSheet` SDK is added via SPM. Without it, navigates to Reunion directly (same as Phase E placeholder). See Phase F checklist for setup steps.
- Push notifications are code-complete but require APNs env vars + DB migration to activate on Railway (see Phase F checklist). Without them, `_push_apns()` logs and returns — SMS continues to work normally.
- `LoserWaitView` is a `fullScreenCover` (not a `.sheet`) from `WaitingView` — deliberate; fits the "modal overlay" feel better than a sheet presentation.

---

### Post-Launch Candidates (Phase 26+)

- **Loser location post-submit correction** — `PATCH /items/{id}/location` endpoint so the loser can update where they lost the item after the fact. Small backend + small UI addition.
- **Map in app flow** — Native pin-drop screen in the loser flow for users who type vague locations. Would improve geocoding accuracy. Medium effort.
- **Finder payout automation** — Replace manual Venmo/PayPal handle lookup with Stripe Connect Express (dormant code in `main.py` already exists; needs business verification).

### Known Intentional Limitations

- Finder payout is manual — tips land in LOFO's Stripe balance; admin must look up `finder_payout_handle` in DB and send payment manually. Stripe Connect (dormant code in `main.py`) is the long-term fix but requires business verification.
- Admin users are plaintext passwords in an env var. Fine for a personal ops tool, but should be hashed if more people get access.

---

## Cursor Prompt for Next Session

> Copy everything between the arrows into a new Cursor window.

> "I'm building LOFO.AI — a lost and found matching app. The project is at `~/Desktop/lofo-ai`. Read `LOFO_AI_Progress.md` first for full context.
>
> **⚠️ IMPORTANT — working style for this session:** Read the progress doc and understand the full state first. Then **describe what you plan to do and ask for approval before making any changes**. Do not make edits proactively.
>
> **Numbering systems — important:**
> - Phases 1–26+ = full project roadmap (backend + web + iOS). Backend/web phases 1–22 done and deployed.
> - iOS Phases A–G = iOS-only build plan. All phases A–G complete. Use A–G labels when working on iOS.
>
> **What's running (Phases 1–22 deployed):** Live API at `https://lofo-ai-production.up.railway.app`, web frontend at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`. Admin at `/admin`, map at `/map`. UptimeRobot keep-alive. Lifecycle cron via GitHub Actions.
>
> **iOS app — ALL phases A–G complete. Build 1.0.0 (6) APPROVED on TestFlight. Public link live: `https://testflight.apple.com/join/PV5qCDKS`. "Friends" external group active (2 testers invited). Next upload = build 7.**
> Native SwiftUI at `~/Desktop/LOFO/LOFO.xcodeproj`. **BUILD SUCCEEDED** — iPhone 17 Pro, iOS 26.3.1, Xcode 26.3. Full finder + loser + match + reunion + tip flows. Push notifications (PushManager + APNs). StripePaymentSheet v25.7.1 SPM added. Supabase `device_tokens` migration done.
>
> **FinderCameraView** is a full native camera viewfinder (AVFoundation): live preview, centered viewfinder bracket overlay, "Point at what you found." center copy, shutter button, library picker, location pill (shows real city/state/zip on device). Falls back to dark gradient on simulator (no real camera).
>
> Full iOS plan: `~/.cursor/plans/swiftui_native_app_transition_e4202362.plan.md`
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector + Supabase Storage, Stripe, Twilio. Railway.
>
> **DB schema:** `items`, `tips`, `reunions`, `device_tokens` (migration done). `used_tokens`, `secret_verifications` (legacy). School tables: `schools` (has `url_token` column), `school_subscriptions`, `school_claims`, `school_lost_pending`, `items.school_id` — all migrations run. `migration_school_mvp.sql` + `migration_school_url_tokens.sql` both complete.
>
> **SMS:** Code-complete, pending Twilio A2P carrier approval (Campaign SID `CM50255157...`, ~2–3 weeks from Mar 12).
>
> **iOS app — 39 Swift files** (added `LocationPickerView.swift` this session):
> - `Theme.swift` — colors, DM Sans + DM Serif Display + DM Serif Display Italic, `LOFOPressStyle`, `lofoCardShadow()`, `serifDisplay()`, `serifDisplayItalic()`, `matchZoomNS` EnvironmentKey (Namespace.ID? optional, iOS 18 zoom transition), **`requiredFieldHighlight(_ triggerCount: Binding<Int>, cornerRadius:)`** — pulsing rust border ViewModifier (3 pulses × 0.65s, settles to 0.55 opacity, Int counter trigger, generation-tracked)
> - `LOFOApp.swift` — `@main`, NavigationStack, `@Namespace matchZoomNS`, AppDelegate adaptor, PushManager, deep link, Stripe key; routes `.loserVerify` → `LoserOTPView`, `.confirmedVerify` → `ConfirmedOTPView`
> - `AppDelegate.swift` — APNs token callbacks → PushManager
> - `Models/Item.swift`, `Models/Match.swift` — all structs are `Sendable`
> - `Services/` — APIClient (uploadSession 90s for photos), LocationManager (CLGeocoder reverse geocoding, startWatching/stopWatching), HapticManager, PushManager, **CameraManager** (AVFoundation, NSObject, not @Observable)
> - `ViewModels/` — AppState (Screen enum includes `.loserVerify`, `.confirmedVerify`; `pop()` + `popToRoot()` helpers), FinderFlowState, LoserFlowState (`matchQueue: [Match]`, `matchedItem: Match?`, `pendingPhone`, `whereDescription`), MenuViewModel
> - `Views/Home/` — HomeView, MenuSheet
> - `Views/Finder/` — FinderCameraView, CameraPreviewView, FinderDoneView, PhoneVerifyView, OTPVerifyView, AllSetView
> - `Views/Loser/` — LostPromptView, WaitingView, LoserOTPView, LoserWaitView, **MatchView** (navy bg, SmileFaceView smile animation, multi-match carousel via `.id(matchIndex)` + `.transition`, `matchIndex` state), OwnershipVerifyView, **ConfirmedView** (centered header, full-width 170pt photo, navy CTA, sends OTP → `.confirmedVerify`), **ConfirmedOTPView** (verifies phone, calls coordinateHandoff, pushes `.tip`)
> - `Views/Shared/` — ItemCardView, TagChipView, LOFOButton, **ReunionView** (rustLight bg, inward-radiating celebration orb with `figure.2.arms.open` icon, two-tone "You're all / set." heading, next-steps list, plain-text "Back To Home" link), **TipView** (centered layout, LOFO navy logo badge, two-tone "Say / Thank You." heading, rust-outline selected amount tiles, custom amount input field, `effectiveCents` logic), PhotoLightboxView, **LocationPickerView** (full-screen map sheet, Uber-style fixed center pin, address chip, dark gradient bottom bar, CLGeocoder reverse geocode on drag stop)
> - `Fonts/` — DMSans-Regular/Medium/Bold.ttf, DMSerifDisplay-Regular.ttf, DMSerifDisplay-Italic.ttf
>
> **Key arch notes:**
> - `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` — all types implicitly @MainActor. Model structs have `Sendable`. APIClient methods do NOT have `nonisolated`. Do NOT change this pattern.
> - `CameraManager` is an exception: `NSObject` (not `@Observable`) with dedicated `DispatchQueue` for AVFoundation. Callbacks dispatch back to main thread.
> - **`parseISO()` in WaitingView + MatchView**: PostgreSQL `::text` timestamps arrive as `2026-03-16 19:58:14.07162+00` (space separator, 5 fractional digits, `+HH` tz). Normalization truncates to 3 fractional digits; `DateFormatter` with `x` pattern handles the rest. Do NOT revert to ISO8601DateFormatter-only.
> - **`Text +` concatenation deprecated in iOS 26**: use `Text("... \(Text(x).modifier())")` string interpolation instead.
> - **`requiredFieldHighlight` API**: trigger is `@Binding<Int>`. `triggerCount += 1` on button tap. Clears on `.onChange(of: fieldValue)` by setting `= 0`.
> - **Italic font**: `DMSerifDisplay-Italic.ttf` internal PostScript name is `DMSerifText-Italic`. Registration uses filename; `serifDisplayItalic()` uses PostScript name. Both must stay in sync.
> - **Multi-match carousel**: `LoserFlowState.matchQueue: [Match]` holds all candidates. `matchedItem: Match?` set only at claim time (used by downstream screens). WaitingView guard: `matchQueue.isEmpty && matchedItem == nil`.
> - **OTP flows**: WaitingView phone → `LoserOTPView` (saves phone to item, shows LoserWaitView). ConfirmedView phone → `ConfirmedOTPView` (calls coordinateHandoff, pushes .tip). Both read from `LoserFlowState.pendingPhone`.
> - **OTP paste/QuickType**: All 3 OTP views (`OTPVerifyView`, `LoserOTPView`, `ConfirmedOTPView`) handle iOS QuickType paste in `handleDigitChange` — detects `numeric.count == 6`, distributes digits across all boxes, returns early. `verify()` guarded with `!isVerifying` to prevent double-call from onChange cascade.
> - **TextEditor backgrounds**: All `TextEditor` instances require `.scrollContentBackground(.hidden)` before `.background(.white)` — otherwise iOS renders its own scroll background on top (appears black). Currently applied in `LostPromptView` and `OwnershipVerifyView`.
> - **TextField foreground colors**: All `TextField` instances must have explicit `.foregroundStyle(LOFOTheme.navy)` — `.primary` defaults can render invisible in sheet presentation contexts. Audit complete as of build 1.0.0 (2).
> - **Location permission**: `NSLocationWhenInUseUsageDescription` key required in `project.pbxproj` for location to work at all. Already added. `LocationManager.startWatching()` reads `manager.authorizationStatus` directly (not cached `authorizationStatus` property) to avoid stale `.notDetermined` on re-open.
>
> **⚠️ Critical — file persistence:** All 37 Swift files in `~/Desktop/LOFO/LOFO/` must exist on disk. If a clean build fails with "Cannot find 'LOFOTheme' in scope" across many files, files have dropped off disk. Use the Cursor Read tool to recover them — Cursor's index retains content even when files drop off disk. (Happened March 17, 2026 — 11 files recovered.)
>
> **TestFlight status (as of March 22, 2026):**
> - **Build 1.0.0 (6) APPROVED** — external review passed. Public link active: `https://testflight.apple.com/join/PV5qCDKS`.
> - "Friends" external group: 2 testers invited (kendaniels@gmail.com, jon.cronin@gmail.com), status "Invited".
> - APNs Key ID + `APNS_TEAM_ID` + `APNS_AUTH_KEY` added to Railway env vars.
> - Merchant ID `merchant.ai.lofo` registered, Apple Pay capability in Xcode.
> - Export compliance set: No encryption beyond iOS standard.
> - **⚠️ Archive signing note:** "Automatically manage signing" fails on Archive when no device UDID registered. Fix: Signing & Capabilities → Release tab → uncheck auto-manage → manually select "LOFO App Store" distribution profile → then Archive.
>
> **New in build 1.0.0 (4) — March 18, 2026 session:**
> - **HomeView redesign**: LOFO wordmark → DM Sans Medium rust 12pt tracking 2.2. Heading → Playfair Display variable font weight 100 (Thin), "Lost something?" upright navy / "Found something?" italic rust, 52pt. Subtitle → "LOST & FOUND. REINVENTED." DM Sans Medium 13pt uppercase tracking 1. Button subtitles updated. `.padding(.top, 32)` between wordmark and heading.
> - **Weekly stat footer**: Rust dot + "X items reunited this week" centered below buttons via overlay. Fetches `GET /stats/public` on appear; hides if 0 or fails.
> - **`lofoBackButton()` ViewModifier** (`Theme.swift`): replaces system back button with 38×38 white circle + chevron matching gear button. Applied to `FinderDoneView`, `PhoneVerifyView`, `OTPVerifyView`, `LostPromptView`, `OwnershipVerifyView`.
> - **`AllSetView` payout mismatch error**: now uses exclamation icon + clearer message. Validates on button tap (standard iOS).
> - **App Version in MenuSheet**: reads `CFBundleShortVersionString (CFBundleVersion)` from bundle — auto-updates, no manual edits needed.
> - **Playfair Display VF fonts** bundled: `PlayfairDisplay-VF.ttf` + `PlayfairDisplay-Italic-VF.ttf`. Helpers: `playfairExtraBold/playfairExtraBoldItalic` use CTFont variable axis API (weight 100). To change weight, update the `900.0` → desired value in `LOFOTheme.playfairVF`.
> - **Backend**: `GET /stats/public` deployed. Fixed RealDictCursor bug (`fetchone()[0]` → `fetchone()['c']`).
> - **`CURRENT_PROJECT_VERSION` = 5. Build 1.0.0 (5) uploaded to TestFlight March 19, 2026 — in external review. Next upload = 6.**
>
> **Admin updates (March 19, 2026):**
> - **Archive button (✕)** on every item row — sets `status = 'archived'`, instantly removes row from table. Record preserved in DB. Recoverable via Supabase SQL (`UPDATE items SET status = 'active' WHERE id = '...'`). `GET /admin/items` excludes archived items. `PATCH /admin/items/{id}/archive` endpoint.
> - **Near-Miss Analyzer** in Debug Matcher tab — paste any item ID (lost or found), see top 10 closest candidates of opposite type ranked by similarity with NO threshold/distance filter. Each candidate shows: score %, colored bar with 78% threshold tick, ✅ WOULD MATCH / ❌ BLOCKED verdict, exact block reasons. Click any candidate → pre-fills pair debugger above and runs it. `POST /admin/debug/near-misses` endpoint.
> - **"🔍 Near-Miss Analyzer →" button** in every expanded row detail panel — one click jumps to Debug tab and runs analysis for that item.
> - **Re-embed All button** in Debug tab — calls `POST /admin/reembed-all`, re-embeds all non-archived items in batches of 50 using current `_build_embedding_text` format. Use after changing embedding format.
> - **`_debug_pair_analysis()` helper** extracted — shared by both the pair debugger and near-miss endpoint. No logic duplication.
>
> **Matching engine redesign (March 19, 2026) — full 5-stage pipeline:**
> - **`_build_embedding_text`**: attribute-only comma-separated format. `"small, blue, white, wool, knit, souvenir text, winter pattern"` — item_type removed entirely from embedding text. Keeps only size, colors, material, features.
> - **`_MATCH_SQL`**: LIMIT 5 → LIMIT 50. Retrieval is now a recall step; precision handled downstream.
> - **Stage A hard filters**: item_type is now a hard categorical gate — `_item_types_compatible()` returns False → candidate excluded entirely (was: raise threshold to 0.88). Color hard gate unchanged. New: sidedness hard gate (`_sides_compatible()`) for gloves/shoes/earbuds/earrings — blocks if both sides explicitly state left vs right.
> - **Stage C Cohere Rerank**: `rerank-english-v3.0` called with structured `"type=X; colors=Y; material=Z; features=A,B"` format. Requires `COHERE_API_KEY` in Railway env vars. Falls back to cosine-only (0.78 threshold) if key absent.
> - **Stage D composite score**: `final_score = (0.55·reranker + 0.20·cosine + 0.15·color_score + 0.10·feature_overlap) × proximity_mult`. `proximity_mult = 1.0 + 0.12 × max(0, 1 − distance_miles/10)` — 1.12× at 0 miles, 1.0× at 10 miles, 1.0× when either item lacks coords. `color_score` is 1.0/0.5/0.0 (match/neutral/incompatible). `feature_overlap` is Jaccard over feature tokens.
> - **Stage E dynamic threshold**: `_query_richness()` classifies loser item as sparse/medium/rich (≤2/3–5/6+ filled fields). Thresholds: 0.30/0.40/0.55 on `final_score`.
> - **`similarity_score` field**: overwritten with `final_score` in response — backward compatible with iOS/web consumers.
> - **New helpers added**: `_sides_compatible`, `_color_score`, `_feature_overlap`, `_query_richness`, `_build_rerank_text`, `_extract_side`.
> - **`cohere`** added to `requirements.txt`.
>
> **⚠️ After deploying — two required steps:**
> 1. Add `COHERE_API_KEY` to Railway environment variables (get key from dashboard.cohere.com).
> 2. Hit "Re-embed All →" in admin Debug tab — regenerates all embeddings with new attribute-only format (old vectors are incompatible).
>
> **On ice (do not implement without discussion):**
> - Tip flow redesign: "tip intent" concept (loser picks amount upfront, charged after reunion confirmed). Post-reunion trigger via SMS relay silence heuristic + time-bomb fallback. Detailed design in Session History Phase 26q.
> - Unit economics: ~$0.25/reunion in Twilio costs, $10 avg tip, net ~$0.87 per loop (2% Stripe on $10, no fixed fee on Apple Pay).
>
> **New this session (March 23, 2026, session 2):**
> - **Subscriber alert throttle**: `school_subscriptions` gets `last_notified_at` column (migration run + confirmed). `_school_notify_subscribers_new_item` now only emails subscribers not notified in last 24h, sends each their own email (privacy fix — was putting all addresses in one To: field), stamps `last_notified_at` after sending.
> - **Subscribe confirmation screen**: replaced `toast + navigate back` (invisible during animation) with inline "You're all set." confirmation state. Re-opening screen resets to blank form.
> - **Thinking screen iOS upgrade**: orb now matches `FinderCameraView.aiOverlay` — outward-expanding stroke rings, center glow, 4 orbiting sparkle dots, rotating ✦ icon. Context-aware copy: admin posting a found item → "Reviewing / *photo…*" + "AI VISION" (static); parent searching → "Searching / *found items…*" + cycling subtitles. `_thinkingMode` variable set before each navigate call.
> - **Admin card "Returned" button**: renamed from "✓ Returned" (looked like a status badge on every card) to "Mark returned" (clearly imperative action). Data was always correct — `status: 'active'` in DB; the misleading copy was the bug.
>
> **New this session (March 23, 2026):**
> - **School app buttons → navy**: removed `rust` modifier from all 8 form CTA buttons in `school.html`. All buttons now match iOS app navy default.
> - **Admin dash stats strip**: new `GET /school/{token}/admin/stats` endpoint (`active_items`, `claims_30d`, `items_returned`). Three-stat row with DM Serif Display numerals rendered above the item grid.
> - **Admin dash heading accent**: `.heading-accent` div under "Posted items". `border-bottom` removed from `.admin-header` and `.browse-header`.
> - **Invalid Date bug fixed**: `fmtDate()` regex normalizes Postgres `+00` timezone offset → `+00:00`. Was failing silently in Safari on all item date displays.
> - **Smart card dates**: `school_admin_items` query now includes `last_claimed_at` (MAX claim date per item). Cards show "Posted Mar 20" + rust "Claimed Mar 22" if claimed.
> - **`lofo-shared.css` — iOS design token alignment**:
>   - Added `--tag-bg: #EAE8F2` (= `LOFOTheme.tagBg` — lavender-tinted chip background)
>   - `.heading-accent` added: 40×1.5px, `rgba(193,122,74,0.35)`, no border-radius — exact iOS `Rectangle().fill(rust.opacity(0.35)).frame(40,1.5)`
>   - `.heading-accent` margins: `margin-top: 16px; margin-bottom: 14px` — mirrors iOS `padding(.top, 16).padding(.bottom, 14)` from `FinderDoneView`
>   - `.page-title`: `margin-bottom: 0` (accent bar now handles spacing)
> - **Tag pills match iOS `TagChipView` exactly**: `--tag-bg` bg, `rgba(26,26,46,0.7)` text, `10px/5px` padding, 12px medium, Capsule, lowercase text. Old: rust-light bg, wrong sizing, capitalized.
> - **Pickup info removed from item detail**: was redundant — already correctly shown on claim-done screen after submit.
> - **`.heading-accent` on all school app headings**: applied to all 9 `.page-title` screens, browse heading (wrapped in column div), and detail title.
> - **`done-title`**: 42px → 38px (matches iOS `serifDisplay(38)` standard).
> - **`done-rule`**: `var(--border)` → `rgba(26,26,46,0.15)`, 40×1.5px — matches iOS `ReunionView` `navy.opacity(0.15)` rule.
>
> **⚠️ iOS app is the design benchmark — not LOFO_MVP.html.** All web design decisions should trace back to the Swift app. `LOFO_MVP.html` is an early prototype; the iOS app is the source of truth.
>
> **New this session (March 22, 2026):**
> - **TestFlight build 1.0.0 (6) approved** — public link live: `https://testflight.apple.com/join/PV5qCDKS`. "Friends" external group, 2 testers invited.
> - **lofoapp.com homepage polished**: Playfair Display weight 900 on `h1`, "Found" capitalized, `&nbsp;` for "by AI" spacing, official App Store badge.
> - **School URL token security**: `url_token` column on `schools` table, all routes use unguessable 18-char hex token. Migration run. SFWS URL: `https://lofoapp.com/school/787c046ec2f5124b79`.
> - **school.html mobile nav redesign**: cream background, house SVG icon, staff login in footer, no backdrop overlay. Desktop sidebar also updated to house icon.
> - **Claim form pre-population**: child/parent/email copied from lost form when entering claim screen.
> - **iOS-style field validation**: `fieldPulse` keyframe (3×0.65s rust border), `markFieldError` + `validateRequired` JS utilities, wired into all 5 form submits.
> - **Photo picker fix**: `display:none` on `input[type="file"]`, `for="admin-file"` on label — eliminates overflow layout bug.
>
> **New this session (March 19–20, 2026):**
> - **Map pin-drop** added to loser flow (`LostPromptView` + new `LocationPickerView`). Uber-style map, address chip, rust pin, "KNOW EXACTLY WHERE?" section label. Pin confirmed → rust checkmark + gray X to clear. GPS still captured as fallback.
> - **Backend pin coords bug fixed** — pin lat/lng no longer overwritten by Nominatim re-geocoding when coords are already provided.
> - **Proximity bonus** added to composite score — `proximity_mult` 1.0–1.12× based on distance. No effect when either item lacks coords.
> - **Twilio A2P resubmitted** — Error 30909 fixed. SMS consent disclosure on all 4 phone screens. New CTA copy + Privacy/Terms URLs filled in. Awaiting TCR review.
> - **Build 6 uploaded to TestFlight** — `CURRENT_PROJECT_VERSION` bumped to 6. Contains: map pin-drop (LocationPickerView + LostPromptView), SMS consent disclosures (PhoneVerifyView + WaitingView). Next upload = build 7.
> - **Build 1.0.0 (6) in external review** — TestFlight "Waiting for Review". Build Metadata confirms: export compliance answered (No), bundle ID ai.lofo.app, symbols included, no blocking flags. Normal Apple queue (1–3 business days).
> - **LOFO for Schools MVP built** — new `school.html` + 10 backend endpoints + DB migration. See full details below.
>
> **LOFO for Schools — what was built (March 20, 2026):**
>
> **Files created:**
> - `school.html` — full single-page app. 11 screens: landing, browse gallery, item detail, claim form, claim done, lost form, thinking (breathing orb), match (navy hero + confidence bar), no-match, no-match done, subscribe, admin login, admin dash, admin post, admin settings. Full LOFO design DNA: navy `#1A1A2E`, cream `#F5F2EC`, rust `#C17A4A`, DM Serif Display headings, DM Sans body. iOS-style push/pop screen transitions (cubic-bezier parallax), stagger entry animations, spring button press, loading states with spinners, emoji item-type placeholders, lightbox, toast.
> - `migration_school_mvp.sql` — creates `schools`, `school_subscriptions`, `school_claims`, `school_lost_pending` tables + `items.school_id` column. **Not yet run in Supabase.**
> - `seed_school_sfws.sql` — inserts SFWS row with slug `sfws`. Default passcode: `sfws-change-me` (Argon2id hash included — rotate immediately after seeding). **Not yet run.**
>
> **Backend changes (`main.py`):**
> - `_INSERT_SQL` updated — now 10 params, added `school_id` (NULL for all existing inserts)
> - `_MATCH_SQL_SCHOOL` — school-scoped pgvector retrieval (both items must share same `school_id`)
> - `_run_match_stages()` — extracted from `match_item`; shared by `/match` and school matching. No logic duplication.
> - `_resend_send_html()` — Resend email helper (requires `RESEND_API_KEY` env var)
> - `_school_after_new_finder_post()` — after admin posts item: emails all subscribers + scans `school_lost_pending` to match-notify waiting parents
> - New Pydantic schemas: `SchoolAdminLoginRequest`, `SchoolSettingsPatch`, `SchoolSubscribeRequest`, `SchoolClaimRequest`, `SchoolLostRequest`
> - New routes: `GET /school/{slug}`, `GET /school/{slug}/data`, `GET /school/{slug}/items`, `POST /school/{slug}/items/from-photo`, `POST /school/{slug}/claim`, `POST /school/{slug}/lost`, `POST /school/{slug}/subscribe`, `POST /school/{slug}/admin/login`, `GET /school/{slug}/admin/items`, `PATCH /school/{slug}/settings`
> - New env vars: `RESEND_API_KEY`, `RESEND_FROM`, `SCHOOL_DEFAULT_NOTIFY_EMAIL`, `LOFO_APP_STORE_URL`
> - `resend` added to `requirements.txt`
>
> **✅ School MVP is LIVE — all 5 go-live steps completed March 20, 2026:**
> 1. ✅ `migration_school_mvp.sql` run in Supabase (fixed ordering bug: ALTER TABLE before CREATE INDEX)
> 2. ✅ `seed_school_sfws.sql` run in Supabase
> 3. ✅ `RESEND_API_KEY` added to Railway env vars
> 4. ✅ Passcode rotated (Argon2id hash updated in DB)
> 5. ✅ Smoke tested — school app loads, staff login works
>
> **Live at:** `https://lofoapp.com/school/787c046ec2f5124b79` (SFWS token — unguessable, do not share publicly)
>
> **School isolation hardened (March 20, 2026):**
> - `_MATCH_SQL` (main app): added `AND f.school_id IS NULL` — consumer losers can never surface school finder items
> - Admin stats: added `AND school_id IS NULL` to active_lost/active_found counts
> - Architecture confirmed multi-school ready: any new school is one `INSERT INTO schools` row + passcode seed, zero code changes
>
> **New this session (March 20, 2026 afternoon):**
> - **school.html UI refined**: sidebar 52→44px, nav icons 20→16px, landing heading 62→48px, emoji icons removed from CTA cards, pickup pill moved below CTAs + restyled to subtle text, app-cta box replaced with plain text line.
> - **Settings email pre-fill bug fixed**: admin email now pre-fills from `schoolData` when opening Settings screen (was always blank).
> - **lofoapp.com live**: static site deployed at `~/Desktop/lofoapp-web` (GitHub: `md-gityup/lofoapp-web`). Homepage + `/privacy` + `/terms` — all on `lofoapp.com`. Deployed via Vercel.
> - **support@lofoapp.com**: ImprovMX forwarding active → marcdaniels@gmail.com. MX + SPF records added in Vercel DNS.
> - **Terms + privacy updated**: SMS consent language matches in-app button text. Support contact → `support@lofoapp.com`. Both Railway and lofoapp.com versions updated.
> - **Twilio A2P resubmitted** (Error 30896): Added 3 opt-in screenshots to repo (`optin-screenshot.png`, `optin-screenshot-finder.png`, `optin-screenshot-terms.png`). Updated opt-in description with screenshot URLs + web verification link. New Privacy/Terms URLs: `lofoapp.com/privacy` + `lofoapp.com/terms`.
> - **iOS MenuSheet**: `support@lofo.ai` → `support@lofoapp.com` (goes into next build).
>
> **lofoapp.com — fully live (March 20, 2026):**
> - Static site: `~/Desktop/lofoapp-web` → GitHub `md-gityup/lofoapp-web` → Vercel → `lofoapp.com`
> - Pages: `/` (homepage), `/privacy`, `/terms`
> - `/school/*` proxies to Railway via `vercel.json` rewrite — so `lofoapp.com/school/{token}` is the clean staff URL
> - `support@lofoapp.com` active via ImprovMX → marcdaniels@gmail.com
>
> **Twilio A2P — 3rd submission (March 20, 2026):**
> - Error 30896 (opt-in verification failure) addressed with: 3 opt-in screenshots in repo, updated opt-in description with screenshot URLs + web verification path, Privacy URL `lofoapp.com/privacy`, Terms URL `lofoapp.com/terms`
> - Awaiting TCR review. No code changes needed when approved.
>
> **New this session (March 20, 2026 evening, session 2):**
>
> **school.html UI polish (8 changes):**
> - **Photo picker fixed** — `overflow:hidden` + SVG upload arrow replaces OS camera emoji. Was visually clipping on desktop.
> - **Sidebar home button** — LOFO asterisk shown at top of sidebar (was `display:none`), now a clickable button that navigates to landing.
> - **Mobile hamburger nav** — hamburger icon on landing top-bar (mobile only). Tapping opens a 280px slide-in drawer from left: Browse / I lost something / Get alerts / Staff login (labeled). Backdrop tap to close.
> - **Removed app-cta promo blocks** from 4 in-flow screens (item detail, claim confirmed, match, no-match-done). Parents no longer see "Download LOFO →" mid-flow.
> - **item-chip** (browse card type badge) — navy fill → rust-light/rust, matching tag pills on detail screen.
> - **Thinking screen** — copy cycles through 3 messages every 1.8s: "Reading your description…" → "Comparing to found items…" → "Checking for a match…". Clears on screen exit.
> - **Admin login button** → rust (was navy, inconsistent with all other form CTAs).
> - **Claim-done checkmark** — SVG circle check (was raw `✓` text character at 56px).
>
> **School email flows — fully working:**
> - Added `_school_page_url(slug)` helper → `https://lofoapp.com/school/{slug}` (was incorrectly linking to consumer LOFO app)
> - Added `_school_email_html()` shared wrapper: navy LOFO header + school name, white card body, footer with school page + lofoapp.com links
> - Added `_email_cta_btn()` for rust/navy CTA buttons in emails
> - **Subscriber new-item email**: photo thumbnail + item type + color, "View found items →" button to school page
> - **Admin claim email**: structured table (child / parent name / email / note), "Open admin dashboard →" navy CTA
> - **Parent possible-match email**: item label + AI confidence % + photo + "Check it out →" CTA
> - **Parent watching-confirmation email**: "Browse found items →" CTA with school URL (was bare text, no link)
>
> **Resend domain — noreply@lofoapp.com live:**
> - `lofoapp.com` verified as sending domain in Resend (DNS records were already in Vercel from ImprovMX setup)
> - `RESEND_FROM = LOFO <noreply@lofoapp.com>` added to Railway env vars
> - All school emails now send from `noreply@lofoapp.com` — looks trustworthy, won't go to spam
>
> **School bugs fixed (March 20, 2026 evening, session 3):**
> 1. ✅ `admin_notify_email` missing from `/school/{slug}/data` response → Settings email always blank on page reload. Fixed: added to public data endpoint.
> 2. ✅ Claim form not cleared between items → stale name/email if parent goes back and claims a different item. Fixed: `onScreenEnter('screen-claim')` now clears all fields.
> 3. ✅ `submitLostRetry` ignored match response → parent never saw a match even if one was found on second submit. Fixed: `res.matches` now checked; routes to `showMatch()` if found.
> 4. ✅ Sidebar Browse icon didn't refresh items → `goNav('screen-browse')` missing `loadItems()`. Fixed.
> 5. ✅ Mobile drawer showed "Staff login" even when logged in → no admin nav on mobile. Fixed: `setAdminSidebarMode` now toggles mobile drawer to show Posted items / Post new item / Settings / Log out when staff is logged in.
>
> **Shared CSS architecture (`lofo-shared.css`) — March 22, 2026:**
> - `lofo-shared.css` created in `~/Desktop/lofo-ai/`. Served by Railway at `GET /lofo-shared.css`. Proxied via Vercel at `lofoapp.com/lofo-shared.css` (added to `vercel.json` rewrites).
> - Contains: CSS tokens, reset, body base, stagger animations, button system, form fields, content wrappers, typography, back-btn, text-link, toast, lightbox, shared mobile overrides.
> - `school.html` links to it via `<link rel="stylesheet" href="/lofo-shared.css">` — dropped ~140 lines of duplicated CSS.
> - **Button upgrades in shared**: spring transition `cubic-bezier(0.34, 1.56, 0.64, 1)`, 12px desktop radius, 15px/500wt base. `.btn-row .btn-primary` rule: iOS-exact spec — `padding: 19px 22px`, `border-radius: 18px`, `font-weight: 400`, full-width. Applies to all form CTAs in school app.
> - `LOFO_MVP.html` still uses its own inline CSS — deliberately deferred (Option B) to avoid breaking the live consumer app. Link it to `lofo-shared.css` in a future pass.
>
> **School admin item actions — March 22, 2026:**
> - `PATCH /school/{token}/items/{item_id}/status` endpoint (admin JWT). Accepts `"inactive"` (returned to owner) or `"archived"` (remove/duplicate).
> - `school_admin_items` excludes `archived` items.
> - Admin card UI: "✓ Returned" (green, immediate) + "Remove" (two-tap confirm: turns rust "Sure?" for 3s). Returned cards grey out + show badge; archived cards fade out + remove from DOM.
>
> **Next priorities:**
> 1. **Staff onboarding at SFWS** — share URL `https://lofoapp.com/school/787c046ec2f5124b79` + passcode `steiner`. Staff → Settings first → set pickup info + admin email. Smoke test: post item → confirm subscriber email arrives from `noreply@lofoapp.com`.
> 2. **iOS build 7** — One code change needed: `support@lofoapp.com` is already confirmed in `MenuSheet.swift`. Cursor change: bump `CURRENT_PROJECT_VERSION` to `7` in `project.pbxproj`. Then archive manually in Xcode: select "Any iOS Device (arm64)" → Product → Archive → Distribute → App Store Connect → Upload.
> 3. **Twilio A2P** — awaiting TCR approval (3rd submission, Error 30896 addressed). No code changes needed when approved. Once approved: test full SMS → resolve page flow end-to-end.
> 4. **App Store screenshots** — 6.7" 1290×2796, 6 screens. Copy drafted in Phase 26 checklist. Needs Xcode simulator + manual capture.
> 5. **Consumer app (LOFO_MVP.html) CSS migration** — link to `lofo-shared.css` and rename `btn-dark` → `btn-primary` etc. Deferred (Option B). Do in a dedicated session with careful testing.
>
> Start by reading `LOFO_AI_Progress.md`, then **describe your plan and wait for approval before making any changes**."

---

## Session History

### School App iOS Design Alignment — March 23, 2026

**What shipped:**

**`lofo-shared.css` — iOS design token alignment:**
- Added `--tag-bg: #EAE8F2` color token (= `LOFOTheme.tagBg` — lavender-tinted chip background used by iOS `TagChipView`)
- Added `.heading-accent` class: 40×1.5px, `rgba(193,122,74,0.35)`, no border-radius — exact match to iOS `Rectangle().fill(LOFOTheme.rust.opacity(0.35)).frame(width:40,height:1.5)` used in `FinderDoneView`, `TipView`, `HomeView`, `OwnershipVerifyView`, etc.
- Updated `.heading-accent` margins: `margin-top: 16px; margin-bottom: 14px` — mirrors iOS `padding(.top, 16).padding(.bottom, 14)`
- Updated `.page-title`: `margin-bottom: 0` (accent bar now owns the spacing)

**school.html — iOS design consistency pass:**
- **All form CTA buttons → navy**: removed `rust` modifier class from all 8 buttons (`btn-primary rust` → `btn-primary`). All CTAs now match iOS app navy default. "Upload & publish" was already navy — the only consistent one.
- **Tag pills match iOS `TagChipView` exactly**: background `var(--tag-bg)` (#EAE8F2), color `rgba(26,26,46,0.7)` (navy 70% opacity), padding `5px 10px`, font-size `12px medium`, border-radius `999px` (Capsule), text `.toLowerCase()`. Previous: rust-light bg, full navy, wrong sizing, capitalized.
- **Pickup info removed from item detail screen**: was redundant — already correctly shown on claim-done screen. Detail screen shows photo + pills + CTA only.
- **`.heading-accent` on all school app headings**: Browse ("Found items", wrapped heading in column div), item detail title, Claim, Lost form, No-match, Subscribe, Staff login, Post a photo, Settings. Plus already-existing one on admin "Posted items".
- **`done-title`**: 42px → 38px to match iOS `serifDisplay(38)` standard. Mobile: 32px → 28px.
- **`done-rule`**: `var(--border)` → `rgba(26,26,46,0.15)`, width 40px — matches iOS `ReunionView` `Rectangle().fill(navy.opacity(0.15)).frame(width:32,height:1.5)`.
- **`border-bottom` removed** from `.browse-header` (same treatment as `.admin-header`).

**Admin dash — stats strip + date fixes (`main.py` + `school.html`):**
- New `GET /school/{token}/admin/stats` endpoint: returns `{active_items, claims_30d, items_returned}`.
- `school_admin_items` query updated: adds `last_claimed_at` (MAX claim date per item).
- Stats strip rendered between admin header and item grid: three DM Serif Display numerals (Active items · Claims 30d · Returned), separated by vertical rules.
- `fmtDate()` bug fixed: Postgres timestamps arrive as `2026-03-20 15:32:44.123456+00`. The `+00` (no colon) is invalid ISO 8601 in Safari → "Invalid Date" on all items. Fixed with regex normalization `([+-])(\d{2})$` → `$1$2:00`.
- Admin cards now show "Posted Mar 20" (always) + rust "Claimed Mar 22" (if `last_claimed_at` exists).

**Design principle established:**
> The iOS Swift app is the design benchmark for all LOFO web surfaces. `LOFO_MVP.html` is an early prototype and not the reference. All design decisions should trace back to `Theme.swift` + the SwiftUI views.

---

### Shared CSS + School Admin Actions + iOS-style Buttons — March 22, 2026

**What shipped:**

**School admin — item actions (`main.py` + `school.html`):**
- New `PATCH /school/{token}/items/{item_id}/status` endpoint (admin JWT required). Accepts `"inactive"` (returned to owner) or `"archived"` (remove/duplicate). Validates item belongs to that school.
- `school_admin_items` now excludes `archived` items (`AND i.status != 'archived'`).
- Admin card UI: each active item card gets two action buttons in a border-top row:
  - **"✓ Returned"** (green) — immediate. Card fades to 50% opacity, buttons swap for green "Returned" badge. Disappears from parent gallery (`/school/{token}/items` only returns `status = 'active'`), stays in admin view.
  - **"Remove"** (muted → rust on confirm) — two-tap: first tap says "Sure?" for 3s, second tap archives. Card fades out and is removed from DOM.
- Returned (`inactive`) items show in admin view with muted opacity + "Returned" badge, no action buttons.
- `SchoolItemStatusPatch` Pydantic model added.

**Shared CSS architecture (`lofo-shared.css`):**
- Created `~/Desktop/lofo-ai/lofo-shared.css` — single source of truth for LOFO design primitives.
- Served by Railway at `GET /lofo-shared.css` (new route in `main.py`).
- Proxied by Vercel: added `{ "source": "/lofo-shared.css", "destination": "https://lofo-ai-production.up.railway.app/lofo-shared.css" }` to `~/Desktop/lofoapp-web/vercel.json`.
- **Contains:** CSS tokens (app-canonical `--bg: #EAE6DE`), reset, body base, stagger animations (`.s-item`, `.s-pop`), button system, loading spinner, form fields + error pulse, `.cx`/`.cx-wide`, `.page-title`/`.page-sub`, `.back-btn`, `.text-link`, toast, lightbox, shared mobile overrides.
- **`school.html`** updated: Google Fonts `<link>` kept, added `<link rel="stylesheet" href="/lofo-shared.css">`, inline `<style>` dropped ~140 lines of duplicated CSS. Only school-specific layout/screen styles remain.
- **`LOFO_MVP.html`** deliberately NOT migrated yet (Option B — deferred to avoid risk to live consumer app).
- **Button upgrades shipped in shared:** spring transition `0.45s cubic-bezier(0.34, 1.56, 0.64, 1)`, 12px desktop radius (was 9px), 15px/500wt base, mobile full-width 52px/18px.

**iOS-style CTA buttons in school app flow screens:**
- Added `.btn-row .btn-primary` rule to `lofo-shared.css`: `padding: 19px 22px`, `border-radius: 18px`, `font-weight: 400`, `width: 100%`, `height: auto` — exact iOS app `.btn-full` spec.
- Applies to all form CTA buttons: Submit claim, Find it, Notify me, Subscribe, Log in, Upload & publish, Save changes.
- Detail screen "This belongs to my child →" button wrapped in `<div class="btn-row">`.
- Match screen `<div class="match-actions">` given additional `btn-row` class.
- Admin header "+ Post found item" button intentionally unaffected (not in `.btn-row` — correct for toolbar context).

---

### School App Security + Polish + TestFlight Approved — March 22, 2026

**What shipped:**

**lofoapp.com homepage (`~/Desktop/lofoapp-web/index.html`):**
- **Playfair Display Black** — `h1` now uses `Playfair Display` variable font weight 900, `letter-spacing: -0.02em`, `word-spacing: -0.02em`. Matches iOS app heading style.
- **"Found" capitalized** — headline reads "Lost & Found," (was "Lost & found,").
- **Word-spacing fix** — `&nbsp;` between "by" and "AI" to prevent line-break and extra visual gap.
- **Official Apple App Store badge** — replaced custom badge `div` with `<img src="https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-us">` linked to `https://testflight.apple.com/join/PV5qCDKS`.

**TestFlight:**
- Build 1.0.0 (6) approved. Public TestFlight link live: `https://testflight.apple.com/join/PV5qCDKS`.
- "Friends" external group created with 2 invited testers (kendaniels@gmail.com, jon.cronin@gmail.com).

**School URL token security (`migration_school_url_tokens.sql` + `main.py`):**
- New `url_token VARCHAR(24) UNIQUE NOT NULL` column on `schools` table. Populated with `encode(gen_random_bytes(9), 'hex')` — 18-char unguessable hex token.
- `migration_school_url_tokens.sql` run in Supabase.
- `main.py`: all `/school/{slug}/*` routes renamed to `/school/{token}/*`. Lookup now uses `WHERE url_token = %s`. Validation regex `_SCHOOL_TOKEN_RE = re.compile(r"^[a-f0-9]{12,24}$")`. Admin JWT compare uses token-fetched school ID. Email helpers use `url_token` for all URLs.
- Public `/school/{token}/data` response no longer exposes `slug`.
- SFWS live URL: `https://lofoapp.com/school/787c046ec2f5124b79`.

**school.html — mobile nav redesign:**
- Drawer background changed to `var(--cream)` (matching main screen). Width `min(300px, 88vw)`.
- Backdrop/overlay disabled (`display: none`).
- Drawer header replaced: house SVG icon (rust, 28px) + school name subtitle below it (set dynamically from `loadSchoolData`).
- "Staff login" button moved from top-right of landing to a `mobile-drawer-footer` div in the drawer.
- "Staff login" button removed from landing top-bar.
- Close button styled to match cream background (`rgba(26,26,46,0.08)` tint, navy icon).

**school.html — desktop sidebar logo:**
- Sidebar home button SVG replaced: asterisk/plus → simple rust house icon (24×24, stroke-width 1.7, matching mobile drawer).

**school.html — claim form pre-population:**
- `onScreenEnter('screen-claim')` now copies `child`, `parent`, `email` values from the lost form into claim form fields. `claim-note` cleared to empty.

**school.html — iOS-style required field validation:**
- CSS: `@keyframes fieldPulse` — 3 pulses × 0.65s, alternates rust border + box-shadow on/off. `.field-error` class applies animation, settles to `border-color: rgba(193,122,74,0.55)`.
- JS: `markFieldError(el)` — adds `.field-error` class, removes on `animationend`. `validateRequired(ids)` — marks all empty fields, returns false if any invalid.
- Wired into: `submitClaim`, `submitLostRetry`, `doSubscribe`, `adminLogin`. `submitLost` description length check uses `markFieldError`.

**school.html — photo picker alignment fix:**
- `input[type="file"]` inside `.photo-picker` changed from `position: absolute; inset: 0; opacity: 0` to `display: none` — removes intrinsic width from layout entirely.
- `<label class="photo-picker">` given `for="admin-file"` attribute to maintain click-to-pick behavior.

---

### School App Navigation Fixes + Admin Orgs Tab — March 21, 2026

**What shipped:**

**Admin dashboard — Organizations tab:**
- New "Organizations" tab in `admin.html` (UI-only rename: "school" → "organization"; DB schema unchanged).
- Three new backend endpoints in `main.py`: `GET /admin/orgs` (per-org summary stats), `GET /admin/org-items` (all org finder items, filterable by org), `GET /admin/org-claims` (all school_claims with org context, filterable).
- Per-org summary cards show: active items, total items, total claims, pending claims, subscriber count, org link.
- Items sub-tab and Claims sub-tab with org filter dropdown. All rendered as sortable tables with org badge.

**Admin + map on lofoapp.com:**
- `vercel.json` in `lofoapp-web` updated with rewrites: `/admin` → Railway `/admin`, `/map` → Railway `/map`.
- Admin dashboard now accessible at `lofoapp.com/admin`.

**Email browse deep-link:**
- Added `_school_browse_url(slug)` helper in `main.py` → `https://lofoapp.com/school/{slug}?browse=1`.
- Three email CTAs updated to use deep-link: subscriber new-item notification ("View found items →"), possible match email ("Check it out →"), watching/no-match email ("Browse found items →").
- `school.html` `DOMContentLoaded`: checks `?browse=1` param → calls `loadItems()` + navigates directly to `screen-browse`.

**Python version pin:**
- Created `.python-version` file with `3.12.9` to prevent Railway's `mise` from attempting to install a non-existent Python version (was crashing deploys).

**school.html navigate() — post-item screen layout fix:**
- Removed `position:absolute; left:0; right:0; top:0; zIndex:10` from the navigate function entirely. These were set on the incoming screen during transitions, but since the outgoing screen hides immediately, there's never two screens visible simultaneously — no layering needed.
- Root cause of bug: if `animationend` didn't fire (e.g. animation cancelled or rapid navigation), the screen stayed stuck with `position:absolute`, causing the photo-picker to render full-width from the page edge, behind/over the sidebar.
- Added `e.target !== next` guard on the `animationend` listener to ignore bubbled events from child elements.
- Added 500ms `setTimeout` fallback that finalizes screen state even if the animation event never fires.

**school.html navigate() — back-home flash fix:**
- `staggerScreen()` was removing `.s-ready` from ALL `.s-item`/`.s-pop` elements on every screen visit, then re-adding it — causing a full visible flash as items vanished and re-animated on the landing screen.
- Fix: `staggerScreen` now skips items that already have `.s-ready` class. Items that haven't been shown yet still animate in normally; revisiting a screen keeps existing items visible.
- Also reordered navigation: animation class is now added before `display: flex`, ensuring `animation-fill-mode: both`'s initial `opacity:0` state is applied on the very first paint frame.

---

### School Flow Bug Fixes — March 20, 2026 (evening, session 3)

**5 bugs found via code audit and fixed:**

1. **`admin_notify_email` not in `/school/{slug}/data` response** (`main.py`) — The public `/data` endpoint returned `slug, name, pickup_info, app_store_url` but NOT `admin_notify_email`. `schoolData.admin_notify_email` was always `undefined`, so the admin email field in Settings was always blank on every page load. Fix: added `admin_notify_email` field to the response.

2. **Claim form not cleared between items** (`school.html`) — If a parent submitted a claim on item A, went back, opened item B, the claim form still had item A's child name, parent name, and email. Fix: added `screen-claim` entry handler in `onScreenEnter` that clears all four fields.

3. **`submitLostRetry` ignored match response** (`school.html`) — When a parent entered email on the no-match screen and resubmitted, the API response was `await`-ed but not captured (`const res` was missing). Always navigated to `screen-no-match-done` even if matches were found. Fix: capture `res`, check `res.matches.length`, route to `showMatch()` if found.

4. **Sidebar Browse icon didn't refresh gallery** (`school.html`) — `goNav('screen-browse')` only called `navigate()`, not `loadItems()`. Items were pre-loaded at boot but stale after staff posts a new item in a different session. Fix: added `if (screenId === 'screen-browse') { loadItems(); }` to `goNav`.

5. **Mobile drawer showed "Staff login" while logged in** (`school.html`) — The mobile nav drawer always showed the public nav. Staff logging in on mobile had no admin navigation in the drawer. Fix: added admin drawer items (`#mobile-drawer-admin-nav`: Posted items / Post new item / Settings / Log out) hidden by default. `setAdminSidebarMode` now also toggles `#mobile-drawer-staff-login` and `#mobile-drawer-admin-nav`.

---

### School UI Polish + Email Flows + Resend Domain — March 20, 2026 (evening, session 2)

**What shipped:**

**school.html — 8 cosmetic/UX fixes:**
- Photo picker (`screen-admin-post`): was visually clipped on desktop — fixed with `overflow:hidden`. Replaced OS camera emoji with rust SVG upload arrow; JS reset uses `innerHTML` to restore SVG after upload.
- Sidebar home button: `.sidebar-logo` was `display:none` — changed to visible flex button, navigates to landing on click.
- Mobile hamburger nav: hamburger added to landing `top-bar` (mobile only). Opens a 280px left drawer with labeled nav items (Browse, I lost something, Get alerts, Staff login). Backdrop click closes. `openMobileNav()` / `closeMobileNav()` in JS.
- Removed `.app-cta` promo blocks from: `screen-detail`, `screen-claim-done`, `screen-match`, `screen-no-match-done`. Landing page app-cta kept.
- `item-chip`: `background: var(--navy); color: #fff` → `background: var(--rust-light); color: var(--rust)`.
- Thinking screen: `startThinkingCycle()` JS timer cycles 3 messages every 1.8s. Started in `onScreenEnter`, cleared on exit.
- Admin login button: added `rust` class.
- Claim-done icon: `✓` text → `<svg>` circle + path checkmark.

**main.py — school email overhaul:**
- `_school_page_url(slug)` → `https://lofoapp.com/school/{slug}`
- `_school_email_html(school_name, body_html, slug)` → full HTML wrapper with navy LOFO header, white card, footer
- `_email_cta_btn(label, url, color)` → inline-style anchor button
- `_school_notify_subscribers_new_item()` rewritten: photo thumbnail, item type + colors, "View found items →" CTA to school page
- `_school_notify_claim_admin()` rewritten: HTML table with child/parent/email/note rows, clickable mailto, "Open admin dashboard →" navy CTA
- `_school_notify_parent_possible_match()` rewritten: item label + confidence % + photo + "Check it out →" CTA
- Inline "watching" email in `school_lost_match()` rewritten: "Browse found items →" CTA with school URL

**Resend domain verification:**
- `lofoapp.com` added and verified in Resend (DNS records for DKIM/SPF/MX/DMARC were already in Vercel from ImprovMX setup — no new records needed)
- `RESEND_FROM = LOFO <noreply@lofoapp.com>` added to Railway Variables
- All school emails now send from `noreply@lofoapp.com`

---

### lofoapp.com School Proxy + Twilio Wrap-Up — March 20, 2026 (evening, cont.)

**What shipped:**

**lofoapp.com/school/* proxy:**
- Added `vercel.json` to `lofoapp-web` with rewrite: `/school/:path*` → `https://lofo-ai-production.up.railway.app/school/:path*`
- Staff URL is now `https://lofoapp.com/school/sfws` (clean, trustworthy domain)
- All relative API calls in school.html proxy correctly through Vercel

**TestFlight review notes updated:**
- What to Test, Beta App Description, Review Notes filled in
- Added note about Twilio A2P pending — sets reviewer expectations for SMS
- Feedback email → `support@lofoapp.com`
- Privacy Policy URL → `https://lofoapp.com/privacy`

**Twilio A2P — 3rd submission:**
- Privacy URL → `lofoapp.com/privacy`, Terms URL → `lofoapp.com/terms`
- Opt-in description updated with 3 screenshot URLs + web verification path
- Awaiting TCR review

---

### Staff Onboarding Prep + Twilio A2P + lofoapp.com — March 20, 2026 (evening)

**What shipped:**

**school.html UI refinements:**
- Sidebar narrowed: `--sidebar-w` 52→44px, nav items 38→32px, SVG icons 20→16px
- Landing heading 62→48px, eyebrow 15→13px, body sub 16→14.5px, container padding reduced
- Emoji icons (🔍📝) removed from CTA cards; border 1.5→1px, padding reduced, title 22→18px
- Pickup info pill moved below CTA grid + links; restyled from heavy navy block to subtle muted text line
- App CTA rust-light box replaced with plain 12px text line

**Settings email pre-fill bug fixed (`school.html`):**
- `goNav` and `onScreenEnter` for `screen-admin-settings` now pre-fill admin email from `schoolData.admin_notify_email`
- Was always clearing to `''`, causing staff to not see their saved email

**lofoapp.com static site:**
- New repo `~/Desktop/lofoapp-web` (GitHub: `md-gityup/lofoapp-web`)
- `index.html` — clean homepage: LOFO wordmark, headline, "iOS app coming soon" badge, footer with Privacy/Terms/email links
- `privacy/index.html` — full privacy policy at `lofoapp.com/privacy`
- `terms/index.html` — full terms of service at `lofoapp.com/terms`
- Deployed via Vercel; `lofoapp.com` domain connected

**support@lofoapp.com:**
- ImprovMX account created; `lofoapp.com` added with catch-all `*@lofoapp.com → marcdaniels@gmail.com`
- MX records (`mx1/mx2.improvmx.com`) + SPF TXT record added in Vercel DNS
- Forwarding confirmed active

**Terms + privacy updated:**
- `terms.html` SMS section: consent language updated to match in-app button text; "Reply HELP for help" → "Reply HELP for support"; contact → `support@lofoapp.com`
- `privacy-policy.html` "Your rights": "contacting us" → `support@lofoapp.com`
- Same changes mirrored in `lofoapp-web/terms/index.html` and `lofoapp-web/privacy/index.html`

**Twilio A2P resubmission (Error 30896 — Opt-in Error):**
- Root cause: TCR reviewer couldn't verify opt-in without navigating full app flow
- Fix: 3 opt-in screenshots committed to `lofo-ai` repo:
  - `optin-screenshot.png` — loser flow (WaitingView phone screen)
  - `optin-screenshot-finder.png` — finder flow (PhoneVerifyView)
  - `optin-screenshot-terms.png` — terms SMS section with STOP/HELP
- New opt-in description written with screenshot URLs + web verification path
- Privacy URL → `lofoapp.com/privacy`, Terms URL → `lofoapp.com/terms`

**iOS:**
- `MenuSheet.swift`: `support@lofo.ai` → `support@lofoapp.com` (goes into build 7)

---

### School Go-Live + UI Redesign — March 20, 2026 (afternoon)

**What shipped:**

**School MVP go-live — 5 ops steps completed:**
1. Fixed `migration_school_mvp.sql` ordering bug (CREATE INDEX on `school_id` ran before `ALTER TABLE items ADD COLUMN school_id` — reordered).
2. Ran migration in Supabase SQL editor.
3. Ran `seed_school_sfws.sql` in Supabase.
4. Added `RESEND_API_KEY` to Railway env vars (from resend.com). Default `RESEND_FROM` = `onboarding@resend.dev` (Resend test domain — fine for MVP).
5. Rotated passcode from `sfws-change-me` to `steiner` (Argon2id hash generated locally, UPDATE run in Supabase).
6. Pushed all uncommitted school code to GitHub (school.html, main.py changes, requirements.txt, migration + seed SQL files were untracked — Railway was running old code without school routes).

**School app now live at:** `https://lofo-ai-production.up.railway.app/school/sfws`

**Desktop UI redesign of `school.html`:**
- Full desktop-first layout: 52px icon sidebar + main content area (no more 480px mobile shell on desktop).
- Sidebar: cream background, thin right border — matches Claude.ai aesthetic. Removed orange asterisk. Icon-only nav with SVG line icons (stroke-width 1.5, round caps) in rust/muted/navy palette. CSS tooltips on hover. Active state: rust icon + soft rust tint.
- Landing screen: LOFO wordmark + italic DM Serif Display school name + large "What did your child *lose?*" heading.
- Browse: auto-fill grid (minmax 200px), sticky header with search.
- Detail: 2-col layout (sticky photo left, info + claim right).
- Forms: centered max-width 540px.
- Admin dash: card grid with photo thumbnails.
- Mobile fully preserved: sidebar hidden, push/pop transitions, top-bars.
- Transitions: simple fade on desktop (no push/pop), push/pop restored at <768px.

**School isolation audit + hardening (`main.py`):**
- `_MATCH_SQL`: added `AND f.school_id IS NULL` — prevents consumer app loser from surfacing school finder items.
- Admin stats (`GET /admin/stats`): added `AND school_id IS NULL` to active_lost/active_found counts — school items no longer inflate consumer app metrics.
- Architecture confirmed: `_MATCH_SQL_SCHOOL` already correctly scopes both loser and finder to same `school_id`. Browse/admin listings already scoped. Multi-school support is zero-code — new school = new row in `schools` table.

---

### LOFO for Schools MVP — March 20, 2026

**What shipped:**

**school.html — new browser-based web app for elementary schools:**
- 11 screens covering the full school-specific flow: landing, browse gallery (stagger grid), item detail + claim form, claim confirmed (with App Store CTA), lost form, thinking/loading (breathing orb), match result (navy hero + confidence bar), no-match, subscribe to notifications, admin login, admin dashboard, admin post item (styled photo picker + vision analysis), admin settings.
- Full LOFO design system: `--navy: #1A1A2E`, `--cream: #F5F2EC`, `--rust: #C17A4A`. DM Serif Display headings, DM Sans body/UI text. Identical visual DNA to `LOFO_MVP.html`.
- iOS-style push/pop screen transitions with `cubic-bezier(0.32,0.72,0,1)` timing — exactly matching the native app's spring physics.
- Stagger entry animations (`s-item`, `s-pop`) for grid items and modal content. Spring button press via `transform: scale(0.94)`.
- `btnLoading()` / `btnReset()` — async button loading states with inline spinner.
- Emoji item-type placeholders (🎒📱🧤👟🕶️…) when no `photo_url` present. Graceful `onerror` fallback on `<img>` tags.
- Confidence bar on match screen animates after screen enters (delayed via `setTimeout`).
- Custom-styled photo picker for admin uploads replaces raw `<input type=file>`.
- Input `:focus` states with rust border, navy shadow.
- Scrollable screen containers — content doesn't clip.
- App Store download CTA on match + claim confirmed screens.

**main.py — backend additions (no changes to existing routes):**
- `_INSERT_SQL` updated for optional `school_id` (10th param). All existing callers pass `None`.
- `_MATCH_SQL_SCHOOL` — school-scoped pgvector recall (both items share `school_id`).
- `_run_match_stages()` — reranker + composite score logic extracted and shared by both `/match` and school matching. Zero duplication.
- `_resend_send_html()` — single Resend API caller. All school emails go through here.
- `_school_after_new_finder_post()` — triggers: (1) subscriber new-item digest email, (2) scan `school_lost_pending` + email waiting parents if match found.
- 10 new `/school/{slug}/*` routes: `GET /school/{slug}` (serve HTML), `GET /school/{slug}/data`, `GET /school/{slug}/items`, `POST /school/{slug}/items/from-photo`, `POST /school/{slug}/claim`, `POST /school/{slug}/lost`, `POST /school/{slug}/subscribe`, `POST /school/{slug}/admin/login`, `GET /school/{slug}/admin/items`, `PATCH /school/{slug}/settings`.
- Admin JWT auth on protected routes (`_require_school_admin()`).
- Orphan cleanup: `school_lost_pending` rows deleted immediately if no match found and no email provided.
- New Pydantic schemas: `SchoolAdminLoginRequest`, `SchoolSettingsPatch`, `SchoolSubscribeRequest`, `SchoolClaimRequest`, `SchoolLostRequest`.
- New env vars: `RESEND_API_KEY`, `RESEND_FROM`, `SCHOOL_DEFAULT_NOTIFY_EMAIL`, `LOFO_APP_STORE_URL`.
- `resend` added to `requirements.txt`.

**migration_school_mvp.sql** — new tables: `schools` (slug, name, pickup_info, admin_passcode_hash, admin_notify_email), `school_subscriptions` (email, school_id), `school_claims` (item_id, school_id, parent_email, parent_name, created_at), `school_lost_pending` (school_id, description, email, embedding). Plus `ALTER TABLE items ADD COLUMN school_id`. **⚠️ NOT YET RUN in Supabase.**

**seed_school_sfws.sql** — inserts SFWS row (`slug=sfws`). Default passcode: `sfws-change-me`. **⚠️ NOT YET RUN. Rotate passcode before sharing with anyone.**

**What's pending before school MVP is live:**
1. Run `migration_school_mvp.sql` in Supabase SQL editor
2. Run `seed_school_sfws.sql` in Supabase SQL editor
3. Add to Railway: `RESEND_API_KEY` (required), `RESEND_FROM` (default: `LOFO <noreply@lofo.ai>`), `SCHOOL_DEFAULT_NOTIFY_EMAIL`, `LOFO_APP_STORE_URL`
4. Change default passcode: generate Argon2id hash of real passcode, UPDATE schools SET admin_passcode_hash
5. Visit `/school/sfws` → staff login → post a test item → browse as parent → verify emails send

---

### Map Pin-Drop + Matching Improvements — March 19, 2026

**What shipped:**

**iOS — Map pin-drop location in loser flow:**
- New `LocationPickerView.swift` (`Views/Shared/`) — full-screen map sheet, Uber-style fixed center pin, address chip floats above pin (reverse geocoded on drag stop), pin lifts/drops animation, dark gradient bottom bar, "Confirm Location" button, X to dismiss.
- `LostPromptView.swift` — `whereField` text input replaced with tappable location pill. Default state shows GPS name as fallback. After pin confirmed: rust-accented "Location pinned" + address + checkmark + gray X to clear. All-caps "KNOW EXACTLY WHERE?" section label with rust location arrow. Placeholder updated to include vague location hint. `pinCoordinate`/`pinLabel` state added. Submit uses pin coords if confirmed, GPS fallback otherwise.
- Both files import MapKit + CoreLocation. CLGeocoder deprecation warnings are pre-existing (same as LocationManager) — non-blocking.

**Backend — pin coords bug fix:**
- `from-text` endpoint: when `where_description` AND `latitude`/`longitude` are both provided (map pin-drop case), pin coords are used directly. Previously, Nominatim geocoded the pin label and overwrote the precise map coordinates with a less accurate result.

**Backend — distance proximity bonus in composite score:**
- Composite formula now includes a proximity multiplier: `final_score = (0.55·reranker + 0.20·cosine + 0.15·color + 0.10·features) × proximity_mult`
- `proximity_mult = 1.0 + 0.12 × max(0, 1 - distance_miles/10)` — 1.12× at 0 miles, 1.0× at 10 miles.
- When either item has no coordinates: `proximity_mult = 1.0` (no change to existing behavior).
- Pin-drop gives precise loser coordinates, making this bonus meaningful for the first time.

**Twilio A2P campaign resubmission:**
- Error 30909 (CTA verification failure) root cause: consent description claimed a checkbox existed; no checkbox present. Description missing STOP/HELP/msg-rates disclosures.
- Fix: SMS consent disclosure added to all 4 phone entry screens (web finder, web loser, iOS `PhoneVerifyView`, iOS `WaitingView`). `terms.html` STOP/HELP bolded, support contact added. Web pushed to GitHub Pages.
- Resubmitted with rewritten CTA copy (see progress doc Notes section). Privacy Policy URL + Terms URL filled in.
- Awaiting TCR review (typically a few days to a week).

---

### Twilio A2P Campaign Fix — March 19, 2026

**What happened:** A2P 10DLC campaign rejected with Error 30909 — CTA verification failed. Rejection reason: consent description claimed a checkbox existed in the app; no checkbox was present. Required disclosures (STOP, HELP, msg & data rates) missing from phone entry screens.

**What shipped:**

**Web (`LOFO_MVP.html`):**
- Finder phone screen (`screen-phone`): Replaced privacy note with full SMS consent disclosure below the Send Code button: *"By tapping 'Send code' you agree to receive SMS notifications from LOFO. Msg & data rates may apply. Reply STOP to opt out. Privacy policy."*
- Loser waiting screen (notify section): Added consent disclosure below the Notify Me button.
- Pushed to GitHub — GitHub Pages updated within ~2 min. TCR reviewers can verify live at `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html`.

**Terms (`terms.html`):** STOP and HELP bolded in SMS section. Message frequency clarified. Support contact line added. Meets Twilio A2P Terms URL requirements.

**iOS:**
- `PhoneVerifyView.swift`: Privacy note replaced with full SMS consent disclosure (same copy as web).
- `WaitingView.swift` (loser phoneSection): Consent disclosure added below Confirm Phone Number button.
- iOS changes go into **build 6** — bump `CURRENT_PROJECT_VERSION` to 6 before archiving.

**Twilio — resubmit using this CTA copy:**
> Users enter their phone number in the LOFO app and tap a button to send a verification code. Directly below the phone input field, the following disclosure is displayed before the user taps: "By tapping Send Code, you agree to receive SMS notifications from LOFO. Msg & data rates may apply. Reply STOP to opt out." Tapping the button constitutes consent. Consent is not required to use the app.
>
> The opt-in flow can be verified live at: https://md-gityup.github.io/lofo-ai/LOFO_MVP.html — select "I found something" or "I lost something", then proceed to the phone number screen.
>
> LOFO sends two types of messages: (1) one-time verification codes when users verify their phone number, and (2) alert notifications when a lost/found item match is detected. Message frequency varies based on user activity, typically 1–3 messages per event. Users may reply STOP at any time to opt out, or HELP for support.
>
> Terms: https://lofo-ai-production.up.railway.app/terms
> Privacy Policy: https://lofo-ai-production.up.railway.app/privacy

**Twilio form fields:**
- Privacy Policy URL: `https://lofo-ai-production.up.railway.app/privacy`
- Terms and Conditions URL: `https://lofo-ai-production.up.railway.app/terms`

---

### Matching Engine Live + Build 1.0.0 (5) — March 19, 2026

**What shipped:**

**Matching engine fully operational with Cohere reranker:**
- Full pipeline tested end-to-end: loser "glove, blue" → 3 finder gloves returned, scores 0.823 / 0.817 / 0.803. No backpacks, beanies, AirPods, or landscape photos.
- Root cause of earlier test failures: stale embeddings (loser item created before Re-embed All was run) caused format mismatch. Resolved by submitting a fresh loser item.
- Cohere client bug fixed: `cohere.ClientV2` doesn't support `.rerank()` → changed to `cohere.Client`. Pushed as hotfix.
- Fallback logic fixed: Cohere error previously zeroed reranker scores and continued with composite formula, producing scores below sparse threshold (0.274 < 0.30) → fixed to branch to cosine-only fallback with richness-adjusted thresholds (0.58/0.62/0.68). Added `[LOFO rerank] OK/error` logging.
- Embedding format settled: `"glove, small, blue, white, wool, knit, souvenir text"` — item_type as first token (once, not repeated). Removes sentence-structure color bias while preserving type recall.

**Build 1.0.0 (5) uploaded to TestFlight:**
- `CURRENT_PROJECT_VERSION` bumped from 4 → 5 in `project.pbxproj` (both Debug + Release).
- Uploaded to App Store Connect, added to external "testers" group.
- Test Information filled in (Beta App Description, What to Test, Feedback Email, Privacy Policy URL, Marketing URL, Review Notes). This unblocks external review — previous build 1.0.0 (4) was stuck "Waiting for Review" for 24h because Test Information was empty.
- Build 1.0.0 (5) currently "Waiting for Review." Once approved, enable public link in Settings tab of "testers" group.

### Matching Engine Redesign — March 19, 2026

**What shipped:**

**Full 5-stage matching pipeline** — replaces cosine-only matching with a reranker-backed composite pipeline.

**Stage A — Hard filters (Python, pre-scoring):**
- item_type: `_item_types_compatible()` now a hard categorical gate — incompatible types excluded entirely before any scoring. Previously raised threshold to 0.88, which failed when wrong-type items already scored 69%.
- Color: existing `_colors_compatible()` hard gate unchanged.
- Sidedness: new `_sides_compatible()` — if both loser and finder feature lists explicitly state conflicting sides (left vs right), hard block. Silent = pass. Applies to gloves, shoes, earbuds, earrings.

**Stage B — pgvector retrieval:**
- `LIMIT 5` → `LIMIT 50`. Retrieval is now a recall step; precision delegated to Stage C/D/E.
- No cosine threshold in SQL (was already absent — just ORDER BY distance + LIMIT).

**Stage C — Cohere Rerank:**
- Model: `rerank-english-v3.0`.
- Query and document format: `"type=glove; colors=blue,white; material=wool; size=small; features=souvenir text,winter pattern"` — structured attribute format, not free text. Gives reranker the clearest signal without description-length noise.
- Requires `COHERE_API_KEY` env var. Graceful fallback to cosine-only (0.78 threshold) if key absent.

**Stage D — Composite score:**
```
final_score = 0.55 * reranker_score
            + 0.20 * cosine_score
            + 0.15 * color_score
            + 0.10 * feature_overlap_score
```
- `color_score`: 1.0 (shared color group) / 0.5 (one or both sides neutral/absent) / 0.0 (confirmed incompatible).
- `feature_overlap_score`: Jaccard over lowercased feature tokens.
- `similarity_score` response field overwritten with `final_score` — backward compatible with all clients.

**Stage E — Dynamic threshold:**
- `_query_richness()`: sparse (≤2 filled fields), medium (3–5), rich (6+).
- Thresholds on `final_score`: 0.30 / 0.40 / 0.55. Sparse queries get more lenient threshold since the reranker has less to work with; the asymmetry is by design.

**`_build_embedding_text()` rewritten:**
- Old: natural language sentence with item_type as subject + repeated. `"A small blue wool glove with winter design. glove."`
- New: comma-separated attribute values only, no item_type. `"small, blue, white, wool, knit, souvenir text, winter pattern"`
- Rationale: item_type is now a categorical gate, not an embedding signal. Embedding only encodes physical attributes that vary within a type. Eliminates cross-type color collisions.

**New helpers added:** `_extract_side`, `_sides_compatible`, `_color_score`, `_feature_overlap`, `_query_richness`, `_build_rerank_text`, `_RERANK_THRESHOLDS`.

**`cohere`** added to `requirements.txt`.

**`_debug_pair_analysis()`**: threshold reference updated from 0.78 → 0.40 (cosine retrieval floor). `would_pass_threshold` → `would_pass_cosine_floor`. Note added that live match uses composite `final_score`, not raw cosine.

**⚠️ Required post-deploy steps:**
1. Add `COHERE_API_KEY` to Railway environment variables (get from dashboard.cohere.com).
2. Hit "Re-embed All →" in admin Debug tab — all existing embeddings are stale with the new attribute-only format.

---

### Admin Tooling + Matching Engine Investigation — March 19, 2026

**What shipped:**

**Build 1.0.0 (4) uploaded to TestFlight** — build from previous session, uploaded this session.

**Admin: Archive button**
- ✕ button added to every item row in Lost/Found tabs. Sets `status = 'archived'`, removes row from table instantly. Record preserved in DB. `GET /admin/items` now excludes `status = 'archived'`. `PATCH /admin/items/{id}/archive` endpoint added.

**Admin: Near-Miss Analyzer**
- New panel in Debug Matcher tab. Input: one item ID. Output: top 10 closest candidates of opposite type, ranked by cosine similarity, no threshold/distance filter applied. Each card shows: score %, colored progress bar with 78% threshold tick line, ✅ WOULD MATCH or ❌ BLOCKED verdict, exact block reason text.
- Clicking a candidate card pre-fills the pair debugger above and runs it — "drill down" from list to full pair analysis in one click.
- "🔍 Near-Miss Analyzer →" button added to expanded row detail panel in Lost/Found tables — jumps to Debug tab and runs analysis for that item automatically.
- `POST /admin/debug/near-misses` endpoint. `_debug_pair_analysis()` helper extracted and shared between this endpoint and the existing pair debugger — no logic duplication.

**Admin: Re-embed All**
- "Re-embed All →" button in Debug tab. Calls `POST /admin/reembed-all` — fetches all non-archived items, re-embeds in batches of 50 via Voyage API, updates `embedding` column. Use after changing `_build_embedding_text` format.

**Matching engine: partial fix**
- `_build_embedding_text` rewritten from key-value (`item_type: glove color: blue...`) to natural language sentence (`"A small blue wool glove with winter design. glove."`). Item_type is sentence subject + repeated at end to anchor the embedding.
- `_item_types_compatible(type_a, type_b)` function added. Checks: exact match, containment ("glove" in "winter glove"), or shared synonym group from `_ITEM_TYPE_SYNONYMS` (20 groups). Wired into match endpoint: incompatible types raise threshold 0.78 → 0.88.

**Matching engine: fundamental problem identified**
Near-Miss Analyzer testing revealed that Voyage-3 general embeddings don't cleanly separate item types. Running "blue glove" loser against all finder items: backpack scored 69%, bracelet 68%, wallet 68%, actual gloves 62–68%. Everything lands in a 7-point band. Color dominates over item type. Natural language format helped but didn't solve score compression. Detailed technical brief prepared (see below) for next agent session.

**Technical brief for matching engine redesign:**

*Architecture:* Each item profile (item_type, color, material, size, features) → `_build_embedding_text()` → Voyage-3 1024-dim vector → stored in pgvector. Match: cosine similarity (`1 - embedding <=> embedding`) → top 5 by score → Python filters: similarity ≥ 0.78, color compatibility, item_type compatibility (raised threshold).

*Problem:* Voyage-3 is a general semantic similarity model, not an object identity classifier. In its embedding space, short physical object descriptions cluster tightly (60–70% similarity). Color is a dominant signal — "blue glove" and "navy blue backpack" score 69%. Score distribution is too compressed to use a threshold alone for type discrimination. Description asymmetry compounds this: finders over-describe (AI extracts 50 words), losers under-describe (8 words), producing a sparse loser vector equidistant from everything.

*What was tried:* Key-value format (equal field weights) → natural language with item_type as subject + repeated (partial improvement) → item_type raised threshold to 0.88 (doesn't help when backpack already scores 69%).

*Open questions for new architecture:*
1. Should item_type be a mandatory hard gate (SQL filter) rather than a scoring component at all?
2. Is cosine similarity the right tool, or would a cross-encoder reranker ("same object: yes/no?") give better precision?
3. Should the embedding only cover color/material/size/features (not item_type), with item_type handled categorically?
4. What threshold strategy works when description lengths are asymmetric by design?
5. Would a two-tower model trained on lost/found pairs outperform a general embedding model?

---

### Build 1.0.0 (3) — HomeView Redesign + Polish — March 18, 2026

**What's in this build:**

**HomeView redesign:**
- LOFO wordmark: changed from DM Serif Display navy to DM Sans Medium rust, 12pt, tracking 2.2 (matches web prototype)
- More space between wordmark and heading: `.padding(.top, 32)` (was 8)
- Heading font: swapped DM Serif Display → Playfair Display variable font at weight 100 (Thin). "Lost something?" upright navy, "Found something?" italic rust. Both 52pt, tracking -1, -11pt gap between groups
- Subtitle: "Lost & Found. Reinvented." in DM Sans Medium 13pt uppercase tracking 1 (matches SUPPORT/INFORMATION header style in menu)
- Button subtitles: "Snap a photo. We'll take it from there." / "Tell us what and where. We're on it."
- Weekly stat footer: rust dot + "X items reunited this week" centered below buttons via overlay (layout-neutral). Fetches from `GET /stats/public` on appear; hides if 0 or fetch fails

**Back button consistency:**
- New `lofoBackButton()` ViewModifier in `Theme.swift` — hides system back button, replaces with 38×38 white circle + 15pt chevron + shadow + LOFOPressStyle. Matches gear button exactly.
- Applied to: `FinderDoneView`, `PhoneVerifyView`, `OTPVerifyView`, `LostPromptView`, `OwnershipVerifyView`

**Payout validation (`AllSetView`):**
- Mismatch error now shows exclamation icon + "Handles don't match — make sure both fields are identical" (was plain text). Validates on Save button tap (standard iOS pattern).

**Settings menu:**
- App Version row now reads from bundle dynamically: `CFBundleShortVersionString (CFBundleVersion)` — shows e.g. "1.0.0 (3)". No manual updates needed.

**Fonts:**
- Playfair Display variable fonts bundled: `PlayfairDisplay-VF.ttf` + `PlayfairDisplay-Italic-VF.ttf`
- Registered in `LOFOTheme.registerFonts()`. Helpers: `playfairExtraBold(_ size)` + `playfairExtraBoldItalic(_ size)` using CTFont variable axis API (weight 100 currently)

**Backend (deployed):**
- `GET /stats/public` — returns `{"reunions_this_week": N}`, no auth. Fixed RealDictCursor key bug (`[0]` → `['c']`).
- 13 seed reunion records inserted via Supabase SQL for testing

**Build number:** `CURRENT_PROJECT_VERSION` bumped to 4 (skipped 3 — two uploads went as build 1 due to missing version bump, then build 2 was the real bug-fix build, so next is 4).

---

### Build 1.0.0 (2) — Real-Device Bug Fixes — March 17, 2026

**What shipped:** TestFlight build 1.0.0 (2) — 10 bug fixes + 1 enhancement from first real-device TestFlight testing session.

**Bug fixes:**
1. **`AllSetView`** — `.red` → `LOFOTheme.rust` on mismatch error (handle fields + error text).
2. **`project.pbxproj`** — Added `NSLocationWhenInUseUsageDescription` key (both Debug + Release). Location was completely non-functional without it — iOS silently ignores permission requests when key is missing.
3. **`LocationManager.startWatching()`** — Reads `manager.authorizationStatus` directly instead of cached `authorizationStatus` property (which starts as `.notDetermined`). Prevents failing to start updates when already authorized.
4. **`FinderCameraView`** — Subtitle copy: "AI will read it automatically" → "Our AI vision will get to work". Bottom shadow gradient between camera frame and shutter bar removed.
5. **`OTPVerifyView` / `LoserOTPView` / `ConfirmedOTPView`** — iOS QuickType/paste now works: `handleDigitChange` detects 6-digit paste, distributes across all boxes. `verify()` guarded with `!isVerifying` to prevent double-call. Applies to all 3 OTP screens.
6. **`HomeView`** — Added `.toolbar(.hidden, for: .navigationBar)` + `.ignoresSafeArea(.keyboard)`. Fixes large gap at top when returning from loser flow (keyboard inset persisted on pop; nav bar geometry shifted layout).
7. **`LostPromptView` / `OwnershipVerifyView`** — Added `.scrollContentBackground(.hidden)` to both `TextEditor` instances. Without it, iOS renders a black background over the white `.background()` modifier.
8. **`WaitingView` `WaitingAttrEditSheet`** — "What did you lose?" field and "Add a detail" field were invisible on tap (missing `.foregroundStyle(LOFOTheme.navy)`). Fixed in both `styledField` helper and inline TextField.
9. **Full app TextField audit** — `LostPromptView` (whereDescription), `AllSetView` (handle + confirmHandle), `FinderDoneView` (secretDetail, newDetail, styledField helper) — all missing `.foregroundStyle(LOFOTheme.navy)`. Fixed across 5 fields in 3 files.
10. **`FinderDoneView`** — Tag chip area capped at 4 rows (`142pt → 112pt`) instead of 5; bottom row was clipping.

**Enhancement:**
- **`FinderCameraView` AI overlay** — Sparkle animation redesigned: main `sparkles` icon rotates 360° continuously (9s linear) + scale/opacity breathe (1.8s easeInOut); 4 orbiting `sparkle` points at diagonal positions (27pt radius) with staggered twinkle in/out (0.28s delay each); center glow pulses with icon.

**Archive checklist (do every time):**
1. Increment `CURRENT_PROJECT_VERSION` in `project.pbxproj` (both Debug + Release targets) — current value is `4`, next upload = `5`, etc. App Store Connect rejects duplicate build numbers.
2. Signing & Capabilities → Release tab → uncheck "Automatically manage signing" → select "LOFO App Store" profile → Archive.
3. The "App Version" row in the Settings menu sheet reads directly from the bundle (`CFBundleShortVersionString` + `CFBundleVersion`) — no code changes needed, it auto-updates.

---

### Phase G — TestFlight Live — March 17, 2026

**What shipped:** Build 1.0.0 (1) successfully archived and uploaded to App Store Connect via Xcode Organizer. Internal TestFlight group created. App now installable on real devices.

**Setup completed (manual steps, user-driven):**
- **Apple Developer Portal:** App ID `ai.lofo.app` with Push Notifications + Apple Pay capabilities. APNs Auth Key (.p8) created and downloaded. Merchant ID `merchant.ai.lofo` registered.
- **Railway env vars added:** `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_AUTH_KEY`, `APNS_BUNDLE_ID=ai.lofo.app`, `APNS_ENVIRONMENT=production`.
- **Xcode:** Signing team switched from "Personal Team" to paid org (`marc daniels — Admin`). Apple Pay capability added with `merchant.ai.lofo`. `LaunchScreen.storyboard` created (plain cream background, no logo). Marketing version `1.0.0`, build `1`.
- **Provisioning:** "LOFO App Store" distribution profile manually created on developer.apple.com (both Apple Distribution certs included), downloaded, and installed. Resolved "No profiles found" error.
- **Archive + Upload:** Product → Archive → Distribute App → App Store Connect → Upload. No issues.
- **Export compliance:** "No, this app does not use encryption beyond what iOS provides" → "None of the algorithms mentioned above".
- **App Store Connect:** Internal group created, build 1.0.0 (1) added after compliance cleared.

---

### Phase 26r — TipView Redesign (UI Polish Pass 8) — March 17, 2026

**What changed:** Full visual redesign of `TipView.swift` to match the app's centered, typographic style.

**Changes:**
- **Layout:** Everything centered (`VStack(alignment: .center)`). Logo badge at top, two-tone heading, body copy, amount grid, custom amount field, CTA button, skip link — all centered.
- **Logo badge:** Navy circle (80pt) with cream "LOFO" text in DM Serif Display — appears with fade + scale animation.
- **Heading:** Two-tone "Say" (navy serif) / "Thank You." (rust italic serif) at 38pt.
- **Body copy:** "LOFO is an entirely free service, but a cash reward is a nice way to say thanks. The recipient won't know about it until 24 hours after your [item] has been returned."
- **Amount tiles:** Selected state changed from navy fill to **rust outline** (2px `LOFOTheme.rust` stroke + rust shadow) — matches OTP verification input active state.
- **Custom amount field:** New text field below grid. Dollar prefix. Clears preset selection when typed into. `effectiveCents` computed property: preset takes priority, falls back to custom input.
- **CTA title:** Dynamic — "Send $X" when amount selected, "Continue without a tip" when nothing selected.
- **Skip link:** Plain underlined text "Skip — no tip this time" centered below CTA button.
- **`startPayment()`:** Now reads `effectiveCents` — works for both preset and custom amounts.

---

### Phase 26q — ReunionView Redesign (UI Polish Pass 7) — March 17, 2026

**What changed:** Full visual redesign of `ReunionView.swift` to match LoserWaitView's centered, screen-filling style.

**Changes:**
- **Background:** `LOFOTheme.rustLight` (warm off-white/peach) replacing plain cream — signals warmth and celebration.
- **Graphic:** New "celebration orb" replaces generic icon — concentric ring animation with `LOFOTheme.rust` strokes **radiating inward** (scaleEffect: `pulse ? 0.28 : 1.90`), larger circumference (130pt) matching WaitingView radar. Core glow circle + `figure.2.arms.open` SF Symbol (navy, 26pt).
- **Heading:** Two-tone "You're all" (navy) / "set." (rust italic) at 40pt. Body: "Both you and the finder have been notified. Reply to our text to message each other."
- **Padding:** `.padding(.horizontal, 10)` on heading, `.padding(.horizontal, 20)` on next-steps list — consistent with other screens.
- **Next steps list:** Three rows with SF Symbol icons — "Watch for a text from us" / "Reply to coordinate pickup" / "Keep an eye on your messages". Each row: icon + text, consistent padding with body copy above.
- **CTA:** Plain text link "Back To Home" (navy @ 40% opacity) instead of filled LOFOButton — matches LoserWaitView pattern.
- **Animations:** Staggered opacity/offset entrance (graphic → heading → list → button, 0.3s intervals).

---

### Phase 26p — ConfirmedView OTP Gate — March 17, 2026

**Problem:** ConfirmedView called `coordinateHandoff()` directly on button tap — no phone verification. Inconsistent with the WaitingView loser flow (Phase 26i), which requires OTP before saving the phone.

**Solution:** Inserted an OTP step between ConfirmedView and the TipView. Phone is now verified before any handoff fires.

**New flow:** ConfirmedView (enter phone + tap "Verify & Connect") → `sendOTP()` → **ConfirmedOTPView** (6-digit verify) → `coordinateHandoff()` → push `.tip`

**Files changed:**
- **`AppState.swift`** — added `.confirmedVerify` case to `Screen` enum.
- **`ConfirmedView.swift`** — replaced `coordinate()` + `isCoordinating` with `sendCode()` + `isSendingCode`. Button relabeled "Verify & Connect". On valid phone: sends OTP, stores E.164 phone in `LoserFlowState.shared.pendingPhone`, pushes `.confirmedVerify`. `coordinateHandoff` logic moved entirely to `ConfirmedOTPView`.
- **New `ConfirmedOTPView.swift`** (`Views/Loser/`) — mirrors `LoserOTPView` exactly. On OTP success: calls `coordinateHandoff(req)` with `finderItem`/`loserItem` from `LoserFlowState`, saves `loserPhone`, registers push token, pushes `.tip`. Error messages use `LOFOTheme.rust` + exclamation icon (consistent with app style).
- **`LOFOApp.swift`** — wired `.confirmedVerify` → `ConfirmedOTPView()`.

---

### Phase 26o — ConfirmedView Polish — March 17, 2026

**`ConfirmedView.swift`:**
- **Header centered**: `VStack(alignment: .leading)` → `alignment: .center` + `.frame(maxWidth: .infinity)`. Scale anchor changed from `.leading` to `.center`. Subtitle gets `.multilineTextAlignment(.center)`.
- **Photo card full-width**: `frame(width: 88, height: 88)` → `frame(maxWidth: .infinity, height: 170)` with `radiusL` corners (matches MatchView photo card exactly). Border stroke removed (not used in MatchView).
- **CTA button navy**: "Connect Us Both" button changed from `.background(.white)` / navy text to `.background(LOFOTheme.navy)` / white text + `.white.opacity(0.6)` subtitle + `.white.opacity(0.45)` arrow. Matches `LOFOButton` style app-wide. Spinner tint changed from navy to white.

---

### Phase 26n — Multi-Match Carousel — March 17, 2026

**Problem:** When multiple finder items matched a loser's description, only the highest-scoring one was shown. Rejecting it sent the user back to the waiting screen, where the next match might never surface.

**Solution:** Full silent carousel — all candidates above threshold are queued up and presented one after another without the user knowing how many there are. Key security consideration: showing "1 of 3" would tell a bad actor to keep trying until they find something easy to claim. No progress indicators anywhere.

**Files changed:**

**`AppState.swift`:**
- Added `pop()` helper (`guard !path.isEmpty else { return }; path.removeLast()`) — used by MatchView to pop back to WaitingView when queue is exhausted.

**`LoserFlowState.swift`:**
- Added `matchQueue: [Match] = []` — stores all candidates from the latest poll.
- Kept `matchedItem: Match?` — still used by OwnershipVerifyView, ConfirmedView, TipView, ReunionView (set at the moment of claim, not at poll time).
- `reset()` clears both.

**`WaitingView.swift` (`startPolling()` + `poll()`):**
- Guards updated: `matchQueue.isEmpty && matchedItem == nil` — prevents re-polling when carousel is active or a match has been claimed.
- `poll()`: `LoserFlowState.shared.matchQueue = matches` (stores entire candidate list, not just `matches.first`). Pushes `.match` on `!matches.isEmpty`.

**`MatchView.swift`:**
- `@State private var matchIndex: Int = 0` — current position in the queue.
- `match` computed property reads `matchQueue[matchIndex]` (not `matchedItem`).
- ScrollView gets `.id(matchIndex).transition(.asymmetric(insertion: .move(edge: .trailing), removal: .move(edge: .leading)))` — SwiftUI applies a horizontal slide transition whenever `matchIndex` changes. Old card exits left, new card enters from right.
- `claimMatch()`: sets `LoserFlowState.shared.matchedItem = match` before navigating (pins the claimed match for all downstream views).
- `rejectMatch()`: appends `match.id` to `rejectedMatchIds`; if next index is in-bounds, calls `withAnimation(.easeInOut(duration: 0.32)) { matchIndex = nextIndex }` + `HapticManager.light()`; if queue exhausted, clears `matchQueue` and calls `appState.pop()`.

**Backend:** No changes — `POST /match` already returns up to 5 candidates (`LIMIT 5` in `_MATCH_SQL`); iOS `findMatches()` already returns `[Match]`. The iOS side was just discarding all but the first result.

---

### Phase 26m — MatchView Polish + WaitingView Bug Fix + ConfirmedView Redesign — March 17, 2026

**MatchView (`Views/Loser/MatchView.swift`) — multiple polish passes:**

- **Smile face flipped happy**: Arc angles changed from `210°→330°` (frown/∩) to `30°→150°` (smile/U). Arc center shifted from `rect.midY + 10` to `rect.midY - 10` so smile sits in lower portion. Eyes shifted from `y: -22` to `y: -28` to stay clearly above smile. Graphic frame reduced 10%: `110×90` → `99×81`.
- **Smile animation rebuilt** — exact WaitingView radar pattern: `ForEach(0..<3)` with `scaleEffect(pulse ? 2.1 : 0.4, anchor: UnitPoint(x:0.5, y:0.376))` + `opacity(pulse ? 0 : 0.45)`, `.easeOut(duration: 2.6).repeatForever(autoreverses: false).delay(Double(i) * 0.87)`, single `@State var pulse = false` toggled on appear. Anchor `y: 0.376` = `30.5/81` — matches arc geometric center in frame. One permanent base arc at r=20 as resting shape. Previous `phase1/phase2/glow` multi-state approach removed.
- **Header compression**: outer `VStack(spacing: 18→10)`, top spacer `28→16`, bottom spacer `8→4`. Heading line pull `-10→-14` to match visual tightness of left-aligned headers elsewhere. Removed "GOOD NEWS" eyebrow label. Item label `.lineLimit(1)` + `.truncationMode(.tail)` — long names never wrap to 3 lines.
- **Match Probability**: label renamed from "MATCH CONFIDENCE". Font `serifDisplay(60→42)` (30% reduction). `VStack(spacing: 5→2)`. `.padding(.top, 4)` removed.
- **Photo card**: height `210→170`.
- **Content top padding**: `28→12`.
- **Attributes pill**: size attribute removed from summary (color + material only). "Details →" → "View Details →". Details sheet title → "Item Details".
- **Details list**: time + distance combined on one line: "Found 2h ago · 0.3 mi away" (clock icon). Saves one row.
- **buildReasons**: now also checks `match.features` for description matches. Removed "X% AI similarity score" fallback entirely — empty array if no attribute match (cleaner than redundant info). Feature match shows as "Feature: gold clasp".

**WaitingView bug fix (`Views/Loser/WaitingView.swift`):**
- **Root cause**: SwiftUI NavigationStack can spuriously re-fire `.onAppear` on WaitingView when navigating deeper (MatchView → ConfirmedView). This restarted polling. After 5s, poll fired again, found same match, pushed `.match` again — putting a second MatchView on top of ConfirmedView. User perceived this as being "taken back."
- **Fix**: `guard LoserFlowState.shared.matchedItem == nil else { return }` added at the top of both `startPolling()` and `poll()`. If a match is already found, any new poll cycle immediately returns without touching navigation.

**ConfirmedView redesign (`Views/Loser/ConfirmedView.swift`):**
- **Removed `ItemCardView`** — full attribute card with pill replaced by a compact 88×88pt `photoThumbnail` (rounded corners, border, `lofoCardShadow()`). Only renders if `match.photoUrl` exists.
- **Single CTA — "Connect Us Both"**: white card button, navy text, subtitle "LOFO texts you both — your numbers stay private", arrow right, `LOFOPressStyle`. Loading state shows spinner. The second button ("I'll Reach Out — Just Notify the Finder") removed entirely — loser has no way to contact finder directly (LOFO never shares contact info), making it a confusing dead end.
- **`coordinate(selfOutreach:)` default**: parameter kept with `= false` default so backend call is unchanged, but no callers pass `true` anymore.

---

### Phase 26l — MatchView Full Redesign (UI Polish Pass 7) + Critical File Recovery — March 17, 2026

**MatchView complete redesign (`Views/Loser/MatchView.swift`):**
- Full `LOFOTheme.navy` background matching LoserWaitView — the screen is a "special moment" visually distinct from all cream flow screens.
- **`SmileFaceView`** (nested private struct): two white filled `Circle`s (7pt, opacity 0.65, offset ±15 / -22) as eyes + three nested `SmileArc` shapes (radii 48/34/20pt; white opacities 0.12/0.28/0.62; `StrokeStyle(lineWidth:, lineCap: .round)`; arc from 210°→330°). `SmileArc: Shape` also a private nested type.
- **"GOOD NEWS"** eyebrow: `sans(11, weight: .medium)`, white 0.45, tracking 2.5.
- **Two-tone heading**: "Is this your" white `serifDisplay(38)` + "wallet?" rust `serifDisplayItalic(38)`, tight `-10pt` bottom padding for close stacking, centered. Plural-aware list: keys/sunglasses/earrings/headphones/gloves/glasses/scissors/airpods/shoes/socks → "Are these your X?".
- **Match Confidence**: `"\(Int(score * 100))%"` white `serifDisplay(60)` + `"MATCH CONFIDENCE"` `sans(10)` white 0.4 tracking 2. No bar — editorial number is the statement.
- **Photo card**: full-width, 210pt height, `radiusL` clip, tappable → `PhotoLightboxView` as `fullScreenCover`.
- **Attributes row**: condensed `"white · leather · small  Details →"` pill (`background(.white.opacity(0.07))`, `radiusM`) — tap → `.sheet` with `LazyVGrid` of `TagChipView` chips + item type heading + rust rule. `presentationDetents([.medium])`, `presentationDragIndicator(.visible)`.
- **Details list**: `clock` icon + `timeAgo()` string, `location.fill` + distance string, rust `checkmark.circle.fill` + match reasons (`buildReasons` matches color/material in loser description, falls back to "XX% AI similarity score").
- **CTAs**: "That's Mine" cream-bg/navy-text button + right arrow (inverted — cream on navy). "Not My Item" white 0.4 underline text. Both `LOFOPressStyle`. `LOFOButton` not used here (inverted color scheme).
- **`parseISO()` + `timeAgo()`** helpers inlined (same PostgreSQL timestamp parsing pattern as WaitingView — handles space separator, 5-digit fractional seconds, `±HH` timezone).
- **Entrance**: `HapticManager.matchConfirm()` on appear. Header `easeOut(0.45s)`, content `spring(response:0.5, dampingFraction:0.82)` with 0.3s delay.

**Critical file recovery (root cause: stale DerivedData cache masking missing files):**
- 11 Swift files had gone missing from `~/Desktop/LOFO/LOFO/` at some prior point. Project continued building because Xcode's DerivedData cached old compiled objects. Modifying `MatchView.swift` (or a clean build) invalidated the cache, triggering a fresh compile and exposing all missing files → 86 "Cannot find 'LOFOTheme' in scope" errors.
- All 11 files restored to disk from Cursor's index (which retained content from prior `Read` calls): `Theme.swift`, `LOFOApp.swift`, `AppDelegate.swift`, `Views/Home/HomeView.swift`, `Views/Finder/CameraPreviewView.swift`, `Views/Finder/FinderCameraView.swift`, `Views/Finder/FinderDoneView.swift`, `Views/Finder/PhoneVerifyView.swift`, `Views/Finder/OTPVerifyView.swift`, `Views/Finder/AllSetView.swift`.
- Build confirmed clean after restoration. No functionality lost.
- **⚠️ Warning for future sessions**: If a clean build fails with "Cannot find 'LOFOTheme' in scope" across many files simultaneously, it means files have gone missing from disk again. Use the Cursor `Read` tool — its index persists file content even when files drop off disk.

---

### Phase 26k — UI Polish Pass 6: Full App Consistency + Stats Bug Fix — March 16, 2026

**MenuSheet rebuild:**
- Removed `NavigationStack` + `.navigationTitle("LOFO")` + `.navigationBarTitleDisplayMode(.inline)` system chrome.
- Custom X dismiss button: `Image(systemName: "xmark")`, `font(.system(size: 13, weight: .medium))`, `LOFOTheme.muted` foreground, `38×38` frame, `.background(.white)`, `.clipShape(Circle())`, `.lofoCardShadow()`. Matches gear button on HomeView exactly.
- Staggered fade+lift entrance: header (0ms), My Usage (100ms), Support (200ms), Information (300ms). Each lifts 14pt over 350ms easeOut.
- `LOFOPressStyle` added to FAQ rows, Contact Us, About LOFO, Terms of Service, Privacy Policy, Done button.
- Stats row: `HStack(alignment: .firstTextBaseline)` — aligns number baselines so "32", "33", "1" all sit on the same line regardless of 1-line vs 2-line labels below.
- `ScrollView(.vertical, showsIndicators: false)` throughout.

**WaitingView consistency + animation rebuild:**
- Rust rule was the only rule in the app using solid `fill(LOFOTheme.rust)` (full opacity) at `32×2pt`. Fixed to standard `rust.opacity(0.35)` at `40×1.5pt`.
- Heading `VStack(spacing: 2)` → `VStack(spacing: 0)` + `.padding(.bottom, -10)` on "Looking for" line. Matches tight stacking on every other two-line heading in the app.
- "Nothing nearby yet…" copy: `sansCaption() muted` → `sans(14) navy.opacity(0.7)` — more prominent, reads like a prompt.
- Button relabeled "Confirm Phone Number".
- Radar animation fully rebuilt to match HTML prototype: 3 stroke rings all 130px, `scale(0.4) opacity(0.14)` → `scale(2.1) opacity(0)`, 2.6s easeOut, delays 0/0.87/1.73s (was 72–148px rings at 1.25× scale, much weaker). Added center glow pulse (navy circle expands 68→92px and fades, matching CSS `box-shadow` pulse from prototype). Frame height 130px.

**Flow screen consistency pass:**
- **MatchView**: `ScrollView(.vertical, showsIndicators: false)` iOS 26 fix. "That's Mine" title case.
- **OwnershipVerifyView**: Error messages → `HStack { Image("exclamationmark.circle") + Text }` in `LOFOTheme.rust`. No more raw `.red`.
- **ConfirmedView**: Heading rebuilt from centered single-color to left-aligned two-tone: badge above, "It's yours." navy + "Confirmed." rust italic, rust rule, muted subtitle. Outer VStack `alignment: .leading`. "Connect Us Both". Same styled error message.
- **TipView**: Styled error message. "Select An Amount", "Skip — No Tip This Time" title-cased.
- **ReunionView full layout pass**: `ScrollView` top-anchored left-aligned (retired double-`Spacer` centering). Connection graphic (pulsing concentric rust circles + link icon) spring-animates first. "You're all" navy `serifDisplay(38)` + "set." rust `serifDisplayItalic(38)`, rust rule, two muted subtitle lines. Done button fades last. `.navigationBarBackButtonHidden(true)`.

**Title case applied to all CTA buttons across 10 files:**
"That's Mine" (×2), "Not My Item", "Verify Ownership", "Connect Us Both", "I'll Reach Out — Just Notify the Finder", "Confirm Phone Number", "Send Code", "Update Description" (×2), "Save Payout Info", "Select An Amount", "Skip — No Tip This Time", "Resend Code" (×2), "Back To Home".

**Backend: `GET /stats/by-items` UUID case bug fixed (`main.py`):**
- Root cause: Swift `UUID.uuidString` produces uppercase UUIDs (`"A7F3B2C4-..."`). PostgreSQL `uuid::text` produces lowercase (`"a7f3b2c4-..."`). Query used `id::text IN (placeholders)` — string comparison always failed, `COUNT(*)` returned 0.
- Fix: `[x.strip().lower() for x in ids.split(",") ...]` — one character change.
- Deployed to Railway, commit `854ff40`.

---

### Phase 26j — Required Field Highlight System + LostPromptView Location UX — March 16, 2026

**Problem:** Tapping action buttons on screens with empty/incomplete required fields gave zero feedback — buttons with `.disabled()` were literally unresponsive, and phone fields silently returned without any indication.

**Solution: `LOFORequiredFieldHighlight` ViewModifier (`Theme.swift`)**
- New private `LOFORequiredFieldHighlight: ViewModifier` + `View.requiredFieldHighlight(_ triggerCount: Binding<Int>, cornerRadius:)` convenience extension.
- Trigger is `@Binding<Int>` — every `+= 1` is always a new value so `onChange` fires unconditionally on every button tap (Bool approach failed because SwiftUI batched `false→true` in the same update cycle).
- On each trigger: `withAnimation(nil) { pulseOpacity = 0 }` snaps border off instantly, then `DispatchQueue.main.async` starts the repeating animation on the next run loop. This ensures every replay runs the full `0 → 1.0` range — without the reset, a re-trigger from the `0.55` resting state only oscillated `0.55 ↔ 1.0`, looking weak.
- Pulse: 5 half-cycles × 0.65s easeInOut = ~3.25s, then settles to steady `0.55` opacity rust border.
- **Generation counter** (`@State private var generation: Int`): incremented on each trigger; the settle `DispatchQueue` callback checks its captured generation — cancels stale callbacks when re-triggered mid-animation.
- When `triggerCount = 0`: border fades out over `0.3s` easeOut (set by caller's `.onChange(of: fieldValue)`).

**LostPromptView (`Views/Loser/`):**
- `.disabled()` removed from "Start Looking" button — button is always tappable.
- `submit()`: empty guard fires `highlightDescription += 1` + `HapticManager.error()`.
- `.requiredFieldHighlight($highlightDescription)` + `.onChange(of: description) { highlightDescription = 0 }`.
- `whereField`: Added `location.fill` rust icon (12pt, 0.75 opacity) before "Where did you lose it?" label. Added "This is optional — you can simply describe where you lost it in the field above and we'll take care of the rest." muted caption below label.

**OwnershipVerifyView (`Views/Loser/`):**
- Same pattern. `.disabled()` removed. `verify()` fires `highlightClaim += 1`. `.onChange(of: claim)` clears.

**PhoneVerifyView (`Views/Finder/`):**
- `sendCode()` fires `highlightPhone += 1` + haptic alongside existing error text. `.onChange(of: phoneNumber)` clears.

**ConfirmedView (`Views/Loser/`):**
- `coordinate()` fires `highlightPhone += 1` + haptic. `.onChange(of: phone)` clears.

**WaitingView (`Views/Loser/`):**
- `sendCode()` was a completely silent `guard...else { return }` — now fires `highlightLoserPhone += 1` + `HapticManager.error()`. `.onChange(of: loserPhone)` clears.

---

### Phase 26i — iOS UI Polish Pass 5 + Loser OTP Flow + LoserWaitView Cleanup — March 16, 2026

**Bug fixes:**
- **WaitingView "Submitted at" blank** — PostgreSQL `::text` timestamps arrive as `2026-03-16 19:58:14.07162+00` (space separator, 5 fractional digits, `+HH` timezone without minutes). `parseISO()` updated with PostgreSQL-style `DateFormatter` formats using `x` ICU pattern (accepts `±HH`). Debug print added to confirm format, then removed.
- **iOS 26 `Text +` deprecation** (6 warnings in WaitingView, OTPVerifyView, PhoneVerifyView) — all converted to `Text("... \(Text(x).modifier())")` string interpolation pattern.

**UI Polish Pass 5 — screens polished:**

**LostPromptView.swift:**
- Two-tone heading: "What did" navy `serifDisplay(38)` + "you lose?" rust `serifDisplayItalic(38)`, `-10pt` stacking
- Rust rule (40×1.5pt, opacity 0.35) + subtitle below
- `ScrollView { }` → `ScrollView(.vertical, showsIndicators: false)` (SwiftUI 6 disambiguation)

**AllSetView.swift:**
- Rust rule added below "All set." heading
- `ScrollView` fix

**TipView.swift (full rewrite):**
- Left-aligned top-anchored layout replacing centered double-Spacer
- 3-stage entrance animation (heading 0ms, amounts 130ms, buttons 260ms)
- Rust rule below heading
- `LOFOPressStyle` on amount buttons, selection shadow

**OwnershipVerifyView.swift (full rewrite):**
- Removed double-`Spacer` centering → top-anchored `ScrollView(.vertical, showsIndicators: false)`
- Two-tone heading "Verify it's" navy `serifDisplay(34)` + "yours." rust `serifDisplayItalic(34)`, `-8pt` stacking
- Rust rule + subtitle
- `lofoCardShadow()` on `TextEditor`
- 3-stage entrance animation

**ConfirmedView.swift:**
- Added country code `Menu` + ISO badge + `(XXX) XXX-XXXX` auto-formatter to phone field (identical to PhoneVerifyView / WaitingView pattern)
- Pre-populates from `LoserFlowState.shared.loserPhone` if user already gave phone on WaitingView
- `coordinate()` updated to prepend country code digits before sending
- `ScrollView` fix

**PhotoLightboxView.swift:**
- Entrance fade (`opacity 0→1`) + scale (`0.96→1`) spring animation on appear

**LoserWaitView.swift (major cleanup):**
- Orb shrunk 30%: outer 220→154, middle 155→109, inner 100→70, core 64→45, dot 8→6; `endRadius` 32→22
- Ring breathe timing: large stagger (0/1.1/2.2s) → tight stagger (0/0.18/0.35s) — all rings breathe together
- Core `RadialGradient`: `white.opacity(0.22)` → `white.opacity(0.07)` (invisible glow, not a solid blob)
- Layout: equal `Spacer()` pair → capped top `Spacer(maxHeight: 72)` + free bottom `Spacer()` (orb in upper third)
- Gap between orb and text: 44pt → 30pt
- "Think positive." → `serifDisplayItalic(40)` `.white.opacity(0.65)` (two-tone heading)
- Added `white.opacity(0.18)` 32×1.5pt rule separator
- "Got it" white pill button → `"Back to home"` plain text link (`white.opacity(0.4)`) calling `isPresented = false` + `appState.popToRoot()`
- Text entrance: `easeOut` → `spring(response: 0.55, dampingFraction: 0.82)`
- Added `@Environment(AppState.self)` for `popToRoot()`

**Loser OTP Flow:**

**AppState.swift:**
- Added `.loserVerify` case to `Screen` enum (between `.waiting` and `.match`)

**LoserFlowState.swift:**
- Added `pendingPhone: String?` field + cleared in `reset()`

**WaitingView.swift:**
- `isSavingPhone` → `isSendingCode: Bool` + `sendCodeError: String?`
- Removed `showLoserWait: Bool` state and `LoserWaitView` `fullScreenCover`
- Phone section: "Notify me" → "Send code →"
- `savePhone()` replaced by `sendCode()`: validates digits, calls `APIClient.shared.sendOTP()`, stores E.164 phone in `LoserFlowState.shared.pendingPhone`, pushes `.loserVerify`
- Error message shown inline in phone section if OTP send fails

**New LoserOTPView.swift** (`Views/Loser/`):
- Left-aligned top-anchored layout
- Two-tone heading "Check your" navy `serifDisplay(36)` + "phone." rust `serifDisplayItalic(36)`, rust rule
- Subtitle shows formatted phone number from `LoserFlowState.shared.pendingPhone` bold inline
- 6 digit boxes: rust active border, auto-advance, auto-submit on 6th digit
- "Didn't get it? Resend code" rust link
- On verify success: `APIClient.shared.updateLoserInfo()` + `PushManager.shared.registerWithServer()` + shows `LoserWaitView` as `fullScreenCover`
- `@State var showLoserWait = false` + `.fullScreenCover(isPresented: $showLoserWait)`

**LOFOApp.swift:**
- Added `.loserVerify: LoserOTPView()` to `navigationDestination` switch

---

### Phase 26h — iOS UI Polish Pass 4 — March 16, 2026

**Screens polished:** FinderDoneView, ItemCardView (shared), PhoneVerifyView, OTPVerifyView, WaitingView

**FinderDoneView.swift:**
- Heading split: `"Nice one."` navy `serifDisplay(38)` + `"We've got it."` rust `serifDisplayItalic(38)`, tight `-12pt` top padding stacking, rust rule (`40×1.5pt`, opacity 0.35), scanning subtitle
- Top padding `paddingXL`→`18pt`; VStack spacing `24`→`28`
- Item card rendered with `showTags: false`; tags moved to `FlowLayout` below card. Height-capped at `142pt` (≈5 rows) using `GeometryReader` in `.background()` for natural-height measurement. "See all →" / "Show less" rust underline toggle with spring animation
- Card subtitle: `LocationManager` (injected via `@Environment`, no `.shared`) `locationName` → formatted `createdAt` time fallback (`formattedSubmitTime`)
- Secret detail section: `HStack(spacing: 2)` lock emoji + small-caps label → field → helper text below
- AttrEditSheet open/close: `withAnimation(.spring(response: 0.95, dampingFraction: 0.72))`
- AttrEditSheet: `FlowLayout` gets `.frame(maxWidth: .infinity, alignment: .leading)` — fixes chip bleed in sheet. Padding `paddingM`→`paddingL`. + button `46×46`→`40×40`, icon `16pt`→`14pt`
- Build fixes: `LocationManager.shared` → `@Environment(LocationManager.self)`; `onChange(of:)` single-arg → two-arg `{ _, new in }`

**ItemCardView.swift:**
- Added `showTags: Bool = true` — when `false`, omits tag row; all existing callsites unaffected
- Added `subtitle: String? = nil` — when `showTags: false`, shows `subtitle ?? size` as muted caption with `.lineLimit(1)`

**PhoneVerifyView.swift (full rewrite):**
- Left-aligned top-anchored `ScrollView` layout (removed double-`Spacer` centering)
- Heading: "Where should / we reach you?" `serifDisplay(36)`, tight stacking, rust rule + subtitle
- Country code: `Menu` with ISO badge (`US`/`GB`/etc. in `tagBg` rounded rect), 12 countries, defaults to `Locale.current.region`. `ForEach` uses `\.region` as ID (fixes US/CA duplicate `+1` bug). Menu items text-only (no emoji — simulator can't render flag emoji)
- Phone field: `HStack` with menu + `1pt` divider + `TextField`. US auto-formats to `(XXX) XXX-XXXX` via `onChange`; other codes show raw digits capped at 15
- Privacy policy helper text using `Text` concatenation (muted body + rust underlined "Privacy policy")
- Button anchored to bottom via `.safeAreaInset(edge: .bottom)` with `LOFOTheme.cream` background
- Content fade+lift entrance via `@State var appeared`
- `sendCode` builds full phone as `countryCode.filter(\.isNumber) + localDigits`

**OTPVerifyView.swift:**
- Active digit box border: `LOFOTheme.navy` → `LOFOTheme.rust`
- Layout: double-`Spacer` centering → top-anchored left-aligned `ScrollView`
- Heading: "Please verify your / phone number." `serifDisplay(36)`, tight stacking, rust rule
- Subtitle: `Text` concatenation shows `formattedPhone` (strips leading `1`, formats 10-digit US as `(XXX) XXX-XXXX`) bold inline
- Resend: `"Didn't get it? "` (muted) + `"Resend code"` (rust underlined) inline `HStack`

**WaitingView.swift:**
- Radar `frame(height: 148)` → `frame(height: 96)` — eliminates invisible ring-space below navy circle
- Radar `.padding(.top, 36)` → `18`; `.padding(.bottom, 24)` → `17`
- Phone section: replaced broken `Text("🇺🇸")` with `Menu` + ISO badge + formatter (exact same pattern as PhoneVerifyView). `savePhone()` prepends country code. Button gets `icon: "arrow.right"`
- `parseISO()`: normalizes microseconds→milliseconds (Supabase returns 6-digit, `ISO8601DateFormatter` only handles 3), then tries ISO8601 + 4 `DateFormatter` fallback formats for timezone-less responses
- ⚠️ "Submitted at" time still blank — `parseISO` is correct but actual API `createdAt` format not confirmed. Debug: print `item?.createdAt` in console on appear

---

### Phase 26g — iOS UI Polish Pass 3 + Backend Intelligence Upgrades — March 15, 2026

**Build environment:** Xcode 26.3, Swift 6 strict concurrency (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`), iOS 26 SDK.

**Swift 6 / SwiftUI 6 build fixes:**
- `ScrollView { }` — iOS 26 added a new `@_alwaysEmitIntoClient nonisolated init(_ axes:content:)` alongside the deprecated `init(_ axes:showsIndicators:content:)`. Both accept `_ axes: Axis.Set = .vertical` so bare `ScrollView { }` and `ScrollView(.vertical) { }` are both ambiguous. Fix: `ScrollView(.vertical, showsIndicators: false) { }` — the `showsIndicators:` label uniquely identifies the old overload. Applied in `FinderDoneView.swift` (outer view + AttrEditSheet) and `WaitingView.swift` (outer view + WaitingAttrEditSheet).
- `Array.remove(at:)` — Swift 6 stdlib added a `@_alwaysEmitIntoClient nonisolated` overload, making the call ambiguous in strict concurrency mode. Fix: `details.removeSubrange(idx...idx)` (functionally identical, no ambiguity). Applied in both edit sheets.
- Root cause investigation technique: read `SwiftUI.swiftinterface` at `/Applications/Xcode.app/.../iPhoneOS.sdk/.../SwiftUI.swiftmodule/...arm64e-apple-ios.swiftinterface` to see the actual overload signatures. Build logs reference `SwiftUI.ScrollView.init:6:10` and `SwiftUI.ScrollView.init:3:22` — these are line:col in that virtual interface file.

**AttrEditSheet + WaitingAttrEditSheet (FinderDoneView.swift / WaitingView.swift):**
- `save()` now calls `APIClient.shared.redescribeAttributes(itemId:itemType:details:)` instead of `updateAttributes`. This routes edits through Claude so "color was actually blue" correctly updates the `color` column rather than being dumped into `features` verbatim.

**WaitingView status cards:**
- Removed "AI-powered visual matching" card (sparkles icon) — redundant/generic.
- Location card changed from hardcoded "Within 10 mi of your location" to dynamic "Near {locationLabel}" where `locationLabel` reads `LoserFlowState.shared.whereDescription` (falls back to "your location" if nil).

**LoserFlowState.swift:**
- Added `whereDescription: String?` field + reset in `reset()`.

**LostPromptView.swift:**
- After submit, sets `LoserFlowState.shared.whereDescription = item.locationName ?? (whereDescription.isEmpty ? nil : whereDescription)`. Claude's extracted location name takes priority over the typed "Where?" field.

**Item.swift:**
- Added `locationName: String?` with `CodingKey "location_name"`. Optional field — only populated by `/items/from-text` response; all other endpoints return nil (decoded as nil automatically since field is `String?`).

**APIClient.swift:**
- Added `redescribeAttributes(itemId:itemType:details:)` → `PATCH /items/{id}/redescribe`.
- `validateResponse(_ response:)` now takes `data: Data` as second parameter. On non-2xx, attempts to decode `{"detail": "..."}` from the response body and includes it in the thrown `APIError`. All four call sites (get, post, patch, perform, photo upload) updated. Error messages now show e.g. "Error 502: Claude API error: overloaded_error" instead of "Server error (502)".

**Backend main.py (deployed to Railway, commit `0a297e6`):**
- `PATCH /items/{id}/redescribe` — new endpoint. `RedescribeRequest(item_type, details: list[str])`. Builds description string, calls Claude with `_TEXT_SYSTEM_PROMPT`, validates profile, updates all attribute columns in DB, calls `_store_embedding`. Returns `{ok, item_type, color, material, size, features}` (same shape as `/attributes`).
- `TextItemResponse(ItemResponse)` — subclass adds `location_name: Optional[str] = None`. Used only on `/items/from-text`. NOTE: adding fields directly to `ItemResponse` crashes Railway on startup (FastAPI builds OpenAPI schema at startup; modifying a multi-endpoint response model triggers a schema conflict). Always subclass instead.
- `_TEXT_SYSTEM_PROMPT` updated: asks Claude to extract `location` (human-readable name), `latitude`, and `longitude` as decimal numbers using its world knowledge. Instructs Claude to return the most precise location (specific field/terminal/corner), not just city.
- `create_item_from_text` geocoding priority: (1) explicit `where_description` → Nominatim, (2) Claude's `latitude`/`longitude` direct (most precise — Claude knows "beach chalet soccer fields" exact coords), (3) Nominatim on Claude's `location` string as fallback, (4) device GPS.
- `_geocode` improved: now retries up to 2× with progressively shorter queries by dropping leading words (handles cases where Nominatim doesn't know a specific sub-landmark but does know the parent).

**Railway crash debugging notes:**
- Symptom: `{"status":"error","code":502,"message":"Application failed to respond"}` from Railway — entire app down, not a Claude error.
- Cause: adding a field to `ItemResponse` (used as `response_model` on multiple endpoints) caused FastAPI to fail during startup OpenAPI schema generation.
- Fix: use a subclass (`TextItemResponse`) for the specific endpoint only.
- Detection method: revert the commit, confirm app comes back up, then re-apply changes with the subclass approach.

---

### Phase 26d — Bug Fixes + Native Camera Viewfinder — March 13, 2026

**What changed:**

**Bug fix 1 — 502 on photo upload (backend `main.py`):**
- Root cause: `claude_client.messages.create()` (synchronous Anthropic SDK) was called directly inside `async def create_item_from_photo`, blocking uvicorn's event loop. Railway's proxy saw no response and returned 502.
- Also: `_store_embedding()` (sync Voyage SDK) had the same problem.
- Fix: both wrapped in `await asyncio.to_thread(...)`. `import asyncio` added to top of `main.py`.
- Committed and pushed to Railway (auto-deploy).

**Bug fix 2 — iOS photos too large / timeout:**
- Simulator photos from the library are full-resolution (3000×4000+ px). JPEG at 0.8 quality without resizing = 3–5 MB payload.
- Fix 1: `UIImage.lofoResized(maxDimension: 1280)` resize helper added. Photos resized before compression (0.72 JPEG quality → typically under 300 KB).
- Fix 2: `APIClient` now has a dedicated `uploadSession` with 90s request / 120s resource timeout for photo uploads. Default session remains 30s/60s for all other calls.

**FinderCameraView — full native camera viewfinder rebuild:**
- **New `CameraManager.swift`** (`Services/`) — `NSObject` subclass (not `@Observable` to avoid `@MainActor` vs AVFoundation background-thread conflict). Owns `AVCaptureSession`, handles permission request, configures session on dedicated `DispatchQueue`, delivers captured photo data via `onCapture` callback on main thread.
- **New `CameraPreviewView.swift`** (`Views/Finder/`) — `UIViewRepresentable` whose backing layer IS `AVCaptureVideoPreviewLayer` (via `layerClass` override). Zero bridging overhead.
- **`FinderCameraView.swift`** completely rewritten:
  - Full-screen live `CameraPreviewView` on device; dark radial gradient fallback on simulator (no camera available).
  - Corner bracket L-shape overlays (4× Path-drawn, 36px inset, 26px arm, white 0.65 opacity).
  - Center copy: "Point at what *you found.*" (34pt serif) + "AI will read it automatically" subtitle.
  - Bottom bar: dark gradient → solid strip with green-dot location pill, shutter button (82px outer ring + 68px inner fill), Back capsule (left), library PhotosPicker icon (right).
  - Shutter tap → `capturePhoto()` → `analyzePhoto()` (resize + API call) → `FinderDoneView` on success.
  - On error: returns to camera view (clears `capturedImageData`).
- **`project.pbxproj`** — `INFOPLIST_KEY_NSCameraUsageDescription` added to both Debug and Release target configs. Required for App Store and for the system camera permission alert.

**Build result:** BUILD SUCCEEDED — iPhone 17 Pro simulator, iOS 26.3.1

---

### Phase 26c — iOS Visual Polish (Remaining Screens) + iOS 18 Zoom Transition — March 13, 2026

**What changed:** Completed the visual upgrade pass across all remaining screens. Every screen in the app now has entrance animations. Added iOS 18 zoom navigation transition for the match reveal moment.

**`Theme.swift`:**
- New `MatchZoomNSKey: EnvironmentKey` for sharing the `@Namespace` across WaitingView (source) and MatchView (destination). Default is `Namespace().wrappedValue` — safe throwaway that falls back to default push animation if not injected.
- `extension EnvironmentValues { var matchZoomNS: Namespace.ID }` — accessed via `@Environment(\.matchZoomNS)` in views.

**`LOFOApp.swift`:**
- `@Namespace private var matchZoomNS` added to App struct.
- `.environment(\.matchZoomNS, matchZoomNS)` injected on the NavigationStack.
- `.match` `navigationDestination` case now applies `.navigationTransition(.zoom(sourceID: "matchRadar", in: matchZoomNS))` under `if #available(iOS 18.0, *)`. Falls back to standard push on iOS 17.

**`WaitingView.swift`:**
- `@Environment(\.matchZoomNS) private var matchZoomNS` added.
- New `@ViewBuilder var radarWithSource` wraps `radarAnimation` with `.matchedTransitionSource(id: "matchRadar", in: matchZoomNS)` under `if #available(iOS 18.0, *)`. Used in place of `radarAnimation` in body. Effect: the searching radar circle zooms out into the MatchView reveal.

**`LostPromptView.swift`:** 3-stage entrance — heading spring-scales from 97%→100% + lifts (0ms), description editor fades+lifts (130ms delay), where field + button fade+lift (240ms delay). `lofoCardShadow()` added on description TextEditor and where TextField.

**`AllSetView.swift`:** 2-stage entrance — heading spring-scales from 97%→100% + lifts (0ms), payout section + Done button fade+lift (180ms delay). `lofoCardShadow()` on `appPicker` and `savedRow`. `savedRow` uses `LOFOPressStyle` Edit button + rust-colored checkmark (matches MatchView's reason checkmarks). Handle fields now have smooth `.transition(.opacity.combined(with: .offset(y: 8)))` on appear.

**`ConfirmedView.swift`:** Big-moment 3-stage entrance (triggers `HapticManager.matchConfirm()` on appear). New `confirmedBadge` — rust-light circle with a rust checkmark icon (56×56). Heading spring-scales from 92%→100% (tighter spring response: 0.46, damping: 0.72 for a more "pop" feel), item card rises from below at 22px (delay 160ms), phone field + buttons fade+lift at 14px (delay 320ms). `lofoCardShadow()` on phone TextField.

**`ReunionView.swift`:** Celebratory design. New `connectionGraphic` — three concentric circles (rust/rustLight palette) with a `link.circle.fill` SF Symbol (34pt). Outer ring gently pulses in size (1.8s easeInOut repeatForever) after entrance. 3-stage entrance: graphic spring-scales from 80%→100% (0ms), text fade+lift (200ms delay), Done button fade+lift (380ms delay). Heading font size bumped 32→34 to match AllSetView's "All set." title weight.

**`FinderCameraView.swift`:** Photo prompt fades+lifts+scales (97%→100%) on appear with 60ms delay. `cameraIconArea` replaces flat camera icon — two concentric soft circles (navy opacity 4–6%) behind the camera icon for depth. `lofoCardShadow()` on the dashed-border photo picker card. Selected image also uses `lofoCardShadow()` (replaces manual `.shadow()`). `aiOverlay` overhauled — pulsing concentric rings (matching WaitingView radar pattern, 3 rings, 2.2s easeOut repeatForever, staggered by 0.65s) with a centered sparkles icon in a soft white circle. "Reviewing photo…" bumped to 20pt. `scanPulse` state starts on aiOverlay's own `.onAppear`.

**Build result:** BUILD SUCCEEDED — iPhone 17 Pro simulator, iOS 26.3.1

---

### Phase 26b — iOS Visual Polish — March 13, 2026

**What changed:** Comprehensive visual upgrade to close the aesthetic gap vs the HTML prototype.

**New in `Theme.swift`:**
- `LOFOPressStyle: ButtonStyle` — spring scale (0.965) + opacity (0.88) on press; applies to every `Button` in the app via `.buttonStyle(LOFOPressStyle())`
- `lofoCardShadow()` view modifier — two-layer shadow (14px soft + 3px sharp) for white cards over cream background

**`LOFOButton.swift`:** `.buttonStyle(LOFOPressStyle())` added; height bumped 52→54; icon weight `.medium`

**`HomeView.swift`:** Three-phase staggered entrance — LOFO wordmark spring-scales from 88%→100% + fades (0ms), subtitle fades + lifts (180ms delay), buttons slide up 22px + fade (280ms delay). Gear button uses `LOFOPressStyle`. Both CTA buttons use `LOFOPressStyle` directly.

**`ItemCardView.swift`:** Flat 1px border replaced with `lofoCardShadow()` — cards now float over the cream background.

**`MatchView.swift`:** Full entrance sequence — navy banner fades+slides down from above (0ms), content spring-rises from below (200ms delay). `@State var barProgress: CGFloat = 0` animates from 0→score over 900ms with 450ms delay (easeOut). Confidence bar tracks `barProgress` instead of raw score. Reasons list checkmarks use cream rust-circle background. `lofoCardShadow()` on reasons card.

**`WaitingView.swift`:** Radar pulse animation — 3 concentric rings (72/110/148px) with staggered `easeOut` repeat (no autoreverses, 2.4s, 0.72s delays) expand outward and fade to 0 continuously. Central `location.magnifyingglass` icon in a soft navy circle. Status pill transitions animated. Content entrance animation (fade+lift).

**`LoserWaitView.swift`:** Orb upgraded — 4 rings (220/155/100/64px). Outer 3 are stroke rings with staggered easeInOut breathe (3.8–4.5s). Inner core uses `RadialGradient` fill (white 0.22→0.06). Center 10px white dot. Text entrance animates in 300ms after appear.

**`LOFOApp.swift`:** Stripe test key `pk_test_51T7nEr...` wired in.

**Build result:** BUILD SUCCEEDED — iPhone 17 Pro, iOS 26.3.1

**Also in this session (Phase G file changes):**
- `project.pbxproj`: bundle ID `ai.lofo.app`, version `1.0.0`, portrait-only, `UILaunchScreen_Generation = YES` with `LOFOCream` named color
- `Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png`: 1024×1024 app icon
- `Assets.xcassets/LOFOCream.colorset`: cream `#F5F2EC` named color for launch screen
- StripePaymentSheet SPM package added in Xcode (v25.7.1)
- Supabase `device_tokens` table migration run

**Remaining manual steps (pending Apple Developer enrollment):**
1. developer.apple.com → App ID `ai.lofo.app` (enable Push + Apple Pay) + APNs key (.p8) + Merchant ID `merchant.ai.lofo`
2. Railway: add `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_AUTH_KEY`, `APNS_BUNDLE_ID`
3. Xcode: Signing & Capabilities → Apple Pay → `merchant.ai.lofo`
4. Product → Archive → TestFlight upload
5. App Store Connect: listing + screenshots + submit

---

### Phase 26 — iOS Phase G: App Store Prep — March 13, 2026

**What changed:** iOS app prepared for App Store submission. No Swift code changes — all changes are in project configuration and assets.

**New files:**
- `LOFO/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png` — 1024×1024 app icon. Navy (#1A1A2E) background, cream (#F5F2EC) LOFO wordmark in Palatino serif, subtle dotted arc motif below. Xcode auto-generates all required icon sizes (60×60, 120×120, 180×180, etc.) from this single file. `Contents.json` updated to reference `AppIcon-1024.png`.
- `LOFO/LaunchScreen.storyboard` — Custom launch screen. Cream background (`#F5F2EC`), `LOFO` label centered in Palatino Roman 64pt, navy color. No spinner. Replaces the auto-generated plain white launch screen. Auto-included via `PBXFileSystemSynchronizedRootGroup`.

**`project.pbxproj` changes (both Debug + Release target configs):**
- `PRODUCT_BUNDLE_IDENTIFIER`: `com.lofo.LOFO` → `ai.lofo.app`
- `MARKETING_VERSION`: `1.0` → `1.0.0`
- `INFOPLIST_KEY_UILaunchScreen_Generation = YES` removed; `INFOPLIST_KEY_UILaunchStoryboardName = LaunchScreen` added
- `INFOPLIST_KEY_UISupportedInterfaceOrientations_iPhone`: restricted to `UIInterfaceOrientationPortrait` (portrait-only — standard for consumer apps, required by App Store if no landscape design exists)

**What remains — manual steps in Xcode + Apple Developer + Railway:**
1. Supabase migration for `device_tokens` table (if not done in Phase F)
2. Apple Developer: create App ID `ai.lofo.app`, APNs key, Merchant ID `merchant.ai.lofo`
3. Railway: add `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_AUTH_KEY`, `APNS_BUNDLE_ID` env vars
4. Xcode: File → Add Package Dependencies → `https://github.com/stripe/stripe-ios` → `StripePaymentSheet`. Replace `pk_test_YOUR_STRIPE_PUBLISHABLE_KEY` in `LOFOApp.init()`. Add Apple Pay capability with `merchant.ai.lofo`.
5. Archive → Product → Archive → Distribute App → App Store Connect → Upload
6. App Store Connect: create listing with name "LOFO", subtitle "Lost & found, reunited by AI", description, keywords, screenshots (6.7" required at 1290×2796), privacy URL, support URL
7. Submit for review

---

### Phase 25 — iOS Phase F: Push Notifications + Stripe PaymentSheet — March 13, 2026

**What changed:** iOS app gains push notification infrastructure and full Stripe PaymentSheet/Apple Pay wiring. Backend adds APNs delivery alongside SMS in both notification helpers.

**New iOS files:**
- `AppDelegate.swift` — `UIApplicationDelegate` registered via `@UIApplicationDelegateAdaptor`. Receives `didRegisterForRemoteNotificationsWithDeviceToken` and `didFailToRegisterForRemoteNotificationsWithError` → forwards both to `PushManager`.
- `Services/PushManager.swift` — `@Observable` singleton. `requestPermission()` calls `UNUserNotificationCenter.requestAuthorization` + `UIApplication.registerForRemoteNotifications()`. `handleDeviceToken()` stores the hex token string. `registerWithServer(phone:)` calls `POST /devices/register`. Implements `UNUserNotificationCenterDelegate` to show banners in foreground and broadcast `Notification.Name.lofoNotificationTap` on tap with `screen` key from payload.

**Updated iOS files:**
- `LOFOApp.swift` — Added `@UIApplicationDelegateAdaptor(AppDelegate.self)`, `.onAppear { PushManager.shared.requestPermission() }`, `.onReceive(NotificationCenter.default.publisher(for: .lofoNotificationTap))` for deep links (pops to root; extendable via `screen` key). Added Stripe publishable key set in `init()` under `#if canImport(StripePaymentSheet)`.
- `APIClient.swift` — Added `registerDevice(phone:deviceToken:platform:)` → `POST /devices/register`.
- `TipView.swift` — Full Stripe `PaymentSheet` + Apple Pay under `#if canImport(StripePaymentSheet)`. `startPayment()` calls backend for `client_secret`, then calls `presentPaymentSheet(clientSecret:)`. Uses `withCheckedContinuation` to bridge `PaymentSheet.present(from:completion:)` into async/await. Apple Pay config: `merchantId = "merchant.ai.lofo"`, `merchantCountryCode = "US"`. Root VC obtained via `UIApplication.connectedScenes` chain. Falls back to direct navigation when SDK not linked.
- `OTPVerifyView.swift` — After OTP success, calls `await PushManager.shared.registerWithServer(phone:)` before navigating to `.allSet`.
- `WaitingView.swift` — After loser phone save, calls `await PushManager.shared.registerWithServer(phone:)` before showing `LoserWaitView`.

**Backend (`main.py`):**
- `DeviceRegisterRequest` schema added.
- `POST /devices/register` endpoint — normalizes phone to E.164, upserts `(phone, device_token, platform)` into `device_tokens` table via `INSERT … ON CONFLICT DO NOTHING`.
- `_get_device_tokens(phone)` helper — queries `device_tokens` table by phone, returns `list[str]`.
- `_push_apns(device_token, title, body, screen)` helper — uses `httpx.Client(http2=True)` for APNs HTTP/2 API. Authenticates via `PyJWT` ES256 token (`iss=APNS_TEAM_ID`, `iat=now`, `kid=APNS_KEY_ID`). Payload: `{"aps": {"alert": {"title", "body"}, "sound": "default"}, "screen": screen}`. Falls back gracefully (prints + returns) if env vars not configured.
- `_notify_waiting_losers()` — now sends APNs push (title: "LOFO — possible match found", screen: "waiting") for each registered token alongside existing SMS.
- `_notify_matched_finder()` — now sends APNs push (title: "LOFO — someone's looking", screen: "finder") for each registered token alongside existing SMS.

**`requirements.txt`:** `httpx` → `httpx[http2]` for HTTP/2 transport (required by APNs API).

**DB migration required (run in Supabase SQL editor):**
```sql
CREATE TABLE IF NOT EXISTS device_tokens (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    phone VARCHAR NOT NULL,
    device_token TEXT NOT NULL,
    platform VARCHAR NOT NULL DEFAULT 'ios',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(phone, device_token)
);
```

**Railway env vars to add:** `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_AUTH_KEY` (full .p8 file contents), `APNS_BUNDLE_ID` (e.g. `ai.lofo.app`). Optional: `APNS_ENVIRONMENT=sandbox` for Simulator testing.

**Xcode steps before Stripe PaymentSheet activates:**
1. File → Add Package Dependencies → `https://github.com/stripe/stripe-ios` → add `StripePaymentSheet` target.
2. Replace `pk_test_YOUR_STRIPE_PUBLISHABLE_KEY` in `LOFOApp.init()`.
3. Signing & Capabilities → Apple Pay → add merchant ID `merchant.ai.lofo` (register at developer.apple.com first).

---

### Phase 24 — iOS Phase E: First Simulator Build — March 12, 2026

**What changed:** iOS app goes from skeleton to compilable. First successful build in iPhone 17 Pro simulator (iOS 26.3.1).

**Compile error fix (`APIClient.swift`, `Item.swift`, `Match.swift`):**
- Root cause: project has `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` + `SWIFT_APPROACHABLE_CONCURRENCY = YES` (Xcode 26.3 defaults). This made all types in the module implicitly `@MainActor`, meaning their `Codable` conformances were MainActor-isolated. The `nonisolated` generic methods in `APIClient` required `T: Sendable`, but `@MainActor`-isolated `Codable` conformances can't satisfy that.
- Fix: removed `nonisolated` and `Sendable` from `APIClient` (class and all methods) + removed `Sendable` from all model structs (`Item`, `Match`, `VerifyResult`, `CoordinateRequest`, `PaymentIntentResult`, `UserStats`, `GenericOK`, `AttributesResult`). URLSession async/await works fine on MainActor — network I/O runs in background, only result handling is on main.

**`LoserWaitView.swift` (new):**
- Navy `fullScreenCover` shown after loser saves phone in `WaitingView`
- 3 concentric ring circles with staggered pulse animations (4s ease-in-out, delays 0/1.33s/2.66s) — breathing orb effect matching web app `screen-loser-wait`
- Copy: "Hang tight. Think positive." / "People do good things. We'll text you the moment someone finds your [item]."
- "Got it" button dismisses; `WaitingView.savePhone()` triggers `showLoserWait = true` after success

**`TipView.swift` (new):**
- $5/$10/$20 amount picker (selection highlighted navy) + "Skip" underline link
- On pay: calls `POST /tip/create-payment-intent` → stores `client_secret` → navigates to `.reunion`
- Stripe `PaymentSheet` wiring deferred — `TODO (Phase E+)` comment marks the exact insertion point
- `ConfirmedView` now navigates to `.tip` instead of `.reunion` after `coordinateHandoff`

**Fonts (`LOFO/Fonts/` — new directory):**
- Downloaded from Google Fonts CDN: `DMSans-Regular.ttf`, `DMSans-Medium.ttf`, `DMSans-Bold.ttf`, `DMSerifDisplay-Regular.ttf`
- Registered at app launch via `CTFontManagerRegisterFontsForURL` in `LOFOApp.init()` — no `Info.plist` changes needed (project uses `GENERATE_INFOPLIST_FILE = YES`)
- `Theme.swift` `sans()` function now uses `DMSans-Regular/Medium/Bold` with system font fallback
- `PBXFileSystemSynchronizedRootGroup` auto-includes the Fonts folder in the bundle — no `.pbxproj` edits needed

**`AppState.swift`:** Added `.tip` to `Screen` enum (between `.confirmed` and `.reunion`)

**`LOFOApp.swift`:** Added `case .tip: TipView()` to `navigationDestination`; added `init()` that calls `LOFOTheme.registerFonts()`

**Stripe iOS SDK:** NOT added via SPM — TipView calls backend directly for first build. To add in Phase F: Xcode → File → Add Package Dependencies → `https://github.com/stripe/stripe-ios` → add `StripePaymentSheet` target, then replace the TODO in TipView.

**Build result:** `** BUILD SUCCEEDED **` — iPhone 17 Pro simulator, iOS 26.3.1, Xcode 26.3

---

### Phase 23 — SwiftUI iOS App Skeleton — March 12, 2026

**What changed:** Native iOS app built at `~/Desktop/LOFO/`. Xcode 26.3 project targeting iOS 17+. 28 Swift files covering the complete screen topology. Backend API unchanged.

**Project location:** `~/Desktop/LOFO/LOFO.xcodeproj`

**Architecture decisions:**
- iOS 17+ target — uses `@Observable` macro (no ObservableObject), `NavigationStack` with path-based routing, `PhotosUI` for camera/library
- Navigation: `AppState.path: NavigationPath` drives all screen transitions. `appState.push(.screen)` = `go('screen-name')` from web app
- State: `FinderFlowState.shared` and `LoserFlowState.shared` are singleton `@Observable` objects that hold flow data across screens (equivalent to the `state` object in LOFO_MVP.html)
- All API calls via `APIClient.shared` — async/await, no third-party networking library needed

**Files created:**
- `Theme.swift` — color palette matches web CSS vars (`--navy: #1A1A2E`, `--cream: #F5F2EC`, etc.), typography helpers for DM Sans + DM Serif Display
- `Models/Item.swift`, `Models/Match.swift` — Codable structs matching all backend JSON responses
- `Services/APIClient.swift` — complete: submitPhoto, submitText, findMatches, verifyOwnership, sendOTP, verifyOTP, updateFinderInfo, updateLoserInfo, updateAttributes, coordinateHandoff, createPaymentIntent, statsByItems
- `Services/LocationManager.swift` — CLLocationManager wrapper, requestLocation on appear
- `Services/HapticManager.swift` — light/medium/heavy/success/error + matchConfirm triple-pulse
- `ViewModels/AppState.swift` — NavigationStack path, showMenu, myItemIDs (UserDefaults)
- `ViewModels/FinderFlowState.swift`, `ViewModels/LoserFlowState.swift` — per-flow state singletons
- `ViewModels/MenuViewModel.swift` — loads usage stats from API
- `Views/Home/HomeView.swift` — two CTAs (camera/text), gear icon
- `Views/Home/MenuSheet.swift` — gear menu: My Usage (stats), Support (FAQ accordion + contact), Information (Terms, Privacy, About)
- `Views/Shared/ItemCardView.swift` — emoji/photo thumbnail, attribute tags, FlowLayout
- `Views/Shared/TagChipView.swift` — attribute chip + removable variant
- `Views/Shared/LOFOButton.swift` — primary/secondary/ghost styles, loading state
- `Views/Shared/ReunionView.swift` — terminal "You're all set" screen
- `Views/Shared/PhotoLightboxView.swift` — fullScreenCover with AsyncImage, claim/dismiss CTAs
- `Views/Finder/FinderCameraView.swift` — PhotosPicker, AI overlay animation, GPS pre-fetch
- `Views/Finder/FinderDoneView.swift` — AI result card, secret detail input
- `Views/Finder/PhoneVerifyView.swift` — phone input
- `Views/Finder/OTPVerifyView.swift` — 6-digit inputs, auto-advance, auto-submit
- `Views/Finder/AllSetView.swift` — payout app picker, dual-entry handle confirm
- `Views/Loser/LostPromptView.swift` — description + where field, GPS
- `Views/Loser/WaitingView.swift` — 5s polling Task, status pills, phone capture after 3 polls
- `Views/Loser/MatchView.swift` — navy banner, confidence bar, item card, location pill, reasons, photo lightbox
- `Views/Loser/OwnershipVerifyView.swift` — claim input, Claude verify
- `Views/Loser/ConfirmedView.swift` — confirmation, phone capture, coordinate handoff
- `LOFOApp.swift` — wires NavigationStack + all `navigationDestination` destinations + MenuSheet sheet

**Phase 24 complete. Still needed (Phase 25 / iOS Phase F):**
- Stripe iOS SDK via SPM (`https://github.com/stripe/stripe-ios`) — add via Xcode File > Add Package Dependencies. Wire `StripePaymentSheet` at the TODO in `TipView.swift`
- Apple Pay: add `PKPaymentAuthorizationController` + merchant ID entitlement once Stripe SDK is linked
- Push notifications: `PushManager`, `POST /devices/register`, APNs in backend notify helpers
- Deep link handling: push tap opens app to relevant screen

---

### Phase 22 — Admin Charts, Map Fix, Mobile Responsive — March 12, 2026

**What changed:** Two data visualization chart cards added to admin dashboard. Blank map bug fixed. Full mobile responsive layout.

**Chart cards (`admin.html`):**
- **Lost vs Found** — Canvas-drawn grouped bar chart (red = lost, blue = found). Shows daily item counts for the current ISO week (Mon–Sun). Auto-scaling Y axis with grid lines, rounded bar tops, day labels. Legend in top-right of card.
- **Avg. Time to Reunion** — Hero number (avg days from loser item creation to reunion coordination, last 30 days). Green/red delta vs previous 30-day window. Active matches (reunion) count. Canvas-drawn smooth bezier line chart with gradient fill, dots at data points, week labels (W1–W5).
- Both charts redraw on window resize (debounced 200ms).
- Charts load in parallel with stats and table data via `loadAll()`.
- "No reunion data yet" fallback when line chart has no data.

**Backend (`main.py`):**
- `GET /admin/charts` — admin-auth-protected endpoint returning: `daily_items` (7 rows via `generate_series`, LEFT JOIN items), `reunion_avg_days` (epoch math on `reunions.created_at - items.created_at`), `reunion_diff_vs_prev` (30-day vs previous 30-day comparison), `active_matches` (active reunion count), `reunion_weekly` (grouped by week, last 35 days).

**Blank map fix (`admin.html`):**
- Root cause: Leaflet map initialized while `#map-tab-container` was `display: none`. Leaflet calculated container size as 0×0, tiles never loaded. Fixed by calling `_adminMap.invalidateSize()` via `setTimeout(..., 0)` in `loadMapTab()` — defers to next tick so the browser reflows first. Affects both geo-link clicks and direct map tab switches.

**Mobile responsive (`admin.html`):**
- 900px breakpoint: stat cards → 2×2 grid, chart cards → single column, header wraps (logo + controls top, time filters centered below), tabs horizontally scrollable, detail panel photo stacks above fields (2-col), debug inputs/metrics/items all single-column.
- 540px breakpoint: tighter padding (36px → 12px), smaller card values/icons/fonts, login card padding reduced, hover nav hints hidden, table cells reduced, map overlays nudged inward, debug button full-width, chart cards tighter padding.

---

### Phase 21 — Bug Fixes, XSS Hardening, Admin UX — March 12, 2026

**What changed:** Deep-dive codebase audit found 8 bugs. All fixed. Admin tabs and geo links improved.

**Bug fixes (`main.py`):**
- `PATCH /items/{id}/loser-info` now normalizes phone to E.164 via `_normalize_phone()` before DB write. Previously stored raw user input, breaking SMS matching.
- `GET /stats/by-items` capped at 100 IDs (`_STATS_BY_ITEMS_MAX_IDS`) to prevent DoS via oversized query strings.

**Bug fixes (`database.py`):**
- `get_connection()` pool corruption: when a dead pooled connection was replaced with a fresh `psycopg2.connect()`, the replacement was returned to the pool via `putconn()` — corrupting pool state. Now tracks `used_replacement` flag; replacement connections are closed directly in `finally`, pooled connections returned normally.

**Bug fixes (`security.py`):**
- `os.environ["JWT_SECRET"]` → `os.getenv("JWT_SECRET", "")` + explicit `RuntimeError` if empty. Prevents cryptic `KeyError` crash on startup.

**Bug fixes (`resolve.html`):**
- `doConfirm()` now returns `true`/`false` based on API response. `submitTip()`, `skipTip()`, and `handleYes()` (no-finder path) all check the result before showing success state. On failure: `showConfirmError()` displays error message with retry option.
- `handleYes()` made `async` so the no-finder path properly `await`s `doConfirm(0)`.

**XSS hardening (all 4 frontend files):**
- Added `esc()` helper (escapes `&<>"'`) to `resolve.html`, `admin.html`, `LOFO_MVP.html`, `map.html`.
- Applied to all user-controlled text rendered via `innerHTML` or template literals.
- Photo URLs validated with `startsWith('https://')` before use in `<img src>` — blocks `javascript:` and `data:` schemes.

**Absolute API paths (`admin.html`, `map.html`):**
- Added `const API = 'https://lofo-ai-production.up.railway.app'` to both files.
- All `fetch()` calls and `window.location.href` redirects updated from relative `/admin/...` to `${API}/admin/...`.
- Static `href="/admin"` links updated via JS on page load.

**Admin tabs (`admin.html`):**
- Removed dark background bar, borders, border-radius, and box-shadow from `.panel-tabs`.
- Tabs now use flat text with a 2px accent-colored underline on the active tab via `::after` pseudo-element.
- Clean separation from table column headers (which use uppercase + letter-spacing).

**Clickable geo coordinates (`admin.html`):**
- Table location columns and detail panel GPS field render green clickable `<span class="loc-link">` when latitude is present.
- `focusMapOnItem(itemId)` sets `_adminMapFocusItemId` and switches to map tab.
- `renderMapPins()` stores each marker in `_adminMarkerById[item.id]`. After rendering, if a focus item is pending, calls `_adminClusters.zoomToShowLayer(marker, callback)` to zoom in (unclustering if needed) and opens the popup automatically.

---

### Phase 20 — In-App Menu Drawer — March 12, 2026

**What changed:** Gear icon on home screen opens a slide-up menu drawer covering App Store legal/support requirements.

**Gear button (`LOFO_MVP.html`):**
- White circle button (SVG gear icon, 36px) in top-right of home screen, positioned via `.home-topbar` flex row alongside the LOFO wordmark
- Same visual treatment as the reference iOS weather app screenshot

**Menu drawer (`LOFO_MVP.html`):**
- Slides up from bottom, dark semi-transparent backdrop (tap to close), handle bar + close ✕ button
- Three sections:
  - **My Usage** — User-level stats: Lost Reports, Found Reports, Reunited. Fetched from `GET /stats/by-items?ids=` on open using item IDs stored in `localStorage` (`lofo_my_item_ids`) when user creates finder or loser items. DM Serif Display numerals. Shows "–" when no items yet.
  - **Support** — FAQs (expand/collapse section, then per-question accordion for 5 FAQs). Contact Us (expand-in-place form → `mailto:support@lofo.ai`).
  - **Information** — Terms of Service, Privacy Policy (both open `/terms` and `/privacy` in new tab), About LOFO (expand-in-place blurb), App Version `1.0.0`.

**Backend (`main.py`):**
- `GET /terms` — serves `terms.html`
- `GET /privacy` — serves `privacy-policy.html`
- `GET /stats/by-items?ids=` — returns `{lost_count, found_count, reunited_count}` for comma-separated item UUIDs; user-level stats (no auth)

---

### Phase 19 — Map as Admin Tab + Map Enhancements + Admin Row Expansion — March 12, 2026

**What changed:** Live map moved from a separate page (`/map`) to a 6th tab inside the admin dashboard panel. Period filter, 10-mile radius circles, and match pair lines added. Admin table rows made clickable with inline detail expansion.

**Admin row expansion (`admin.html`):**
- Lost Items and Found Items rows are now clickable — expand an animated inline panel below the row
- Panel shows: full photo (160px, click to open original), all attributes (color, material, size, full features list), status pill, full reported/expiry timestamps, GPS (6 decimal places), unmasked phone number, payout app+handle (finder only), secret indicator (finder only), item ID (monospace)
- One row open at a time — clicking another row collapses the previous
- Click same row again to collapse
- Action buttons (Deactivate/+30d) and photo thumbnail use `event.stopPropagation()` — don't trigger expand
- Full item data stored in `rowDataMap` keyed by ID; no extra API calls on expand

**Why:** Eliminates the JWT/sessionStorage hand-off between `/admin` and `/map`. Everything stays in one auth context. Also makes the map a real ops tool.

**Backend (`main.py`):**
- `GET /admin/map-pins` now accepts `?period=` — filters items by `created_at` (Today/Week/Month/All)
- `GET /admin/map-pairs` — new endpoint returning reunion pairs where both items have GPS coords; used for drawing match lines. Also accepts `?period=` filtering on `r.created_at`.

**Frontend (`admin.html`):**
- Leaflet + MarkerCluster CSS/JS loaded in `<head>`
- 6th tab "🗺 Map" added to the panel tab row
- Header "🗺 Live Map" `<a>` → `<button onclick="setTab('map')">` (activates tab, no page nav)
- `#map-tab-container` added inside panel alongside `#table-container` and `#debug-container`
- `setTab('map')` shows map container, sets `panel.style.overflow = 'visible'` (lets Leaflet popups extend above panel edge), calls `loadMapTab()`
- `setPeriod()` → `loadAll()` → `loadMapTab()` when on map tab — period filter auto-refreshes map
- Map lazily initializes Leaflet on first tab visit
- 10-mile radius circle (`L.circle`, 16093.4m): drawn on `popupopen`, removed on `popupclose`
- Match pair lines: dashed green `L.polyline` for each reunion pair with GPS on both sides. Tooltip shows item types. Toggle in legend.
- Floating overlays (legend, stats, refresh button) positioned inside `#map-tab-container`
- `map.html` and `GET /map` route kept intact as standalone fallback

---

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

*Built with Cursor + Claude. Zero prior coding experience. March 5–12, 2026.*
