---
name: gst-compliance
description: >
  GST compliance and registration skill for Vision Loop. Use for any GST
  registration, filing, or compliance task — Form GST REG-01 guidance,
  GSTR-1/3B filing schedules, LUT export, ITC reconciliation, or service
  advisory operations.
  Activate when the user asks about GST registration, GST filing, GSTIN,
  PAN validation, SAC codes, or the ₹1,999 GST registration service.
---

# GST Compliance Skill

## Entity Context
- **Proprietor:** Sapna Jaiswal
- **State:** Uttar Pradesh (State Code 09)
- **GST Threshold:** ₹20 Lakhs/year for services
- **Business Type:** Sole Proprietorship
- **Service Offering:** Tier 1 — New GST Registration @ ₹1,999 (All-Inclusive)

## Key Reference Files
| Document | Path |
|---|---|
| Service Blueprint | `data/services/GST_FILING_AND_REGISTRATION_CONSULTING_SERVICE.md` |
| YouTube Episode Script | `data/media/YOUTUBE_GST_REGISTRATION_EPISODE_SCRIPT.md` |
| Video Payload JSON | `data/media/gst_registration_video_payload.json` |
| Compliance Handbook | `data/compliance/YOUTUBE_INDIA_STATUTORY_AND_COMMUNITY_GUIDELINES.md` |

## Form GST REG-01 — Quick Reference

### Part A (TRN Generation)
```
gst.gov.in → Services → Registration → New Registration
→ Taxpayer → State: UP → Legal Name (exact PAN match)
→ PAN + Email + Mobile → CAPTCHA → OTP → TRN (15 days valid)
```

### Part B (6 Tabs)
| Tab | Key Action |
|---|---|
| Business Details | Select `Sole Proprietorship` — never skip this |
| Promoters | Upload photo, enter Aadhaar |
| Authorized Signatory | Tick "Also an Authorized Signatory" |
| **Principal Place of Business** | **Nature of Possession: `Consent`** — upload NOC + electricity bill |
| Goods & Services | SAC 998361 (YouTube), 998314 (IT), 999299 (Freelancer) |
| Verification | EVC via Aadhaar OTP → Submit → ARN generated |

## MCP Tool: `gst_validate_pan`
```json
{ "pan": "BGVPJ3356G" }
→ { "valid": true, "type": "Individual", "fourth_letter": "P" }
```

## MCP Tool: `gst_validate_gstin`
```json
{ "gstin": "09BGVPJ3356G1ZK" }
→ { "valid": true, "state_code": "09", "state": "Uttar Pradesh", "pan_embedded": "BGVPJ3356G" }
```

## Liabilities — Always Disclose
1. Monthly filing mandatory (GSTR-1 by 11th, GSTR-3B by 20th) even on ₹0 income
2. Late penalty: ₹50/day (₹20/day NIL) up to ₹10,000 per return
3. 18% p.a. interest on unpaid tax
4. B2C business disadvantage — adds 18% to price vs unregistered competitor
5. Cancellation is NOT automatic — must apply explicitly

## SAC Codes for Vision Loop Services
| SAC | Description |
|---|---|
| `997311` | Commercial Vehicle Operating Lease |
| `998314` | IT / Software Development Services |
| `998361` | Digital Advertising & YouTube Content |
| `999299` | Other Services NEC (General Freelancer) |
