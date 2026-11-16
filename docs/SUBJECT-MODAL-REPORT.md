# NGIS-SYSTEM — Add New Subject & Subject Creation Modal (Master MVP Fix)

**Status:** Complete and validated · 2026-11-16
**Target:** `http://127.0.0.1:3000/pages/admin/admin-subjects.html`

---

## 1. Root cause of the broken "Add New Subject" button

Three layered problems — none of which was "just a missing listener":

1. **No popup ever existed.** The Khmer-suite UI (`khmer-suite-ui.js`) rendered the
   button with `data-act="subject-add"`, but clicking it ran a handler that
   inline-appended a placeholder row ("New Subject N") to the table. A subject
   creation modal was never built (the page's `modalHtml()` is the timetable
   Quick-Lesson-Editor, a different modal).
2. **Two duplicate handlers fought each other.** The button was wired twice — a
   direct `addBtn.onclick` (line ~3131) AND a delegated global `case 'subject-add'`
   (line ~4908) — so a click inserted two unnamed stub rows.
3. **The inline path could never persist for Admins.** Subject state lives in the
   authoritative `data/timetable_state.json` and is saved via `PUT /api/timetable/state`,
   which is guarded by `_builder_write_guard()` — **`admin` is in
   `READONLY_TIMETABLE_ROLES`** (timetable drafting belongs to the Principal
   Portal). So every admin "add/edit/delete" silently remained localStorage-only.

**Bonus root-cause bug found during real-browser testing:** `ui-cleanup.css` ships a
global modal-suppression rule — `[id$="Backdrop"]:not(.open):not(.is-open):not(.show)
{ display:none !important }`. The first modal implementation (id `sfBackdrop`,
no `.open` class) was rendered **invisible to real users** — DOM checks passed but
Playwright reported every field "not visible" for real clicks. Fixed by following
the app's established `.open` convention.

## 2. What was fixed / built

### Backend — `timetable_models.py` + `timetable_api.py`
New surgical endpoints on the **existing** store singleton (`data/timetable_state.json`
— no duplicate database, no parallel storage):

| Endpoint | Guard | Purpose |
|---|---|---|
| `POST /api/timetable/subjects` | `_subject_write_guard` — admin, principal, editor, super_admin/superadmin only; student/teacher/staff/monitoring → 403 | Create subject + per-class teacher assignments |
| `PUT /api/timetable/subjects/<id>` | same | Update fields + reconcile assignments |
| `DELETE /api/timetable/subjects/<id>` | same | Delete (mirrors existing client semantics incl. grid-cell cleanup) |

Store methods `add_subject` / `update_subject` / `delete_subject` run under the
store's `_lock`, bump `revision`, append to `state.history` (audited with actor via
`X-Actor`), and atomically persist. Validation (server-side, authoritative):
name required; code required + regex + **uniqueness**; duplicate English-name
rejection; department required; lessons 1–15; hex color; class/teacher IDs must
exist; **a teacher is required per selected class** (the timetable engine's
chip/auto-assign model needs one); no duplicate class selections.

**Grid protection on edit:** assignments for classes that already have scheduled
lessons for the subject are never removed; teacher swaps on such classes keep the
original teacher and surface a warning — preserving existing academic records.

RBAC note: subjects/curriculum management is deliberately writable by Admin
(different concern from timetable *drafting*, which stays Principal-only under
`_builder_write_guard`). Authorization is enforced server-side from the bearer
token / `X-Actor-Role` header — hidden frontend buttons are irrelevant.

### Frontend — `khmer-suite-ui.js`
- **Root cause fix:** both duplicate handlers now open ONE shared modal
  (`SubjectForm.open()`); the inline stub-row insertion is gone. The wizard-tab
  "+ Add Subject" button uses the same modal.
- **SubjectForm modal** (appended to `document.body`, `.open is-open` classes per
  app convention): header "Add New Subject" + required subtitle + close icon;
  two-column form on desktop (single column ≤640px); fields — Subject Name
  (Khmer), Subject Name (English)\*, Short Name, Subject Code\*, Academic
  Department\* (loaded from existing subject departments), Lessons per Week,
  Status (Active/Inactive — existing `active` field), Timetable Color
  (auto-suggested from the name via the existing `getSubjectColor` palette);
  **Assigned Classes section** — Grade Level + Campus + search filters,
  checkbox class list loaded from the real database (12 classes, 2 campuses,
  grades 7–12), selected classes shown as **removable chips with a per-class
  teacher dropdown** (searchable filter, all 34 teachers loaded, different
  teachers per class supported), live selected-count, honest empty state when
  filters match nothing.
- **Validation:** per-field inline errors (next to the field), class/teacher
  errors under the section, focus jumps to first invalid field, form is never
  cleared on failure, duplicate submissions blocked (disabled button + spinner).
- **Loading & feedback:** real backend response awaited (no artificial delays);
  NGIS global toast engine (success/warning/error); server warnings surfaced.
- **Directory integration:** after save the engine adopts the authoritative
  server state (new `KSEngine.reloadFromServer()`) and re-renders — KPI counts,
  table rows and the new **department · N classes sub-line** update without a
  page reload. Persistence verified across page reloads.
- **Edit reuse:** the same modal opens from a per-row **Edit** button (prefilled
  fields, preselected classes, preselected teachers, lock badge on grid-protected
  classes). The inline row editing, lock and delete flows are preserved — delete
  now persists server-side too.
- **"Save Changes" repaired:** inline edits now persist per-subject through
  `PUT /api/timetable/subjects/<id>` (previously they vanished because the
  whole-state autosave is read-only for admins).
- **Interactions:** Cancel/close/Escape/backdrop close; unsaved-changes confirm;
  focus moves into the modal on open and returns to the opener on close;
  background blocked by fixed backdrop; footer stays accessible while content
  scrolls (`shrink-0` footer + scrollable body, viewport-capped height).

## 3. Files modified
- `timetable_models.py` — `SubjectValidationError`, store CRUD methods
- `timetable_api.py` — `_subject_write_guard`, POST/PUT/DELETE routes
- `assets/js/khmer-suite-engine.js` — `reloadFromServer()`
- `assets/js/khmer-suite-ui.js` — modal module, handler repairs, edit button,
  department sub-line, Save Changes/delete API routing

## 4. Test results (all passing)
- **API (curl):** create w/ 2 assignments ✓ (assignments inherit class shifts) ·
  duplicate code 400 ✓ · duplicate name 400 ✓ · missing teacher 400 ✓ · unknown
  class 400 ✓ · student 403 ✓ · teacher 403 ✓ · update (lessons+teacher swap+add
  class) ✓ · persisted to disk + history log ✓ · delete ✓ · delete-missing 404 ✓
- **Browser (real clicks/typing):** button opens modal ✓ · real keyboard input ✓ ·
  dynamic filters (grade 7 → 2 classes; Depo Campus → 2) ✓ · 3-class multi-select
  with removable chips ✓ · per-class teachers (3 different) ✓ · submit → created,
  modal closes, KPI 13→14, directory shows "Modern Physics" ✓ · persisted across
  reload ✓ · edit prefill + save ✓ · duplicate-code submit → server message
  "Subject code M is already used by Mathematics", form preserved ✓ ·
  delete via UI → persisted (13/144 restored) ✓ · Escape + unsaved-changes
  confirm ✓ · focus return to opener ✓ · console clean ✓
- **Responsive:** 320 / 768 / 1024 / 1440 / 1920 — no horizontal overflow; single
  column on mobile; footer accessible; screenshots in `.testshots/subject-modal-*.png`
- **Regression:** `/api/timetable/state` healthy (13 subjects, 25 grid cells),
  timetable pages load, grid untouched by subject CRUD.

## 5. Remaining limitations
- Subject `department` (academic, Khmer-named, e.g. ភាសាខ្មែរ) and class
  `department` (program, English-named, e.g. "Khmer Program") are two existing
  vocabularies with **no mapping table in the database**; class eligibility is
  therefore filtered by grade level + campus + search (real data), not by
  subject-department→program inference. Adding that mapping requires a data-model
  decision, not a UI patch.
- Teacher filtering by department/campus is not applied (teachers in
  `timetable_state.json` carry no campus field); all teachers are offered,
  searchable — assignment validity is enforced server-side.
- "Campus access restrictions" could not be exercised: the current auth model
  (demo personas + provisioned accounts) has no per-admin campus scoping to
  enforce; the endpoint structure is ready if one is added.
- Role resolution for the new guard relies on the existing convention
  (bearer `mock-jwt-token-*` or `X-Actor-Role` header); provisioned
  `um-session-*` tokens carry no role header and would need one to write.
