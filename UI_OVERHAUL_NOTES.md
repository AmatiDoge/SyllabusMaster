# UI Overhaul — 2026-06-11

A cohesive visual refresh across all three pages (landing → auth → dashboard), **design only — zero functional changes**. The existing warm "academic paper" identity was kept and elevated, not replaced.

## Design system (shared across all pages)
- **Display font:** `Frank Ruhl Libre` — an editorial Hebrew+Latin serif, used for headings, the SyllaBot logo, and big numbers. Gives the product a scholarly, premium, distinctive voice (vs. the previous generic sans).
- **Body/UI font:** `Rubik` — geometric, friendly, full Hebrew support; replaces Heebo as the default UI face (Heebo kept as fallback).
- **Palette:** warm cream paper `#f4f1ea`, warm ink `#1b1714`/`#2b2622`, deeper terracotta accent `#df4a22`. Tokens: `--sans`, `--display`, `--shadow-sm/md/lg`, `--accent-soft`, `--border-strong`.
- **Depth:** softer, larger layered shadows; hover lift on cards/buttons; refined focus states.

## What changed per page
- **index.html** — serif hero headline + stats, enriched palette, demo card depth, step-card hover lift, button shadow. All `data-i18n`, ids, classes, onclick handlers untouched.
- **auth.html** — same tokens; serif logo; tokenized font usage. Forms/tabs/Google/legal modals unchanged in behavior.
- **dashboard.html** — **CSS-only**. Font link + `:root` tokens + body font + serif on headings (`.ob-title`, `.rv-title`, `.dash-title`, `#week-title`, `.sp-title`, `.ob-logo`). Semantic course colors (`--exam`/`--task`/`--syllabus`) left intact. No JS touched.

## Verification (all passed)
- `node --check` clean on every inline `<script>` block in dashboard.html (the ~2,800-line file).
- No console errors on landing, auth, or onboarding.
- Screenshotted desktop + mobile (375px); RTL (he) and LTR (en) both verified.
- All `getElementById`/class hooks referenced by JS confirmed present after edits.

## Progress
- [x] landing  [x] auth  [x] dashboard  [x] verification  [x] shipped to main

## Preview locally
`python3 -m http.server 4180 --directory .` → http://localhost:4180

## Ship (already done on this branch's merge)
`git checkout main && git merge ui-overhaul && git push origin main`
