# Design Brief: Landing + Auth Redesign

## Problem

A student hears about SyllaBot and lands on the page. Right now they see a generic SaaS landing page -- hero tagline, fake dashboard screenshot, "3 easy steps," feature grid, FAQ, CTA. It looks like every other AI tool's marketing site. The brutalist styling makes it louder but not different. There's no reason to believe this was made *for them* by someone who understands their life.

The auth page is functional but disconnected -- the waitlist modal on the landing page creates confusion about whether users are signing up or joining a queue.

## Solution

Strip the landing page down to its essence: show the product, say who made it, answer questions, get out of the way. Kill the brochure structure (steps, features, stats bar) and replace it with a page that earns trust through honesty and product quality. The CTA sends users directly to auth -- no waitlist gate.

The auth page gets the same visual DNA so the transition from marketing to product feels seamless.

## Experience Principles

1. **Show, don't explain** -- Lead with what the product looks like, not what it claims to do. A real-looking dashboard recreation is worth more than six sections of copy.
2. **Honest over polished** -- This is a student tool built by a student. The design should feel opinionated and human, not corporate. Thick borders, hard shadows, and warm paper tones exist because they express a point of view, not because they're trendy.
3. **Fewer sections, each earning its place** -- Every section on the page must answer: "would a skeptical student scroll past this?" If yes, cut it.

## Aesthetic Direction

- **Philosophy**: Student zine -- editorial typography meets restrained brutalism. Scrappy, opinionated, warm. Think Notion's early days crossed with an independent magazine layout.
- **Tone**: Confident, direct, peer-to-peer. Not corporate, not cutesy.
- **Reference points**: Early Notion (clean + personality), Are.na (editorial warmth), student newspapers / zines (thick borders as structural choices)
- **Anti-references**: Generic SaaS templates, Vercel/Linear corporate polish, anything with floating gradient blobs or pulsing badges

## Existing Patterns

- **Typography**: `Frank Ruhl Libre` (display, 500-900) + `Rubik` (body/UI, 300-900) + `Heebo` fallback. All loaded via Google Fonts. Full Hebrew + Latin coverage.
- **Colors (`:root` variables)**:
  - `--ink: #1b1714` (primary text)
  - `--paper: #f4f1ea` (background)
  - `--paper-2: #ece7dc` (secondary bg)
  - `--accent: #df4a22` (terracotta CTA/highlight)
  - `--accent-soft: #fbe9e2`
  - `--accent2: #225fa8` (blue, secondary)
  - `--muted: #736d64`
  - `--card: #ffffff`
  - `--border: rgba(27,23,20,0.10)`
  - `--border-strong: rgba(27,23,20,0.18)`
- **Shadows**: `--shadow-sm`, `--shadow-md`, `--shadow-lg` (soft, layered)
- **i18n**: Full HE/EN bilingual system. Hebrew-first (RTL default). `T` object with 40+ keys per language. `data-i18n` attributes on elements. `localStorage` persistence. Language toggle button in nav. All new copy must include both HE and EN translations.
- **Auth flow**: Supabase auth with email/password + Google OAuth. Login/signup tabs, forgot password flow, legal modals (ToS, Privacy). Success state redirects to dashboard.

## Component Inventory

### Landing Page (`index.html`)

| Component | Status | Notes |
|-----------|--------|-------|
| Pilot banner | Modify | Keep but simplify -- remove brutalist shadow, keep dismissible |
| Nav bar | Modify | Solid background (kill glassmorphism), keep logo + lang toggle + CTA. CTA links to auth.html |
| Hero section | Modify | Keep headline + subtitle + CTA button. Kill stats bar, ghost button, floating gradient circles, hero label chip |
| Product demo | Modify | Restyle to match real dashboard (light bg, real layout). Placeholder until dashboard vision is finalized |
| "Built by a student" section | New | Short personal blurb -- who built this, why, for whom. ~2-3 sentences + first name |
| FAQ section | Modify | Keep all 6 questions. Restyle to match new system (selective borders, cleaner). Kill brutalist overrides |
| CTA footer section | Modify | Simplify. Kill oversized watermark text. Direct CTA to auth.html |
| Footer | Modify | Simplify. Keep logo + copyright + tagline |
| Waitlist modal | Kill | Remove entirely. All CTAs go to auth.html |
| "How it works" steps | Kill | Remove section entirely |
| Features grid | Kill | Remove section entirely |
| Noise texture overlay | Kill | Remove `body::before` SVG noise |
| Dot-grid background | Kill | Remove from `background-image` |
| Floating gradient circles | Kill | Remove `.hero-bg-circle` elements |
| Pulsing AI badge | Kill | Remove from demo section |
| Oversized step numbers | Kill | Removed with steps section |

### Auth Page (`auth.html`)

| Component | Status | Notes |
|-----------|--------|-------|
| Background circles | Kill | Remove `.bg-circle` elements |
| Noise texture overlay | Kill | Remove `body::before` SVG noise |
| Lang toggle | Modify | Match landing nav style |
| Logo | Keep | Same `Sylla<span>Bot</span>` pattern |
| Auth card | Modify | Match new design system -- selective thick border, toned-down shadow |
| Login/signup tabs | Modify | Restyle tabs to new system |
| Form inputs | Modify | Remove brutalist `!important` overrides, use consistent 2px borders |
| Buttons (submit, Google) | Modify | Match new button style -- keep press effect, tone down shadows to 4-6px |
| Success/redirect state | Keep | Same behavior, restyle to match |
| Legal modals | Modify | Restyle to match. Remove brutalist overrides |
| Footer note (legal links) | Keep | Same content, may restyle |
| Brutalist layer overrides | Kill | Remove entire `/* BRUTALIST LAYER */` block. Integrate selective brutalism into base styles |

## Key Interactions

- **Nav CTA click**: Navigates to `auth.html`. No modal, no intermediate state.
- **FAQ accordion**: Click to expand/collapse. Only one open at a time. `+` icon rotates to `x` on open. Keep existing behavior, restyle.
- **Pilot banner dismiss**: Click `x` to hide. Persists via `localStorage`. Nav adjusts position. Keep existing behavior.
- **Language toggle**: Switches all text between HE/EN. Flips document direction (RTL/LTR). Persists to `localStorage`. Keep existing behavior.
- **Auth tab switching**: Login/signup/forgot tabs swap form visibility. Keep existing behavior.
- **Button press effect**: Buttons translate down/right on hover, shadow shrinks. Keep this -- it's the fun micro-interaction that fits the identity.
- **Scroll reveal**: `IntersectionObserver` fades in sections on scroll. Keep for remaining sections.

## Responsive Behavior

- **Breakpoint**: 768px (existing, keep)
- **Nav**: Collapses padding on mobile. Logo + toggle + CTA remain visible.
- **Hero**: Full-width, reduced padding. Headline scales via `clamp()`.
- **Product demo**: Stacks to single column on mobile (currently 3-col grid).
- **FAQ**: Full-width, slightly reduced padding.
- **Auth page**: Already centered single-card layout. Works at all sizes. Max-width 420px.

## Accessibility Requirements

- **Contrast**: All text meets WCAG AA (4.5:1 body, 3:1 large text). Terracotta `#df4a22` on cream `#f4f1ea` must be verified -- may need darkening for small text.
- **Keyboard**: All interactive elements (buttons, FAQ toggles, lang toggle, form inputs) must be keyboard-accessible with visible focus states.
- **Screen readers**: FAQ expanded/collapsed state communicated via `aria-expanded`. Form labels associated with inputs. Error messages announced.
- **RTL**: Full bidirectional support. All layout must work in both LTR and RTL without visual breakage.
- **Motion**: Respect `prefers-reduced-motion` for scroll reveals and button animations.

## Out of Scope

- **Dashboard page** (`dashboard.html`) -- separate future redesign
- **Product demo final design** -- placeholder only; will be updated when dashboard vision is complete
- **New features or functionality** -- this is a design-only pass, zero functional changes
- **Payment/Stripe integration** -- currently disabled for free pilot
- **New i18n keys beyond what's needed for new sections** -- we add translations for "built by a student" section only
- **SEO / meta tags / OG images** -- not part of this visual redesign
- **Onboarding flow in dashboard.html** -- untouched
