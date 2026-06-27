# MASTER BUILD PROMPT — School Management System (Production-Ready SaaS)

> **Purpose of this document.** This is the single source of truth for building a secure, scalable, multi-tenant-ready School Management System. It is written to be handed directly to an AI coding agent **or** a development team. It defines *what* to build, *how* to build it, *in what order*, and *how we will know it is done*.

---

## 0. HOW TO USE THIS PROMPT (Instructions to the Builder)

Read this entire document before writing any code. Then:

1. **Confirm scope.** Build strictly in the phase order defined in §16. Do **not** build Phase 2/3 features before Phase 1 is complete and passing acceptance criteria.
2. **Ask before assuming.** If any requirement is ambiguous or conflicts with another, stop and list your questions in a `QUESTIONS.md` file rather than guessing. Record every assumption you *do* make in `ASSUMPTIONS.md`.
3. **No placeholders shipped as "done."** Every feature marked complete must be wired end-to-end: UI → API → database → response → UI state (loading, success, empty, error).
4. **Follow the conventions** in §4–§9 exactly (naming, error envelope, auth, RBAC). Consistency matters more than cleverness.
5. **Security and data integrity are non-negotiable.** A feature that works but leaks data or skips an authorization check is a failed feature.
6. **Deliver in vertical slices.** Each slice = one role + one feature working fully, not "all backends, then all frontends."
7. **Test as you go.** No feature is "done" without the tests defined in §18.
8. **Flag stack risks.** You may implement the stack in §3 as specified, but if a choice materially threatens the performance targets in §6, note it in `ASSUMPTIONS.md` with a recommended alternative — do not silently substitute.

**Definition of "production-ready" for this project:** secure by default, observable (logs + health checks), recoverable (backups + restore tested), documented (README + API docs), and load-tested against the targets in §6.

---

## 1. PRODUCT VISION

A modern school operating system serving five roles (Super Admin, Admin, Teacher, Student, Parent) from one codebase. It manages the full academic lifecycle: enrollment, classes, timetables, attendance, assignments, grades/exams, report cards, fees, announcements, messaging, documents, and analytics.

**Design north star:** the clarity of Google Workspace, the structure of Notion, the restraint of Apple Human Interface Guidelines. Calm, fast, obvious. Animations are subtle and functional, never decorative.

**Non-goals (explicitly out of scope unless promoted later):** payment gateway integration beyond recording payments (Phase 3), native mobile apps (web-responsive only), AI tutoring, video conferencing.

---

## 2. SCOPE PHILOSOPHY — "MVP" vs FULL PLATFORM

The original brief lists a complete enterprise platform under the word "MVP." To keep delivery realistic and de-risked, requirements are split into phases (§16). **Nothing from the original brief is dropped** — it is sequenced.

- **MVP (Phase 1)** = the smallest version a real school could run a term on: auth, RBAC, users, classes, timetable, attendance, assignments, grades, announcements, basic dashboards, report-card PDF.
- **Phase 2** = engagement and depth: notifications, messaging, calendar, documents vault, analytics, smart alerts, 2FA.
- **Phase 3** = operations and scale: fees/payments, audit/device logs UI, backups/restore UI, branding, maintenance mode, advanced admin tooling.

---

## 3. TECH STACK

| Layer | Choice | Notes |
|---|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript (ES modules) | Component-based modular architecture; a small client router; no heavy framework. See §5 for structure. |
| Backend | Node.js (LTS) + Express.js | Layered: routes → controllers → services → repositories. |
| Database | Supabase PostgreSQL | Use SQL migrations (not ad-hoc changes). Row Level Security where applicable. |
| File storage | Supabase Storage | Bucket structure in §13. Signed URLs only; no public buckets for student data. |
| Auth | JWT access + rotating refresh tokens | Session + device tracking table. TOTP 2FA (Phase 2). See §8. |
| Edge/CDN/WAF | Cloudflare | TLS, WAF rules, rate limiting at edge, caching static assets. |
| Caching | In-memory + Redis-compatible (optional) | Cache reference data (subjects, classes), hot dashboard queries. |
| Connection pooling | Supabase pooler / PgBouncer | Required to survive concurrent load (§6). |
| Deployment | Docker + docker-compose | 12-factor config via env vars (§17). Multi-stage build. |

> **Stack note (flag, don't override):** Vanilla JS at this feature depth is workable but demands disciplined module boundaries and a tiny client-side router/state layer. Implement it cleanly per §5; if it threatens the §6 targets, log the concern.

---

## 4. ARCHITECTURE PRINCIPLES

- **Separation of concerns.** No SQL in controllers, no business logic in routes, no DOM logic in data modules.
- **Single responsibility components.** Reusable UI primitives (Button, Card, Table, Modal, Toast, Skeleton, EmptyState, ErrorState).
- **Stateless API.** Auth via tokens; no server session affinity (horizontal scaling friendly).
- **Idempotent + predictable.** Same input → same output. Mutations validated server-side regardless of client validation.
- **Fail safe.** On error, default to *deny* (authorization) and *show error state* (UI), never silent failure.
- **Observability built in.** Structured JSON logs, request IDs, `/health` and `/ready` endpoints.

---

## 5. PROJECT STRUCTURE (reference)

```
/server
  /src
    /routes        # HTTP routing only
    /controllers   # request/response, validation orchestration
    /services      # business logic, authorization decisions
    /repositories  # DB access (parameterized queries / Supabase client)
    /middleware    # auth, rbac, rateLimit, errorHandler, requestId
    /validators    # input schemas (zod/joi)
    /lib           # jwt, storage, mailer, logger, cache
    /jobs          # backups, alert evaluation, cleanup
  /migrations      # ordered SQL migrations
  /tests
/client
  /src
    /components    # reusable UI primitives
    /pages         # per-role views
    /modules       # api client, auth, router, store, theme, i18n
    /styles        # design tokens + global CSS
    /assets
/docker
README.md  .env.example  ASSUMPTIONS.md  QUESTIONS.md
```

---

## 6. NON-FUNCTIONAL REQUIREMENTS (measurable)

- **Concurrency:** sustain **5,000 concurrent users** with no error-rate increase.
- **Latency:** initial page load **< 2.0s** on a typical connection; API **p95 < 300ms** for reads, **p95 < 600ms** for writes.
- **Availability target:** 99.9% (design for it; document single points of failure).
- **Performance techniques (required):** skeleton loaders, lazy loading, code splitting per route, server-side pagination, response caching of reference data, image optimization (WebP + responsive sizes), gzip/brotli compression, debounced search, virtualized long lists.
- **Rate limiting:** per-IP and per-user limits; stricter limits on auth endpoints (login, refresh, password reset).
- **Accessibility:** WCAG 2.1 AA — keyboard navigable, focus states, ARIA roles, color-contrast compliant in both themes.

---

## 7. SECURITY REQUIREMENTS (OWASP-aligned)

Implement all of the following and document each in `SECURITY.md`:

- **Authentication:** bcrypt/argon2 password hashing; email verification; account lockout / backoff after repeated failures; TOTP 2FA (Phase 2).
- **Authorization:** centralized RBAC middleware enforcing the matrix in §10 on **every** endpoint. Never trust the client's claimed role.
- **Injection:** parameterized queries only (no string-concatenated SQL); validate/escape all input.
- **XSS:** output encoding, Content-Security-Policy header, sanitize rich text.
- **CSRF:** CSRF tokens for cookie-based flows; SameSite cookies.
- **Transport:** HTTPS only (HSTS); secure, httpOnly, SameSite cookies for refresh tokens.
- **Secrets:** env-var driven; never committed; rotated.
- **Sessions:** access-token TTL ~15 min; refresh rotation with reuse detection; device/session table with revoke-all.
- **Auditing:** immutable audit log of sensitive actions (login, role change, grade edit, fee change, data export). IP + device captured.
- **Data exposure:** least-privilege queries; signed Storage URLs; mask/redact PII in logs.
- **Headers/edge:** Cloudflare WAF, rate limiting, bot mitigation; standard security headers (X-Frame-Options, X-Content-Type-Options, Referrer-Policy).

---

## 8. AUTH & SESSION DESIGN (concrete)

- **Login** → returns short-lived access JWT (claims: `sub`, `role`, `school_id`, `exp`) + sets rotating refresh token (httpOnly cookie).
- **Refresh** → issues new access token, rotates refresh token, records device/session; detects token reuse → revoke session family + alert.
- **Logout** → revokes current session; "logout all devices" revokes the family.
- **2FA (Phase 2)** → TOTP enrollment + backup codes; required for Admin/Super Admin.
- **Password reset** → time-boxed signed token via email; invalidates existing sessions on completion.
- **Device tracking** → table records device fingerprint, IP, user agent, last seen, status (active/revoked).

---

## 9. API CONVENTIONS

- **Style:** REST, resource-based, plural nouns: `/api/v1/students`, `/api/v1/classes/:id/attendance`.
- **Pagination:** `?page=`, `?limit=` (default 25, max 100) → response includes `meta: { page, limit, total, totalPages }`.
- **Filtering/sorting:** `?sort=-createdAt&status=pending&q=search`.
- **Status codes:** 200/201 success, 400 validation, 401 unauthenticated, 403 unauthorized, 404 not found, 409 conflict, 422 semantic error, 429 rate-limited, 500 server.
- **Error envelope (always):**
  ```json
  { "error": { "code": "VALIDATION_ERROR", "message": "Human readable", "details": [], "requestId": "uuid" } }
  ```
- **Success envelope:** `{ "data": ..., "meta": ... }`.
- **Versioning:** prefix `/api/v1`. **Idempotency keys** on payment/mutation-sensitive endpoints.

---

## 10. ROLES & PERMISSION MATRIX (RBAC)

**Super Admin** is permanent: cannot be deleted, removed, suspended, or have role downgraded — enforce at DB constraint + service layer + UI.

| Capability | Super Admin | Admin | Teacher | Student | Parent |
|---|:--:|:--:|:--:|:--:|:--:|
| Manage admins / system settings | ✅ | ❌ | ❌ | ❌ | ❌ |
| Cloudflare / DB / storage health, backups, device & security logs, branding, maintenance mode | ✅ | ❌ | ❌ | ❌ | ❌ |
| Manage students/teachers/parents, classes, subjects, timetables | ✅ | ✅ | ❌ | ❌ | ❌ |
| Fees & payments, school years, departments, reports, audit logs | ✅ | ✅ | ❌ | ❌ | ❌ |
| Take/edit attendance (assigned classes) | ✅ | ✅ | ✅ (assigned) | ❌ | ❌ |
| Enter/edit grades (assigned classes) | ✅ | ✅ | ✅ (assigned) | ❌ | ❌ |
| Create/grade assignments | ✅ | ✅ | ✅ (assigned) | view/submit | view |
| Post announcements | ✅ school-wide | ✅ school-wide | ✅ class/subject | ❌ | ❌ |
| View own academic data | — | — | own teaching data | ✅ self only | linked children only |
| Messaging | ✅ | ✅ | ✅ | Phase 2 | ✅ (teachers/admin) |
| Delete Super Admin | ❌ | ❌ | ❌ | ❌ | ❌ |

**Data-scoping rule:** Teachers see only assigned classes/students; Students see only their own records; Parents see only linked children. Enforce in the service layer for every query.

---

## 11. DATA MODEL (core schema)

Normalized PostgreSQL. All tables include `id (uuid pk)`, `created_at`, `updated_at`, and `school_id` (tenant key for future multi-school). Use FKs + indexes on all foreign keys and on common filter columns.

- **users** — id, email (unique), password_hash, role_id, status, email_verified, two_factor_enabled, last_login_at
- **roles** — id, name (super_admin/admin/teacher/student/parent), permissions (jsonb)
- **students** — user_id, student_id (unique, locked), class_id, enrollment_date, guardian links, academic_history (locked)
- **teachers** — user_id, employee_id (unique, locked), department_id, subjects (m2m)
- **parents** — user_id; **parent_student** (m2m link table)
- **classes** — name, grade, homeroom_teacher_id, school_year_id
- **subjects** — name, code; **class_subject_teacher** (assignment join)
- **timetables** — class_id, subject_id, teacher_id, day_of_week, period, start_time, end_time, room
- **attendance** — student_id, class_id, date, status (present/late/absent/excused), note, recorded_by
- **exams** — name, subject_id, class_id, date, max_score, status (upcoming/completed)
- **grades** — student_id, exam_id/subject_id, score, semester, comment, entered_by
- **assignments** — title, description, subject_id, class_id, teacher_id, due_at, attachments
- **submissions** — assignment_id, student_id, files, submitted_at, status (submitted/pending/overdue), grade, feedback
- **documents** — owner scope, type (report_card/certificate/letter/exam_slip/lesson_plan…), storage_path, version
- **announcements** — title, body, category, scope (school/class/subject), pinned, audience, created_by
- **notifications** — user_id, type, payload, read_at
- **fees / payments** — fee plans, amounts, due_dates, scholarships, discounts; payments record amount, date, method, receipt; balances derived
- **messages** — thread_id, sender_id, recipient_id, body, read_at
- **calendar_events** — type (holiday/exam/event/parent_meeting/sports), date(s), audience
- **audit_logs** — actor_id, action, entity, before/after (jsonb), ip, device, timestamp (immutable)
- **system_logs**, **devices/sessions**, **backups** (status, type, size, location, timestamp)

Provide an **ER diagram** in the README and ordered SQL migrations.

---

## 12. FEATURE SPECIFICATIONS BY PORTAL

Each feature below must ship with: loading (skeleton), empty, error, and success states; server-side validation; RBAC scoping; pagination on lists.

### 12.1 STUDENT PORTAL
- **Dashboard:** welcome, today's classes, upcoming exams, attendance %, announcements; quick actions (download report card, open assignments, view timetable, view announcements).
- **Timetable:** daily + weekly views; subject, room, teacher.
- **Attendance:** present/late/absent counts, %, monthly calendar, charts.
- **Grades & Exams:** subject scores, semester averages, GPA, optional ranking, teacher comments; PDF report-card download; exam schedule (upcoming/completed).
- **Assignments:** list with title, description, subject, deadline countdown, attachments, teacher comments; upload PDF/images/docs; status (submitted/pending/overdue); search + filters (all/pending/submitted/overdue).
- **My Documents:** download report cards, certificates, letters, exam slips (signed URLs).
- **Announcements:** categories (school/class/sports/emergency/events).
- **Notifications:** new assignment, exam tomorrow, fee due, new announcement.
- **Calendar:** holidays, exams, events, parent meetings.
- **Profile:** editable photo/phone/address/emergency contact; locked student ID/academic history/assigned class.
- **Help Center:** FAQ, report issue, contact administration.
- **Premium UX:** digital student ID, dark mode, favorite subjects, global search, online/offline status, export buttons, skeletons, mobile responsive.

### 12.2 TEACHER PORTAL
- **Dashboard:** welcome, today's classes/schedule, total students, pending reviews, today's attendance, notifications, announcements, upcoming deadlines, recent activity; quick actions (take attendance, enter grades, create assignment, post announcement).
- **My Classes:** roster, student count, homeroom label, student search, grade/homeroom filters.
- **Attendance:** present/late/absent/excused; bulk attendance; history; notes.
- **Grades:** input/update, bulk import, comments, exam management.
- **Assignments:** create, upload files, deadlines, grade submissions, feedback; status (open/due soon/overdue/closed).
- **Documents:** upload lesson plans/worksheets/PDFs/exam papers; search; version history; download.
- **Announcements:** class/subject/homework reminders; pin; notification send; Telegram integration (Phase 2).
- **Analytics:** average class score, attendance trend, completion rate, performance trend.
- **Student Insights:** flags for at-risk, low attendance, excellent performance.
- **Profile:** editable photo/phone/email/language/password; locked employee ID/subjects/official records.
- **Support:** IT request, report issue, FAQ, contact admin.

### 12.3 PARENT PORTAL
- **Dashboard:** children count, today's attendance, upcoming exams, pending assignments, outstanding fees, announcements; quick actions (attendance, grades, pay fees, announcements).
- **My Children:** photo, student ID, class, grade, homeroom teacher; switch between children.
- **Attendance:** present/late/absent, %, calendar, excused; alerts (absent/late/present today).
- **Grades & Exams:** GPA, scores, semester averages, comments, report cards, exam schedules, PDF download.
- **Assignments:** title/subject/due date/status; filters (all/pending/submitted/overdue).
- **Fees & Payments:** total/paid/remaining, due dates, history, scholarships, discounts, receipt download. (Recording + display in scope; gateway in Phase 3.)
- **Announcements:** school/class/events/emergency/exams; pin; mark as read.
- **Calendar:** holidays/exams/events/parent meetings/sports day.
- **Messaging:** message teachers & administration; read/send/replies.
- **Documents:** report cards, certificates, enrollment letters, exam schedules.
- **Notifications:** child absent, new assignment, exam tomorrow, tuition due, announcement.
- **Smart Alerts:** 3 consecutive absences, GPA drop, overdue assignment, excellent performance.
- **Child Progress Overview:** attendance %, GPA, assignments completed %, upcoming exams.
- **Profile:** editable photo/phone/email/language/password; locked grades/attendance/official records.

### 12.4 ADMIN PANEL
Manage: users, roles, classes, subjects, timetables, fees, payments, announcements, school years, departments, storage, audit logs, reports. (Cannot touch Super Admin account.)

### 12.5 SUPER ADMIN PANEL
Everything Admin can do, plus: Cloudflare settings, database health, storage health, API monitoring, backups, security logs, device logs, school branding, maintenance mode.

---

## 13. FILE STORAGE (Supabase)

Buckets/folders — **private by default, signed URLs only**, path-scoped by role/owner:
```
students/  teachers/  parents/  assignments/  report-cards/
certificates/  exam-slips/  documents/  avatars/  announcements/
```
Rules: validate file type + size on upload; virus/MIME check; never expose raw bucket URLs for PII; enforce storage RLS matching the RBAC matrix.

---

## 14. BACKUP & DISASTER RECOVERY

- **Daily automatic backups** of database + storage + documents/images/reports.
- **Backup logs** (status, type, size, location, timestamp) surfaced in Super Admin panel.
- **Restore system** with a documented, *tested* restore runbook (a backup you've never restored is not a backup).
- Define **RPO ≤ 24h** and **RTO** target; document both.

---

## 15. UI/UX SYSTEM

- **Themes:** white / soft gray base, blue accent, full dark-mode support; design tokens for color, spacing, radius, shadow, typography.
- **Layout:** desktop-first, tablet + mobile responsive; sticky + collapsible sidebar; top nav bar.
- **Components (reusable):** modern rounded cards, smooth transitions, professional charts, progress bars, toast notifications, skeleton loaders, empty states, error states.
- **Global features:** dark mode, global search, mobile responsive, skeleton loading, online/offline status, fast loading, pagination, export buttons, toast notifications, keyboard shortcuts, accessibility support.
- **Motion:** subtle, ≤200ms, easing-based; respect `prefers-reduced-motion`.

---

## 16. PHASED DELIVERY ROADMAP

**Phase 0 — Foundation:** repo, Docker, env config, migrations, design tokens/components, auth (login/refresh/logout), RBAC middleware, error envelope, logging, health checks, seed data.

**Phase 1 — MVP (a school can run a term):** user/class/subject/timetable management; attendance (teacher entry + student/parent view); assignments (create/submit/grade); grades & exams; report-card PDF; announcements; role dashboards; profiles; help center; global UX (dark mode, search, skeletons, pagination, toasts).

**Phase 2 — Engagement:** notification center, smart alerts, messaging, calendar, documents vault + versioning, analytics & student insights, 2FA, email verification polish, Telegram integration.

**Phase 3 — Operations & scale:** fees/payments + receipts, audit/device/security log UIs, backup/restore UI, branding, maintenance mode, API monitoring, performance hardening + load test to 5,000 concurrent users.

---

## 17. CONFIGURATION & DEPLOYMENT

- 12-factor: all secrets/config via env vars; ship `.env.example`.
- Required env keys (example): `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET`, `ACCESS_TTL`, `REFRESH_TTL`, `STORAGE_BUCKET_PREFIX`, `SMTP_*`, `CLOUDFLARE_*`, `RATE_LIMIT_*`, `NODE_ENV`.
- Multi-stage Dockerfile + docker-compose (app, db pooler, optional cache).
- Production build: minified/compressed assets, source maps stored separately, no debug logging.

---

## 18. TESTING & QA

- **Unit tests:** services, validators, RBAC decisions.
- **Integration tests:** every API endpoint incl. authz failure paths (403 when out of scope).
- **E2E (happy + unhappy):** key flows per role (login, take attendance, submit assignment, view grades, post announcement).
- **Security tests:** authz bypass attempts, injection, XSS, CSRF, rate-limit, token reuse detection.
- **Load test:** ramp to 5,000 concurrent users; record p95 latency + error rate against §6.
- **Accessibility audit:** automated + keyboard-only pass.
- A feature is **not done** until its tests pass and its empty/error/loading states are verified.

---

## 19. DEFINITION OF DONE (per feature)

- [ ] RBAC enforced server-side and data correctly scoped
- [ ] Server-side validation + proper error envelope
- [ ] Loading (skeleton), empty, error, success states implemented
- [ ] Responsive (desktop/tablet/mobile) + dark mode + a11y
- [ ] Pagination/filter/sort on lists
- [ ] Audit log entry for sensitive mutations
- [ ] Unit + integration tests passing
- [ ] Documented in API docs / README

---

## 20. DELIVERABLES

1. Running app via `docker-compose up` with seed data and demo accounts (one per role).
2. Ordered SQL migrations + ER diagram.
3. README (setup, env, architecture overview), API docs, `SECURITY.md`, restore runbook.
4. `ASSUMPTIONS.md` and `QUESTIONS.md`.
5. Test suite + load-test results.

**Demo accounts to seed:** `superadmin@`, `admin@`, `teacher@`, `student@`, `parent@` (linked to the student), with realistic sample classes, timetable, attendance, assignments, grades, and announcements so every screen has data.

---

## 21. OPEN DECISIONS TO CONFIRM BEFORE BUILD

1. Single school now, or design tenant key for multi-school from day one? (Recommended: keep `school_id` everywhere even if single-tenant.)
2. Grading scale + GPA formula (e.g., 4.0, percentage, letter)? Provide the exact formula.
3. Academic structure: semesters vs terms vs trimesters? Number of grading periods?
4. Fees: currency, supported payment methods, whether online payment gateway is in scope for Phase 3.
5. Languages for i18n (which locales, RTL needed?).
6. Notification channels for Phase 2: in-app only, email, Telegram — and priority order.

---

*End of master prompt. Build in phase order. When in doubt, deny access, show an error state, and ask a question rather than guess.*
