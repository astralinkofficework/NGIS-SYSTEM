const express = require("express");
const router = express.Router();
const { requireAuth } = require("../middleware/auth");
const {
  getMessages,
  markConversationRead,
  getUserNotifications,
  markNotificationsRead,
} = require("../db/queries");

// GET /api/messages/:conversationId?before=<iso>&limit=50
router.get("/:conversationId", requireAuth, async (req, res) => {
  const { conversationId } = req.params;
  const limit = Math.min(parseInt(req.query.limit) || 50, 100);
  const before = req.query.before || null;

  try {
    const msgs = await getMessages(conversationId, req.user.id, limit, before);
    res.json(msgs);
  } catch (err) {
    if (err.message === "NOT_PARTICIPANT") {
      return res.status(403).json({ error: "Access denied" });
    }
    res.status(500).json({ error: err.message });
  }
});

// POST /api/messages/:conversationId/read — mark all as read
router.post("/:conversationId/read", requireAuth, async (req, res) => {
  try {
    await markConversationRead(req.params.conversationId, req.user.id);
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/notifications
router.get("/notifications", requireAuth, async (req, res) => {
  try {
    const notifs = await getUserNotifications(req.user.id);
    res.json(notifs);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/notifications/read
router.post("/notifications/read", requireAuth, async (req, res) => {
  try {
    await markNotificationsRead(req.user.id);
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
