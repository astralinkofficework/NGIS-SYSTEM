# NGIS System — Project Map

Quick reference for every file in the project. Find any section in under 10 seconds.

---

## Entry Point

| File | Purpose |
|------|---------|
| `index.html` | Login page — role selector → redirects to correct dashboard |

---

## Pages by Role

### Student (`student-*`)
| File | Section |
|------|---------|
| `student.html` | Dashboard — hero banner, profile card, events, schedule, deadlines |
| `student-profile.html` | Profile — personal info, avatar, contact |
| `student-grades.html` | Grades — subject scores, semester GPA |
| `student-notifications.html` | Notifications — alerts, announcements |
| `student-announcements.html` | Announcements — school-wide + dept posts |
| `student-assignments.html` | Assignments — due dates, submission status |
| `student-attendance.html` | Attendance — daily/monthly record |
| `student-calendar.html` | Calendar — events and schedule view |
| `student-timetable.html` | Timetable — weekly class grid |
| `student-documents.html` | Documents — uploaded files |
| `student-fees.html` | Fees — payment history |

### Teacher (`teacher-*`)
| File | Section |
|------|---------|
| `teacher.html` | Dashboard |
| `teacher-classes.html` | My Classes |
| `teacher-grades.html` | Grade entry |
| `teacher-attendance.html` | Attendance marking |
| `teacher-assignments.html` | Assignment management |
| `teacher-announcements.html` | Post announcements |
| `teacher-notifications.html` | Notifications |
| `teacher-calendar.html` | Calendar |
| `teacher-profile.html` | Profile |
| `teacher-documents.html` | Documents |

### Parent (`parent-*`)
| File | Section |
|------|---------|
| `parent.html` | Dashboard |
| `parent-children.html` | Children overview |
| `parent-grades.html` | Child grades |
| `parent-attendance.html` | Child attendance |
| `parent-announcements.html` | School announcements |
| `parent-notifications.html` | Notifications |
| `parent-calendar.html` | School calendar |
| `parent-profile.html` | Profile |
| `parent-documents.html` | Documents |
| `parent-assignments.html` | Child assignments |
| `parent-fees.html` | Fee payments |

### Admin (`admin-*`)
| File | Section |
|------|---------|
| `admin.html` | Dashboard |
| `admin-users.html` | User management |
| `admin-classes.html` | Classes |
| `admin-timetables.html` | Timetable builder |
| `admin-fees.html` | Fee management |
| `admin-reports.html` | Reports + analytics |
| `admin-logs.html` | Audit logs |
| `admin-settings.html` | System settings |

### Shared Pages (all roles)
| File | Section |
|------|---------|
| `departments.html` | Department grid — English, Khmer, Chinese |
| `department.html` | Single department — Attendance, Report Card, Lessons, Assignments, Timetable |
| `announcements.html` | Filtered announcements with pinned + unread |
| `lessons.html` | Lesson file browser — subject → file list → preview modal |
| `exams.html` | Exam timetable + countdown + checklist |
| `chat.html` | Direct messaging |
| `group-chat.html` | Class group chat |

---

## Assets

```
assets/
├── css/
│   ├── app.css          ← EDIT THIS for all global styles + design tokens
│   ├── chat.css         ← Direct chat styles
│   └── group-chat.css   ← Group chat styles
├── js/
│   ├── layout.js        ← EDIT THIS to change sidebar nav or topbar
│   ├── app.js           ← App-wide JS utilities
│   ├── chat.js          ← Direct chat logic
│   └── group-chat.js    ← Group chat + socket logic
└── images/
    └── color.png
```

### Key CSS variables (in `assets/css/app.css`)
```css
--primary:  #1F6B3A   /* Forest green — buttons, icons, active states */
--accent:   #F2C230   /* Gold — highlights, badges */
--bg:       #F8FAF5   /* Page background */
```

### How `layout.js` works
Every page sets `window.PAGE = { role, active }` before loading `layout.js`.
The script reads that and renders the correct sidebar + topbar for the role.

---

## Backend

```
server/
├── server.js            ← Express + Socket.io entry point
├── config/supabase.js   ← Supabase client
├── routes/              ← REST API routes
├── socket/              ← Socket.io event handlers
├── db/                  ← SQL schema + query helpers
└── middleware/auth.js   ← Auth middleware
```

---

## Design Prototypes (not production pages)

```
_concepts/
├── dashboard-concept.html   ← Teal hero + 3-col overlapping grid concept
└── hub-concept.html         ← Upcoming + Deadlines compound card concept
```

---

## Docs

```
docs/
├── REDESIGN-CHANGES.md
└── school-management-system-master-prompt.md
```

---

## Stale / To-Delete

| File | Status |
|------|--------|
| `layout.js` (root) | Old "EduFlow / Saint Patrick's Academy" copy — safe to delete. Real file is `assets/js/layout.js` |
