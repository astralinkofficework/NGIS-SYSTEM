/**
 * NGIS School ERP — Authentication Routes
 */

"use strict";

const express = require("express");
const bcrypt = require("bcryptjs");
const { getDb } = require("../db/connection");
const { signToken, authenticate } = require("../middleware/auth");

const router = express.Router();

router.post("/login", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "email and password are required" },
    });
  }

  const db = getDb();
  const user = db
    .prepare(
      `SELECT id, email, password_hash, role, status, first_name, last_name, phone, avatar_url
       FROM users WHERE email = ?`
    )
    .get(email.toLowerCase().trim());

  if (!user) {
    return res.status(401).json({
      error: { code: "INVALID_CREDENTIALS", message: "Invalid email or password" },
    });
  }

  if (user.status !== "active") {
    return res.status(403).json({
      error: { code: "ACCOUNT_INACTIVE", message: "Your account is not active" },
    });
  }

  const valid = bcrypt.compareSync(password, user.password_hash);
  if (!valid) {
    return res.status(401).json({
      error: { code: "INVALID_CREDENTIALS", message: "Invalid email or password" },
    });
  }

  db.prepare(`UPDATE users SET last_login_at = datetime('now') WHERE id = ?`).run(user.id);

  const token = signToken(user);
  const profile = {
    id: user.id,
    email: user.email,
    role: user.role,
    firstName: user.first_name,
    lastName: user.last_name,
    phone: user.phone,
    avatarUrl: user.avatar_url,
  };

  if (user.role === "student") {
    const student = db.prepare(`SELECT * FROM students WHERE user_id = ?`).get(user.id);
    if (student) profile.student = student;
  } else if (user.role === "teacher") {
    const teacher = db.prepare(`SELECT * FROM teachers WHERE user_id = ?`).get(user.id);
    if (teacher) profile.teacher = teacher;
  } else if (user.role === "parent") {
    const parent = db.prepare(`SELECT * FROM parents WHERE user_id = ?`).get(user.id);
    if (parent) {
      profile.parent = parent;
      profile.children = db
        .prepare(
          `SELECT s.* FROM students s
           INNER JOIN parent_students ps ON ps.student_id = s.id
           WHERE ps.parent_id = ?`
        )
        .all(parent.id);
    }
  }

  res.json({ data: { token, user: profile } });
});

router.get("/me", authenticate, (req, res) => {
  const db = getDb();
  const profile = { ...req.user };

  if (req.user.role === "student") {
    const student = db.prepare(`SELECT * FROM students WHERE user_id = ?`).get(req.user.id);
    if (student) profile.student = student;
  } else if (req.user.role === "teacher") {
    const teacher = db.prepare(`SELECT * FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (teacher) profile.teacher = teacher;
  } else if (req.user.role === "parent") {
    const parent = db.prepare(`SELECT * FROM parents WHERE user_id = ?`).get(req.user.id);
    if (parent) {
      profile.parent = parent;
      profile.children = db
        .prepare(
          `SELECT s.* FROM students s
           INNER JOIN parent_students ps ON ps.student_id = s.id
           WHERE ps.parent_id = ?`
        )
        .all(parent.id);
    }
  }

  res.json({ data: profile });
});

/**
 * POST /api/auth/change-password
 * Body: { currentPassword, newPassword }
 */
router.post("/change-password", authenticate, (req, res) => {
  const { currentPassword, newPassword } = req.body || {};

  if (!currentPassword || !newPassword) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "currentPassword and newPassword are required" },
    });
  }

  if (String(newPassword).length < 8) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "New password must be at least 8 characters" },
    });
  }

  const db = getDb();
  const user = db.prepare(`SELECT id, password_hash FROM users WHERE id = ?`).get(req.user.id);
  if (!user) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "User not found" } });
  }

  if (!bcrypt.compareSync(currentPassword, user.password_hash)) {
    return res.status(401).json({
      error: { code: "INVALID_CREDENTIALS", message: "Current password is incorrect" },
    });
  }

  const hash = bcrypt.hashSync(newPassword, 10);
  db.prepare(`UPDATE users SET password_hash = ?, updated_at = datetime('now') WHERE id = ?`).run(hash, user.id);

  res.json({ message: "Password updated successfully" });
});

module.exports = router;
