/**
 * NGIS School ERP — Student Routes
 * Proper authorization based on role + relationship
 */

"use strict";

const express = require("express");
const { getDb } = require("../db/connection");
const {
  authenticate,
  requireRole,
  loadStudentProfile,
  loadParentProfile,
} = require("../middleware/auth");

const router = express.Router();

/**
 * GET /api/students/me
 * Student can only see their own profile
 */
router.get(
  "/me",
  authenticate,
  requireRole("student"),
  loadStudentProfile,
  (req, res) => {
    const db = getDb();
    const user = db
      .prepare(`SELECT first_name, last_name, email, phone, avatar_url FROM users WHERE id = ?`)
      .get(req.user.id);

    res.json({
      data: {
        ...req.student,
        firstName: user.first_name,
        lastName: user.last_name,
        email: user.email,
        phone: user.phone,
        avatarUrl: user.avatar_url,
      },
    });
  }
);

/**
 * GET /api/students/:id
 * - Admin: can view any student
 * - Teacher: can view students in their classes (simplified for now)
 * - Parent: can view only their linked children
 * - Student: can only view themselves
 */
router.get("/:id", authenticate, (req, res) => {
  const db = getDb();
  const studentId = req.params.id;

  const student = db
    .prepare(
      `SELECT s.*, u.first_name, u.last_name, u.email, u.phone, u.avatar_url
       FROM students s
       JOIN users u ON u.id = s.user_id
       WHERE s.id = ?`
    )
    .get(studentId);

  if (!student) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Student not found" },
    });
  }

  const role = req.user.role;

  // Student can only access own record
  if (role === "student") {
    if (student.user_id !== req.user.id) {
      return res.status(403).json({
        error: { code: "FORBIDDEN", message: "You can only access your own profile" },
      });
    }
  }

  // Parent can only access linked children
  if (role === "parent") {
    const parent = db.prepare(`SELECT id FROM parents WHERE user_id = ?`).get(req.user.id);
    if (!parent) {
      return res.status(403).json({ error: { code: "FORBIDDEN", message: "Parent profile not found" } });
    }

    const link = db
      .prepare(`SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?`)
      .get(parent.id, studentId);

    if (!link) {
      return res.status(403).json({
        error: { code: "FORBIDDEN", message: "You can only access your own children" },
      });
    }
  }

  // Teacher access will be refined later with class assignments
  // Admin has full access

  res.json({ data: student });
});

/**
 * GET /api/students
 * Admin only (list all)
 */
router.get("/", authenticate, requireRole("admin"), (req, res) => {
  const db = getDb();
  const students = db
    .prepare(
      `SELECT s.*, u.first_name, u.last_name, u.email, u.phone
       FROM students s
       JOIN users u ON u.id = s.user_id
       ORDER BY u.last_name, u.first_name`
    )
    .all();

  res.json({ data: students, meta: { total: students.length } });
});

module.exports = router;
