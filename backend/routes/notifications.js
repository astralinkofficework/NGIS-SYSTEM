/**
 * NGIS School ERP — Notifications Routes
 */

"use strict";

const express = require("express");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();

/** Helper used by other modules */
function createNotification(db, { userId, type, title, message, link }) {
  const id = uuidv4();
  db.prepare(`
    INSERT INTO notifications (id, user_id, type, title, message, link, read)
    VALUES (?, ?, ?, ?, ?, ?, 0)
  `).run(id, userId, type || "info", title, message, link || null);
  return id;
}

/**
 * GET /api/notifications
 */
router.get("/", authenticate, (req, res) => {
  const db = getDb();
  const rows = db.prepare(`
    SELECT * FROM notifications
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT 50
  `).all(req.user.id);

  const unread = rows.filter((r) => !r.read).length;
  res.json({ data: rows, meta: { total: rows.length, unread } });
});

/**
 * POST /api/notifications/:id/read
 */
router.post("/:id/read", authenticate, (req, res) => {
  const db = getDb();
  const row = db.prepare(`SELECT * FROM notifications WHERE id = ? AND user_id = ?`).get(req.params.id, req.user.id);
  if (!row) {
    return res.status(404).json({ error: { code: "NOT_FOUND", message: "Notification not found" } });
  }
  db.prepare(`UPDATE notifications SET read = 1 WHERE id = ?`).run(row.id);
  res.json({ message: "Marked as read" });
});

/**
 * POST /api/notifications/read-all
 */
router.post("/read-all", authenticate, (req, res) => {
  const db = getDb();
  const result = db.prepare(`UPDATE notifications SET read = 1 WHERE user_id = ? AND read = 0`).run(req.user.id);
  res.json({ message: "All marked as read", meta: { updated: result.changes } });
});

/**
 * POST /api/notifications  (admin only — manual broadcast test)
 * Body: { userId, type, title, message, link? }
 */
router.post("/", authenticate, requireRole("admin"), (req, res) => {
  const db = getDb();
  const { userId, type, title, message, link } = req.body || {};
  if (!userId || !title || !message) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "userId, title, and message are required" },
    });
  }
  const id = createNotification(db, { userId, type, title, message, link });
  const created = db.prepare(`SELECT * FROM notifications WHERE id = ?`).get(id);
  res.status(201).json({ data: created });
});

module.exports = router;
module.exports.createNotification = createNotification;
