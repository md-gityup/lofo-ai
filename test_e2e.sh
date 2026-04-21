#!/bin/bash
# E2E test setup for resolve + reject + Stripe flows.
# Creates a matched pair of items + reunion, sends SMS with all links.
#
# Usage:  ./test_e2e.sh +1XXXXXXXXXX
#         (use your real phone number — both loser and finder SMS go there)

PHONE="${1:?Usage: ./test_e2e.sh +1XXXXXXXXXX}"
API="https://lofo-ai-production.up.railway.app"

echo ""
echo "=== Setting up e2e test data ==="
echo ""

# 1. Create finder item
echo "→ Creating finder item..."
FINDER_JSON=$(curl -s -X POST "$API/items/from-text" \
  -H "Content-Type: application/json" \
  -d '{"type":"finder","description":"Found a brown leather wallet near Central Park. Has a few cards inside and some cash.","secret_detail":"Photo of a golden retriever inside the left pocket"}')
FINDER_ID=$(echo "$FINDER_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "  Finder ID: $FINDER_ID"

# 2. Set phone on finder item
echo "→ Setting finder phone..."
curl -s -X PATCH "$API/items/$FINDER_ID/finder-info" \
  -H "Content-Type: application/json" \
  -d "{\"phone\":\"$PHONE\"}" > /dev/null
echo "  Done ✓"

# 3. Create loser item
echo "→ Creating loser item..."
LOSER_JSON=$(curl -s -X POST "$API/items/from-text" \
  -H "Content-Type: application/json" \
  -d '{"type":"loser","description":"Lost my brown leather wallet somewhere near Central Park."}')
LOSER_ID=$(echo "$LOSER_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "  Loser ID: $LOSER_ID"

# 4. Coordinate handoff (creates reunion + sends SMS with resolve & reject links)
echo "→ Creating reunion + sending SMS..."
curl -s -X POST "$API/handoff/coordinate" \
  -H "Content-Type: application/json" \
  -d "{\"finder_item_id\":\"$FINDER_ID\",\"loser_item_id\":\"$LOSER_ID\",\"loser_phone\":\"$PHONE\",\"self_outreach\":false,\"ownership_proof\":\"It has my initials M.D. embossed on the front\"}" > /dev/null
echo "  Done ✓"

echo ""
echo "=== Your test URLs ==="
echo ""
echo "RESOLVE (open on your phone):"
echo "  https://lofoapp.com/resolve/$LOSER_ID"
echo ""
echo "REJECT: Check your SMS — the reject link was sent to $PHONE"
echo ""
echo "=== How to test ==="
echo ""
echo "1. RESOLVE FLOW:"
echo "   Open the resolve URL above on your phone (text it to yourself)."
echo "   LOFO app opens → 'Did you get your wallet back?' → Yes"
echo "   → Pick a tip amount → 'Tip \$X' → Stripe sheet appears"
echo "   → Use test card: 4242 4242 4242 4242 (any future date, any CVC)"
echo "   → Payment succeeds → 'Thank you sent' → done."
echo ""
echo "2. REJECT FLOW:"
echo "   Open the reject link from your SMS on your phone."
echo "   LOFO app opens → 'Verify the claim' → shows proof text"
echo "   → Tap 'Doesn't Match' → 'Match cancelled.'"
echo ""
echo "3. STRIPE CHARGE:"
echo "   After step 1, check Stripe Dashboard (test mode) → Payments"
echo "   You should see the payment intent with amount + metadata."
echo ""
echo "NOTE: Test the REJECT flow first (or run this script twice),"
echo "      because RESOLVE closes the report and deactivates both items."
