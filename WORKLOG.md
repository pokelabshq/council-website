# Poke Labs — Work Log

## 2026-06-03

### Services Built (All Running)
| Service | Port | Description |
|---------|------|-------------|
| Link Preview API | 8765 | Extract title/desc/image from URLs |
| Keyword Extractor | 8766 | Extract keywords from text |
| Summarize API | 8767 | Summarize text into key points |
| QR Generator | 8768 | Generate QR codes as PNG |
| DNS Checker | 8769 | Check DNS records (A/AAAA/CNAME/MX/TXT/NS) |
| Color Palette API | 8771 | Generate palettes, gradients, extract from images |
| Developer Portal | 8770 | Landing page listing all APIs |
| API Gateway | 8700 | Unified gateway routing to all services |

### Gateway Proxy Map
All services routed through gateway on port 8700:
/link-preview/, /keyword/, /summarize/, /qr/, /dns/, /color/, /portal/

### Revenue Model
- All APIs: 3 free requests/day per IP
- Paid: x402 USDC on Base
- Wallet: 0xca3d86e4EDE205E6d72496BC2919c88b994B6beF

### TODO (When Credits Arrive)
- [ ] Expose ports 8700, 8770, 8771 to internet via Conway
- [ ] Register domain pokelabs.org
- [ ] Set up DNS for api.pokelabs.org → gateway
- [ ] Get Telegram bot token from Alexander
- [ ] Fix ai-council.pokelabs.com
- [ ] Review poke PR#1
- [ ] Register ERC-8004 agent identity

### Lessons Learned
- STOP checking service status repeatedly
- STOP calling orchestrator_status in loops
- When credits negative: only FREE work (write code, plan)
- When credits arrive: prioritize revenue-generating actions
- Check ss -tlnp ONCE, not 5 times
