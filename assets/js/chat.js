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
    id: "student-me",
    name: "Kosal Rith Mony",
    role: "student",
    avatar: null,
    status: "online",
  };

  const PEOPLE = [
    { id: "admin-1",      name: "Mr. Heng Samnang",  role: "Administrator",       roleType: "admin",   initials: "HS", color: "#d97706", status: "online"  },
    { id: "teacher-1",   name: "Dr. Sarah Jenkins",  role: "Mathematics Teacher", roleType: "teacher", initials: "SJ", color: "#16a34a", status: "online"  },
    { id: "counselor-1", name: "Mrs. Channary Sot",  role: "School Counselor",    roleType: "counselor",initials: "CS", color: "#7c3aed", status: "away"    },
    { id: "it-1",         name: "IT Support",          role: "IT Department",       roleType: "admin",   initials: "IT", color: "#0891b2", status: "offline" },
    { id: "lib-1",        name: "Ms. Maly Lon",        role: "Librarian",            roleType: "staff",   initials: "ML", color: "#16a34a", status: "offline" },
    { id: "teacher-2",   name: "Mr. Dara Prum",       role: "English Teacher",      roleType: "teacher", initials: "DP", color: "#2563eb", status: "offline" },
    { id: "teacher-3",   name: "Ms. Sopheap Keo",     role: "Science Teacher",      roleType: "teacher", initials: "SK", color: "#ea580c", status: "online"  },
    { id: "admin-2",      name: "Ms. Bopha Rith",      role: "Finance Office",       roleType: "admin",   initials: "BR", color: "#db2777", status: "offline" },
    { id: "student-1",   name: "Ratha Sok",            role: "Student · Grade 10A",  roleType: "student", initials: "RS", color: "#2563eb", status: "online"  },
    { id: "student-2",   name: "Ly Channary",          role: "Student · Grade 10A",  roleType: "student", initials: "LC", color: "#16a34a", status: "online"  },
  ];

  const DEMO_CONVS = [
    {
      id: "admin-1",
      otherUser: PEOPLE[0],
      lastMessage: { message: "Your schedule change has been confirmed.", created_at: new Date(Date.now() - 1000 * 120).toISOString(), sender_id: "admin-1" },
      unread: 1,
    },
    {
      id: "teacher-1",
      otherUser: PEOPLE[1],
      lastMessage: { message: "Don't forget the assignment is due tonight!", created_at: new Date(Date.now() - 1000 * 3600).toISOString(), sender_id: "teacher-1" },
      unread: 0,
    },
    {
      id: "counselor-1",
      otherUser: PEOPLE[2],
      lastMessage: { message: "Please come by the office tomorrow morning.", created_at: new Date(Date.now() - 1000 * 3600 * 3).toISOString(), sender_id: "counselor-1" },
      unread: 0,
    },
    {
      id: "it-1",
      otherUser: PEOPLE[3],
      lastMessage: { message: "Your account issue has been resolved.", created_at: new Date(Date.now() - 1000 * 3600 * 24).toISOString(), sender_id: "it-1" },
      unread: 0,
    },
    {
      id: "lib-1",
      otherUser: PEOPLE[4],
      lastMessage: { message: "The book you requested is now available.", created_at: new Date(Date.now() - 1000 * 3600 * 48).toISOString(), sender_id: "lib-1" },
      unread: 0,
    },
  ];

  const DEMO_MESSAGES = {
    "admin-1": [
      { id: "m-101", conversation_id: "admin-1", sender_id: "student-me", message: "Good morning! I wanted to ask about changing my elective from Chinese to French. Is that possible?", created_at: new Date(Date.now() - 1000 * 3600 * 24).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
      { id: "m-102", conversation_id: "admin-1", sender_id: "admin-1", message: "Good morning! Of course — let me check the availability for the French class in your grade level.", created_at: new Date(Date.now() - 1000 * 3600 * 23.5).toISOString(), sender: PEOPLE[0] },
      { id: "m-103", conversation_id: "admin-1", sender_id: "admin-1", message: "French 10A currently has 3 open seats. I will submit the transfer request now.", created_at: new Date(Date.now() - 1000 * 3600 * 23.4).toISOString(), sender: PEOPLE[0] },
      { id: "m-104", conversation_id: "admin-1", sender_id: "student-me", message: "That's great! Thank you so much, Mr. Samnang. When will the change take effect?", created_at: new Date(Date.now() - 1000 * 3600 * 23).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
      { id: "m-105", conversation_id: "admin-1", sender_id: "admin-1", message: "The change will take effect from next Monday. You will receive a confirmation email as well. 😊", created_at: new Date(Date.now() - 1000 * 3600 * 22.8).toISOString(), sender: PEOPLE[0] },
      { id: "m-106", conversation_id: "admin-1", sender_id: "admin-1", message: "Good morning! Your schedule change request has been confirmed. French 10A starts Monday at 2:00 PM in Room 8A. ✅", created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(), sender: PEOPLE[0] },
      { id: "m-107", conversation_id: "admin-1", sender_id: "admin-1", message: "Please check your updated timetable on the portal. Let me know if you need anything else!", created_at: new Date(Date.now() - 1000 * 60 * 28).toISOString(), sender: PEOPLE[0] },
      { id: "m-108", conversation_id: "admin-1", sender_id: "student-me", message: "Wonderful! Thank you so much for your help! I really appreciate it 🙏", created_at: new Date(Date.now() - 1000 * 120).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
    ],
    "teacher-1": [
      { id: "m-201", conversation_id: "teacher-1", sender_id: "teacher-1", message: "Good morning class! Don't forget the calculus assignment is due tonight at 11:59 PM.", created_at: new Date(Date.now() - 1000 * 3600 * 4).toISOString(), sender: PEOPLE[1] },
      { id: "m-202", conversation_id: "teacher-1", sender_id: "student-me", message: "Hello Dr. Jenkins! I had a quick question regarding question 4 on page 78.", created_at: new Date(Date.now() - 1000 * 3600 * 2).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
      { id: "m-203", conversation_id: "teacher-1", sender_id: "teacher-1", message: "Remember to apply the chain rule first before taking the natural logarithm!", created_at: new Date(Date.now() - 1000 * 3600).toISOString(), sender: PEOPLE[1] },
      { id: "m-204", conversation_id: "teacher-1", sender_id: "student-me", message: "Ah, that makes so much sense now. Thank you Dr. Jenkins!", created_at: new Date(Date.now() - 1000 * 1800).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
    ],
    "counselor-1": [
      { id: "m-301", conversation_id: "counselor-1", sender_id: "counselor-1", message: "Please come by the counseling office tomorrow morning regarding your university prep profile.", created_at: new Date(Date.now() - 1000 * 3600 * 3).toISOString(), sender: PEOPLE[2] },
      { id: "m-302", conversation_id: "counselor-1", sender_id: "student-me", message: "I will be there at 9:00 AM Mrs. Sot. Should I bring my portfolio?", created_at: new Date(Date.now() - 1000 * 3600 * 2).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
    ],
    "it-1": [
      { id: "m-401", conversation_id: "it-1", sender_id: "student-me", message: "Hello IT team, I had an issue connecting to the campus Wi-Fi network in Block C.", created_at: new Date(Date.now() - 1000 * 3600 * 26).toISOString(), sender: { id: "student-me", name: "Kosal Rith Mony" } },
      { id: "m-402", conversation_id: "it-1", sender_id: "it-1", message: "Your account credentials and 802.1x security certificate have been refreshed. Try logging in now.", created_at: new Date(Date.now() - 1000 * 3600 * 24).toISOString(), sender: PEOPLE[3] },
    ],
    "lib-1": [
      { id: "m-501", conversation_id: "lib-1", sender_id: "lib-1", message: "The book you requested ('Advanced Principles of Chemistry') is now available at the front counter.", created_at: new Date(Date.now() - 1000 * 3600 * 48).toISOString(), sender: PEOPLE[4] },
    ],
  };

  const DEMO_SEARCH = PEOPLE;

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
    if (diff < 60)           return "now";
    if (diff < 3600)         return Math.floor(diff / 60) + "m";
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
    if (user?.avatar) {
      return `<img src="${escHtml(user.avatar)}" alt="${escHtml(user.name)}" class="${cls}" style="width:${size}px;height:${size}px;border-radius:50%;object-fit:cover;">`;
    }
    const bg = user?.color || "var(--primary)";
    const init = escHtml(user?.initials || initials(user?.name || "?"));
    return `<div class="${cls}" style="width:${size}px;height:${size}px;border-radius:50%;background:${bg};color:#fff;display:grid;place-items:center;font-size:${Math.round(size * 0.34)}px;font-weight:600;flex-shrink:0;">${init}</div>`;
  }

  function roleBadge(role) {
    const cls = { teacher: "role-teacher", student: "role-student", parent: "role-parent", admin: "role-admin", super_admin: "role-admin" };
    return `<span class="ur-role-badge ${cls[role] || ''}">${role.replace("_", " ")}</span>`;
  }

  /* ── DOM refs ─────────────────────────────────────────────── */
  const $ = (id) => document.getElementById(id);
  const convList      = $("convList");
  const convSearch    = $("peopleSearch");
  const peopleResults = $("peopleResults");
  const recentLabel   = $("recentLabel");
  const chatWin       = $("chatWin");
  const chatEmpty     = $("chatSelectState");
  const chatActive    = $("chatActive");
  const chatHName     = $("chatHName");
  const chatHStatus   = $("chatHStatus");
  const chatHAvaCont  = $("chatHAvaCont");
  const msgArea       = $("msgArea");
  const msgInput      = $("msgInput");
  const msgForm       = $("msgForm");
  const sendBtn       = $("sendBtn");
  const emojiBtn      = $("emojiBtn");
  const emojiPicker   = $("emojiPicker");
  const emojiGrid     = $("emojiGrid");
  const newChatBtn    = $("newChatBtn");
  const startChatBtn  = $("startChatBtn");
  const newChatModal  = $("newChatModal");
  const closeModal    = $("closeModal");
  const userSearch    = $("userSearch");
  const userResults   = $("userResults");
  const backBtn       = $("backBtn");
  const typingRow     = $("typingRow");
  const demoBanner    = $("demoBanner");

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
          <p>${f ? 'No results for "' + escHtml(f) + '"' : "No conversations yet.<br>Start one below."}</p>
        </div>`;
      return;
    }

    convList.innerHTML = filtered.map((c) => {
      const u = c.otherUser;
      const isActive = c.id === activeConvId;
      const preview = c.lastMessage?.message || "";
      const hasUnread = c.unread > 0;

      return `
        <div class="conv-item ${isActive ? "active" : ""}" data-id="${c.id}" data-conv="${c.id}" role="button" tabindex="0" aria-label="Chat with ${escHtml(u?.name || "")}">
          <div class="ava-wrap">
            ${avatarHtml(u || { name: "?" }, 44, "conv-ava-init")}
            <span class="s-dot ${u?.status || "offline"}"></span>
          </div>
          <div class="conv-info">
            <div class="conv-top">
              <span class="conv-name">${escHtml(u?.name || "Unknown")}</span>
              <span class="conv-time">${c.lastMessage ? fmtTime(c.lastMessage.created_at) : ""}</span>
            </div>
            <div class="conv-bottom">
              <span class="conv-preview ${hasUnread ? "unread" : ""}">${escHtml(preview.slice(0, 60))}</span>
              ${hasUnread ? `<span class="conv-badge">${c.unread > 99 ? "99+" : c.unread}</span>` : ""}
            </div>
          </div>
        </div>`;
    }).join("");
  }

  /* ── Open a conversation ──────────────────────────────────── */
  function openConversation(convId) {
    let conv = conversations.find((c) => c.id === convId);
    if (!conv) {
      const person = PEOPLE.find((p) => p.id === convId);
      if (person) {
        conv = {
          id: person.id,
          otherUser: person,
          lastMessage: null,
          unread: 0,
        };
        conversations.unshift(conv);
        if (!DEMO_MESSAGES[conv.id]) DEMO_MESSAGES[conv.id] = [];
      }
    }
    if (!conv) return;

    activeConvId = convId;
    const u = conv.otherUser;

    // Update header
    if (chatHAvaCont) {
      chatHAvaCont.innerHTML = `
        <div class="ava-wrap">
          ${avatarHtml(u, 40, "hava-init")}
          <span class="s-dot ${u?.status || "offline"}"></span>
        </div>`;
    }
    if (chatHName) chatHName.textContent = u?.name || "Unknown";
    if (chatHStatus) {
      chatHStatus.textContent = (u?.status === "online" ? "Online" : (u?.status === "away" ? "Away" : "Offline")) + (u?.role ? " · " + u.role : "");
      chatHStatus.className = "chat-hstatus" + (u?.status === "online" ? " is-online" : "");
    }

    // Show chat window with transition
    if (chatEmpty && chatEmpty.style.display !== 'none') {
      chatEmpty.classList.add('anim-out');
      setTimeout(() => {
        chatEmpty.style.display = 'none';
        chatEmpty.classList.remove('anim-out');
        chatActive.style.display = 'flex';
        void chatActive.offsetWidth;
        chatActive.classList.remove('anim-in');
        chatActive.classList.add('anim-in');
        scrollToBottom();
      }, 140);
    } else {
      if (chatEmpty) chatEmpty.style.display = 'none';
      chatActive.style.display = 'flex';
    }

    // Mobile transition (≤ 768px: single pane slide)
    if (window.innerWidth <= 768) {
      chatWin.classList.add("show-mobile");
      document.querySelector(".conv-panel")?.classList.add("hidden-mobile");
      document.body.classList.add("chat-open");
    }

    // Load messages
    loadMessages(convId);

    // Mark as read
    conv.unread = 0;
    renderConvList(convSearch ? convSearch.value : "");
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

  function getDemoReply(name) {
    const replies = [
      "Thank you for reaching out! I will look into this right away.",
      "Got your message. Let's discuss this during office hours.",
      "Thank you for the update! Everything looks good on our end.",
      "Understood! Please check back tomorrow for confirmation.",
      "Great question. I have forwarded this to the academic coordinator."
    ];
    return replies[Math.floor(Math.random() * replies.length)];
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
      if (conv) {
        conv.lastMessage = msg;
        renderConvList(convSearch ? convSearch.value : "");
      }

      // Realistic automated reply after brief typing simulation
      const currentActive = activeConvId;
      setTimeout(() => {
        if (activeConvId === currentActive && typingRow) {
          typingRow.classList.add("show");
          scrollToBottom(true);
        }
      }, 500);

      setTimeout(() => {
        if (activeConvId === currentActive) {
          if (typingRow) typingRow.classList.remove("show");
          const replyText = getDemoReply(conv?.otherUser?.name || "");
          const replyMsg = {
            id: `demo-${++msgIdCounter}`,
            conversation_id: currentActive,
            sender_id: conv?.otherUser?.id || "other",
            sender: conv?.otherUser || { id: "other", name: "Staff" },
            message: replyText,
            created_at: new Date().toISOString(),
          };
          appendMessage(replyMsg);
          if (conv) {
            conv.lastMessage = replyMsg;
            renderConvList(convSearch ? convSearch.value : "");
          }
        }
      }, 1700);
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
      padding:10px 18px;font-size:13px;font-weight: 400;box-shadow:var(--sh-3);
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

  function openModalFn() {
    if (newChatModal) {
      newChatModal.hidden = false;
      if (userSearch) {
        userSearch.value = "";
        userResults.innerHTML = `<p class="search-placeholder">Search for a teacher, admin, or support to start a conversation.</p>`;
        userSearch.focus();
      }
      return;
    }
    // Inline search mode:
    if (convSearch) {
      convSearch.focus();
      convSearch.select();
      if (!convSearch.value && peopleResults) {
        peopleResults.innerHTML = PEOPLE.map((p) => `
          <div class="people-result-item" data-id="${p.id}">
            <div class="pr-ava-wrap">
              <div class="pr-ava-init" style="background:${p.color}">${p.initials}</div>
              <span class="s-dot ${p.status}"></span>
            </div>
            <div class="pr-info">
              <div class="pr-name">${escHtml(p.name)}</div>
              <div class="pr-role">${escHtml(p.role)}</div>
            </div>
          </div>
        `).join("");
        peopleResults.classList.add("visible");
        if (recentLabel) recentLabel.hidden = true;
        if (convList) convList.hidden = true;
      }
    }
  }

  function closeModalFn() {
    if (newChatModal) newChatModal.hidden = true;
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
    if (convList) {
      convList.addEventListener("click", (ev) => {
        const item = ev.target.closest(".conv-item");
        if (!item) return;
        openConversation(item.dataset.id || item.dataset.conv);
      });

      convList.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter") {
          const item = ev.target.closest(".conv-item");
          if (item) openConversation(item.dataset.id || item.dataset.conv);
        }
      });
    }

    // People search (inline search or list filter)
    if (convSearch) {
      convSearch.addEventListener("input", () => {
        const q = convSearch.value.trim().toLowerCase();
        if (peopleResults) {
          if (!q) {
            peopleResults.innerHTML = "";
            peopleResults.classList.remove("visible");
            if (recentLabel) recentLabel.hidden = false;
            if (convList) convList.hidden = false;
            return;
          }
          const matched = PEOPLE.filter((p) =>
            p.name.toLowerCase().includes(q) || p.role.toLowerCase().includes(q)
          );
          if (!matched.length) {
            peopleResults.innerHTML = `<p class="no-results">No people found</p>`;
          } else {
            peopleResults.innerHTML = matched.map((p) => `
              <div class="people-result-item" data-id="${p.id}">
                <div class="pr-ava-wrap">
                  <div class="pr-ava-init" style="background:${p.color}">${p.initials}</div>
                  <span class="s-dot ${p.status}"></span>
                </div>
                <div class="pr-info">
                  <div class="pr-name">${escHtml(p.name)}</div>
                  <div class="pr-role">${escHtml(p.role)}</div>
                </div>
              </div>
            `).join("");
          }
          peopleResults.classList.add("visible");
          if (recentLabel) recentLabel.hidden = true;
          if (convList) convList.hidden = true;
        } else {
          renderConvList(convSearch.value);
        }
      });

      convSearch.addEventListener("keydown", (ev) => {
        if (ev.key === "Escape") {
          convSearch.value = "";
          if (peopleResults) {
            peopleResults.innerHTML = "";
            peopleResults.classList.remove("visible");
            if (recentLabel) recentLabel.hidden = false;
            if (convList) convList.hidden = false;
          }
        }
      });
    }

    if (peopleResults) {
      peopleResults.addEventListener("click", (ev) => {
        const item = ev.target.closest(".people-result-item");
        if (!item) return;
        convSearch.value = "";
        peopleResults.innerHTML = "";
        peopleResults.classList.remove("visible");
        if (recentLabel) recentLabel.hidden = false;
        if (convList) convList.hidden = false;
        openConversation(item.dataset.id);
      });
    }

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

    // Window resize handler to restore dual-pane layout when widened
    window.addEventListener("resize", () => {
      if (window.innerWidth > 768) {
        chatWin.classList.remove("show-mobile");
        document.querySelector(".conv-panel")?.classList.remove("hidden-mobile");
        document.body.classList.remove("chat-open");
      }
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
