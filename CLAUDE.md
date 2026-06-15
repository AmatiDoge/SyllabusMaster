# SyllabusMaster (SyllaBot)

## Project Overview
SyllaBot is an AI-powered academic dashboard for students. It parses course syllabi (PDFs) using the Anthropic API and displays a unified weekly schedule, exams, and deadlines in a clean dashboard.

## Tech Stack
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Auth & Database:** Supabase (project ref: `uukpuvizkjgcssmlqltk`)
- **Payments:** Stripe
- **AI:** Anthropic API (PDF syllabus analysis)
- **Hosting:** GitHub Pages

## Key Files
| File | Purpose |
|------|---------|
| `index.html` | Landing page |
| `auth.html` | Login / signup |
| `dashboard.html` | Main app (schedule, exams, courses) |

## Supabase
- **Project ref:** `uukpuvizkjgcssmlqltk`
- Edge functions live locally at `~/Developer/Syllabot/syllabus-functions/`

| Function | Purpose |
|----------|---------|
| `analyze-syllabus` | Parse uploaded PDF with Anthropic API |
| `create-checkout` | Create Stripe checkout session |
| `confirm-payment` | Confirm Stripe payment and unlock premium |
| `billing-portal` | Open Stripe billing portal for the user |

### Deploying Edge Functions
Always deploy with the `--no-verify-jwt` flag:
```bash
supabase functions deploy <function-name> --project-ref uukpuvizkjgcssmlqltk --no-verify-jwt
```

## Git Workflow
Always commit and push after making changes:
```bash
git add -A && git commit -m "<message>" && git push
```

## Local Development
Start the dev server on port 3000:
```bash
npx serve .
# → http://localhost:3000
```

## Academic Calendar
- **Semester start:** 2026-03-15
- **Duration:** 14 weeks
- **Passover break:** Week 3 (no classes)

Week numbers are calculated relative to the semester start date, skipping the Passover break week.

## Course Colors
Course colors are stored in the `courseColors` object in `dashboard.html` and persisted to the `course_colors` column in Supabase. When adding or modifying color logic, keep both in sync.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec
