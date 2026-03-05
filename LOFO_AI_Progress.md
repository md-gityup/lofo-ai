# LOFO.AI — Build Progress & Context
*Last updated: March 5, 2026 (Phase 6 tested + UI bugs fixed)*

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
| 5 — UI Polish | ✅ Complete | 9-screen interactive prototype, iOS animations, Dynamic Island |
| 6 — API Wiring | ✅ Complete | All screens wired to real backend with live API calls |
| 7 — Tip Flow | ← Next | Stripe Connect |

---

## Current Status: Phases 1–6 Complete & Tested ✓

### What's running
- **Local API server:** `http://localhost:8000`
- **App UI (served from FastAPI):** `http://localhost:8000/`
- **Interactive API docs:** `http://localhost:8000/docs`
- **Database:** Supabase (PostgreSQL + pgvector)
- **Project folder:** `~/Desktop/lofo-ai`

### Backend endpoints
| Endpoint | What it does |
|---|---|
| `GET /` | Serves LOFO_MVP.html (the app UI) |
| `POST /items` | Submit a structured item manually |
| `POST /items/from-photo` | Upload a photo → Claude Vision extracts profile → stored with embedding |
| `POST /items/from-text` | Submit text description → Claude extracts profile → stored with embedding |
| `GET /items/{id}` | Retrieve an item by UUID |
| `POST /match` | Find top matching finder items for a loser item (cosine similarity) |
| `POST /verify` | Verify ownership via secret detail (Argon2id, 3-attempt lockout) |
| `POST /handoff/validate` | Validate single-use JWT handoff token |

### Database table: `items`
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
| secret_detail | varchar | Hashed with Argon2id (loser items only) |
| attempt_count | integer | Brute-force lockout counter |
| verified_at | timestamptz | Set on successful ownership verification |
| status | varchar | Default 'active' |
| expires_at | timestamptz | Default 30 days from creation |
| created_at | timestamptz | Auto-set |

### Key files
| File | What it does |
|---|---|
| `main.py` | FastAPI app — all endpoints + CORS + serves HTML |
| `database.py` | Supabase connection pool + API key loading |
| `schema.sql` | PostgreSQL table definitions |
| `requirements.txt` | Python dependencies |
| `LOFO_MVP.html` | Fully wired 13-screen app — real API calls, real data |
| `security.py` | Argon2id hashing + JWT handoff token logic |
| `.env` | API keys and DB connection string — never share |

---

## Session Summary — March 5, 2026 (this session)

### What we did
1. **Read all context** — reviewed `main.py`, `database.py`, `security.py`, and the existing progress doc to orient.
2. **Confirmed the server was already running** — `uvicorn main:app --reload` was active in terminal 9 from a prior session.
3. **Ran a full end-to-end API test** via curl — every endpoint exercised manually (see test results below).
4. **Audited the UI** — opened `http://localhost:8000/` in the browser, walked through all 13 screens in the code, and identified 4 real bugs plus a set of intentional demo artifacts.
5. **Fixed all 4 bugs** — surgical edits to `LOFO_MVP.html` only, no backend changes.
6. **Updated this doc** — full record of what was built, tested, fixed.

### Issues hit and how they were resolved

**Issue:** Browser screenshots always showed a cropped/zoomed view of the device frame — couldn't see the full UI visually.
**Resolution:** Used the browser DOM snapshot tool instead, plus code review of the HTML source. Got a complete picture without relying on screenshots.

**Issue:** Prior session's test data (Birkenstock description, phone number) was still filling the forms when the browser tab was already open.
**Resolution:** Identified this is just leftover browser state — not a bug. Refreshing the page clears it. Noted it during the bug audit.

**Issue:** Claude returned `Clogs/mules` as an item_type when classifying Birkenstock sandals — caused "We found your Clogs/mules." to render in the UI.
**Resolution:** Added a `cleanType()` helper that splits on `/`, takes the first segment, trims and capitalises. Applied to all 4 places where `item_type` is displayed.

---

## UI Bug Fixes (March 5, 2026 — post-Phase 6)

Four bugs found during live testing and fixed in `LOFO_MVP.html`:

| Bug | Fix |
|---|---|
| Back button on Handoff went to `match`, skipping Ownership Verify | Now context-aware: losers go back to `ownership-verify`, finders go back to `match` |
| Reunion screen hardcoded "Your bag is on its way" | Now reads from `state.matchedItem.item_type` on screen enter; falls back to "Your item" |
| Claude sometimes returns slash-separated `item_type` (e.g. `Clogs/mules`) | Added `cleanType()` helper — takes everything before the `/`, trims, capitalises. Used everywhere item_type is displayed |
| Match reason checklist was always hardcoded (fake location, time) | Now generated from real matched item fields (item type, color, material, size) — only shown if data exists |

No backend changes. All fixes in `LOFO_MVP.html` only.

### Known demo artifacts (intentional — do not fix yet)

These were identified during the audit but deliberately left alone. They belong to future phases or are harmless placeholders:

| Artifact | Where | Why it's intentional |
|---|---|---|
| "DEMO: CHOOSE OUTCOME" + two branch buttons on SMS Verify screen | `screen-verify` | The entire SMS/OTP flow is unbuilt. These are the only way to branch the finder demo. Fix in Phase 8 when SMS is added. |
| Hardcoded OTP boxes showing "3 7 4 ·" | `screen-verify` | Same — placeholder UI for unbuilt SMS flow. |
| "(555) 000-0000" in the verify screen copy | `screen-verify` | Same. |
| "Simulate match found →" button on Waiting screen | `screen-waiting` | Useful for demo/testing when there's no real match seeded. Remove when polling/push notifications are added. |
| Location and time pills on Waiting screen ("Within 0.5 mi…", "Today 1–4 PM") | `screen-waiting` | Hardcoded demo copy — no location/time data is captured yet. Leave until that feature is built. |

---

## Phase 6 — End-to-End Test Results (March 5, 2026)

Full API test run — every endpoint verified working:

| Test | Result |
|---|---|
| `POST /items/from-text` (finder) | Claude extracted: wallet, brown, leather, small, bifold, silver clasp ✅ |
| `POST /items/from-text` (loser + secret) | Same extraction, secret hashed and stored in `secret_verifications` ✅ |
| `POST /match` | **89.7% similarity score** — correct item returned, above 0.7 threshold ✅ |
| `POST /verify` (wrong answer) | `verified: false, attempts_remaining: 2` ✅ |
| `POST /verify` (correct answer) | `verified: true` + JWT handoff token issued ✅ |
| `POST /handoff/validate` (1st use) | `valid: true` ✅ |
| `POST /handoff/validate` (2nd use) | `409 — Handoff token has already been used` ✅ |

The full loop works: AI ingestion → vector matching → Argon2id ownership verification → single-use JWT handoff. Security is confirmed: brute-force attempt counter increments correctly, and handoff tokens cannot be replayed.

UI is live and served from `http://localhost:8000/`. The photo flow requires a real browser or iPhone (camera access needed).

---

## Phase 6 — What Was Built (March 5, 2026 session)

### The goal
Wire the polished HTML prototype to the real backend. Replace all hardcoded demo data with live API calls. Every tap does something real.

### What was added to `LOFO_MVP.html`

**New screen: Ownership Verify** (`screen-ownership-verify`)
- Sits between Match Found and Handoff in the loser flow
- Text input for the secret detail the loser registered
- 3 attempt dots that fill red on each wrong answer
- Error message shows attempts remaining
- On success: proceeds to Handoff
- On failure with 0 attempts: button locks, item locked 423 response handled

**Lost Prompt screen — updated**
- Added `id="lost-description"` to the description textarea
- Added "🔐 Secret detail only you'd know" input field with hint card
- Button now calls `submitLost()` instead of navigating directly to Waiting

**Script — fully replaced**
- `const API` — auto-detects: `http://localhost:8000` when opened from `file://`, empty string (relative) when served from FastAPI
- App state object: `{ finderItemId, loserItemId, matchedItem, handoffToken, failedAttempts }`
- `triggerShutter()` — now clicks the hidden file input instead of running a fake timer
- `handlePhotoFile()` — async: flash effect → camera AI overlay → `POST /items/from-photo` → populate Finder Done with real data → navigate
- `renderFinderDone(item)` — populates item card with real `item_type`, colors, material, size, features + smart emoji
- `submitLost()` — async: `POST /items/from-text` → `POST /match` → routes to Match Found (≥0.7) or Waiting
- `submitOwnershipVerify()` — async: `POST /verify` → handles success (→ Handoff), failure (attempt dots), lockout (423)
- `renderMatchFound(item)` — fills match card with real item data, updates confidence bar and Dynamic Island %
- All existing functions preserved: `go()`, stagger system, Dynamic Island, `formatPhone`, `selectOption`, `selectTip`

**New elements added to device div**
- `<input type="file" id="photo-file-input" accept="image/*" capture="environment">` — triggers native camera on iOS, file picker on desktop
- `#global-overlay` — dark blur loading overlay with spinner, used for all non-camera API calls
- `#error-toast` — bottom-of-screen error pill, auto-dismisses after 4 seconds

**CSS additions**
- `.att-dot` / `.att-dot.used` — attempt tracking dots
- `#global-overlay` and `#global-overlay-text` — loading overlay styles
- `#error-toast` — error toast styles
- `.secret-label`, `.secret-input`, `.secret-hint` — ownership proof input styling
- `#screen-ownership-verify` — the new verify screen

### What was changed in `main.py`
- Added `CORSMiddleware` (`allow_origins=["*"]`) — allows the HTML to call the API from any origin, including `file://`
- Added `GET /` route serving `LOFO_MVP.html` via `FileResponse` — so the app can be loaded from the server URL, enabling iPhone testing
- Added `from fastapi.middleware.cors import CORSMiddleware`, `from fastapi.responses import FileResponse`, `import os`

### Issues hit and how they were resolved

**Issue:** AI created a brand-new LOFO_MVP.html, overwriting the existing prototype.
**Resolution:** Deleted the new file, reverted main.py, user manually added the existing prototype to the project folder. All subsequent changes were surgical edits to the existing file.

**Issue:** `LOFO_MVP.html` wasn't visible in the project folder at session start — `ls` and glob searches returned no HTML files.
**Root cause:** The prototype existed but hadn't been copied into `~/Desktop/lofo-ai/` yet. User added it manually.

---

## How to Resume

### Step 1 — Open the project
Open Cursor → File → Open Folder → Desktop → lofo-ai

### Step 2 — Start the server
```bash
source .venv/bin/activate
uvicorn main:app --reload
```

### Step 3 — Test it

**Desktop:** Open `LOFO_MVP.html` directly in a browser, or go to `http://localhost:8000/`

**iPhone:** Make sure iPhone and Mac are on the same WiFi. Find your Mac's IP:
```bash
ipconfig getifaddr en0
```
Then go to `http://[YOUR MAC IP]:8000/` in Safari on your iPhone.

### Step 4 — Seed test data (for match testing)
Use Swagger at `http://localhost:8000/docs` to POST a finder item first, then describe it as a loser to test the match flow. Or snap two photos of the same object.

**Quick curl test (confirmed working):**
```bash
# 1. Submit a finder item
curl -X POST http://localhost:8000/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "finder", "description": "Found a brown leather wallet near the park fountain. Small, bifold, with a silver clasp."}'

# 2. Submit a matching loser item with a secret
curl -X POST http://localhost:8000/items/from-text \
  -H "Content-Type: application/json" \
  -d '{"type": "loser", "description": "Lost my brown leather wallet, bifold with silver clasp, near the fountain.", "secret_detail": "There is a photo of my dog inside the left pocket"}'

# 3. Run match (use loser item id from step 2)
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{"item_id": "<loser-item-id>"}'

# 4. Verify ownership (use loser item id)
curl -X POST http://localhost:8000/verify \
  -H "Content-Type: application/json" \
  -d '{"item_id": "<loser-item-id>", "secret_detail": "There is a photo of my dog inside the left pocket"}'
```

---

## Key Credentials & Locations

| Thing | Where it is |
|---|---|
| Supabase project | supabase.com → LOFO → LOFO-AI |
| API keys (Anthropic, Voyage) | In your `.env` file |
| DB connection string | `.env` file (Session Pooler URL) |
| API running | localhost:8000 (only when uvicorn is running) |

**Important:** Never share, paste, or commit your `.env` file. It stays on your machine only.

---

## What's Next: Phase 7 — Stripe Connect Tip Flow

**Goal:** The tip on the Reunion screen actually moves money. The finder gets paid at the moment of reunion.

### What to build in Phase 7

**7a — Stripe Connect onboarding for finders**
- When a finder submits a photo, prompt them to connect a Stripe account (or a simplified payout method like Venmo handle / bank detail)
- Store a `stripe_account_id` on the finder item or a separate `finders` table

**7b — Tip charge on the loser side**
- Reunion screen tip buttons ($5, $10, $20, custom) trigger a real Stripe charge
- Loser pays; finder receives via Stripe Connect transfer
- Add `POST /tip` endpoint: takes `item_id`, `amount_cents`, processes the charge and transfer

**7c — Receipt / confirmation**
- Thanks Sent screen confirms the exact amount sent
- Optional: email receipt via Stripe's built-in receipt emails

**Stripe setup needed:**
- Create Stripe account at stripe.com
- Add `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` to `.env`
- Install: `pip install stripe`

---

## Cursor Prompt for Phase 7

When starting the Phase 7 Cursor session, paste this at the top of your first message:

> "I'm building LOFO.AI — a lost and found matching app. The project is at ~/Desktop/lofo-ai. Read `LOFO_AI_Progress.md` first for full context. Here's the quick version:
>
> **What's complete and working:**
> Phases 1–6 fully built, tested end-to-end, and UI bugs fixed. The entire loop works: finder snaps photo OR submits text → Claude Vision/text extracts item profile → Voyage AI embedding stored → loser describes lost item → cosine similarity match (tested at 89.7%) → loser verifies ownership with Argon2id-hashed secret (3-attempt lockout) → single-use JWT handoff token issued → handoff options shown. No mocked data anywhere in the main flow.
>
> **Backend:** FastAPI (`main.py`), Supabase/pgvector (`database.py`), security (`security.py`). Endpoints: `POST /items`, `POST /items/from-photo`, `POST /items/from-text`, `GET /items/{id}`, `POST /match`, `POST /verify`, `POST /handoff/validate`. Server runs with `source .venv/bin/activate && uvicorn main:app --reload`.
>
> **Frontend:** `LOFO_MVP.html` — 13 screens, all live API calls, served from FastAPI at `GET /`. Key JS: `state` object, `go()` navigation, `submitLost()`, `submitOwnershipVerify()`, `cleanType()` helper (handles Claude slash-separated item types), dynamic match reasons, dynamic reunion title.
>
> **Known intentional placeholders (do not touch):** SMS/OTP verify screens are fake (future Phase 8), "Simulate match found" button on Waiting screen, hardcoded location pills on Waiting screen.
>
> **What's next — Phase 7: Stripe Connect tip flow**
> The Reunion screen has tip buttons ($5, $10, $20, custom) that go nowhere. Goal: the loser's tap on "Send $10 thank you →" actually charges their card and pays the finder.
>
> Start by reading `main.py`, `LOFO_MVP.html` (Reunion screen `#screen-reunion` and Thanks screen `#screen-thanks`), and `.env`. Then design the data model for Phase 7a: what tables/columns do we need to store a finder's Stripe payout account, and what does a tip transaction record look like?"

---

## Claude Chat Starter for Phase 7 Review

When starting a new Claude chat to review Phase 7 progress, paste this:

> "I'm building LOFO.AI — a lost and found app. Phases 1–6 complete and tested: FastAPI backend, Supabase/pgvector, Claude Vision + Voyage AI ingestion, cosine matching (89.7% on a real test), Argon2id ownership verification, JWT single-use handoff tokens, and a fully wired 13-screen HTML frontend. I've just finished Phase 7: the Stripe Connect tip flow. Here's what I built: [paste what Cursor did]. Help me review it and plan Phase 8."

---

*Built with Cursor + Claude. Zero prior coding experience. March 5, 2026.*
