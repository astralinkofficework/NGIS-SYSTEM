-- ============================================================
-- NGIS School ERP — Core Database Schema
-- Phase 1 Foundation
-- ============================================================

PRAGMA foreign_keys = ON;

-- ── Users (central identity) ───────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id            TEXT PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role          TEXT NOT NULL CHECK(role IN ('admin','teacher','student','parent')),
  status        TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','inactive','suspended')),
  first_name    TEXT NOT NULL,
  last_name     TEXT NOT NULL,
  phone         TEXT,
  avatar_url    TEXT,
  last_login_at TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ── Students ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
  id              TEXT PRIMARY KEY,
  user_id         TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  student_number  TEXT NOT NULL UNIQUE,
  grade           TEXT NOT NULL,
  class_id        TEXT,
  house           TEXT,
  date_of_birth   TEXT,
  enrollment_date TEXT,
  gpa             REAL DEFAULT 0,
  attendance_rate REAL DEFAULT 0,
  status          TEXT NOT NULL DEFAULT 'active',
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_students_class ON students(class_id);
CREATE INDEX IF NOT EXISTS idx_students_user ON students(user_id);

-- ── Parents ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS parents (
  id           TEXT PRIMARY KEY,
  user_id      TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  relationship TEXT DEFAULT 'parent',
  created_at   TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Parent ↔ Student relationship ─────────────────────────
CREATE TABLE IF NOT EXISTS parent_students (
  parent_id  TEXT NOT NULL REFERENCES parents(id) ON DELETE CASCADE,
  student_id TEXT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  is_primary INTEGER DEFAULT 0,
  PRIMARY KEY (parent_id, student_id)
);

-- ── Teachers ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS teachers (
  id              TEXT PRIMARY KEY,
  user_id         TEXT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  employee_number TEXT UNIQUE,
  department      TEXT,
  qualifications  TEXT,
  hire_date       TEXT,
  status          TEXT NOT NULL DEFAULT 'active',
  created_at      TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Classes ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS classes (
  id            TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  grade         TEXT NOT NULL,
  academic_year TEXT NOT NULL,
  campus        TEXT DEFAULT 'Sensok',
  homeroom_teacher_id TEXT REFERENCES teachers(id),
  capacity      INTEGER DEFAULT 40,
  status        TEXT NOT NULL DEFAULT 'active',
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Subjects ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS subjects (
  id          TEXT PRIMARY KEY,
  code        TEXT NOT NULL UNIQUE,
  name        TEXT NOT NULL,
  description TEXT,
  department  TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Class ↔ Subject ↔ Teacher assignment ──────────────────
CREATE TABLE IF NOT EXISTS class_subjects (
  id          TEXT PRIMARY KEY,
  class_id    TEXT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  subject_id  TEXT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
  teacher_id  TEXT REFERENCES teachers(id),
  academic_year TEXT NOT NULL,
  UNIQUE(class_id, subject_id, academic_year)
);

-- ── Assignments ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS assignments (
  id           TEXT PRIMARY KEY,
  title        TEXT NOT NULL,
  description  TEXT,
  subject_id   TEXT NOT NULL REFERENCES subjects(id),
  class_id     TEXT NOT NULL REFERENCES classes(id),
  teacher_id   TEXT NOT NULL REFERENCES teachers(id),
  due_date     TEXT NOT NULL,
  max_score    REAL DEFAULT 100,
  status       TEXT NOT NULL DEFAULT 'draft' CHECK(status IN ('draft','published','closed')),
  created_at   TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT NOT NULL DEFAULT (datetime('now')),
  published_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_assignments_class ON assignments(class_id);
CREATE INDEX IF NOT EXISTS idx_assignments_teacher ON assignments(teacher_id);

-- ── Submissions ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS submissions (
  id            TEXT PRIMARY KEY,
  assignment_id TEXT NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
  student_id    TEXT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  submitted_at  TEXT,
  status        TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','submitted','late','graded','returned')),
  score         REAL,
  feedback      TEXT,
  graded_by     TEXT REFERENCES teachers(id),
  graded_at     TEXT,
  created_at    TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at    TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(assignment_id, student_id)
);

-- ── Grades ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS grades (
  id               TEXT PRIMARY KEY,
  student_id       TEXT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  subject_id       TEXT NOT NULL REFERENCES subjects(id),
  class_id         TEXT NOT NULL REFERENCES classes(id),
  assessment_type  TEXT NOT NULL,
  assessment_title TEXT NOT NULL,
  score            REAL NOT NULL,
  max_score        REAL NOT NULL DEFAULT 100,
  letter_grade     TEXT,
  percentage       REAL,
  recorded_by      TEXT REFERENCES teachers(id),
  comments         TEXT,
  recorded_at      TEXT NOT NULL DEFAULT (datetime('now')),
  created_at       TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_grades_student ON grades(student_id);

-- ── Attendance ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attendance (
  id          TEXT PRIMARY KEY,
  student_id  TEXT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  class_id    TEXT NOT NULL REFERENCES classes(id),
  date        TEXT NOT NULL, -- YYYY-MM-DD
  status      TEXT NOT NULL CHECK(status IN ('present','absent','late','excused')),
  marked_by   TEXT REFERENCES teachers(id),
  notes       TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(student_id, class_id, date)
);

CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_class_date ON attendance(class_id, date);

-- ── Announcements ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS announcements (
  id          TEXT PRIMARY KEY,
  title       TEXT NOT NULL,
  body        TEXT NOT NULL,
  audience    TEXT NOT NULL DEFAULT 'all',
  priority    TEXT NOT NULL DEFAULT 'normal' CHECK(priority IN ('normal','high','urgent')),
  pinned      INTEGER DEFAULT 0,
  published   INTEGER DEFAULT 1,
  created_by  TEXT REFERENCES users(id),
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ── Notifications ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
  id         TEXT PRIMARY KEY,
  user_id    TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type       TEXT NOT NULL,
  title      TEXT NOT NULL,
  message    TEXT NOT NULL,
  link       TEXT,
  read       INTEGER DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);

-- ── Service Requests ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS service_requests (
  id           TEXT PRIMARY KEY,
  student_id   TEXT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  category     TEXT NOT NULL,
  type         TEXT NOT NULL,
  title        TEXT NOT NULL,
  description  TEXT,
  status       TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','pending','in_progress','completed','rejected')),
  priority     TEXT NOT NULL DEFAULT 'normal' CHECK(priority IN ('normal','high','urgent')),
  campus       TEXT,
  assignee     TEXT,
  comments     TEXT NOT NULL DEFAULT '[]',
  created_at   TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_service_requests_student ON service_requests(student_id);
CREATE INDEX IF NOT EXISTS idx_service_requests_status ON service_requests(status);

-- ── Audit Log ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_logs (
  id          TEXT PRIMARY KEY,
  actor_id    TEXT REFERENCES users(id),
  action      TEXT NOT NULL,
  resource    TEXT NOT NULL,
  resource_id TEXT,
  old_value   TEXT,
  new_value   TEXT,
  ip_address  TEXT,
  created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_logs(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at);
