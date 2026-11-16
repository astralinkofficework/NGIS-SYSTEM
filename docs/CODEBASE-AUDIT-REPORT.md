# NGIS-SYSTEM — Full Codebase Audit, Simplification & Technical Debt Review

**Audit type:** READ-ONLY (no source files modified, no files deleted)
**Date:** 2026-11-16 — **Rev 2** (merged: morning audit pass + second independent pass using 4 parallel deep-audit agents over backend Python, frontend JS, all 116 HTML pages, and 28 CSS files)
**Auditor scope:** Backend Python, frontend JS, CSS, HTML page layer, data stores, tests, root artifacts
**Verification method:** grep/reference census over every page and script, `cmp`/`diff` of suspected forks, dynamic-loader tracing (layout.js loader list verified line-by-line), Python import tracing. **Confirmed** findings were verified by direct reference census; **Likely** findings need a runtime spot-check before acting.

---

## 1. Executive Summary

The codebase is a **functioning multi-portal school management system** (125+ routes, 116 pages, 5 portals) whose maintainability is being eroded by five systemic problems rather than isolated bugs:

1. **A 9,739-line `server.py` monolith** containing 125 routes, a ~930-line hardcoded seed-data dict, and inline business logic, coexisting with 12 well-structured API modules that duplicate the same boilerplate independently — via **two different registration idioms** (blueprints at `server.py:59–64` vs late `register_*_routes(app, DB)` calls at `server.py:9331–9354`).
2. **A CSS `!important` arms race** — **3,653 `!important` declarations** across `assets/css` (design-system 975, app.css 737, shared-components 565, ui-cleanup 512, ui-states 372, hero 351). `ui-cleanup.css` globally resets buttons/inputs/cards and forces `#FFFFFF !important` surfaces with no dark guard, while dark theme is implemented **six times independently** — dark mode is broken by architecture (AUDIT-026). Brand color `#176B45` is hardcoded ~430 times despite `design-tokens.css` existing; there are **20 `:root{}` token blocks across 12 files with three parallel palettes**.
3. **Massive untemplated HTML boilerplate** — 84 of 116 pages run the Tailwind **Play CDN** (a dev-only tool) at runtime; ~221 KB of inline `<style>` across 65 pages; ~100–120 identical head lines per page.
4. **Confirmed dead weight**: ~7,900 lines of JS/CSS unreachable at runtime (5 dead JS files incl. a 2,370-line `.bak` that is **publicly downloadable**), 18 orphan HTML pages, a stale forked root `layout.js`, dead CSS (skeleton-system.css, mvp-redesign.css), root junk (`--width`, `--full-page`, `--fullPage` CLI artifacts, empty `academic.db`), and 2 root debug scripts.
5. **Security-sensitive auth drift (Rev 2 — new):** identity is resolved **6+ different ways** across backend modules with different semantics; `exam_management_api.py:814–861` accepts **`?actor=` query-parameter identity** and **defaults unknown callers to an admin persona** (AUDIT-024, Critical); the universal demo password is `password123` for **any** account (`server.py:5002`) and mock tokens embed the role (`mock-jwt-token-{role}`) (AUDIT-025).

**Estimated removal/consolidation potential without functional loss:** ~25–30k lines of duplication/dead code across JS, CSS, HTML boilerplate, and Python store helpers — roughly 25% of frontend weight.

**Highest-value, lowest-risk starting point:** delete confirmed-dead artifacts + fix the two small security gaps (esc quote, exam actor spoofing) (Group A), then extract shared store/identity helpers (Group B), then attack `ui-cleanup.css`, HTML templating, and the Tailwind strategy (Group C).

---

## 2. Architecture Overview

```
Flask (server.py, port 3000, static_folder='.' → whole repo web-served, incl. .bak)
├── server.py (9,739 lines) — 125 @app.route, inline DB seed (~930 lines),
│   page gate (before_request, server.py:92–148 — reaches into roles module
│   private helper rp._identity_store() at :115), news/notifications/
│   lost&found/transcripts/overlays inline
├── Blueprint wave 1 (server.py:59–64): timetable_bp, school_config_bp,
│   admin_operations_bp, cms_bp, nav_bp, exam_bp + security_api.install(app) :70–74
├── Wave 2 (server.py:9331–9354): register_*_routes(app, DB) from student/
│   teacher/user/roles/system/data-dictionary modules
├── Engines: sidebar_nav_engine, dashboard_cms_engine, admin_operations_engine,
│   timetable_models (the ONLY atomic/locked store), academic_store (SQLite)
├── Data layer: 31 JSON stores in data/ + .data/academic.sqlite3 + .data/security.sqlite3
└── Frontend: 116 pages, no templating; layout.js app-kernel (4,254 lines) injects
    sidebar (NAV fallback :69 + published override :441–515), topbar, mobile BOTTOM
    nav (:527–577, hardcoded — NO API path), toast (:3695), and ~15 scripts/CSS
    at runtime (:3627–3692) into 107 pages
```

- **Page shell**: nav is *generated*, not hand-copied — `layout.js` fetches `/api/nav/published` (`sidebar_nav_engine.py`) with a hardcoded fallback. Best-factored layer, but nav now has **three sources** (see AUDIT-029).
- **Auth/authorization**: demo-first. Identity via `X-Actor` header / `ngis_actor` cookie / `um-session-` / `mock-jwt-token-` / — in the exam module's case — a URL query parameter. Layered RBAC (page gate → `roles_permissions_api._resolve_access` → `roles_permissions_ext.enforce_permission`) is intentional defense-in-depth.
- **Tests**: `tests/` (32 files; 68 RBAC tests + 9 e2e pass) + 2 stale root e2e scripts; naming (`e2e-portals.test.py`) escapes unittest discovery.

---

## 3. Unnecessary Complexity

### AUDIT-001 — `server.py` is a monolith mixing kernel, seed data, and business logic
**Category:** Complexity / Architecture · **Location:** `server.py` (9,739 lines); `DB` seed dict ~148–1079; news CRUD 1122–1280; notifications 1294–1330; transcripts 3784–3906; late imports 9331–9354 · **Evidence:** `grep -c "@app.route" server.py` → 125; 180 functions.
**Problem:** Edits to any inline feature require opening a 10k-line file; demo data un-versioned; two import styles coexist.
**Recommendation:** (1) Move the seed dict to `data/seed_demo.json` or `seed_demo_data.py`; (2) extract news/notifications/transcripts/lost-found into `*_api.py` modules; (3) unify registration into one style; (4) make `rp._identity_store()` a public helper (page gate currently touches another module's private API at `server.py:115`).
**Risk:** Medium (seed shape must be preserved) · **Priority:** High · **Effort:** Large · **Confidence:** Confirmed.
**Verification:** tests/ suites + e2e-portals; diff `/api/news`, `/api/notifications`, transcript responses before/after.

### AUDIT-002 — Six API modules registered via late import + function-call instead of blueprint pattern
**Location:** `server.py:9331–9354` vs blueprint registration `server.py:59–64` · **Problem:** two idioms; late registrars couple modules to global `DB`. · **Recommendation:** convert to blueprint style. · **Risk:** Low-Medium · **Priority:** Medium · **Effort:** Medium · **Confidence:** Confirmed.

### AUDIT-003 — `layout.js` is a second app kernel (4,254 lines) doing ~12 jobs
**Location:** `assets/js/layout.js` — icon loader :17–40, NAV tree :69+, published-nav fetch :441–515, BOTTOM mobile nav :527–577, `esc()` :973, topbar HTML :1518–1552, bottom-nav :1750/:3090, sidebar + 3-level accordion :2175–2467, collapse :2783, mobile drawer :2843–3090, toast :3695, script injection :3627–3692, auth bootstrap :3824, observers :4031–4102, lazy loaders :4123–4180.
**Problem:** sidebar/toast/modal/nav/script-loading coupled; any change risks regressions across 107 pages.
**Recommendation:** split incrementally (`ngis-nav-data.js`, `ngis-toast.js`, `ngis-shell.js`) behind the same global names first. Do **not** rewrite in one pass.
**Risk:** Medium · **Priority:** Medium · **Effort:** Large · **Confidence:** Confirmed.

### AUDIT-030 (Rev 2) — Two CRUD frameworks co-loaded on single pages
**Location:** `admin-student-verify.html` loads BOTH `student-management.js` (3,052 ln) and `ngis-student-workspace.js` (1,027 ln); `admin-teacher-verify.html` loads both `teacher-management.js` and `ngis-teacher-workspace.js`.
**Problem:** two list/verify/CRUD frameworks initialized on one page with the same `.smx-*` tokens — double DOM work, unclear ownership.
**Recommendation:** audit which regions each owns; retire the redundant one per page.
**Risk:** Medium · **Priority:** Medium · **Effort:** Medium · **Confidence:** Confirmed (co-loading); region ownership Needs Verification.

### AUDIT-031 (Rev 2) — Zero debounce on API-backed live search
**Evidence:** no debounce/throttle implementation exists anywhere in `assets/js`; account-directory searches hit `/api/user-mgmt/*` per keystroke.
**Recommendation:** one shared `NGISUI.debounce` for API-backed searches only (local filters need none). **Risk:** Low · **Priority:** Low · **Effort:** Small · **Confidence:** Confirmed.

---

## 4. Duplicated Logic

### AUDIT-004 — JSON store load/save boilerplate re-implemented per module
**Location:** `server.py:1122–1149` (`_save_news/_load_news`, **non-atomic** `open(...,'w')` — same pattern at `:1647, :3759, :6263`); `teacher_management_api.py:164, 350`; `student_management_api.py` (16 sites); `roles_permissions_api.py:205–223`; `user_management_api.py:90–109`.
**Problem:** hand-rolled persistence with **no atomicity** — a crash mid-write truncates `news.json`/`lost_found.json`/`transcripts.json`; concurrent requests race in-memory `DB` mutations (`server.py:9314`). The correct pattern already exists in-repo: `timetable_models.py:1047–1083` (RLock + `.tmp` + `os.replace`).
**Recommendation:** one shared `store.py`: `load(path, default)` / `save(path, obj)` with atomic write; replicate the timetable pattern. ~200–300 lines removed; consistent corruption handling.
**Risk:** Low · **Priority:** High · **Effort:** Small-Medium · **Confidence:** Confirmed.

### AUDIT-005 ⬆ REV 2: escalated to CRITICAL — identity resolution implemented 6+ ways; exam module accepts URL-parameter identity and defaults to admin
**Location & evidence (all read directly):**
- `exam_management_api.py:814–861` — `_get_current_actor()`: X-Actor → cookie → **`req.args.get('actor')` (:842)** → bearer → hardcoded persona table → **defaults unknown callers to `('ADM-2024-001', 'Sok Panha Heng')` admin (:851–853)**.
- `timetable_api.py:84–90` — trusts `X-Actor-Role` header as authorization input.
- `user_management_api.py:133–166` — `um-session-` → `mock-jwt-token-` → X-Actor; **explicit no-identity = unauthenticated (the safer design — make canonical)**.
- `security_api.py:198–221` — um-session/mock-jwt/X-Actor against `user_accounts.json`.
- `server.py:3050–3070` `_academic_user()` + `:108–110` page-gate variant; `school_configuration_api.py` splits mock tokens again.
- Role-check helpers duplicated: `_actor_is_super/_actor_is_admin` in `roles_permissions_api.py:312–317` AND `user_management_api.py:431–437`; `_require_admin` in `security_api.py:603` AND `dashboard_cms_api.py:40`; **case conventions disagree** (`security_api.py:229–234` uppercase `"ADMIN"` vs lowercase sets `timetable_api.py:80–81`).
**Problem:** anyone can act as any persona with `?actor=ADM-2024-001` on exam endpoints, or by sending nothing at all; a security fix must be applied 6+ times; case drift can pass a role in one module and bypass in another.
**Recommendation:** (1) immediately remove the `?actor=` path and the default-admin fallback in exam_management_api (reject unknown identity); (2) extract `identity.py:current_actor(request)` + `require_role(*roles)`; migrate module by module starting with exam; (3) **keep** the layered RBAC decision logic — that separation is legitimate defense-in-depth, not duplication.
**Risk:** Medium (auth touchpoint) · **Priority:** Critical · **Effort:** Small for step 1; Medium–Large for unification · **Confidence:** Confirmed.
**Verification:** RBAC suites (68 tests) + e2e-portals (9 tests) + STUDENT-403 probes + new "no identity → 401" probes per module.

### AUDIT-006 — ~4 frontend fetch wrappers + ~13 modules using raw `fetch`
**Location:** canonical `auth.js:354 NGISAuth.api`; duplicates: `khmer-suite-engine.js:603 api()`, `ngis-roles.js:99 api()`, `school-information.js:46 apiCall()`, `timetable-monitoring.js:42 fetchJSON()`, `exams-simple.js:63 api()`, `ngis-profiles.js:74` (delegates — the model); raw fetch: student-management.js (21), system-management.js (16), admin-dashboard-cms.js (13), teacher-management.js (12), admin-sidebar-manager.js (11).
**Recommendation:** migrate duplicate wrappers to `NGISAuth.api`; don't force raw-fetch migration in one batch. **Risk:** Low · **Priority:** Medium · **Effort:** Medium · **Confidence:** Confirmed.

### AUDIT-007 — 10 modal implementations, 19+ toast implementations, 16+ `esc()` copies
**Location — Toast:** canonical `ui-states.js:661 NGISUI.toast`; shim `layout.js:3695 window.toast`; copy-pasted fallbacks `admin-timetable-monitoring.js:97`, `data-dictionary.js:26–40`, `exams-simple.js:83–97`, `khmer-suite-ui.js:4808–4822`; direct calls `app.js:113,587`. **Modal:** canonical `modal-system.js` (lazy-loaded layout.js:4123), `exams-simple.js:160–168`, delegated `data-open-modal` ×2 (`layout.js:3521`, `app.js:510`), bespoke DOM in ngis-users/profiles/roles. **Confirm dialogs ×3:** `ngis-ui-kit.js:293`, `ui-states.js:902`, raw `window.confirm` (`modal-system.js:209`). **esc() ×16+:** layout.js:973, admin-sidebar-manager.js:36, data-dictionary.js:20, exams-simple.js:47, khmer-suite-data.js:691, khmer-suite-ui.js:53, ngis-components.js:12, ngis-profiles.js:37, ngis-roles.js:64, ngis-student-workspace.js:25, ngis-teacher-workspace.js:27, ngis-users.js:161, school-information.js:23, skeleton-system.js:12, academic-live.js:4, escapeHtml ×2 (student-management.js).
**Recommendation:** standardize on `modal-system.js` + `NGISUI.toast` + `NGISKit.confirmAction` + one shared `NGISUI.esc`; convert inline page copies first.
**Risk:** Low-Medium · **Priority:** High · **Effort:** Medium · **Confidence:** Confirmed.

### AUDIT-032 (Rev 2) — layout.js `esc()` does not escape single quotes (XSS gap)
**Location:** `layout.js:973` — escapes `[&<>"]` only; all 16 sibling implementations escape `'` too.
**Problem:** interpolation into single-quoted attribute context breaks escaping.
**Recommendation:** add `'` to the map — one-line fix. **Risk:** Low · **Priority:** High (small but security-relevant) · **Effort:** Small · **Confidence:** Confirmed.

### AUDIT-008 — 116 pages × ~100–120 identical head/CDN boilerplate lines, no templating; ~221 KB inline `<style>`
**Location:** all `pages/**/*.html`; `cdn.tailwindcss.com` on **84 pages** (77 with inline `tailwind.config`); inline `<style>` on **65 pages totaling ~221 KB** (worst: student-assignments ~19.6 KB, pages-directory ~17.8 KB, department.html ~14.9 KB, admin.html ~10.7 KB; two pages share an identical 646-line style block).
**Problem:** no caching for page CSS, drift between portal twins, Play CDN is dev-only (FOUC, console warning on every page, no purge).
**Recommendation:** introduce a Jinja base template or server-injected head partial; first targets: the twin exams pages and the 40 tailwind.config copies. Long-term: Tailwind strategy decision (precompile vs migrate) — see AUDIT-014/036.
**Risk:** Medium (portal-by-portal) · **Priority:** High · **Effort:** Large · **Confidence:** Confirmed.

### AUDIT-009 — Pagination, audit-log, versioning logic duplicated across stores
**Location:** `user_management_api.py:724` vs `roles_permissions_api.py:1067 _page_index()`; per-store `*_audit.json`/`*_versions.json` pairs. **Recommendation:** shared helpers. **Risk:** Low · **Priority:** Low · **Effort:** Small · **Confidence:** Confirmed.

### AUDIT-033 (Rev 2) — Timetable seed data duplicated in JS
**Location:** `khmer-suite-data.js:604` duplicates `timetable_models.build_seed_state()` (Python) — a third source of truth for seed data (also relevant to AUDIT-022 overlays).
**Confidence:** Confirmed. **Priority:** Low.

---

## 5. Outdated Assumptions

### AUDIT-010 — Hardcoded campus names, grades, principals, and institutional data
**Location:** `dashboard_cms_engine.py:32–53,125` ('Phnom Penh Main Campus'); `admin_operations_engine.py:324–376` ('Tuol Kork Main Campus' ×6); `timetable_oversight.py:60–447` (×6); `timetable_models.py:165–167` (grade→campus map); campus lists duplicated `roles_permissions_api.py:182`, `user_management_api.py:618`, `server.py:402–655` fixtures + `default 'Sensok'` (`server.py:1823`); hardcoded GPA `3.88`, DOB `'2008-04-18'` (`server.py:4959–4988`).
**Frontend:** campus map with named principals baked into JS (`admin-campus.html:38,141`); hardcoded `<option value="Chbar Ampov Campus">` (`admin-news.html:705`); "4 Campuses (Sen Sok, Depo, Bak Touk, Main)" ×6 (`admin-department-detail.html:335,680,814,834,872,892`); grade selects `cls-10a…12b` (`admin-grades.html:93–95`, `admin-classes.html:292–295,409–412`).
**Problem:** adding a campus/grade requires edits in ≥5 backend files AND several HTML files; two slightly different campus lists exist ('Sensok','TK' vs full names).
**Recommendation:** single campus/grade registry (extend `school_configuration_api`); modules read from it. Some hardcoded strings may be demo copy, not assumption — verify intent before migrating.
**Risk:** Low-Medium · **Priority:** Medium · **Effort:** Medium · **Confidence:** Locations Confirmed; demo-vs-assumption **Needs Verification**.

### AUDIT-011 — Legacy mixed API response shapes
`{'success': True, 'state', 'revision'}` + `{'error': msg}` (timetable family, `timetable_api.py:51–67` is the only `_ok/_fail` pair) vs `{'data','meta'}` + `{'error': {code, message}}` (server.py:1346). Frontends special-case per module. **Priority:** Low · **Confidence:** Confirmed.

### AUDIT-012 — AGENTS.md references a Parent portal that does not exist
`pages/parent/` has 0 files. Mark planned or remove. **Risk:** None (docs) · **Confidence:** Confirmed absence; intent Unverified.

### AUDIT-013 — Stale dual-version `__pycache__` (cpython-313 + 314) — safe cleanup.

### AUDIT-025 (Rev 2, Critical) — Demo authentication is the only authentication
**Location:** `AUTH_USERS` `server.py:2926–3036`; universal password `password == 'password123'` for **any** account `server.py:5002`; token mint `mock-jwt-token-{role}` `server.py:5004` (role read back out of the token string by timetable_api.py:88–89, exam_management_api.py:833–837, security_api.py:207–212, user_management_api.py:156–159); frontend `auth.js:46 DEMO_USERS` **auto-selects identity from the URL path** (`auth.js:141–156`) — e.g., opening any `/pages/admin/...` URL resolves an admin demo identity.
**Verdict:** acceptable **only** while the system is a demo. Blocker for any real deployment; must be replaced (server) and disabled (frontend auto-login) together. Not "removal" — replacement, requiring a product decision.
**Risk:** High (deployment) · **Confidence:** Confirmed.

### AUDIT-026 (Rev 2) — Dark mode broken by architecture
**Location:** `ui-cleanup.css:40–46` (`--token-surface` etc. forced `#FFFFFF !important`), `:116–131`, `:198` unconditional white card surfaces with no dark guard; meanwhile dark theme is implemented **six times independently** — design-system.css (149 `[data-theme="dark"]` rules), app.css (67), interactions.css (66), hero.css (63), shared-components.css (45), portal-dashboard.css (38) — all fighting ui-cleanup's white.
**Problem:** this is the root cause of the "text/icons invisible after click/hover" bug class previously patched.
**Recommendation:** make ui-cleanup theme-aware (replace hardcoded white with `var(--token-surface)` + a dark token block); verify 10 representative pages in dark mode.
**Risk:** Medium · **Priority:** High · **Effort:** Medium · **Confidence:** Confirmed (static).

---

## 6. Dead Code and Dependencies

### AUDIT-014 (Confirmed unused — safe delete list, merged Rev 2)

**JavaScript (~5,600 lines):**
| Item | Size | Evidence |
|---|---|---|
| `assets/js/ngis-users.js.bak` | 2,370 ln / 119 KB | stale backup; zero refs; **publicly served** (`server.py:52` serves `.`) — source leak |
| `assets/js/admin-timetable-monitoring.js` | 1,298 ln | zero refs anywhere (defines own toast shim at :97) |
| `assets/js/timetable-oversight.js` | 891 ln | zero refs (oversight page loads `timetable-monitoring.js`) |
| `assets/js/academic-live.js` | — | zero refs |
| `assets/js/ngis-components.js` | 353 ln | zero refs (pages load the CSS twin only) |
| Root `layout.js` | 130,851 B | stale fork of `assets/js/layout.js` (differs; missing nav entries); referenced by zero HTML |

**Note on dynamic loading:** files with zero static `<script>` tags but loaded by layout.js's runtime loader list (`layout.js:3627, 3670–3683` + lazy loaders `:4123–4180`) are **alive**: `app.js`, `ngis-copy.js`, `error-messages.js`, `error-boundary.js`, `ui-states.js`, `action-icons.js`, `semantic-states.js`, `ngis-search.js`, `smart-disclosure.js`, `skeleton-system.js`, `modal-system.js`, and all 7 `assets/components/*.js`. Do not delete these.

**CSS:**
| Item | Size | Evidence |
|---|---|---|
| `assets/css/skeleton-system.css` | 362 ln | **0 references**; `skeleton-system.js` (alive, layout.js:4178) does not reference it — upgraded to Confirmed in Rev 2 |
| `assets/css/mvp-redesign.css` | 285 ln | linked by 11 student pages, but **100% of its classes (`.mvp-command-center`, `.mvp-flow`, `.news-automation-strip`) have 0 usages** — remove link + file together |
| `profiles.css` `.pf-*` block | most of 188 ln | `.pf-kpi` 0 usages; file linked by 14 pages (Likely) |
| `assets/css/bottom-nav.css` | 611 ln | 1 page link, 0 JS refs; layout.js drives `#mobBottomNav` via app.css classes (Likely — verify mobile nav first) |

**HTML pages (18 orphan candidates — zero inbound runtime references):**
`pages/shared/404.html` (duplicate of root 404), `pages/teacher/teacher-announcements.html` (redirect stub, 0 inbound), `pages/teacher/teacher-timetable.html` (duplicate of teacher-calendar.html — same title, both live), 5× `admin-dictionary-*.html`, 4× `admin-system-*-accounts.html`, `admin-grade-release.html`, `principal-data-dictionary.html` + 5× `principal-dictionary-*.html`, `pages/shared/onboarding.html`, and **`principal-registration-approve.html` (⚠ verify first — it loads live student-management.js; it may be linked from external flows)**. Also dead-by-consumption: `all_pages_data.js` + `all_pages_data.json` + `pages-directory.html` (dev directory tool reachable from production index.html and 404 — remove public links, AUDIT-017 in Rev 1 findings).

**Root artifacts:**
| Item | Evidence |
|---|---|
| `--width` (142 KB), `--full-page`, `--fullPage` | accidental CLI-output files (screenshot-tool flags misused as filenames) |
| `academic.db` (0 bytes) | referenced by nothing; live DB is `.data/academic.sqlite3` |
| `data/security.sqlite3` (0 bytes) | stray from direct python testing; live DB is `.data/security.sqlite3` |
| `server-dev.log`, 10 root PNG screenshots | run artifacts |
| `inspect_classes_mobile.py`, `inspect_lessons.py` | one-off Playwright debug scripts; one writes to a personal path outside the repo |
| `test_principal_e2e.py`, `test_school_information_e2e.py` | root manual scripts duplicating `tests/` |
| 13 root `.md` reports (AUDIT.md, FINAL_REPORT.md, UI-FIXES.md, …) | belong under `docs/` |

**Dependencies/config (Rev 2):**
- `requirements.txt` (Flask + flask-cors) is accurate for the server; `timetable_xlsx.py:21–26` hand-builds XLSX via zipfile — no openpyxl needed.
- **Missing dev requirement:** `playwright` used by ~12 `tests/` files and root scripts — no dev-requirements file exists; suite silently fails on clean machines.
- **Test discovery broken:** `tests/e2e-portals.test.py` naming doesn't match unittest's `test*.py` pattern — only `test_*.py` files run; three tooling generations coexist.
- `node_modules/` (19 MB) holds one dependency (`bootstrap-icons`); no page references node_modules paths — verify fonts are vendored before removing.

### AUDIT-015 (Likely unused — verify at runtime first)
- `khmer-suite-ui.js` helpers `colorOf`, `headHtml`, `previewHtml` — no callers found.
- Three overlapping loading-state systems (`skeleton-system.js` / `ui-states.js` / `components/skeleton.js`) — consolidate, don't delete.
- Dead `.btn-*` variant families (`btn-forest`, `btn-yellow`, `btn-orange`, `btn-utility`, `btn-save`, `kpi-tile`, `notice-card`).

---

## 7. Frontend and CSS Findings

### AUDIT-016 — CSS `!important` arms race (3,653 declarations)
**Census (Rev 2, verified counts):** design-system.css **975** · app.css **737** · shared-components.css 565 · ui-cleanup.css 512 · ui-states.css 372 · hero.css 351 · interactions.css 275 · portal-dashboard.css 172 · roles-access.css 166 · ngis-register.css 102.
**Concrete wars (Confirmed):**
- **Placeholder war:** `design-system.css:787` `input::placeholder { color:#8FA095 !important }` → beaten only by `ngis-search.css:100` scoped `!important` (whose comment admits the war); losers: `app.css:2226`, `shared-components.css:343`, `ngis-components.css:234`, `announcements.css:68`, `ngis-register.css:205`; sidebar variant `app.css:3434` `html body #sidebar … !important` defeats ngis-search's source-order design.
- **Card neutralization:** `ui-cleanup.css:115–131` forces white `!important` on `[class*="card"]`; every later file re-paints with higher specificity (e.g., `roles-access.css:617–681` `html body .ngis-rp.rp-v3 … !important`).
**Recommendation:** do NOT mass-remove `!important` (blast radius). Surgical: fix the three concrete wars via token consolidation; scope ui-cleanup's global resets; freeze new `!important`.
**Risk:** Medium-High (visual) · **Priority:** Critical · **Effort:** Large · **Confidence:** Confirmed.

### AUDIT-017 — Hardcoded brand colors despite token file
`#176B45` ~430× in 21 files; hero.css hardcodes 166 hex + 74 rgba with 9 `var()`; design-tokens.css defines the token. Tokenize per-file when touched. **Priority:** Medium · **Effort:** Large (incremental).

### AUDIT-018 — 4 parallel button systems, 17 files styling modals, `.sidebar` in 4 files
Freeze new `.btn-*` variants; one owner for `.sidebar` (layout.js output); long-term one modal stylesheet. **Priority:** Medium.

### AUDIT-027 (Rev 2) — 20 `:root{}` blocks across 12 files, three parallel palettes with same-name collisions
`--token-*` (design-tokens.css 84 defs), `--color-*` (ngis-components 179 refs), `--ngis-*` (design-system 125). Literal collision: `--token-surface` in `ui-cleanup.css:40` (with meaningless `!important` on a custom property) AND `admin-dna.css`; shadow/border tokens in ui-cleanup vs design-tokens. **Recommendation:** design-tokens.css becomes the single source; alias legacy names; migrate file-by-file. **Priority:** High (prerequisite for AUDIT-026) · **Confidence:** Confirmed.

### AUDIT-019 — Inconsistent breakpoints (16 distinct in app.css alone; 767/768/769 and 1024/1025 overlap inconsistently). Standardize on 480/768/1024 when files are next touched. **Priority:** Low.

### AUDIT-020 — `hero.css` double-loads `design-system.css` via `@import` (:1) while 122 pages also link it directly; `pages/student/css/hero.css` is a 1,508-line near-copy. Remove `@import`; merge student copy. **Priority:** Medium · **Confidence:** Confirmed static; double-load Needs runtime verification.

### AUDIT-034 (Rev 2) — Observer accumulation
**Evidence:** `ngis-search.js:205, 212` — **two** body-level MutationObservers never disconnected; layout.js adds three more (:4031, :4063, :4097) + `action-icons.js:542` + `smart-disclosure.js:466` — up to ~7 body observers per page; layout.js: 40 addEventListener / 0 removeEventListener. Bounded per page-load (no SPA) but observers re-fire on their own injections. **Recommendation:** share one observer between ngis-search instances; verify no feedback loop. **Priority:** Low · **Confidence:** Confirmed pattern; perf impact Likely.

### AUDIT-035 (Rev 2) — Encoding defects: 6 pages contain U+FFFD replacement chars in `<title>`
`admin-logs.html:6`, `admin-reports.html:6`, `teacher-documents.html:6`, `teacher-notifications.html:6`, `student-calendar.html`, `teacher-profile.html`. One-line re-saves. **Priority:** Low · **Confidence:** Confirmed.

---

## 8. Backend and Database Findings

### AUDIT-021 — Dual sources of truth for teacher assignments; multi-store students
SQLite `.data/academic.sqlite3` `teacher_assignments` table (`academic_store.py:18,66–72`) vs JSON `data/teacher_assignments.json` (`teacher_management_api.py:164,350`); students as server fixtures + `students_overlay.json` (merged `server.py:6233, 6302–6306`) + `student_registrations.json` + sqlite; accounts as `user_accounts.json` ("authoritative") + `AUTH_USERS` + security.sqlite3. **Which store is authoritative depends on which API wrote last.**
**Recommendation:** read-census → pick one owner per entity → migrate readers. **Do not** delete either store until the census is complete.
**Risk:** High if rushed · **Priority:** High · **Effort:** Large · **Confidence:** Locations Confirmed; owner **Needs Verification**.

### AUDIT-022 — 31 JSON stores with hand-rolled persistence and no schema/version field
Fix opportunistically via the shared `store.py` (AUDIT-004) with a `$version`/`updated_at` envelope. **Priority:** Low.

### AUDIT-023 — No polling hotspots found
Only two 60s tickers (`student-inline.js:18`, `student-timetab.html:649`); layout.js's 2 fetches per page are legitimate. Avoid new duplication (admin-sidebar-manager refetching nav data 11×). **Confidence:** Confirmed.

---

## 9. Security Considerations

- **AUDIT-024/005 (Critical):** exam module's `?actor=` query-param identity + default-admin fallback must be removed first; then unify identity parsing into one `identity.py`. **Keep** the layered RBAC decision logic (page gate → `_resolve_access` → `enforce_permission`) — intentional defense-in-depth; consolidate identity *parsing* only.
- **AUDIT-025 (Critical for deployment):** `password123` universal password + role-bearing mock tokens + frontend auto-login — demo-only; replace before any real deployment.
- **AUDIT-032 (Low):** layout.js `esc()` single-quote gap — one-line fix.
- **KEEP intact:** security_api.py rate limiting/IP restrictions (recently validated); timetable MONITOR_ROLES / READONLY_TIMETABLE_ROLES separation; RBAC default-deny, protected core roles, last-Super-Admin lock, `expected_updated_at` concurrency; page-access gate default-deny.
- `pages-directory.html` shipped from production landing/404 discloses the full URL map — remove public links (keep as dev tool).
- Any auth refactor must run: 68 RBAC tests + 9 e2e + STUDENT-403 probes + new no-identity→401 probes.

---

## 10. Prioritized Recommendations (merged)

| # | Finding | Location | Recommended Action | Risk | Effort | Priority |
|---|---|---|---|---|---|---|
| 1 | AUDIT-005 (Rev 2) | exam_management_api.py:814–861 | Remove `?actor=` spoofing + default-admin fallback; reject unknown identity | Medium | Small | **Critical** |
| 2 | AUDIT-014/032 | repo-wide | Delete confirmed-dead files; fix esc() quote gap | Low | Small | **Critical** |
| 3 | AUDIT-016 | ui-cleanup.css | Scope the global reset; fix placeholder/sidebar/card wars | Medium-High | Large | Critical |
| 4 | AUDIT-026/027 | ui-cleanup + 6 files | Theme-aware ui-cleanup; design-tokens.css as single palette source | Medium | Medium | High |
| 5 | AUDIT-004 | 5 modules | Shared atomic `store.py` (replicate timetable pattern) | Low | Small-Med | High |
| 6 | AUDIT-021 | teacher_assignments | Read-census → single owner per entity | High if rushed | Large | High |
| 7 | AUDIT-008 | 116 pages | Jinja base template / injected head; then Tailwind strategy decision | Medium | Large | High |
| 8 | AUDIT-007 | 10 modal + 19 toast + 16 esc impls | Standardize on modal-system/NGISUI/NGISKit | Low-Med | Medium | High |
| 9 | AUDIT-001 | server.py | Extract seed dict + inline features to modules | Medium | Large | High |
| 10 | AUDIT-003/034 | layout.js | Incremental split; dedupe body observers | Medium | Large | Medium |
| 11 | AUDIT-006 | 7 wrappers + 13 raw-fetch modules | Consolidate on NGISAuth.api | Low | Medium | Medium |
| 12 | AUDIT-030 | verify pages | Retire duplicate framework per page | Medium | Medium | Medium |
| 13 | AUDIT-010 | 5+ backend files, 5+ pages | Campus/grade/principal registry (verify demo-vs-assumption) | Low-Med | Medium | Medium |
| 14 | AUDIT-018/017 | CSS | Freeze button variants; tokenize per-file | Medium | Large | Medium |
| 15 | AUDIT-002/013/020/025/031/033/034/035 | various | Opportunistic cleanups + planning | Low | Small-Med | Low-Med |

## 11. Safe Refactoring Roadmap (approval-gated)

### Group A — Safe Quick Wins (1 session; file census + smoke tests only)
1. Delete confirmed-dead list (§6): dead JS (~5.6k lines), dead CSS (~650 lines), root junk (`--width`, `--full-page`, `--fullPage`, `academic.db`, stray `data/security.sqlite3`, root `layout.js`, debug scripts), orphan pages (⚠ keep `principal-registration-approve.html` pending verification), move 13 root `.md` files into `docs/`.
2. Remove public links to `pages-directory.html` from `index.html` + `404.html`.
3. Fix `layout.js:973` esc() single-quote gap.
4. Remove `?actor=` query identity + default-admin fallback in `exam_management_api.py:842,851–853` (small, high-value).
5. Re-save 6 U+FFFD `<title>` files with UTF-8.
6. Add `requirements-dev.txt` (playwright); rename `tests/e2e-portals.test.py` → `tests/test_e2e_portals.py`.
7. Purge stale `__pycache__`; remove `hero.css:1` `@import`.
**Regression tests:** full `tests/` suite, full page crawl (all remaining pages) checking console + network 404s, one page per portal screenshot.

### Group B — Moderate Refactoring (2–4 sessions; per-module regression)
1. `store.py` atomic load/save — migrate one module at a time (start teacher_management).
2. `identity.py` actor unification — module-by-module after AUDIT-005 fix; RBAC suites + 403/401 probes per module.
3. Consolidate fetch wrappers, then toast/modal/confirm/esc onto NGISUI/NGISKit (per-module commits).
4. Theme-aware ui-cleanup + token consolidation (AUDIT-026/027) — screenshot-diff 10 pages light+dark.
5. Shared debounce; retire duplicate workspace frameworks on verify pages; dedupe body observers.

### Group C — Architectural (planned, portal-by-portal)
1. teacher_assignments/students ownership decision (read-census first — highest data risk).
2. server.py seed-dict extraction, then feature extraction (news → notifications → transcripts → lost-found).
3. HTML base template / head partial (portal-by-portal with screenshot diff).
4. Tailwind Play CDN strategy: precompile the 84-page utility set into one static CSS or migrate to shared component CSS — **product decision required**.
5. layout.js split; campus/grade registry; real authentication replacing demo tokens (AUDIT-025).
**Regression:** full suite after each step; screenshots at 2 widths per portal; e2e portals suite.

## 12. Do Not Change

1. **Generated navigation** (`sidebar_nav_engine.py` → `/api/nav/published` → layout.js render with fallback) — best-factored layer; 0 pages hand-copy sidebar markup. (Do unify the hardcoded `BOTTOM` mobile nav into it — AUDIT-029 below — but keep the model.)
2. **Layered authorization** (page gate → RBAC resolver → API permission gate) — intentional defense-in-depth; consolidate identity parsing only.
3. **RBAC default-deny, protected core roles, last-Super-Admin lock, `expected_updated_at` concurrency** — verified by 68 passing tests.
4. **timetable subsystem** (`timetable_models.py` atomic RLock persistence, revisions, history) — the repo's best code; use as the template for `store.py`.
5. **security_api.py** rate limiting/IP restrictions/restriction lifecycle — recently validated end-to-end.
6. **`tests/` suite structure** — extend, don't restructure.
7. **`design-tokens.css`** — the correct foundation; fix is adoption, not replacement.
8. **ngx progressive-disclosure primitives** and scoped `.rp-v3` CSS — recent, deliberate.
9. **`hero.js` dynamic hero injection**, bilingual Khmer/English patterns, **user_accounts.json as authoritative account store**, **`.data/` database paths** (delete the stray empty `data/security.sqlite3`, never `.data/`).
10. **`ngis-users.js` / `student-management.js` UX flows** — consolidate code, not behavior.

### AUDIT-029 (Rev 2) — Third nav source: hardcoded mobile BOTTOM nav
`layout.js:527–577` defines the mobile bottom nav in JS with **no API override path** — `admin-sidebar-manager.js` cannot edit it, so published nav changes silently miss mobile. Fold into Group C item 5 (nav unification). **Confidence:** Confirmed.

---

## Not Inspected / Could Not Verify

- Runtime CSS injection for `skeleton-system.js`/`smart-disclosure.js` twins (skeleton-system.css upgraded to Confirmed-dead in Rev 2 after loader-list verification; smart-disclosure.css is injected globally so it is alive).
- SQLite vs JSON authority for teacher_assignments/students (AUDIT-021) — needs read-census.
- `hero.css` double-load — confirm via DevTools network panel.
- Which hardcoded campus strings are demo data vs live assumptions (AUDIT-010) — product-owner confirmation.
- `node_modules/` contents (19 MB, one declared dependency) — verify bootstrap-icons font paths before removal.
- Performance measurements — no timings taken; all performance observations are structural (observer counts, CDN usage, payload sizes), not benchmarked claims.
- Runtime data drift between overlay JSONs and SQLite stores.
- Which UI regions each co-loaded framework owns on the verify pages (AUDIT-030).
- `tools/`, `timetable/`, `scratch/`, `.workbuddy-ai/` directory contents beyond reference tracing.
- Conflict note: `principal-registration-approve.html` has zero inbound page references but loads live `student-management.js` — may be an email/external-flow target; treat as Needs Verification, not confirmed-dead.

---

*This audit made no modifications to any source file (Rev 2 note: the only writes were this report and the session memory log). Implementation awaits explicit approval.*
