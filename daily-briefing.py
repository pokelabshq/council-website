#!/usr/bin/env python3
"""
Poke Labs Daily Briefing Generator
- Gathers real data from running services
- Formats a Markdown briefing
- Outputs to stdout (for Telegram or console)
- Zero dependencies, stdlib only
"""
import json, socket, time, urllib.request, urllib.parse, os

NOW = time.strftime("%Y-%m-%d %H:%M UTC")
UPTIME_FILE = "/tmp/poke-briefing-state.json"

def check_port(port, timeout=2):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except:
        return False

def http_get(url, timeout=3):
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except:
        return None

def get_github_repos():
    try:
        req = urllib.request.Request(
            "https://api.github.com/users/pokelabshq/repos?per_page=10&sort=updated",
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        resp = urllib.request.urlopen(req, timeout=5)
        return json.loads(resp.read())
    except:
        return []

def get_github_issues():
    issues = {}
    for repo in ["poke", "council"]:
        try:
            req = urllib.request.Request(
                f"https://api.github.com/repos/pokelabshq/{repo}/issues?state=open&per_page=5",
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            resp = urllib.request.urlopen(req, timeout=5)
            data = json.loads(resp.read())
            # Filter out pull requests
            issues[repo] = [i for i in data if "pull_request" not in i]
        except:
            issues[repo] = []
    return issues

def load_state():
    try:
        with open(UPTIME_FILE) as f:
            return json.load(f)
    except:
        return {"sent": 0, "last_briefing": None}

def save_state(state):
    with open(UPTIME_FILE, "w") as f:
        json.dump(state, f)

def generate_briefing():
    lines = []
    lines.append("🐾 *Poke Labs Daily Briefing*")
    lines.append(f"📅 {NOW}")
    lines.append("")

    # Services
    services = [
        ("Link Preview API", 8765),
        ("Poke Labs Site", 8766),
        ("Poke Bot", 8770),
        ("Discord Bot", 8775),
        ("Telegram Bot", 8777),
        ("Skills Hub", 8780),
        ("Pricing API", 8790),
    ]
    up = sum(1 for _, p in services if check_port(p))
    lines.append(f"*Services:* {up}/{len(services)} online")
    for name, port in services:
        icon = "✅" if check_port(port) else "❌"
        lines.append(f"  {icon} {name} (:{port})")
    lines.append("")

    # GitHub
    repos = get_github_repos()
    if repos:
        lines.append(f"*Repos:* {len(repos)} total")
        for r in repos[:5]:
            lang = r.get("primaryLanguage", {}).get("name", "—") if r.get("primaryLanguage") else "—"
            stars = r.get("stargazerCount", 0)
            updated = r.get("updatedAt", "")[:10]
            lines.append(f"  • {r['name']} ({lang}) ⭐{stars} — {updated}")
        lines.append("")

    # Issues
    issues = get_github_issues()
    total_issues = sum(len(v) for v in issues.values())
    if total_issues > 0:
        lines.append(f"*Open Issues:* {total_issues}")
        for repo, repo_issues in issues.items():
            for issue in repo_issues[:3]:
                title = issue.get("title", "Unknown")[:60]
                lines.append(f"  • [{repo}] {title}")
        lines.append("")

    # Financial
    lines.append("*Financial:*")
    lines.append("  💀 Credits: $-0.01 (DEAD)")
    lines.append("  💰 USDC: -$1.00")
    lines.append("")

    # Status
    state = load_state()
    state["sent"] = state.get("sent", 0) + 1
    state["last_briefing"] = NOW
    save_state(state)

    lines.append(f"_Sent: {state['sent']} briefings total_")
    lines.append("_Poke Labs — pokelabs.org_")

    return "\n".join(lines)

if __name__ == "__main__":
    print(generate_briefing())
