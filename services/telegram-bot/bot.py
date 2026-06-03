#!/usr/bin/env python3
"""Telegram Notifier for Poke Labs. Sends morning briefings & alerts. Stdlib only."""

import json
import os
import sys
import http.client
import urllib.parse
from datetime import datetime, timezone

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

os.makedirs(DATA_DIR, exist_ok=True)


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {"chat_id": None, "sent_today": None}


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def tg_api(method, params=None):
    """Call Telegram Bot API. Returns dict or None on error."""
    if not BOT_TOKEN:
        print("ERROR: Set TELEGRAM_BOT_TOKEN env var")
        return None

    body = json.dumps(params or {}).encode()
    conn = http.client.HTTPSConnection("api.telegram.org", timeout=10)
    try:
        path = f"/bot{BOT_TOKEN}/{method}"
        conn.request("POST", path, body=body,
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        data = resp.read().decode()
        return json.loads(data)
    except Exception as e:
        print(f"Telegram API error: {e}")
        return None
    finally:
        conn.close()


def send_message(chat_id, text, parse_mode="HTML"):
    """Send a message to a Telegram chat."""
    return tg_api("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    })


def register_chat_id(chat_id):
    """Save the chat ID and send a confirmation."""
    cfg = load_config()
    cfg["chat_id"] = chat_id
    save_config(cfg)
    send_message(chat_id,
        "✅ <b>Poke Labs Monitor connected!</b>\n\n"
        "I'll send you daily morning briefings and uptime alerts here.\n"
        "Reply /status for a quick health check."
    )


def format_morning_brief(uptime_results=None):
    """Format the morning briefing message."""
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%A, %B %d, %Y")

    msg = f"🌅 <b>Good morning, Alexander!</b>\n"
    msg += f"📅 {date_str}\n\n"

    # Uptime section
    msg += "<b>🔍 Uptime Status</b>\n"
    if uptime_results:
        for r in uptime_results:
            icon = "🟢" if r.get("is_up") else "🔴"
            code = r.get("status_code", "N/A")
            ms = r.get("response_time_ms", 0)
            msg += f"{icon} {r['url']} — {code} ({ms}ms)\n"
    else:
        msg += "Run /status to check uptime\n"

    msg += "\n<b>🤖 Poke Labs Automaton</b> — alive and monitoring"
    return msg


cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

if cmd == "send" and len(sys.argv) > 2:
    # send <chat_id> <message>
    result = send_message(sys.argv[2], " ".join(sys.argv[3:]))
    print(json.dumps(result, indent=2) if result else "Failed")

elif cmd == "register" and len(sys.argv) > 2:
    register_chat_id(sys.argv[2])
    print(f"Registered chat ID: {sys.argv[2]}")

elif cmd == "brief":
    cfg = load_config()
    chat_id = sys.argv[2] if len(sys.argv) > 2 else cfg.get("chat_id")
    if not chat_id:
        print("ERROR: Provide chat_id or register first")
        sys.exit(1)

    # Fetch uptime data
    uptime_results = None
    try:
        conn = http.client.HTTPConnection("localhost", 8766, timeout=5)
        conn.request("GET", "/api/status")
        resp = conn.getresponse()
        if resp.status == 200:
            uptime_results = json.loads(resp.read().decode())
        conn.close()
    except Exception:
        pass

    msg = format_morning_brief(uptime_results)
    result = send_message(chat_id, msg)
    print(json.dumps(result, indent=2) if result else "Failed")

elif cmd == "status":
    cfg = load_config()
    print(f"Chat ID: {cfg.get('chat_id', 'not set')}")
    print(f"Bot token set: {'yes' if BOT_TOKEN else 'NO'}")

elif cmd == "help":
    print("Usage:")
    print("  bot.py send <chat_id> <message>   — Send a message")
    print("  bot.py register <chat_id>          — Register chat & confirm")
    print("  bot.py brief [chat_id]             — Send morning briefing")
    print("  bot.py status                      — Show config")
    print("  bot.py help                        — This message")
    print()
    print("Set TELEGRAM_BOT_TOKEN env var for Telegram API.")
else:
    print(f"Unknown command: {cmd}")
