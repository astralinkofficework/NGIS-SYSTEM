/* Mock dataset — front-end only. Mirrors §11 data model shape so screens have
   realistic data. In production these come from /api/v1/* (see server/). */

export const SCHOOL = { id: 'sch_001', name: 'Northgate International School', short: 'NGIS', year: '2025–2026', term: 'Term 2' };

export const USERS = {
  superadmin: { id: 'u_sa', name: 'Sarah Okonkwo', role: 'super_admin', email: 'superadmin@ngis.edu', initials: 'SO', title: 'System Owner' },
  admin:      { id: 'u_ad', name: 'David Mensah',   role: 'admin',       email: 'admin@ngis.edu',      initials: 'DM', title: 'School Administrator' },
  teacher:    { id: 'u_te', name: 'Amara Bello',    role: 'teacher',     email: 'teacher@ngis.edu',    initials: 'AB', title: 'Mathematics & Physics', employee_id: 'EMP-2041' },
  student:    { id: 'u_st', name: 'Leo Carter',     role: 'student',     email: 'student@ngis.edu',    initials: 'LC', title: 'Grade 10 · Class 10-B', student_id: 'STU-10B-014', class: '10-B', gpa: 3.78 },
  parent:     { id: 'u_pa', name: 'Maria Carter',   role: 'parent',      email: 'parent@ngis.edu',     initials: 'MC', title: 'Parent / Guardian' },
};

export const ROLE_LABEL = {
  super_admin: 'Super Admin', admin: 'Admin', teacher: 'Teacher', student: 'Student', parent: 'Parent',
};

export const SUBJECTS = [
  { code: 'MATH', name: 'Mathematics', color: 'var(--chart-1)' },
  { code: 'PHYS', name: 'Physics', color: 'var(--chart-4)' },
  { code: 'ENG',  name: 'English Literature', color: 'var(--chart-2)' },
  { code: 'CHEM', name: 'Chemistry', color: 'var(--chart-5)' },
  { code: 'HIST', name: 'History', color: 'var(--chart-3)' },
  { code: 'BIO',  name: 'Biology', color: 'var(--chart-6)' },
  { code: 'CS',   name: 'Computer Science', color: 'var(--chart-1)' },
];

export const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
export const PERIODS = [
  { p: 1, time: '08:00–08:50' }, { p: 2, time: '09:00–09:50' },
  { p: 3, time: '10:10–11:00' }, { p: 4, time: '11:10–12:00' },
  { p: 5, time: '13:00–13:50' }, { p: 6, time: '14:00–14:50' },
];

// timetable[day][periodIndex] = {subj, room, teacher} | null
export const TIMETABLE = {
  Mon: [s('MATH','204','Ms. Bello'), s('ENG','118','Mr. Adeyemi'), null, s('PHYS','Lab 2','Ms. Bello'), s('HIST','210','Mrs. Cole'), null],
  Tue: [s('CHEM','Lab 1','Dr. Singh'), s('MATH','204','Ms. Bello'), s('CS','Lab 3','Mr. Tan'), null, s('ENG','118','Mr. Adeyemi'), s('BIO','Lab 2','Dr. Okafor')],
  Wed: [s('PHYS','Lab 2','Ms. Bello'), s('HIST','210','Mrs. Cole'), s('MATH','204','Ms. Bello'), s('ENG','118','Mr. Adeyemi'), null, null],
  Thu: [s('BIO','Lab 2','Dr. Okafor'), s('CS','Lab 3','Mr. Tan'), s('CHEM','Lab 1','Dr. Singh'), s('MATH','204','Ms. Bello'), s('PHYS','Lab 2','Ms. Bello'), null],
  Fri: [s('ENG','118','Mr. Adeyemi'), s('MATH','204','Ms. Bello'), s('HIST','210','Mrs. Cole'), null, s('CS','Lab 3','Mr. Tan'), null],
};
function s(code, room, teacher) {
  const subj = SUBJECTS.find((x) => x.code === code);
  return { code, name: subj.name, color: subj.color, room, teacher };
}

export const GRADES = [
  { subject: 'Mathematics',        score: 92, max: 100, grade: 'A',  semesterAvg: 89, comment: 'Excellent analytical work.' },
  { subject: 'Physics',            score: 85, max: 100, grade: 'A-', semesterAvg: 83, comment: 'Strong grasp of mechanics.' },
  { subject: 'English Literature', score: 78, max: 100, grade: 'B+', semesterAvg: 80, comment: 'Improve essay structure.' },
  { subject: 'Chemistry',          score: 88, max: 100, grade: 'A-', semesterAvg: 86, comment: 'Great lab discipline.' },
  { subject: 'History',            score: 74, max: 100, grade: 'B',  semesterAvg: 76, comment: 'More source analysis needed.' },
  { subject: 'Computer Science',   score: 95, max: 100, grade: 'A+', semesterAvg: 93, comment: 'Outstanding project work.' },
];

export const EXAMS = [
  { name: 'Mid-Term: Calculus',    subject: 'Mathematics',      date: '2026-06-25', status: 'upcoming', max: 100 },
  { name: 'Unit Test: Optics',     subject: 'Physics',          date: '2026-06-27', status: 'upcoming', max: 50 },
  { name: 'Essay: Macbeth',        subject: 'English Literature',date: '2026-06-30', status: 'upcoming', max: 40 },
  { name: 'Quiz: Stoichiometry',   subject: 'Chemistry',        date: '2026-06-12', status: 'completed', score: 44, max: 50 },
  { name: 'Final: Algorithms',     subject: 'Computer Science', date: '2026-06-09', status: 'completed', score: 95, max: 100 },
];

export const ASSIGNMENTS = [
  { id: 'a1', title: 'Quadratic Equations — Problem Set 7', subject: 'Mathematics',       due: '2026-06-24', status: 'pending',   teacher: 'Ms. Bello' },
  { id: 'a2', title: 'Lab Report: Refraction of Light',      subject: 'Physics',            due: '2026-06-23', status: 'pending',   teacher: 'Ms. Bello' },
  { id: 'a3', title: 'Character Analysis: Lady Macbeth',     subject: 'English Literature', due: '2026-06-20', status: 'overdue',   teacher: 'Mr. Adeyemi' },
  { id: 'a4', title: 'Periodic Trends Worksheet',            subject: 'Chemistry',          due: '2026-06-18', status: 'submitted', teacher: 'Dr. Singh', grade: '18/20' },
  { id: 'a5', title: 'Sorting Algorithms — Code Challenge',  subject: 'Computer Science',   due: '2026-06-15', status: 'submitted', teacher: 'Mr. Tan',   grade: '100/100' },
  { id: 'a6', title: 'Causes of WWI — Source Pack',          subject: 'History',            due: '2026-07-02', status: 'pending',   teacher: 'Mrs. Cole' },
];

export const ANNOUNCEMENTS = [
  { id: 'an1', title: 'Term 2 Examination Schedule Released', category: 'exams', scope: 'school', pinned: true,  body: 'The full examination timetable for Term 2 is now available. Please review your subjects and rooms.', author: 'Admin Office', date: '2026-06-20' },
  { id: 'an2', title: 'Science Fair — Registration Open',     category: 'events', scope: 'school', pinned: false, body: 'Register your projects for the annual science fair by June 28th.', author: 'Dr. Singh', date: '2026-06-19' },
  { id: 'an3', title: 'Physics Class: Bring Calculators Tomorrow', category: 'class', scope: 'class', pinned: false, body: 'We will be doing optics calculations. Scientific calculators required.', author: 'Ms. Bello', date: '2026-06-21' },
  { id: 'an4', title: 'Early Dismissal — Staff Development Day', category: 'emergency', scope: 'school', pinned: true, body: 'School closes at 12:30 on Friday for staff training.', author: 'Principal', date: '2026-06-18' },
];

export const NOTIFICATIONS = [
  { id: 'n1', type: 'assignment', text: 'New assignment in Physics: Lab Report', time: '12m ago', read: false, icon: 'clipboard' },
  { id: 'n2', type: 'exam', text: 'Mathematics mid-term in 3 days', time: '1h ago', read: false, icon: 'calendar' },
  { id: 'n3', type: 'announce', text: 'New announcement: Term 2 Exam Schedule', time: '2h ago', read: false, icon: 'bell' },
  { id: 'n4', type: 'grade', text: 'Grade posted for CS — Algorithms Final', time: 'Yesterday', read: true, icon: 'award' },
];

// 30 days attendance: status by day-of-month (1..30)
export const ATTENDANCE_MONTH = (() => {
  const out = {};
  const pattern = { 3:'late', 8:'absent', 14:'late', 19:'excused', 22:'absent' };
  for (let d = 1; d <= 30; d++) {
    const dow = (d + 5) % 7; // pseudo weekend skip
    if (dow === 0 || dow === 6) { out[d] = null; continue; }
    out[d] = pattern[d] || 'present';
  }
  return out;
})();

export const ATTENDANCE_SUMMARY = { present: 88, late: 4, absent: 3, excused: 2, rate: 92.6 };

// Teacher's class roster
export const ROSTER = [
  { id: 'STU-10B-001', name: 'Aisha Rahman',  attendance: 96, gpa: 3.9, flag: 'excellent' },
  { id: 'STU-10B-002', name: 'Ben Lindqvist',  attendance: 71, gpa: 2.4, flag: 'at-risk' },
  { id: 'STU-10B-003', name: 'Chioma Eze',     attendance: 88, gpa: 3.5, flag: null },
  { id: 'STU-10B-004', name: 'Daniel Park',    attendance: 93, gpa: 3.7, flag: null },
  { id: 'STU-10B-005', name: 'Elena Rossi',    attendance: 79, gpa: 2.9, flag: 'low-attendance' },
  { id: 'STU-10B-006', name: 'Farid Hassan',   attendance: 98, gpa: 4.0, flag: 'excellent' },
  { id: 'STU-10B-014', name: 'Leo Carter',     attendance: 92, gpa: 3.78, flag: null },
];

// Parent → children
export const CHILDREN = [
  { id: 'STU-10B-014', name: 'Leo Carter', class: '10-B', grade: 10, gpa: 3.78, attendance: 92, pendingAssignments: 3, fees: 0, initials: 'LC' },
  { id: 'STU-07A-022', name: 'Mia Carter', class: '7-A',  grade: 7,  gpa: 3.95, attendance: 97, pendingAssignments: 1, fees: 250, initials: 'MC' },
];

export const FEES = {
  total: 4800, paid: 4550, remaining: 250,
  items: [
    { label: 'Tuition — Term 2', amount: 3200, due: '2026-04-01', status: 'paid' },
    { label: 'Lab & Materials',  amount: 600,  due: '2026-04-01', status: 'paid' },
    { label: 'Activities & Sports', amount: 450, due: '2026-04-01', status: 'paid' },
    { label: 'Library & Tech Fee', amount: 300, due: '2026-04-01', status: 'paid' },
    { label: 'Field Trip — Science Museum', amount: 250, due: '2026-07-01', status: 'pending' },
  ],
};

export const SMART_ALERTS = [
  { id: 'sa1', level: 'danger',  icon: 'alert',  title: '3 consecutive absences', text: 'Mia was absent Jun 16–18. Contact homeroom teacher.', child: 'Mia Carter' },
  { id: 'sa2', level: 'warning', icon: 'trend',  title: 'GPA dropped 0.3', text: "Leo's English grade fell this term.", child: 'Leo Carter' },
  { id: 'sa3', level: 'success', icon: 'award',  title: 'Excellent performance', text: 'Mia scored top 5% in Mathematics.', child: 'Mia Carter' },
];

// Admin / Super Admin data
export const ADMIN_STATS = { students: 1284, teachers: 86, parents: 1102, classes: 48, activeToday: 1147, feesCollected: 92 };

export const USER_DIRECTORY = [
  { id: 'STU-10B-014', name: 'Leo Carter',    role: 'student', email: 'leo.c@ngis.edu',   status: 'active',   joined: '2024-09-01' },
  { id: 'EMP-2041',    name: 'Amara Bello',   role: 'teacher', email: 'a.bello@ngis.edu', status: 'active',   joined: '2021-08-15' },
  { id: 'PAR-0455',    name: 'Maria Carter',  role: 'parent',  email: 'm.carter@ngis.edu',status: 'active',   joined: '2024-09-01' },
  { id: 'STU-07A-022', name: 'Mia Carter',    role: 'student', email: 'mia.c@ngis.edu',   status: 'active',   joined: '2024-09-01' },
  { id: 'EMP-1180',    name: 'David Mensah',  role: 'admin',   email: 'd.mensah@ngis.edu',status: 'active',   joined: '2019-01-10' },
  { id: 'STU-09C-031', name: 'Ben Lindqvist', role: 'student', email: 'ben.l@ngis.edu',   status: 'suspended',joined: '2023-09-01' },
  { id: 'EMP-2210',    name: 'Raj Singh',     role: 'teacher', email: 'r.singh@ngis.edu', status: 'pending',  joined: '2026-06-10' },
];

export const SYSTEM_HEALTH = [
  { name: 'API Gateway',       status: 'operational', metric: 'p95 182ms', icon: 'server',   level: 'success' },
  { name: 'PostgreSQL (Supabase)', status: 'operational', metric: '34% load', icon: 'database', level: 'success' },
  { name: 'Object Storage',    status: 'operational', metric: '128 GB used', icon: 'cloud',    level: 'success' },
  { name: 'Cloudflare WAF',    status: 'degraded',    metric: '2 rules flagged', icon: 'shield',  level: 'warning' },
];

export const BACKUPS = [
  { type: 'Full (DB + Storage)', size: '4.2 GB', location: 'eu-west-1', when: '2026-06-22 02:00', status: 'success' },
  { type: 'Full (DB + Storage)', size: '4.1 GB', location: 'eu-west-1', when: '2026-06-21 02:00', status: 'success' },
  { type: 'Incremental',         size: '320 MB', location: 'eu-west-1', when: '2026-06-20 14:00', status: 'success' },
  { type: 'Full (DB + Storage)', size: '4.1 GB', location: 'eu-west-1', when: '2026-06-20 02:00', status: 'failed'  },
];

export const SECURITY_LOG = [
  { actor: 'admin@ngis.edu', action: 'role.change', entity: 'STU-09C-031 → suspended', ip: '102.89.x.x', when: '09:14', device: 'Chrome · macOS' },
  { actor: 'teacher@ngis.edu', action: 'grade.edit', entity: 'Grade MATH/STU-10B-014', ip: '197.210.x.x', when: '08:51', device: 'Safari · iPad' },
  { actor: 'superadmin@ngis.edu', action: 'login.success', entity: 'Session started', ip: '41.58.x.x', when: '08:02', device: 'Firefox · Windows' },
  { actor: 'unknown', action: 'login.failed', entity: '5 attempts → lockout', ip: '185.220.x.x', when: '03:22', device: 'Unknown' },
];

// Weekly attendance trend for charts (% present per weekday)
export const ATTENDANCE_TREND = [94, 96, 91, 88, 93];
export const CLASS_SCORE_DIST = [ // grade buckets
  { label: 'A', value: 12 }, { label: 'B', value: 9 }, { label: 'C', value: 5 }, { label: 'D', value: 2 }, { label: 'F', value: 1 },
];
export const PERFORMANCE_TREND = [72, 75, 74, 78, 81, 83]; // monthly avg
