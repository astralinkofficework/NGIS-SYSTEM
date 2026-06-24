"use strict";

const express = require("express");
const router  = express.Router();
const { requireAuth }       = require("../middleware/auth");
const {
  getUserClasses,
  getClassMessages,
  validateClassAccess,
  markClassRead,
  getClassMembers,
} = require("../db/group-queries");

// All routes require authentication
router.use(requireAuth);

// GET /api/classes — list classes the current user belongs to
router.get("/", async (req, res) => {
  try {
    const classes = await getUserClasses(req.user.id);
    res.json(classes);
  } catch (err) {
    console.error("[classes] getUserClasses:", err.message);
    res.status(500).json({ error: "Failed to load classes" });
  }
});

// GET /api/classes/:id/members — class member list
router.get("/:id/members", async (req, res) => {
  try {
    await validateClassAccess(req.params.id, req.user.id);
    const members = await getClassMembers(req.params.id);
    res.json(members);
  } catch (err) {
    if (err.message === "ACCESS_DENIED") return res.status(403).json({ error: "Not a member of this class" });
    res.status(500).json({ error: "Failed to load members" });
  }
});

// GET /api/classes/:id/messages?before=ISO&limit=50
router.get("/:id/messages", async (req, res) => {
  try {
    await validateClassAccess(req.params.id, req.user.id);
    const { before, limit } = req.query;
    const messages = await getClassMessages(
      req.params.id,
      before || null,
      Math.min(parseInt(limit) || 50, 100)
    );
    res.json(messages);
  } catch (err) {
    if (err.message === "ACCESS_DENIED") return res.status(403).json({ error: "Not a member of this class" });
    res.status(500).json({ error: "Failed to load messages" });
  }
});

// POST /api/classes/:id/read — mark class as read
router.post("/:id/read", async (req, res) => {
  try {
    await validateClassAccess(req.params.id, req.user.id);
    await markClassRead(req.params.id, req.user.id);
    res.json({ ok: true });
  } catch (err) {
    if (err.message === "ACCESS_DENIED") return res.status(403).json({ error: "Not a member of this class" });
    res.status(500).json({ error: "Failed to mark as read" });
  }
});

module.exports = router;
