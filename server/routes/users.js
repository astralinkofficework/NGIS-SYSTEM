const express = require("express");
const router = express.Router();
const { requireAuth } = require("../middleware/auth");
const { searchUsers, getUserById } = require("../db/queries");

// GET /api/users/search?q=name
router.get("/search", requireAuth, async (req, res) => {
  const q = (req.query.q || "").trim();
  if (q.length < 1) return res.json([]);

  try {
    const users = await searchUsers(q, req.user.role);
    // Remove the requesting user from results
    const filtered = users.filter((u) => u.id !== req.user.id);
    res.json(filtered);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/users/:id
router.get("/:id", requireAuth, async (req, res) => {
  try {
    const user = await getUserById(req.params.id);
    res.json(user);
  } catch {
    res.status(404).json({ error: "User not found" });
  }
});

// GET /api/users/me
router.get("/me", requireAuth, (req, res) => {
  res.json(req.user);
});

module.exports = router;
