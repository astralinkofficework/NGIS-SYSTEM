/**
 * NGIS School ERP — Database Seed
 * Creates demo users + sample academic data
 * Run after init: node backend/db/seed.js
 *
 * Default password for all demo accounts: password123
 */

"use strict";

const bcrypt = require("bcryptjs");
const { getDb, closeDb } = require("./connection");

const PASSWORD = "password123";
const hash = bcrypt.hashSync(PASSWORD, 10);

const db = getDb();

console.log("══════════════════════════════════════════════");
console.log("  NGIS Database Seed");
console.log("══════════════════════════════════════════════");

// Fixed IDs for stable demo data
const IDS = {
  adminUser: "user-admin-001",
  teacherUser: "user-teacher-001",
  teacher: "teacher-001",
  studentUser: "user-student-001",
  student: "student-001",
  parentUser: "user-parent-001",
  parent: "parent-001",
  class10A: "cls-10a",
  class11B: "cls-11b",
};

const insertUser = db.prepare(`
  INSERT OR IGNORE INTO users (id, email, password_hash, role, status, first_name, last_name, phone)
  VALUES (@id, @email, @password_hash, @role, 'active', @first_name, @last_name, @phone)
`);

const insertStudent = db.prepare(`
  INSERT OR IGNORE INTO students (id, user_id, student_number, grade, class_id, house, date_of_birth, enrollment_date, gpa, attendance_rate)
  VALUES (@id, @user_id, @student_number, @grade, @class_id, @house, @date_of_birth, @enrollment_date, @gpa, @attendance_rate)
`);

const insertTeacher = db.prepare(`
  INSERT OR IGNORE INTO teachers (id, user_id, employee_number, department, qualifications, hire_date)
  VALUES (@id, @user_id, @employee_number, @department, @qualifications, @hire_date)
`);

const insertParent = db.prepare(`
  INSERT OR IGNORE INTO parents (id, user_id, relationship)
  VALUES (@id, @user_id, @relationship)
`);

const insertClass = db.prepare(`
  INSERT OR IGNORE INTO classes (id, name, grade, academic_year, campus, capacity, homeroom_teacher_id)
  VALUES (@id, @name, @grade, @academic_year, @campus, @capacity, @homeroom_teacher_id)
`);

const insertSubject = db.prepare(`
  INSERT OR IGNORE INTO subjects (id, code, name, department)
  VALUES (@id, @code, @name, @department)
`);

const insertParentStudent = db.prepare(`
  INSERT OR IGNORE INTO parent_students (parent_id, student_id, is_primary)
  VALUES (@parent_id, @student_id, @is_primary)
`);

const insertClassSubject = db.prepare(`
  INSERT OR IGNORE INTO class_subjects (id, class_id, subject_id, teacher_id, academic_year)
  VALUES (@id, @class_id, @subject_id, @teacher_id, @academic_year)
`);

const insertAssignment = db.prepare(`
  INSERT OR IGNORE INTO assignments (id, title, description, subject_id, class_id, teacher_id, due_date, max_score, status, published_at)
  VALUES (@id, @title, @description, @subject_id, @class_id, @teacher_id, @due_date, @max_score, @status, datetime('now'))
`);

const insertGrade = db.prepare(`
  INSERT OR IGNORE INTO grades (id, student_id, subject_id, class_id, assessment_type, assessment_title, score, max_score, letter_grade, percentage, recorded_by, comments)
  VALUES (@id, @student_id, @subject_id, @class_id, @assessment_type, @assessment_title, @score, @max_score, @letter_grade, @percentage, @recorded_by, @comments)
`);

// ── Classes ────────────────────────────────────────────────
insertClass.run({ id: IDS.class10A, name: "10A", grade: "Grade 10", academic_year: "2025-26", campus: "Sensok", capacity: 35, homeroom_teacher_id: null });
insertClass.run({ id: IDS.class11B, name: "11B", grade: "Grade 11", academic_year: "2025-26", campus: "Sensok", capacity: 32, homeroom_teacher_id: null });
console.log("  ✓ Classes created");

// ── Subjects ───────────────────────────────────────────────
const subjects = [
  { id: "subj-math", code: "MATH", name: "Mathematics", department: "Science" },
  { id: "subj-phys", code: "PHYS", name: "Physics", department: "Science" },
  { id: "subj-chem", code: "CHEM", name: "Chemistry", department: "Science" },
  { id: "subj-eng",  code: "ENG",  name: "English", department: "Languages" },
  { id: "subj-hist", code: "HIST", name: "History", department: "Humanities" },
];
subjects.forEach(s => insertSubject.run(s));
console.log("  ✓ Subjects created");

// ── Admin ──────────────────────────────────────────────────
insertUser.run({
  id: IDS.adminUser,
  email: "admin@ngis.edu.kh",
  password_hash: hash,
  role: "admin",
  first_name: "System",
  last_name: "Administrator",
  phone: "+855 23 000 001",
});
console.log("  ✓ Admin → admin@ngis.edu.kh");

// ── Teacher ────────────────────────────────────────────────
insertUser.run({
  id: IDS.teacherUser,
  email: "sophea@ngis.edu.kh",
  password_hash: hash,
  role: "teacher",
  first_name: "Chea",
  last_name: "Sophea",
  phone: "+855 98 765 432",
});
insertTeacher.run({
  id: IDS.teacher,
  user_id: IDS.teacherUser,
  employee_number: "TCH-0001",
  department: "Science",
  qualifications: JSON.stringify(["B.Sc Mathematics", "M.Sc Physics"]),
  hire_date: "2020-08-01",
});
// Update homeroom
db.prepare(`UPDATE classes SET homeroom_teacher_id = ? WHERE id = ?`).run(IDS.teacher, IDS.class10A);
console.log("  ✓ Teacher → sophea@ngis.edu.kh");

// ── Student ────────────────────────────────────────────────
insertUser.run({
  id: IDS.studentUser,
  email: "nrinphouneta@ngis.edu.kh",
  password_hash: hash,
  role: "student",
  first_name: "Nrinphouneta",
  last_name: "Hok",
  phone: "+855 12 345 678",
});
insertStudent.run({
  id: IDS.student,
  user_id: IDS.studentUser,
  student_number: "2026-STD-0142",
  grade: "Grade 10",
  class_id: IDS.class10A,
  house: "Yellow Falcon",
  date_of_birth: "2008-05-15",
  enrollment_date: "2024-09-01",
  gpa: 3.87,
  attendance_rate: 96,
});
console.log("  ✓ Student → nrinphouneta@ngis.edu.kh");

// ── Parent ─────────────────────────────────────────────────
insertUser.run({
  id: IDS.parentUser,
  email: "parent.hok@gmail.com",
  password_hash: hash,
  role: "parent",
  first_name: "Sokha",
  last_name: "Hok",
  phone: "+855 12 999 888",
});
insertParent.run({
  id: IDS.parent,
  user_id: IDS.parentUser,
  relationship: "father",
});
insertParentStudent.run({
  parent_id: IDS.parent,
  student_id: IDS.student,
  is_primary: 1,
});
console.log("  ✓ Parent → parent.hok@gmail.com (linked to Nrinphouneta)");

// ── Class ↔ Subject ↔ Teacher ──────────────────────────────
[
  { id: "cs-1", class_id: IDS.class10A, subject_id: "subj-math", teacher_id: IDS.teacher },
  { id: "cs-2", class_id: IDS.class10A, subject_id: "subj-phys", teacher_id: IDS.teacher },
  { id: "cs-3", class_id: IDS.class10A, subject_id: "subj-chem", teacher_id: IDS.teacher },
  { id: "cs-4", class_id: IDS.class10A, subject_id: "subj-eng",  teacher_id: IDS.teacher },
  { id: "cs-5", class_id: IDS.class10A, subject_id: "subj-hist", teacher_id: IDS.teacher },
].forEach(r => insertClassSubject.run({ ...r, academic_year: "2025-26" }));
console.log("  ✓ Class-subject assignments created");

// ── Sample Assignments ─────────────────────────────────────
const assignments = [
  {
    id: "asgn-001",
    title: "Mathematics Problem Set 4",
    description: "Complete exercises 1–20 from Chapter 8 (Quadratic Equations).",
    subject_id: "subj-math",
    class_id: IDS.class10A,
    teacher_id: IDS.teacher,
    due_date: "2026-09-10",
    max_score: 100,
    status: "published",
  },
  {
    id: "asgn-002",
    title: "Physics Lab Report — Wave Interference",
    description: "Write a full lab report on the wave interference experiment conducted in class.",
    subject_id: "subj-phys",
    class_id: IDS.class10A,
    teacher_id: IDS.teacher,
    due_date: "2026-09-12",
    max_score: 50,
    status: "published",
  },
  {
    id: "asgn-003",
    title: "Chemistry Worksheet — Periodic Table",
    description: "Fill in the worksheet on element groups and properties.",
    subject_id: "subj-chem",
    class_id: IDS.class10A,
    teacher_id: IDS.teacher,
    due_date: "2026-09-08",
    max_score: 30,
    status: "published",
  },
  {
    id: "asgn-004",
    title: "English Book Review",
    description: "Write a 500-word review of the assigned novel.",
    subject_id: "subj-eng",
    class_id: IDS.class10A,
    teacher_id: IDS.teacher,
    due_date: "2026-09-15",
    max_score: 40,
    status: "published",
  },
];

assignments.forEach(a => insertAssignment.run(a));
console.log("  ✓ Sample assignments created (4)");

// ── Sample Grades ──────────────────────────────────────────
insertGrade.run({
  id: "grade-001",
  student_id: IDS.student,
  subject_id: "subj-phys",
  class_id: IDS.class10A,
  assessment_type: "lab",
  assessment_title: "Chemistry Practical",
  score: 88,
  max_score: 100,
  letter_grade: "A",
  percentage: 88,
  recorded_by: IDS.teacher,
  comments: "Excellent performance. Well-structured answers.",
});
insertGrade.run({
  id: "grade-002",
  student_id: IDS.student,
  subject_id: "subj-math",
  class_id: IDS.class10A,
  assessment_type: "quiz",
  assessment_title: "Algebra Quiz 3",
  score: 92,
  max_score: 100,
  letter_grade: "A",
  percentage: 92,
  recorded_by: IDS.teacher,
  comments: "Outstanding work.",
});
console.log("  ✓ Sample grades created");

console.log("══════════════════════════════════════════════");
console.log("  Demo accounts (password: password123)");
console.log("  • admin@ngis.edu.kh");
console.log("  • sophea@ngis.edu.kh");
console.log("  • nrinphouneta@ngis.edu.kh");
console.log("  • parent.hok@gmail.com");
console.log("══════════════════════════════════════════════\n");

closeDb();
