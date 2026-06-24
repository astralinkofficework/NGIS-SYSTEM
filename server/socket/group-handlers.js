"use strict";

const {
  getUserClasses,
  validateClassAccess,
  sendGroupMessage,
  markClassRead,
} = require("../db/group-queries");

const supabase = require("../config/supabase");

// Track typing users per class: Map<classId, Map<userId, name>>
const typingUsers = new Map();

function registerGroupHandlers(io, socket) {
  const user = socket.user;

  // ── On connect: join all class rooms ──────────────────────
  getUserClasses(user.id)
    .then((classes) => {
      classes.forEach((c) => socket.join(`class:${c.id}`));
    })
    .catch(() => {});

  // ── Join a specific class room (called after page load) ───
  socket.on("join_class", async (classId) => {
    try {
      await validateClassAccess(classId, user.id);
      socket.join(`class:${classId}`);
    } catch {
      socket.emit("error", { message: "Access denied to this class" });
    }
  });

  // ── Send group message ─────────────────────────────────────
  socket.on("send_group_message", async (data, ack) => {
    const { classId, message } = data || {};
    if (!classId || !message?.trim()) {
      return ack?.({ error: "Invalid message" });
    }

    const text = message.trim().slice(0, 2000);

    try {
      await validateClassAccess(classId, user.id);
      const msg = await sendGroupMessage(classId, user.id, text);

      // Emit to everyone in the class room (including sender)
      io.to(`class:${classId}`).emit("new_group_message", msg);

      ack?.({ ok: true, message: msg });

      // Clear any typing indicator for this user
      clearTyping(io, classId, user.id, user.name);

      // Push in-app notification to members who are NOT in the room
      const room = io.sockets.adapter.rooms.get(`class:${classId}`);
      const socketsInRoom = room ? [...room] : [];
      const userIdsInRoom = socketsInRoom
        .map((sid) => io.sockets.sockets.get(sid)?.user?.id)
        .filter(Boolean);

      const { data: members } = await supabase
        .from("class_members")
        .select("user_id")
        .eq("class_id", classId)
        .neq("user_id", user.id);

      for (const m of members || []) {
        if (!userIdsInRoom.includes(m.user_id)) {
          io.to(`user:${m.user_id}`).emit("group_notification", {
            classId,
            senderName: user.name,
            senderRole: user.role,
            preview: text.slice(0, 80),
          });
        }
      }
    } catch (err) {
      ack?.({ error: err.message === "ACCESS_DENIED" ? "Not a member of this class" : "Failed to send" });
    }
  });

  // ── Mark class as read ─────────────────────────────────────
  socket.on("mark_class_read", async ({ classId }) => {
    if (!classId) return;
    try {
      await validateClassAccess(classId, user.id);
      await markClassRead(classId, user.id);
      // Let sender know their read was acknowledged (updates unread badge)
      socket.emit("class_read_ack", { classId });
    } catch {}
  });

  // ── Typing indicators ──────────────────────────────────────
  socket.on("typing_class_start", ({ classId }) => {
    if (!classId) return;
    if (!typingUsers.has(classId)) typingUsers.set(classId, new Map());
    typingUsers.get(classId).set(user.id, user.name);
    socket.to(`class:${classId}`).emit("class_typing", {
      classId,
      userId: user.id,
      name: user.name,
      role: user.role,
      isTyping: true,
    });
  });

  socket.on("typing_class_stop", ({ classId }) => {
    clearTyping(io, classId, user.id, user.name, socket);
  });

  // ── Disconnect: clear typing for all classes ───────────────
  socket.on("disconnect", () => {
    for (const [classId] of typingUsers) {
      clearTyping(io, classId, user.id, user.name, socket);
    }
  });
}

function clearTyping(io, classId, userId, userName, socket) {
  if (typingUsers.has(classId)) {
    typingUsers.get(classId).delete(userId);
    if (typingUsers.get(classId).size === 0) typingUsers.delete(classId);
  }
  const emitter = socket ? socket.to(`class:${classId}`) : io.to(`class:${classId}`);
  emitter.emit("class_typing", {
    classId,
    userId,
    name: userName,
    isTyping: false,
  });
}

module.exports = { registerGroupHandlers };
