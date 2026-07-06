/* ============================================================
   NGIS Chat Client — assets/js/chat.js
   Connects to the Socket.io chat server.
   Falls back to DEMO MODE if no server is reachable.
   ============================================================ */
(function () {
  "use strict";

  /* ── Config ───────────────────────────────────────────────── */
  const SERVER_URL = window.CHAT_SERVER || "http://localhost:3001";
  const TOKEN_KEY  = "ngis_chat_token";
  const USER_KEY   = "ngis_chat_user";

  /* ── Demo data ────────────────────────────────────────────── */
  const DEMO_USER = {
    id: "demo-me",
    name: "Kosal Rith Mony",
    role: "student",
    avatar: null,
    status: "online",
  };

  const DEMO_CONVS = [
    {
      id: "conv-1",
      otherUser: { id: "u-2", name: "Dr. Sarah Jenkins", role: "teacher", avatar: null, status: "online" },
      lastMessage: { message: "Please submit your assignment by Friday.", created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(), sender_id: "u-2" },
      unread: 2,
    },
    {
      id: "conv-2",
      otherUser: { id: "u-3", name: "Mr. David Chen", role: "teacher", avatar: null, status: "away" },
      lastMessage: { message: "Great work on the midterm!", created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), sender_id: "u-3" },
      unread: 0,
    },
    {
      id: "conv-3",
      otherUser: { id: "u-4", name: "School Support", role: "admin", avatar: null, status: "offline" },
      lastMessage: { message: "Your request has been processed.", created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), sender_id: "u-4" },
      unread: 0,
    },
  ];

  const DEMO_MESSAGES = {
    "conv-1": [
      { id: "m-1", conversation_id: "conv-1", sender_id: "u-2", message: "Good morning! How are you doing?", created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), sender: { id: "u-2", name: "Dr. Sarah Jenkins" } },
      { id: "m-2", conversation_id: "conv-1", sender_id: "demo-me", message: "Good morning! I am doing well, thank you.", created_at: new Date(Date.now() - 1000 * 60 * 25).toISOString(), sender: { id: "demo-me", name: "Kosal Rith Mony" } },
      { id: "m-3", conversation_id: "conv-1", sender_id: "u-2", message: "Please submit your assignment by Friday.", created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(), sender: { id: "u-2", name: "Dr. Sarah Jenkins" } },
    ],
    "conv-2": [
      { id: "m-4", conversation_id: "conv-2", sender_id: "demo-me", message: "Sir, can I get feedback on my essay?", created_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(), sender: { id: "demo-me", name: "Kosal Rith Mony" } },
      { id: "m-5", conversation_id: "conv-2", sender_id: "u-3", message: "Great work on the midterm!", created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(), sender: { id: "u-3", name: "Mr. David Chen" } },
    ],
    "conv-3": [
      { id: "m-6", conversation_id: "conv-3", sender_id: "u-4", message: "Your request has been processed.", created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), sender: { id: "u-4", name: "School Support" } },
    ],
  };

  const DEMO_SEARCH = [
    { id: "u-2", name: "Dr. Sarah Jenkins", role: "teacher", avatar: null, status: "online" },
    { id: "u-3", name: "Mr. David Chen",    role: "teacher", avatar: null, status: "away" },
    { id: "u-4", name: "School Support",    role: "admin",   avatar: null, status: "offline" },
    { id: "u-5", name: "Ms. Linda Ouk",     role: "teacher", avatar: null, status: "online" },
  ];

  /* ── Emoji set ────────────────────────────────────────────── */
  const EMOJIS = [
    "😀","😊","😂","🤣","😍","🥰","😎","🤗","😢",
    "😭","😡","🤔","🙄","😮","🤯","😴","👍","👎",
    "👏","🙏","❤️","🔥","✅","❌","⭐","🎉","💯",
    "📚","📖","✏️","📝","📅","⏰","📊","💪","👨‍🏫",
    "👩‍🏫","👨‍🎓","👩‍🎓","🏫","📌","📎","🖊️","📋","🗓️",
  ];

  /* ── State ────────────────────────────────────────────────── */
  let socket        = null;
  let currentUser   = null;
  let conversations = [];
  let activeConvId  = null;
  let messages      = {};
  let typingTimers  = {};
  let isDemo        = false;
  let msgIdCounter  = 100;

  /* ── Helpers ─────────────────────────────────────────────── */
  function initials(name = "") {
    return name.split(" ").slice(0, 2).map((w) => w[0]).join("").toUpperCase();
  }

  function fmtTime(iso) {
    const d = new Date(iso);
    const now = new Date();
    const diff = (now - d) / 1000;
    if (diff < 60)           return "just now";
    if (diff < 3600)         return Math.floor(diff / 60) + "m ago";
    if (diff < 86400)        return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    if (diff < 86400 * 7)   return d.toLocaleDateString([], { weekday: "short" });
    return d.toLocaleDateString([], { month: "short", day: "numeric" });
  }

  function fmtMsgTime(iso) {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function fmtDateSep(iso) {
    const d = new Date(iso);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    if (d.toDateString() === today.toDateString()) return "Today";
    if (d.toDateString() === yesterday.toDateString()) return "Yesterday";
    return d.toLocaleDateString([], { weekday: "long", month: "long", day: "numeric" });
  }

  function escHtml(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  function avatarHtml(user, size = 46, cls = "") {
    if (user.avatar) {
      return `<img src="${escHtml(user.avatar)}" alt="${escHtml(user.name)}" class="${cls}" style="width:${size}px;height:${size}px;border-radius:50%;object-fit:cover;">`;
    }
    return `<div class="${cls}" style="width:${size}px;height:${size}px;border-radius:50%;background:var(--primary);color:#fff;display:grid;place-items:center;font-size:${Math.round(size * 0.34)}px;font-weight:700;flex-shrink:0;">${escHtml(initials(user.name))}</div>`;
  }

  function roleBadge(role) {
    const cls = { teacher: "role-teacher", student: "role-student", parent: "role-parent", admin: "role-admin", super_admin: "role-admin" };
    return `<span class="ur-role-badge ${cls[role] || ''}">${role.replace("_", " ")}</span>`;
  }

  /* ── DOM refs ─────────────────────────────────────────────── */
  const $ = (id) => document.getElementById(id);
  const convList    = $("convList");
  const convSearch  = $("peopleSearch");
  const chatWin     = $("chatWin");
  const chatEmpty   = $("chatSelectState");
  const chatActive  = $("chatActive");
  const chatHName   = $("chatHName");
  const chatHStatus = $("chatHStatus");
  const chatHAvaCont= $("chatHAvaCont");
  const msgArea     = $("msgArea");
  const msgInput    = $("msgInput");
  const msgForm     = $("msgForm");
  const sendBtn     = $("sendBtn");
  const emojiBtn    = $("emojiBtn");
  const emojiPicker = $("emojiPicker");
  const emojiGrid   = $("emojiGrid");
  const newChatBtn  = $("newChatBtn");
  const startChatBtn= $("startChatBtn");
  const newChatModal= $("newChatModal");
  const closeModal  = $("closeModal");
  const userSearch  = $("userSearch");
  const userResults = $("userResults");
  const backBtn     = $("backBtn");
  const typingRow   = $("typingRow");
  const demoBanner  = $("demoBanner");

  /* ── Build emoji grid ─────────────────────────────────────── */
  function buildEmojiGrid() {
    emojiGrid.innerHTML = EMOJIS.map(
      (e) => `<button type="button" class="e-btn" data-emoji="${e}">${e}</button>`
    ).join("");

    emojiGrid.addEventListener("click", (ev) => {
      const btn = ev.target.closest(".e-btn");
      if (!btn) return;
      const cursor = msgInput.selectionStart;
      const val = msgInput.value;
      msgInput.value = val.slice(0, cursor) + btn.dataset.emoji + val.slice(cursor);
      msgInput.focus();
      const newPos = cursor + btn.dataset.emoji.length;
      msgInput.setSelectionRange(newPos, newPos);
      emojiPicker.hidden = true;
      updateSendBtn();
    });
  }

  /* ── Conversations list ───────────────────────────────────── */
  function renderConvList(filter = "") {
    const f = filter.toLowerCase().trim();
    const filtered = f
      ? conversations.filter((c) => c.otherUser?.name.toLowerCase().includes(f))
      : conversations;

    if (!filtered.length) {
      convList.innerHTML = `
        <div class="conv-empty-state">
          <span class="material-symbols-outlined">chat_bubble_outline</span>
          <p>${f ? "No results for "" + escHtml(f) + """ : "No conversations yet.<br>Start one below."}</p>
        </div>`;
      return;
    }

    convList.innerHTML = filtered.map((c) => {
      const u = c.otherUser;
      const isActive = c.id === activeConvId;
      const preview = c.lastMessage?.message || "";
      const hasUnread = c.unread > 0;

      return `
        <div class="conv-item ${isActive ? "active" : ""}" data-id="${c.id}" role="button" tabindex="0" aria-label="Chat with ${escHtml(u?.name || "")}">
          <div class="ava-wrap">
            ${avatarHtml(u || { name: "?" }, 46, "conv-ava-init")}
            <span class="s-dot ${u?.status || "offline"}"></span>
          </div>
          <div class="conv-info">
            <div class="conv-top">
              <span class="conv-name">${escHtml(u?.name || "Unknown")}</span>
              <span class="conv-time">${c.lastMessage ? fmtTime(c.lastMessage.created_at) : ""}</span>
            </div>
            <span class="conv-preview ${hasUnread ? "unread" : ""}">${escHtml(preview.slice(0, 60))}</span>
          </div>
          ${hasUnread ? `<span class="conv-badge">${c.unread > 99 ? "99+" : c.unread}</span>` : ""}
        </div>`;
    }).join("");
  }

  /* ── Open a conversation ──────────────────────────────────── */
  function openConversation(convId) {
    activeConvId = convId;
    const conv = conversations.find((c) => c.id === convId);
    if (!conv) return;

    const u = conv.otherUser;

    // Update header
    chatHAvaCont.innerHTML = `
      <div class="ava-wrap">
        ${avatarHtml(u, 40, "hava-init")}
        <span class="s-dot ${u?.status || "offline"}"></span>
      </div>`;
    chatHName.textContent = u?.name || "Unknown";
    chatHStatus.textContent = capitalize(u?.status || "offline");
    chatHStatus.className = "chat-hstatus" + (u?.status === "online" ? " is-online" : "");

    // Show chat window
    if (chatEmpty) chatEmpty.style.display = 'none';
    chatActive.style.display = 'flex';

    // Mobile transition
    chatWin.classList.add("show-mobile");
    document.querySelector(".conv-panel")?.classList.add("hidden-mobile");

    // Load messages
    loadMessages(convId);

    // Mark as read
    conv.unread = 0;
    renderConvList(convSearch.value);
    markRead(convId);
  }

  function capitalize(s) { return s ? s[0].toUpperCase() + s.slice(1) : s; }

  /* ── Load messages ────────────────────────────────────────── */
  async function loadMessages(convId) {
    msgArea.innerHTML = `<div class="chat-loading"><div class="spinner"></div> Loading messages…</div>`;

    let msgs;
    if (isDemo) {
      msgs = (DEMO_MESSAGES[convId] || []).slice();
    } else {
      try {
        const token = localStorage.getItem(TOKEN_KEY);
        const res = await fetch(`${SERVER_URL}/api/messages/${convId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        msgs = await res.json();
      } catch {
        msgs = [];
      }
    }

    messages[convId] = msgs;
    renderMessages(convId);
    scrollToBottom();
  }

  /* ── Render messages ─────────────────────────────────────── */
  function renderMessages(convId) {
    const msgs = messages[convId] || [];
    if (!msgs.length) {
      msgArea.innerHTML = `
        <div class="conv-empty-state" style="flex:1;justify-content:center;">
          <span class="material-symbols-outlined">chat</span>
          <p>No messages yet. Say hello!</p>
        </div>`;
      return;
    }

    let html = "";
    let lastDate = "";
    let lastSender = null;
    let groupCount = 0;

    msgs.forEach((msg, i) => {
      const isOut = msg.sender_id === currentUser.id;
      const dateStr = fmtDateSep(msg.created_at);
      const sender = msg.sender || { id: msg.sender_id, name: "User" };
      const isNewSender = sender.id !== lastSender;
      const nextMsg = msgs[i + 1];
      const isLastInGroup = !nextMsg || nextMsg.sender_id !== msg.sender_id;

      if (dateStr !== lastDate) {
        html += `<div class="msg-date-sep">${escHtml(dateStr)}</div>`;
        lastDate = dateStr;
        lastSender = null;
        groupCount = 0;
      }

      if (isNewSender) groupCount = 0;
      groupCount++;

      const bubbleCls = groupCount === 1 ? "" : isLastInGroup ? "grp-last" : "grp-mid";

      const avaHtml = isOut ? "" : (
        isLastInGroup
          ? avatarHtml(sender, 28, "msg-sender-init")
          : `<div class="msg-ava-spacer"></div>`
      );

      html += `
        <div class="msg-row ${isOut ? "out" : ""}" data-msg-id="${msg.id}">
          ${isOut ? "" : avaHtml}
          <div class="msg-group">
            <div class="msg-bubble ${bubbleCls}">${escHtml(msg.message)}</div>
            ${isLastInGroup ? `
              <div class="msg-meta">
                <span class="msg-time">${fmtMsgTime(msg.created_at)}</span>
                ${isOut ? `<span class="msg-tick" id="tick-${msg.id}"><span class="material-symbols-outlined">done_all</span></span>` : ""}
              </div>` : ""}
          </div>
        </div>`;

      lastSender = sender.id;
    });

    msgArea.innerHTML = html;
  }

  function scrollToBottom(smooth = false) {
    msgArea.scrollTo({ top: msgArea.scrollHeight, behavior: smooth ? "smooth" : "instant" });
  }

  /* ── Append a single new message ─────────────────────────── */
  function appendMessage(msg) {
    const isOut = msg.sender_id === currentUser.id;
    const sender = msg.sender || { id: msg.sender_id, name: "?" };

    const row = document.createElement("div");
    row.className = `msg-row ${isOut ? "out" : ""}`;
    row.dataset.msgId = msg.id;

    const ava = isOut ? "" : avatarHtml(sender, 28, "msg-sender-init");

    row.innerHTML = `
      ${isOut ? "" : ava}
      <div class="msg-group">
        <div class="msg-bubble">${escHtml(msg.message)}</div>
        <div class="msg-meta">
          <span class="msg-time">${fmtMsgTime(msg.created_at)}</span>
          ${isOut ? `<span class="msg-tick" id="tick-${msg.id}"><span class="material-symbols-outlined">done_all</span></span>` : ""}
        </div>
      </div>`;

    // Remove empty state if present
    const empty = msgArea.querySelector(".conv-empty-state");
    if (empty) empty.remove();

    msgArea.appendChild(row);

    // Store it
    if (!messages[msg.conversation_id]) messages[msg.conversation_id] = [];
    messages[msg.conversation_id].push(msg);

    scrollToBottom(true);
  }

  /* ── Send a message ───────────────────────────────────────── */
  function sendMessage() {
    const text = msgInput.value.trim();
    if (!text || !activeConvId) return;

    msgInput.value = "";
    updateSendBtn();
    stopTyping();

    if (isDemo) {
      const msg = {
        id: `demo-${++msgIdCounter}`,
        conversation_id: activeConvId,
        sender_id: currentUser.id,
        sender: { id: currentUser.id, name: currentUser.name },
        message: text,
        created_at: new Date().toISOString(),
      };
      appendMessage(msg);

      // Update conv preview
      const conv = conversations.find((c) => c.id === activeConvId);
      if (conv) { conv.lastMessage = msg; renderConvList(convSearch.value); }
      return;
    }

    socket.emit("send_message", { conversationId: activeConvId, message: text }, (res) => {
      if (res?.error) showToast(res.error, "error");
    });
  }

  /* ── Typing ───────────────────────────────────────────────── */
  let typingTimeout = null;

  function startTyping() {
    if (!socket || !activeConvId || isDemo) return;
    socket.emit("typing_start", { conversationId: activeConvId });
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(stopTyping, 3000);
  }

  function stopTyping() {
    clearTimeout(typingTimeout);
    if (!socket || !activeConvId || isDemo) return;
    socket.emit("typing_stop", { conversationId: activeConvId });
  }

  /* ── Mark read ────────────────────────────────────────────── */
  function markRead(convId) {
    if (isDemo) return;
    if (socket) socket.emit("mark_read", { conversationId: convId });
    const token = localStorage.getItem(TOKEN_KEY);
    fetch(`${SERVER_URL}/api/messages/${convId}/read`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    }).catch(() => {});
  }

  /* ── User search (modal) ──────────────────────────────────── */
  let searchDebounce = null;

  async function searchUsers(q) {
    if (!q.trim()) {
      userResults.innerHTML = `<p class="search-placeholder">Search for a teacher, admin, or support to start a conversation.</p>`;
      return;
    }

    userResults.innerHTML = `<div class="chat-loading"><div class="spinner"></div></div>`;

    let results;
    if (isDemo) {
      results = DEMO_SEARCH.filter((u) => u.name.toLowerCase().includes(q.toLowerCase()));
    } else {
      try {
        const token = localStorage.getItem(TOKEN_KEY);
        const res = await fetch(`${SERVER_URL}/api/users/search?q=${encodeURIComponent(q)}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        results = await res.json();
      } catch {
        results = [];
      }
    }

    if (!results.length) {
      userResults.innerHTML = `<p class="search-placeholder">No users found matching "${escHtml(q)}".</p>`;
      return;
    }

    userResults.innerHTML = results.map((u) => `
      <div class="user-result-item" data-uid="${u.id}" data-uname="${escHtml(u.name)}" data-urole="${u.role}" tabindex="0" role="button">
        <div class="ur-ava-init">${escHtml(initials(u.name))}</div>
        <div class="ur-info">
          <div class="ur-name">${escHtml(u.name)}</div>
          <div class="ur-role">${capitalize(u.role.replace("_", " "))}</div>
        </div>
        ${roleBadge(u.role)}
      </div>`
    ).join("");
  }

  /* ── Start a new conversation ─────────────────────────────── */
  async function startConversation(targetId, targetName, targetRole) {
    closeModalFn();

    if (isDemo) {
      // Find existing or create demo conv
      let conv = conversations.find((c) => c.otherUser?.id === targetId);
      if (!conv) {
        conv = {
          id: `conv-demo-${targetId}`,
          otherUser: { id: targetId, name: targetName, role: targetRole, avatar: null, status: "offline" },
          lastMessage: null,
          unread: 0,
        };
        conversations.unshift(conv);
        DEMO_MESSAGES[conv.id] = [];
      }
      renderConvList();
      openConversation(conv.id);
      return;
    }

    try {
      const token = localStorage.getItem(TOKEN_KEY);
      const res = await fetch(`${SERVER_URL}/api/conversations`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ targetId }),
      });

      const data = await res.json();
      if (!res.ok) { showToast(data.error || "Cannot start conversation", "error"); return; }

      // Reload conversations then open
      await loadConversations();
      openConversation(data.id);

      if (socket) socket.emit("join_conversation", data.id);
    } catch {
      showToast("Connection error", "error");
    }
  }

  /* ── Load conversations from server ──────────────────────── */
  async function loadConversations() {
    if (isDemo) {
      conversations = [...DEMO_CONVS];
      renderConvList();
      return;
    }

    try {
      const token = localStorage.getItem(TOKEN_KEY);
      const res = await fetch(`${SERVER_URL}/api/conversations`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      conversations = await res.json();
      renderConvList();
    } catch {
      conversations = [];
      renderConvList();
    }
  }

  /* ── Update user online status dots ──────────────────────── */
  function updateStatusDots(userId, status) {
    // Update in conversations list
    conversations.forEach((c) => {
      if (c.otherUser?.id === userId) {
        c.otherUser.status = status;
      }
    });

    // Update active chat header
    if (activeConvId) {
      const conv = conversations.find((c) => c.id === activeConvId);
      if (conv?.otherUser?.id === userId) {
        const dot = chatHAvaCont.querySelector(".s-dot");
        if (dot) dot.className = `s-dot ${status}`;
        chatHStatus.textContent = capitalize(status);
        chatHStatus.className = "chat-hstatus" + (status === "online" ? " is-online" : "");
      }
    }

    renderConvList(convSearch.value);
  }

  /* ── Toast notifications ──────────────────────────────────── */
  function showToast(msg, type = "info") {
    // Use layout.js toast if available
    if (window.ngisToast) { window.ngisToast(msg, type); return; }
    const t = document.createElement("div");
    t.style.cssText = `position:fixed;bottom:80px;left:50%;transform:translateX(-50%);
      background:var(--surface);border:1px solid var(--border);border-radius:10px;
      padding:10px 18px;font-size:13px;font-weight:600;box-shadow:var(--sh-3);
      z-index:999;color:var(--text);animation:ep-in .2s ease;`;
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }

  /* ── Auto-resize textarea ─────────────────────────────────── */
  function autoResize() {
    msgInput.style.height = "auto";
    msgInput.style.height = Math.min(msgInput.scrollHeight, 130) + "px";
  }

  function updateSendBtn() {
    sendBtn.disabled = !msgInput.value.trim();
  }

  /* ── Modal helpers ────────────────────────────────────────── */
  function openModalFn() {
    newChatModal.hidden = false;
    userSearch.value = "";
    userResults.innerHTML = `<p class="search-placeholder">Search for a teacher, admin, or support to start a conversation.</p>`;
    userSearch.focus();
  }

  function closeModalFn() {
    newChatModal.hidden = true;
  }

  /* ── Connect to Socket.io ─────────────────────────────────── */
  function connectSocket(token) {
    if (typeof io === "undefined") { enableDemoMode(); return; }

    socket = io(SERVER_URL, {
      auth: { token },
      timeout: 5000,
      reconnectionAttempts: 3,
    });

    socket.on("connect", () => {
      console.log("[chat] socket connected");
    });

    socket.on("connect_error", (err) => {
      console.warn("[chat] socket error:", err.message);
      if (!isDemo) enableDemoMode();
    });

    socket.on("new_message", (msg) => {
      // If this conversation is active, append message
      if (msg.conversation_id === activeConvId) {
        appendMessage(msg);
        markRead(msg.conversation_id);
      } else {
        // Update unread count and preview
        const conv = conversations.find((c) => c.id === msg.conversation_id);
        if (conv) {
          conv.unread = (conv.unread || 0) + 1;
          conv.lastMessage = msg;
          renderConvList(convSearch.value);
        }
        // Show browser notification
        showBrowserNotif(msg);
      }
    });

    socket.on("messages_read", ({ conversationId, readBy }) => {
      if (conversationId === activeConvId && readBy !== currentUser.id) {
        // Mark ticks as read (blue)
        const ticks = msgArea.querySelectorAll(".msg-tick");
        ticks.forEach((t) => t.classList.add("read"));
      }
    });

    socket.on("user_status", ({ userId, status }) => {
      updateStatusDots(userId, status);
    });

    socket.on("typing", ({ conversationId, userId, isTyping }) => {
      if (conversationId !== activeConvId || userId === currentUser.id) return;
      typingRow.classList.toggle("show", isTyping);
      clearTimeout(typingTimers[userId]);
      if (isTyping) {
        typingTimers[userId] = setTimeout(() => typingRow.classList.remove("show"), 4000);
      }
    });

    socket.on("notification", ({ conversationId, senderName, preview }) => {
      showToast(`${senderName}: ${preview}`);
    });
  }

  /* ── Browser push notifications ──────────────────────────── */
  function requestNotifPermission() {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }
  }

  function showBrowserNotif(msg) {
    if (!("Notification" in window) || Notification.permission !== "granted") return;
    const sender = msg.sender?.name || "Someone";
    new Notification(`${sender} — NGIS Chat`, {
      body: msg.message.slice(0, 80),
      icon: "assets/icons/icon-192.png",
    });
  }

  /* ── Demo mode ────────────────────────────────────────────── */
  function enableDemoMode() {
    if (isDemo) return;
    isDemo = true;
    if (demoBanner) demoBanner.hidden = false;
    console.info("[chat] running in demo mode — no server connected");
    loadConversations();
  }

  /* ── Init ─────────────────────────────────────────────────── */
  function init() {
    buildEmojiGrid();

    // Resolve current user
    currentUser =
      window.CURRENT_USER ||
      JSON.parse(localStorage.getItem(USER_KEY) || "null") ||
      DEMO_USER;

    const token = localStorage.getItem(TOKEN_KEY);

    // Try to connect to server; fall back to demo if needed
    if (token && typeof io !== "undefined") {
      connectSocket(token);
    } else {
      enableDemoMode();
    }

    loadConversations();
    requestNotifPermission();

    /* ── Event listeners ──────────────────────────────────── */

    // Conversation list click
    convList.addEventListener("click", (ev) => {
      const item = ev.target.closest(".conv-item");
      if (!item) return;
      openConversation(item.dataset.id);
    });

    convList.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") {
        const item = ev.target.closest(".conv-item");
        if (item) openConversation(item.dataset.id);
      }
    });

    // Conversation search
    if (convSearch) convSearch.addEventListener("input", () => renderConvList(convSearch.value));

    // Send form
    msgForm.addEventListener("submit", (ev) => {
      ev.preventDefault();
      sendMessage();
    });

    // Textarea: auto-resize + typing indicator
    msgInput.addEventListener("input", () => {
      autoResize();
      updateSendBtn();
      startTyping();
    });

    msgInput.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter" && !ev.shiftKey) {
        ev.preventDefault();
        sendMessage();
      }
    });

    msgInput.addEventListener("blur", stopTyping);

    // Emoji toggle
    emojiBtn.addEventListener("click", (ev) => {
      ev.stopPropagation();
      emojiPicker.hidden = !emojiPicker.hidden;
    });

    document.addEventListener("click", (ev) => {
      if (!emojiPicker.contains(ev.target) && ev.target !== emojiBtn) {
        emojiPicker.hidden = true;
      }
    });

    // New chat modal
    [newChatBtn, startChatBtn].forEach((btn) => {
      if (btn) btn.addEventListener("click", openModalFn);
    });

    if (closeModal) closeModal.addEventListener("click", closeModalFn);

    if (newChatModal) newChatModal.addEventListener("click", (ev) => {
      if (ev.target === newChatModal) closeModalFn();
    });

    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape") {
        closeModalFn();
        emojiPicker.hidden = true;
      }
    });

    // User search in modal
    if (userSearch) userSearch.addEventListener("input", () => {
      clearTimeout(searchDebounce);
      searchDebounce = setTimeout(() => searchUsers(userSearch.value), 280);
    });

    // Start chat from user result
    if (userResults) userResults.addEventListener("click", (ev) => {
      const item = ev.target.closest(".user-result-item");
      if (!item) return;
      startConversation(item.dataset.uid, item.dataset.uname, item.dataset.urole);
    });

    if (userResults) userResults.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") {
        const item = ev.target.closest(".user-result-item");
        if (item) startConversation(item.dataset.uid, item.dataset.uname, item.dataset.urole);
      }
    });

    // Back button (mobile)
    if (backBtn) backBtn.addEventListener("click", () => {
      chatWin.classList.remove("show-mobile");
      document.querySelector(".conv-panel")?.classList.remove("hidden-mobile");
      document.body.classList.remove("chat-open");
      activeConvId = null;
      chatActive.style.display = 'none';
      if (chatEmpty) chatEmpty.style.display = '';
    });

    // Initial send button state
    updateSendBtn();
  }

  // Wait for DOM
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
