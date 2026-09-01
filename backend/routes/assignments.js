/**
 * NGIS School ERP — Assignments Routes
 * Teacher: create, list own, grade
 * Student: list own class assignments, submit
 * Parent: view child's assignments
 * Admin: full access
 */

"use strict";

const express = require("express");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();

/**
 * GET /api/assignments
 * Role-scoped list
 */
router.get("/", authenticate, (req, res) => {
  const db = getDb();
  const role = req.user.role;

  if (role === "admin") {
    const rows = db.prepare(`
      SELECT a.*, s.name as subject_name, c.name as class_name,
             u.first_name || ' ' || u.last_name as teacher_name
      FROM assignments a
      LEFT JOIN subjects s ON s.id = a.subject_id
      LEFT JOIN classes c ON c.id = a.class_id
      LEFT JOIN teachers t ON t.id = a.teacher_id
      LEFT JOIN users u ON u.id = t.user_id
      ORDER BY a.due_date DESC
    `).all();
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  if (role === "teacher") {
    const teacher = db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (!teacher) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher profile not found" } });

    const rows = db.prepare(`
      SELECT a.*, s.name as subject_name, c.name as class_name
      FROM assignments a
      LEFT JOIN subjects s ON s.id = a.subject_id
      LEFT JOIN classes c ON c.id = a.class_id
      WHERE a.teacher_id = ?
      ORDER BY a.due_date DESC
    `).all(teacher.id);
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  if (role === "student") {
    const student = db.prepare(`SELECT * FROM students WHERE user_id = ?`).get(req.user.id);
    if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student profile not found" } });

    const rows = db.prepare(`
      SELECT a.*, s.name as subject_name, c.name as class_name,
             sub.status as submission_status, sub.score, sub.submitted_at
      FROM assignments a
      LEFT JOIN subjects s ON s.id = a.subject_id
      LEFT JOIN classes c ON c.id = a.class_id
      LEFT JOIN submissions sub ON sub.assignment_id = a.id AND sub.student_id = ?
      WHERE a.class_id = ? AND a.status = 'published'
      ORDER BY a.due_date ASC
    `).all(student.id, student.class_id);
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  if (role === "parent") {
    // Parent must pass ?studentId= and we verify relationship
    const studentId = req.query.studentId;
    if (!studentId) {
      return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "studentId query param required" } });
    }

    const parent = db.prepare(`SELECT id FROM parents WHERE user_id = ?`).get(req.user.id);
    if (!parent) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Parent profile not found" } });

    const link = db.prepare(`SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?`).get(parent.id, studentId);
    if (!link) {
      return res.status(403).json({ error: { code: "FORBIDDEN", message: "You do not have access to this student" } });
    }

    const student = db.prepare(`SELECT * FROM students WHERE id = ?`).get(studentId);
    if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });

    const rows = db.prepare(`
      SELECT a.*, s.name as subject_name,
             sub.status as submission_status, sub.score, sub.submitted_at
      FROM assignments a
      LEFT JOIN subjects s ON s.id = a.subject_id
      LEFT JOIN submissions sub ON sub.assignment_id = a.id AND sub.student_id = ?
      WHERE a.class_id = ? AND a.status = 'published'
      ORDER BY a.due_date ASC
    `).all(studentId, student.class_id);
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  return res.status(403).json({ error: { code: "FORBIDDEN", message: "Access denied" } });
});

/**
 * POST /api/assignments
 * Teacher (or Admin) creates an assignment
 */
router.post("/", authenticate, requireRole("teacher", "admin"), (req, res) => {
  const db = getDb();
  const { title, description, subjectId, classId, dueDate, maxScore } = req.body;

  if (!title || !subjectId || !classId || !dueDate) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "title, subjectId, classId, and dueDate are required" },
    });
  }

  let teacherId = null;

  if (req.user.role === "teacher") {
    const teacher = db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (!teacher) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher profile not found" } });
    teacherId = teacher.id;
  } else {
    // Admin can optionally pass teacherId
    teacherId = req.body.teacherId || null;
  }

  const id = uuidv4();
  db.prepare(`
    INSERT INTO assignments (id, title, description, subject_id, class_id, teacher_id, due_date, max_score, status, published_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'published', datetime('now'))
  `).run(id, title, description || "", subjectId, classId, teacherId, dueDate, maxScore || 100);

  const created = db.prepare(`SELECT * FROM assignments WHERE id = ?`).get(id);
  res.status(201).json({ data: created });
});

/**
 * POST /api/assignments/:id/submit
 * Student submits work
 */
router.post("/:id/submit", authenticate, requireRole("student"), (req, res) => {
  const db = getDb();
  const assignmentId = req.params.id;

  const student = db.prepare(`SELECT * FROM students WHERE user_id = ?`).get(req.user.id);
  if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student profile not found" } });

  const assignment = db.prepare(`SELECT * FROM assignments WHERE id = ? AND status = 'published'`).get(assignmentId);
  if (!assignment) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Assignment not found" } });

  // Student must belong to the assignment's class
  if (student.class_id !== assignment.class_id) {
    return res.status(403).json({ error: { code: "FORBIDDEN", message: "This assignment is not for your class" } });
  }

  const existing = db.prepare(`SELECT id FROM submissions WHERE assignment_id = ? AND student_id = ?`).get(assignmentId, student.id);

  const now = new Date().toISOString();
  const isLate = assignment.due_date && now > assignment.due_date + "T23:59:59";

  if (existing) {
    db.prepare(`
      UPDATE submissions SET status = ?, submitted_at = ?, updated_at = datetime('now')
      WHERE id = ?
    `).run(isLate ? "late" : "submitted", now, existing.id);

    const updated = db.prepare(`SELECT * FROM submissions WHERE id = ?`).get(existing.id);
    return res.json({ data: updated, message: "Submission updated" });
  }

  const id = uuidv4();
  db.prepare(`
    INSERT INTO submissions (id, assignment_id, student_id, submitted_at, status)
    VALUES (?, ?, ?, ?, ?)
  `).run(id, assignmentId, student.id, now, isLate ? "late" : "submitted");

  const created = db.prepare(`SELECT * FROM submissions WHERE id = ?`).get(id);
  res.status(201).json({ data: created, message: "Submitted successfully" });
});

/**
 * POST /api/assignments/:id/grade
 * Teacher grades a student's submission
 * Body: { studentId, score, feedback }
 */
router.post("/:id/grade", authenticate, requireRole("teacher", "admin"), (req, res) => {
  const db = getDb();
  const assignmentId = req.params.id;
  const { studentId, score, feedback } = req.body;

  if (!studentId || score === undefined) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "studentId and score are required" } });
  }

  const assignment = db.prepare(`SELECT * FROM assignments WHERE id = ?`).get(assignmentId);
  if (!assignment) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Assignment not found" } });

  // Teacher can only grade their own assignments
  if (req.user.role === "teacher") {
    const teacher = db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (!teacher || teacher.id !== assignment.teacher_id) {
      return res.status(403).json({ error: { code: "FORBIDDEN", message: "You can only grade your own assignments" } });
    }
  }

  let submission = db.prepare(`SELECT * FROM submissions WHERE assignment_id = ? AND student_id = ?`).get(assignmentId, studentId);

  if (!submission) {
    // Create a graded submission even if student didn't submit
    const id = uuidv4();
    db.prepare(`
      INSERT INTO submissions (id, assignment_id, student_id, status, score, feedback, graded_by, graded_at)
      VALUES (?, ?, ?, 'graded', ?, ?, ?, datetime('now'))
    `).run(id, assignmentId, studentId, score, feedback || "", req.user.role === "teacher" ? 
      db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id)?.id : null);
    submission = db.prepare(`SELECT * FROM submissions WHERE id = ?`).get(id);
  } else {
    db.prepare(`
      UPDATE submissions
      SET status = 'graded', score = ?, feedback = ?, graded_at = datetime('now'), updated_at = datetime('now')
      WHERE id = ?
    `).run(score, feedback || "", submission.id);
    submission = db.prepare(`SELECT * FROM submissions WHERE id = ?`).get(submission.id);
  }

  res.json({ data: submission, message: "Graded successfully" });
});

module.exports = router;
