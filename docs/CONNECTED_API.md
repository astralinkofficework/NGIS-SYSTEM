# NGIS Connected ERP — API Map

Run the connected stack:

```bash
npm install
npm run db:init
npm run db:seed
node server-v2.js
```

Open: `http://localhost:3000`

## Demo accounts (password: `password123`)

| Role    | Email                      |
|---------|----------------------------|
| Admin   | admin@ngis.edu.kh          |
| Teacher | sophea@ngis.edu.kh         |
| Student | nrinphouneta@ngis.edu.kh   |
| Parent  | parent.hok@gmail.com       |

---

## Auth

| Method | Path | Access |
|--------|------|--------|
| POST | `/api/auth/login` | Public |
| GET | `/api/auth/me` | Authenticated |
| POST | `/api/auth/change-password` | Authenticated |

## Students

| Method | Path | Access |
|--------|------|--------|
| GET | `/api/students/me` | Student |
| GET | `/api/students` | Admin |
| POST | `/api/students` | Admin (create) |
| GET | `/api/students/:id` | Role-scoped |

## Parent

| Method | Path | Access |
|--------|------|--------|
| GET | `/api/parent/children` | Parent |
| GET | `/api/parent/children/:studentId` | Parent (linked) |
| GET | `/api/parent/children/:studentId/grades` | Parent (linked) |

## Academics

| Method | Path | Access |
|--------|------|--------|
| GET/POST | `/api/assignments` | Role-scoped |
| POST | `/api/assignments/:id/submit` | Student |
| POST | `/api/assignments/:id/grade` | Teacher |
| GET/POST | `/api/grades` | Role-scoped |
| GET/POST | `/api/attendance` | Role-scoped |

## Communications

| Method | Path | Access |
|--------|------|--------|
| GET/POST/PATCH/DELETE | `/api/announcements` | Role-scoped |
| GET | `/api/notifications` | Authenticated |
| POST | `/api/notifications/:id/read` | Owner |
| POST | `/api/notifications/read-all` | Owner |

## Admin

| Method | Path | Access |
|--------|------|--------|
| GET | `/api/admin/students` | Admin |
| GET/POST | `/api/admin/teachers` | Admin |
| GET/POST | `/api/admin/parents` | Admin |
| POST | `/api/admin/link-parent-student` | Admin |

---

## Connected UI pages

| Page | Role |
|------|------|
| `pages/student/student-assignments.html` | Student |
| `pages/student/student-grades.html` | Student |
| `pages/student/student-announcements.html` | Student |
| `pages/student/student-notifications.html` | Student |
| `pages/student/student-profile.html` | Student (change password) |
| `pages/teacher/teacher-assignments.html` | Teacher |
| `pages/teacher/teacher-attendance.html` | Teacher |
| `pages/teacher/teacher-announcements.html` | Teacher |
| `pages/parent/parent-grades.html` | Parent |
| `pages/parent/parent-attendance.html` | Parent |
| `pages/parent/parent-announcements.html` | Parent |
| `pages/parent/parent-notifications.html` | Parent |
| `pages/admin/admin-students.html` | Admin |
| `pages/admin/admin-accounts.html` | Admin |

## Architecture notes

- Single SQLite database (`backend/db/ngis.sqlite`)
- JWT auth + role middleware
- One source of truth for all four portals
- Grade create auto-notifies the student
