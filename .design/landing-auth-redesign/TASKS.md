# Build Tasks: Landing + Auth Redesign

Generated from: .design/landing-auth-redesign/DESIGN_BRIEF.md
Tokens: .design/landing-auth-redesign/DESIGN_TOKENS.css
Date: 2026-06-12

## Foundation

- [x] **1. Token integration + page cleanup (index.html)**: Replace the existing `:root` block with the new design tokens from DESIGN_TOKENS.css. Remove the `body::before` noise texture overlay, the dot-grid from `background-image`, and the floating gradient circles (`.hero-bg-circle` CSS + HTML). Body background becomes plain `var(--color-bg)`. Remove the entire `/* BRUTALIST LAYER */` CSS block if one exists (landing had inline brutalist overrides in step/feature styles). Keep Google Fonts link unchanged. _Modifies: index.html `:root` and `body` styles._

## Core UI — Landing Page

- [x] **2. Nav bar**: Solid `var(--color-bg)` background with `var(--border-thin)` bottom border. Kill `backdrop-filter: blur()` glassmorphism. Logo stays (`Sylla<span>Bot</span>`), lang toggle stays, nav CTA becomes a link to `auth.html` (not `onclick` opening a modal). Style CTA with `var(--border-structural)` + `var(--shadow-press-rest)` + press effect on hover. Pilot banner above nav: simplify to plain dark bar, remove any hard shadow. _Modifies: nav, `.nav-cta`, `.logo`, `#pilot-banner` CSS + HTML._

- [x] **3. Hero section**: Strip to: display headline (Frank Ruhl Libre, `var(--text-4xl)`, `var(--weight-black)`) + subtitle (`var(--text-lg)`, `var(--color-text-muted)`) + single primary CTA button linking to `auth.html`. Kill: `.hero-label` chip, `.hero-stats` bar, `.btn-ghost` "how it works" button, `.hero-bg-circle` elements (HTML), `fadeUp` stagger delays on removed elements. Keep `fadeUp` animation on headline + subtitle + CTA. Highlight span on key word stays with terracotta underline. _Modifies: `.hero`, `h1`, `.hero-sub`, `.hero-actions`. Removes: `.hero-label`, `.hero-stats`, `.stat-*`, `.btn-ghost` CSS + HTML._

- [x] **4. Product demo section**: Restyle the demo wrapper to light background (`var(--color-bg-card)`) with `var(--border-heavy)` + `var(--shadow-hard-lg)`. Remove dark theme (currently `background: var(--ink)`). Keep 3-column card layout with real Hebrew course data. Restyle cards with subtle borders instead of dark translucent backgrounds. Remove the `.ai-badge` pulsing element (HTML + CSS). Remove the macOS dot topbar or simplify it. Mark this section with a code comment as `<!-- DEMO: placeholder — update when dashboard redesign is complete -->`. _Modifies: `.demo-wrapper`, `.demo-topbar`, `.demo-content`, `.demo-card`, badge styles. Removes: `.ai-badge` HTML + CSS._

- [x] **5. "Built by a student" section**: New section between demo and FAQ. Simple layout: centered, max-width `var(--max-width-content)`. Contains a short personal message (~2-3 sentences about who built SyllaBot and why), and a first name. Style with `var(--font-display)` for the heading, `var(--font-body)` for body text. Add `var(--border-structural)` left/right border or a subtle card treatment to distinguish it. Add both HE and EN translations to the `T` object with new i18n keys (`aboutTitle`, `aboutBody`, `aboutName`). Add `data-i18n` attributes to elements. _New section + i18n entries._

- [x] **6. FAQ section**: Keep all 6 questions and the accordion behavior (JS untouched). Restyle: remove any brutalist overrides, use `var(--border-thin)` for item separators, `var(--font-display)` for section title, clean `faq-icon` with `var(--color-border-ink)` border. FAQ toggle interaction stays the same. Section label chip: use `var(--color-accent-soft)` bg + `var(--color-accent-text)` text + `var(--border-thin)` border. _Modifies: `.faq-section`, `.faq-item`, `.faq-q`, `.faq-icon`, `.faq-a`, `.section-label` CSS._

- [x] **7. CTA footer + page footer**: CTA section: keep terracotta background (`var(--color-accent)`), remove the oversized `::before` watermark text. Simplify to heading + one line + button. Button becomes white with `var(--border-heavy)` ink border + press effect. CTA links to `auth.html`. Footer: keep logo + copyright + tagline. Use `var(--border-thin)` top separator. _Modifies: `.cta-section`, `.btn-white`, `footer` CSS + HTML. Removes: `.cta-section::before`._

- [x] **8. Dead code removal (index.html)**: Remove all HTML, CSS, JS, and i18n keys for killed sections: "How it works" steps (`#how` section + `.steps`, `.step`, `.step-num`, `.step-icon` CSS + `step*` i18n keys), features grid (`.features-section` + `.features-grid`, `.feature`, `.feature-icon` CSS + `feat*` i18n keys), waitlist modal (if any modal HTML remains). Remove associated `reveal` observer targets that no longer exist. Keep the `IntersectionObserver` JS for remaining `.reveal` elements. Clean up unused CSS (`.btn-ghost`, gradient circle keyframes `float1`/`float2`, `.ai-badge` `pulse` keyframe). _Removes: ~200 lines of HTML, ~150 lines of CSS, ~30 i18n keys._

## Core UI — Auth Page

- [x] **9. Auth page redesign (auth.html)**: Replace `:root` with new design tokens. Remove: `body::before` noise texture, `.bg-circle` elements (HTML + CSS), entire `/* BRUTALIST LAYER */` override block. Restyle auth card with `var(--border-heavy)` + `var(--shadow-hard-accent)` (accent-colored hard shadow). Tabs: `var(--border-structural)` container, active tab with `var(--shadow-hard-sm)`. Inputs: `2px solid var(--color-border-ink)`, focus state with `var(--shadow-focus)`. Buttons: `var(--border-structural)` + press effect (`var(--shadow-press-rest)` → `var(--shadow-press-hover)` on hover). Primary button: `var(--color-accent)` background. Google button: white with ink border. Lang toggle: match landing nav style. Legal modals: `var(--border-heavy)` + `var(--shadow-hard-md)`. All existing JS behavior unchanged. _Modifies: all CSS in auth.html. Removes: brutalist layer, noise, circles._

## Responsive & Polish

- [x] **10. Responsive pass**: Verify both pages at 768px and 375px breakpoints. Landing: hero padding reduces, demo grid stacks to 1 column, FAQ/CTA padding shrinks, "built by a student" section padding adjusts. Auth: already single-column, verify card doesn't overflow at 375px, lang toggle doesn't overlap content. Fix any RTL layout breakage at mobile widths. _Modifies: `@media` queries in both files._

- [x] **11. Accessibility + final QA**: Verify terracotta contrast for small text (use `var(--color-accent-text)` where needed). Add `aria-expanded` to FAQ toggle buttons. Ensure all form labels in auth are properly associated. Add `prefers-reduced-motion` media query to disable `fadeUp` and press animations. Keyboard-test all interactive elements (tab through nav → hero CTA → FAQ toggles → CTA button; tab through auth form). Verify RTL (Hebrew) and LTR (English) on both pages. Run `node --check` on any inline `<script>` blocks. _Modifies: both files, CSS + HTML attributes._
