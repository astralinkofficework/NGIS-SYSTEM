/**
 * ============================================================
 * NGIS School Management System — Express Server
 * New Gateway International School · 2026
 * ============================================================
 * Serves the entire static frontend and exposes a lightweight
 * REST-style API layer for news, notifications, and data.
 * Run:  node server.js  (or: npm start)
 * URL:  http://localhost:3000
 * ============================================================
 */

"use strict";

const express = require("express");
const path    = require("path");
const http    = require("http");

const app  = express();
const PORT = process.env.PORT || 3000;
const ROOT = __dirname;

/* ── Middleware ─────────────────────────────────────────────── */
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* Security headers */
app.use((_req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  next();
});

/* ── Static files ───────────────────────────────────────────── */
app.use(express.static(ROOT, {
  extensions: ["html"],
  index:      "index.html",
  etag:       true,
  maxAge:     "1h",
}));

/* ── In-memory data store (replaces DB until backend is wired) ── */
const DB = {
  /* ── News ── */
  news: [
    {
      id: 1, title: "School Sports Day 2026 — All Teams Ready",
      message: "Annual sports day is confirmed for July 20. All students must register by July 15.",
      image: null, audience: "all", priority: "normal",
      date: "2026-07-04", category: "events", pinned: false, views: 142, published: true
    },
    {
      id: 2, title: "Mid-Term Exam Schedule Released",
      message: "The official mid-term examination timetable for Semester 2, AY 2025-26 has been published.",
      image: null, audience: "all", priority: "urgent",
      date: "2026-07-03", category: "exams", pinned: true, views: 389, published: true
    },
    {
      id: 3, title: "New Library Resources Available",
      message: "The digital library has been updated with 200+ new reference materials across all subjects.",
      image: null, audience: "students", priority: "normal",
      date: "2026-07-02", category: "academic", pinned: false, views: 97, published: true
    },
    {
      id: 4, title: "Parent-Teacher Meeting — July 12",
      message: "All parents are invited to attend the progress review meeting. Booking required.",
      image: null, audience: "parents", priority: "normal",
      date: "2026-07-01", category: "events", pinned: false, views: 201, published: true
    },
    {
      id: 5, title: "School Closed — National Holiday July 25",
      message: "The school will be closed on July 25, 2026 in observance of the national holiday.",
      image: null, audience: "all", priority: "urgent",
      date: "2026-06-30", category: "urgent", pinned: true, views: 512, published: true
    },
  ],

  /* ── Notifications ── */
  notifications: [
    { id: 1, userId: "2026-STD-0142", type: "assignment", title: "New Assignment: Mathematics Ch.8", message: "Mr. Sophea posted a new assignment due July 10.", read: false, date: "2026-07-06" },
    { id: 2, userId: "2026-STD-0142", type: "exam",       title: "Exam Tomorrow: Physics Mid-Term", message: "Your Physics mid-term exam is scheduled for tomorrow at 8:00 AM.", read: false, date: "2026-07-05" },
    { id: 3, userId: "2026-STD-0142", type: "grade",      title: "Grade Released: Chemistry Practical", message: "Your Chemistry practical assessment result is now available. Score: 88%.", read: false, date: "2026-07-04" },
    { id: 4, userId: "2026-STD-0142", type: "general",    title: "Certificate Awarded: Perfect Attendance", message: "Congratulations! You have earned the Perfect Attendance certificate for May 2026.", read: true,  date: "2026-07-03" },
    { id: 5, userId: "2026-STD-0142", type: "club",       title: "Robotics Club: Meeting Tomorrow 3PM", message: "Reminder: Robotics Club weekly session is tomorrow after school.", read: true,  date: "2026-07-02" },
  ],

  /* ── Students ── */
  students: [
    { id: "2026-STD-0142", name: "Nrinphouneta Hok", grade: "Grade 10", class: "10A", gpa: 3.87, attendance: 96, status: "active" },
    { id: "2026-STD-0143", name: "Kosal Rith Mony",  grade: "Grade 11", class: "11B", gpa: 3.72, attendance: 94, status: "active" },
    { id: "2026-STD-0144", name: "Sophea Chan",      grade: "Grade 10", class: "10A", gpa: 3.55, attendance: 91, status: "active" },
  ],

  /* ── Clubs ── */
  clubs: [
    { id: 1, name: "Robotics Club",      description: "Build and program robots for competitions.", supervisor: "Mr. Ratanak Som",  members: 24, schedule: "Every Thursday 3-5 PM", capacity: 30, icon: "precision_manufacturing" },
    { id: 2, name: "Debate Society",     description: "Develop critical thinking and public speaking.", supervisor: "Ms. Nary Chan",   members: 18, schedule: "Every Tuesday 3-4:30 PM", capacity: 25, icon: "record_voice_over" },
    { id: 3, name: "Photography Club",   description: "Learn photography and visual storytelling.", supervisor: "Mr. Dara Vin",    members: 15, schedule: "Every Friday 3-5 PM", capacity: 20, icon: "camera_alt" },
    { id: 4, name: "Math Olympiad",      description: "Prepare for national mathematics competitions.", supervisor: "Mr. Chea Sophea", members: 12, schedule: "Every Wednesday 3-4 PM", capacity: 15, icon: "calculate" },
    { id: 5, name: "Green Earth Club",   description: "Environmental awareness and sustainability.", supervisor: "Ms. Bopha Keo",   members: 30, schedule: "Every Monday 3-4 PM",  capacity: 35, icon: "eco" },
    { id: 6, name: "Drama & Arts Club",  description: "Perform, create, and express through art.", supervisor: "Ms. Sreymom Lim",  members: 22, schedule: "Every Friday 2-4 PM",  capacity: 30, icon: "theater_comedy" },
  ],

  /* ── Lost & Found ── */
  lostFound: [
    { id: 1, type: "lost",  item: "Blue Water Bottle", description: "500ml blue Thermos brand, initials 'NK' scratched on the bottom.", location: "Cafeteria", date: "2026-07-04", status: "open",   photo: null, reporter: "Nrinphouneta Hok" },
    { id: 2, type: "found", item: "Glasses Case",      description: "Black hard-shell glasses case, no glasses inside.",              location: "Library",   date: "2026-07-05", status: "open",   photo: null, reporter: "Admin Office" },
    { id: 3, type: "found", item: "USB Flash Drive",   description: "16GB SanDisk USB, pink color.",                                  location: "Room 204",  date: "2026-07-03", status: "open",   photo: null, reporter: "Mr. Ratanak Som" },
    { id: 4, type: "lost",  item: "Scientific Calculator", description: "Casio FX-991ES Plus, has a sticker of a cat on the back.", location: "Physics Lab", date: "2026-07-02", status: "claimed", photo: null, reporter: "Sophea Chan" },
  ],

  /* ── Competitions ── */
  competitions: [
    { id: 1, name: "National Math Olympiad 2026",       type: "academic", deadline: "2026-07-20", date: "2026-08-10", eligibility: "Grade 10-12", teamSize: 1, status: "open",   registered: false },
    { id: 2, name: "ASEAN Robotics Championship",       type: "stem",     deadline: "2026-07-15", date: "2026-08-25", eligibility: "Grade 9-12",  teamSize: 3, status: "open",   registered: true  },
    { id: 3, name: "Inter-School Debate Tournament",    type: "academic", deadline: "2026-07-10", date: "2026-07-28", eligibility: "Grade 10-12", teamSize: 2, status: "closed", registered: false },
    { id: 4, name: "Photography Exhibition 2026",       type: "arts",     deadline: "2026-07-25", date: "2026-08-15", eligibility: "All Grades",  teamSize: 1, status: "open",   registered: false },
    { id: 5, name: "National Science Fair",             type: "stem",     deadline: "2026-08-01", date: "2026-08-30", eligibility: "Grade 9-12",  teamSize: 4, status: "open",   registered: false },
  ],

  /* ── Certificates ── */
  certificates: [
    { id: 1, title: "Perfect Attendance",       category: "attendance", date: "2026-06-30", semester: "Sem 1 2025-26", description: "Awarded for 100% attendance in Semester 1.", verifyCode: "NGIS-ATT-2026-0142-01" },
    { id: 2, title: "Academic Excellence",      category: "academic",   date: "2026-03-15", semester: "Sem 1 2025-26", description: "Top 5% GPA in Grade 10 Science Stream.",    verifyCode: "NGIS-ACE-2026-0142-01" },
    { id: 3, title: "ASEAN Robotics — 2nd Place", category: "competition", date: "2026-02-20", semester: "AY 2025-26", description: "2nd place finish at the ASEAN Robotics Championship 2026.", verifyCode: "NGIS-ROB-2026-0142-01" },
    { id: 4, title: "Community Service Award",  category: "behavior",   date: "2025-12-10", semester: "Sem 1 2025-26", description: "Recognized for 40+ hours of community service.", verifyCode: "NGIS-CSA-2025-0142-01" },
  ],

  /* ── Elections ── */
  elections: [
    {
      id: 1, title: "Student Council President 2026-27",
      status: "open", deadline: "2026-07-10", votesTotal: 87,
      candidates: [
        { id: "c1", name: "Kosal Rith Mony",  grade: "Grade 11", manifesto: "I will work to improve the school canteen menu and organize more cultural events.", votes: 34, photo: null },
        { id: "c2", name: "Sreyleak Chhun",   grade: "Grade 11", manifesto: "My focus is on digital learning resources and creating more study spaces.", votes: 31, photo: null },
        { id: "c3", name: "Panha Vuth",       grade: "Grade 10", manifesto: "I want to launch a peer tutoring program and improve sports facilities.", votes: 22, photo: null },
      ]
    }
  ],

  /* ── Feedback ── */
  feedback: [],

  /* ── Team Projects ── */
  projects: [
    {
      id: 1, title: "Physics Group Lab Report — Wave Interference",
      subject: "Physics", teacher: "Mr. Dara Vin", deadline: "2026-07-14",
      members: ["Nrinphouneta Hok", "Kosal Mony", "Sophea Chan", "Virak Heng"],
      tasks: [
        { id: "t1", title: "Set up experiment apparatus", status: "done",        assignee: "Kosal Mony" },
        { id: "t2", title: "Record wave frequency data",  status: "in-progress", assignee: "Nrinphouneta Hok" },
        { id: "t3", title: "Analyze results",             status: "todo",        assignee: "Sophea Chan" },
        { id: "t4", title: "Write final report",          status: "todo",        assignee: "Virak Heng" },
      ]
    }
  ],
};

let _nextId = 100;
const newId = () => ++_nextId;

/* ── API Routes ─────────────────────────────────────────────── */

/* Health check */
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", time: new Date().toISOString(), version: "1.0.0", name: "NGIS School Management System" });
});

/* ── NEWS ── */
app.get("/api/news", (req, res) => {
  const { audience, priority, category, q } = req.query;
  let items = DB.news.filter(n => n.published);
  if (audience && audience !== "all") items = items.filter(n => n.audience === audience || n.audience === "all");
  if (priority)  items = items.filter(n => n.priority === priority);
  if (category)  items = items.filter(n => n.category === category);
  if (q) { const lq = q.toLowerCase(); items = items.filter(n => n.title.toLowerCase().includes(lq) || n.message.toLowerCase().includes(lq)); }
  items.sort((a, b) => {
    if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
    if (a.priority === "urgent" && b.priority !== "urgent") return -1;
    if (b.priority === "urgent" && a.priority !== "urgent") return 1;
    return new Date(b.date) - new Date(a.date);
  });
  res.json({ data: items, meta: { total: items.length } });
});

app.get("/api/news/:id", (req, res) => {
  const item = DB.news.find(n => n.id === parseInt(req.params.id));
  if (!item) return res.status(404).json({ error: { code: "NOT_FOUND", message: "News post not found" } });
  item.views = (item.views || 0) + 1;
  res.json({ data: item });
});

app.post("/api/news", (req, res) => {
  const { title, message, audience, priority, category, pinned, image } = req.body;
  if (!title || !message) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "title and message are required" } });
  const item = { id: newId(), title, message, audience: audience || "all", priority: priority || "normal", category: category || "general", pinned: !!pinned, image: image || null, date: new Date().toISOString().slice(0,10), views: 0, published: true };
  DB.news.unshift(item);
  res.status(201).json({ data: item });
});

app.put("/api/news/:id", (req, res) => {
  const idx = DB.news.findIndex(n => n.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: { code: "NOT_FOUND", message: "News post not found" } });
  Object.assign(DB.news[idx], req.body);
  res.json({ data: DB.news[idx] });
});

app.delete("/api/news/:id", (req, res) => {
  const idx = DB.news.findIndex(n => n.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: { code: "NOT_FOUND", message: "News post not found" } });
  const deleted = DB.news.splice(idx, 1)[0];
  res.json({ data: deleted, message: "Deleted successfully" });
});

/* ── NOTIFICATIONS ── */
app.get("/api/notifications", (req, res) => {
  const { userId } = req.query;
  let items = userId ? DB.notifications.filter(n => n.userId === userId) : DB.notifications;
  res.json({ data: items, meta: { total: items.length, unread: items.filter(n => !n.read).length } });
});

app.put("/api/notifications/:id/read", (req, res) => {
  const n = DB.notifications.find(n => n.id === parseInt(req.params.id));
  if (!n) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Notification not found" } });
  n.read = true;
  res.json({ data: n });
});

app.put("/api/notifications/read-all", (req, res) => {
  const { userId } = req.body;
  DB.notifications.filter(n => !userId || n.userId === userId).forEach(n => { n.read = true; });
  res.json({ message: "All notifications marked as read" });
});

/* ── STUDENTS ── */
app.get("/api/students", (_req, res) => {
  res.json({ data: DB.students, meta: { total: DB.students.length } });
});

app.get("/api/students/:id", (req, res) => {
  const s = DB.students.find(s => s.id === req.params.id);
  if (!s) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });
  res.json({ data: s });
});

/* ── CLUBS ── */
app.get("/api/clubs", (_req, res) => {
  res.json({ data: DB.clubs, meta: { total: DB.clubs.length } });
});

app.post("/api/clubs/:id/join", (req, res) => {
  const club = DB.clubs.find(c => c.id === parseInt(req.params.id));
  if (!club) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Club not found" } });
  if (club.members >= club.capacity) return res.status(409).json({ error: { code: "FULL", message: "Club is at full capacity" } });
  club.members++;
  res.json({ data: club, message: "Join request submitted" });
});

/* ── LOST & FOUND ── */
app.get("/api/lost-found", (req, res) => {
  const { type, status } = req.query;
  let items = [...DB.lostFound];
  if (type)   items = items.filter(i => i.type === type);
  if (status) items = items.filter(i => i.status === status);
  res.json({ data: items, meta: { total: items.length } });
});

app.post("/api/lost-found", (req, res) => {
  const { type, item, description, location } = req.body;
  if (!type || !item || !description || !location) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "type, item, description, location required" } });
  const entry = { id: newId(), type, item, description, location, date: new Date().toISOString().slice(0,10), status: "open", photo: null, reporter: req.body.reporter || "Student" };
  DB.lostFound.unshift(entry);
  res.status(201).json({ data: entry });
});

/* ── COMPETITIONS ── */
app.get("/api/competitions", (_req, res) => {
  res.json({ data: DB.competitions, meta: { total: DB.competitions.length } });
});

app.post("/api/competitions/:id/register", (req, res) => {
  const comp = DB.competitions.find(c => c.id === parseInt(req.params.id));
  if (!comp) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Competition not found" } });
  if (comp.status === "closed") return res.status(409).json({ error: { code: "CLOSED", message: "Registration is closed" } });
  comp.registered = true;
  res.json({ data: comp, message: "Registered successfully" });
});

/* ── CERTIFICATES ── */
app.get("/api/certificates", (req, res) => {
  const { userId } = req.query;
  res.json({ data: DB.certificates, meta: { total: DB.certificates.length } });
});

app.get("/api/certificates/verify/:code", (req, res) => {
  const cert = DB.certificates.find(c => c.verifyCode === req.params.code);
  if (!cert) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Certificate not found or invalid" } });
  res.json({ data: cert, valid: true });
});

/* ── ELECTIONS ── */
app.get("/api/elections", (_req, res) => {
  res.json({ data: DB.elections, meta: { total: DB.elections.length } });
});

app.post("/api/elections/:id/vote", (req, res) => {
  const election = DB.elections.find(e => e.id === parseInt(req.params.id));
  if (!election) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Election not found" } });
  if (election.status !== "open") return res.status(409).json({ error: { code: "CLOSED", message: "Voting is closed" } });
  const candidate = election.candidates.find(c => c.id === req.body.candidateId);
  if (!candidate) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Invalid candidate" } });
  candidate.votes++;
  election.votesTotal++;
  election.voted = true;
  res.json({ data: election, message: "Vote recorded successfully" });
});

/* ── FEEDBACK ── */
app.post("/api/feedback", (req, res) => {
  const { message, anonymous, category } = req.body;
  if (!message) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "message is required" } });
  const entry = { id: newId(), message, category: category || "general", anonymous: !!anonymous, status: "submitted", date: new Date().toISOString().slice(0,10), reporter: anonymous ? "Anonymous" : (req.body.reporter || "Student") };
  DB.feedback.push(entry);
  res.status(201).json({ data: entry, message: "Feedback submitted successfully" });
});

/* ── TEAM PROJECTS ── */
app.get("/api/projects", (_req, res) => {
  res.json({ data: DB.projects, meta: { total: DB.projects.length } });
});

app.put("/api/projects/:pid/tasks/:tid", (req, res) => {
  const project = DB.projects.find(p => p.id === parseInt(req.params.pid));
  if (!project) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Project not found" } });
  const task = project.tasks.find(t => t.id === req.params.tid);
  if (!task) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Task not found" } });
  if (req.body.status) task.status = req.body.status;
  if (req.body.title)  task.title  = req.body.title;
  res.json({ data: project });
});

/* ── Dashboard summary ── */
app.get("/api/dashboard/:role", (req, res) => {
  const role = req.params.role;
  const base = {
    role,
    date: new Date().toISOString(),
    unreadNotifications: DB.notifications.filter(n => !n.read).length,
    news: DB.news.filter(n => n.published && n.pinned).slice(0, 3),
  };
  if (role === "student") {
    Object.assign(base, {
      student: DB.students[0],
      upcomingExams: 6,
      pendingAssignments: 3,
      attendanceRate: 96,
      gpa: 3.87,
      clubs: DB.clubs.slice(0, 2),
      certificates: DB.certificates.length,
    });
  } else if (role === "admin") {
    Object.assign(base, {
      totalStudents: DB.students.length,
      totalClubs:    DB.clubs.length,
      openLostFound: DB.lostFound.filter(i => i.status === "open").length,
      openElections: DB.elections.filter(e => e.status === "open").length,
    });
  }
  res.json({ data: base });
});

/* ── Catch-all: serve index.html for any unmatched route ── */
app.get("*", (req, res) => {
  /* If it looks like a static file request that doesn't exist, 404 */
  if (req.path.match(/\.(css|js|png|jpg|jpeg|gif|svg|ico|woff2?|ttf|eot|map)$/)) {
    return res.status(404).send("Not found");
  }
  res.sendFile(path.join(ROOT, "index.html"));
});

/* ── Start ───────────────────────────────────────────────────── */
const server = http.createServer(app);

server.listen(PORT, () => {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║   NGIS — New Gateway International School                ║");
  console.log("║   School Management System · Express Server              ║");
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log(`║   Running at:  http://localhost:${PORT}                       ║`);
  console.log(`║   Environment: ${(process.env.NODE_ENV || "development").padEnd(43)}║`);
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log("║   Portals:                                               ║");
  console.log(`║   Admin   →  http://localhost:${PORT}/pages/admin/admin.html  ║`);
  console.log(`║   Teacher →  http://localhost:${PORT}/pages/teacher/teacher.html ║`);
  console.log(`║   Student →  http://localhost:${PORT}/pages/student/student.html ║`);
  console.log(`║   Parent  →  http://localhost:${PORT}/pages/parent/parent.html  ║`);
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log(`║   API:  http://localhost:${PORT}/api/health                    ║`);
  console.log("╚══════════════════════════════════════════════════════════╝");
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`\n  ✗  Port ${PORT} is already in use. Try PORT=3001 node server.js\n`);
  } else {
    console.error("Server error:", err);
  }
  process.exit(1);
});

module.exports = app;
