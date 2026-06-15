# Build Tasks: Dashboard Redesign

Generated from: .design/dashboard-redesign/DESIGN_BRIEF.md
Tokens: .design/landing-auth-redesign/DESIGN_TOKENS.css
IA: .design/dashboard-redesign/INFORMATION_ARCHITECTURE.md
Date: 2026-06-13

## Foundation

- [x] **1. Token integration + page cleanup (dashboard.html)**: Replace `:root` block (lines 16-20) with the full token system from DESIGN_TOKENS.css. Add dashboard-specific tokens: type colors (`--color-type-exam`, `--color-type-task`, `--color-type-reading`, `--color-type-lecture`, `--color-type-practice`, `--color-type-quiz`, `--color-type-video`, `--color-type-presentation`), urgency colors (`--color-urgency-critical`, `--color-urgency-soon`, `--color-urgency-ok`), and the refined 10-color course palette as `--course-color-1` through `--course-color-10`. Remove `body::before` noise texture (line 23). Remove entire `/* BRUTALIST LAYER */` block (lines 362-385). Migrate all old token refs: `--bg` → `--color-bg`, `--card` → `--color-bg-card`, `--text` → `--color-text`, `--sans` → `--font-body`, `--display` → `--font-display`, `--red/--orange/--green` → status tokens, `--exam/--task/--syllabus` → type tokens. Update `COLOR_PALETTE` array in JS (line 636) to the refined palette. Update `WL_TYPE_COLORS` object (line ~2590) to use the new type color values. _Modifies: `:root`, `body`, brutalist layer, JS color constants._

- [x] **2. Display font + heading rules**: Update the heading selector (line 22: `.ob-logo, .ob-title, .rv-title, .dash-title, #week-title, .sp-title`) to use `var(--font-display)` and `var(--weight-black)`. Apply `var(--tracking-tight)` to display headings. Ensure all `font-family: var(--sans)` refs become `var(--font-body)` and `font-family: var(--display)` refs become `var(--font-display)`. _Modifies: heading rule, font references throughout CSS._

## Core UI — Dashboard Chrome

- [x] **3. Top bar redesign**: Restyle `.top-bar` with `var(--color-bg-card)` background, `var(--border-structural)` bottom border, no `box-shadow` (kill soft shadow). Add logo `Sylla<span>Bot</span>` linking to `index.html` at the start. Restyle `.btn-sm` buttons (settings, logout) with `var(--border-structural)` + press effect. Restyle `.sync-dot` colors to use `var(--color-success)` / `var(--color-warning)` / `var(--color-error)`. Restyle `.user-name` and `#date-display` with token typography/colors (kill hardcoded `#636e72`, `box-shadow`). _Modifies: `.top-bar`, `.btn-sm`, `.sync-dot`, `.user-name`, `#date-display`. Adds: logo element in HTML._

- [x] **4. View switcher redesign**: Replace `.view-switcher` pill bar with a tab bar using `var(--border-structural)` container, `var(--color-bg)` background. Restyle `.view-btn` tabs: active tab gets `var(--color-bg-card)` background + `2px solid var(--color-border-ink)` border + `var(--shadow-hard-sm)`. Replace emoji labels (📋⏱️📊) with text labels from i18n. Add `role="tablist"` to container and `role="tab"` + `aria-selected` to each button. _Modifies: `.view-switcher`, `.view-btn`. Modifies: view switcher HTML._

## Core UI — Focus View

- [x] **5. Focus view layout — Upcoming Deadlines**: Replace the 3-column `.container` + `.box` layout with a single-column, max-width `var(--max-width-wide)` layout for Focus view. Create new "Upcoming Deadlines" section from the exams data. Add urgency tiers with colored `border-inline-start`: critical (≤3 days, `var(--color-error)`), soon (≤7 days, `var(--color-warning)`), upcoming (>7 days, `var(--color-border)`). Past items muted with `var(--color-text-muted)` + reduced opacity. Section container: `var(--color-bg-card)` background + `var(--border-structural)` + `var(--shadow-hard-md)`. Section header: `var(--font-display)` + `var(--weight-black)`. Add inline "+" add row at bottom with i18n. Keep existing exam delete functionality. _New section structure, modifies: `render()` function for exams rendering._

- [x] **6. Focus view layout — This Week section**: Create "This Week" section showing current week's syllabus items grouped by course. Header: week number + date range + progress indicator ("4/7 done" counter). Course subheadings with color dot. Items as checkboxes with course-colored left border. Week navigation arrows in header (keep existing `currentWeekIdx` logic). Add inline "+" add row at bottom. Progress indicator updates on completion. _New section structure, modifies: `render()` function for syllabus rendering, reuses existing week navigation logic._

- [x] **7. Focus view layout — Tasks section**: Create standalone "Tasks" section below This Week. Items from `userTasks[]` with checkboxes. No week grouping. Add inline "+" add row at bottom. Reuse existing task toggle (`userTasks[i].f`) and delete functionality. _New section structure, modifies: `render()` function for tasks rendering._

- [x] **8. Task completion animation**: Replace `.done` strikethrough (line 163) with: checkbox fills with `var(--color-success)` bg + SVG checkmark draws in (stroke animation, 300ms, `var(--ease-bounce)`). Item text transitions to `var(--color-text-muted)` + opacity 0.5 over 200ms. Add `.completing` transition class. Progress counter in This Week header updates simultaneously. All animations disabled under `prefers-reduced-motion`. Apply to both syllabus checkbox items and task checkbox items. _New CSS animations + modified JS for checkbox toggle._

- [x] **9. Inline add rows**: Add a "+" row at the bottom of each Focus section (Deadlines, This Week, Tasks). Click → input appears in-place with auto-focus. Enter submits with smart defaults (current week for This Week items, type inferred from section). Escape cancels, clears input. Style: `var(--color-text-muted)` text, `var(--border-thin)` top separator, input uses `2px solid var(--color-border-ink)` on focus. Add i18n keys for placeholder text. _New HTML + CSS + JS for inline add behavior. Modifies: `render()` to append add rows._

- [x] **10. Add Event modal**: New modal overlay triggered from inline add row "more options" link or a dedicated "+" button in top bar. Contains: course dropdown (populated from user's courses), type chip selector (single-select tag chips styled with type colors), description input, date picker, week number (auto-calculated from date via `semesterStart`). Style: `var(--border-heavy)` + `var(--shadow-hard-accent)` on modal card (same as auth card). Primary CTA "Add" with press effect. `role="dialog"` + `aria-labelledby` + focus trap + Escape to close. Add full i18n keys (HE + EN). _New HTML + CSS + JS. New i18n keys in STRINGS object._

## Core UI — Tag Badges + Item Rows

- [x] **11. Tag badge + item row restyling**: Restyle `.badge` / `.tag-*` classes: use type color tokens for backgrounds (tinted soft versions) and text. Apply `var(--border-thin)` to badges. Restyle `.item-row` with `var(--color-bg-card)` background, `var(--border-thin)` bottom separator instead of hardcoded `#f1f1f1`. Restyle `.timer` urgency badges to use status tokens (`var(--color-error-soft)` / `var(--color-warning-soft)` / `var(--color-success-soft)`). Restyle `.del-btn` with `var(--color-error)` color. Restyle `.course-label` to use course color from `courseColors` with `var(--font-body)`. Restyle `.empty-state` with token typography. _Modifies: all badge, item row, timer, and course label CSS._

## Core UI — Timeline View

- [x] **12. Timeline view restyling**: Restyle `#view-timeline` container with `var(--color-bg-card)` + `var(--border-structural)` + `var(--shadow-hard-md)`. Restyle `.tl-month-header` with `var(--font-display)` + `var(--tracking-wider)` + `var(--border-thin)` bottom. Restyle `.tl-item` hover to `var(--color-bg-secondary)`. Replace hardcoded urgency backgrounds (`.tl-urgent` `#fff5f5`, `.tl-soon` `#fffbf0`) with `var(--color-error-soft)` and `var(--color-warning-soft)`. Restyle `.tl-days-badge` urgency variants with status tokens. Restyle `.tl-date-col` and `.tl-title` with token typography. All hardcoded colors → CSS variables. _Modifies: all timeline CSS classes._

## Core UI — Workload View

- [x] **13. Workload view restyling**: Restyle `.wl-card` with `var(--color-bg-card)` + `var(--border-structural)` + `var(--shadow-hard-md)`. Restyle `.wl-title` with `var(--font-display)` + `var(--weight-black)`. Restyle `.wl-pill` filter chips: active state gets `var(--border-structural)` + `var(--shadow-hard-sm)`, inactive gets `var(--border-thin)` + muted opacity. Restyle `.wl-filter-label` with token typography. Update `WL_TYPE_COLORS` references in `renderWorkload()` to use the new type color values from task 1. Ensure chart background matches `var(--color-bg-card)`. _Modifies: all workload CSS classes, `renderWorkload()` JS._

## Core UI — Onboarding

- [x] **14. Onboarding restyling**: Restyle `.ob-card` with `var(--border-heavy)` + `var(--shadow-hard-accent)`. Restyle `.drop-zone` with `2.5px dashed var(--color-border-ink)`, hover shadow `var(--shadow-hard-sm)` with success tint. Restyle `.ob-cta` and wizard nav buttons with `var(--border-structural)` + press effect. Restyle wizard progress dots, file status badges, and progress bar with token colors. Restyle `.file-course-input` with `2px solid var(--color-border-ink)` + `var(--shadow-focus)` on focus. Restyle page selector thumbnails with `var(--border-thin)`, selected state with `var(--border-structural)`. All hardcoded colors → CSS variables. _Modifies: all onboarding CSS (lines 31-106)._

- [x] **15. Review screen simplification**: Modify `showReviewScreen()` and `renderReviewUI()` to: (a) default-collapse confirmed items into a summary line ("18 items confirmed ✓") with an expand/collapse toggle, (b) show uncertain items expanded and editable by default. Replace the dual save buttons (`.rv-btn-all` + `.rv-btn-confirmed`) with a single primary CTA "Save & go to dashboard". Restyle `.rv-course-group` with `var(--border-structural)` + `var(--shadow-hard-sm)`. Restyle `.rv-card` and `.rv-compact-item` with `var(--border-thin)` + type-colored `border-inline-start`. Add i18n keys for "X items confirmed", expand/collapse labels. _Modifies: review HTML structure, `showReviewScreen()`, `renderReviewUI()`, `rvCourseGroupsHtml()`, `confirmReview()`. Removes: `.rv-btn-confirmed`._

## Core UI — Settings Panel

- [x] **16. Settings panel restyling + reorg**: Restyle `#settings-panel` with `var(--border-heavy)` inline-start border + `var(--shadow-hard-lg)`. Background: `var(--color-bg-card)`. Reorganize sections in order: My Courses, Semester, Language, Calendar, Account. Restyle `.sp-title` with `var(--font-display)`. Restyle all inputs with `2px solid var(--color-border-ink)` + `var(--shadow-focus)`. Restyle `.sp-save-btn` and other buttons with press effect. Restyle account delete button with `var(--color-error)` accent. Replace floating color picker popup (`#sp-color-picker`) with inline swatch row that expands below the clicked course row — selected swatch gets `var(--border-structural)` ring. All hardcoded colors → CSS variables. _Modifies: settings panel CSS + HTML structure, color picker JS (`openColorPicker`, `pickColor`)._

## Core UI — Feedback Modal

- [x] **17. Feedback modal restyling**: Restyle `#feedback-btn` FAB with `var(--border-structural)` + `var(--shadow-hard-md)` + press effect. Restyle `#feedback-modal` with `var(--border-heavy)` + `var(--shadow-hard-accent)`. Restyle star rating with token colors. Restyle `#feedback-text` textarea with `2px solid var(--color-border-ink)` + `var(--shadow-focus)`. Restyle `.fb-submit` with `var(--color-accent)` bg + press effect. Restyle overlay with `var(--color-overlay)`. _Modifies: all feedback CSS (lines 291-315)._

## Responsive & Polish

- [x] **18. Responsive pass**: Verify dashboard at 768px and 375px breakpoints. Focus view: single column stays, padding reduces. Top bar: collapse user info on mobile, keep view switcher + settings accessible. Add Event modal: full-width on mobile. Settings panel: full-width overlay on mobile. Review screen: already has 520px breakpoint — extend to 375px. Workload chart: reduce padding, ensure touch targets on filter pills (≥44px). Timeline: full-width, reduce padding. Touch targets ≥44px for all interactive elements. Fix any RTL layout breakage at mobile widths. _Modifies/adds: `@media` queries throughout._

- [x] **19. Accessibility + final QA**: Add `role="tablist"` / `role="tab"` / `aria-selected` to view switcher (if not done in task 4). Add `role="dialog"` + `aria-labelledby` + focus trap to Add Event modal + feedback modal + settings panel. Add `aria-live="polite"` to progress indicators (This Week counter, analysis progress). Add `aria-checked` to task/syllabus checkboxes. Verify terracotta contrast for small text (use `var(--color-accent-text)` where needed). Add `prefers-reduced-motion` media query to disable all animations (completion, slide-in panels, fade transitions). Keyboard-test: tab through top bar → view switcher → main content → add rows → FAB. Escape closes all overlays. Verify RTL (Hebrew) and LTR (English). Run `node --check` equivalent on all inline `<script>` blocks. _Modifies: both CSS + HTML attributes throughout._

## Review

- [ ] **20. Design review**: Run /design-review against the brief.
