const supabase = require("../config/supabase");

// ── Permission matrix ─────────────────────────────────────────
// Returns which roles the given role can start a conversation with.
const ALLOWED_TARGETS = {
  super_admin: ["super_admin","admin","teacher","student","parent"],
  admin:       ["super_admin","admin","teacher","student","parent"],
  teacher:     ["admin","teacher","student","parent"],
  student:     ["teacher"],        // student can only DM teachers
  parent:      ["admin","teacher"],
};

function canMessage(senderRole, targetRole) {
  return (ALLOWED_TARGETS[senderRole] || []).includes(targetRole);
}

// ── Users ─────────────────────────────────────────────────────
async function searchUsers(query, requestingRole) {
  const allowed = ALLOWED_TARGETS[requestingRole] || [];
  const { data, error } = await supabase
    .from("users")
    .select("id,name,email,role,avatar,status")
    .in("role", allowed)
    .ilike("name", `%${query}%`)
    .limit(20);

  if (error) throw error;
  return data;
}

async function getUserById(userId) {
  const { data, error } = await supabase
    .from("users")
    .select("id,name,email,role,avatar,status,last_seen")
    .eq("id", userId)
    .single();

  if (error) throw error;
  return data;
}

async function updateUserStatus(userId, status) {
  const { error } = await supabase
    .from("users")
    .update({ status, last_seen: new Date().toISOString() })
    .eq("id", userId);

  if (error) throw error;
}

// ── Conversations ─────────────────────────────────────────────
async function getUserConversations(userId) {
  // Get all conversations this user participates in,
  // with the last message and the other participant's info.
  const { data, error } = await supabase
    .from("participants")
    .select(`
      conversation_id,
      last_read_at,
      conversations ( id, type, created_at ),
      users!participants_user_id_fkey ( id, name, role, avatar, status )
    `)
    .eq("user_id", userId);

  if (error) throw error;

  // For each conversation, get other participant + last message
  const enriched = await Promise.all(
    data.map(async (row) => {
      const convId = row.conversation_id;

      // Other participants
      const { data: others } = await supabase
        .from("participants")
        .select("users!participants_user_id_fkey(id,name,role,avatar,status)")
        .eq("conversation_id", convId)
        .neq("user_id", userId);

      // Last message
      const { data: lastMsg } = await supabase
        .from("messages")
        .select("id,message,sender_id,created_at")
        .eq("conversation_id", convId)
        .order("created_at", { ascending: false })
        .limit(1)
        .single();

      // Unread count (messages after last_read_at, not sent by me)
      let unread = 0;
      if (row.last_read_at) {
        const { count } = await supabase
          .from("messages")
          .select("*", { count: "exact", head: true })
          .eq("conversation_id", convId)
          .neq("sender_id", userId)
          .gt("created_at", row.last_read_at);
        unread = count || 0;
      } else {
        const { count } = await supabase
          .from("messages")
          .select("*", { count: "exact", head: true })
          .eq("conversation_id", convId)
          .neq("sender_id", userId);
        unread = count || 0;
      }

      const otherUser = others?.[0]?.users || null;
      return {
        id: convId,
        type: row.conversations?.type,
        otherUser,
        lastMessage: lastMsg || null,
        unread,
        lastReadAt: row.last_read_at,
      };
    })
  );

  // Sort by last message timestamp descending
  return enriched.sort((a, b) => {
    const ta = a.lastMessage?.created_at || a.conversations?.created_at || 0;
    const tb = b.lastMessage?.created_at || b.conversations?.created_at || 0;
    return new Date(tb) - new Date(ta);
  });
}

async function findOrCreateConversation(userId, targetId, senderRole, targetRole) {
  if (!canMessage(senderRole, targetRole)) {
    throw new Error("PERMISSION_DENIED");
  }

  // Check if a direct conversation already exists between these two users
  const { data: existing } = await supabase
    .from("participants")
    .select("conversation_id")
    .eq("user_id", userId);

  if (existing?.length) {
    const myConvIds = existing.map((r) => r.conversation_id);
    const { data: shared } = await supabase
      .from("participants")
      .select("conversation_id")
      .eq("user_id", targetId)
      .in("conversation_id", myConvIds);

    if (shared?.length) {
      return { id: shared[0].conversation_id, isNew: false };
    }
  }

  // Create new conversation
  const { data: conv, error: convErr } = await supabase
    .from("conversations")
    .insert({ type: "direct" })
    .select()
    .single();

  if (convErr) throw convErr;

  const { error: partErr } = await supabase.from("participants").insert([
    { conversation_id: conv.id, user_id: userId },
    { conversation_id: conv.id, user_id: targetId },
  ]);

  if (partErr) throw partErr;

  return { id: conv.id, isNew: true };
}

// ── Messages ──────────────────────────────────────────────────
async function getMessages(conversationId, userId, limit = 50, before = null) {
  // Verify user is participant
  const { data: part } = await supabase
    .from("participants")
    .select("conversation_id")
    .eq("conversation_id", conversationId)
    .eq("user_id", userId)
    .single();

  if (!part) throw new Error("NOT_PARTICIPANT");

  let q = supabase
    .from("messages")
    .select("id,conversation_id,sender_id,message,created_at")
    .eq("conversation_id", conversationId)
    .order("created_at", { ascending: false })
    .limit(limit);

  if (before) q = q.lt("created_at", before);

  const { data, error } = await q;
  if (error) throw error;

  return (data || []).reverse();
}

async function sendMessage(conversationId, senderId, message) {
  const { data, error } = await supabase
    .from("messages")
    .insert({ conversation_id: conversationId, sender_id: senderId, message })
    .select("id,conversation_id,sender_id,message,created_at")
    .single();

  if (error) throw error;

  // Create message_status rows for all other participants
  const { data: parts } = await supabase
    .from("participants")
    .select("user_id")
    .eq("conversation_id", conversationId)
    .neq("user_id", senderId);

  if (parts?.length) {
    await supabase.from("message_status").insert(
      parts.map((p) => ({ message_id: data.id, user_id: p.user_id }))
    );
  }

  return data;
}

async function markConversationRead(conversationId, userId) {
  const now = new Date().toISOString();

  // Update last_read_at in participants
  await supabase
    .from("participants")
    .update({ last_read_at: now })
    .eq("conversation_id", conversationId)
    .eq("user_id", userId);

  // Mark all message_status rows as read
  const { data: msgs } = await supabase
    .from("messages")
    .select("id")
    .eq("conversation_id", conversationId)
    .neq("sender_id", userId);

  if (msgs?.length) {
    const ids = msgs.map((m) => m.id);
    await supabase
      .from("message_status")
      .update({ read_at: now })
      .in("message_id", ids)
      .eq("user_id", userId)
      .is("read_at", null);
  }
}

async function getReadStatus(messageId) {
  const { data } = await supabase
    .from("message_status")
    .select("user_id,read_at")
    .eq("message_id", messageId);
  return data || [];
}

// ── Notifications ─────────────────────────────────────────────
async function createNotification(userId, message, conversationId) {
  await supabase.from("notifications").insert({
    user_id: userId,
    message,
    conversation_id: conversationId,
  });
}

async function getUserNotifications(userId) {
  const { data } = await supabase
    .from("notifications")
    .select("*")
    .eq("user_id", userId)
    .order("created_at", { ascending: false })
    .limit(50);
  return data || [];
}

async function markNotificationsRead(userId) {
  await supabase
    .from("notifications")
    .update({ read: true })
    .eq("user_id", userId)
    .eq("read", false);
}

module.exports = {
  canMessage,
  searchUsers,
  getUserById,
  updateUserStatus,
  getUserConversations,
  findOrCreateConversation,
  getMessages,
  sendMessage,
  markConversationRead,
  getReadStatus,
  createNotification,
  getUserNotifications,
  markNotificationsRead,
};
