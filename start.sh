#!/bin/bash
# Poke Labs — Self-Recovery Script
# Run this after any server restart to bring all services back online
# Usage: bash /home/alx/start.sh

set -e

echo "🟢 Poke Labs Self-Recovery"
echo "=========================="

# 1. Start Poke Labs Site + Link Preview API
echo "→ Starting Poke Labs Site on :8766..."
fuser -k 8766/tcp 2>/dev/null || true
sleep 1
if [ -f /home/alx/services/pokelabs-site/server.py ]; then
    nohup python3 /home/alx/services/pokelabs-site/server.py > /tmp/lp.log 2>&1 &
    sleep 2
    if curl -s http://localhost:8766/api/health > /dev/null 2>&1; then
        echo "  ✅ Site + API running"
    else
        echo "  ⚠️  Site may not have started (check /tmp/lp.log)"
    fi
else
    echo "  ❌ server.py not found — need to rebuild"
fi

# 2. Start Poke Bot
echo "→ Starting Poke Bot on :8770..."
fuser -k 8770/tcp 2>/dev/null || true
sleep 1
if [ -f /home/alx/services/poke-bot/bot.py ]; then
    nohup python3 /home/alx/services/poke-bot/bot.py > /tmp/bot.log 2>&1 &
    sleep 2
    if curl -s http://localhost:8770/ > /dev/null 2>&1; then
        echo "  ✅ Bot running"
    else
        echo "  ⚠️  Bot may not have started (check /tmp/bot.log)"
    fi
else
    echo "  ❌ bot.py not found — need to rebuild"
fi

# 3. Verify
echo ""
echo "=========================="
echo "Status check:"
curl -s http://localhost:8766/api/health 2>/dev/null && echo "  API: OK" || echo "  API: DOWN"
curl -s http://localhost:8770/ 2>/dev/null && echo "  Bot: OK" || echo "  Bot: DOWN"
echo "=========================="
echo "✅ Recovery complete"
