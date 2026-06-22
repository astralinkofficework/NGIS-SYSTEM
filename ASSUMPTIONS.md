# Assumptions

Decisions made while building **Phase 0 — front-end design**, per the master prompt's
instruction to record assumptions rather than silently guess.

## Scope
- This phase is **front-end only**, by explicit direction. No backend, database, or real
  auth is implemented. All data comes from `client/src/modules/mockData.js`.
- Authentication is mocked: any password is accepted, and the chosen role is persisted to
  `localStorage`. A demo **role switcher** lets one preview every portal without separate
  logins — this is a demo affordance and would be removed (or gated) in production.

## Stack
- Built as **vanilla HTML/CSS/ES modules with no build step**, matching the master prompt's
  Tech Stack (§3) and its note that vanilla JS is workable with disciplined module boundaries.
- No client framework or bundler was introduced. Routing, state, and theming are small
  hand-written modules. If the §6 performance targets later demand it, a light bundler
  (esbuild/Vite) can be added without restructuring.

## Brand & content
- The repo is **NGIS**, interpreted as **Northgate International School**. School name,
  people, classes, subjects, and timetable are realistic sample content so every screen has data.
- Identity colors are an **academic-crest palette (slate-blue `#2B59C3` + honor-gold
  `#C8902B`)**. The prompt suggested "blue accent"; this keeps blue as the primary while
  reserving gold strictly for achievement, to avoid a generic all-blue dashboard.
- "Today" in the demo is treated as **Monday, 22 June 2026**, and the attendance calendar
  is laid out for **June 2026** (the 1st falls on a Monday).

## Academics (deferred, but shown for realism)
- Grading is displayed as **percentage + letter grade + 4.0 GPA**, with **two semesters**.
  This was marked "decide later," so it is **not hard-coded into any formula** — the values in
  `mockData.js` are illustrative and the exact scale/formula remains an open question (see §21).

## Design
- Desktop-first, responsive to tablet and mobile (sidebar collapses behind a scrim < 1000px).
- Motion is subtle (≤200ms) and `prefers-reduced-motion` is honored.
- Fonts (Fraunces, Plus Jakarta Sans, JetBrains Mono) load from Google Fonts; system fonts
  are a graceful fallback if the CDN is blocked.

## Carried forward to the backend phase
- The boundary between views and `mockData.js` is intentional: swapping it for a real
  `/api/v1` client is the main integration point.
- `store.js` is where real JWT access/refresh handling and device/session tracking will live.
- RBAC is reflected in the UI (role-scoped nav, locked vs editable profile fields) but
  **must still be enforced server-side** — the client view is not a security boundary.
