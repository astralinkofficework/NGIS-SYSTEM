/**
 * NGIS School ERP — Grades Routes
 */

"use strict";

const express = require("express");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");
const { createNotification } = require("./notifications");
const { writeAudit } = require("../lib/audit");

const router = express.Router();

function letterFromPercent(p) {
  if (p >= 90) return "A";
  if (p >= 80) return "B";
  if (p >= 70) return "C";
  if (p >= 60) return "D";
  return "F";
}

router.get("/", authenticate, (req, res) => {
  const db = getDb();
  const role = req.user.role;

  if (role === "student") {
    const student = db.prepare(`SELECT id FROM students WHERE user_id = ?`).get(req.user.id);
    if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });

    const rows = db.prepare(`
      SELECT g.*, s.name as subject_name
      FROM grades g
      LEFT JOIN subjects s ON s.id = g.subject_id
      WHERE g.student_id = ?
      ORDER BY g.recorded_at DESC
    `).all(student.id);
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  if (role === "parent") {
    const studentId = req.query.studentId;
    if (!studentId) {
      return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "studentId required" } });
    }
    const parent = db.prepare(`SELECT id FROM parents WHERE user_id = ?`).get(req.user.id);
    if (!parent) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Parent not found" } });

    const link = db.prepare(`SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?`).get(parent.id, studentId);
    if (!link) return res.status(403).json({ error: { code: "FORBIDDEN", message: "Access denied" } });

    const rows = db.prepare(`
      SELECT g.*, s.name as subject_name
      FROM grades g
      LEFT JOIN subjects s ON s.id = g.subject_id
      WHERE g.student_id = ?
      ORDER BY g.recorded_at DESC
    `).all(studentId);
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  if (role === "teacher") {
    const teacher = db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (!teacher) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher not found" } });

    const rows = db.prepare(`
      SELECT g.*, s.name as subject_name, st.student_number,
             u.first_name || ' ' || u.last_name as student_name
      FROM grades g
      LEFT JOIN subjects s ON s.id = g.subject_id
      LEFT JOIN students st ON st.id = g.student_id
      LEFT JOIN users u ON u.id = st.user_id
      WHERE g.recorded_by = ?
      ORDER BY g.recorded_at DESC
    `).all(teacher.id);
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  if (role === "admin") {
    const rows = db.prepare(`
      SELECT g.*, s.name as subject_name
      FROM grades g
      LEFT JOIN subjects s ON s.id = g.subject_id
      ORDER BY g.recorded_at DESC
      LIMIT 200
    `).all();
    return res.json({ data: rows, meta: { total: rows.length } });
  }

  return res.status(403).json({ error: { code: "FORBIDDEN", message: "Access denied" } });
});

router.post("/", authenticate, requireRole("teacher", "admin"), (req, res) => {
  const db = getDb();
  const { studentId, subjectId, classId, assessmentType, assessmentTitle, score, maxScore, comments } = req.body;

  if (!studentId || !subjectId || !classId || score === undefined) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "studentId, subjectId, classId, and score are required" },
    });
  }

  let recordedBy = null;
  if (req.user.role === "teacher") {
    const teacher = db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (!teacher) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher not found" } });
    recordedBy = teacher.id;
  }

  const max = maxScore || 100;
  const percentage = (Number(score) / max) * 100;
  const letter = letterFromPercent(percentage);
  const title = assessmentTitle || "Assessment";

  const id = uuidv4();
  db.prepare(`
    INSERT INTO grades (id, student_id, subject_id, class_id, assessment_type, assessment_title, score, max_score, letter_grade, percentage, recorded_by, comments)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    id, studentId, subjectId, classId,
    assessmentType || "exam",
    title,
    score, max, letter, percentage,
    recordedBy, comments || ""
  );

  writeAudit(db, {
    actorId: req.user.id,
    action: "create",
    resource: "grade",
    resourceId: id,
    newValue: { studentId, subjectId, score, max, letter, title },
    ip: req.ip,
  });

  try {
    const student = db.prepare(`SELECT user_id FROM students WHERE id = ?`).get(studentId);
    if (student) {
      createNotification(db, {
        userId: student.user_id,
        type: "grade",
        title: "New grade posted",
        message: `${title}: ${score}/${max} (${letter})`,
        link: "/pages/student/student-grades.html",
      });
    }
  } catch (_) { /* non-fatal */ }

  const created = db.prepare(`SELECT * FROM grades WHERE id = ?`).get(id);
  res.status(201).json({ data: created });
});

module.exports = router;
