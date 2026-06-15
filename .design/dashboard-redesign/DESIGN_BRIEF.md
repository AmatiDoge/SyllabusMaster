# Design Brief: Dashboard Redesign

## Problem

A student opens the dashboard and sees three equal-weight boxes (Exams, Tasks, Syllabus by Week) all shouting at the same volume. Thick borders and 12px offset shadows on every element. No visual hierarchy — an exam in 3 days looks the same as one in 18 days. Completing a task gives a limp strikethrough. There's no way to add events manually without re-running the onboarding flow. The whole page uses ad-hoc colors and old tokens (`--bg`, `--text`, `--sans`) that don't match the redesigned landing and auth pages.

The dashboard *works* — but it doesn't feel good to use daily. It doesn't reward progress, surface urgency, or help students feel in control.

## Solution

Redesign the dashboard as a three-mode tool that gives students calm confidence over their semester:

1. **Focus view** (default) — "What matters right now." Today's tasks, imminent deadlines, this week's readings. Not everything, just what needs attention.
2. **Timeline view** — "The whole picture." Scroll through the semester chronologically, see what's coming, spot clusters.
3. **Workload view** — "Can I plan ahead?" Stacked bar chart + stats showing load distribution across weeks and courses.

Each view serves a distinct purpose. The default view shifts from "here's everything in 3 columns" to "here's what's urgent, with a clear path to the bigger picture."

Task completion becomes satisfying — a check animation, visual demotion (item stays but recedes), and a progress indicator showing momentum ("4/7 done this week"). Think crossing something off in a paper planner.

Adding new events gets two paths: inline "+" rows for quick adds (type and enter), and a structured modal form for full details (course, type, date, description).

The entire page migrates to the established design token system from the landing/auth redesign, bringing visual consistency across the product.

## Experience Principles

1. **Urgency through hierarchy, not volume** — Use color temperature, spacing, and typography weight to communicate what matters, not border thickness on everything. An exam in 3 days should *feel* urgent without a neon badge.
2. **Reward progress visibly** — Every completed task should feel like a small win. Progress indicators, satisfying animations, and visual momentum replace flat strikethroughs.
3. **Calm command center** — The dashboard should make students feel *in control*, not overwhelmed. Default to showing less with clear paths to more. Progressive disclosure over information dump.

## Aesthetic Direction

- **Philosophy**: Student zine — editorial typography + restrained brutalism. Consistent with landing/auth redesign.
- **Tone**: Functional warmth. This is a daily-use tool, not a marketing page. The brutalism is selective — structural borders on key containers, hard shadows on interactive elements, but the content areas breathe.
- **Reference points**: Notion's task views (clean hierarchy), Linear's issue tracker (urgency without noise), Things 3 (completion satisfaction), Todoist (focused daily view)
- **Anti-references**: Jira (overwhelming), Google Classroom (sterile), over-gamified dashboards with confetti and streaks

## Existing Patterns

- **Typography**: `Frank Ruhl Libre` (display, 500-900) + `Rubik` (body/UI, 300-900) + `Heebo` fallback. All loaded via Google Fonts. Full Hebrew + Latin coverage.
- **Design Tokens**: Full token system established in `.design/landing-auth-redesign/DESIGN_TOKENS.css` and already applied to `index.html` and `auth.html`. Dashboard must use the same `:root` block.
- **Colors (new token system)**:
  - `--color-bg: #f4f1ea` (warm cream paper)
  - `--color-bg-card: #ffffff`
  - `--color-text: #1b1714` (ink)
  - `--color-text-muted: #736d64`
  - `--color-accent: #df4a22` (terracotta)
  - `--color-accent-text: #c03d18` (AA-safe for small text)
  - `--color-border-ink: #1b1714`
- **Borders**: `--border-thin` (1.5px), `--border-structural` (2.5px), `--border-heavy` (3px)
- **Shadows**: Soft (`--shadow-sm/md/lg`) + hard brutalist (`--shadow-hard-sm/md/lg`) + press effect (`--shadow-press-rest/hover`)
- **i18n**: Full HE/EN bilingual system. Hebrew-first (RTL default). `STRINGS` object with keys per language. `applyLang()` function updates DOM text, direction, and re-renders. `localStorage` persistence.
- **Auth**: Supabase auth. Dashboard checks session on load, redirects to auth.html if not logged in.
- **Data**: Supabase `user_data` table stores tasks, exams, syllabus, done_map, course_colors, semester_start, rev (optimistic concurrency), ics_token, preferred_view.
- **External libs**: Chart.js v4 (workload), DOMPurify v3 (sanitization), pdf.js v3 (PDF processing).

## Component Inventory

### Dashboard Chrome

| Component | Status | Notes |
|-----------|--------|-------|
| Auth loading screen | Keep | Restyle spinner to match tokens |
| Top bar | Modify | Title, view switcher, date, user info. Restyle with tokens, improve view switcher tabs |
| View switcher | Modify | Replace emoji labels (📋⏱️📊) with text labels. Style as tab bar with `--border-structural` + active state with `--shadow-hard-sm` |
| Sync status dot | Keep | Restyle colors to use status tokens |
| Settings button | Modify | Match new button style with press effect |
| Feedback FAB | Modify | Restyle with tokens |

### Focus View (was List View)

| Component | Status | Notes |
|-----------|--------|-------|
| 3-column box layout | Kill | Replace with single-column focused layout |
| Exams & Deadlines box | Modify | Becomes "Upcoming Deadlines" section in focus view. Add urgency tiers: critical (≤3 days, red), soon (≤7 days, orange), upcoming (>7 days, neutral) |
| Tasks box | Modify | Becomes "Today's Tasks" section. Add progress indicator (e.g., "4/7 done"). Group by course |
| Syllabus by Week box | Modify | Becomes "This Week" section. Show current week's readings/items with course grouping |
| Task completion | Modify | Replace strikethrough with: check animation, visual demotion (opacity + muted color), progress ring/bar update |
| Inline add row | New | "+" row at bottom of tasks/deadlines for quick add. Type, hit enter |
| Add event modal | New | Structured form: course dropdown, type selector (exam/task/reading/etc), date picker, description, week number. Triggered from "+" row's "more options" or a dedicated button |
| Week navigation | Modify | Keep arrows but add context — show week number + date range prominently |
| Item delete | Modify | Keep but soften — fade-out animation instead of instant removal |
| Course color dots | Keep | Restyle to align with refined palette |
| Tag badges | Modify | Use `--color-accent-soft` style backgrounds with `--border-thin`. Refine per-type colors as tokens |

### Timeline View

| Component | Status | Notes |
|-----------|--------|-------|
| Month group headers | Modify | Use `--font-display` for month names, `--border-structural` separator |
| Timeline items | Modify | Better urgency states — use color temperature not just classes. Past items muted, urgent items warm |
| Timeline bars | Modify | Course-colored left border. Match card treatment from focus view |
| Click-to-jump | Keep | Click timeline item to jump to that week in focus view |

### Workload View

| Component | Status | Notes |
|-----------|--------|-------|
| Chart.js stacked bar | Modify | Restyle with refined type color palette. Match chart background to `--color-bg-card` |
| Course filter pills | Modify | Use token-based chip styling: `--color-accent-soft` bg, `--border-thin`, press effect on toggle |
| Exam markers | Keep | Red diamonds on chart stay |
| Click-to-jump | Keep | Click bar to jump to that week |

### Onboarding Flow

| Component | Status | Notes |
|-----------|--------|-------|
| Drop zone | Modify | Restyle with tokens. Keep dashed border, refine hover shadow |
| Wizard cards | Modify | Restyle with `--border-heavy` + `--shadow-hard-accent`. Keep auto-typing effect |
| Semester date step | Modify | Restyle input + button with tokens |
| Analysis progress | Modify | Restyle status badges, progress bar with tokens |
| Review screen | Modify | Collapse confirmed items by default (show count: "12 items confirmed"). Surface uncertain items for attention. Single "Save all" primary CTA instead of dual buttons |
| Page selector | Modify | Restyle thumbnails and checkboxes with tokens |

### Settings Panel

| Component | Status | Notes |
|-----------|--------|-------|
| Side panel | Modify | Restyle with `--border-heavy` left border (right in RTL), `--shadow-hard-lg`. Reorganize sections logically |
| Course list | Modify | Keep editable list, restyle rows |
| Color picker | Modify | Replace floating swatch popup with a cleaner inline picker. Better visual for selected state |
| Semester start input | Modify | Restyle with token input styles |
| Language toggle | Modify | Match landing/auth toggle style |
| Calendar export | Modify | Restyle buttons with press effect |
| Account section | Modify | Restyle delete button as destructive (red accent) |

### Feedback Modal

| Component | Status | Notes |
|-----------|--------|-------|
| Star rating | Modify | Restyle with tokens. Keep 1-5 scale |
| Textarea | Modify | `2px solid var(--color-border-ink)` border, focus with `--shadow-focus` |
| Submit button | Modify | Press effect, `--color-accent` background |
| Success state | Modify | Restyle with tokens |

### Removed / Killed

| Component | Notes |
|-----------|-------|
| BRUTALIST LAYER override block | Remove entire block (lines 362-385). Integrate selective brutalism into base component styles via tokens |
| `body::before` noise texture | Remove if present |
| Old `:root` variables | Replace with full token system |
| Hardcoded colors outside tokens | Migrate to CSS variables |

## Semantic Color System

### Type Colors (new tokens)

Event type colors become part of the token system for consistency:

| Type | Hebrew | Token | Color | Usage |
|------|--------|-------|-------|-------|
| Exam | מבחן | `--color-type-exam` | `#8e44ad` (purple) | Exam badges, timeline markers |
| Task | מטלה | `--color-type-task` | `#e67e22` (warm orange) | Task badges, workload bars |
| Reading | קריאה | `--color-type-reading` | `#27ae60` (green) | Reading badges |
| Lecture | שיעור | `--color-type-lecture` | `#8e44ad` (purple) | Lecture badges |
| Practice | תרגול | `--color-type-practice` | `#16a085` (teal) | Practice badges |
| Quiz | בוחן | `--color-type-quiz` | `#c0392b` (red) | Quiz badges |
| Video | סרטון/צפייה | `--color-type-video` | `#2980b9` (blue) | Video badges |
| Presentation | פרזנטציה | `--color-type-presentation` | `#d35400` (deep orange) | Presentation badges |

### Course Color Palette (refined)

Replace the current high-saturation palette with one that harmonizes with the warm paper aesthetic:

```
#2d7d46  (forest green — was #27ae60)
#2a6ca3  (deep blue — was #2980b9)
#7b3fa0  (plum — was #8e44ad)
#c76b1e  (amber — was #e67e22)
#1a8a7a  (deep teal — was #16a085)
#3f51b5  (indigo — keep)
#b53a3a  (brick red — was #c0392b)
#9e7c1a  (dark gold — was #b8860b)
#1a9e8a  (jade — was #1abc9c)
#b54a1e  (rust — was #d35400)
```

Slightly desaturated, warmer undertones, better contrast on cream backgrounds.

## Key Interactions

### Focus View
- **Task completion**: Click checkbox → check animation (scale bounce via `--ease-bounce`, 200ms) → item opacity drops to 0.5, text color becomes `--color-text-muted`, subtle slide-down. Progress indicator updates (e.g., ring fills, "4/7" counter increments). Item stays in list but visually recedes.
- **Inline add**: Click "+" row → input appears in-place with focus. Type description, hit Enter to add with smart defaults (current course context, current week, type inferred from section). Tab to set optional fields. Escape to cancel.
- **Add modal**: Click "..." or "more options" on inline add → modal with: course dropdown (populated from user's courses), type selector (tag chips), date picker, week number, description textarea. Primary CTA "Add" with press effect.
- **Week navigation**: Arrow buttons cycle weeks. Current week highlighted. Week range displayed as "Week 5: Mar 15-21".
- **Item delete**: Click delete → item fades out (200ms opacity transition) → removed from data → `save()`.

### Timeline View
- **Scroll**: Vertical scroll through semester. Month headers sticky. Items colored by urgency.
- **Jump**: Click any item → switches to Focus view at that week.
- **Urgency tiers**: Past items grey/muted. ≤3 days: red/warm left border. ≤7 days: orange. ≤14 days: amber. >14 days: neutral.

### Workload View
- **Filter**: Click course pills to toggle visibility. Active pills have `--shadow-hard-sm`, inactive are muted.
- **Hover**: Tooltip shows week details (item count by type + exam warnings).
- **Jump**: Click bar → switches to Focus view at that week.

### Onboarding Review (simplified)
- **Default state**: Uncertain items expanded (full detail, editable). Confirmed items collapsed into a summary line: "12 items confirmed ✓" with expand toggle.
- **Confirm uncertain item**: Click "✓ Correct" → item moves to confirmed group, counter updates.
- **Edit**: Inline edit for description and week number. No modal.
- **Save**: Single primary CTA "Save & go to dashboard" at bottom. No dual-button confusion.

### Settings Panel
- **Open**: Slides in from right (RTL) / left (LTR) with `--shadow-hard-lg`.
- **Color picker**: Click course color dot → inline swatch row expands below the course row (not a floating popup). Selected swatch gets `--border-structural` ring.
- **Close**: Click outside or X button. Slide out animation.

### Completion Animation Spec
- Checkbox fills with `--color-success` background
- Checkmark draws in (SVG stroke animation, 300ms)
- Item text transitions to `--color-text-muted` (200ms)
- Item opacity to 0.5 (200ms, 100ms delay)
- Progress indicator increments simultaneously
- All animations respect `prefers-reduced-motion` (instant state change, no animation)

## Responsive Behavior

- **Breakpoint**: 768px (tablet) and 375px (mobile). Consistent with landing/auth.
- **Desktop (>768px)**: Focus view uses comfortable single-column layout with max-width. Settings panel overlays from side. Workload chart full-width.
- **Tablet (768px)**: Same layout, reduced padding. Settings panel full-width overlay.
- **Mobile (≤375px)**: Full-width everything. Top bar simplifies (collapse user info). View switcher stays accessible. Add modal goes full-screen. Week navigation uses swipe gestures if feasible, otherwise arrows. Touch targets ≥44px.
- **Onboarding**: Drop zone full-width. Wizard card full-width. Review screen full-screen on mobile (already has `@media 520px` for this).

## Accessibility Requirements

- **Contrast**: All text meets WCAG AA (4.5:1 body, 3:1 large text). Urgency colors verified against `--color-bg` and `--color-bg-card`.
- **Keyboard**: All interactive elements keyboard-accessible. Tab order: top bar → view switcher → main content → add rows → settings. Focus trapped in modals/settings when open. Escape closes overlays.
- **Screen readers**: Progress indicators announced via `aria-live`. Task completion state communicated via `aria-checked`. View switcher uses `role="tablist"` / `role="tab"`. Add modal uses `role="dialog"` with `aria-labelledby`.
- **RTL**: Full bidirectional support. Settings panel direction flips. Timeline layout works in both directions. Chart labels render correctly in Hebrew.
- **Motion**: `prefers-reduced-motion` disables all animations (check animation, fade transitions, slide-in panels). State changes happen instantly.
- **Color**: Urgency is not communicated by color alone — text labels ("3 days", "passed") supplement the color coding.

## Out of Scope

- **Landing page** (`index.html`) — already redesigned
- **Auth page** (`auth.html`) — already redesigned
- **New Supabase tables or edge functions** — no backend changes
- **PDF analysis pipeline** — AI behavior unchanged
- **Onboarding flow structure** — drop → wizard → analyze → review → save stays the same
- **Payment/Stripe** — disabled for pilot
- **New features** (notifications, calendar sync, multi-device) — future work
- **Dark mode** — tokens are defined but implementation deferred
- **Chart.js library swap** — keep Chart.js v4, just restyle
