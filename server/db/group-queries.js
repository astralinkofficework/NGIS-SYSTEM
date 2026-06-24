"use strict";

const supabase = require("../config/supabase");

// ── Get all classes a user belongs to ────────────────────────
async function getUserClasses(userId) {
  const { data: memberships, error } = await supabase
    .from("class_members")
    .select("class_id, role, classes(id, name, grade_level, section)")
    .eq("user_id", userId);

  if (error) throw error;

  // Enrich each class with last message + unread count
  const enriched = await Promise.all(
    memberships.map(async (m) => {
      const cls = m.classes;

      // Last message
      const { data: last } = await supabase
        .from("group_messages")
        .select("message, created_at, sender:users!sender_id(name)")
        .eq("class_id", cls.id)
        .order("created_at", { ascending: false })
        .limit(1)
        .maybeSingle();

      // Last read timestamp for this user
      const { data: readRow } = await supabase
        .from("class_reads")
        .select("last_read_at")
        .eq("class_id", cls.id)
        .eq("user_id", userId)
        .maybeSingle();

      // Unread = messages from others after last_read_at
      let unread = 0;
      if (readRow?.last_read_at) {
        const { count } = await supabase
          .from("group_messages")
          .select("id", { count: "exact", head: true })
          .eq("class_id", cls.id)
          .neq("sender_id", userId)
          .gt("created_at", readRow.last_read_at);
        unread = count || 0;
      } else {
        // Never read: count all messages not from this user
        const { count } = await supabase
          .from("group_messages")
          .select("id", { count: "exact", head: true })
          .eq("class_id", cls.id)
          .neq("sender_id", userId);
        unread = count || 0;
      }

      return {
        id: cls.id,
        name: cls.name,
        grade_level: cls.grade_level,
        section: cls.section,
        unread,
        last_message: last?.message || null,
        last_at: last?.created_at || null,
        last_sender: last?.sender?.name || null,
      };
    })
  );

  // Sort: classes with unread first, then by last_at
  return enriched.sort((a, b) => {
    if (b.unread !== a.unread) return b.unread - a.unread;
    return new Date(b.last_at || 0) - new Date(a.last_at || 0);
  });
}

// ── Get messages for a class (paginated, newest-first then reversed) ──
async function getClassMessages(classId, before = null, limit = 50) {
  let q = supabase
    .from("group_messages")
    .select(
      "id, message, created_at, sender:users!sender_id(id, name, role, avatar)"
    )
    .eq("class_id", classId)
    .order("created_at", { ascending: false })
    .limit(limit);

  if (before) q = q.lt("created_at", before);

  const { data, error } = await q;
  if (error) throw error;

  return data.reverse(); // Return in chronological order
}

// ── Verify the user is a member of the class ─────────────────
async function validateClassAccess(classId, userId) {
  const { data, error } = await supabase
    .from("class_members")
    .select("role")
    .eq("class_id", classId)
    .eq("user_id", userId)
    .maybeSingle();

  if (error || !data) throw new Error("ACCESS_DENIED");
  return data.role;
}

// ── Send a group message ──────────────────────────────────────
async function sendGroupMessage(classId, senderId, message) {
  const { data, error } = await supabase
    .from("group_messages")
    .insert({ class_id: classId, sender_id: senderId, message })
    .select(
      "id, message, created_at, sender:users!sender_id(id, name, role, avatar)"
    )
    .single();

  if (error) throw error;
  return data;
}

// ── Mark a class as read for a user ──────────────────────────
async function markClassRead(classId, userId) {
  const { error } = await supabase
    .from("class_reads")
    .upsert(
      { class_id: classId, user_id: userId, last_read_at: new Date().toISOString() },
      { onConflict: "class_id,user_id" }
    );

  if (error) throw error;
}

// ── Get members of a class ────────────────────────────────────
async function getClassMembers(classId) {
  const { data, error } = await supabase
    .from("class_members")
    .select("role, joined_at, users(id, name, role, avatar, status)")
    .eq("class_id", classId);

  if (error) throw error;
  return data;
}

module.exports = {
  getUserClasses,
  getClassMessages,
  validateClassAccess,
  sendGroupMessage,
  markClassRead,
  getClassMembers,
};
