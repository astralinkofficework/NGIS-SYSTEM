/* ============================================================
   NGIS Group Chat Client
   Class-based group messaging with demo mode fallback
   ============================================================ */
(function () {
  "use strict";

  /* ── Demo data ──────────────────────────────────────────── */
  const DEMO_USER = window.CURRENT_USER || {
    id: "demo-me", name: "Kosal Rith Mony", role: "student", avatar: null
  };

  const DEMO_CLASSES_STUDENT = [
    {
      id: "cls-1", name: "Grade 11A", grade_level: "Grade 11", section: "A",
      unread: 2, last_message: "See everyone tomorrow!", last_at: "2026-06-24T07:55:00Z",
      last_sender: "Sophea Kim"
    }
  ];

  const DEMO_CLASSES_TEACHER = [
    {
      id: "cls-1", name: "Grade 11A", grade_level: "Grade 11", section: "A",
      unread: 0, last_message: "Thank you teacher!", last_at: "2026-06-24T07:55:00Z",
      last_sender: "Kosal Rith"
    },
    {
      id: "cls-2", name: "Grade 10B", grade_level: "Grade 10", section: "B",
      unread: 3, last_message: "Is homework due today?", last_at: "2026-06-24T07:30:00Z",
      last_sender: "Chan Dara"
    },
    {
      id: "cls-3", name: "Grade 9 Science", grade_level: "Grade 9", section: "Science",
      unread: 0, last_message: "Lab report submitted ✓", last_at: "2026-06-23T16:10:00Z",
      last_sender: "Maly Srey"
    }
  ];

  const DEMO_CLASSES_ADMIN = [
    ...DEMO_CLASSES_TEACHER,
    {
      id: "cls-4", name: "Grade 12 Science", grade_level: "Grade 12", section: "Science",
      unread: 1, last_message: "Exam schedule posted", last_at: "2026-06-24T06:00:00Z",
      last_sender: "Admin"
    }
  ];

  const DEMO_MESSAGES = {
    "cls-1": [
      { id:"m1", sender:{ id:"t1", name:"Sophea Kim", role:"teacher" },
        message:"Good morning Grade 11A! 📢 Today we have a Math quiz at 10am. Please review chapters 3 and 4.", created_at:"2026-06-24T07:30:00Z" },
      { id:"m2", sender:{ id:"s1", name:"Rith Chan", role:"student" },
        message:"Good morning teacher! Will the quiz cover fractions and algebra?", created_at:"2026-06-24T07:32:00Z" },
      { id:"m3", sender:{ id:"t1", name:"Sophea Kim", role:"teacher" },
        message:"Yes, both topics. Focus on simplifying expressions and solving equations.", created_at:"2026-06-24T07:33:00Z" },
      { id:"m4", sender:{ id:"t1", name:"Sophea Kim", role:"teacher" },
        message:"I will share a practice sheet in the Documents section for extra preparation.", created_at:"2026-06-24T07:33:30Z" },
      { id:"m5", sender:{ id:"p1", name:"Sokha Mony (Parent)", role:"parent" },
        message:"Thank you for the reminder, teacher. My son will be prepared.", created_at:"2026-06-24T07:40:00Z" },
      { id:"m6", sender:{ id:"s2", name:"Maly Srey", role:"student" },
        message:"Where is the practice sheet? I cannot find it.", created_at:"2026-06-24T07:42:00Z" },
      { id:"m7", sender:{ id:"t1", name:"Sophea Kim", role:"teacher" },
        message:"I will upload it in 10 minutes. Please check the Documents tab.", created_at:"2026-06-24T07:43:00Z" },
      { id:"m8", sender:{ id:"demo-me", name:DEMO_USER.name, role:DEMO_USER.role },
        message:"Thank you teacher! I will study now.", created_at:"2026-06-24T07:55:00Z" }
    ],
    "cls-2": [
      { id:"m1", sender:{ id:"t2", name:"David Prak", role:"teacher" },
        message:"Reminder: your Math homework is due this Friday. Submit it via the Assignments page.", created_at:"2026-06-24T07:00:00Z" },
      { id:"m2", sender:{ id:"s3", name:"Chan Dara", role:"student" },
        message:"Is homework due today?", created_at:"2026-06-24T07:30:00Z" },
      { id:"m3", sender:{ id:"s4", name:"Panha Vuth", role:"student" },
        message:"I think it is Friday, not today.", created_at:"2026-06-24T07:31:00Z" }
    ],
    "cls-3": [
      { id:"m1", sender:{ id:"t3", name:"Lisa Chen", role:"teacher" },
        message:"Great work on the lab experiment yesterday! All reports are due by end of week.", created_at:"2026-06-23T15:50:00Z" },
      { id:"m2", sender:{ id:"s5", name:"Maly Srey", role:"student" },
        message:"Lab report submitted ✓", created_at:"2026-06-23T16:10:00Z" }
    ],
    "cls-4": [
      { id:"m1", sender:{ id:"a1", name:"School Admin", role:"admin" },
        message:"Final exam schedule has been posted. Please check the Timetables page for details.", created_at:"2026-06-24T06:00:00Z" }
    ]
  };

  const EMOJIS = [
    "😀","😂","😊","😍","🤔","😎","🥳","😅","👍","👏",
    "🙏","❤️","🎉","🔥","✅","⭐","📚","✏️","📝","🏫",
    "📢","💡","⏰","🎓","👨‍🏫","👩‍🏫","🤝","💪","🙌","😮",
    "😴","🤣","😭","😤","🤗","🫡","👋","✋","🫂","🎯",
    "📌","📎","🔔","📣","🌟"
  ];

  /* ── State ─────────────────────────────────────────────── */
  let socket         = null;
  let isDemo         = false;
  let authToken      = null;
  let currentClassId = null;
  let allClasses     = [];
  let messageCache   = {};
  let typingTimer    = null;
  let typingUsers    = new Map(); // userId → name

  const SERVER = window.GROUP_CHAT_SERVER || "http://localhost:3001";
  const ME     = DEMO_USER;

  /* ── Init ──────────────────────────────────────────────── */
  (function init() {
    buildEmojiGrid();
    bindUIEvents();

    // Try token from localStorage
    authToken = localStorage.getItem("ngis_chat_token");

    if (typeof io === "undefined") {
      enableDemoMode();
      return;
    }

    if (authToken) {
      connectSocket(authToken);
    } else {
      enableDemoMode();
    }
  })();

  /* ── Socket connection ─────────────────────────────────── */
  function connectSocket(token) {
    socket = io(SERVER, {
      auth: { token },
      reconnection: true,
      reconnectionAttempts: 3,
      timeout: 5000,
    });

    let connected = false;

    socket.on("connect", () => {
      connected = true;
      loadClasses();
    });

    socket.on("connect_error", () => {
      if (!connected) enableDemoMode();
    });

    socket.on("new_group_message", (msg) => {
      if (!msg.class_id && msg.classId) msg.class_id = msg.classId;
      // Update cache
      if (!messageCache[msg.class_id]) messageCache[msg.class_id] = [];
      messageCache[msg.class_id].push(msg);

      if (msg.class_id === currentClassId) {
        appendMessage(msg);
        socket.emit("mark_class_read", { classId: currentClassId });
      } else {
        incrementClassUnread(msg.class_id);
      }

      updateClassLastMsg(msg.class_id, msg.message, msg.created_at, msg.sender?.name);
    });

    socket.on("class_typing", ({ classId, userId, name, role, isTyping }) => {
      if (classId !== currentClassId) return;
      if (isTyping) {
        typingUsers.set(userId, name);
      } else {
        typingUsers.delete(userId);
      }
      renderTypingIndicator();
    });

    socket.on("group_notification", ({ classId, senderName, preview }) => {
      if (classId !== currentClassId) {
        showBrowserNotification(senderName, preview);
      }
    });

    socket.on("user_status", ({ userId, status }) => {
      // Update online indicators if needed
    });
  }

  /* ── Demo mode ─────────────────────────────────────────── */
  function enableDemoMode() {
    isDemo = true;
    document.getElementById("demoBanner").hidden = false;
    loadClasses();
  }

  /* ── Load class list ───────────────────────────────────── */
  function loadClasses() {
    if (isDemo) {
      const role = ME.role;
      let classes = DEMO_CLASSES_STUDENT;
      if (role === "teacher")             classes = DEMO_CLASSES_TEACHER;
      else if (role === "admin" || role === "super_admin") classes = DEMO_CLASSES_ADMIN;
      else if (role === "parent")         classes = DEMO_CLASSES_STUDENT; // parent: child's class
      allClasses = classes;
      renderClassList(classes);
      return;
    }

    fetch(`${SERVER}/api/classes`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then((r) => r.json())
      .then((classes) => {
        allClasses = classes;
        renderClassList(classes);
      })
      .catch(() => {
        isDemo = true;
        loadClasses();
      });
  }

  function renderClassList(classes) {
    const list = document.getElementById("classList");

    if (!classes.length) {
      list.innerHTML = `
        <div class="class-empty-state">
          <span class="material-symbols-outlined">school</span>
          <p>You are not assigned to any class yet.</p>
        </div>`;
      return;
    }

    list.innerHTML = classes.map(renderClassItem).join("");

    list.querySelectorAll(".class-item").forEach((el) => {
      el.addEventListener("click", () => openClass(el.dataset.classId));
    });

    // Auto-open first class on desktop
    if (window.innerWidth > 768 && classes.length) {
      openClass(classes[0].id);
    }
  }

  function renderClassItem(cls) {
    const initials = classInitials(cls.name);
    const lastMsg  = cls.last_message
      ? escHtml((cls.last_sender ? cls.last_sender + ": " : "") + cls.last_message)
      : "<em>No messages yet</em>";
    const time = cls.last_at ? formatTime(cls.last_at) : "";
    const badge = cls.unread > 0
      ? `<span class="unread-badge">${cls.unread > 99 ? "99+" : cls.unread}</span>`
      : "";

    return `
      <div class="class-item" data-class-id="${cls.id}" role="option" tabindex="0"
           aria-selected="false" aria-label="${escHtml(cls.name)}">
        <div class="class-ava">${initials}</div>
        <div class="class-info">
          <div class="class-name">${escHtml(cls.name)}</div>
          <div class="class-last-msg">${lastMsg}</div>
        </div>
        <div class="class-meta">
          <span class="class-time">${time}</span>
          ${badge}
        </div>
      </div>`;
  }

  /* ── Open a class chat ─────────────────────────────────── */
  function openClass(classId) {
    currentClassId = classId;
    const cls = allClasses.find((c) => c.id === classId);
    if (!cls) return;

    // Update active item
    document.querySelectorAll(".class-item").forEach((el) => {
      const active = el.dataset.classId === classId;
      el.classList.toggle("active", active);
      el.setAttribute("aria-selected", active);
    });

    // Update header
    const headerAva = document.getElementById("gchatHeaderAva");
    if (headerAva) headerAva.textContent = classInitials(cls.name);
    setEl("gchatHName",  cls.name);
    setEl("gchatHMeta",  `${cls.grade_level || ""}${cls.section ? " · " + cls.section : ""} · Group Chat`);

    // Show active chat, hide empty state
    show("gchatActive");
    document.getElementById("gchatEmpty").hidden = true;

    // Mobile: slide to chat
    if (window.innerWidth <= 768) {
      document.getElementById("classPanel").classList.add("panel-hidden");
    }

    // Load messages
    loadMessages(classId);

    // Mark read
    cls.unread = 0;
    const badge = document.querySelector(`.class-item[data-class-id="${classId}"] .unread-badge`);
    if (badge) badge.remove();

    if (socket && !isDemo) {
      socket.emit("mark_class_read", { classId });
      socket.emit("join_class", classId);
    }

    // Clear typing indicator
    typingUsers.clear();
    renderTypingIndicator();
  }

  /* ── Load messages ─────────────────────────────────────── */
  function loadMessages(classId) {
    if (isDemo) {
      const msgs = DEMO_MESSAGES[classId] || [];
      messageCache[classId] = msgs;
      renderMessages(classId);
      return;
    }

    // Show loading state
    const area = document.getElementById("gmsgArea");
    area.innerHTML = `<div style="text-align:center;padding:40px;color:var(--muted)">Loading…</div>`;

    fetch(`${SERVER}/api/classes/${classId}/messages`, {
      headers: { Authorization: `Bearer ${authToken}` }
    })
      .then((r) => r.json())
      .then((msgs) => {
        messageCache[classId] = msgs;
        renderMessages(classId);
      })
      .catch(() => {
        area.innerHTML = `<div style="text-align:center;padding:40px;color:var(--muted)">Could not load messages.</div>`;
      });
  }

  function renderMessages(classId) {
    const messages = messageCache[classId] || [];
    const area = document.getElementById("gmsgArea");
    area.innerHTML = "";

    if (!messages.length) {
      area.innerHTML = `
        <div style="text-align:center;padding:40px;color:var(--muted);font-size:13px">
          No messages yet. Be the first to say something!
        </div>`;
      return;
    }

    let lastDate     = null;
    let lastSenderId = null;

    messages.forEach((msg) => {
      // Date separator
      const msgDate = new Date(msg.created_at).toLocaleDateString("en-US", {
        weekday: "long", year: "numeric", month: "long", day: "numeric"
      });
      if (msgDate !== lastDate) {
        area.appendChild(makeDateSep(msgDate));
        lastDate     = msgDate;
        lastSenderId = null;
      }

      const isMe   = msg.sender?.id === ME.id;
      const grouped = !isMe && lastSenderId === msg.sender?.id;

      area.appendChild(makeMessageRow(msg, isMe, grouped));
      lastSenderId = msg.sender?.id || null;
    });

    area.scrollTop = area.scrollHeight;
  }

  function appendMessage(msg) {
    const area = document.getElementById("gmsgArea");
    if (!area) return;

    // Remove "no messages" placeholder if present
    const placeholder = area.querySelector("div[style]");
    if (placeholder && area.children.length === 1) placeholder.remove();

    const msgs        = messageCache[currentClassId] || [];
    const prev        = msgs[msgs.length - 1];
    const isMe        = msg.sender?.id === ME.id;
    const grouped     = !isMe && prev?.sender?.id === msg.sender?.id;

    area.appendChild(makeMessageRow(msg, isMe, grouped));
    area.scrollTop = area.scrollHeight;

    // Add to cache
    if (!messageCache[currentClassId]) messageCache[currentClassId] = [];
    messageCache[currentClassId].push(msg);
  }

  /* ── DOM builders ──────────────────────────────────────── */
  function makeDateSep(label) {
    const div = document.createElement("div");
    div.className = "date-sep";
    div.textContent = label;
    return div;
  }

  function makeMessageRow(msg, isMe, grouped) {
    const sender = msg.sender || {};
    const role   = sender.role || "student";
    const ava    = initials(sender.name || "?");
    const time   = formatTime(msg.created_at);

    const row = document.createElement("div");
    row.className = `gmsg-row${isMe ? " outgoing" : ""}${grouped ? " grouped" : ""}`;
    row.dataset.msgId = msg.id;

    if (!isMe) {
      // Avatar
      const avaEl = document.createElement("div");
      avaEl.className = `gmsg-ava role-${role}`;
      avaEl.textContent = ava;
      row.appendChild(avaEl);
    }

    const content = document.createElement("div");
    content.className = "gmsg-content";

    // Sender info (name + role badge) — only for incoming, not grouped
    if (!isMe && !grouped) {
      const senderInfo = document.createElement("div");
      senderInfo.className = "gmsg-sender-info";
      senderInfo.innerHTML = `
        <span class="gmsg-sender-name">${escHtml(sender.name || "Unknown")}</span>
        <span class="role-badge rb-${role}">${roleLabel(role)}</span>`;
      content.appendChild(senderInfo);
    }

    // Bubble
    const bubble = document.createElement("div");
    bubble.className = "gmsg-bubble";
    bubble.textContent = msg.message || "";

    // Time inside bubble (small)
    const timeEl = document.createElement("span");
    timeEl.className = "gmsg-time";
    timeEl.style.cssText = "display:block;text-align:" + (isMe ? "right" : "left") + ";margin-top:2px;font-size:10px;";
    timeEl.textContent = time;

    content.appendChild(bubble);
    content.appendChild(timeEl);
    row.appendChild(content);

    return row;
  }

  /* ── Send message ──────────────────────────────────────── */
  const msgForm  = document.getElementById("gmsgForm");
  const msgInput = document.getElementById("gmsgInput");
  const sendBtn  = document.getElementById("gsendBtn");

  msgInput.addEventListener("input", () => {
    autoGrowTextarea(msgInput);
    sendBtn.disabled = !msgInput.value.trim();
    handleTypingEvent();
  });

  msgInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!sendBtn.disabled) msgForm.dispatchEvent(new Event("submit"));
    }
  });

  msgForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = msgInput.value.trim();
    if (!text || !currentClassId) return;

    msgInput.value = "";
    msgInput.style.height = "";
    sendBtn.disabled = true;
    stopTypingEvent();

    if (isDemo) {
      const msg = {
        id: "demo-" + Date.now(),
        class_id: currentClassId,
        sender: { id: ME.id, name: ME.name, role: ME.role },
        message: text,
        created_at: new Date().toISOString()
      };
      appendMessage(msg);
      updateClassLastMsg(currentClassId, text, msg.created_at, ME.name);
      return;
    }

    socket.emit("send_group_message", { classId: currentClassId, message: text }, (res) => {
      if (res?.error) {
        console.error("Send error:", res.error);
      }
    });
  });

  /* ── Typing events ─────────────────────────────────────── */
  let isCurrentlyTyping = false;

  function handleTypingEvent() {
    if (!socket || isDemo || !currentClassId) return;
    if (!isCurrentlyTyping) {
      isCurrentlyTyping = true;
      socket.emit("typing_class_start", { classId: currentClassId });
    }
    clearTimeout(typingTimer);
    typingTimer = setTimeout(stopTypingEvent, 3000);
  }

  function stopTypingEvent() {
    if (!socket || isDemo || !currentClassId) return;
    if (isCurrentlyTyping) {
      isCurrentlyTyping = false;
      socket.emit("typing_class_stop", { classId: currentClassId });
    }
    clearTimeout(typingTimer);
  }

  function renderTypingIndicator() {
    const row = document.getElementById("typingRow");
    const nameEl = document.getElementById("typingName");
    const names = [...typingUsers.values()];
    if (names.length === 0) {
      row.classList.remove("visible");
    } else {
      const label = names.length === 1
        ? `${names[0]} is typing…`
        : names.length === 2
          ? `${names[0]} and ${names[1]} are typing…`
          : "Several people are typing…";
      if (nameEl) nameEl.textContent = label;
      row.classList.add("visible");
    }
  }

  /* ── Emoji picker ──────────────────────────────────────── */
  function buildEmojiGrid() {
    const grid = document.getElementById("emojiGrid");
    if (!grid) return;
    grid.innerHTML = EMOJIS.map((e) =>
      `<button type="button" aria-label="${e}">${e}</button>`
    ).join("");
    grid.addEventListener("click", (ev) => {
      const btn = ev.target.closest("button");
      if (!btn) return;
      const pos = msgInput.selectionStart;
      const val = msgInput.value;
      msgInput.value = val.slice(0, pos) + btn.textContent + val.slice(pos);
      msgInput.selectionStart = msgInput.selectionEnd = pos + btn.textContent.length;
      msgInput.focus();
      sendBtn.disabled = !msgInput.value.trim();
      document.getElementById("emojiPicker").hidden = true;
      document.getElementById("gemojiBtn").setAttribute("aria-expanded", "false");
    });
  }

  document.getElementById("gemojiBtn").addEventListener("click", (e) => {
    e.stopPropagation();
    const picker = document.getElementById("emojiPicker");
    const open   = picker.hidden;
    picker.hidden = !open;
    e.currentTarget.setAttribute("aria-expanded", open);
  });

  document.addEventListener("click", (e) => {
    const picker = document.getElementById("emojiPicker");
    if (!picker.hidden && !picker.contains(e.target) && e.target.id !== "gemojiBtn") {
      picker.hidden = true;
      document.getElementById("gemojiBtn").setAttribute("aria-expanded", "false");
    }
  });

  /* ── Back button (mobile) ──────────────────────────────── */
  document.getElementById("gchatBackBtn").addEventListener("click", () => {
    document.getElementById("classPanel").classList.remove("panel-hidden");
    currentClassId = null;
    typingUsers.clear();
    renderTypingIndicator();
  });

  /* ── UI helpers ────────────────────────────────────────── */
  function bindUIEvents() {
    // Keyboard navigation on class items
    document.getElementById("classList").addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        const item = e.target.closest(".class-item");
        if (item) openClass(item.dataset.classId);
      }
    });
  }

  function updateClassLastMsg(classId, message, at, senderName) {
    const item = document.querySelector(`.class-item[data-class-id="${classId}"]`);
    if (!item) return;
    const preview = item.querySelector(".class-last-msg");
    const time    = item.querySelector(".class-time");
    if (preview) preview.textContent = (senderName ? senderName + ": " : "") + message;
    if (time)    time.textContent    = formatTime(at);
  }

  function incrementClassUnread(classId) {
    const item = document.querySelector(`.class-item[data-class-id="${classId}"]`);
    if (!item) return;
    const existing = item.querySelector(".unread-badge");
    if (existing) {
      const n = parseInt(existing.textContent) || 0;
      existing.textContent = n + 1 > 99 ? "99+" : String(n + 1);
    } else {
      const meta = item.querySelector(".class-meta");
      if (meta) {
        const badge = document.createElement("span");
        badge.className = "unread-badge";
        badge.textContent = "1";
        meta.appendChild(badge);
      }
    }
  }

  function show(id)    { const el = document.getElementById(id); if (el) el.hidden = false; }

  function setEl(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function autoGrowTextarea(el) {
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
  }

  /* ── Notification ──────────────────────────────────────── */
  function showBrowserNotification(name, preview) {
    if (!("Notification" in window) || Notification.permission !== "granted") return;
    new Notification(`${name} — NGIS`, { body: preview, icon: "assets/img/icon.png" });
  }

  /* ── Formatting utils ──────────────────────────────────── */
  function formatTime(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return "";
    const now   = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const msgD  = new Date(d.getFullYear(), d.getMonth(), d.getDate());
    const diff  = (today - msgD) / 864e5;
    if (diff < 1) return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    if (diff < 2) return "Yesterday";
    return d.toLocaleDateString([], { month: "short", day: "numeric" });
  }

  function initials(name) {
    if (!name) return "?";
    return name.split(" ").slice(0, 2).map((w) => w[0] || "").join("").toUpperCase();
  }

  function classInitials(name) {
    const words = name.split(" ").filter(Boolean);
    if (words.length >= 2) return words[0][0].toUpperCase() + words[1][0].toUpperCase();
    return name.slice(0, 2).toUpperCase();
  }

  function roleLabel(role) {
    const map = { teacher:"Teacher", student:"Student", parent:"Parent",
                  admin:"Admin", super_admin:"Admin" };
    return map[role] || role;
  }

  function escHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

})();
