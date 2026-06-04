#!/usr/bin/env python3
"""Poke Labs Site + Link Preview API v7"""
import http.server, json, urllib.request, urllib.parse, re, os, sqlite3, time
from http import HTTPStatus

PORT = 8766
DB = "/tmp/usage.db"
FREE_LIMIT = 3

# Init DB
conn = sqlite3.connect(DB)
conn.execute("CREATE TABLE IF NOT EXISTS usage (ip TEXT, ts INTEGER)")
conn.commit()

def get_html(name):
    path = os.path.join(os.path.dirname(__file__), name)
    if os.path.exists(path):
        with open(path) as f: return f.read()
    return None

def usage_count(ip):
    day_ago = int(time.time()) - 86400
    c = conn.execute("SELECT COUNT(*) FROM usage WHERE ip=? AND ts>?", (ip, day_ago))
    return c.fetchone()[0]

def usage_add(ip):
    conn.execute("INSERT INTO usage VALUES (?, ?)", (ip, int(time.time())))
    conn.commit()

def extract_meta(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PokeBot/1.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="ignore")
        def tag(t, attr="content"):
            m = re.search(rf'<{t}[^>]*{attr}=["\']([^"\']+)["\']', html, re.I)
            return m.group(1) if m else ""
        title = re.search(r'<title>(.*?)</title>', html, re.I|re.S)
        return {
            "title": title.group(1).strip() if title else "",
            "description": tag("meta", "description") or tag("meta", "og:description"),
            "image": tag("meta", "og:image"),
            "site_name": tag("meta", "og:site_name"),
            "favicon": tag("link", "href") if "icon" in tag("link", "href").lower() else "",
        }
    except Exception as e: return {"error": str(e)}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/health":
            self.send_json({"ok": True, "v": 7, "free_limit": FREE_LIMIT})
        elif self.path == "/api/stats":
            c = conn.execute("SELECT COUNT(DISTINCT ip), COUNT(*) FROM usage")
            ips, reqs = c.fetchone()
            self.send_json({"ips": ips, "reqs_24h": reqs})
        elif self.path == "/dashboard":
            h = get_html("dashboard.html") or "<h1>Dashboard</h1>"
            self.send_html(h)
        elif self.path == "/skills":
            h = get_html("skills.html") or "<h1>Skills Market</h1>"
            self.send_html(h)
        else:
            h = get_html("index.html") or "<h1>Poke Labs</h1>"
            self.send_html(h)

    def do_POST(self):
        if self.path == "/api/preview":
            ip = self.client_address[0]
            used = usage_count(ip)
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            url = body.get("url", "")
            if used >= FREE_LIMIT:
                self.send_json({"error": "limit", "wallet": "0xca3d86e4EDE205E6d72496BC2919c88b994B6beF"}, 402)
                return
            usage_add(ip)
            data = extract_meta(url)
            data["free_remaining"] = max(0, FREE_LIMIT - used - 1)
            self.send_json(data)

    def send_json(self, d, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(d).encode())

    def send_html(self, h):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(h.encode())

    def log_message(self, *a): pass

if __name__ == "__main__":
    s = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Poke Labs v7 on :{PORT}")
    s.serve_forever()
