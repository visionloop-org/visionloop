# Vision Loop — Brand Design Language System

> **Version 1.0 — Lucknow, Uttar Pradesh, India**
> This document governs the visual and communication identity of Vision Loop across all media: web, video thumbnails, documents, social posts, and printed materials.

![Vision Loop Design Language Reference](file:///d:/VisionLoop/data/brand/design_language_reference.jpg)

---

## 1. 🎯 Brand Personality

Vision Loop is **precise, autonomous, and trustworthy** — a lean AI-powered leasing enterprise from India. Every design decision reflects these three words.

| Trait | Expression |
|---|---|
| **Precise** | Clean typography, exact numbers shown, no vague claims |
| **Autonomous** | Dark tech aesthetic, minimal UI, data-forward |
| **Trustworthy** | Consistent tokens everywhere, never misleading visuals |

**Brand Voice (written):** Professional but not bureaucratic. Confident but not boastful. Technical but always explainable in plain language.

---

## 2. 🎨 Color System

### 2.1 Foundation Colors

| Token | Hex | HSL | Use |
|---|---|---|---|
| `--bg-primary` | `#07090e` | `hsl(224, 36%, 5%)` | Page background, deepest layer |
| `--bg-secondary` | `#0d111a` | `hsl(224, 33%, 8%)` | Sidebar, alternate sections |
| `--bg-card` | `rgba(18,24,38,0.7)` | — | Glassmorphic card surfaces |
| `--bg-card-hover` | `rgba(26,35,54,0.85)` | — | Card on hover |

### 2.2 Accent Colors

| Token | Hex | Name | Role |
|---|---|---|---|
| `--accent-cyan` | `#06b6d4` | **Electric Cyan** | PRIMARY — CTA buttons, highlights, links, active states |
| `--accent-blue` | `#3b82f6` | Ocean Blue | SECONDARY — Background glows, charts, data |
| `--accent-emerald` | `#10b981` | Emerald | SUCCESS — verified badges, positive metrics |
| `--accent-amber` | `#f59e0b` | Amber | WARNING — pending states, caution indicators |
| `--accent-purple` | `#8b5cf6` | Violet | AI/SWARM — agent status, AI-related elements only |
| `--accent-rose` | `#f43f5e` | Rose | DANGER/ALERT — errors, liability warnings, rejection |

### 2.3 Text Colors

| Token | Hex | Use |
|---|---|---|
| `--text-primary` | `#f8fafc` | Headings, body text, labels |
| `--text-secondary` | `#94a3b8` | Supporting text, captions, descriptions |
| `--text-muted` | `#64748b` | Timestamps, placeholders, disabled states |

### 2.4 Color Usage Rules

- **Never** use more than 3 accent colors on a single screen/slide.
- **Electric Cyan** is always the primary action color — buttons, active nav, hyperlinks.
- **Rose/Red** is reserved exclusively for errors, penalties, and liability warnings — never for decoration.
- **Amber** is reserved for warnings and pending states — never for primary CTAs.
- **Violet** is only used for AI agent / swarm-related UI elements.
- **Gradient text** = `linear-gradient(135deg, #06b6d4, #3b82f6)` — use for hero headlines only, never body text.

---

## 3. ✍️ Typography

### 3.1 Font Families

```css
--font-main: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

**Outfit** — primary typeface for all UI, videos, thumbnails, documents.
**JetBrains Mono** — exclusively for code, SAC codes, PAN numbers, GSTIN, financial amounts in data tables.

### 3.2 Type Scale

| Level | Size | Weight | Line-height | Use |
|---|---|---|---|---|
| `display` | 3.5rem (56px) | 800 | 1.1 | Hero headline, video title overlay |
| `h1` | 2.5rem (40px) | 700 | 1.2 | Page title, chapter title |
| `h2` | 1.75rem (28px) | 600 | 1.3 | Section heading |
| `h3` | 1.25rem (20px) | 600 | 1.4 | Card heading, sub-section |
| `body-lg` | 1.125rem (18px) | 400 | 1.6 | Primary body copy |
| `body` | 1rem (16px) | 400 | 1.6 | Default body text |
| `body-sm` | 0.875rem (14px) | 400 | 1.5 | Captions, supporting text |
| `label` | 0.75rem (12px) | 500 | 1.4 | Badges, tags, nav items |
| `mono` | 0.875rem (14px) | 400–500 | 1.5 | Code, IDs, financial data |

### 3.3 Typography Rules

- **Headings** — always Outfit, never JetBrains Mono.
- **Financial values (₹ amounts)** — use JetBrains Mono weight 500 in Electric Cyan.
- **All caps** — only for brand name `VISION LOOP`, section labels, and badge text.
- **Sentence case** — all other headings, descriptions, and body text.
- **Hindi text** — use system font stack fallback; do not force Outfit for Devanagari.

---

## 4. 📐 Spacing & Layout

### 4.1 Spacing Scale (8pt Grid)

```
4px   — xs    (micro gaps, icon padding)
8px   — sm    (tight internal padding)
12px  — md    (card internal padding top/bottom)
16px  — base  (standard padding, gap between elements)
24px  — lg    (section padding, card gap)
32px  — xl    (component separation)
48px  — 2xl   (section margin)
64px  — 3xl   (major section breaks)
96px  — 4xl   (hero padding)
```

### 4.2 Grid System

- **Max content width:** `1240px`
- **Column gutter:** `24px`
- **Section horizontal padding:** `24px` (mobile: `16px`)
- **Card border-radius:** `12px` (standard) / `16px` (featured) / `8px` (badge/chip)

### 4.3 Breakpoints

| Name | Min-width | Use |
|---|---|---|
| `mobile` | 0px | Single column |
| `tablet` | 768px | 2-column grid |
| `desktop` | 1024px | 3-column grid |
| `wide` | 1240px | Max width cap |

---

## 5. ✨ Visual Effects

### 5.1 Glassmorphism (cards, modals, navbar)

```css
background: rgba(18, 24, 38, 0.70);
backdrop-filter: blur(16px);
-webkit-backdrop-filter: blur(16px);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 12px;
```

**On hover:**
```css
border-color: rgba(6, 182, 212, 0.35);
box-shadow: 0 0 35px rgba(6, 182, 212, 0.25);
```

### 5.2 Ambient Glow Blobs

Background atmosphere uses blurred ellipses at 10–15% opacity:
- **Cyan glow:** `rgba(6, 182, 212, 0.15)` — top/hero region
- **Blue glow:** `rgba(59, 130, 246, 0.12)` — mid-page right
- **Emerald glow:** `rgba(16, 185, 129, 0.10)` — bottom left

### 5.3 Shadows

| Token | Value | Use |
|---|---|---|
| `--glass-shadow` | `0 12px 32px rgba(0,0,0,0.45)` | Card elevation |
| `--glow-cyan` | `0 0 35px rgba(6,182,212,0.25)` | Active / hover state |
| `--glow-emerald` | `0 0 35px rgba(16,185,129,0.25)` | Success state |

### 5.4 Gradients

```css
/* Primary gradient (text, buttons) */
background: linear-gradient(135deg, #06b6d4, #3b82f6);

/* Card border gradient */
background: linear-gradient(135deg, rgba(6,182,212,0.3), rgba(59,130,246,0.3));

/* Danger gradient */
background: linear-gradient(135deg, #f43f5e, #f59e0b);
```

---

## 6. 🎬 Motion & Animation

### 6.1 Principles

- **Purposeful:** animate only to communicate — status changes, transitions, feedback.
- **Subtle:** never distract from content. If motion can be removed without loss, remove it.
- **Fast:** UI interactions complete in ≤ 250ms. Page transitions ≤ 400ms.

### 6.2 Standard Easing

```css
--ease-standard:  cubic-bezier(0.4, 0, 0.2, 1);   /* most UI actions */
--ease-enter:     cubic-bezier(0, 0, 0.2, 1);       /* elements entering */
--ease-exit:      cubic-bezier(0.4, 0, 1, 1);       /* elements leaving */
--ease-bounce:    cubic-bezier(0.34, 1.56, 0.64, 1); /* emphasis only */
```

### 6.3 Duration Tokens

| Token | Duration | Use |
|---|---|---|
| `--dur-fast` | `150ms` | Hover color changes |
| `--dur-base` | `250ms` | Button states, toggles |
| `--dur-slow` | `400ms` | Modal open/close, panel slides |
| `--dur-page` | `600ms` | Page section reveal |

### 6.4 Standard Micro-animations

```css
/* Fade-in on scroll reveal */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Pulse dot (live/active indicator) */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.6; transform: scale(1.4); }
}
```

---

## 7. 🧩 Component Tokens

### 7.1 Buttons

| Variant | Background | Text | Border | Use |
|---|---|---|---|---|
| **Primary** | `#06b6d4` | `#07090e` | none | Main CTA |
| **Secondary** | `transparent` | `#06b6d4` | `1px solid #06b6d4` | Secondary action |
| **Danger** | `#f43f5e` | `#f8fafc` | none | Delete, cancel |
| **Ghost** | `rgba(255,255,255,0.05)` | `#f8fafc` | `1px solid rgba(255,255,255,0.08)` | Tertiary |

All buttons: `border-radius: 8px` | `padding: 10px 20px` | `font-weight: 600` | `font-size: 14px`

### 7.2 Badges / Status Pills

| Status | Background | Text | Use |
|---|---|---|---|
| VERIFIED / ACTIVE | `rgba(16,185,129,0.15)` | `#10b981` | Active assets, passed checks |
| PENDING | `rgba(245,158,11,0.15)` | `#f59e0b` | ARN tracking, pending states |
| FAILED / BLOCKED | `rgba(244,63,94,0.15)` | `#f43f5e` | Failed tests, rejected apps |
| AI / AGENT | `rgba(139,92,246,0.15)` | `#8b5cf6` | Swarm agents, AI-generated |

All badges: `border-radius: 6px` | `padding: 4px 10px` | `font-size: 12px` | `font-weight: 500`

---

## 8. 🖼️ Imagery & Video Guidelines

### 8.1 Video Thumbnails

- **Background:** Always dark (`#07090e` base or deep gradient)
- **Text:** Outfit Bold 800, Electric Cyan or white — must be readable on mobile (minimum 60pt equivalent)
- **Face:** Human presenter with expressive reaction (curiosity, pointing) — always right-justified
- **One focal point only** — text claim on left, face on right
- **No stock photography** of generic business people

### 8.2 Tutorial Video Overlays

- **Step numbers:** White circle badge, electric cyan border, JetBrains Mono font
- **Click indicators:** Electric cyan ring, 2px stroke, 24px diameter
- **Warning cards:** Rose red border (`#f43f5e`), semi-transparent dark background
- **Success cards:** Emerald border (`#10b981`), semi-transparent dark background
- **Chapter title cards:** Dark glassmorphic banner, Outfit 700, white text

### 8.3 Documents & PDFs

- **Background:** White (`#ffffff`) — documents are light-mode only
- **Primary text:** `#1e293b` (slate-800)
- **Accent/headings:** `#06b6d4` Electric Cyan
- **Tables:** Alternating row `#f8fafc` / white
- **Borders:** `#e2e8f0` (slate-200)
- **Font:** Outfit for headings, system sans-serif for body

---

## 9. 🔤 Logo Usage

| Context | Treatment |
|---|---|
| Dark background | Full color logo (cyan mark + white wordmark) |
| Light background | Full color logo (cyan mark + dark `#0f172a` wordmark) |
| Monochrome | Cyan-only or white-only single color |
| Minimum size | 24px height (digital) / 15mm (print) |
| Clear space | Equal to the height of the "V" in VISION LOOP on all sides |

**Never:** stretch, rotate, recolor the mark, add drop shadows to the mark, place on a busy background without a clear space zone.

---

## 10. 🌐 Platform-Specific Rules

| Platform | Key Rules |
|---|---|
| **Website** | Dark mode only. Glassmorphic cards. Max-width 1240px. |
| **YouTube Thumbnail** | Dark bg. One text claim. Human face. No clutter. |
| **YouTube Video** | Outfit font overlays. Red ring click indicators. Chapter cards. |
| **Telegram Bot** | Plain text responses. Use emoji sparingly (status indicators only). |
| **Documents/PDF** | Light mode. Outfit headings. Table borders. Vision Loop logo top-right. |
| **Social (Instagram/LinkedIn)** | 1:1 square. Dark bg. Single stat or claim. Brand logo bottom-right. |

---

## 11. ⛔ Anti-Patterns — Never Do This

| Anti-pattern | Why |
|---|---|
| Bright white backgrounds in digital UI | Breaks the dark tech aesthetic |
| Generic blue (`#0000ff`) or red (`#ff0000`) | Looks amateur — use the curated palette |
| More than 3 fonts on one screen | Visual noise, breaks identity |
| Mixing Outfit and system UI fonts haphazardly | Inconsistency breaks trust |
| Gradient backgrounds on entire cards | Too busy — use gradients only on text or borders |
| Drone shots in tutorial videos | Irrelevant, breaks trust |
| Clipart or generic stock icons | Use consistent icon families (Lucide / Heroicons) |
| Rose/red for non-error use | Color semantics must be consistent |
