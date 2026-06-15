# Information Architecture: Dashboard Redesign

Generated from: .design/dashboard-redesign/DESIGN_BRIEF.md
Date: 2026-06-13

## Page States

The dashboard is a single-page app with two major modes and several overlay states:

```
dashboard.html
├── [1] Auth Loading        → spinner, checks session
├── [2] Onboarding Mode     → shown if no user data exists
│   ├── Drop Zone           → upload PDFs
│   ├── Wizard              → name each course + optional page selector
│   ├── Semester Date       → set start date
│   ├── Analysis            → AI processing with progress
│   └── Review              → confirm/edit/delete parsed items
└── [3] Dashboard Mode      → shown after onboarding complete or data exists
    ├── Top Bar             → always visible
    ├── Focus View          → default active view
    ├── Timeline View       → hidden until selected
    ├── Workload View       → hidden until selected
    ├── [overlay] Settings Panel    → slides in from edge
    ├── [overlay] Add Event Modal   → centered modal
    └── [overlay] Feedback Modal    → centered modal
```

## View Architecture

### Top Bar (persistent across all views)

```
┌─────────────────────────────────────────────────────────────────┐
│  SyllaBot    [Focus] [Timeline] [Workload]     ⚙ Settings  👤  │
│              ───────                            sync●           │
│              active tab                                         │
└─────────────────────────────────────────────────────────────────┘
```

**Elements:**
- Logo: `Sylla<span>Bot</span>` linking to index.html
- View switcher: 3 tabs with `role="tablist"`. Active tab has `--border-structural` + `--shadow-hard-sm`
- Settings gear button (opens settings panel)
- User display: first name or email truncated
- Sync status dot (green/orange/red)
- Feedback button (fixed position, bottom corner)

**Hierarchy:** View switcher is the primary interactive element. Settings and user info are secondary.

### Focus View (default)

The Focus view replaces the old 3-column layout with a single-column, priority-ordered layout.

```
┌─────────────────────────────────────────────────────────┐
│  TOP BAR                                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  UPCOMING DEADLINES                               │  │
│  │  Exams and deadlines sorted by urgency            │  │
│  │                                                   │  │
│  │  ┌─ critical (≤3 days) ────────────────────────┐  │  │
│  │  │ 🔴 Cognitive Psychology — Exam      2 days  │  │  │
│  │  └────────────────────────────────────────────  │  │  │
│  │  ┌─ soon (≤7 days) ───────────────────────────┐│  │  │
│  │  │ 🟠 Research Methods — Paper due     5 days  │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  ┌─ upcoming (>7 days) ───────────────────────┐│  │  │
│  │  │ ○  Statistics — Midterm             18 days │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  [+ Add deadline]                                 │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  THIS WEEK — Week 5: Mar 15–21        ‹ ●●●○○ ›  │  │
│  │                                          4/7 done │  │
│  │                                                   │  │
│  │  Cognitive Psychology                             │  │
│  │  ☑ Read chapter 4              ░░░ (done, muted)  │  │
│  │  ☐ Watch lecture recording                        │  │
│  │                                                   │  │
│  │  Research Methods                                 │  │
│  │  ☐ Practice exercise set 3                        │  │
│  │  ☐ Read methodology paper                         │  │
│  │                                                   │  │
│  │  [+ Add item to this week]                        │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  TASKS                                            │  │
│  │  Standalone tasks not tied to a specific week     │  │
│  │                                                   │  │
│  │  ☐ Register for next semester courses             │  │
│  │  ☑ Submit library card form        (done, muted)  │  │
│  │                                                   │  │
│  │  [+ Add task]                                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Section order (top to bottom):**

1. **Upcoming Deadlines** — Exams and deadline-type items, sorted by date ascending. Grouped visually by urgency tier:
   - Critical (≤3 days): warm red left border, `--color-error` accent
   - Soon (≤7 days): orange left border, `--color-warning` accent
   - Upcoming (>7 days): neutral, `--color-border` left border
   - Past: muted, `--color-text-muted`, pushed to bottom or hidden

2. **This Week** — Current week's syllabus items grouped by course. Header shows week number + date range + progress (e.g., "4/7 done"). Week navigation arrows to move between weeks. Completed items stay but visually recede (muted, reduced opacity).

3. **Tasks** — Standalone tasks (from `userTasks[]`). Checkboxes with completion animation. Not grouped by week.

Each section has an inline "+" add row at the bottom.

**Content priority:** Deadlines first (time-sensitive), then this week's work (actionable), then general tasks (backlog).

### Timeline View

```
┌─────────────────────────────────────────────────────────┐
│  TOP BAR                                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  MARCH 2026                          ── month header ── │
│  ┌─────────────────────────────────────────────────┐    │
│  │ ● Cognitive Psychology — Exam          Mar 20   │    │
│  │   Week 1                                        │    │
│  └─────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────┐    │
│  │ ● Research Methods — Paper due         Mar 25   │    │
│  │   Week 2                                        │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  APRIL 2026                          ── month header ── │
│  ┌─────────────────────────────────────────────────┐    │
│  │ ● Statistics — Midterm                 Apr 10   │    │
│  │   Week 4                                        │    │
│  └─────────────────────────────────────────────────┘    │
│  ...                                                    │
└─────────────────────────────────────────────────────────┘
```

**Structure:**
- Vertical chronological list
- Grouped by month (Hebrew locale month names)
- Sticky month headers with `--font-display`
- Each item shows: course color dot, course name, event type tag, date, week number
- Urgency indicated by left border color (same tiers as focus view)
- Past items muted (`opacity: 0.4`)
- Click item → switch to Focus view at that week

**Data source:** Combines `userExams[]` + syllabus items of type "מטלה" (tasks/assignments), sorted by date ascending.

### Workload View

```
┌─────────────────────────────────────────────────────────┐
│  TOP BAR                                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Course filters:                                        │
│  [Cog Psych ●] [Research ●] [Stats ●] [Linguistics ●]  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ██                                             │    │
│  │  ██ ██                          ◆ = exam        │    │
│  │  ██ ██    ██                                    │    │
│  │  ██ ██ ██ ██    ██ ██                           │    │
│  │  ██ ██ ██ ██ ██ ██ ██ ██                        │    │
│  │  ──────────────────────────────────────          │    │
│  │  W1 W2 W3 W4 W5 W6 W7 W8 W9 ...               │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Structure:**
- Course filter pills at top (toggle visibility per course)
- Chart.js stacked bar chart (items per week, colored by type)
- Red diamond markers for exam weeks
- Click bar → switch to Focus view at that week
- Tooltip on hover: item count breakdown by type + exam warnings

## Onboarding Flow

The onboarding is a linear wizard. Each step replaces the previous.

```
Step 1: Drop Zone
  "Upload your syllabus PDFs"
  [drag area] or [browse button]
  ↓ files selected

Step 2: Wizard (loops per file)
  "Name this course" — file 1 of 3
  [course name input with auto-typing placeholder]
  [optional: select pages toggle → thumbnail grid]
  [← Prev] [Next →]
  ↓ all files named

Step 3: Semester Date
  "When does your semester start?"
  [date input, default 2026-03-15]
  [Continue →]
  ↓ date set

Step 4: Analysis
  File list with live status:
  ├── cognitive-psych.pdf  ✓ Done — 8 items found
  ├── research-methods.pdf ◌ Analyzing...
  └── statistics.pdf       ○ Waiting
  [progress bar: 1/3 complete]
  ↓ all files analyzed

Step 5: Review
  ┌─────────────────────────────────────────┐
  │  Review Your Schedule                   │
  │  24 items · 18 confirmed · 6 uncertain  │
  │                                         │
  │  ⚠ NEEDS ATTENTION (6 items)           │
  │  ┌─ Cognitive Psychology ──────────┐    │
  │  │ ☐ "Exam" — Week ?? — Edit/Del  │    │
  │  │ ☐ "Reading" — Week 3 — Edit    │    │
  │  └─────────────────────────────────┘    │
  │                                         │
  │  ✓ CONFIRMED (18 items)        [expand] │
  │    12 syllabus items, 6 exams           │
  │                                         │
  │  [Save & go to dashboard]               │
  └─────────────────────────────────────────┘
```

**Review screen changes (from brief):**
- Uncertain items (confidence < 80%) expanded by default, editable
- Confirmed items collapsed into summary: "18 items confirmed ✓" with expand toggle
- Single primary CTA: "Save & go to dashboard"
- Remove the dual-button (save confirmed only / save all) pattern

## Overlays

### Settings Panel

Slides in from the inline-end edge (right in RTL, left in LTR). Covers ~360px width on desktop, full-width on mobile.

```
┌──────────────────────────────┐
│  Settings                  ✕ │
│  ─────────────────────────── │
│                              │
│  MY COURSES                  │
│  ┌────────────────────────┐  │
│  │ ● Cognitive Psychology │  │ ← click dot for color picker
│  │   [inline swatch row]  │  │ ← expands below when dot clicked
│  │ ● Research Methods     │  │
│  │ ● Statistics           │  │
│  └────────────────────────┘  │
│                              │
│  SEMESTER                    │
│  Start date: [2026-03-15]    │
│                              │
│  LANGUAGE                    │
│  [עברית ▾]                   │
│                              │
│  CALENDAR                    │
│  [Download .ics]             │
│  [Copy subscription link]    │
│                              │
│  ACCOUNT                     │
│  [Delete account]  ← red     │
│                              │
└──────────────────────────────┘
```

**Section order (by frequency of use):**
1. My Courses (most interactive — color changes)
2. Semester (set once, rarely changed)
3. Language (set once)
4. Calendar (occasional export)
5. Account (destructive, bottom)

**Color picker change:** Instead of a floating popup, clicking a course color dot expands an inline swatch row directly below that course row. Selected swatch gets a `--border-structural` ring. Click another dot → previous one collapses, new one expands.

### Add Event Modal

```
┌──────────────────────────────────┐
│  Add Event                    ✕  │
│  ─────────────────────────────── │
│                                  │
│  Course                          │
│  [▾ Select course          ]     │
│                                  │
│  Type                            │
│  [Exam] [Task] [Reading] [Quiz]  │  ← chip selector, single select
│  [Lecture] [Video] [Practice]    │
│                                  │
│  Description                     │
│  [                          ]    │
│                                  │
│  Date            Week            │
│  [YYYY-MM-DD]    [auto / ##]     │  ← week auto-calculates from date
│                                  │
│  [Add Event]                     │
└──────────────────────────────────┘
```

**Behavior:**
- Course dropdown populated from user's existing courses
- Type is a chip/tag selector (single select). Visual style matches tag badges in the dashboard
- Week auto-calculates from date based on semester start. Can be overridden manually
- "Add Event" is primary CTA with press effect
- Modal closes on success, item appears in relevant view
- Keyboard: Enter submits, Escape closes, Tab navigates fields

### Feedback Modal

```
┌──────────────────────────────────┐
│  How's SyllaBot working?     ✕   │
│  Your feedback helps improve it  │
│                                  │
│  ☆ ☆ ☆ ☆ ☆                      │
│                                  │
│  [Tell us more...            ]   │
│  [                           ]   │
│                                  │
│  ☐ I'm open to a short chat     │
│                                  │
│  [Send Feedback]                 │
└──────────────────────────────────┘
```

No structural changes. Restyle only.

## Navigation Map

```
                    ┌─────────────┐
                    │  auth.html  │
                    └──────┬──────┘
                           │ login success
                           ▼
              ┌────────────────────────┐
              │    dashboard.html      │
              │    (auth loading)      │
              └────────┬───────────────┘
                       │
          ┌────────────┼────────────────┐
          │ no data    │ has data       │
          ▼            ▼                │
    ┌──────────┐  ┌──────────┐          │
    │Onboarding│  │ Focus    │◄─────┐   │
    │  Flow    │  │ View     │      │   │
    └────┬─────┘  └────┬─────┘      │   │
         │             │            │   │
         │ save        │ tab switch │   │
         │             ▼            │   │
         │        ┌──────────┐     │   │
         └───────►│ Timeline │─────┤   │
                  │ View     │click│   │
                  └────┬─────┘ item│   │
                       │            │   │
                       │ tab switch │   │
                       ▼            │   │
                  ┌──────────┐     │   │
                  │ Workload │─────┘   │
                  │ View     │click    │
                  └──────────┘ bar     │
                                       │
    Overlays (accessible from any view):
    ├── Settings Panel (gear icon)
    ├── Add Event Modal (+ buttons)
    └── Feedback Modal (FAB button)
```

## Data Flow

```
Supabase user_data
  │
  ├── tasks[]        → Tasks section (Focus), inline editable
  ├── exams[]        → Upcoming Deadlines (Focus), Timeline, Workload markers
  ├── syllabus[]     → This Week (Focus), Timeline, Workload bars
  ├── done_map{}     → Completion state for syllabus items
  ├── course_colors{}→ Color dots everywhere, Settings color picker
  ├── semester_start → Week calculation, week navigation
  ├── rev            → Optimistic concurrency lock
  ├── ics_token      → Calendar subscription URL
  └── preferred_view → Remembered last active view tab

  All mutations go through:
  save() → debounce 800ms → saveToSupabase() → upsert with rev check
```

## Keyboard Navigation Order

```
Tab order (Focus view):
1. Logo (link to index.html)
2. View switcher tabs (Focus → Timeline → Workload)
3. Settings button
4. Upcoming Deadlines items (each item focusable for delete)
5. Deadline inline add row
6. This Week navigation arrows
7. This Week items (checkboxes)
8. This Week inline add row
9. Tasks items (checkboxes)
10. Tasks inline add row
11. Feedback FAB

When overlay is open:
- Focus trapped inside overlay
- Escape closes overlay
- Tab cycles through overlay controls only
```

## RTL Considerations

| Element | RTL (Hebrew) | LTR (English) |
|---------|-------------|---------------|
| Settings panel | Slides from right | Slides from left |
| Week nav arrows | ‹ = forward, › = back | › = forward, ‹ = back |
| Urgency left border | Becomes right border (inline-start) | Left border |
| Course color dot | Right side of name | Left side of name |
| Progress text | "4/7 הושלמו" | "4/7 done" |
| Tag badges | Same position (inline) | Same position (inline) |
| Chart labels | Right-aligned | Left-aligned |
| Add row "+" | Right-aligned | Left-aligned |
| Modal close "✕" | Top-left | Top-right |
