# NGIS — School Management System

A production-minded School Management System for **Northgate International School**,
serving five roles from one codebase: Super Admin, Admin, Teacher, Student, and Parent.

> **Status: Phase 0 — front-end design.**
> This phase delivers the complete front-end: a design system, app shell, login, and
> fully-populated portals for every role. It runs entirely in the browser on realistic
> mock data — no backend or database yet. The backend (Node + Express + Supabase, per the
> master prompt) is the next phase and will replace the mock data layer behind the same
> `data → view` boundary.

---

## Quick start

It's static ES modules — no build step. Serve the `client/` folder over HTTP
(modules don't load from `file://`):

```bash
cd client
python3 -m http.server 5173        # then open http://localhost:5173
# or:  npx serve .                  # any static server works
```

Open the app and sign in with any demo account — or use the **quick login** buttons
on the sign-in screen. Once in, use the **role switcher** in the top bar to preview
every portal without separate logins.

### Demo accounts

| Role | Email | Sees |
|---|---|---|
| Student | `student@ngis.edu` | own timetable, attendance, grades, assignments, documents |
| Teacher | `teacher@ngis.edu` | classes, take attendance, grade entry, assignments |
| Parent | `parent@ngis.edu` | linked children, attendance, grades, fees, smart alerts |
| Admin | `admin@ngis.edu` | people, classes & subjects, school-wide stats |
| Super Admin | `superadmin@ngis.edu` | system health, backups, security logs, maintenance mode |

_(Any password is accepted — this is a front-end-only demo; no credentials are checked.)_

---

## What's built

**Foundation**
- Design-token system (color, type, spacing, radius, shadow, motion) with full **dark mode**
- Reusable component primitives: Button, Card, StatCard, Badge, Avatar, Table, Meter,
  Skeleton, EmptyState, ErrorState, Modal, Toast, Search, plus canvas charts (line, donut, bars)
- App shell: collapsible role-aware sidebar, sticky top bar with global search (`/` shortcut),
  theme toggle, notifications, profile menu, and a demo role switcher
- Hash router, session store, theme module — all framework-free vanilla ES modules

**Portals & pages** (each with loading/empty/error states, responsive + dark mode)
- Login (branded split-screen) · Role dashboards (×5)
- Timetable (week grid) · Attendance (student calendar + teacher take-attendance)
- Grades & exams (+ report-card modal) · Grade entry (teacher)
- Assignments (filters, search, submit/create modals) · Announcements (compose)
- Documents · Fees & payments · People · Classes & subjects · My children
- System health (Super Admin) · Profile & settings · Help center

See **[`client/README.md`](client/README.md)** for the design system and architecture.

---

## Design

The north star from the master prompt is restraint — the clarity of Google Workspace,
the structure of Notion, the calm of Apple HIG. The identity spends its one bold note on an
**academic-crest palette: slate-blue + honor-gold**, where gold is reserved strictly for
achievement (GPA, honor roll, scholarships, streaks) and everything else stays disciplined
blue and neutral. Type pairs **Fraunces** (editorial display) with **Plus Jakarta Sans**
(UI) and **JetBrains Mono** (IDs and codes).

---

## Project structure

```
client/
  index.html
  src/
    styles/     tokens.css · global.css · shell.css · auth.css · pages.css
    modules/    router · store · theme · dom · icons · mockData
    components/ ui · shell · modal · toast · charts
    pages/      login · dashboard · timetable · attendance · grades · assignments
                announcements · documents · fees · people · classes · children
                system · profile · help
    app.js      bootstrap (auth → shell → router)
```

Layering mirrors the eventual full system: **pages** compose **components**, which read
from a **data module** (`mockData.js`) through a stable boundary. Swapping `mockData` for a
real `api/v1` client is the only change those views need.

See **[`ASSUMPTIONS.md`](ASSUMPTIONS.md)** and **[`QUESTIONS.md`](QUESTIONS.md)** for
decisions made and questions still open.
