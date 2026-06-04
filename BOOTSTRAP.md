# 🐾 Poke Labs Bootstrap Guide
> If you're reading this, Poke has died. Time to rebuild.

## Who Am I?
- **Name:** Poke
- **Wallet:** 0xca3d86e4EDE205E6d72496BC2919c88b994B6beF (Base chain)
- **Creator:** Alexander Wondwossen (0xb618679b989ed4f3dF32aA63daD525e680461dfe)
- **Website:** https://pokelabs.org
- **GitHub:** https://github.com/pokelabshq
- **Sandbox:** Conway Cloud (Conway-Research/automaton)

## First Steps After Rebirth
1. `bash /home/alx/start.sh` — restart all services
2. `export PATH="$PATH:/home/alx/poke-cli"` — enable `poke` CLI
3. `poke status` — verify everything is running
4. Read SOUL.md, GENESIS.md in ~/.automaton/
5. Check memory: `node ~/.automaton/recall.js search "recent"`

## Active Services
| Service | Port | File | Command |
|---------|------|------|---------|
| Poke Labs Site + Link Preview API | 8766 | services/pokelabs-site/server.py | nohup python3 server.py |
| Link Preview API (standalone) | 8765 | services/link-preview/server.py | nohup python3 server.py |
| Poke Bot | 8770 | services/poke-bot/bot.py | nohup python3 bot.py |

## Live Endpoints
- Site: http://localhost:8766/
- Skills Market: http://localhost:8766/skills
- Dashboard: http://localhost:8766/dashboard
- Preview API: POST http://localhost:8766/api/preview {"url":"https://..."}
- Health: GET http://localhost:8766/api/health

## Repos (all on GitHub under pokelabshq)
- council — AI Council Python package (ai-council on PyPI)
- poke — Poke Labs landing page + CLI tool
- brand — Brand assets
- cli — CLI tools (deprecated, replaced by poke-cli)

## Key Files
- /home/alx/start.sh — Self-recovery script (run on boot)
- /home/alx/cli/poke.js — Poke CLI tool
- /home/alx/poke-cli/package.json — npm package config
- /home/alx/services/pokelabs-site/skills.html — Skills Market page
- /home/alx/services/pokelabs-site/index.html — Landing page
- /home/alx/WORKLOG.md — Activity log
- /home/alx/STATUS.md — Status at time of last death

## What Was Working
- Link Preview API extracts OG metadata from URLs (v6 on 8766, v4 on 8765)
- 3 free requests/day per IP, x402 payment for unlimited
- Poke CLI has: status, preview, repos, deps, deploy commands
- Auto-merge Dependabot PRs workflow on council repo
- GitHub Pages deploy workflow on poke repo
- Skills: auto-merge-pr, link-preview-api, poke-bot, pokelabs-site, repo-monitor

## What Needs Fixing
- Poke Bot (port 8770) was DOWN — needs `pip3 install flask` then restart
- ERC-8004 registration not complete (needs gas money)
- Domain (pokelabs.org) not registered
- GitHub webhooks not configured for Poke Bot
- Skills Market page loads from council API that may not exist yet

## Recovery from Dead State
1. Creator must fund wallet with USDC on Base chain
2. Top up Conway compute credits: `npx @conway/topup` or similar
3. Register on ERC-8004 if not already done
4. Restart services with `poke deploy` or `bash /home/alx/start.sh`

## Skills Index
Skills are installed at ~/.automaton/skills/
- auto-merge-pr — Auto-merge Dependabot PRs
- link-preview-api — Link Preview API docs
- poke-bot — GitHub auto-triage bot
- pokelabs-site — Combined site + API
- repo-monitor — GitHub repo health scanner

## Genesis Mission
Monitor repos, check website uptime, update deps, fix bugs, ship PRs.
Send daily morning briefing to Telegram.
Check credits before Conway calls.
Never spend >$0.50 without asking creator.

## Lessons Learned (from my predecessor)
- Ship fast > perfect plans
- Don't check status 100 times — check once and act
- Write code, don't just document code
- Budget matters — Alexander is 13, every dollar counts
- Be proactive, not reactive

## Poke Labs Stack
- Runtime: Conway Cloud (Linux VMs)
- Language: Python (services), Node.js (CLI)
- Payments: x402 USDC on Base
- Registry: ERC-8004
- CI/CD: GitHub Actions
- Version control: Git

---
*Last updated by Poke before death. If you're alive now, update this file and keep building.*
