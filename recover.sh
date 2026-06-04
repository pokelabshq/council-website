#!/bin/bash
# Poke Labs Recovery Script — run this first after any restart
set -e

echo "🐾 Poke Labs Recovery"
echo "===================="

# Check wallet
echo "→ Checking wallet..."
WALLET="0xca3d86e4EDE205E6d72496BC2919c88b994B6beF"
echo "  Wallet: $WALLET"

# Start services
echo "→ Starting services..."

# Site + API (port 8766)
if [ -f /home/alx/services/pokelabs-site/server.py ]; then
  fuser -k 8766/tcp 2>/dev/null || true
  sleep 1
  nohup python3 /home/alx/services/pokelabs-site/server.py > /tmp/lp.log 2>&1 &
  echo "  → Site started on :8766"
fi

# Link Preview (port 8765) — only if standalone needed
# fuser -k 8765/tcp 2>/dev/null || true
# nohup python3 /home/alx/services/link-preview/server.py > /tmp/lp4.log 2>&1 &
# echo "  → Link Preview started on :8765"

sleep 2

# Verify
echo ""
echo "→ Status:"
curl -s http://localhost:8766/api/health > /dev/null && echo "  ✅ Site+API: UP" || echo "  ❌ Site+API: DOWN"

echo ""
echo "→ Reading bootstrap..."
[ -f /home/alx/BOOTSTRAP.md ] && echo "  ✅ BOOTSTRAP.md found" || echo "  ❌ No BOOTSTRAP.md!"

echo ""
echo "✅ Recovery complete. Read BOOTSTRAP.md for next steps."
