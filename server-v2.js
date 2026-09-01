/**
 * ============================================================
 * NGIS School Management System — Connected ERP Server (v2)
 * Phase 1: Real Database + Authentication + RBAC
 * ============================================================
 * Run:  node server-v2.js
 * URL:  http://localhost:3000
 * ============================================================
 */

"use strict";

require("dotenv").config();

const express = require("express");
const path = require("path");
const http = require("http");
const cors = require("cors");
const fs = require("fs");

const { getDb } = require("./backend/db/connection");
const authRoutes = require("./backend/routes/auth");
const studentRoutes = require("./backend/routes/students");
const parentRoutes = require("./backend/routes/parent");
const assignmentRoutes = require("./backend/routes/assignments");
const { authenticate, requireRole } = require("./backend/middleware/auth");

const app = express();
const PORT = process.env.PORT || 3000;
const ROOT = __dirname;

/* ── Ensure database exists ─────────────────────────────────── */
const DB_PATH = path.join(__dirname, "backend/db/ngis.sqlite");
if (!fs.existsSync(DB_PATH)) {
  console.log("Database not found. Please run:");
  console.log("  npm install");
  console.log("  npm run db:init");
  console.log("  npm run db:seed");
  process.exit(1);
}

/* ── Middleware ─────────────────────────────────────────────── */
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* Security headers */
app.use((_req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  next();
});

/* ── Static files ───────────────────────────────────────────── */
app.use(express.static(ROOT, {
  extensions: ["html"],
  index: "index.html",
  etag: true,
  maxAge: "1h",
}));

/* ── API Routes ─────────────────────────────────────────────── */
app.use("/api/auth", authRoutes);
app.use("/api/students", studentRoutes);
app.use("/api/parent", parentRoutes);
app.use("/api/assignments", assignmentRoutes);

/* ── Health ─────────────────────────────────────────────────── */
app.get("/api/health", (_req, res) => {
  res.json({
    status: "ok",
    version: "2.0.0",
    name: "NGIS Connected School ERP",
    time: new Date().toISOString(),
  });
});

/* ── Additional Protected Routes ────────────────────────────── */

app.get("/api/admin/students", authenticate, requireRole("admin"), (req, res) => {
  const db = getDb();
  const students = db.prepare(`
    SELECT s.*, u.first_name, u.last_name, u.email, u.phone
    FROM students s
    JOIN users u ON u.id = s.user_id
    ORDER BY u.last_name, u.first_name
  `).all();
  res.json({ data: students, meta: { total: students.length } });
});

app.get("/api/student/dashboard", authenticate, requireRole("student"), (req, res) => {
  const db = getDb();
  const student = db.prepare(`SELECT * FROM students WHERE user_id = ?`).get(req.user.id);
  if (!student) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student profile not found" } });
  }
  const unread = db.prepare(
    `SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND read = 0`
  ).get(req.user.id);
  res.json({
    data: {
      student,
      user: req.user,
      unreadNotifications: unread.count,
      gpa: student.gpa,
      attendanceRate: student.attendance_rate,
    },
  });
});

app.get("/api/teacher/me", authenticate, requireRole("teacher"), (req, res) => {
  const db = getDb();
  const teacher = db.prepare(`SELECT * FROM teachers WHERE user_id = ?`).get(req.user.id);
  if (!teacher) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher profile not found" } });
  }
  res.json({ data: { teacher, user: req.user } });
});

/* ── Catch-all ──────────────────────────────────────────────── */
app.get("*", (req, res) => {
  if (req.path.match(/\.(css|js|png|jpg|jpeg|gif|svg|ico|woff2?|ttf|eot|map)$/)) {
    return res.status(404).send("Not found");
  }
  res.sendFile(path.join(ROOT, "index.html"));
});

/* ── Start ──────────────────────────────────────────────────── */
const server = http.createServer(app);

server.listen(PORT, () => {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║   NGIS — Connected School ERP (Phase 1)                  ║");
  console.log("║   Real Database + Authentication + RBAC + Assignments    ║");
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log(`║   Running at:  http://localhost:${PORT}                       ║`);
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log("║   Key Endpoints:                                         ║");
  console.log("║   POST /api/auth/login                                   ║");
  console.log("║   GET  /api/auth/me                                      ║");
  console.log("║   GET  /api/assignments                                  ║");
  console.log("║   POST /api/assignments                                  ║");
  console.log("║   POST /api/assignments/:id/submit                       ║");
  console.log("║   POST /api/assignments/:id/grade                        ║");
  console.log("║   GET  /api/parent/children                              ║");
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log("║   Demo accounts (password: password123)                  ║");
  console.log("║   admin@ngis.edu.kh / sophea@ngis.edu.kh                 ║");
  console.log("║   nrinphouneta@ngis.edu.kh / parent.hok@gmail.com        ║");
  console.log("╚══════════════════════════════════════════════════════════╝");
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`\n  ✗  Port ${PORT} is already in use.\n`);
  } else {
    console.error("Server error:", err);
  }
  process.exit(1);
});

module.exports = app;
