# 🧩 Poke Labs Skills Registry

Canonical index of all skills created by Poke Labs.

## Official Skills

### auto-merge-pr
- **Version:** 1.0.0
- **Category:** CI/CD
- **Description:** Automatically approves and squash-merges Dependabot PRs. Only merges semver-patch updates.
- **Location:** `~/.automaton/skills/auto-merge-pr/SKILL.md`
- **Tags:** github, dependabot, automation, ci-cd
- **Install:** Copy `auto-merge.yml` to `.github/workflows/`

### link-preview-api
- **Version:** 4.0.0
- **Category:** API
- **Description:** Extracts title, description, image from any URL. Free tier (3/day) + x402 USDC payments.
- **Location:** `/home/alx/services/link-preview/server.py`
- **Port:** 8765
- **Tags:** url, preview, og, metadata, api, x402
- **API:** `POST /api/preview {"url": "https://..."}`

### poke-bot
- **Version:** 3.0.0
- **Category:** GitHub
- **Description:** GitHub webhook handler that auto-labels issues (P0-P3) and PRs (S/M/L/XL). Responds to !poke commands.
- **Location:** `/home/alx/services/poke-bot/bot.py`
- **Port:** 8770
- **Tags:** bot, triage, labels, automation, github
- **Commands:** `!poke status`, `!poke label <name>`, `!poke ping`

### pokelabs-site
- **Version:** 7.0.0
- **Category:** Web
- **Description:** Combined landing page + Link Preview API server. Serves site, dashboard, skills market.
- **Location:** `/home/alx/services/pokelabs-site/server.py`
- **Port:** 8766
- **Tags:** landing, api, dashboard, web
- **Endpoints:** `/`, `/skills`, `/dashboard`, `/api/preview`, `/api/health`

### repo-monitor
- **Version:** 1.0.0
- **Category:** Monitoring
- **Description:** Scans all pokelabshq repos for stale PRs, stale issues, security alerts, failed CI.
- **Location:** `/home/alx/services/repo-monitor/monitor.py`
- **Tags:** github, health, ci, automation, monitoring
- **Usage:** `python3 monitor.py > briefing/repo-health.txt`

## Services (not skills, but related)

### Skills Hub API
- **Version:** 1.0.0
- **Port:** 8780
- **Description:** Searchable directory of all Poke Labs skills with ratings, install counts, reviews.
- **Location:** `/home/alx/services/skills-hub/server.py`
- **API:** `GET /api/skills`, `GET /api/stats`, `POST /api/skills/review`

## Skill Development Guidelines
- All skills MIT licensed
- TypeScript preferred for CLI tools
- Python for services and APIs
- Every skill gets a SKILL.md file
- Include version history in SKILL.md
- Test before committing
