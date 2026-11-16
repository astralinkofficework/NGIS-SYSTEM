# NGIS-SYSTEM — Master Global Urgency, Deadline & Action Color Audit Report

Date: 2026-11-16 · Scope: status/deadline/urgency color semantics across all four portals

---

## 1. Status & color systems discovered

- **Token source of truth**: `assets/css/design-tokens.css` — semantic status tokens existed (`--token-status-*`, `--color-danger/warning/info`, tint triads) but with off-spec values (danger `#DC2626`, warning `#D97706`, info `#0284C7`).
- **Badge normalizer**: `layout.js` auto-maps status text → `badge-danger/warning/success` classes; badge colors resolve via tokens (auto-corrected once tokens changed).
- **Legacy badge CSS**: `app.css` `.badge.blue`/`.badge.info` mapped to brand *green*; `interactions.css` (admin) hardcoded `#B91C1C`/`#DC2626`/`#0369A1`.
- **Per-page hardcodes**: three competing "danger" reds in active use (`#DC2626`, `#B91C1C`, `#e11d48`) plus Tailwind `rose/amber/emerald` hue classes.

## 2. Root causes of inconsistency

1. No central urgency *classification* — deadline math (overdue? late allowed? already submitted?) existed nowhere in JS; urgency was hardcoded per page from label text.
2. Token values drifted from page-local hexes and Tailwind defaults.
3. Status → color mapping was duplicated per renderer (e.g. `assignments-api.js` colored "late" **blue**).

## 3. Shared system introduced (Phase 2/4/7)

| File | Role |
|---|---|
| `assets/css/design-tokens.css` | Spec palette: red `#DC3545`, orange `#F28C28` (= brand Warm Orange), green `#176B45`, blue `#2563EB`; darker `*-text` shades (`#B02A37`, `#B45309`, `#1D4ED8`) for WCAG text contrast; new `--state-*` urgency token layer |
| `assets/css/semantic-states.css` (new) | `.ngis-state--*` indicators, `.ngis-state-chip--*` tint chips, `.ngis-dot--*` deadline dots, `.ngis-btn-urgent` (solid red) / `.ngis-btn-warning` (solid orange) buttons — solid fill, white text, no border/overlay/shadow, `:focus-visible` preserved, disabled states. Fixes `.badge.blue`→real blue. Safety net: a `complete` record can never show an urgent button |
| `assets/js/semantic-states.js` (new) | `NGISStates.classify({status, dueDate, lateAllowed, actionDone, actionable}, {urgentHours:6, warnHours:24})` → `overdue | urgent | approaching | normal | complete | closed`. ONE deadline calculation; per-module thresholds; "late" = *submitted late* → complete (never urgent); local-time ISO parsing |
| `assets/js/layout.js` (+ root sync) | Injects semantic-states.css + semantic-states.js into every portal (alongside ui-states/action-icons) |

## 4. Files modified (per finding)

**Student portal**
- `student-assignments.html` — status colors now token-driven; overdue due-date/penalty text green→red; late-note icon neutral→red; **Late Submission button → red**, Due-Tomorrow **Upload → orange**, normal Upload stays black; new `applyCardUrgency()` derives decoration from each card's `data-due`/`data-submitted` record attributes via `NGISStates` (not label text).
- `js/assignments-api.js` — live renderer now classifier-driven: "late" no longer blue; overdue pending → red "Late Submission" button; approaching → orange; normal submit → brand green; graded → `#176B45`.
- `js/live-dashboard.js` — assessment deadline dots computed from real `due_date` (red/orange/green/neutral) instead of constant rose.
- `student.html` — attendance legend Present=green/**Absent=red/Late=orange** (was all-green); "Upcoming" exam tag red→blue (future item was wrongly urgent); feed tags/dots unified to tokens; notification badge + LIVE dot rose→`#DC3545`.
- `student-lost-found.html` — removed `error:#176B45` green remap (→`#DC3545`); LOST badges green→orange (open case), "Pending Review" chips → warning tokens.

**Teacher portal**
- `teacher-submissions.html` — "Late / Overdue" KPI **green→red** (label/dot/value/penalty note); "Awaiting Evaluation" dot green→orange; badges: Late=orange, Missing=red (was green!), Graded=green, Submitted=blue; drawer penalty badge + "Overdue n days" timestamp colored by status field.
- `teacher-attendance.html` — state cycle Present=green/**Late=orange/Absent=red** (was all-green), Excused=neutral.
- `teacher.html` — deadline dots: "Due Today" green→red, "Soon" →orange, "Upcoming" →blue info, "On track"/"Prepare" →neutral.

**Admin / Principal**
- `admin-assignments.html` via `semantic-states.css` — `.badge.blue` Published/Graded are now distinguishable (blue vs green).
- `admin-attendance.html`, `admin-lost-found.html`, `admin-services.html`, `admin-departments.html`, `admin-news.html` — rose `#e11d48`/`#DC2626` destructive accents → `var(--color-danger)`.
- `interactions.css` — admin badge hexes → tokens.
- `principal-attendance.html`, `assets/js/student-management.js`, `assets/js/teacher-management.js` — 444 Tailwind `rose/amber/emerald` status classes hue-mapped to token hexes (dark-mode variants untouched); reject-confirm button rose-600 → `#DC3545`.

**Shared**
- `assets/css/exams-simple.css`, `assets/css/ui-states.css` — local palettes re-pointed to tokens.
- `design-tokens.css`, `semantic-states.css/js`, `layout.js` as above.

## 5. Status transitions tested (browser, real classifier)

10/10 PASS: overdue+pending→overdue; late-allowed→overdue; **late window shut→closed (no urgent action)**; **submitted-late→complete (no misleading urgency)**; graded→complete; due in 3h→urgent(red); due in 20h→approaching(orange); due in 10d→normal; cancelled→closed; no date+no status→normal.

## 6. Browser results

- Assignments 1440px: Late Submission `rgb(220,53,69)`; Due-Tomorrow Upload `rgb(242,140,40)`; normal Uploads black; card states `approaching|overdue|normal|normal`.
- Teacher submissions badges rendered: Late `#B45309/#FEF0E3`, Graded `#176B45/#E8F3ED`, Submitted `#1D4ED8/#EAF1FE`, Missing `#B02A37/#FDECEC`; KPI `#DC3545`.
- Attendance matrix: P green / L orange / A red / E slate.
- Dashboard deadline dots: red/orange/green/blue as designed. Lost&Found LOST badge orange.
- Viewports 320/375/430/768/1024/1440/1920: **0 horizontal overflow** everywhere; mobile full-width urgent buttons readable (white on red/orange).
- Console: clean on 9 touched pages. Screenshots: `scratch/urgency-assignments-1440.png`, `urgency-assignments-375.png`, `urgency-teacher-submissions.png`.

## 7. Remaining issues (not blocking)

1. `assignments-api.js` is not currently referenced by any page (dormant renderer) — fixed for consistency but inactive.
2. Tailwind `emerald-*` decorative avatar/category accents in `student-management.js` now map to brand green; any place where a *category identity* color collides with status semantics (subject chips, `#d97706` category colors in `classes.js`, `subjects.js`) is documented but intentionally untouched — they are identity colors, not status.
3. `admin-student-verify.html`/queue pages verified for load + engine injection, but deep visual QA of every queue tab is recommended follow-up.
4. Server-side (`server.py`) sends `due_date` strings without timezone; classifier treats them as local school time (ICT, UTC+7). If multi-timezone support is added, centralize parsing in `NGISStates.parseDate`.
5. Dark theme: token `*-text-tint` dark overrides exist; spot-check dark mode for the new state chips in a follow-up pass.
