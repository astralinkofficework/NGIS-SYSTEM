/**
 * NGIS School ERP — Parent Routes
 * All access is scoped to the parent's actual linked children.
 */

"use strict";

const express = require("express");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();

/**
 * GET /api/parent/children
 * Returns all children linked to the authenticated parent
 */
router.get("/children", authenticate, requireRole("parent"), (req, res) => {
  const db = getDb();
  const parent = db.prepare(`SELECT * FROM parents WHERE user_id = ?`).get(req.user.id);

  if (!parent) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Parent profile not found" },
    });
  }

  const children = db
    .prepare(
      `SELECT s.*, u.first_name, u.last_name, u.email, u.phone, u.avatar_url
       FROM students s
       JOIN parent_students ps ON ps.student_id = s.id
       JOIN users u ON u.id = s.user_id
       WHERE ps.parent_id = ?
       ORDER BY u.first_name`
    )
    .all(parent.id);

  res.json({ data: children, meta: { total: children.length } });
});

/**
 * GET /api/parent/children/:studentId
 * Secure access to a specific child (must be linked)
 */
router.get("/children/:studentId", authenticate, requireRole("parent"), (req, res) => {
  const db = getDb();
  const parent = db.prepare(`SELECT id FROM parents WHERE user_id = ?`).get(req.user.id);

  if (!parent) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Parent profile not found" },
    });
  }

  // Critical authorization check
  const link = db
    .prepare(`SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?`)
    .get(parent.id, req.params.studentId);

  if (!link) {
    return res.status(403).json({
      error: { code: "FORBIDDEN", message: "You do not have access to this student" },
    });
  }

  const student = db
    .prepare(
      `SELECT s.*, u.first_name, u.last_name, u.email, u.phone, u.avatar_url
       FROM students s
       JOIN users u ON u.id = s.user_id
       WHERE s.id = ?`
    )
    .get(req.params.studentId);

  if (!student) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Student not found" },
    });
  }

  res.json({ data: student });
});

/**
 * GET /api/parent/children/:studentId/grades
 * Parent can view grades of their own children only
 */
router.get("/children/:studentId/grades", authenticate, requireRole("parent"), (req, res) => {
  const db = getDb();
  const parent = db.prepare(`SELECT id FROM parents WHERE user_id = ?`).get(req.user.id);

  if (!parent) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Parent profile not found" } });
  }

  const link = db
    .prepare(`SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?`)
    .get(parent.id, req.params.studentId);

  if (!link) {
    return res.status(403).json({
      error: { code: "FORBIDDEN", message: "You do not have access to this student" },
    });
  }

  const grades = db
    .prepare(
      `SELECT g.*, sub.name as subject_name
       FROM grades g
       JOIN subjects sub ON sub.id = g.subject_id
       WHERE g.student_id = ?
       ORDER BY g.recorded_at DESC`
    )
    .all(req.params.studentId);

  res.json({ data: grades, meta: { total: grades.length } });
});

module.exports = router;
