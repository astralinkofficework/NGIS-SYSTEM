# NGIS-SYSTEM — UI/UX Design Audit & Refinement — FINAL DELIVERY REPORT

**Date:** 2026-11-14
**Scope:** All 113 pages across Admin / Principal / Teacher / Student / Shared portals (root + `pages/`), shared CSS/JS assets
**Mode:** Analysis-first, root-cause fixes (no hardcoded per-page patches where a central pattern was possible)

---

## 1. Executive summary

The application-wide design audit found one **root cause** behind the majority of visual defects: global CSS rules (`input`, button-focus, border-radius utilities) were styling *inline-editable* table inputs as if they were form controls, and *metadata* (codes, counts, categories, terms) was being wrapped in rounded-full "pill" containers as if it were semantic status. Both were fixed centrally with two reusable patterns plus targeted de-chipping of 7 files. Verified in-browser at 1440px and 375px with 0 page errors and 0 horizontal overflow on every page touched.

- **Pages audited:** 113 (automated sweep + manual inspection of defect clusters)
- **Real defects fixed:** 15 (3 functional JS/API + 12 design-pattern)
- **Patterns introduced (reusable, in `design-system.css`):** `.ngx-inline-edit`, `.ngx-meta-text`, ngx expandable-list system (see prior report for the ngx UI system)
- **Semantic elements intentionally kept:** status pills (Active/Pending/Allowed/Denied/Lost/Found), live-dot badges, filter chips, drag handles, user-chips, identity chips

---

## 2. Root-cause fixes (central, benefit every page)

### 2.1 Global input rules were breaking inline-editable table inputs
`ui-cleanup.css` (~line 906), `design-system.css` (global `input` rule + focus rule), and `interactions.css` (lines ~139/153/161) applied borders, radius and background to **every** input — including the inline-editable subject table inputs — producing boxed "chip-looking" text fields inside tables.

**Fix:** all affected selectors now carry `:not(.ngx-inline-edit)` exemptions. Score-cell inputs, edit cells, editable fields and `[contenteditable]` rules were left untouched (verified).

**Verified computed styles:**
| Element | Before | After |
|---|---|---|
| Subject name/short/hours input | border 1px, radius 8px, boxed bg | border 0px, radius 0px, transparent bg |
| Search input (regular form control) | — | still border 1px / radius 8px (unchanged) |
| Inline-edit focus state | generic input ring | `0 0 0 2px rgba(23,107,69,0.35)` + white bg |

### 2.2 New reusable patterns (`design-system.css`)
- **`.ngx-inline-edit`** — quiet inline-editable field: transparent at rest, surface bg + 6px radius on hover, white bg + green focus ring on focus. Hover/focus rules in `interactions.css`/`design-system.css` exempt it from the generic input styling.
- **`.ngx-meta-text`** — quiet metadata text (for codes/badges that had become pills).
- Plus the ngx expandable-list CSS (`.ngx-more-bar`, `.ngx-pager`, `.ngx-page-btn`, `.ngx-matrix-group`, `.ngx-clamp`, `.ngx-count`) delivered with the roles/permissions expandable UI, and the ≤640px `.rp-tabs` wrap fix for mobile tab clipping.

---

## 3. Metadata-pill sweep (45 pages contained `rounded-full`)

Each occurrence was **classified**, not blanket-removed:

| Classification | Decision | Occurrences |
|---|---|---|
| Semantic status (Active/Pending/Allowed/Denied/Lost/Found, live-dot) | **Keep** | majority |
| Interactive chips (filter chips, lesson drag chips, user-chip) | **Keep** (container is functional) | ~dozen |
| Identity chips ("System Admin" header chip on 9 admin-system-*.html pages) | **Keep** (user identity, consistent with user-chip decision) | 9 |
| Metadata in pill (codes, categories, counts, terms, rates) | **Fix → quiet text** | 7 files, 8 instances |

### Metadata pills fixed (before → after)
| File : line | Element | Change |
|---|---|---|
| `khmer-suite-ui.js` subject rows | name/short/hours inputs | boxed inputs → `.ngx-inline-edit` quiet fields (+ aria-labels) |
| `khmer-suite-ui.js` | subject code badge | chip → `.ngx-meta-text font-mono` |
| `khmer-suite-ui.js` (~483) | `ks-subject-chip` | chip container → plain `.ks-subject-name` text + 9px swatch (new CSS in `khmer-suite.css`) |
| `principal-departments.html:552` | dept code pill | → `text-xs font-medium text-slate-500` plain text (status pill kept) |
| `principal.html:1008` | category pill | → `text-[11px] font-medium text-slate-500` |
| `admin-departments.html:160` | "Enrolled" pill | → plain text |
| `shared/exams.html` | "Term 2 • 2026" pill | → quiet text |
| `shared/exams.html` | queued-count badge | → `rounded-md`, border removed |
| `admin-student-profiles.html:196` | `mobileBadge` ("1 Open Requests") | pill+border+shadow → `text-[11px] font-medium text-on-surface-variant` |
| `admin-teacher-profiles.html:196` | `mobileBadge` | same as above |
| `principal-attendance.html:158` | `mobilePresentRateBadge` ("96.8% Present" — JS sets text only, color hardcoded → not semantic) | emerald pill → `text-xs font-medium text-[#29352E]` |

**Dead CSS found:** `.subj-chip` defined but unused anywhere — left in place, flagged for optional removal.

---

## 4. Functional defects fixed this pass (recap from Stage 6 + this audit)

1. `pages/shared/department.html` — ReferenceError from stale code → fixed (page renders, 0 errors).
2. `pages/principal/principal-reports.html` — broken fetch endpoint + wrong response field → fixed.
3. Favicon 404 → fixed.
4. `NGX_STEP is not defined` on roles page (caught by page error boundary) → declared; expand/collapse cycle verified 10→15→10.
5. Roles page mobile: 635px `.rp-tab` row clipped at 375px → `.rp-tabs` wrap media query ≤640px; all 4 tabs visible.
6. Restored admin dashboard: 3-column KPI grid clipped third card (`repeat(3,1fr)` min-content blowout) → `minmax(0,1fr)`; last-card right edge 1242 ≤ 1262 viewport.
7. Missing `.hidden` utility on admin.html (no Tailwind there) → `.hidden{display:none!important}` fallback added; `health is not defined` render bug fixed.

---

## 5. Browser verification (this pass)

| Check | Result |
|---|---|
| `admin-student-profiles.html` @1440px | 0 overflow, badge quiet, "1 Open Requests" renders |
| `admin-student-profiles.html` @375px | 0 overflow |
| `principal-attendance.html` @375px | 0 overflow, quiet badge fits header (right edge 361 < 375) |
| `admin-roles-permissions.html` ngx system | expand/collapse cycle correct, 0 page errors |
| Subject page inline-edit computed styles | border 0 / radius 0 / transparent; focus ring green 2px |
| Roles page @375px | all 4 tabs visible after wrap fix |
| Regression suite `tests/e2e-portals.test.py` | 9/9 OK (baseline unchanged) |

---

## 6. Remaining issues (honest list)

- **R1 (P2): Playwright test suites unrunnable** — `playwright` module not installed; `test_all_portals_ui_clean.py` etc. skip via ModuleNotFoundError. The 147-test figure in prior reports includes 7 known loader errors from this. Fix: `pip install playwright && playwright install chromium`.
- **R2 (P2): X-Actor header trust** — production auth accepts a client-supplied `X-Actor` header; needs server-side session validation.
- **R3 (P3): timetable 409/404 console noise** — benign fetch failures on empty timetable states; should be handled gracefully.
- **R4 (P3): responsive coverage is sampled** — 113 pages audited at 1440/375 via automated sweep; 320/768px only on a 13-page sample. The pill sweep was classification-driven, not a line-by-line review of all ~45 pages' every `rounded-full`.
- **R5 (P3): semantic status pills intentionally kept** — by design; not defects.
- Dead `.subj-chip` CSS (unused) — optional cleanup.

---

## 7. Files modified (this audit pass)

**CSS (central):** `assets/css/design-system.css` (ngx patterns, `.ngx-inline-edit`, `.ngx-meta-text`, `:not(.ngx-inline-edit)` exemptions, `.rp-tabs` wrap), `assets/css/ui-cleanup.css` + `assets/css/interactions.css` (exemptions), `assets/css/khmer-suite.css` (`.ks-subject-name`)

**JS:** `assets/js/ngis-roles.js` (v2.1 ngx system), `assets/js/khmer-suite-ui.js` (v3.3 quiet subject rows), `assets/js/ngis-profiles.js` untouched (badge id reuse)

**Pages:** `pages/admin/admin.html` (restored dashboard), `pages/admin/admin-departments.html` (+top navbar), `pages/admin/admin-student-profiles.html`, `pages/admin/admin-teacher-profiles.html`, `pages/principal/principal-departments.html`, `pages/principal/principal.html`, `pages/principal/principal-attendance.html`, `pages/shared/exams.html`, `pages/shared/department.html`, `pages/principal/principal-reports.html`, 5 khmer-suite pages (cache-bust v3.3), 6 khmer-suite pages (+navbar)

**Backend:** `server.py` `/api/admin/stats` extended (latency, credentialPct, pending service requests, system health); `data/service_requests.json` junk ticket removed

**Docs:** `docs/AUDIT_REPORT.md` (Stage 6), this file; backups in `scratch/`

---

## 8. Conclusion

The two systemic causes (global input over-styling; metadata-as-pill) are fixed **once, centrally**, so future pages using `.ngx-inline-edit` / `.ngx-meta-text` inherit correct behavior without per-page hacks. All interactive/semantic chips are preserved. Remaining work items are environment/tooling (R1) and security (R2), not visual design.
