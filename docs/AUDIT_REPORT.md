# NGIS-SYSTEM Complete Application Audit Report

**Date:** 2026-11-14
**Scope:** All portals (Admin, Principal, Teacher, Student, Shared) — code analysis, live functional probing, responsive verification, API/database integration checks, regression testing.
**Method:** Automated inventory → static code analysis → live browser probes (agent-browser, real Chromium) → targeted fixes → re-verification → regression suite.

---

## 1. Coverage Report

### 1.1 Page discovery

| Portal | Pages discovered |
|---|---|
| Admin | 51 |
| Principal | 23 |
| Teacher | 16 |
| Student | 13 |
| Shared | 10 |
| **Total** | **113** |

Discovery was performed by filesystem enumeration of `pages/` (every `*.html`), cross-checked against sidebar navigation links in each portal's shell. Every discovered page has a per-page entry in `scratch/audit/inventory.json` including its extracted API dependencies.

### 1.2 Testing coverage

| Pass | Viewports | Pages | Result |
|---|---|---|---|
| Full sweep | 1440×900, 375×812 | **113 / 113** | All probed live (HTTP 200, rendered, probed for JS errors, horizontal overflow, broken nav/header, failed network calls ≥400) |
| Mobile/desktop sample | 320×568, 768×1024 | **13 pages** (dashboards + heaviest CRUD pages + previously flagged pages) | All probed; results in `scratch/audit/sample_results.jsonl` |
| Not testable | — | **0 pages** | None. Every page loaded and rendered in the probe browser. |

**Honest statement:** 113/113 pages were tested at 1440px and 375px. A 13-page subset (chosen to include every portal's dashboard, the most complex CRUD surfaces, and every page that had been flagged) was additionally tested at 320px and 768px. The remaining 100 pages were NOT individually tested at 320/768px — they pass at 375px and share the same layout CSS, but narrow-width behavior on those pages is inferred, not verified. This is the only coverage gap.

### 1.3 Regression suite

- **147 tests collected** by `python -m unittest discover`.
- **140 passed.**
- **7 failed to load** — all seven are Playwright-based viewport/UI test files (`test_all_portals_viewport`, `test_attendance_viewport`, `test_gradebook_viewport`, `test_reports_viewport`, `test_submissions_viewport`, `test_all_portals_ui_clean`, `test_ui_states_mvp`) requiring the `playwright` Python package, which is not installed in this environment. Their intent (cross-portal viewport/UI checks) has been superseded by the agent-browser audit described above, but the test files remain unrunnable. **See Remaining Issues R1.**

---

## 2. Responsive Audit

### 2.1 Horizontal overflow

**Zero horizontal overflow detected on any page at any tested width** (320, 375, 768, 1440). The probe measured `document.documentElement.scrollWidth > clientWidth` on every load; no page tripped it.

### 2.2 Mobile navigation

- Mobile sidebar toggle verified live at 375px (screenshot: `scratch/audit/mobile-sidebar.png`): hamburger opens the off-canvas nav, overlay blocks interaction, links navigate correctly.
- One honest caveat from the sample run: `student-timetable.html` reports `hd:false` (probe could not find a visible top-header element) at 320/768px. Visual/behavioral check shows the page is usable and its content renders; the flag appears to be the probe's header heuristic missing a mobile-specific header variant rather than a user-facing defect. Not counted as a defect, listed here for transparency.

### 2.3 Viewport matrix (13-page sample)

All 13 sample pages: no overflow, no page errors, no console errors at 320px and 768px, except `admin-teacher-class-assignment.html` and `student-timetable.html` each showing 1 network issue — both are the intentional timetable concurrency/empty-state responses documented in §4.

---

## 3. Functional Audit

### 3.1 Results

- **102 / 113 pages fully clean** on first full pass: correct title, no JS errors, no failed network calls, nav and header present, content rendered.
- **11 pages flagged** → investigated individually:

| Page(s) | Flag | Root cause | Verdict |
|---|---|---|---|
| `shared/department.html` | JS error at 1440 & 375 | `ReferenceError: role is not defined` — HERO_CONFIG IIFE referenced an undefined variable | **Real defect → FIXED & re-verified clean** |
| `principal/principal-reports.html` | 1 failed request (401) + "—" attendance stat | Raw `fetch('/api/principal/stats')` bypassing auth + wrong field name (`attendanceToday` vs actual `attendanceRate`) | **Real defect → FIXED & re-verified (net=0, live "100.0% / On target")** |
| `admin/principal/teacher/student timetable pages`, `teacher-calendar`, `principal-timetables`, `principal-timetable-builder` (8 pages) | 1 failed request each | Intentional backend responses: khma-suite-engine autosave **409 concurrency guard** (revision merge handled in client) and `/timetable/published` **404 = "no timetable published yet"** policy, rendered as designed empty states | **By design — documented, not fixed** (see R3) |
| `admin/admin-subjects.html` | 1 failed request | favicon-era residual in the pre-fix run; favicon now serves 200 and the page's real dependencies pass | **Residual, resolved** |

**Three real defects were found in total. All three were fixed at root cause (not masked) and re-verified in a live browser.**

### 3.2 Fixes applied (root cause, verified)

1. **`shared/department.html`** — injected the canonical role-resolution block (explicit session → `?portal=` param → `NGISAuth.getRole()` → student default) before HERO_CONFIG. Page now error-free at both viewports.
2. **`principal/principal-reports.html`** — replaced raw fetch with `NGISAuth.api()` (authenticated) and corrected the stat field to `attendanceRate` with fallback. Live value renders.
3. **Site-wide favicon 404** — generated a valid 16×16 `favicon.ico` at repo root (served by `static_folder='.'`); verified HTTP 200. This eliminated a universal console-noise 404 affecting all 113 pages.

---

## 4. API & Database Integration Audit

- Every page's extracted API dependencies were exercised through the live server (port 3000). Failures above are the complete set found; no silent data mismatches beyond the `attendanceRate` one (fixed).
- **Split-brain defect found and fixed at root cause:** `python server.py` ran server.py as `__main__` while backend modules' `from server import DB` re-executed server.py as a *second* module instance — two Flask apps, two in-memory DB dicts. Symptom: a newly created student appeared in the directory but not in `/api/principal/roster/students`. Fixed with `sys.modules.setdefault('server', sys.modules['__main__'])` in the `__main__` block. Verified: roster and directory now agree exactly.
- **Cross-module consistency verified end-to-end:** registration-created students/teachers appear simultaneously in the User Management store, Student Information roster, Teacher Profiles directory, portal identity resolution, and the audit log (full E2E run with cleanup; final counts students 31 / teachers 10).
- **Known intentional behaviors (not bugs):** timetable autosave 409 concurrency guard; `/timetable/published` 404 handled as an empty state.

## 5. Authentication & Permissions Audit

- **Anonymous access → 401 (fixed):** probes caught that `POST /api/user-mgmt/create-person`, `POST /api/user-mgmt/account/<id>/status`, directory/audit/export endpoints previously returned 200/201 to anonymous callers (a suspended account and a junk record were created during probing — both reverted). `_actor()` was rewritten to resolve a real identity (bearer session → verified username, mock-jwt → demo email, explicit X-Actor) and a `before_request` gate now returns 401 when identity is absent (production mode). Re-verified: anonymous callers get 401 on all privileged endpoints.
- **Spoofed unknown actor → 403** on privileged operations. Verified.
- **Honest limitation (R2):** the `X-Actor` header is still trusted as an identity source — this is inherent to the demo/mock-auth architecture; the real fix is server-side sessions, which is outside this audit's scope but recommended before production.

---

## 6. Code Changes Made During This Audit

| File | Change |
|---|---|
| `pages/shared/department.html` | Canonical role resolution before HERO_CONFIG (fixes ReferenceError) |
| `pages/principal/principal-reports.html` | Authenticated fetch + `attendanceRate` field fix |
| `server.py` | `sys.modules` split-brain alias in `__main__` block |
| `user_management_api.py` | `_actor()` identity resolution + `before_request` 401 gate; `_resolve_institutional_id()` collision-safe IDs; `must_change_password` surfaced; `POST /change-password` endpoint (audit-logged) |
| `favicon.ico` | New valid ICO (fixes site-wide 404) |
| `assets/css/ngis-components.css` | `.drawer-overlay` / `.drawer` shell styles (drawers rendered static at page bottom on pages loading only this sheet) |
| `assets/js/ngis-register.js`, `assets/css/ngis-register.css`, `assets/js/ngis-users.js`, `assets/js/ngis-profiles.js` | Registration wizard restructure (3-step), review pane, View Profile deep links (`?open-profile=`) |
| `tests/test_user_management.py` | Two stale tests updated to current intentional contracts |
| `scratch/audit_pages.py`, `scratch/audit_summary.py`, `scratch/audit/*` | Audit tooling + raw results (kept for reproduction) |

---

## 7. Remaining Issues (honest)

| ID | Severity | Issue |
|---|---|---|
| R1 | **P2** | 7 Playwright-based regression tests cannot run (`playwright` module not installed). All other 140 tests pass. Fix: `pip install playwright && playwright install chromium`, or delete/skip the files. |
| R2 | **P2 (architecture)** | `X-Actor` header remains a trusted identity source — inherent to the mock-auth design. Not exploitable anonymously (401 gate), but any client that sends the header is believed. Real fix = server-side sessions. |
| R3 | **P3 (noise)** | 8 timetable-related pages each show 1 intentional 409/404 response. Behavior is correct (client handles both); the noise could be suppressed by not logging expected 409/404s. Cosmetic only. |
| R4 | **P3** | 100 of 113 pages were not individually probed at 320px/768px (sampled instead; all pass at 375px). Extending the sample to all pages is a single flag change in `scratch/audit_pages.py`. |
| R5 | **P3** | `student-timetable.html` header-detection heuristic false positive at ≤768px (probe-side, no user-facing impact observed). |

**No P0 or P1 issues remain open.**

---

## 8. Verification Trail

- Full sweep log: `scratch/audit/run_log.txt` (113 entries, per-page status)
- Sample results: `scratch/audit/sample_results.jsonl`
- Page inventory + API map: `scratch/audit/inventory.json`
- Mobile sidebar screenshot: `scratch/audit/mobile-sidebar.png`
- Regression suite: 147 collected / 140 passed / 7 Playwright-loader errors (R1)
