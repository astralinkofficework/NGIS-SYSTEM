/**
 * NGIS School ERP — Announcements Routes
 */

"use strict";

const express = require("express");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();

/**
 * GET /api/announcements
 * Returns published announcements visible to the caller's role.
 * Admin/Teacher can also see drafts if ?all=1
 */
router.get("/", authenticate, (req, res) => {
  const db = getDb();
  const role = req.user.role;
  const showAll = req.query.all === "1" && (role === "admin" || role === "teacher");

  let rows;
  if (showAll) {
    rows = db.prepare(`
      SELECT a.*, u.first_name || ' ' || u.last_name as author_name
      FROM announcements a
      LEFT JOIN users u ON u.id = a.created_by
      ORDER BY a.pinned DESC, a.created_at DESC
      LIMIT 100
    `).all();
  } else {
    // Audience filter: all, role-specific, or class:/grade: prefixes (basic match)
    rows = db.prepare(`
      SELECT a.*, u.first_name || ' ' || u.last_name as author_name
      FROM announcements a
      LEFT JOIN users u ON u.id = a.created_by
      WHERE a.published = 1
        AND (
          a.audience = 'all'
          OR a.audience = ?
          OR a.audience LIKE 'class:%'
          OR a.audience LIKE 'grade:%'
        )
      ORDER BY a.pinned DESC, a.created_at DESC
      LIMIT 50
    `).all(role === "student" ? "students" : role === "parent" ? "parents" : role === "teacher" ? "teachers" : "all");

    // Tighten class/grade targeting for students
    if (role === "student") {
      const student = db.prepare(`SELECT class_id, grade FROM students WHERE user_id = ?`).get(req.user.id);
      if (student) {
        rows = rows.filter((a) => {
          if (a.audience === "all" || a.audience === "students") return true;
          if (a.audience === `class:${student.class_id}`) return true;
          if (a.audience === `grade:${student.grade}`) return true;
          if (a.audience.startsWith("class:") || a.audience.startsWith("grade:")) return false;
          return true;
        });
      }
    }
  }

  res.json({ data: rows, meta: { total: rows.length } });
});

/**
 * POST /api/announcements
 * Admin or Teacher create
 */
router.post("/", authenticate, requireRole("admin", "teacher"), (req, res) => {
  const db = getDb();
  const { title, body, audience, priority, pinned, published } = req.body || {};

  if (!title || !body) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "title and body are required" },
    });
  }

  const id = uuidv4();
  db.prepare(`
    INSERT INTO announcements (id, title, body, audience, priority, pinned, published, created_by)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    id,
    title,
    body,
    audience || "all",
    priority || "normal",
    pinned ? 1 : 0,
    published === false || published === 0 ? 0 : 1,
    req.user.id
  );

  const created = db.prepare(`SELECT * FROM announcements WHERE id = ?`).get(id);
  res.status(201).json({ data: created });
});

/**
 * PATCH /api/announcements/:id
 */
router.patch("/:id", authenticate, requireRole("admin", "teacher"), (req, res) => {
  const db = getDb();
  const existing = db.prepare(`SELECT * FROM announcements WHERE id = ?`).get(req.params.id);
  if (!existing) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Announcement not found" } });
  }

  // Teachers can only edit their own; admin can edit any
  if (req.user.role === "teacher" && existing.created_by !== req.user.id) {
    return res.status(403).json({ error: { code: "FORBIDDEN", message: "You can only edit your own announcements" } });
  }

  const title = req.body.title ?? existing.title;
  const body = req.body.body ?? existing.body;
  const audience = req.body.audience ?? existing.audience;
  const priority = req.body.priority ?? existing.priority;
  const pinned = req.body.pinned !== undefined ? (req.body.pinned ? 1 : 0) : existing.pinned;
  const published = req.body.published !== undefined ? (req.body.published ? 1 : 0) : existing.published;

  db.prepare(`
    UPDATE announcements
    SET title = ?, body = ?, audience = ?, priority = ?, pinned = ?, published = ?, updated_at = datetime('now')
    WHERE id = ?
  `).run(title, body, audience, priority, pinned, published, existing.id);

  const updated = db.prepare(`SELECT * FROM announcements WHERE id = ?`).get(existing.id);
  res.json({ data: updated });
});

/**
 * DELETE /api/announcements/:id
 */
router.delete("/:id", authenticate, requireRole("admin", "teacher"), (req, res) => {
  const db = getDb();
  const existing = db.prepare(`SELECT * FROM announcements WHERE id = ?`).get(req.params.id);
  if (!existing) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Announcement not found" } });
  }
  if (req.user.role === "teacher" && existing.created_by !== req.user.id) {
    return res.status(403).json({ error: { code: "FORBIDDEN", message: "You can only delete your own announcements" } });
  }

  db.prepare(`DELETE FROM announcements WHERE id = ?`).run(existing.id);
  res.json({ message: "Deleted" });
});

module.exports = router;
