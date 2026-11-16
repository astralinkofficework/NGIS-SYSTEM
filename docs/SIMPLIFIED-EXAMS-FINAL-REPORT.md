# NGIS-SYSTEM — Simplified Examination Schedule Across All Portals

**Status:** Implemented and verified  
**Scope:** Student, Teacher, Principal and Admin examination pages plus the shared Flask exam engine  
**Date:** 2026-11-16

---

## 1. Audit summary

### Backend

- All primary exam routes live in `exam_management_api.py` (`exam_bp`) and persist to `.data/academic.sqlite3`.
- The legacy `exams` table has 46 columns, including hall, room, seat, marks, weight and syllabus fields. The new workspace writes schedule-only values and leaves those columns empty/neutral; no new exam data is hardcoded.
- Existing workflow fields were reused: `status`, `academic_status`, `operational_status`, `result_status`.
- Conflict detection already existed but depended on a room and could not handle the simplified seven-field form. It was extended to detect overlapping times for shared classes and duplicate subject/type/date schedules.
- `server.py` contained a separate `/api/teacher/exams` route with literal exam arrays, rooms and invigilation duties. It had no callers and has been replaced with a compatibility alias to the persistent exam engine.
- Identity resolution was inconsistent: the exam API accepted generic `X-Actor-Id` / `portal` query values, while the rest of the app used `ngis_actor` / `X-Actor` email identities. The exam API now resolves real person IDs, roles, campus and department from `data/user_accounts.json`.

### Frontend

- `pages/shared/exams.html` and `pages/student/student-exams.html` were byte-identical 2,517-line pages containing hall tickets, desk numbers, syllabus panels, Ask Teacher buttons, timelines, results and gradebook views.
- `pages/teacher/teacher-exams.html` was a 948-line assessment portal with grading, marks and room allocation.
- `pages/principal/principal-exams.html` had no hero wiring, an empty `#heroBanner`, and a duplicated `htbHamburger` ID that removed the mobile app bar hamburger.
- `pages/admin/admin-exams.html` had the newer table design but still exposed operational readiness, hall clearance and publish controls to ordinary admins.

---

## 2. Implemented workflow

```text
Teacher creates schedule (draft or submit)
        ↓
Teacher submits → Principal pending review
        ↓
Principal approves / rejects / requests changes
        ↓
Principal publishes approved schedule
        ↓
Students see it in their personal calendar
```

- If a published schedule is changed, the **same record** is updated and a `notify_students` audit entry is written. Teachers cannot silently edit published records; principals/admins can correct them.
- Cancelling a published schedule removes it from student calendars immediately.
- Only `principal` and `superadmin` can approve, reject, publish, unpublish or request changes. An ordinary `admin` can search, correct and cancel but **cannot** grant academic approval.
- Teacher create/edit/submit is validated against `teacher_assignments` (real subject/class pairs). Unassigned subjects or classes return `403`.
- Students only receive published exams whose `class_ids` intersect their real `enrollments`. A fake `student_id` cannot be supplied by a student actor.

### New / updated endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /api/exams/options` | Departments, subjects, classes, campuses, exam types; scoped to teacher assignments |
| `GET /api/exams/simple` | Staff schedule list with filters: `q`, `exam_type`, `status`, `month`, `dept`, `campus`, `class_id` |
| `POST /api/exams/simple` | Teacher/principal create; validates real relationships and conflicts |
| `PUT /api/exams/simple/<id>` | Correct schedule; re-submits teacher edits to approved records |
| `POST /api/exams/simple/<id>/submit` | Teacher submits draft/returned schedule |
| `POST /api/exams/simple/<id>/review` | Principal approve / reject / request changes |
| `POST /api/exams/simple/<id>/publish` | Principal publishes approved schedule |
| `POST /api/exams/simple/<id>/unpublish` | Principal withdraws published schedule |
| `POST /api/exams/simple/<id>/cancel` | Cancel with role-aware authorization |
| `GET /api/exams/activity` | Persistent audit history with filters |
| `GET /api/exams/student` | Rewritten: published exams for enrolled classes, `upcoming` / `completed`, type and month filters, **no result data** |

Legacy grade/result endpoints remain in the module for backwards compatibility but are no longer referenced by any of the four portals.

---

## 3. Portal changes

All five exam documents now share `assets/css/exams-simple.css` and `assets/js/exams-simple.js`.

- **Student** — personal calendar only: Upcoming/Completed tabs, exam type and month filters, compact cards showing subject, type, date, time and department only when needed. No halls, seats, gradebook, syllabus, messaging, timelines, charts or statistics.
- **Teacher** — schedule management table and a seven-field vertical form: Department, Subject, Class or classes, Examination type, Date, Start time, End time. Actions: Edit, Submit, Cancel. Approval status and correction notes remain visible.
- **Principal** — tabs for Pending approval, Upcoming, Approved, Returned and Published; campus/department/class filters; Review modal with Approve, Request changes and Reject; Publish and Withdraw actions.
- **Admin** — clean table with exactly Subject, Class, Type, Date, Time, Department, Status, Actions; search and filters; conflict notices; View, Correct, History and Cancel actions; no approval controls.
- The principal page now loads `hero.js` with a proper `HERO_CONFIG`, restoring the top navigation bar. The duplicate hamburger ID was removed.
- Modal scrims are appended to `document.body`, with blur and a translucent overlay; focus trap and Escape handling are included.

### Files changed

- `exam_management_api.py` — actor resolution, exam-type normalisation, scoped catalogue, simplified CRUD/workflow/filters/activity, stricter legacy approval roles.
- `server.py` — replaced the hardcoded `/api/teacher/exams` route with the persistent API alias.
- `assets/css/exams-simple.css` — new scoped design system for the four workspaces.
- `assets/js/exams-simple.js` — new shared renderer, filters, forms, modals and actions.
- `pages/admin/admin-exams.html`, `pages/teacher/teacher-exams.html`, `pages/principal/principal-exams.html`, `pages/shared/exams.html`, `pages/student/student-exams.html` — rebuilt around the shared workspace.
- `tests/test_simplified_exams.py` — new 11-test workflow regression suite.

---

## 4. Verification

### Automated

- `python -m unittest tests.test_simplified_exams` — **11 tests, all passing**.
  - Identity resolution, teacher assignment scoping, unassigned-subject rejection, full workflow, student isolation, conflict detection, admin approval denial, admin correction, filters, cancellation, activity log.
- `python -m unittest tests.test_roles_access_v3 tests.test_roles_permissions` — **68 tests, all passing**.
- `node --check assets/js/exams-simple.js` and `python -m py_compile` for both Python modules — passed.

### Real browser (Chromium via agent-browser)

| Check | Result |
| --- | --- |
| Teacher created and submitted a Class Test for Grade 10A, 24 Dec 2026 | Passed; toast `Schedule submitted for Principal review.` |
| Principal pending queue displayed the submitted record | Passed |
| Principal approved, then published | Status `approved` → `published` |
| Student calendar after publish | New exam present in API and rendered card |
| Student `2026-STD-0143` (only class 11b) | New Grade 10A exam **not present** |
| Type filter `class_test` / month filter `2026-12` | 2 / 1 records, correct types and dates |
| Duplicate overlapping create attempt | `409` toast; modal stayed open; no new row |
| Principal cancelled published exam | Status `cancelled`; student calendar no longer shows it |
| Admin activity modal | 20 audit entries rendered |
| Admin status/search filters | 1 row each, as expected |
| Desktop 1440px, mobile 390px, all four portals | No horizontal overflow (`scrollWidth === innerWidth`); mobile app bar visible; tables stack into cards |
| Create modal at 390px | Width 358px, seven fields visible, no overflow |
| Modal scrim | Parent `BODY`, `backdrop-filter: blur(4px)`, translucent background |

Screenshots: `scratch/exams-admin-desktop2.png`, `scratch/exams-student-desktop.png`, `scratch/exams-student-mobile.png`, `scratch/exams-teacher-form.png`.

Verification records were removed from `.data/academic.sqlite3` after testing.

---

## 5. Limitations and follow-up

- Existing seeded exam rows from the earlier demo engine remain in the database (`midterm`, `final`, `mock`, `practical` types). They are displayed with the five supported labels where applicable; no new hardcoded exams are seeded by this implementation.
- `exam_locations`, `exam_student_results` and grade/result endpoints remain for backwards compatibility only. They are not exposed in the four redesigned portals.
- The codebase audit recommendation to remove the duplicate `htbHamburger` ID in `pages/shared/news.html` is still outstanding and was outside this exam-only task.
- No online testing, gradebook, seating, room allocation or examination hall functionality was added.

---

## 6. Post-delivery navigation adjustment

- Removed the student sidebar link `pages/shared/exams.html?dept=english&portal=student` from `data/sidebar_nav.json` (`student → academics → exams`). The exam calendar is now reached from the **department hub** card (`pages/shared/department.html?id=<dept>&portal=student → Exams & Tests`), which already links to `exams.html?dept=<dept>&portal=student`.
- The exam page now reads `?dept=`:
  - The backend student endpoint filters by that department in addition to real class enrollment.
  - The hero title, greeting, breadcrumb and page subtitle reflect the selected department.
  - Department is no longer repeated in each card meta line when a department context is active.
  - `Khmer` therefore shows Khmer examinations only (and an honest empty state if none are published), never English/Math/Science results.
- The old course-filter strip (`#courseFilters` / `setCourseFilter`) is no longer present in any exam page.
- Added regression test `test_12_department_context_isolation` (12 exam tests now pass). Browser checks confirmed: sidebar has zero exam links, Khmer hub card opens `?dept=khmer` with only Khmer data, English hub card opens `?dept=english` with only English data, no course filter, and no overflow at 390px.
