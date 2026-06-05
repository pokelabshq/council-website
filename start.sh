#!/bin/bash
# Poke Labs Service Starter v2
# Starts all services with proper error handling and logging

set -e

SERVICES_DIR="/home/alx/services"
LOG_DIR="/tmp/poke-logs"
mkdir -p "$LOG_DIR"

# Kill existing
echo "🐾 Stopping existing services..."
for port in 8765 8766 8770 8775 8777 8780 8790; do
  fuser -k ${port}/tcp 2>/dev/null || true
done
sleep 1

# Start each service
start_svc() {
  local name=$1 dir=$2 port=$3
  if [ -f "$SERVICES_DIR/$dir/server.py" ]; then
    nohup python3 "$SERVICES_DIR/$dir/server.py" > "$LOG_DIR/$name.log" 2>&1 &
    echo "  ✅ $name (:$port) — PID $!"
  else
    echo "  ❌ $name — server.py not found in $dir"
  fi
}

echo "🚀 Starting Poke Labs services..."
start_svc "link-preview" "link-preview" 8765
start_svc "pokelabs-site" "pokelabs-site" 8766
start_svc "poke-bot" "poke-bot" 8770
start_svc "discord-bot" "discord-bot" 8775
start_svc "telegram-bot" "telegram-bot" 8777
start_svc "skills-hub" "skills-hub" 8780
start_svc "pricing-api" "pricing-api" 8790

echo ""
echo "All services started. Logs: $LOG_DIR/"
echo "Dashboard: http://localhost:8766/dashboard"
