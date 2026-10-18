<!-- Design system source of truth. AI must follow these tokens and rules when generating UI. -->

# Prajna – Design System

**Last Updated**: 2026-10-18
**Status**: Active
**Related Documents**: Architecture.md, Rules.md

> This document defines the Prajna visual and design system applied across the web interface: colors, typography, radius, motion, the "Why?"/trace treatment, the restricted state, and the mascot. Values below are the **default palette** (teal brand + saffron for restricted) chosen for an Indian-rooted, calm-but-confident feel.

## 1. Design Principles
- **Clarity over decoration** — the graph answer and its path are the hero.
- **Show the work** — every answer exposes a traceable path; trust comes from transparency.
- **Calm, confident, Indian-rooted** — teal + saffron, generous whitespace, no neon.
- **Consistency creates trust** — one token set, used everywhere.
- **Accessible by default** — contrast, focus, keyboard, 44px targets.
- **Motion with meaning** — animation shows reasoning (the mascot traversing the graph), never decoration.
- **Graph-first clarity** — interface surfaces knowledge pathways and permissions intuitively.

## 2. Color System

### 2.1 Brand / Primary Colors (teal — "seeing / answering")
| Token | Light Mode Hex | Dark Mode Hex | Usage |
|---|---|---|---|
| primary-50 | #E6F6F1 | #0C2A23 | Subtle brand tint / hover bg |
| primary-100 | #C3E9DE | #10352C | Light fills |
| primary-300 | #5FC6AC | #2E8C75 | Accents, chips |
| primary-500 | #12A885 | #2BC4A0 | Main actions, links, brand |
| primary-600 | #0E8A6D | #46D3B2 | Hover / active |
| primary-700 | #0A6B55 | #6FE0C6 | Pressed / strong text on light tint |
| primary-900 | #064033 | #B9F0E3 | Text on light brand tint |

### 2.2 Neutral / Gray Scale
| Token | Light | Dark | Usage |
|---|---|---|---|
| gray-50 | #F7F8F8 | #0E1211 | Page background |
| gray-100 | #EEF0F0 | #151A19 | Card background (light) |
| gray-200 | #E1E4E4 | #1E2524 | Borders / dividers |
| gray-300 | #CBD0CF | #2A3231 | Strong border |
| gray-400 | #A6AEAD | #3C4645 | Disabled text |
| gray-500 | #7E8786 | #5A6564 | Muted text |
| gray-600 | #5D6665 | #808B89 | Secondary text |
| gray-700 | #434B4A | #AEB7B5 | Body text (dark surfaces) |
| gray-800 | #2A302F | #D6DBDA | Headings (dark) |
| gray-900 | #161A19 | #F2F4F3 | Primary text |

### 2.3 Semantic Colors
| Token | Light | Dark | Usage |
|---|---|---|---|
| success | #1E9E75 | #46D3B2 | Confirmations |
| warning | #C77D11 | #EDA33B | Cautions |
| error | #C0392B | #F0756A | Errors |
| info | #2C74B3 | #5BA3E0 | Neutral info |
| **restricted** | #E07A1F (saffron) | #F0A64D | Permission-denied state, mascot "eye closed" |

### 2.4 Background & Surface Colors
| Token | Light | Dark | Usage |
|---|---|---|---|
| bg-page | #F7F8F8 | #0E1211 | App background |
| bg-surface | #FFFFFF | #151A19 | Cards, chat bubbles |
| bg-elevated | #FFFFFF | #1E2524 | Popovers, menus |
| bg-overlay | rgba(16,20,19,0.45) | rgba(0,0,0,0.6) | Modal scrim |
| bg-path | #E6F6F1 | #0C2A23 | "Why?" path panel background |

### 2.5 Color Usage Rules
- Primary (teal) only for the main action per view, links, and the brand mark; everything else neutral.
- **Saffron = restricted only.** Never use it for ordinary accents.
- Body text contrast ≥ 4.5:1; large text ≥ 3:1.
- Avoid pure black/pure white surfaces; use gray-900/gray-50.
- Color is never the only signal (pair with icon/label), e.g., restricted shows a lock icon + text, not just saffron.

## 3. Typography

### 3.1 Font Families
- **Display / Headings:** `"Inter", system-ui, sans-serif` (proposed default; swap for a brand face later).
- **Body:** `"Inter", system-ui, sans-serif`.
- **Monospace (Cypher, code, paths):** `"JetBrains Mono", ui-monospace, monospace`.
- Fallback: always end stacks with `system-ui`/`sans-serif`/`monospace`.

### 3.2 Type Scale
| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|---|---|---|---|---|---|
| display | 2.5rem / 40px | 600 | 1.15 | -0.02em | Landing hero only |
| h1 | 2rem / 32px | 600 | 1.2 | -0.01em | Page title |
| h2 | 1.5rem / 24px | 600 | 1.25 | -0.01em | Section |
| h3 | 1.25rem / 20px | 500 | 1.3 | 0 | Subsection |
| body-lg | 1.125rem / 18px | 400 | 1.6 | 0 | Lead text |
| body | 1rem / 16px | 400 | 1.6 | 0 | Default body / chat |
| body-sm | 0.875rem / 14px | 400 | 1.5 | 0 | Secondary, metadata |
| caption | 0.75rem / 12px | 500 | 1.4 | 0.01em | Labels, badges |
| code | 0.875rem / 14px | 400 | 1.5 | 0 | Cypher / paths (mono) |

### 3.3 Typography Rules
- Max line length ~72ch for reading columns.
- One h1 per screen; never skip heading levels.
- Weights: 400 body, 500 labels/subheads, 600 headings. Avoid 700.
- Cypher and graph paths always in monospace.

## 4. Spacing & Layout

### 4.1 Spacing Scale (base 4px)
`0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80` (px). Use tokens `space-1=4` … `space-20=80`.

### 4.2 Layout
- Max content width: 1200px; reading column 720px.
- Breakpoints: mobile < 640, tablet 640–1024, desktop 1024–1440, wide > 1440.
- Chat column centered; "Why?" panel as a right drawer (desktop) or sheet (mobile).
- Container padding: 16px mobile, 24px tablet, 32px desktop.

## 5. Elevation, Borders & Radius

### Border Radius Scale
| Token | Value | Usage |
|---|---|---|
| radius-sm | 6px | Inputs, small buttons |
| radius-md | 10px | Buttons, chips |
| radius-lg | 14px | Cards, panels, chat bubbles |
| radius-xl | 20px | Modals |
| radius-full | 9999px | Pills, avatars, mascot |

### Shadows / Elevation
| Level | Light | Dark |
|---|---|---|
| elevation-1 (card) | 0 1px 2px rgba(16,20,19,0.06), 0 1px 3px rgba(16,20,19,0.08) | 0 1px 2px rgba(0,0,0,0.4) |
| elevation-2 (popover) | 0 4px 12px rgba(16,20,19,0.10) | 0 4px 16px rgba(0,0,0,0.5) |
| elevation-3 (modal) | 0 12px 32px rgba(16,20,19,0.16) | 0 12px 40px rgba(0,0,0,0.6) |

### Borders
- Width: 1px default, 2px for the focused/featured accent.
- Color: gray-200 (light) / gray-200-dark; focus ring uses primary-500.

## 6. Component Guidelines (High-Level)

#### Buttons
- Variants: primary (teal filled), secondary (neutral outline), ghost (text only), destructive (error).
- Sizes: sm (32px), md (40px), lg (48px).
- States: default, hover (primary-600), focus (2px primary-500 ring), active (scale 0.98), disabled (gray-300 text, no shadow), loading (spinner + disabled).
- One primary button per view. Icon + text: icon left, 8px gap.

#### Form Elements
- Input/select 40px tall, radius-sm, 1px gray-200 border, focus ring primary-500.
- Label above field (body-sm, gray-600). Help text below (caption). Error text in `error` color + icon; never color alone.

#### Cards / Panels
- bg-surface, radius-lg, elevation-1, padding 16–20px.
- "Why?" panel: bg-path, radius-lg, monospace path, clickable citations.

#### Modals / Dialogs
- Sizes: sm 420px, md 560px, lg 720px. Scrim bg-overlay. Focus trapped; Esc closes; return focus to trigger.

#### Navigation
- Sidebar (sessions) + top bar. Active item: primary-500 text + subtle primary-50 bg. Add a persona switcher and a tenant switcher in the top bar for the demo.

#### Chat bubble
- User: neutral surface, right-aligned. Assistant: bg-surface with mascot avatar, left-aligned. Inline citation markers `[1]` are clickable, primary-500.

#### Restricted banner (flagship state)
- Saffron (`restricted`) left border, lock icon, text "You don't have access to that." Mascot eye closes. No restricted title revealed.

## 7. Iconography
- Library: **Lucide** (outline).
- Sizes: 16, 20, 24. Inline icons 16–20; 24 for headers.
- Stroke width 1.5–2; color `currentColor`.
- Outline by default; avoid filled except active nav.

## 8. Motion & Interaction
- Duration scale: 120ms (micro), 180ms (standard), 240ms (panel), 320ms (modal).
- Easing: `cubic-bezier(0.3, 0.7, 0.3, 1)` for enters; ease-out for exits.
- Animate: mascot (thinking traversal), "Why?" panel slide, streaming text. Do not animate: large layout shifts, color of body text.
- Respect `prefers-reduced-motion`: disable mascot traversal and non-essential transitions.

## 9. Accessibility Requirements
- Contrast: body ≥ 4.5:1; large/UI ≥ 3:1.
- Visible focus ring (2px primary-500) on all interactive elements; never remove outlines without a replacement.
- Full keyboard navigation; Esc closes overlays; focus trap in modals.
- Screen-reader labels on icon-only buttons and the mascot (e.g., `aria-label="Prajna is thinking"` / `"restricted"`).
- Touch targets ≥ 44×44px.
- Color never the only indicator (restricted = saffron + lock icon + text).

## 10. Implementation Notes for Developers & AI
- Apply the brand tokens in `web/tailwind-themes` / the Tailwind config.
- Organise tokens as CSS variables (`--color-primary-500`, `--radius-lg`, `--space-4`) plus Tailwind theme extension; reference tokens, never raw hex, in components.
- Dark mode: provide both light/dark values for every token above.
- Mascot: plain SVG + CSS animation (states: idle, thinking, answer, restricted); use as the assistant avatar and loading indicator.
- Keep components to Tailwind utility classes; do not introduce a second styling system.

## 11. Design Debt & Future Improvements
- Proposed palette is a default; replace with a finalised brand palette post-hackathon.
- Inter/JetBrains Mono are placeholders; a custom display face could strengthen the brand.
- In-app graph path view is minimal; a richer interactive 3D explorer is future work.
- Continuous component styling improvements for brand polish.