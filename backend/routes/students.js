/**
 * NGIS School ERP — Student Routes
 */

"use strict";

const express = require("express");
const bcrypt = require("bcryptjs");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const {
  authenticate,
  requireRole,
  loadStudentProfile,
} = require("../middleware/auth");

const router = express.Router();

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
 * POST /api/students
 * Admin creates a student user + profile
 * Body: { email, password?, firstName, lastName, phone?, studentNumber, grade, classId?, house? }
 */
router.post("/", authenticate, requireRole("admin"), (req, res) => {
  const db = getDb();
  const {
    email,
    password,
    firstName,
    lastName,
    phone,
    studentNumber,
    grade,
    classId,
    house,
    dateOfBirth,
  } = req.body || {};

  if (!email || !firstName || !lastName || !studentNumber || !grade) {
    return res.status(400).json({
      error: {
        code: "VALIDATION_ERROR",
        message: "email, firstName, lastName, studentNumber, and grade are required",
      },
    });
  }

  const normalizedEmail = String(email).toLowerCase().trim();
  const existing = db.prepare(`SELECT id FROM users WHERE email = ?`).get(normalizedEmail);
  if (existing) {
    return res.status(409).json({
      error: { code: "CONFLICT", message: "Email already registered" },
    });
  }

  const existingNumber = db.prepare(`SELECT id FROM students WHERE student_number = ?`).get(studentNumber);
  if (existingNumber) {
    return res.status(409).json({
      error: { code: "CONFLICT", message: "Student number already exists" },
    });
  }

  const userId = uuidv4();
  const studentId = uuidv4();
  const tempPassword = password || "password123";
  const hash = bcrypt.hashSync(tempPassword, 10);

  const tx = db.transaction(() => {
    db.prepare(`
      INSERT INTO users (id, email, password_hash, role, status, first_name, last_name, phone)
      VALUES (?, ?, ?, 'student', 'active', ?, ?, ?)
    `).run(userId, normalizedEmail, hash, firstName, lastName, phone || null);

    db.prepare(`
      INSERT INTO students (id, user_id, student_number, grade, class_id, house, date_of_birth, enrollment_date, gpa, attendance_rate)
      VALUES (?, ?, ?, ?, ?, ?, ?, date('now'), 0, 100)
    `).run(
      studentId,
      userId,
      studentNumber,
      grade,
      classId || null,
      house || null,
      dateOfBirth || null
    );
  });

  try {
    tx();
  } catch (err) {
    return res.status(500).json({
      error: { code: "SERVER_ERROR", message: err.message || "Failed to create student" },
    });
  }

  const created = db.prepare(`
    SELECT s.*, u.first_name, u.last_name, u.email, u.phone
    FROM students s JOIN users u ON u.id = s.user_id
    WHERE s.id = ?
  `).get(studentId);

  res.status(201).json({
    data: created,
    meta: { temporaryPassword: password ? undefined : tempPassword },
  });
});

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

  if (role === "student") {
    if (student.user_id !== req.user.id) {
      return res.status(403).json({
        error: { code: "FORBIDDEN", message: "You can only access your own profile" },
      });
    }
  }

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

  res.json({ data: student });
});

module.exports = router;
