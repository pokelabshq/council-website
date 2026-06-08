#!/bin/bash
# 🐾 Poke Labs — Deploy All Services
# Run: bash /home/alx/deploy-all.sh
# Or:  curl -sL https://raw.githubusercontent.com/pokelabshq/council/main/deploy-all.sh | bash

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  🐾 Poke Labs — Deploy All Services"
echo "  $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo -e "${NC}"

SERVICES_DIR="/home/alx/services"
LOG_DIR="/tmp/poke-logs"
mkdir -p "$LOG_DIR"

declare -A PORTS=(
  ["link-preview"]="8765"
  ["pokelabs-site"]="8766"
  ["poke-hub"]="8775"
  ["skills-marketplace"]="8781"
)

declare -A DESCRIPTIONS=(
  ["link-preview"]="Link Preview API v4"
  ["pokelabs-site"]="Poke Labs Site v7"
  ["poke-hub"]="Poke Hub v2.0"
  ["skills-marketplace"]="Skills Marketplace v1.0"
)

start_service() {
  local name="$1"
  local port="$2"
  local desc="$3"
  local server=""
  
  # Find server file
  for f in "$SERVICES_DIR/$name/server.py" "$SERVICES_DIR/$name/bot.py" "$SERVICES_DIR/$name/app.py"; do
    if [ -f "$f" ]; then server="$f"; break; fi
  done
  
  if [ -z "$server" ]; then
    echo -e "  ${RED}✗${NC} $name — no server file found"
    return 1
  fi
  
  # Kill existing
  fuser -k "$port/tcp" 2>/dev/null || true
  sleep 0.5
  
  # Start
  nohup python3 "$server" > "$LOG_DIR/$name.log" 2>&1 &
  local pid=$!
  sleep 2
  
  # Verify
  if curl -s --max-time 2 "http://localhost:$port/api/health" > /dev/null 2>&1; then
    local ver=$(curl -s "http://localhost:$port/api/health" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('v','?'))" 2>/dev/null || echo "?")
    echo -e "  ${GREEN}●${NC} $desc (:$port) — PID $pid, v$ver"
    return 0
  else
    echo -e "  ${RED}●${NC} $desc (:$port) — FAILED (check $LOG_DIR/$name.log)"
    return 1
  fi
}

echo "  Starting services..."
echo ""

OK=0
FAIL=0
for name in link-preview pokelabs-site poke-hub skills-marketplace; do
  if start_service "$name" "${PORTS[$name]}" "${DESCRIPTIONS[$name]}"; then
    ((OK++))
  else
    ((FAIL++))
  fi
done

echo ""
echo "  Results: ${GREEN}$OK online${NC}, ${RED}$FAIL failed${NC}"
echo "  Logs: $LOG_DIR/*.log"
echo ""

# Show service URLs
if command -v hostname &>/dev/null; then
  HOST=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "localhost")
  echo "  URLs:"
  for name in link-preview pokelabs-site poke-hub skills-marketplace; do
    echo "    http://$HOST:${PORTS[$name]}"
  done
fi

echo ""
echo "  To stop all: fuser -k 8765/tcp 8766/tcp 8775/tcp 8781/tcp"
echo ""
