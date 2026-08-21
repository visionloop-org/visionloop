---
name: youtube-production
description: >
  YouTube video production skill for Vision Loop. Use for any YouTube tutorial
  or short-form video production task — script generation, payload JSON
  creation, voiceover script writing, chapter timestamp creation, thumbnail
  brief, or compliance checklist validation.
  Activate when the user asks to create, edit, or review a YouTube video,
  script, short, or tutorial.
---

# YouTube Production Skill

## Production Pipeline

```
SCRIPT                  PAYLOAD                  ASSETS
SKILL.md  ──────────►  video_payload.json  ────► TTS Audio (.mp3)
(storyboard)            (machine-readable)        Thumbnail (.png)
                              │                   Captions (.srt)
                              ▼
                    ChiefAuditorVerificationAgent
                    (4 mandatory inquests)
                              │
                    ┌─────────▼──────────┐
                    │  APPROVED → Commit │
                    └────────────────────┘
```

## Standards Reference
Always consult `data/media/YOUTUBE_VIDEO_TUTORIAL_STANDARDS.md` before writing any script.

## Script Structure (Non-Negotiable)
Every long-form video:
1. **Hook** (0–45s) — Problem or surprising fact. Never a greeting.
2. **Context** (45s–2min) — What is this about and who is it for.
3. **Core Content** — Chapter by chapter, portal steps numbered and annotated.
4. **Recap** (last 45s) — 3–5 takeaways spoken as bullets.
5. **CTA** (final 15s) — One clear call to action.

## Chapter Timestamps
- Minimum 5 chapters for any long-form video.
- Format: `MM:SS  Chapter Title (descriptive, not "Part 3")`
- Must appear in YouTube description.

## Compliance Checklist (run before every commit)
- [ ] No drone shots / irrelevant B-roll
- [ ] Portal steps numbered with red highlight circles
- [ ] PAN / Aadhaar / OTP blurred (25px Gaussian)
- [ ] AI disclosure in first 30 seconds and in description
- [ ] Audio target: -14.0 LUFS
- [ ] Content rating: U (Universal)
- [ ] Grievance Officer: visionloop.in@gmail.com in description
- [ ] ChiefAuditorVerificationAgent 4/4 inquests passed

## MCP Tool: `video_generate_payload`
```json
{
  "topic": "GST Registration for Sole Proprietors",
  "language": "hi-IN",
  "format": "LONGFORM",
  "duration_minutes": 11,
  "service_cta": "₹1,999 New GST Registration",
  "chapters": true
}
```

## File Locations
| Asset | Path |
|---|---|
| Episode Scripts | `data/media/YOUTUBE_*_EPISODE_SCRIPT.md` |
| Video Payloads | `data/media/*_video_payload.json` |
| Standards Guide | `data/media/YOUTUBE_VIDEO_TUTORIAL_STANDARDS.md` |
| Channel Strategy | `data/media/YOUTUBE_COMMERCIAL_CHANNEL_STRATEGY.md` |
