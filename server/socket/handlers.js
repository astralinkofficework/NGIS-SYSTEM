const {
  sendMessage,
  markConversationRead,
  getUserConversations,
  updateUserStatus,
  createNotification,
} = require("../db/queries");

// Track online users: Map<userId, socketId>
const onlineUsers = new Map();

function registerHandlers(io, socket) {
  const user = socket.user;

  // ── Connect ─────────────────────────────────────────────────
  onlineUsers.set(user.id, socket.id);
  updateUserStatus(user.id, "online").catch(() => {});

  // Join personal room for targeted events
  socket.join(`user:${user.id}`);

  // Join all conversation rooms
  getUserConversations(user.id)
    .then((convs) => convs.forEach((c) => socket.join(`conv:${c.id}`)))
    .catch(() => {});

  // Broadcast online status to all connected users
  io.emit("user_status", { userId: user.id, status: "online" });

  // ── Send message ─────────────────────────────────────────────
  socket.on("send_message", async (data, ack) => {
    const { conversationId, message } = data || {};
    if (!conversationId || !message?.trim()) {
      return ack?.({ error: "Invalid message" });
    }

    const text = message.trim().slice(0, 2000);

    try {
      const msg = await sendMessage(conversationId, user.id, text);

      // Attach sender info for immediate render
      const fullMsg = { ...msg, sender: { id: user.id, name: user.name, avatar: user.avatar } };

      // Emit to everyone in the conversation room
      io.to(`conv:${conversationId}`).emit("new_message", fullMsg);

      ack?.({ ok: true, message: fullMsg });

      // Create a push notification for offline participants
      const room = io.sockets.adapter.rooms.get(`conv:${conversationId}`);
      const participantSockets = room ? [...room] : [];
      const onlineInRoom = participantSockets
        .map((sid) => io.sockets.sockets.get(sid)?.user?.id)
        .filter(Boolean);

      // Notify participants who are in the conversation but not viewing it
      // (we can't know if they have this conv open, so we notify all others)
      const { data: parts } = await require("../config/supabase")
        .from("participants")
        .select("user_id")
        .eq("conversation_id", conversationId)
        .neq("user_id", user.id);

      for (const p of parts || []) {
        await createNotification(
          p.user_id,
          `${user.name}: ${text.slice(0, 60)}${text.length > 60 ? "…" : ""}`,
          conversationId
        );
        // Push notification event to that user's personal room
        io.to(`user:${p.user_id}`).emit("notification", {
          conversationId,
          senderName: user.name,
          preview: text.slice(0, 80),
        });
      }
    } catch (err) {
      ack?.({ error: err.message });
    }
  });

  // ── Join a new conversation room (after creating a DM) ───────
  socket.on("join_conversation", (conversationId) => {
    socket.join(`conv:${conversationId}`);
  });

  // ── Mark conversation as read ────────────────────────────────
  socket.on("mark_read", async ({ conversationId }) => {
    if (!conversationId) return;
    try {
      await markConversationRead(conversationId, user.id);
      // Notify the other participant their messages were read
      socket.to(`conv:${conversationId}`).emit("messages_read", {
        conversationId,
        readBy: user.id,
      });
    } catch {}
  });

  // ── Typing indicators ────────────────────────────────────────
  socket.on("typing_start", ({ conversationId }) => {
    socket.to(`conv:${conversationId}`).emit("typing", {
      conversationId,
      userId: user.id,
      isTyping: true,
    });
  });

  socket.on("typing_stop", ({ conversationId }) => {
    socket.to(`conv:${conversationId}`).emit("typing", {
      conversationId,
      userId: user.id,
      isTyping: false,
    });
  });

  // ── Disconnect ───────────────────────────────────────────────
  socket.on("disconnect", () => {
    onlineUsers.delete(user.id);
    updateUserStatus(user.id, "offline").catch(() => {});
    io.emit("user_status", { userId: user.id, status: "offline" });
  });
}

module.exports = { registerHandlers, onlineUsers };
