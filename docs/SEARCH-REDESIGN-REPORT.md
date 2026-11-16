# NGIS-SYSTEM — Master Search Bar UI/UX Audit & Redesign Report

**Date:** 2026-11-16
**Scope:** Every search bar / search input across all portals (Student, Teacher, Principal, Admin, Super Admin, Shared).
**Constraint honored:** No business logic changed; no new frameworks; no unrelated redesigns.

---

## 1. Root cause of the reported icon/placeholder overlap (`departments.html`)

The Academic Departments search box (and 16 other bars) used the fragile
**absolute-positioned Tailwind pattern**:

```html
<div class="relative ...">
  <span class="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 ...">search</span>
  <input class="... pl-10 pr-4 ...">
</div>
```

Overlap appears when the Material Symbols font is slow/unloaded: the span
renders the raw ligature text `search` (~45 px wide) inside an 18 px
absolute-positioned box, crossing into the input's 40 px padding. The layout
also depended on JS enhancement timing (`ngis-search.js`) and Tailwind CDN.

**Fix at source:** all raw bars were converted to the shared flexbox shell
`.ngis-search` directly in markup (icon → input → kbd/clear in flow order).
Overlap is now structurally impossible: the input is placed *after* the icon
box by flex, regardless of font/JS state.

## 2. Shared design system (`assets/css/ngis-search.css` + `assets/js/ngis-search.js`)

One token set drives global header, sidebar, and all page-level searches:

| Token | Value |
|---|---|
| `--ngis-search-bg` | `#FFFFFF` |
| `--ngis-search-border` | `1px solid #E1E9E3` |
| `--ngis-search-radius` | `10px` |
| `--ngis-search-height` | `44px` standard / `38px` compact |
| `--ngis-search-text` | `#29352E` |
| `--ngis-search-placeholder` | `#87958B` |
| `--ngis-search-icon` | 18px, `#6B7B71` |
| Horizontal padding / gap | `14px` / `10px` |

Dark theme tokens included. Enhancer adds: aria-labels, clear button
(`.ngis-search-clear`), `has-value` state, loading/disabled variants.

### CSS hardening done in this task
- **`:where(.ngis-search)` for `width`** (zero specificity) — page width
  utilities like `sm:w-56` / `max-w-md` always win; fixes latent width override.
- **Icon `overflow: hidden` + `white-space: nowrap`** — slow-loading icon fonts
  can never spill into the input.
- **Native WebKit search-cancel glyph hidden** — prevents duplicate clear
  buttons next to the shared `.ngis-search-clear`.
- **Placeholder `!important`** — `design-system.css:787` forces
  `input::placeholder { color:#8FA095 !important }` globally; the scoped token
  rule now legitimately outranks it (incl. dark mode).

## 3. Pages converted from raw absolute pattern to shared flex shell (17 bars / 14 files)

| Page | Input(s) | Extras preserved |
|---|---|---|
| `shared/departments.html` | `#dept-search` | — |
| `student/student-assignments.html` | `#asgnSearch` | `sm:w-56` width |
| `admin/admin-absence-stats.html` | `#tableSearchInput` | page clear btn `#searchClearBtn` |
| `admin/admin-attendance.html` | `#searchFilter` | `oninput="applyFilters()"` |
| `principal/principal-activity.html` | `#searchInput` | legacy inline `padding-left:44px!important` removed |
| `principal/principal-lost-found.html` | `#lfSearchInput` | `order-first` layout |
| `principal/principal-services.html` | `#searchInput` | `⌘K` kbd moved into flex flow |
| `teacher/teacher-lessons.html` | `#lessonSearch` | — |
| `teacher/teacher-roster.html` | `#rosterSearchInput` | — |
| `admin/admin-timetables.html` | `#monSearch` | **icon was after input in DOM — reordered** |
| `admin/admin-lost-found.html` | `#lfSearch` | — |
| `admin/admin-news.html` | `#tableSearchInput` | — |
| `admin/admin-campuses.html` | `#campusSearch` | page clear btn `#campusSearchClear` |
| `admin/admin-classes.html` | `#streamSearch #teacherSearch #subjectSearch #roomSearch` | modal dropdown minis → `ngis-search--compact`; `#teacherSearch` had `person_search` glyph → unified to `search` |

**Dark-mode stale rules neutralized:** `departments.html` (`#dept-search`
black bg) and `student-assignments.html` (`#asgnSearch` slate bg) — shared
dark tokens now govern.

## 4. Additional defects found & fixed

1. **`shared/lessons.html` — icon overlapped input** (`oak-filter-search-wrap`
   had no CSS anywhere). Converted to shared shell; enhancer now adds the
   clear button; `oakSearchResources` filter verified working (essay → 0 +
   empty state, clear → 6).
2. **`admin/admin-news.html` + `admin/admin-lost-found.html` — search bar
   squeezed to 30 px** by unshrinkable sibling filter rows (pre-existing).
   Fix: `min-w-[240px]` on the search shell + toolbar rows now wrap
   (`md:flex-wrap` / `lg:flex-wrap`); filters gracefully wrap on narrow desktop.
3. **`shared/departments.html` — no empty-results message.** Added
   `#dept-search-empty` (`ngis-search-empty`, `role="status"`):
   "No departments match your search."

## 5. Test results (all executed in-browser via agent-browser)

- **Geometry:** 21 search inputs across 15 pages — flex shell, no icon/text
  overlap, input fits wrapper. Includes header (`htbSearchInput`), sidebar
  (`sidebarSearchInput`), and page-level bars on: departments, admin-departments,
  admin-department-detail, student/teacher/principal/admin services & lost-found,
  assignments, attendance, campuses, classes (4 modal minis), news, timetables,
  lessons, exams, announcements, gradebook, roster, activity.
- **States:** default (white/`#E1E9E3`/10px), hover (border deepens), focus
  (green border + 3px ring `rgba(23,107,69,.12)`), typing (clear appears,
  no overlap with long query), clear (restores full result set), compact
  variant 38px in modal dropdowns.
- **Functionality:** departments filter (khmer → 1 card; clear → 3),
  lessons filter (essay → 0 + empty state; clear → 6), sidebar nav filter
  ("timetable" → only Class Timetable; clear → 11 links), header search
  accepts input + clear button. No pagination/filter breakage observed.
- **Responsive 320 / 375 / 768 / 1024 px** (departments, admin-news,
  principal-services): zero horizontal overflow, zero bad searches.
- **Console:** clean on all tested pages (only the pre-existing Tailwind CDN
  production warning).
- **Dark mode:** shell `rgb(31,46,38)` bg, transparent input, placeholder
  `#9AAA9F` — token-driven, no stale black-input rule.
- **Accessibility:** aria-labels added by enhancer (`aria-label="Clear search"`,
  placeholder-derived labels), empty-state uses `role="status"`, icon spans
  `aria-hidden`.

Screenshots: `.testshots/search-final-dept-1440-focus.png`,
`.testshots/search-final-dept-375.png`, before-state in
`.testshots/search-audit-dept-before.png`.

## 6. Files touched

- `assets/css/ngis-search.css` (hardening: `:where` width, icon overflow,
  webkit cancel, placeholder importance)
- `pages/shared/departments.html`, `pages/shared/lessons.html`
- `pages/student/student-assignments.html`
- `pages/principal/principal-activity.html`, `principal-lost-found.html`, `principal-services.html`
- `pages/teacher/teacher-lessons.html`, `teacher-roster.html`
- `pages/admin/admin-absence-stats.html`, `admin-attendance.html`, `admin-campuses.html`,
  `admin-classes.html`, `admin-lost-found.html`, `admin-news.html`, `admin-timetables.html`

No backend or business-logic files were modified.
