# LOFO.AI — Build Progress & Context
*Last updated: March 16, 2026 — Phase 26k / UI polish pass 6: all screens consistent, radar animation, stats UUID bug fix, title case CTAs. BUILD SUCCEEDED. Full summary in Session History below.*

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
| 26 — iOS Phase G: App Store Prep *(iOS Phase G)* | ✅ Complete (manual steps remain) | App icon 1024×1024, LaunchScreen.storyboard, bundle ID `ai.lofo.app`, version `1.0.0`, portrait-only. Archive → TestFlight + App Store Connect: manual steps below. |

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

*None — all known bugs resolved. (WaitingView "Submitted at" blank fixed in Phase 26i — PostgreSQL `::text` timestamp format confirmed as `2026-03-16 19:58:14.07162+00`.)*

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
| **G — App Store Prep** | **26** | **✅ Complete (manual steps remain)** | App icon 1024×1024, `LaunchScreen.storyboard`, bundle ID `ai.lofo.app`, version `1.0.0`, portrait-only. Stripe SPM + Apple Pay + APNs + Archive + App Store Connect: manual steps below. |

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
> **iOS app — ALL phases A–G complete + UI polish passes 2–5 done:**
> Native SwiftUI at `~/Desktop/LOFO/LOFO.xcodeproj`. **BUILD SUCCEEDED** — iPhone 17 Pro, iOS 26.3.1, Xcode 26.3. Full finder + loser + match + reunion + tip flows. Push notifications (PushManager + APNs). StripePaymentSheet v25.7.1 SPM added, test key `pk_test_51T7nErBOu...` wired. Supabase `device_tokens` migration done.
>
> **Visual polish complete on all screens built so far.** `LOFOPressStyle` everywhere, staggered entrance animations on every screen, card shadows, MatchView animated confidence bar, WaitingView radar pulse, LoserWaitView orb, ConfirmedView celebratory badge, ReunionView connection graphic with pulse. iOS 18 zoom transition: WaitingView radar → MatchView.
>
> **UI Polish Pass 2 (Phase 26e–f) — complete:**
> - **HomeView rebuilt**: small left-aligned LOFO wordmark, 4-line hero heading ("Lost / something? / Found / something?" with tight line spacing), rust rule, italic serif subtitle, large left-aligned buttons with subtitles ("Snap a photo, done" / "Describe it, we'll look") + right arrows.
> - **HomeView heading typography (final)**: "Lost something?" = `serifDisplay(50)` navy. "Found something?" = `serifDisplayItalic(50)` rust. All 4 lines use `.padding(.top, -20)` for tight stacking.
> - **Italic font fix**: `DMSerifDisplay-Italic.ttf` file has internal PostScript name `DMSerifText-Italic`. Registration uses filename `"DMSerifDisplay-Italic"` (to find the file); `serifDisplayItalic()` uses PostScript name `"DMSerifText-Italic"` (for rendering). Both must stay in sync.
> - **LOFOButton redesigned app-wide**: left-aligned text, arrow right, `radiusL` corners, `padding(.vertical, 20)` — affects every CTA in the app. Ghost style is now a simple underlined text link.
> - **All screen heading fonts** bumped to match web prototype sizes (FinderDone 38, LostPrompt 38, Waiting 34, LoserWait 40, Match banner 38, OwnershipVerify 34, Confirmed 38, AllSet 40, Reunion 38).
> - **Home subtitle** changed from `sans(15)` to `serifDisplay(17)` to match proto.
> - **FinderCameraView bug fixes**: bottom bar Color-in-ZStack bug fixed (buttons now truly pinned to bottom). Corner brackets now use percentage-based centered viewfinder box (12–88% h, 14–70% v) instead of device-corner insets.
> - **Namespace warning fixed**: `MatchZoomNSKey.defaultValue` changed to `Namespace.ID?` / `nil` — no more "Reading a Namespace property outside View.body" warning.
> - **LocationManager**: real reverse geocoding (city, state, zip via CLGeocoder). Fixed `@MainActor` concurrency bug (geocoder was called from `nonisolated` context). Camera screen now uses `startWatching()`/`stopWatching()` (continuous updates) instead of one-shot `requestLocation()`. Location pill shows actual place name and updates live.
>
> **FinderCameraView** is a full native camera viewfinder (AVFoundation): live preview, centered viewfinder bracket overlay, "Point at what you found." center copy, shutter button, library picker, location pill (shows real city/state/zip on device). Falls back to dark gradient on simulator (no real camera). White simulator background is expected — real camera feed shows on device.
>
> **Backend bug fixed:** `asyncio.to_thread()` wraps Claude Vision + Voyage embedding calls in `/items/from-photo` so the sync SDK no longer blocks uvicorn's event loop (was causing 502s). Deployed to Railway.
>
> Full iOS plan: `~/.cursor/plans/swiftui_native_app_transition_e4202362.plan.md`
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector + Supabase Storage, Stripe, Twilio. Railway.
>
> **DB schema:** `items`, `tips`, `reunions`, `device_tokens` (migration done). `used_tokens`, `secret_verifications` (legacy).
>
> **SMS:** Code-complete, pending Twilio A2P carrier approval (Campaign SID `CM50255157...`, ~2–3 weeks from Mar 12).
>
> **iOS app — 36 Swift files:**
> - `Theme.swift` — colors, DM Sans + DM Serif Display + DM Serif Display Italic, `LOFOPressStyle`, `lofoCardShadow()`, `serifDisplay()`, `serifDisplayItalic()`, `matchZoomNS` EnvironmentKey (Namespace.ID? optional, iOS 18 zoom transition), **`requiredFieldHighlight(_ triggerCount: Binding<Int>, cornerRadius:)`** — pulsing rust border ViewModifier (3 pulses × 0.65s, settles to 0.55 opacity, Int counter trigger, generation-tracked, snaps to 0 before each replay so full-range pulse every time)
> - `LOFOApp.swift` — `@main`, NavigationStack, `@Namespace matchZoomNS`, AppDelegate adaptor, PushManager, deep link, Stripe key; routes `.loserVerify` → `LoserOTPView`
> - `AppDelegate.swift` — APNs token callbacks → PushManager
> - `Models/Item.swift`, `Models/Match.swift` — all structs are `Sendable` (required for Stripe SDK strict concurrency)
> - `Services/` — APIClient (uploadSession 90s for photos), LocationManager (CLGeocoder reverse geocoding, startWatching/stopWatching), HapticManager, PushManager, **CameraManager** (AVFoundation, NSObject, not @Observable)
> - `ViewModels/` — AppState (Screen enum: finder + loser cases incl. `.loserVerify`), FinderFlowState, LoserFlowState (`pendingPhone` + `whereDescription` fields), MenuViewModel
> - `Views/Home/` — HomeView (proto-matching hero heading + left-aligned buttons with subtitles), MenuSheet
> - `Views/Finder/` — **FinderCameraView** (full native camera viewfinder, centered bracket overlay, live location pill), **CameraPreviewView** (UIViewRepresentable), FinderDoneView, PhoneVerifyView, OTPVerifyView, AllSetView
> - `Views/Loser/` — LostPromptView, WaitingView (radar pulse + matchedTransitionSource; phone section sends OTP → pushes `.loserVerify`), **LoserOTPView** (loser-specific OTP verify; on success shows LoserWaitView), LoserWaitView (breathing orb, "Hang tight. / Think positive.", "Back to home" → popToRoot), MatchView (animated bar + zoom transition), OwnershipVerifyView, ConfirmedView
> - `Views/Shared/` — ItemCardView (card shadow), TagChipView, **LOFOButton** (left-aligned + arrow right, radiusL, ghost = underline link), ReunionView (connection graphic), TipView, PhotoLightboxView
> - `Fonts/` — DMSans-Regular/Medium/Bold.ttf, DMSerifDisplay-Regular.ttf, **DMSerifDisplay-Italic.ttf**
>
> **Key arch notes:**
> - `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` — all types implicitly @MainActor. Model structs have `Sendable`. APIClient methods do NOT have `nonisolated`. Do NOT change this pattern.
> - `CameraManager` is an exception: it's an `NSObject` (not `@Observable`) with a dedicated `DispatchQueue` for AVFoundation session ops. Callbacks dispatch back to main thread. This pattern intentionally deviates from the rest of the app to handle AVFoundation's threading requirements.
> - `LocationManager` geocoding: `reverseGeocode(location:)` is a regular (non-nonisolated) `@MainActor` method called from inside `Task { @MainActor in }` in the delegate callback. CLGeocoder callbacks fire on main thread so `locationName` is set directly.
> - **`parseISO()` in WaitingView**: PostgreSQL `::text` timestamps arrive as `2026-03-16 19:58:14.07162+00` (space separator, 5 fractional digits, `+HH` tz). Normalization truncates to 3 fractional digits; `DateFormatter` with `x` pattern (accepts `±HH`) handles the rest. Do NOT revert to ISO8601DateFormatter-only — it will fail.
> - **`Text +` concatenation deprecated in iOS 26**: use `Text("... \(Text(x).modifier())")` string interpolation instead. Already applied in WaitingView, OTPVerifyView, PhoneVerifyView.
> - **`requiredFieldHighlight` API**: trigger is `@Binding<Int>` (not Bool). `triggerCount += 1` on button tap — always a new value so `onChange` fires unconditionally on every tap. `triggerCount = 0` clears the border (set in `.onChange(of: fieldValue)`). Inside the modifier: `withAnimation(nil) { pulseOpacity = 0 }` + `DispatchQueue.main.async` snaps to 0 before each replay so the pulse always runs full-range `0 → 1.0`, not `0.55 → 1.0` (which looked weak). Generation counter cancels stale settle-to-0.55 callbacks on re-trigger.
>
> **Next priorities — waiting on Apple Developer enrollment:**
> 1. developer.apple.com → App ID `ai.lofo.app` (Push + Apple Pay caps) + APNs key (.p8) + Merchant ID `merchant.ai.lofo`
> 2. Railway env vars: `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_AUTH_KEY`, `APNS_BUNDLE_ID=ai.lofo.app`, `APNS_ENVIRONMENT=production`
> 3. Xcode → Signing & Capabilities → Apple Pay → add `merchant.ai.lofo`
> 4. Product → Archive → Distribute → TestFlight upload
> 5. App Store Connect — listing (name: LOFO, subtitle: Lost & found, reunited by AI), screenshots (6.7" 1290×2796), privacy URL, submit for review
> Full step-by-step in 'iOS Phase G Checklist' section.
>
> **UI Polish Pass 5 (Phase 26i) — complete:**
> - **LostPromptView**: Two-tone heading "What did" navy + "you lose?" rust italic. Rust rule + subtitle. `ScrollView` SwiftUI 6 fix.
> - **AllSetView**: Rust rule below "All set." heading. `ScrollView` fix.
> - **TipView**: Full rewrite — left-aligned top-anchored layout, 3-stage entrance animation, rust rule, `LOFOPressStyle` on amount buttons with selection shadow.
> - **OwnershipVerifyView**: Full rewrite — removed double-Spacer centering, two-tone heading "Verify it's" navy + "yours." rust italic, rust rule, `lofoCardShadow()` on TextEditor, 3-stage entrance animation.
> - **ConfirmedView**: Country code `Menu` + ISO badge + auto-formatter on phone field (same pattern as PhoneVerifyView/WaitingView). Pre-populates from `LoserFlowState.shared.loserPhone`.
> - **PhotoLightboxView**: Entrance fade + scale-in animation on appear (spring).
> - **LoserWaitView**: Orb shrunk 30% (154/109/70/45/6px), rings breathe together (0/0.18/0.35s stagger), core glow white 0.07→clear (no blob), layout raised to upper third. "Think positive." → `serifDisplayItalic` white 65%. White rule separator added. "Got it" pill → "Back To Home" plain text link → `popToRoot()`. Text entrance changed to spring.
>
> **Loser OTP flow (Phase 26i) — complete:**
> - Loser phone flow now requires SMS verification before saving phone to item.
> - `AppState.Screen`: added `.loserVerify`.
> - `LoserFlowState`: added `pendingPhone: String?` (set when "Send Code" tapped, cleared on reset).
> - `WaitingView`: "Notify me" → "Send Code →"; `savePhone()` replaced by `sendCode()` which calls `sendOTP()`, stores `pendingPhone`, pushes `.loserVerify`. `showLoserWait` state and `fullScreenCover` removed from WaitingView.
> - **New `LoserOTPView`** (`Views/Loser/`): "Check your / phone." two-tone heading, 6 digit boxes (auto-advance, auto-submit on 6th), resend link. On verify success: saves phone to item + registers APNs push token + presents `LoserWaitView` as `fullScreenCover`.
> - `LOFOApp`: `.loserVerify` → `LoserOTPView()` wired in navigationDestination.
>
> **Phase 26j — Required field validation highlight system — complete:**
> - **`LOFORequiredFieldHighlight` ViewModifier** added to `Theme.swift`. Usage: `.requiredFieldHighlight($triggerCount, cornerRadius:)` where `triggerCount` is `@State var highlightXxx = 0`. Pulses 3× (5 half-cycles × 0.65s easeInOut = 3.25s), then settles to steady `0.55` opacity rust border. Trigger is `Int` — every `+= 1` is always a new value so `onChange` fires unconditionally. Before each pulse: `withAnimation(nil) { pulseOpacity = 0 }` + `DispatchQueue.main.async` ensures full-range `0→1.0` pulse on every tap (not weak `0.55→1.0`). Generation-tracked — stale settle callbacks cancelled on re-trigger. Clears when caller sets `= 0`.
> - **LostPromptView**: `.disabled()` removed from "Start Looking" button. `submit()` does `highlightDescription += 1` + haptic on empty. `.onChange(of: description)` does `highlightDescription = 0` on typing.
> - **OwnershipVerifyView**: Same — `.disabled()` removed, `verify()` does `highlightClaim += 1`.
> - **PhoneVerifyView**, **ConfirmedView**, **WaitingView** phone section: `highlightPhone += 1` / `highlightLoserPhone += 1` + haptic on invalid phone; `.onChange` clears to `0`. WaitingView `sendCode()` was previously a completely silent `guard...else { return }` — now provides feedback.
> - **LostPromptView "Where" field**: `location.fill` rust icon before label. "This is optional — you can simply describe where you lost it in the field above and we'll take care of the rest." helper text added below label.
>
> **Phase 26k — UI Polish Pass 6: full app consistency pass — complete:**
> - **MenuSheet rebuilt**: `NavigationStack` removed. Custom X dismiss button (white circle, muted, 38×38, `lofoCardShadow()` — matches gear icon on HomeView). Staggered fade+lift entrance (header 0ms, usage 100ms, support 200ms, info 300ms). `LOFOPressStyle` on all row buttons. `HStack(alignment: .firstTextBaseline)` on stats row — aligns number baselines regardless of 1-line vs 2-line labels below.
> - **WaitingView consistency fixes**: Rust rule corrected (solid rust → `rust.opacity(0.35)`, `32×2` → `40×1.5` — was the only offender in the entire app). Heading line spacing corrected (`VStack(spacing: 2)` → `spacing: 0` + `.padding(.bottom, -10)` on line 1). Phone section copy bumped to `sans(14) navy.opacity(0.7)`. Button relabeled "Confirm Phone Number".
> - **WaitingView radar animation** rebuilt to match HTML prototype exactly: 3 stroke rings all 130px, `scale(0.4) opacity(0.14)` → `scale(2.1) opacity(0)`, 2.6s easeOut, delays 0/0.87/1.73s. Center circle 68px + expanding glow pulse (navy circle grows 68→92 and fades, simulates CSS `box-shadow` pulse). Frame height 130px.
> - **MatchView**: `ScrollView(.vertical, showsIndicators: false)` iOS 26 fix. "That's Mine" title case.
> - **OwnershipVerifyView**: Error messages now use `rust` color + `exclamationmark.circle` icon — no more raw `.red` Text.
> - **ConfirmedView**: Heading rebuilt — left-aligned, badge above, "It's yours." navy `serifDisplay(38)` + "Confirmed." rust `serifDisplayItalic(38)` tight-stacked, rust rule, muted subtitle. Outer `VStack(alignment: .leading)`. "Connect Us Both" title case. Same styled error treatment.
> - **TipView**: Styled error message. Button titles title-cased.
> - **ReunionView full layout pass**: `ScrollView` top-anchored left-aligned. Connection graphic spring-animates first. "You're all" navy `serifDisplay(38)` + "set." rust `serifDisplayItalic(38)`, rust rule, two muted subtitle lines. Done button fades last. `.navigationBarBackButtonHidden(true)`.
> - **All CTA buttons — title case applied app-wide**: "That's Mine", "Not My Item", "Verify Ownership", "Connect Us Both", "I'll Reach Out — Just Notify the Finder", "Confirm Phone Number", "Send Code", "Update Description", "Save Payout Info", "Select An Amount", "Skip — No Tip This Time", "Resend Code", "Back To Home".
> - **Backend bug fix — `GET /stats/by-items` UUID case mismatch**: Swift `UUID.uuidString` is uppercase; PostgreSQL `uuid::text` is lowercase. Added `.lower()` to incoming ID strings before DB comparison. Deployed to Railway (commit `854ff40`). Stats in MenuSheet now show correctly after submitting items through iOS app.
>
> **All screens now fully polished.** No remaining polish candidates.
>
> Start by reading `LOFO_AI_Progress.md`, then **describe your plan and wait for approval before making any changes**."

---

## Session History

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
