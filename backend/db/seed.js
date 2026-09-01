/**
 * NGIS School ERP — Database Seed
 * Creates demo users for Admin, Teacher, Student, Parent
 * Run after init: node backend/db/seed.js
 *
 * Default password for all demo accounts: password123
 */

"use strict";

const bcrypt = require("bcryptjs");
const { v4: uuidv4 } = require("uuid");
const { getDb, closeDb } = require("./connection");

const PASSWORD = "password123";
const hash = bcrypt.hashSync(PASSWORD, 10);

const db = getDb();

console.log("══════════════════════════════════════════════");
console.log("  NGIS Database Seed");
console.log("══════════════════════════════════════════════");

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
  INSERT OR IGNORE INTO classes (id, name, grade, academic_year, campus, capacity)
  VALUES (@id, @name, @grade, @academic_year, @campus, @capacity)
`);

const insertSubject = db.prepare(`
  INSERT OR IGNORE INTO subjects (id, code, name, department)
  VALUES (@id, @code, @name, @department)
`);

const insertParentStudent = db.prepare(`
  INSERT OR IGNORE INTO parent_students (parent_id, student_id, is_primary)
  VALUES (@parent_id, @student_id, @is_primary)
`);

// ── Classes ────────────────────────────────────────────────
const class10A = { id: "cls-10a", name: "10A", grade: "Grade 10", academic_year: "2025-26", campus: "Sensok", capacity: 35 };
const class11B = { id: "cls-11b", name: "11B", grade: "Grade 11", academic_year: "2025-26", campus: "Sensok", capacity: 32 };

insertClass.run(class10A);
insertClass.run(class11B);
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
const adminId = uuidv4();
insertUser.run({
  id: adminId,
  email: "admin@ngis.edu.kh",
  password_hash: hash,
  role: "admin",
  first_name: "System",
  last_name: "Administrator",
  phone: "+855 23 000 001",
});
console.log("  ✓ Admin user created → admin@ngis.edu.kh");

// ── Teacher ────────────────────────────────────────────────
const teacherUserId = uuidv4();
const teacherId = uuidv4();
insertUser.run({
  id: teacherUserId,
  email: "sophea@ngis.edu.kh",
  password_hash: hash,
  role: "teacher",
  first_name: "Chea",
  last_name: "Sophea",
  phone: "+855 98 765 432",
});
insertTeacher.run({
  id: teacherId,
  user_id: teacherUserId,
  employee_number: "TCH-0001",
  department: "Science",
  qualifications: JSON.stringify(["B.Sc Mathematics", "M.Sc Physics"]),
  hire_date: "2020-08-01",
});
console.log("  ✓ Teacher created → sophea@ngis.edu.kh");

// ── Student ────────────────────────────────────────────────
const studentUserId = uuidv4();
const studentId = uuidv4();
insertUser.run({
  id: studentUserId,
  email: "nrinphouneta@ngis.edu.kh",
  password_hash: hash,
  role: "student",
  first_name: "Nrinphouneta",
  last_name: "Hok",
  phone: "+855 12 345 678",
});
insertStudent.run({
  id: studentId,
  user_id: studentUserId,
  student_number: "2026-STD-0142",
  grade: "Grade 10",
  class_id: "cls-10a",
  house: "Yellow Falcon",
  date_of_birth: "2008-05-15",
  enrollment_date: "2024-09-01",
  gpa: 3.87,
  attendance_rate: 96,
});
console.log("  ✓ Student created → nrinphouneta@ngis.edu.kh");

// ── Parent ─────────────────────────────────────────────────
const parentUserId = uuidv4();
const parentId = uuidv4();
insertUser.run({
  id: parentUserId,
  email: "parent.hok@gmail.com",
  password_hash: hash,
  role: "parent",
  first_name: "Sokha",
  last_name: "Hok",
  phone: "+855 12 999 888",
});
insertParent.run({
  id: parentId,
  user_id: parentUserId,
  relationship: "father",
});
insertParentStudent.run({
  parent_id: parentId,
  student_id: studentId,
  is_primary: 1,
});
console.log("  ✓ Parent created → parent.hok@gmail.com (linked to Nrinphouneta)");

console.log("══════════════════════════════════════════════");
console.log("  Demo accounts ready (password: password123)");
console.log("  • admin@ngis.edu.kh");
console.log("  • sophea@ngis.edu.kh");
console.log("  • nrinphouneta@ngis.edu.kh");
console.log("  • parent.hok@gmail.com");
console.log("══════════════════════════════════════════════\n");

closeDb();
