# LOFO.AI — Claude Code Instructions

## What This Project Is
A lost and found app built with AI. A finder snaps a photo of something found. A loser describes what they lost. AI matches them, verifies ownership, coordinates the return, and prompts a tip. Built almost entirely by vibe coding — no manual coding by the developer.

---

## End of Every Session
**Always update `LOFO_AI_Progress.md` at the end of every session.** Add a new entry at the top of the Session History section with:
- Date
- What was built or changed
- Any new endpoints, files, or DB columns added
- Current status and what's next

---

## Developer Style
- I am not a developer. I vibe code — describe what I want, you build it.
- Never ask me to write code manually or edit files myself.
- Keep explanations simple. No jargon unless necessary.
- When something is done, tell me clearly: what changed, what to do next.

---

## Output Format Rules
This project has three distinct frontends — use the right approach for each:
- **Web app + school app** (`LOFO_MVP.html`, `school.html`, `admin.html`, etc.): Plain HTML only. Never use React, Vue, or any JS framework.
- **iOS app** (`~/Desktop/LOFO/`): SwiftUI only. All files are `.swift`. Target iOS 17+, use `@Observable`.
- **Backend:** Python + FastAPI only (`main.py`).
- **Styling (web):** DM Sans (body) + DM Serif Display (headings). Cream/warm color palette.
- Never restructure or rename existing files without asking first.

---

## Project Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) — `main.py` |
| Database | Supabase (PostgreSQL + pgvector) |
| Hosting | Railway (auto-deploys on git push to `main`) |
| Frontend | GitHub Pages → `https://md-gityup.github.io/lofo-ai/LOFO_MVP.html` |
| Admin | `https://lofoapp.com/admin` (proxied via Vercel → Railway) |
| AI | Claude Vision + Voyage AI embeddings + Cohere Rerank |
| SMS | Twilio Verify (OTP) + Twilio Messaging (notifications + relay) |
| Payments | Stripe (inline card + Apple Pay) |
| iOS | SwiftUI, iOS 17+, `~/Desktop/LOFO/LOFO.xcodeproj` |

---

## Key Files

| File | Purpose |
|---|---|
| `main.py` | All FastAPI endpoints + CORS + serves HTML |
| `database.py` | Supabase connection pool |
| `security.py` | Argon2id hashing + JWT handoff tokens |
| `LOFO_MVP.html` | 16-screen web app |
| `admin.html` | Admin dashboard (login, stat cards, tables, map, charts) |
| `map.html` | Full-screen Leaflet live map |
| `resolve.html` | Post-reunion tip + item closure page (linked from handoff SMS) |
| `school.html` | School admin portal (URL token secured) |
| `.env` | API keys — never commit, never share |
| `LOFO_AI_Progress.md` | Full build history + roadmap — source of truth |

---

## Deployment
- **Push to `main` branch** → Railway auto-deploys in ~1 min
- No manual deploy steps needed
- Local dev: `cd ~/Desktop/lofo-ai && source .venv/bin/activate && uvicorn main:app --reload`
- Live API: `https://lofo-ai-production.up.railway.app`

---

## Database Tables
- **`items`** — all lost/found items (finder + loser), embeddings, GPS, phone, photo_url, status
- **`reunions`** — matched pairs, both phones, relay status
- **`tips`** — Stripe payment records
- **`used_tokens`** — JWT replay prevention

Key columns to know: `type` ('finder'|'loser'), `status` ('active'|'inactive'), `embedding` (vector 1024), `expires_at` (30 days, auto-extended at day 28), `secret_detail` (ownership verify), `phone` (E.164 format)

---

## Matching Engine (as of March 19, 2026)
5-stage pipeline:
1. Categorical gate on `item_type` (hard block if mismatch)
2. Cosine similarity on attribute-only embeddings (LIMIT 50)
3. Haversine proximity filter (10-mile radius)
4. Cohere Rerank stage
5. Composite score: `0.55·reranker + 0.20·cosine + 0.15·color + 0.10·features`

Requires `COHERE_API_KEY` in Railway env vars.

---

## Active Status (as of April 21, 2026)
- All 26 phases complete and deployed ✅
- iOS app — build 1.0.0 (15) ready for TestFlight
- Twilio A2P 10DLC campaign `CM50255157d8c0965b92369a1f90b3ab2b` approved ✅
- Full reunion flow validated end-to-end on web app AND on iOS TestFlight build 10 ✅
- **Reject flow validated end-to-end** ✅ — universal link → app → verify claim → reject → SMS to loser
- **Resolve flow validated end-to-end** ✅ — universal link → app → confirm → tip → Stripe PaymentSheet → close
- **Real Stripe charge validated end-to-end** ✅ — $5 test charge succeeded, visible in Stripe Dashboard
- Stripe iOS SDK (`StripePaymentSheet` via `stripe-ios-spm` v24.25.0) linked as SPM dependency. Uses `merchant.ai.lofo` for Apple Pay.
- Universal Links working on device — Build 15 includes Stripe SDK + `CODE_SIGN_ENTITLEMENTS` + Associated Domains.
- App-link fallback page (`app-link.html`) — browser requests to app-only links (e.g. reject) get a branded "open in app" page instead of raw JSON.

---

## What's Pending / Known Issues
- High-value / ownership verification path not yet tested end-to-end (web or iOS)
- Switch Stripe keys from test (`pk_test_*`) to live before App Store submission
- Configure `STRIPE_WEBHOOK_SECRET` in Railway for production webhook signature verification
- Re-embed all items after any matching engine changes (use "Re-embed All →" in admin Debug tab)
- Web app link (`_APP_URL`) removed from match notification SMS — push notifications handle iOS users; Stripe Connect redirects still use `_APP_URL` (lower priority)

---

## Environment Variables (all set in Railway)
`DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `COHERE_API_KEY`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `TWILIO_VERIFY_SID`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_URL`, `ADMIN_USERS`, `CRON_SECRET`
