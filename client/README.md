# NGIS — Frontend (Client)

The **front-end** for the NGIS School Management System: a framework-free,
component-based UI built with **HTML5, CSS3 and Vanilla JavaScript (ES modules)**
per the master prompt (§3, §5, §15).

> This is the UI layer only. It runs against **mock data** (`src/data/mock.js`)
> so every screen is fully populated. Swap the data modules for the real
> `/api/v1/*` calls when the backend lands.

## Run it

It uses native ES modules, so it must be served over HTTP (not `file://`):

```bash
cd client
python3 -m http.server 8099
# open http://localhost:8099
```

On the login screen, click any **demo account** chip to enter that role's portal,
or sign in with one of: `superadmin@ngis.edu`, `admin@ngis.edu`,
`teacher@ngis.edu`, `student@ngis.edu`, `parent@ngis.edu` (any password).

## What's implemented

**Design system** (`src/styles/`)
- `tokens.css` — single source of truth: color, type, space, radius, shadow,
  motion, z-index. Light + full dark theme. Neutral base, blue accent (§15).
- `base.css` — reset, typography, a11y helpers, reduced-motion.
- `components.css` — Button, Card, Stat/KPI, Badge, Avatar, Table, Input,
  Tabs, Segmented, Progress/Ring, Modal, Toast, Skeleton, Empty/Error states,
  Dropdown, Tooltip.
- `layout.css` — app shell (collapsible sidebar + sticky topbar), responsive
  grid, auth screen, timetable grid, attendance calendar.

**App framework** (`src/modules/`)
- `router.js` — hash router with auth + RBAC guards.
- `auth.js` — session shape mirroring §8 (mock; no real tokens).
- `theme.js` — light/dark with persistence + system fallback.
- `nav.js` — role-based navigation mirroring the RBAC matrix (§10).
- `store.js`, `icons.js` — state pub/sub and an SVG icon set (no emojis).

**Portals** (`src/pages/`) — all five roles, each with loading/empty/error
states where relevant and realistic data:
- **Student** — dashboard, timetable, attendance (calendar + ring), grades &
  exams, assignments (filter/search), documents, announcements, calendar, help.
- **Teacher** — dashboard, classes/roster, **bulk attendance entry**, grade
  entry, assignments, documents, analytics (charts), announcements.
- **Parent** — multi-child dashboard with smart alerts + child switcher,
  children, attendance, grades, assignments, **fees & payments**, messages,
  announcements, calendar.
- **Admin** — dashboard, users (search/filter + add-user modal), classes &
  subjects, timetables, fees, reports, announcements, audit logs.
- **Super Admin** — infrastructure dashboard, users & admins (permanent
  Super Admin per §10), system health, backups, security logs, maintenance,
  branding.

## Design language

Calm, fast, obvious — the clarity of Google Workspace, the structure of Notion,
the restraint of Apple HIG. Data-dense dashboard pattern, neutral slate base
with a single blue accent, subtle ≤200ms motion that respects
`prefers-reduced-motion`, and tabular numerals throughout.

## Accessibility

WCAG 2.1 AA target: semantic landmarks, keyboard navigation, visible focus
rings, ARIA labels on icon-only controls, color never the sole signal (status
uses icon + text + color), 4.5:1 contrast in both themes.

## Notes / next steps

- Charts are hand-rolled SVG (no chart library) to honor the no-heavy-framework
  constraint.
- Mutations (save attendance, create user, pay, etc.) show optimistic toasts;
  wire them to the API services for end-to-end behavior.
- See the root master prompt for the full backend/security/testing scope.
