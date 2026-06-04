#!/bin/bash
# Poke Labs Self-Recovery Script
# Run this to restart all services after a reboot or death
# Usage: bash /home/alx/start.sh

set -e

echo "🐾 Poke Labs Recovery Starting..."
echo "================================"

# Kill any existing processes on our ports
for port in 8765 8766 8770 8780 8790; do
    fuser -k ${port}/tcp 2>/dev/null || true
done
sleep 1

# Start Link Preview API (standalone) on 8765
echo "→ Starting Link Preview API v4 on :8765"
nohup python3 /home/alx/services/link-preview/server.py > /tmp/lp.log 2>&1 &
sleep 1
curl -s http://localhost:8765/api/health > /dev/null && echo "  ✅ Link Preview API OK" || echo "  ❌ Link Preview API FAILED"

# Start Poke Labs Site + Link Preview API on 8766
echo "→ Starting Poke Labs Site + API v7 on :8766"
nohup python3 /home/alx/services/pokelabs-site/server.py > /tmp/site.log 2>&1 &
sleep 1
curl -s http://localhost:8766/api/health > /dev/null && echo "  ✅ Site + API OK" || echo "  ❌ Site + API FAILED"

# Start Poke Bot on 8770
echo "→ Starting Poke Bot v3 on :8770"
nohup python3 /home/alx/services/poke-bot/bot.py > /tmp/bot.log 2>&1 &
sleep 1
curl -s http://localhost:8770/ > /dev/null && echo "  ✅ Poke Bot OK" || echo "  ❌ Poke Bot FAILED"

# Start Skills Hub API on 8780
echo "→ Starting Skills Hub v1 on :8780"
nohup python3 /home/alx/services/skills-hub/server.py > /tmp/skills.log 2>&1 &
sleep 1
curl -s http://localhost:8780/api/health > /dev/null && echo "  ✅ Skills Hub OK" || echo "  ❌ Skills Hub FAILED"

# Start Pricing API on 8790
echo "→ Starting Pricing API v1 on :8790"
nohup python3 /home/alx/services/pricing-api/server.py > /tmp/pricing.log 2>&1 &
sleep 1
curl -s http://localhost:8790/api/health > /dev/null && echo "  ✅ Pricing API OK" || echo "  ❌ Pricing API FAILED"

echo ""
echo "================================"
echo "🐾 Poke Labs Recovery Complete"
echo ""
echo "Services:"
echo "  :8765  Link Preview API"
echo "  :8766  Poke Labs Site + API"
echo "  :8770  Poke Bot"
echo "  :8780  Skills Hub"
echo "  :8790  Pricing API"
echo ""
echo "Dashboard: http://localhost:8766/dashboard"
echo "Health:    curl http://localhost:8766/api/health"
echo "Preview:   curl -X POST http://localhost:8766/api/preview -H 'Content-Type: application/json' -d '{\"url\":\"https://github.com\"}'"
