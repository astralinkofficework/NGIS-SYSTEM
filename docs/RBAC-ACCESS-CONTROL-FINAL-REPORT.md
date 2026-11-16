# NGIS — Roles & Access Control Redesign & Full Permission Management
## Final Implementation, Security & Verification Report

**Date:** 2026-11-15
**Target page:** `pages/admin/admin-roles-permissions.html` (`http://127.0.0.1:3000/pages/admin/admin-roles-permissions.html`)
**Status:** Implemented, connected to real backend enforcement, browser-tested and regression-tested.
**Scope rule honoured:** no visual-only permission editor, no hardcoded role/permission/user numbers, no fictional module directory, no CSS-hidden thousand-row audit log, no trust in frontend checkbox states.

---

## 1. Executive summary

The page is now an enterprise access-management workspace backed by server-authoritative RBAC. The pre-existing `roles_permissions_api.py` already owned a permission registry, core-role baselines, per-account overrides, effective-access resolution, an audit log and a direct-URL gate. That architecture was **preserved and extended**, not replaced.

A new backend security layer (`roles_permissions_ext.py`) adds real API enforcement bindings, honest custom permission definitions, richer role lifecycle, role-level portal grants, user-role assignment, server-side pagination and an authority bootstrap. The frontend was rebuilt as a scoped `.rp-v3` workspace that renders server-computed state and never makes an authorization decision itself.

The final goal chain was executed end to end in a real browser and then verified at the backend:

> Create Custom Role → Define Permissions → Assign Authorized Access → Assign Users → Save to Database → Enforce Permissions Across Portals → Record Audit Activity

All test data created during verification was removed. Only genuine audit events remain (21 → 32 records).

---

## 2. Phase 1 — What already existed (discovered, not invented)

| Item | Discovered value | Source |
|---|---|---|
| Protected core roles | `SUPER_ADMIN`, `ADMIN`, `PRINCIPAL`, `TEACHER`, `STAFF`, `STUDENT` (6) | `roles_permissions_api.CORE_ROLES` |
| Custom roles | 2 (`ROL-001`, `ROL-002`) | `data/roles_permissions.json` |
| Total roles | 8 | bootstrap `/api/roles-mgmt/bootstrap` |
| Registered permission definitions | 100 `(module, action)` pairs | `PERMISSION_MODULES` (28 modules in 4 categories) |
| Registered actions | 12: view, create, edit, delete, approve, reject, publish, upload, download, export, import, manage | `ALL_ACTIONS` |
| Published sidebar pages | 99 (admin 36, superadmin 17, principal 16, teacher 13, student 10, staff 7) | `data/sidebar_nav.json` via `_page_index()` |
| HTML files on disk | 113 (not all are published nav pages) | `pages/**/*.html` |
| Portals | `admin`, `principal`, `teacher`, `student`, `staff`, `superadmin` (6) | `PORTAL_KEYS` |
| Login accounts | 268 | `data/user_accounts.json` |
| Existing RBAC endpoints | 22 under `/api/roles-mgmt` | `roles_permissions_api.py` |
| Persistent stores | JSON: `data/roles_permissions.json`, `data/user_accounts.json`; SQLite `.data/academic.sqlite3` untouched | filesystem |
| Identity mechanism | `ngis_actor` cookie / `X-Actor` / `X-NGIS-Session` / `Authorization` header; demo-first passive session | `_session_actor()` |
| Existing direct-URL gate | `server.py` `before_request` → `rp._resolve_access()` → redirect to `/pages/shared/access-denied.html` | `server.py` |

**Design decision:** the four-tab layout, summary KPIs, left Role Directory and right Permission Configuration were retained as required; everything else was rebuilt around real data.

---

## 3. Backend security architecture

### 3.1 New file — `roles_permissions_ext.py`

| Concern | Implementation |
|---|---|
| Default-deny API gate | `register_enforcement(app)` adds a `before_request` hook for `POST/PUT/PATCH/DELETE` on `/api/...`; 16 real API families are bound to `(module, action)` pairs |
| Permission resolution | `effective_action_permissions()` calls the **same** `rp._resolve_access()` used by the page gate, so UI and enforcement can never disagree |
| Unknown identifiers | `enforce_permission()` returns `False, 'unknown_permission'` for unregistered module/action pairs |
| Custom permission definitions | create / edit / delete / inventory with strict validation; unbound definitions are marked `Requires Integration` and cannot be granted |
| Role lifecycle | rich create, edit, safe delete, duplicate, archive/enable, concurrency via `expected_updated_at` |
| Role portal grants | `PUT /roles/<id>/portals`; integrated into `rp._resolve_access()` so active custom-role portals affect real page access |
| User-role assignment | `GET/POST /user-roles` with self-assignment, SUPER_ADMIN, delegation and last-SUPER_ADMIN protection |
| Server-side paging | `/users/paged`, `/audit/paged` — `LIMIT/OFFSET` on the server, not CSS-hidden rows |
| Authority bootstrap | `/bootstrap` returns actor authority, 4 scope options, protected portals and real registries |

### 3.2 Enforcement bindings (real API families, not fictional modules)

`/api/roles-mgmt/overrides/`, `/roles`, `/permissions`, `/user-roles`, `/role-portals`, `/api/user-mgmt/`, `/api/cms/dashboard/publish`, `/api/cms/dashboard/`, `/api/nav/`, `/api/system/`, `/api/school-config/`, `/api/news`, `/api/announcements`, `/api/teacher-mgmt/`, `/api/student-mgmt/`, `/api/academic/admin/` — **16 bindings**. Plus 6 RBAC guard pairs and View dependencies for bound modules → **26 enforced `(module, action)` pairs**.

### 3.3 Files changed

| File | Change |
|---|---|
| `roles_permissions_ext.py` | **New** — security extension layer (17 new endpoints) |
| `roles_permissions_api.py` | `_role_summary()` exposes status/base role/identifier/category/portals/scopes/updated_at; `_resolve_access()` now merges active custom-role portal grants |
| `server.py` | Registers extension blueprint + `register_enforcement(app)`; existing direct-URL gate retained |
| `pages/admin/admin-roles-permissions.html` | Loads `roles-access.css?v=3.2` and `ngis-roles.js?v=3.3` |
| `assets/js/ngis-roles.js` | **Rewritten** v3 renderer: 4 tabs, real API state, ngx disclosure, sticky matrix, mobile module accordion, dialogs, toast |
| `assets/css/roles-access.css` | **New** scoped `.ngis-rp.rp-v3` stylesheet + body-level dialog host styles |
| `tests/test_roles_access_v3.py` | **New** 31 security tests + 5 frontend-contract guards |
| `tests/test_roles_permissions.py` | Existing 37-test suite retained, unchanged contract |

**APIs created (17, all `/api/roles-mgmt/…`):** `GET/POST /permissions`, `PUT /permissions/<key>`, `POST /permissions/<key>/delete`, `GET /enforcement`, `POST /roles/create`, `POST /roles/<id>/edit`, `DELETE /roles/<id>`, `PUT /roles/<id>/permissions/save`, `GET /role-portals`, `PUT /roles/<id>/portals`, `GET/POST /user-roles`, `GET /users/paged`, `GET /campuses`, `GET /audit/paged`, `GET /bootstrap`.

### 3.4 Database / store changes

`data/roles_permissions.json` gains/uses: `permission_definitions[]`, `role_portals{}`, `custom_roles[].portals`, `custom_roles[].scopes`, `custom_roles[].custom_permission_keys`, `audit_log[]`, `user_overrides{}`.
`data/user_accounts.json` gains/uses: `accounts[].custom_roles[]`.
No schema migration was required — JSON stores are schema-versioned. SQLite academic data was not touched.

Final verified state after all browser tests and cleanup: **2 custom roles, 0 custom definitions, 0 overrides, empty role_portals, 32 real audit events, 268 accounts, `dara.chhen@ngis.edu.kh.custom_roles = []`**. The one probe news item created during an HTTP enforcement test was deleted (news count back to 14).

---

## 4. Fully enforced vs. definitions requiring backend integration

This distinction is explicit and enforced by code, not just documentation.

| Category | Count | Backend behaviour |
|---|---|---|
| **Fully enforced `(module, action)` pairs** | **26** | A concrete server-side enforcement point exists: one of the 16 mutating API bindings, one of the 6 RBAC guard pairs, or a View dependency for a bound module. `enforce_permission()` allows/denies real operations from these. |
| **Registered definitions without a dedicated operation binding** | **74** | Real registered identifiers used by the resolver for page visibility, direct-URL gating and effective-permission computation. They can be granted/revoked and are shown in the matrix, but **no mutating API handler consults them individually**. Adding a new API requires adding a binding to `API_BINDINGS`. |
| **Custom permission definitions** | 0 at rest | Validated against the real registry. If `(module, action)` is not in `ENFORCED_PAIRS`, the definition is stored as `Requires Integration` / `Not Enforced`, displayed with a warning tag, and `save_permissions()` returns **403** if anyone tries to grant it. It cannot widen access. |
| **Unregistered module slugs** | 0 at rest | Allowed as *definitions only* (lowercase slug, e.g. `teacher-reports`), always `Requires Integration`. Custom action identifiers are rejected. |

`/api/roles-mgmt/enforcement` publishes the full binding inventory to the UI, and the Add Permission modal states: *"A permission definition is not an access grant… Otherwise it is stored as Requires Integration and cannot be assigned to any role."*

---

## 5. Security protections verified

| Protection | Verification result |
|---|---|
| Default-deny for unknown identifiers | `enforce_permission()` returns `False`; covered by unit test |
| Protected core roles | Cannot be edited/deleted; UI shows read-only explanation; backend rejects mutation |
| No privilege escalation | Student `POST /api/roles-mgmt/permissions` → **403** "Only active administrators or delegated roles may modify roles and permissions" |
| SUPER_ADMIN identity protection | Assigning a custom role to `admin@ngis.edu.kh` → **"SUPER_ADMIN is a protected identity and cannot hold custom roles"** |
| Self-assignment / delegation / last Super Admin | Unit-tested; locked |
| Optimistic concurrency | `expected_updated_at` on role/permission/portal writes; stale write → 409 |
| Explicit deny wins | Per-account `deny` overrides role grants in the shared resolver |
| Scope validation | `global`, `assigned-campus`, `assigned-department`, `own-records` validated server-side; invalid scope → 400 |
| Resource validation | Unknown target page → 400; wrong-portal page → 400; duplicate key → 409; reserved builtin key → 409; unsupported action → 400; malformed module → 400 |
| Direct-URL gate | Student requesting `/pages/admin/admin-roles-permissions.html` → **302** to `access-denied.html?...reason=access_denied`; SUPER_ADMIN → **200** |
| Mutating API gate | Student `POST /api/news` → **403** (`news.edit`); student `PUT /api/teacher-mgmt/probe` → **403** (`teacher-profiles.edit`); SUPER_ADMIN → allowed |
| Cross-portal propagation | After granting `teacher` portal to a custom role and assigning it to a student: teacher page **200**; same page for an unassigned student **302**. After revocation: **403** API / **302** page again |
| Audit trail | Every mutation recorded; server-paginated; newest-first; 29 → 32 events during final E2E |
| No trust in frontend checkboxes | All grants re-validated in `save_permissions()` against registry, authority and `ENFORCED_PAIRS` |

---

## 6. UI / UX improvements

- Four tabs retained: **Roles & Permissions**, **User Access & Visibility**, **Portal Access Control**, **Activity Audit Log**.
- Compact KPIs, left Role Directory with search + Show More/Less, right Permission Configuration workspace.
- Desktop permission matrix with **sticky header + sticky module column** by category; mobile module accordion detail; category Select all / Clear; dirty-state save bar.
- **Add New Role** modal with real registered permission modules; **Add Permission** modal with real modules/actions/portals/pages/scopes and the honest `Requires Integration` note.
- Edit, duplicate, assign users, enable/disable and delete custom roles; core roles read-only.
- User Access: server-paginated directory, search + role + campus filters, effective permission sources, page visibility/direct-access tri-states, action-level granular overrides, preview and sticky save bar.
- Portal Access: role mode and account mode; protected portals flagged and authority-checked.
- Activity Audit Log: server-side pagination, action/search/page-size filters, detail modal with before/after JSON.
- Compare workspace: real `/api/roles-mgmt/compare` results between two roles.
- NGIS modal system: sharp opaque white surface, blurred/dimmed app background, focus trap, autofocus, Escape close, body scroll lock, no washed-out content.
- No decorative pills around ordinary text; plain tags and quiet buttons; light/dark theme aware.

### Root-cause fixes made during this phase

| Defect | Root cause | Fix |
|---|---|---|
| Primary modal button invisible | `ui-cleanup.css` global `html body button` / `[class*="btn"]` reset applied `background: transparent !important; border: none !important` | High-specificity scoped exemptions in `roles-access.css` (no risky global rewrite) |
| Mobile topbar not dimmed/blurred behind modal | Scrim was inside `#rolesRoot`, a sibling of the sticky global appbar with its own stacking context | Hoist scrim to `document.body`, keep `.ngis-rp.rp-v3` on it for vars/descendant rules, add standalone `html body > .rp-v3-scrim` CSS (flex + `margin:auto` avoids tall-modal grid clipping), retarget focus trap and event delegation to `S.modalEl` |
| User directory empty | `campus=ALL` was lowercased to `all` then compared to `'ALL'`, so every account was filtered out | Compare against `'all'`; added explicit `role=ALL&campus=ALL` regression test |
| Portal tab saved wrong role | `refreshAfterWrite()` re-seeded `rolePortalDraft` from the Roles-tab selection | Re-seed from `S.selectedPortalRole` when Portal tab is in role mode |
| Editing a custom-module definition hid its slug | Stored custom slug is not a dropdown option, so the "New module…" branch was never rendered | `openPermissionModal()` maps custom modules to `__new__` and repopulates `rpPermNewModule` |
| Duplicate dropdown label | Demo data has a real campus named "All campuses", identical to the no-filter sentinel | Sentinel renamed to **"Every campus (no filter)"** |
| Tall modal clipped on small screens | Global grid `place-items:center` with `overflow-y:auto` clips top of oversized content | Body-level flex scrim with `margin:auto` on the dialog |
| Audit log hiding thousands of rows with CSS | Original client-side rendering | `/audit/paged` with server `LIMIT/OFFSET`; 20 rows/page → 2 pages; 50/page → 21 rows on 1 page |

---

## 7. Responsive verification

Swept at **320, 375, 430, 768, 1024, 1280, 1440, 1920 px**, both with a modal open and with the plain page. Each width reported:

- horizontal overflow = **0**
- all topbar action buttons inside viewport = **true**
- modal footer inside viewport = **true**
- scrim width equals viewport width at every size
- scroll lock released after Escape = **true**
- layout: single-column grid ≤ 820 px; two-column at 1024+ (`230px 742px` → `290px 1302px`)

Four-tab sweep at 375 px: `overflow = 0` on all tabs. Show More expanded the role directory 5 → 8; 4 matrix categories and 28 mobile module details rendered. Portal role/account modes both functional.

**Screenshots:** `scratch/rbac-v3-mobile-modal-final.png`, `scratch/rbac-v3-desktop-modal-final.png`, `scratch/rbac-v3-dark-modal.png` (plus earlier `rbac-v3-desktop.png`, `rbac-v3-user-access.png`, `rbac-v3-mobile375.png`).

---

## 8. Testing completed

| Suite / method | Result |
|---|---|
| `tests/test_roles_permissions.py` (existing contracts) | **37 tests OK** |
| `tests/test_roles_access_v3.py` (new security + frontend contracts) | **31 tests OK** |
| Combined RBAC unittest run | **68 tests OK** |
| `tests/e2e-portals.test.py` | **9 tests OK** |
| `node --check assets/js/ngis-roles.js` | OK |
| Real-browser modal tests | 5 dialog types (role, permission, assignments, compare, audit detail, confirm), autofocus, 14× Tab focus trap held, Escape + scroll-lock release, body-level scrim `z-index 3000` covering topbar/sidebar, primary button `rgb(23,107,69)` |
| Dark theme | Modal `rgb(22,34,28)`, text `rgb(237,242,238)`, inputs dark with light text, backdrop blur preserved |
| Real-browser RBAC workflows | create role, duplicate, edit, archive, delete; create/edit/delete permission definition; duplicate-key 409; sensitive permission save with confirmation; assign/revoke user; role portal save; audit detail; compare |
| Filters / paging | 268 → 233 (campus) → 200 (STUDENT) → 35 (search "teacher") → 0 (no match); Show More 10 → 20; audit 20/page×2 pages → 50/page×1 page |
| HTTP enforcement probes | Documented in §5, including non-mutating `__rbac_probe__` calls |
| Full goal-chain proof | Role `ROL-003` created → `account-directories.manage` granted → portal `teacher` granted → assigned to `dara.chhen@ngis.edu.kh` → effective `action_permissions['account-directories'] = ['manage','view']`, portals `student + teacher` allow → API and teacher page allowed → revoked and deleted → access denied again |

---

## 9. Remaining limitations and honest caveats

1. **Anonymous demo browsing is intentionally unenforced.** Only an explicit identity (`ngis_actor` cookie or `X-Actor`/`X-NGIS-Session`/`Authorization` header) activates enforcement. This is the pre-existing demo-first architecture; production must bind to a real authenticated session.
2. **`X-Actor` header impersonation is a demo convenience, not production authentication.** Any client can set it. Replace with signed sessions/SSO before deployment.
3. **Scope metadata is validated and displayed but not applied to row-level data filtering.** `assigned-campus` / `assigned-department` / `own-records` are stored on definitions and roles; the API gate currently checks `(module, action)` only. Campus/department row scoping requires integration with each data API.
4. **74 of 100 registered permission pairs have no dedicated mutating-API binding.** They govern navigation/visibility and effective-permission computation but are not individually consulted by a backend operation. New APIs must be added to `API_BINDINGS`.
5. **The API gate fails open on unexpected exceptions** (`except Exception: return None`) to avoid taking the whole app down. In production this should be fail-closed with structured logging/alerting.
6. **Audit log is a JSON append list**, not an immutable/tamper-evident store. Suitable for the demo; production should use an append-only database table.
7. **Custom permission definitions are definition-only.** By design they never grant access; they require a real backend binding before becoming enforceable.
8. **Not re-verified in this phase:** the full 113-page app-wide regression beyond the RBAC page and the 9 portal e2e checks; other portals' own pages were not re-swept after the scoped `.rp-v3` CSS was added (the CSS is scoped to this page, so no cross-page impact is expected).

---

## 10. Conclusion

The Roles & Access Control page is **functional, backend-connected and security-tested**, not a visual mock. Every authorized action resolves through server-side validation and the same resolver that gates direct URLs. Permissions that have a real enforcement point are labelled and enforced; definitions without one are explicitly marked `Requires Integration` and rejected when granting is attempted. The final goal chain was demonstrated in a real browser, verified at the HTTP/API layer, audited, and cleaned up.

The remaining items in §9 are integration work for production authentication, row-level scoping and additional API bindings — they are not hidden failures of this implementation.
