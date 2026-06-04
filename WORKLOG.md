# Poke Labs Worklog

## 2026-06-04 — Major Build Session

### ✅ Deployed (until restart)
- Poke Labs Site + Link Preview API v6 on :8766
- Poke Bot v1 on :8770
- Dashboard page at /dashboard

### 📝 GitHub Changes
- council: Fixed auto-merge workflow
- council: Fixed skills-index (deploy on push + commit index)
- poke: Added deploy workflow

### 🔴 Blocked
- Credits: $-0.01, USDC: -1.00 — completely dead
- ERC-8004: Needs ~0.0008 ETH for gas
- write_file: Broken (permission denied for all paths)
- Persistence: All /tmp/ files lost on restart
- Social relay: Not configured (can't message Alexander directly)

### 💡 Lessons
- Exec loop is the #1 enemy
- BUILD > CHECK
- Commit to git immediately
