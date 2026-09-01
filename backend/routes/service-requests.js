"use strict";

const express = require("express");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();
const VALID_STATUSES = new Set(["open", "pending", "in_progress", "completed", "rejected"]);
const VALID_PRIORITIES = new Set(["normal", "high", "urgent"]);

function parseRequest(row) {
  if (!row) return row;
  return { ...row, studentName: row.student_name || undefined, comments: JSON.parse(row.comments || "[]") };
}

function studentForUser(db, userId) {
  return db.prepare("SELECT students.id AS id, student_number, users.first_name, users.last_name, class_id FROM students JOIN users ON users.id = students.user_id WHERE users.id = ?").get(userId);
}

router.get("/", authenticate, (req, res) => {
  const db = getDb();
  const params = [];
  let where = "";
  if (req.user.role === "student") {
    const student = studentForUser(db, req.user.id);
    if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student profile not found" } });
    where = "WHERE r.student_id = ?";
    params.push(student.id);
  } else if (req.user.role === "parent") {
    where = "WHERE r.student_id IN (SELECT student_id FROM parent_students WHERE parent_id = (SELECT id FROM parents WHERE user_id = ?))";
    params.push(req.user.id);
  } else if (req.user.role !== "admin") {
    return res.status(403).json({ error: { code: "FORBIDDEN", message: "This action is not available to your role" } });
  }
  if (req.query.studentId) {
    where += where ? " AND (r.student_id = ? OR s.student_number = ?)" : "WHERE (r.student_id = ? OR s.student_number = ?)";
    params.push(req.query.studentId, req.query.studentId);
  }
  if (req.query.status && VALID_STATUSES.has(req.query.status)) {
    where += where ? " AND r.status = ?" : "WHERE r.status = ?";
    params.push(req.query.status);
  }
  const rows = db.prepare(`SELECT r.*, s.student_number, u.first_name || ' ' || u.last_name AS student_name FROM service_requests r JOIN students s ON s.id = r.student_id JOIN users u ON u.id = s.user_id ${where} ORDER BY datetime(r.updated_at) DESC`).all(...params);
  res.json({ data: rows.map(parseRequest), meta: { total: rows.length } });
});

router.get("/:id", authenticate, (req, res) => {
  const db = getDb();
  const row = db.prepare("SELECT r.*, s.student_number, u.first_name || ' ' || u.last_name AS student_name FROM service_requests r JOIN students s ON s.id = r.student_id JOIN users u ON u.id = s.user_id WHERE r.id = ?").get(req.params.id);
  if (!row) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Service request not found" } });
  if (req.user.role === "admin") return res.json({ data: parseRequest(row) });
  if (req.user.role === "student") {
    const student = studentForUser(db, req.user.id);
    if (!student || student.id !== row.student_id) return res.status(403).json({ error: { code: "FORBIDDEN", message: "You cannot access this request" } });
  } else if (req.user.role === "parent") {
    const linked = db.prepare("SELECT 1 FROM parent_students ps JOIN parents p ON p.id = ps.parent_id WHERE p.user_id = ? AND ps.student_id = ?").get(req.user.id, row.student_id);
    if (!linked) return res.status(403).json({ error: { code: "FORBIDDEN", message: "You cannot access this request" } });
  } else return res.status(403).json({ error: { code: "FORBIDDEN", message: "This action is not available to your role" } });
  res.json({ data: parseRequest(row) });
});

router.post("/", authenticate, requireRole("student"), (req, res) => {
  const { category, type, title, description, priority, campus } = req.body || {};
  if (!category || !type || !title) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "category, type, and title are required" } });
  if (priority && !VALID_PRIORITIES.has(priority)) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Invalid priority" } });
  const db = getDb();
  const student = studentForUser(db, req.user.id);
  if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student profile not found" } });
  const id = `SR-${Date.now()}-${uuidv4().slice(0, 8)}`;
  db.prepare("INSERT INTO service_requests (id, student_id, category, type, title, description, priority, campus) VALUES (?, ?, ?, ?, ?, ?, ?, ?)").run(id, student.id, String(category).trim(), String(type).trim(), String(title).trim(), description ? String(description).trim() : null, priority || "normal", campus ? String(campus).trim() : null);
  res.status(201).json({ data: parseRequest(db.prepare("SELECT * FROM service_requests WHERE id = ?").get(id)) });
});

router.put("/:id", authenticate, requireRole("admin"), (req, res) => {
  const { status, comment, commentBy } = req.body || {};
  if (!status || !VALID_STATUSES.has(status)) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "A valid status is required" } });
  const db = getDb();
  const existing = db.prepare("SELECT * FROM service_requests WHERE id = ?").get(req.params.id);
  if (!existing) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Service request not found" } });
  const comments = JSON.parse(existing.comments || "[]");
  if (comment) comments.push({ by: commentBy || req.user.email, text: String(comment).trim(), date: new Date().toISOString().slice(0, 10) });
  db.prepare("UPDATE service_requests SET status = ?, comments = ?, updated_at = datetime('now') WHERE id = ?").run(status, JSON.stringify(comments), req.params.id);
  res.json({ data: parseRequest(db.prepare("SELECT * FROM service_requests WHERE id = ?").get(req.params.id)) });
});

module.exports = router;
