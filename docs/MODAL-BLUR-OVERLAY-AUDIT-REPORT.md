# NGIS-SYSTEM — Modal Blur, White Overlay & Visibility Audit — FINAL REPORT

**Date:** 2026-11-14
**Primary reference:** Register New Teacher modal (3-step wizard, `admin-users-*.html` × 5 pages)
**Scope:** All portals (Admin / Principal / Teacher / Student / Shared), all modal systems, all form controls
**Method:** Real-browser DOM + computed-style + CSSOM inspection (no guessed property fixes)

---

## 1. What was inspected

- The full modal stack on `admin-users-teachers.html`: backdrop (`.nrg-backdrop` → global `.smx-modal-backdrop`), modal container (`.ngis-modal`), stepbar, panes, fields, footer — computed styles of every layer (`background`, `backdrop-filter`, `opacity`, `z-index`, `filter`, borders).
- The global modal architecture in `design-system.css` (§ "Global Modal & Popup UI System") covering 15+ backdrop/modal class systems (`smx-`, `ngis-`, `rp-`, `ks-`, `lf-`, `srv-`, `si-`, `cms-`, `oak-`, `dialog::backdrop`).
- Global input styling layers that compete on every text field app-wide: `interactions.css`, `design-system.css`, `ui-cleanup.css`, `shared-components.css`, plus Tailwind v4 preflight/forms injected inline.
- The design-token layer (`design-tokens.css`) vs. every `var(--token-*)` consumer.
- Sweep for pseudo-element/gradient overlays, `mix-blend-mode`, and scroll-fade gradients (only benign 1.5px bottom-nav hairlines found).

**Verified correct (no fix needed):** backdrop dim+blur (rgba(15,23,20,.42)/blur 6px, z-2000) sits strictly behind the modal (opaque white, z-2001, `filter: none`); no overlay intercepts modal clicks; entrance/exit animation classes resolve; scroll lock releases on close (X and Esc).

---

## 2. Root causes found (3 — all systemic)

### RC1 — Step indicators faded to 45% (the screenshot symptom)
`ngis-register.js` sets the `disabled` attribute on all non-completed **step buttons** (including the active one) purely as a click-guard. The global disabled rule `shared-components.css:264` — `button:disabled { opacity: .45 !important }` — then faded **every** step indicator to 45%, making "1 Information — 2 Credentials — 3 Review" unreadable.

**Fix** (`ngis-register.css`, scoped shield section): `html body .nrg-backdrop button.nrg-step { opacity: 1 !important }` with `cursor` split for enabled/disabled steps. Native `disabled` still blocks clicks + stays announced to AT. Also bumped upcoming-step label color `#8FA095` → `--nrg-muted` `#64746A` (contrast on `#F7F9F7` was ~2.4:1).

### RC2 — **68 design tokens used but never defined** (app-wide washed-out forms)
`shared-components.css` consumes a `--token-*` namespace (`--token-space-2/3`, `--token-target-min`, `--token-radius-md`, `--token-text-*`, `--token-accent*`, `--token-status-*-bg/border/text`, …) that was **never defined anywhere**. `design-tokens.css` (the intended single source of truth) defines a `--color-*` namespace — the bridge was missing. Every declaration using an undefined token became *invalid at computed-value time* and silently fell back to initial values. Consequences:
- **Every text input/select/textarea app-wide had `padding: 0`** → 23px-tall cramped fields with weak contrast (exactly the "faded form fields / weak input contrast" in the screenshot).
- `app.css:38-55` maps `--primary`, `--text-primary`, `--accent`, … to these tokens **without fallbacks** — the app's own semantic variables were broken.

**Fix:** added the complete `--token-*` bridge layer to `design-tokens.css` (spacing scale, control sizing, typography, radii, accent/danger/status triads, motion, focus ring) + dark-theme overrides — mapping only to already-defined tokens, zero new colors. Result: inputs regain `padding: 8px 12px`, `min-height: 36px`, `radius: 8px`, correct text color; status pills regain their tint/border/text colors; `app.css` semantic vars resolve.

### RC3 — Inputs forced white even in dark theme (invisible text)
Global input rules pinned literal `#FFFFFF` backgrounds with `!important` (`design-system.css:735`, `interactions.css` hover/focus, `ui-cleanup.css` `--input-bg`): in dark theme inputs stayed white while text turned light → unreadable while typing.

**Fix:** theme-aware values — `var(--color-surface, #FFFFFF)` / `var(--input-bg, #F7F9F7)` / `var(--input-border, …)` — plus dark overrides `--input-bg: #1F2E26`, `--input-border: 1.5px solid #2D3A31` in `ui-cleanup.css`'s existing dark block (placed *after* the light `:root` so the cascade resolves correctly). Light-mode rendering is unchanged (verified computed styles).

Also: the wizard's self-themed `.nrg-input`/`.nrg-select` fields are now exempted (`:not(.nrg-input):not(.nrg-select)`) from the three global input rule-sets — same central pattern as the `.ngx-inline-edit` exemption delivered earlier.

---

## 3. Minor repairs

- `nrg-section-head` sections after the first had no top spacing (INSTITUTIONAL PLACEMENT crowded the field above) → `margin-top: 18px` for non-first section heads.
- Cache-busts: `ngis-register.css v1.2` (5 pages), `design-system.css v1.5` (10 pages).

---

## 4. Files modified

| File | Change |
|---|---|
| `assets/css/ngis-register.css` | step opacity/cursor shield override; upcoming-label contrast; section-head spacing |
| `assets/css/design-tokens.css` | complete `--token-*` bridge layer (+dark overrides) |
| `assets/css/design-system.css` | input rule: theme-aware bg; `.nrg-*` exemptions |
| `assets/css/interactions.css` | base/hover/focus input rules: theme-aware bg/border/color; `.nrg-*` exemptions |
| `assets/css/ui-cleanup.css` | input rule: `.nrg-*` exemption; dark `--input-bg/--input-border/--input-radius` overrides |
| `assets/js/ngis-register.js` | untouched (functionality preserved) |
| `pages/admin/admin-users-{teachers,students,staff,principals,admins}.html` | CSS cache-busts |

## 5. Functional regression (Phase 12) — teacher wizard, real browser

- Validation: empty required selects → step blocked with readable error banner ✔
- Step 1→2→3: stepper states correct (`is-upcoming` / `is-active` / `is-done`×2), review card with 8 rows ✔
- Back/forward navigation preserves data ✔
- Close via X and Esc; `body.ngis-modal-open` scroll lock released ✔
- No actual submissions executed (no test data created) ✔

## 6. Visual verification (Phase 11/14)

| Check | Result |
|---|---|
| Modal open @1440px (teacher + student) | backdrop blurred/dimmed, modal solid white, sharp — screenshots in `scratch/modal-audit/` |
| Stepbar | active step solid green, done = mint check badge, upcoming readable gray |
| Student wizard mobile @375px | modal 351px, 0 overflow, footer accessible |
| Dark theme wizard | dark surfaces, light readable text (was white-on-white) |
| Dark theme regular page inputs (exams) | `#1F2E26` bg + `#E8F3ED` text (was white + light text) |
| Light theme regular page inputs | `#F7F9F7`/`#29352E`/`#E1E9E3` — unchanged |
| 8 key pages post-fix | 0 console errors, 0 horizontal overflow each |
| `tests/e2e-portals.test.py` | 9/9 OK (baseline unchanged) |

## 7. Remaining issues (honest list)

- **Playwright suites still unrunnable** (`playwright` not installed) — broader viewport-matrix automation unavailable; R1 from prior audit.
- Responsive testing sampled at 1440/375 (+ wizard states); 320/768/1024/1920 not individually screenshotted this pass.
- Light-mode input **text** color moved `#000000` → `--color-text` `#29352E` (interactions.css base rule now token-driven) — visually near-identical, palette-consistent; flagged for transparency.
- Intentional `ui-cleanup.css` token nukes (`--token-border: transparent !important` etc.) remain — they define the app's "transparent cards" look and were left alone.
- The 45-page `rounded-full`/status-pill system is governed by the separate design audit (see `docs/UI-DESIGN-AUDIT-FINAL-REPORT.md`).

## 8. Before/after screenshots (`scratch/modal-audit/`)

`before-teacher-step1.png` (washed-out steps, cramped inputs) → `after-tokens-step1.png`, `tokens-student-wiz.png`, `tokens-student-wiz-375.png`, `wizard-step3-review.png`, `wizard-dark-fixed.png`, `tokens-admin-dash.png` (no dashboard regression from the token bridge).
