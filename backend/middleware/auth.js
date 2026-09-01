/**
 * NGIS School ERP — Authentication & Authorization Middleware
 *
 * Never trust role information sent by the frontend.
 * The backend determines the authenticated user's identity and permissions.
 */

"use strict";

const jwt = require("jsonwebtoken");
const { getDb } = require("../db/connection");

const JWT_SECRET = process.env.JWT_SECRET || "ngis-dev-secret-change-in-production-2026";
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || "12h";

/**
 * Generate a signed JWT for a user
 */
function signToken(user) {
  return jwt.sign(
    {
      sub: user.id,
      role: user.role,
      email: user.email,
    },
    JWT_SECRET,
    { expiresIn: JWT_EXPIRES_IN }
  );
}

/**
 * Verify JWT and attach user to req.user
 */
function authenticate(req, res, next) {
  const header = req.headers.authorization;

  if (!header || !header.startsWith("Bearer ")) {
    return res.status(401).json({
      error: { code: "UNAUTHORIZED", message: "Authentication required" },
    });
  }

  const token = header.slice(7);

  try {
    const payload = jwt.verify(token, JWT_SECRET);
    const db = getDb();

    const user = db
      .prepare(
        `SELECT id, email, role, status, first_name, last_name, phone, avatar_url
         FROM users WHERE id = ?`
      )
      .get(payload.sub);

    if (!user) {
      return res.status(401).json({
        error: { code: "UNAUTHORIZED", message: "User no longer exists" },
      });
    }

    if (user.status !== "active") {
      return res.status(403).json({
        error: { code: "FORBIDDEN", message: "Account is not active" },
      });
    }

    // Attach clean user object (never trust frontend role)
    req.user = {
      id: user.id,
      email: user.email,
      role: user.role,
      status: user.status,
      firstName: user.first_name,
      lastName: user.last_name,
      phone: user.phone,
      avatarUrl: user.avatar_url,
    };

    next();
  } catch (err) {
    return res.status(401).json({
      error: { code: "UNAUTHORIZED", message: "Invalid or expired token" },
    });
  }
}

/**
 * Require one or more roles
 * Usage: requireRole('admin'), requireRole('teacher', 'admin')
 */
function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        error: { code: "UNAUTHORIZED", message: "Authentication required" },
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        error: {
          code: "FORBIDDEN",
          message: `This action requires one of the following roles: ${roles.join(", ")}`,
        },
      });
    }

    next();
  };
}

/**
 * Helper: load student record linked to the current user (if role = student)
 */
function loadStudentProfile(req, res, next) {
  if (req.user.role !== "student") return next();

  const db = getDb();
  const student = db
    .prepare(`SELECT * FROM students WHERE user_id = ?`)
    .get(req.user.id);

  if (!student) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Student profile not found" },
    });
  }

  req.student = student;
  next();
}

/**
 * Helper: load parent record + linked children
 */
function loadParentProfile(req, res, next) {
  if (req.user.role !== "parent") return next();

  const db = getDb();
  const parent = db
    .prepare(`SELECT * FROM parents WHERE user_id = ?`)
    .get(req.user.id);

  if (!parent) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Parent profile not found" },
    });
  }

  const children = db
    .prepare(
      `SELECT s.* FROM students s
       INNER JOIN parent_students ps ON ps.student_id = s.id
       WHERE ps.parent_id = ?`
    )
    .all(parent.id);

  req.parent = parent;
  req.children = children;
  next();
}

/**
 * Helper: load teacher record
 */
function loadTeacherProfile(req, res, next) {
  if (req.user.role !== "teacher") return next();

  const db = getDb();
  const teacher = db
    .prepare(`SELECT * FROM teachers WHERE user_id = ?`)
    .get(req.user.id);

  if (!teacher) {
    return res.status(404).json({
      error: { code: "NOT_FOUND", message: "Teacher profile not found" },
    });
  }

  req.teacher = teacher;
  next();
}

module.exports = {
  signToken,
  authenticate,
  requireRole,
  loadStudentProfile,
  loadParentProfile,
  loadTeacherProfile,
  JWT_SECRET,
};
