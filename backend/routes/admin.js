/**
 * NGIS School ERP — Admin utility routes
 */

"use strict";

const express = require("express");
const bcrypt = require("bcryptjs");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();

router.use(authenticate, requireRole("admin"));

/**
 * POST /api/admin/teachers
 * Create teacher user + profile
 */
router.post("/teachers", (req, res) => {
  const db = getDb();
  const { email, password, firstName, lastName, phone, employeeNumber, department } = req.body || {};

  if (!email || !firstName || !lastName || !employeeNumber) {
    return res.status(400).json({
      error: {
        code: "VALIDATION_ERROR",
        message: "email, firstName, lastName, and employeeNumber are required",
      },
    });
  }

  const normalizedEmail = String(email).toLowerCase().trim();
  if (db.prepare(`SELECT id FROM users WHERE email = ?`).get(normalizedEmail)) {
    return res.status(409).json({ error: { code: "CONFLICT", message: "Email already registered" } });
  }
  if (db.prepare(`SELECT id FROM teachers WHERE employee_number = ?`).get(employeeNumber)) {
    return res.status(409).json({ error: { code: "CONFLICT", message: "Employee number already exists" } });
  }

  const userId = uuidv4();
  const teacherId = uuidv4();
  const tempPassword = password || "password123";
  const hash = bcrypt.hashSync(tempPassword, 10);

  try {
    const tx = db.transaction(() => {
      db.prepare(`
        INSERT INTO users (id, email, password_hash, role, status, first_name, last_name, phone)
        VALUES (?, ?, ?, 'teacher', 'active', ?, ?, ?)
      `).run(userId, normalizedEmail, hash, firstName, lastName, phone || null);

      db.prepare(`
        INSERT INTO teachers (id, user_id, employee_number, department, hire_date)
        VALUES (?, ?, ?, ?, date('now'))
      `).run(teacherId, userId, employeeNumber, department || null);
    });
    tx();
  } catch (err) {
    return res.status(500).json({ error: { code: "SERVER_ERROR", message: err.message } });
  }

  const created = db.prepare(`
    SELECT t.*, u.first_name, u.last_name, u.email, u.phone
    FROM teachers t JOIN users u ON u.id = t.user_id
    WHERE t.id = ?
  `).get(teacherId);

  res.status(201).json({
    data: created,
    meta: { temporaryPassword: password ? undefined : tempPassword },
  });
});

/**
 * POST /api/admin/parents
 * Create parent user + profile
 */
router.post("/parents", (req, res) => {
  const db = getDb();
  const { email, password, firstName, lastName, phone, relationship } = req.body || {};

  if (!email || !firstName || !lastName) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "email, firstName, and lastName are required" },
    });
  }

  const normalizedEmail = String(email).toLowerCase().trim();
  if (db.prepare(`SELECT id FROM users WHERE email = ?`).get(normalizedEmail)) {
    return res.status(409).json({ error: { code: "CONFLICT", message: "Email already registered" } });
  }

  const userId = uuidv4();
  const parentId = uuidv4();
  const tempPassword = password || "password123";
  const hash = bcrypt.hashSync(tempPassword, 10);

  try {
    const tx = db.transaction(() => {
      db.prepare(`
        INSERT INTO users (id, email, password_hash, role, status, first_name, last_name, phone)
        VALUES (?, ?, ?, 'parent', 'active', ?, ?, ?)
      `).run(userId, normalizedEmail, hash, firstName, lastName, phone || null);

      db.prepare(`
        INSERT INTO parents (id, user_id, relationship)
        VALUES (?, ?, ?)
      `).run(parentId, userId, relationship || "guardian");
    });
    tx();
  } catch (err) {
    return res.status(500).json({ error: { code: "SERVER_ERROR", message: err.message } });
  }

  const created = db.prepare(`
    SELECT p.*, u.first_name, u.last_name, u.email, u.phone
    FROM parents p JOIN users u ON u.id = p.user_id
    WHERE p.id = ?
  `).get(parentId);

  res.status(201).json({
    data: created,
    meta: { temporaryPassword: password ? undefined : tempPassword },
  });
});

/**
 * POST /api/admin/link-parent-student
 * Body: { parentId, studentId, isPrimary? }
 */
router.post("/link-parent-student", (req, res) => {
  const db = getDb();
  const { parentId, studentId, isPrimary } = req.body || {};

  if (!parentId || !studentId) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "parentId and studentId are required" },
    });
  }

  const parent = db.prepare(`SELECT id FROM parents WHERE id = ?`).get(parentId);
  const student = db.prepare(`SELECT id FROM students WHERE id = ?`).get(studentId);
  if (!parent || !student) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Parent or student not found" } });
  }

  const existing = db.prepare(`
    SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?
  `).get(parentId, studentId);

  if (existing) {
    return res.status(409).json({ error: { code: "CONFLICT", message: "Already linked" } });
  }

  db.prepare(`
    INSERT INTO parent_students (parent_id, student_id, is_primary)
    VALUES (?, ?, ?)
  `).run(parentId, studentId, isPrimary ? 1 : 0);

  res.status(201).json({ message: "Parent linked to student", data: { parentId, studentId } });
});

/**
 * GET /api/admin/parents — list parents
 */
router.get("/parents", (req, res) => {
  const db = getDb();
  const rows = db.prepare(`
    SELECT p.*, u.first_name, u.last_name, u.email, u.phone
    FROM parents p JOIN users u ON u.id = p.user_id
    ORDER BY u.last_name, u.first_name
  `).all();
  res.json({ data: rows, meta: { total: rows.length } });
});

/**
 * GET /api/admin/teachers — list teachers
 */
router.get("/teachers", (req, res) => {
  const db = getDb();
  const rows = db.prepare(`
    SELECT t.*, u.first_name, u.last_name, u.email, u.phone
    FROM teachers t JOIN users u ON u.id = t.user_id
    ORDER BY u.last_name, u.first_name
  `).all();
  res.json({ data: rows, meta: { total: rows.length } });
});

module.exports = router;
