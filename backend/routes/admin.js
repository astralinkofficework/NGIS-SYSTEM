/**
 * NGIS School ERP — Admin utility routes
 */

"use strict";

const express = require("express");
const bcrypt = require("bcryptjs");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");
const { writeAudit } = require("../lib/audit");

const router = express.Router();

router.use(authenticate, requireRole("admin"));

/** GET /api/admin/stats */
router.get("/stats", (req, res) => {
  const db = getDb();
  const students = db.prepare(`SELECT COUNT(*) as c FROM students`).get().c;
  const teachers = db.prepare(`SELECT COUNT(*) as c FROM teachers`).get().c;
  const parents = db.prepare(`SELECT COUNT(*) as c FROM parents`).get().c;
  const classes = db.prepare(`SELECT COUNT(*) as c FROM classes`).get().c;
  const assignments = db.prepare(`SELECT COUNT(*) as c FROM assignments WHERE status = 'published'`).get().c;
  const grades = db.prepare(`SELECT COUNT(*) as c FROM grades`).get().c;
  const announcements = db.prepare(`SELECT COUNT(*) as c FROM announcements WHERE published = 1`).get().c;

  res.json({
    data: { students, teachers, parents, classes, assignments, grades, announcements },
  });
});

/** GET /api/admin/audit?limit=20 */
router.get("/audit", (req, res) => {
  const db = getDb();
  const limit = Math.min(Number(req.query.limit) || 20, 100);
  const rows = db.prepare(`
    SELECT a.*, u.first_name || ' ' || u.last_name as actor_name, u.email as actor_email
    FROM audit_logs a
    LEFT JOIN users u ON u.id = a.actor_id
    ORDER BY a.created_at DESC
    LIMIT ?
  `).all(limit);
  res.json({ data: rows, meta: { total: rows.length } });
});

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

  writeAudit(db, {
    actorId: req.user.id,
    action: "create",
    resource: "teacher",
    resourceId: teacherId,
    newValue: { email: normalizedEmail, employeeNumber },
    ip: req.ip,
  });

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

  writeAudit(db, {
    actorId: req.user.id,
    action: "create",
    resource: "parent",
    resourceId: parentId,
    newValue: { email: normalizedEmail },
    ip: req.ip,
  });

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

  writeAudit(db, {
    actorId: req.user.id,
    action: "link",
    resource: "parent_student",
    resourceId: `${parentId}:${studentId}`,
    newValue: { parentId, studentId },
    ip: req.ip,
  });

  res.status(201).json({ message: "Parent linked to student", data: { parentId, studentId } });
});

router.get("/parents", (req, res) => {
  const db = getDb();
  const rows = db.prepare(`
    SELECT p.*, u.first_name, u.last_name, u.email, u.phone
    FROM parents p JOIN users u ON u.id = p.user_id
    ORDER BY u.last_name, u.first_name
  `).all();
  res.json({ data: rows, meta: { total: rows.length } });
});

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
