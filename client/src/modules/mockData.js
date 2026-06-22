// =====================================================================
// Mock data for the NGIS front-end demo.
// Realistic Northgate International School content so every screen has data.
// This will be replaced by the API client (api/v1) once the backend exists.
// =====================================================================

export const school = {
  name: "Northgate International School",
  short: "NGIS",
  year: "2025–2026",
  term: "Semester 2",
  motto: "Learn boldly. Grow together.",
};

export const roles = ["super_admin", "admin", "teacher", "student", "parent"];

export const roleLabels = {
  super_admin: "Super Admin",
  admin: "Administrator",
  teacher: "Teacher",
  student: "Student",
  parent: "Parent",
};

// --- Demo accounts (one per role) ------------------------------------
export const accounts = {
  student: {
    id: "u-stu-1", role: "student", name: "Maya Chen", email: "student@ngis.edu",
    studentId: "NGIS-2025-0418", grade: "Grade 10", section: "B", homeroom: "Mr. David Okafor",
    avatar: null, phone: "+1 (415) 555-0142", address: "248 Maple Crescent, Northgate",
    enrolled: "2021-09-01", gpa: 3.72, attendancePct: 96, rank: 4, rankOf: 32,
  },
  teacher: {
    id: "u-tch-1", role: "teacher", name: "David Okafor", email: "teacher@ngis.edu",
    employeeId: "NGIS-T-0091", department: "Mathematics & Sciences", title: "Senior Mathematics Teacher",
    subjects: ["Mathematics", "Physics"], phone: "+1 (415) 555-0188",
  },
  parent: {
    id: "u-par-1", role: "parent", name: "Linda Chen", email: "parent@ngis.edu",
    phone: "+1 (415) 555-0142", children: ["u-stu-1", "u-stu-2"],
  },
  admin: {
    id: "u-adm-1", role: "admin", name: "Sarah Whitfield", email: "admin@ngis.edu",
    title: "Academic Administrator",
  },
  super_admin: {
    id: "u-sa-1", role: "super_admin", name: "Marcus Reyes", email: "superadmin@ngis.edu",
    title: "System Owner", protected: true,
  },
};

export const children = {
  "u-stu-1": { id: "u-stu-1", name: "Maya Chen", grade: "Grade 10-B", studentId: "NGIS-2025-0418",
    homeroom: "Mr. David Okafor", gpa: 3.72, attendancePct: 96, pendingAssignments: 2, fafter: false },
  "u-stu-2": { id: "u-stu-2", name: "Leo Chen", grade: "Grade 7-A", studentId: "NGIS-2025-0731",
    homeroom: "Ms. Priya Nair", gpa: 3.41, attendancePct: 88, pendingAssignments: 4, alert: true },
};

export const subjects = [
  { code: "MATH", name: "Mathematics", teacher: "Mr. David Okafor" },
  { code: "PHYS", name: "Physics", teacher: "Mr. David Okafor" },
  { code: "CHEM", name: "Chemistry", teacher: "Ms. Aisha Rahman" },
  { code: "BIO", name: "Biology", teacher: "Ms. Priya Nair" },
  { code: "ENG", name: "English Literature", teacher: "Mr. James Holloway" },
  { code: "HIST", name: "World History", teacher: "Ms. Elena Vargas" },
  { code: "CS", name: "Computer Science", teacher: "Mr. Tom Becker" },
  { code: "ART", name: "Visual Art", teacher: "Ms. Yuki Tanaka" },
];

// --- Timetable (Grade 10-B) ------------------------------------------
const T = (subject, teacher, room, start, end) => ({ subject, teacher, room, start, end });
export const timetable = {
  Monday: [
    T("Mathematics", "Mr. Okafor", "Rm 204", "08:30", "09:20"),
    T("Physics", "Mr. Okafor", "Lab 2", "09:30", "10:20"),
    T("English Literature", "Mr. Holloway", "Rm 118", "10:40", "11:30"),
    T("World History", "Ms. Vargas", "Rm 222", "11:40", "12:30"),
    T("Computer Science", "Mr. Becker", "Lab 5", "13:30", "14:20"),
  ],
  Tuesday: [
    T("Chemistry", "Ms. Rahman", "Lab 1", "08:30", "09:20"),
    T("Mathematics", "Mr. Okafor", "Rm 204", "09:30", "10:20"),
    T("Biology", "Ms. Nair", "Lab 3", "10:40", "11:30"),
    T("Visual Art", "Ms. Tanaka", "Studio", "11:40", "12:30"),
    T("English Literature", "Mr. Holloway", "Rm 118", "13:30", "14:20"),
  ],
  Wednesday: [
    T("Physics", "Mr. Okafor", "Lab 2", "08:30", "09:20"),
    T("Mathematics", "Mr. Okafor", "Rm 204", "09:30", "10:20"),
    T("World History", "Ms. Vargas", "Rm 222", "10:40", "11:30"),
    T("Computer Science", "Mr. Becker", "Lab 5", "11:40", "12:30"),
  ],
  Thursday: [
    T("Biology", "Ms. Nair", "Lab 3", "08:30", "09:20"),
    T("Chemistry", "Ms. Rahman", "Lab 1", "09:30", "10:20"),
    T("Mathematics", "Mr. Okafor", "Rm 204", "10:40", "11:30"),
    T("English Literature", "Mr. Holloway", "Rm 118", "11:40", "12:30"),
    T("Visual Art", "Ms. Tanaka", "Studio", "13:30", "14:20"),
  ],
  Friday: [
    T("World History", "Ms. Vargas", "Rm 222", "08:30", "09:20"),
    T("Physics", "Mr. Okafor", "Lab 2", "09:30", "10:20"),
    T("Computer Science", "Mr. Becker", "Lab 5", "10:40", "11:30"),
    T("Mathematics", "Mr. Okafor", "Rm 204", "11:40", "12:30"),
  ],
};
export const weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

// --- Grades (student view) -------------------------------------------
export const grades = [
  { subject: "Mathematics", code: "MATH", s1: 91, s2: 88, gpa: 3.9, letter: "A-", comment: "Excellent problem-solving; keep refining proofs.", trend: "up" },
  { subject: "Physics", code: "PHYS", s1: 84, s2: 87, gpa: 3.7, letter: "B+", comment: "Strong lab work this term.", trend: "up" },
  { subject: "Chemistry", code: "CHEM", s1: 79, s2: 82, gpa: 3.3, letter: "B", comment: "Improving steadily — review titration.", trend: "up" },
  { subject: "Biology", code: "BIO", s1: 88, s2: 90, gpa: 3.9, letter: "A-", comment: "Consistently thorough.", trend: "flat" },
  { subject: "English Literature", code: "ENG", s1: 93, s2: 91, gpa: 4.0, letter: "A", comment: "Outstanding essays.", trend: "flat" },
  { subject: "World History", code: "HIST", s1: 76, s2: 73, gpa: 2.7, letter: "C+", comment: "Watch source analysis depth.", trend: "down" },
  { subject: "Computer Science", code: "CS", s1: 95, s2: 96, gpa: 4.0, letter: "A", comment: "Exceptional final project.", trend: "up" },
  { subject: "Visual Art", code: "ART", s1: 85, s2: 86, gpa: 3.7, letter: "B+", comment: "Creative portfolio.", trend: "flat" },
];

export const exams = [
  { name: "Physics — Unit 4 Test", subject: "Physics", date: "2026-06-24", status: "upcoming", room: "Lab 2" },
  { name: "Mathematics — Midterm", subject: "Mathematics", date: "2026-06-26", status: "upcoming", room: "Hall A" },
  { name: "Chemistry — Quiz 3", subject: "Chemistry", date: "2026-06-29", status: "upcoming", room: "Lab 1" },
  { name: "English — Essay Exam", subject: "English Literature", date: "2026-06-15", status: "completed", score: 91 },
  { name: "Biology — Unit 3 Test", subject: "Biology", date: "2026-06-10", status: "completed", score: 90 },
];

// --- Assignments ------------------------------------------------------
export const assignments = [
  { id: "a1", title: "Quadratic Functions — Problem Set 7", subject: "Mathematics", due: "2026-06-23", status: "pending", desc: "Complete problems 1–18; show all working." },
  { id: "a2", title: "Lab Report: Projectile Motion", subject: "Physics", due: "2026-06-25", status: "pending", desc: "Submit your write-up with graphs and error analysis." },
  { id: "a3", title: "Essay: Symbolism in 'The Great Gatsby'", subject: "English Literature", due: "2026-06-20", status: "submitted", desc: "1,000–1,200 words, MLA format.", grade: "A", feedback: "Compelling thesis." },
  { id: "a4", title: "World War I — Source Analysis", subject: "World History", due: "2026-06-18", status: "overdue", desc: "Analyse two primary sources." },
  { id: "a5", title: "Build a To-Do App", subject: "Computer Science", due: "2026-06-19", status: "submitted", desc: "Vanilla JS, no frameworks.", grade: "A", feedback: "Clean module structure." },
  { id: "a6", title: "Cell Division Diagram", subject: "Biology", due: "2026-06-30", status: "pending", desc: "Annotated diagram of mitosis." },
];

// --- Announcements ----------------------------------------------------
export const announcements = [
  { id: "n1", title: "Semester 2 final exam schedule published", body: "The full examination timetable is now available. Please review your subject dates and reporting rooms. Exams begin June 24.", category: "exams", scope: "school", author: "Academic Office", date: "2026-06-21", pinned: true },
  { id: "n2", title: "Inter-house Sports Day — June 27", body: "Wear your house colours. Field events start at 9:00 AM on the main grounds. Parents welcome.", category: "sports", scope: "school", author: "Athletics Dept", date: "2026-06-20", pinned: false },
  { id: "n3", title: "Mathematics — extra revision session Thursday", body: "Optional revision for the midterm, Thursday 3:30 PM in Rm 204. Bring your problem sets.", category: "class", scope: "class", author: "Mr. Okafor", date: "2026-06-19", pinned: false },
  { id: "n4", title: "Library extended hours during exams", body: "The library will stay open until 7:00 PM on weekdays through July 4.", category: "school", scope: "school", author: "Library", date: "2026-06-18", pinned: false },
  { id: "n5", title: "Heat advisory — hydration reminder", body: "Please bring a water bottle. Outdoor PE is moved indoors this week.", category: "emergency", scope: "school", author: "School Nurse", date: "2026-06-17", pinned: false },
];

export const categoryTone = {
  exams: "accent", sports: "ok", class: "info", school: "default", emergency: "danger", events: "gold",
};

// --- Notifications ----------------------------------------------------
export const notifications = [
  { id: "x1", icon: "clipboard", title: "New assignment posted", body: "Lab Report: Projectile Motion — due Jun 25", time: "2h ago", unread: true },
  { id: "x2", icon: "calendar", title: "Exam tomorrow", body: "Physics — Unit 4 Test, Lab 2, 08:30", time: "5h ago", unread: true },
  { id: "x3", icon: "megaphone", title: "New announcement", body: "Inter-house Sports Day — June 27", time: "1d ago", unread: false },
  { id: "x4", icon: "award", title: "Grade released", body: "English — Essay Exam: A (91%)", time: "2d ago", unread: false },
];

// --- Attendance (monthly summary for student) ------------------------
export const attendanceSummary = { present: 78, late: 5, absent: 2, excused: 3 };
// June 2026 — June 1 is a Monday. Status per weekday: present|late|absent|excused.
// Weekends are omitted from the school calendar.
export const attendanceMonth = {
  1: "present", 2: "present", 3: "present", 4: "present", 5: "present",
  8: "late", 9: "present", 10: "present", 11: "present", 12: "present",
  15: "present", 16: "present", 17: "absent", 18: "excused", 19: "present",
  22: "present", 23: "present", 24: "present", 25: "present", 26: "late",
  29: "present", 30: "present",
};

// --- Teacher: classes + roster ---------------------------------------
export const teacherClasses = [
  { id: "c1", name: "Grade 10-B", subject: "Mathematics", students: 32, homeroom: true, next: "Mon 08:30", avg: 84, attendance: 95 },
  { id: "c2", name: "Grade 10-B", subject: "Physics", students: 32, homeroom: false, next: "Mon 09:30", avg: 81, attendance: 94 },
  { id: "c3", name: "Grade 11-A", subject: "Mathematics", students: 28, homeroom: false, next: "Tue 10:40", avg: 87, attendance: 97 },
  { id: "c4", name: "Grade 9-C", subject: "Mathematics", students: 30, homeroom: false, next: "Wed 11:40", avg: 79, attendance: 91 },
];

export const roster = [
  { id: "s1", name: "Maya Chen", sid: "NGIS-2025-0418", avg: 89, att: 96, status: "present", flag: "excellent" },
  { id: "s2", name: "Liam Patel", sid: "NGIS-2025-0419", avg: 76, att: 92, status: "present" },
  { id: "s3", name: "Sofia Romano", sid: "NGIS-2025-0420", avg: 91, att: 98, status: "present", flag: "excellent" },
  { id: "s4", name: "Noah Kim", sid: "NGIS-2025-0421", avg: 64, att: 79, status: "absent", flag: "at-risk" },
  { id: "s5", name: "Ava Thompson", sid: "NGIS-2025-0422", avg: 82, att: 94, status: "present" },
  { id: "s6", name: "Ethan Wright", sid: "NGIS-2025-0423", avg: 70, att: 84, status: "late", flag: "low-attendance" },
  { id: "s7", name: "Isabella Cruz", sid: "NGIS-2025-0424", avg: 88, att: 95, status: "present" },
  { id: "s8", name: "Daniel Osei", sid: "NGIS-2025-0425", avg: 85, att: 93, status: "present" },
  { id: "s9", name: "Mia Hassan", sid: "NGIS-2025-0426", avg: 79, att: 90, status: "present" },
  { id: "s10", name: "Lucas Müller", sid: "NGIS-2025-0427", avg: 73, att: 86, status: "present" },
];

// --- Fees (parent view) ----------------------------------------------
export const fees = {
  total: 8400, paid: 5600, remaining: 2800, currency: "$",
  plan: [
    { label: "Tuition — Semester 2", amount: 4000, due: "2026-06-30", status: "due", paid: 1200 },
    { label: "Lab & Materials", amount: 600, due: "2026-06-30", status: "paid" },
    { label: "Tuition — Semester 1", amount: 4000, due: "2026-01-15", status: "paid" },
  ],
  scholarship: { name: "Academic Merit Award", amount: 800 },
  history: [
    { date: "2026-06-01", desc: "Tuition — Semester 2 (partial)", amount: 1200, method: "Bank transfer", receipt: "RC-20418" },
    { date: "2026-01-12", desc: "Tuition — Semester 1", amount: 4000, method: "Card", receipt: "RC-19932" },
    { date: "2026-01-12", desc: "Lab & Materials", amount: 600, method: "Card", receipt: "RC-19933" },
  ],
};

// --- Admin: school-wide numbers --------------------------------------
export const adminStats = {
  students: 1284, teachers: 96, parents: 1502, classes: 48,
  attendanceToday: 94.2, feesCollectedPct: 81, openIssues: 7,
  enrollmentTrend: [1180, 1205, 1221, 1240, 1262, 1284],
};
export const recentUsers = [
  { name: "Priya Nair", role: "teacher", email: "p.nair@ngis.edu", status: "active", joined: "2026-06-18" },
  { name: "Leo Chen", role: "student", email: "leo.c@ngis.edu", status: "active", joined: "2026-06-17" },
  { name: "Robert Fox", role: "parent", email: "r.fox@ngis.edu", status: "pending", joined: "2026-06-16" },
  { name: "Yuki Tanaka", role: "teacher", email: "y.tanaka@ngis.edu", status: "active", joined: "2026-06-15" },
  { name: "Hana Suzuki", role: "student", email: "hana.s@ngis.edu", status: "suspended", joined: "2026-06-14" },
];

// --- Super Admin: system health --------------------------------------
export const systemHealth = [
  { name: "API", icon: "server", status: "operational", metric: "p95 182ms", sub: "12.4k req/min" },
  { name: "Database", icon: "database", status: "operational", metric: "38% load", sub: "Supabase · pooled" },
  { name: "Storage", icon: "cloud", status: "operational", metric: "412 GB", sub: "of 2 TB used" },
  { name: "Cloudflare", icon: "shield", status: "degraded", metric: "WAF active", sub: "1 rule throttled" },
];
export const backups = [
  { date: "2026-06-22 02:00", type: "Full", size: "8.2 GB", location: "s3://ngis-backups", status: "success" },
  { date: "2026-06-21 02:00", type: "Full", size: "8.1 GB", location: "s3://ngis-backups", status: "success" },
  { date: "2026-06-20 02:00", type: "Full", size: "8.0 GB", location: "s3://ngis-backups", status: "success" },
  { date: "2026-06-19 02:00", type: "Full", size: "7.9 GB", location: "s3://ngis-backups", status: "warning" },
];
export const securityLog = [
  { time: "08:42", actor: "admin@ngis.edu", action: "Role changed: Liam Patel → student", ip: "10.0.4.18", level: "info" },
  { time: "08:31", actor: "superadmin@ngis.edu", action: "Backup restore test completed", ip: "10.0.4.2", level: "ok" },
  { time: "07:58", actor: "unknown", action: "Failed login (5x) — account locked", ip: "203.0.113.44", level: "warn" },
  { time: "07:12", actor: "teacher@ngis.edu", action: "Grade edited: Maya Chen / Physics", ip: "10.0.4.55", level: "info" },
];

// --- documents --------------------------------------------------------
export const documents = [
  { name: "Report Card — Semester 1", type: "report_card", date: "2026-01-20", size: "240 KB" },
  { name: "Enrollment Certificate 2025–26", type: "certificate", date: "2025-09-02", size: "180 KB" },
  { name: "Exam Slip — Semester 2", type: "exam_slip", date: "2026-06-21", size: "96 KB" },
  { name: "Achievement Letter — Honor Roll", type: "letter", date: "2026-02-11", size: "120 KB" },
];

export const docTypeLabel = {
  report_card: "Report card", certificate: "Certificate", exam_slip: "Exam slip",
  letter: "Letter", lesson_plan: "Lesson plan",
};
