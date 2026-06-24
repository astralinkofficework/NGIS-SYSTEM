const express = require("express");
const router = express.Router();
const { requireAuth } = require("../middleware/auth");
const {
  getUserConversations,
  findOrCreateConversation,
  getUserById,
} = require("../db/queries");

// GET /api/conversations — list all conversations for current user
router.get("/", requireAuth, async (req, res) => {
  try {
    const convs = await getUserConversations(req.user.id);
    res.json(convs);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/conversations — create or open a DM with another user
router.post("/", requireAuth, async (req, res) => {
  const { targetId } = req.body;
  if (!targetId) return res.status(400).json({ error: "targetId required" });

  try {
    const target = await getUserById(targetId);
    if (!target) return res.status(404).json({ error: "Target user not found" });

    const result = await findOrCreateConversation(
      req.user.id,
      targetId,
      req.user.role,
      target.role
    );

    res.status(result.isNew ? 201 : 200).json(result);
  } catch (err) {
    if (err.message === "PERMISSION_DENIED") {
      return res.status(403).json({ error: "You cannot message this user" });
    }
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
