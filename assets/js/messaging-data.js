/* ============================================================
   NGIS Messaging Module — assets/js/messaging-data.js
   Shared demo dataset + role permission matrix for the
   messaging module pages (frontend demo — no backend yet).
   ============================================================ */
(function () {
  "use strict";

  var ROLE = (window.PAGE && window.PAGE.role) || "student";

  /* ── Permission matrix (frontend demo of server-side policy) ──
     In production every check must be re-validated server-side. */
  var PERMS = {
    student: ["dm", "class_chat", "group_chat", "dept_channel", "school_ann", "search", "report"],
    parent:  ["dm", "school_ann", "campus_ann", "search", "report"],
    teacher: ["dm", "class_chat", "group_chat", "dept_channel", "school_ann", "campus_ann", "class_ann", "requests", "pinned", "search", "moderation", "report"],
    admin:   ["dm", "class_chat", "group_chat", "dept_channel", "school_ann", "campus_ann", "class_ann", "requests", "pinned", "search", "moderation", "report", "admin", "telegram", "audit", "suspend"]
  };

  function can(action) {
    return (PERMS[ROLE] || []).indexOf(action) !== -1;
  }

  /* ── Current user (demo identities per role) ── */
  var ME = {
    student: { id: "STU-2026-0142", name: "Nrinphouneta Hok", role: "student", roleLabel: "Student · Grade 10A", campus: "Sen Sok", dept: "Science", grade: "Grade 10", classId: "10A", initials: "NH", color: "#0e7490", status: "online" },
    parent:  { id: "PAR-2026-0001", name: "Chan Dara Vuth", role: "parent", roleLabel: "Parent / Guardian", campus: "Sen Sok", dept: "—", grade: "—", classId: "—", initials: "CV", color: "#b45309", status: "online" },
    teacher: { id: "TCH-2026-0001", name: "Dr. Sarah Jenkins", role: "teacher", roleLabel: "Mathematics Teacher", campus: "Sen Sok", dept: "Mathematics", grade: "—", classId: "10A", initials: "SJ", color: "#16a34a", status: "online" },
    admin:   { id: "ADM-2026-0001", name: "Heng Samnang", role: "admin", roleLabel: "Super Administrator", campus: "Sen Sok", dept: "Administration", grade: "—", classId: "—", initials: "HS", color: "#d97706", status: "online" }
  };

  /* ── School directory (authenticated users only) ── */
  var DIRECTORY = [
    { id: "TCH-2026-0001", name: "Dr. Sarah Jenkins", role: "teacher", roleLabel: "Mathematics Teacher", dept: "Mathematics", campus: "Sen Sok", classId: "10A", initials: "SJ", color: "#16a34a", status: "online" },
    { id: "TCH-2026-0002", name: "Mr. Sophea", role: "teacher", roleLabel: "Physics Teacher", dept: "Science", campus: "Sen Sok", classId: "10A", initials: "SP", color: "#0891b2", status: "online" },
    { id: "TCH-2026-0003", name: "Ms. Kiry Sokha", role: "teacher", roleLabel: "Biology Teacher", dept: "Science", campus: "Sen Sok", classId: "10B", initials: "KS", color: "#7c3aed", status: "away" },
    { id: "TCH-2026-0004", name: "Mr. Oudom", role: "teacher", roleLabel: "Mathematics Teacher", dept: "Mathematics", campus: "Depo", classId: "11A", initials: "OU", color: "#2563eb", status: "offline" },
    { id: "TCH-2026-0005", name: "Mrs. Neary", role: "teacher", roleLabel: "English Teacher", dept: "English", campus: "Sen Sok", classId: "10A", initials: "NE", color: "#db2777", status: "offline" },
    { id: "TCH-2026-0006", name: "Mr. Heng Samnang", role: "teacher", roleLabel: "Chinese Teacher", dept: "Chinese", campus: "Bak Touk", classId: "12A", initials: "HS", color: "#d97706", status: "online" },
    { id: "STU-2026-0001", name: "Ratha Sok", role: "student", roleLabel: "Student · Grade 10A", dept: "Science", campus: "Sen Sok", classId: "10A", initials: "RS", color: "#2563eb", status: "online" },
    { id: "STU-2026-0002", name: "Ly Channary", role: "student", roleLabel: "Student · Grade 10A", dept: "Science", campus: "Sen Sok", classId: "10A", initials: "LC", color: "#16a34a", status: "online" },
    { id: "STU-2026-0003", name: "Vuth Dara", role: "student", roleLabel: "Student · Grade 10A", dept: "Science", campus: "Sen Sok", classId: "10A", initials: "VD", color: "#7c3aed", status: "away" },
    { id: "STU-2026-0004", name: "Emily Jenkins", role: "student", roleLabel: "Student · Grade 10B", dept: "English", campus: "Sen Sok", classId: "10B", initials: "EJ", color: "#0891b2", status: "online" },
    { id: "STU-2026-0005", name: "Kevin Jenkins", role: "student", roleLabel: "Student · Grade 8A", dept: "Khmer", campus: "Depo", classId: "8A", initials: "KJ", color: "#ea580c", status: "offline" },
    { id: "ADM-2026-0001", name: "Heng Samnang", role: "admin", roleLabel: "Super Administrator", dept: "Administration", campus: "Sen Sok", classId: "—", initials: "HS", color: "#d97706", status: "online" },
    { id: "ADM-2026-0002", name: "Keo Pich", role: "admin", roleLabel: "Campus Admin · Depo", dept: "Finance", campus: "Depo", classId: "—", initials: "KP", color: "#db2777", status: "away" },
    { id: "PRI-2026-0001", name: "Dr. Lay Kimchhean", role: "principal", roleLabel: "Principal · Sen Sok", dept: "Science", campus: "Sen Sok", classId: "—", initials: "LK", color: "#0f766e", status: "online" },
    { id: "PRI-2026-0002", name: "Mrs. Tep Vanny", role: "principal", roleLabel: "Dept Principal · English", dept: "English", campus: "Depo", classId: "—", initials: "TV", color: "#b91c1c", status: "offline" }
  ];

  /* ── Class structure: Campus → Grade → Class (auto-membership) ── */
  var CAMPUS_TREE = [
    {
      campus: "Sen Sok",
      grades: [
        { grade: "Grade 10", classes: [
          { id: "SS-G10-10A", name: "Class 10A", members: 28, homeroom: "Dr. Sarah Jenkins", subject: "Homeroom", unread: 3, lastMsg: "Dr. Sarah Jenkins: Quiz results are on the portal", time: "2m" },
          { id: "SS-G10-10B", name: "Class 10B", members: 26, homeroom: "Ms. Kiry Sokha", subject: "Homeroom", unread: 0, lastMsg: "Ms. Kiry Sokha: Lab reports due Friday", time: "1h" },
          { id: "SS-G10-10C", name: "Class 10C", members: 27, homeroom: "Mr. Sophea", subject: "Homeroom", unread: 0, lastMsg: "Mr. Sophea: Field trip forms signed?", time: "3h" }
        ]},
        { grade: "Grade 11", classes: [
          { id: "SS-G11-11A", name: "Class 11A", members: 25, homeroom: "Mr. Oudom", subject: "Homeroom", unread: 1, lastMsg: "Mr. Oudom: Study group at lunch", time: "5h" },
          { id: "SS-G11-11B", name: "Class 11B", members: 24, homeroom: "Mrs. Neary", subject: "Homeroom", unread: 0, lastMsg: "Mrs. Neary: Essay outlines checked", time: "Yesterday" }
        ]}
      ]
    },
    {
      campus: "Depo",
      grades: [
        { grade: "Grade 8", classes: [
          { id: "DP-G8-8A", name: "Class 8A", members: 30, homeroom: "Mr. Heng Samnang", subject: "Homeroom", unread: 0, lastMsg: "Mr. Heng Samnang: Khmer dictation tomorrow", time: "Yesterday" }
        ]},
        { grade: "Grade 11", classes: [
          { id: "DP-G11-11A", name: "Class 11A", members: 22, homeroom: "Mr. Oudom", subject: "Homeroom", unread: 0, lastMsg: "Mr. Oudom: No homework this weekend", time: "2d" }
        ]}
      ]
    },
    {
      campus: "Bak Touk",
      grades: [
        { grade: "Grade 12", classes: [
          { id: "BT-G12-12A", name: "Class 12A", members: 23, homeroom: "Mr. Heng Samnang", subject: "Homeroom", unread: 0, lastMsg: "Mr. Heng Samnang: Graduation photos Tuesday", time: "3d" }
        ]}
      ]
    }
  ];

  /* ── Department channels ── */
  var CHANNELS = [
    { id: "CH-KHM", dept: "Khmer", name: "Khmer Department", desc: "Khmer language curriculum, events and resources.", members: 48, unread: 2, posting: "teachers", lastMsg: "Mrs. Tep Vanny: Khmer literature week schedule", time: "12m", icon: "ខ" },
    { id: "CH-ENG", dept: "English", name: "English Department", desc: "English curriculum, IELTS prep and shared resources.", members: 52, unread: 1, posting: "teachers", lastMsg: "Dr. Lay Kimchhean: Oral exam rubric updated", time: "44m", icon: "EN" },
    { id: "CH-SCI", dept: "Science", name: "Science Department", desc: "Physics, chemistry, biology and lab coordination.", members: 41, unread: 0, posting: "teachers", lastMsg: "Dr. Sarah Jenkins: Lab safety refresher on Monday", time: "2h", icon: "SC" },
    { id: "CH-MATH", dept: "Mathematics", name: "Mathematics Department", desc: "Mathematics curriculum and assessment planning.", members: 36, unread: 0, posting: "teachers", lastMsg: "Mr. Oudom: Semester 2 pacing guide", time: "5h", icon: "MA" },
    { id: "CH-CHN", dept: "Chinese", name: "Chinese Department", desc: "Chinese language program and cultural events.", members: 19, unread: 0, posting: "teachers", lastMsg: "Mr. Heng Samnang: Chinese New Year program draft", time: "Yesterday", icon: "CN" },
    { id: "CH-PE", dept: "Physical Education", name: "Physical Education", desc: "Sports programs and athletics coordination.", members: 14, unread: 0, posting: "admins", lastMsg: "Mr. Phearith Kong: Sports Day roster final", time: "2d", icon: "PE" },
    { id: "CH-ADM", dept: "Administration", name: "School Administration", desc: "Whole-school operations. Staff only.", members: 12, unread: 1, posting: "admins", lastMsg: "Heng Samnang: Staff assembly Friday 7:45 AM", time: "3d", icon: "AD" }
  ];

  /* ── Announcements (school + campus + targeted) ── */
  var ANNOUNCEMENTS = [
    { id: "AN-1001", scope: "school", title: "Semester 2 Final Examination Timetable", body: "Final examinations run 14–25 July 2026. Check your personal schedule in the Exams section.", audience: "All campuses · All grades", priority: "urgent", pinned: true, status: "published", reads: 1184, total: 1240, author: "Administration Office", authorRole: "School Administration", date: "2026-06-20", telegram: true },
    { id: "AN-1002", scope: "campus", title: "Sen Sok Campus — Fire Drill 9 July", body: "Fire drill for all Sen Sok students and staff at 9:00 AM on 9 July. Assemble at the sports field.", audience: "Sen Sok Campus · All grades", priority: "important", pinned: true, status: "published", reads: 642, total: 680, author: "Keo Pich", authorRole: "Campus Admin", date: "2026-06-24", telegram: true },
    { id: "AN-1003", scope: "dept", title: "Science Fair 2026 — Registration Deadline 5 July", body: "Open to all Grade 10–12 students. Submit your proposal to your homeroom teacher before Friday, 5 July.", audience: "Science Dept · Grades 10–12", priority: "important", pinned: false, status: "published", reads: 561, total: 610, author: "Dr. Kosal Vann", authorRole: "Science Department", date: "2026-06-21", telegram: false },
    { id: "AN-1004", scope: "grade", title: "Grade 10 — Parent-Teacher Meetings 12 July", body: "Progress review meetings for all Grade 10 parents. Booking opens Monday via the parent portal.", audience: "Grade 10 · Parents", priority: "normal", pinned: false, status: "published", reads: 210, total: 240, author: "Dr. Sarah Jenkins", authorRole: "Homeroom Teacher", date: "2026-06-26", telegram: false },
    { id: "AN-1005", scope: "class", title: "Class 10A — Room change for Physics", body: "Physics practical moves to Lab 2 (Room 204) this week while Lab 1 is maintained.", audience: "Class 10A · Sen Sok", priority: "normal", pinned: false, status: "published", reads: 27, total: 28, author: "Mr. Sophea", authorRole: "Physics Teacher", date: "2026-06-28", telegram: true },
    { id: "AN-1006", scope: "school", title: "School Closed — Royal Ploughing Day", body: "NGIS will be closed on Monday, 1 July 2026. Normal schedule resumes Tuesday, 2 July.", audience: "All campuses · All grades", priority: "normal", pinned: false, status: "published", reads: 990, total: 1240, author: "Administration Office", authorRole: "School Administration", date: "2026-06-26", telegram: true },
    { id: "AN-1007", scope: "campus", title: "Depo Campus — Canteen Menu Update", body: "Updated canteen menu effective 7 July. allergen information available at the canteen desk.", audience: "Depo Campus · All grades", priority: "info", pinned: false, status: "scheduled", reads: 0, total: 310, author: "Keo Pich", authorRole: "Campus Admin", date: "2026-07-05", telegram: false },
    { id: "AN-1008", scope: "school", title: "Draft: Annual Sports Day Registration", body: "Draft — register with your PE teacher before 2 July. Prize ceremony at 4 PM.", audience: "All campuses · Grades 7–12", priority: "normal", pinned: false, status: "draft", reads: 0, total: 0, author: "Mr. Phearith Kong", authorRole: "Physical Education", date: "2026-06-25", telegram: false }
  ];

  /* ── Direct / group conversation index (for dashboard + archived + pinned) ── */
  var CONVERSATIONS = [
    { id: "conv-1", type: "direct", name: "Dr. Sarah Jenkins", sub: "Mathematics Teacher", lastMsg: "Quiz results are on the portal — great improvement!", time: "2m", unread: 2, pinned: true, archived: false, muted: false, status: "online", initials: "SJ", color: "#16a34a" },
    { id: "conv-2", type: "direct", name: "Mr. Sophea", sub: "Physics Teacher", lastMsg: "Force is always perpendicular to the magnetic field.", time: "26m", unread: 1, pinned: true, archived: false, muted: false, status: "online", initials: "SP", color: "#0891b2" },
    { id: "conv-3", type: "direct", name: "Heng Samnang", sub: "Super Administrator", lastMsg: "Your schedule change has been confirmed.", time: "1h", unread: 0, pinned: false, archived: false, muted: true, status: "online", initials: "HS", color: "#d97706" },
    { id: "conv-4", type: "direct", name: "Ratha Sok", sub: "Student · Grade 10A", lastMsg: "Can you share the notes from today?", time: "3h", unread: 0, pinned: false, archived: false, muted: false, status: "online", initials: "RS", color: "#2563eb" },
    { id: "conv-5", type: "direct", name: "Mrs. Neary", sub: "English Teacher", lastMsg: "Please revise Chapters 3 and 4 of the guidebook.", time: "Yesterday", unread: 0, pinned: false, archived: false, muted: false, status: "offline", initials: "NE", color: "#db2777" },
    { id: "conv-6", type: "group", name: "Grade 10A Study Group", sub: "12 members · You created it", lastMsg: "Ly Channary: Who has the chemistry formula sheet?", time: "4h", unread: 5, pinned: false, archived: false, muted: false, status: null, initials: "GS", color: "#7c3aed" },
    { id: "conv-7", type: "group", name: "Science Club", sub: "34 members · Dr. Kosal Vann", lastMsg: "Dr. Kosal Vann: Olympiad practice moved to Room 310", time: "Yesterday", unread: 0, pinned: false, archived: false, muted: true, status: null, initials: "SC", color: "#0e7490" },
    { id: "conv-8", type: "direct", name: "Ms. Kiry Sokha", sub: "Biology Teacher", lastMsg: "Good job on the lab report! You scored 88%.", time: "2d", unread: 0, pinned: false, archived: true, muted: false, status: "away", initials: "KS", color: "#7c3aed" },
    { id: "conv-9", type: "direct", name: "IT Support", sub: "IT Department", lastMsg: "Your account issue has been resolved.", time: "4d", unread: 0, pinned: false, archived: true, muted: false, status: "offline", initials: "IT", color: "#475569" },
    { id: "conv-10", type: "group", name: "Football Team 2026", sub: "18 members · Mr. Phearith Kong", lastMsg: "Mr. Phearith Kong: Training cancelled on Thursday", time: "5d", unread: 0, pinned: false, archived: true, muted: false, status: null, initials: "FT", color: "#b45309" }
  ];

  /* ── Message requests (restricted contacts awaiting approval) ── */
  var REQUESTS = [
    { id: "RQ-1", from: "Kevin Jenkins", fromRole: "Student · Grade 8A", fromInit: "KJ", fromColor: "#ea580c", campus: "Depo", preview: "Hi! I have a question about the science fair — can Grade 8 students join?", time: "18m", status: "pending", mutual: "none", note: "Not in your classes or department" },
    { id: "RQ-2", from: "Chan Dara Vuth", fromRole: "Parent / Guardian", fromInit: "CV", fromColor: "#b45309", campus: "Sen Sok", preview: "Hello, regarding my child's math placement for next term…", time: "2h", status: "pending", mutual: "child", note: "Guardian of a student you teach" },
    { id: "RQ-3", from: "Sreyleak Pov", fromRole: "Student · Grade 11B", fromInit: "SP", fromColor: "#94a3b8", campus: "Sen Sok", preview: "Do you still have the old exam papers from last year?", time: "1d", status: "pending", mutual: "none", note: "Not in your classes or department" },
    { id: "RQ-4", from: "Mrs. Tep Vanny", fromRole: "Dept Principal · English", fromInit: "TV", fromColor: "#b91c1c", campus: "Depo", preview: "Please review the department channel posting policy.", time: "2d", status: "approved", mutual: "school", note: "School administration scope" },
    { id: "RQ-5", from: "Panha Heng", fromRole: "Student · Grade 12A", fromInit: "PH", fromColor: "#94a3b8", campus: "Bak Touk", preview: "Can someone from the math department help with vectors?", time: "3d", status: "declined", mutual: "none", note: "Not in your classes or department" }
  ];

  /* ── Pinned messages (across conversations) ── */
  var PINNED = [
    { id: "PN-1", conv: "Dr. Sarah Jenkins", convType: "direct", sender: "Dr. Sarah Jenkins", senderInit: "SJ", senderColor: "#16a34a", text: "Semester 2 final exam: Monday 14 July, 8:00 AM, Hall 2. Bring your student ID and calculator.", date: "2026-06-28", pinnedBy: "You", type: "text" },
    { id: "PN-2", conv: "Class 10A", convType: "class", sender: "Mr. Sophea", senderInit: "SP", senderColor: "#0891b2", text: "Physics practical — Room 204 this week. Wear lab coats and closed shoes.", date: "2026-06-27", pinnedBy: "Mr. Sophea", type: "text", attachment: { name: "Lab Safety Checklist.pdf", size: "84 KB" } },
    { id: "PN-3", conv: "Grade 10A Study Group", convType: "group", sender: "Ly Channary", senderInit: "LC", senderColor: "#16a34a", text: "Shared folder: Semester 2 notes — chemistry formula sheet included.", date: "2026-06-25", pinnedBy: "You", type: "link", attachment: { name: "Chemistry Formula Sheet.pdf", size: "212 KB" } },
    { id: "PN-4", conv: "Science Department", convType: "channel", sender: "Dr. Kosal Vann", senderInit: "KV", senderColor: "#0f766e", text: "Lab safety refresher is mandatory for all science students on Monday 7 July.", date: "2026-06-24", pinnedBy: "Dr. Kosal Vann", type: "text" }
  ];

  /* ── Saved messages ── */
  var SAVED = [
    { id: "SV-1", type: "text", from: "Dr. Sarah Jenkins", text: "Integration by parts — remember the LIATE rule when choosing u and dv.", date: "2026-06-28", conv: "Direct message" },
    { id: "SV-2", type: "file", from: "Mr. Sophea", text: "Chapter 6 slides — electromagnetism diagrams", date: "2026-06-27", conv: "Direct message", attachment: { name: "Physics Ch6 Slides.pdf", size: "1.2 MB" } },
    { id: "SV-3", type: "text", from: "Class 10A", text: "Room change: Physics practical moves to Lab 2 (Room 204) this week.", date: "2026-06-27", conv: "Class 10A" },
    { id: "SV-4", type: "file", from: "Science Club", text: "Olympiad past papers 2022–2025", date: "2026-06-22", conv: "Science Club", attachment: { name: "Olympiad Past Papers.zip", size: "4.8 MB" } },
    { id: "SV-5", type: "link", from: "Heng Samnang", text: "Student handbook 2025-26 — https://ngis.edu.kh/handbook", date: "2026-06-20", conv: "Direct message" }
  ];

  /* ── Attachments & shared files ── */
  var ATTACHMENTS = [
    { id: "AT-1", name: "Semester 2 Exam Timetable 2025-26.pdf", type: "pdf", size: "248 KB", from: "Dr. Sarah Jenkins", conv: "Direct message", date: "2026-06-28" },
    { id: "AT-2", name: "Physics Ch6 Slides.pdf", type: "pdf", size: "1.2 MB", from: "Mr. Sophea", conv: "Direct message", date: "2026-06-27" },
    { id: "AT-3", name: "Lab Safety Checklist.pdf", type: "pdf", size: "84 KB", from: "Mr. Sophea", conv: "Class 10A", date: "2026-06-27" },
    { id: "AT-4", name: "Chemistry Formula Sheet.pdf", type: "pdf", size: "212 KB", from: "Ly Channary", conv: "Grade 10A Study Group", date: "2026-06-25" },
    { id: "AT-5", name: "Science Fair Guidelines.pdf", type: "pdf", size: "185 KB", from: "Dr. Kosal Vann", conv: "Science Department", date: "2026-06-21" },
    { id: "AT-6", name: "Sports Day Event List.pdf", type: "pdf", size: "156 KB", from: "Mr. Phearith Kong", conv: "School Announcements", date: "2026-06-25" },
    { id: "AT-7", name: "Olympiad Past Papers.zip", type: "archive", size: "4.8 MB", from: "Dr. Kosal Vann", conv: "Science Club", date: "2026-06-22" },
    { id: "AT-8", name: "Field Trip Permission Form.docx", type: "doc", size: "64 KB", from: "Ms. Kiry Sokha", conv: "Class 10B", date: "2026-06-24" },
    { id: "AT-9", name: "Group Photo — Science Club.jpg", type: "image", size: "2.1 MB", from: "Ratha Sok", conv: "Science Club", date: "2026-06-18" },
    { id: "AT-10", name: "Oral Exam Rubric S2 2026.pdf", type: "pdf", size: "120 KB", from: "Mrs. Neary", conv: "English Department", date: "2026-06-28" },
    { id: "AT-11", name: "Math Practice Set 4.pdf", type: "pdf", size: "98 KB", from: "Mr. Oudom", conv: "Direct message", date: "2026-06-26" },
    { id: "AT-12", name: "Chinese Writing Assignment 4.pdf", type: "pdf", size: "98 KB", from: "Mr. Heng Samnang", conv: "Chinese Department", date: "2026-06-27" }
  ];

  /* ── Message search index (unified discovery) ── */
  var SEARCH_INDEX = [
    { id: "SR-1", type: "message", sender: "Dr. Sarah Jenkins", conv: "Direct message", convType: "direct", text: "Semester 2 final exam: Monday 14 July, 8:00 AM, Hall 2.", date: "2026-06-28", campus: "Sen Sok", dept: "Mathematics", classId: "10A", hasAttachment: false },
    { id: "SR-2", type: "message", sender: "Mr. Sophea", conv: "Class 10A", convType: "class", text: "Physics practical moves to Lab 2 (Room 204) this week.", date: "2026-06-27", campus: "Sen Sok", dept: "Science", classId: "10A", hasAttachment: true },
    { id: "SR-3", type: "announcement", sender: "Administration Office", conv: "School Announcements", convType: "announcement", text: "Semester 2 Final Examination Timetable — exams run 14–25 July 2026.", date: "2026-06-20", campus: "All campuses", dept: "—", classId: "—", hasAttachment: true },
    { id: "SR-4", type: "message", sender: "Ly Channary", conv: "Grade 10A Study Group", convType: "group", text: "Who has the chemistry formula sheet? Shared the updated one here.", date: "2026-06-25", campus: "Sen Sok", dept: "Science", classId: "10A", hasAttachment: true },
    { id: "SR-5", type: "message", sender: "Dr. Kosal Vann", conv: "Science Department", convType: "channel", text: "Science Fair registration closes 5 July — submit proposals to homeroom teachers.", date: "2026-06-21", campus: "All campuses", dept: "Science", classId: "—", hasAttachment: false },
    { id: "SR-6", type: "file", sender: "Mr. Sophea", conv: "Direct message", convType: "direct", text: "Physics Ch6 Slides.pdf (1.2 MB) — electromagnetism diagrams.", date: "2026-06-27", campus: "Sen Sok", dept: "Science", classId: "10A", hasAttachment: true },
    { id: "SR-7", type: "message", sender: "Mr. Oudom", conv: "Class 11A", convType: "class", text: "Study group at lunch tomorrow — bring your calculus questions.", date: "2026-06-26", campus: "Sen Sok", dept: "Mathematics", classId: "11A", hasAttachment: false },
    { id: "SR-8", type: "announcement", sender: "Keo Pich", conv: "Campus Announcements", convType: "announcement", text: "Sen Sok Campus — Fire drill for all students and staff at 9:00 AM on 9 July.", date: "2026-06-24", campus: "Sen Sok", dept: "—", classId: "—", hasAttachment: false },
    { id: "SR-9", type: "message", sender: "Mrs. Neary", conv: "English Department", convType: "channel", text: "Oral exam rubric updated for Semester 2 — closed-book format.", date: "2026-06-28", campus: "All campuses", dept: "English", classId: "—", hasAttachment: true },
    { id: "SR-10", type: "message", sender: "Ratha Sok", conv: "Grade 10A Study Group", convType: "group", text: "Can someone explain question 3b from exercise 5.3?", date: "2026-06-26", campus: "Sen Sok", dept: "Science", classId: "10A", hasAttachment: false }
  ];

  /* ── Notification preferences categories ── */
  var NOTIF_CATEGORIES = [
    { key: "dm", label: "Direct messages", desc: "New one-to-one messages from eligible users", inApp: true, telegram: true, push: true },
    { key: "group", label: "Group chat messages", desc: "Messages in groups you created or joined", inApp: true, telegram: false, push: true },
    { key: "class_ann", label: "Class announcements", desc: "Teacher announcements in your class chats", inApp: true, telegram: true, push: true },
    { key: "school_ann", label: "School announcements", desc: "Whole-school and campus-wide notices", inApp: true, telegram: true, push: true },
    { key: "invite", label: "Group invitations", desc: "When someone invites you to a group", inApp: true, telegram: false, push: true },
    { key: "mention", label: "Mentions & replies", desc: "When someone mentions or replies to you", inApp: true, telegram: true, push: true },
    { key: "request", label: "Message requests", desc: "New requests from restricted contacts", inApp: true, telegram: false, push: false },
    { key: "file", label: "File shared", desc: "When a file is shared with you", inApp: true, telegram: false, push: false },
    { key: "important", label: "Important announcements", desc: "Urgent school notices marked important", inApp: true, telegram: true, push: true },
    { key: "deadline", label: "Assignment deadlines", desc: "Reminders before assignment due dates", inApp: true, telegram: true, push: true },
    { key: "exam", label: "Examination schedules", desc: "Exam timetable changes and reminders", inApp: true, telegram: true, push: true },
    { key: "timetable", label: "Timetable changes", desc: "Class or room schedule changes", inApp: true, telegram: true, push: true },
    { key: "services", label: "Student Services updates", desc: "Status changes on your service requests", inApp: true, telegram: false, push: true },
    { key: "tasks", label: "Assigned tasks", desc: "Staff-only: tasks assigned to you", inApp: true, telegram: false, push: true }
  ];

  /* ── Telegram integration state (demo — not operational until configured) ── */
  var TELEGRAM = {
    botName: "NGIS Notify Bot",
    botUser: "@NGIS_NotifyBot",
    configured: true,
    health: "operational",
    latency: "24 ms",
    linked: true,
    linkedUser: "Nrinphouneta Hok",
    chatId: "583920144",
    linkedAt: "2026-06-18 10:42",
    rateLimit: { max: 30, window: "per second", used: 7 },
    destinations: [
      { id: "TG-1", name: "School Announcements", type: "channel", target: "@NGIS_Announcements", scope: "All campuses", active: true },
      { id: "TG-2", name: "Sen Sok Campus", type: "group", target: "t.me/ngis_sensok", scope: "Sen Sok Campus", active: true },
      { id: "TG-3", name: "Depo Campus", type: "group", target: "t.me/ngis_depo", scope: "Depo Campus", active: true },
      { id: "TG-4", name: "Science Department", type: "group", target: "t.me/ngis_science", scope: "Science Dept", active: true },
      { id: "TG-5", name: "Mathematics Department", type: "group", target: "t.me/ngis_math", scope: "Mathematics Dept", active: false },
      { id: "TG-6", name: "Parents Broadcast", type: "channel", target: "@NGIS_Parents", scope: "Parents · All campuses", active: true }
    ],
    deliveries: [
      { id: "DL-9001", ts: "2026-06-28 09:14:22", category: "School announcement", target: "@NGIS_Announcements", status: "delivered", attempts: 1, detail: "Semester 2 Final Examination Timetable" },
      { id: "DL-9002", ts: "2026-06-28 08:31:07", category: "Class announcement", target: "583920144", status: "delivered", attempts: 1, detail: "Room change: Physics practical" },
      { id: "DL-9003", ts: "2026-06-28 08:02:44", category: "Direct message", target: "612044837", status: "failed", attempts: 3, detail: "User has not started the bot — queued for retry" },
      { id: "DL-9004", ts: "2026-06-27 16:20:11", category: "Exam schedule", target: "@NGIS_Announcements", status: "delivered", attempts: 1, detail: "Semester 2 exam timetable" },
      { id: "DL-9005", ts: "2026-06-27 14:45:30", category: "Group message", target: "t.me/ngis_science", status: "delivered", attempts: 1, detail: "Lab safety refresher notice" },
      { id: "DL-9006", ts: "2026-06-27 11:12:58", category: "Timetable change", target: "583920144", status: "retrying", attempts: 2, detail: "Room change — retry scheduled in 15 min" },
      { id: "DL-9007", ts: "2026-06-27 09:05:12", category: "Assignment deadline", target: "612044837", status: "delivered", attempts: 1, detail: "Algebra homework 4 due Friday" }
    ]
  };

  /* ── Messaging audit events ── */
  var AUDIT_EVENTS = [
    { id: "AU-90001", ts: "2026-06-28 09:41:10", actor: "Nrinphouneta Hok", actorRole: "Student", action: "message.sent", resource: "Direct message · Dr. Sarah Jenkins", detail: "Text message (142 chars)", ip: "10.20.4.18", result: "success" },
    { id: "AU-90002", ts: "2026-06-28 09:32:55", actor: "Dr. Sarah Jenkins", actorRole: "Teacher", action: "announcement.published", resource: "Class 10A announcement", detail: "Quiz results published to Class 10A (28 recipients)", ip: "10.20.4.7", result: "success" },
    { id: "AU-90003", ts: "2026-06-28 09:18:02", actor: "Ratha Sok", actorRole: "Student", action: "message.reported", resource: "Grade 10A Study Group", detail: "Reported message for inappropriate content", ip: "10.20.4.31", result: "pending_review" },
    { id: "AU-90004", ts: "2026-06-28 08:47:33", actor: "Heng Samnang", actorRole: "Super Admin", action: "telegram.destination.updated", resource: "@NGIS_Announcements", detail: "Enabled school announcement delivery", ip: "10.20.1.2", result: "success" },
    { id: "AU-90005", ts: "2026-06-28 08:31:07", actor: "System", actorRole: "Messaging Service", action: "telegram.delivered", resource: "583920144", detail: "Class announcement delivered to linked account", ip: "—", result: "success" },
    { id: "AU-90006", ts: "2026-06-28 08:02:44", actor: "System", actorRole: "Messaging Service", action: "telegram.failed", resource: "612044837", detail: "Delivery failed after 3 attempts — user has not started bot", ip: "—", result: "failed" },
    { id: "AU-90007", ts: "2026-06-27 17:12:40", actor: "Mr. Sophea", actorRole: "Teacher", action: "file.shared", resource: "Class 10A", detail: "Lab Safety Checklist.pdf (84 KB) — type validated", ip: "10.20.4.9", result: "success" },
    { id: "AU-90008", ts: "2026-06-27 16:55:03", actor: "Heng Samnang", actorRole: "Super Admin", action: "moderation.message_hidden", resource: "Grade 10A Study Group", detail: "Message hidden pending review — spam policy 4.2", ip: "10.20.1.2", result: "success" },
    { id: "AU-90009", ts: "2026-06-27 15:20:19", actor: "Ly Channary", actorRole: "Student", action: "group.created", resource: "Grade 10A Study Group", detail: "Student-created group — 12 eligible members invited", ip: "10.20.4.22", result: "success" },
    { id: "AU-90010", ts: "2026-06-27 14:08:51", actor: "Ms. Kiry Sokha", actorRole: "Teacher", action: "conversation.archived", resource: "Direct message · Ratha Sok", detail: "Conversation archived by teacher", ip: "10.20.4.11", result: "success" },
    { id: "AU-90011", ts: "2026-06-27 11:44:27", actor: "System", actorRole: "Messaging Service", action: "attachment.blocked", resource: "Class 10B", detail: "Blocked upload setup.exe — executable files are not permitted", ip: "—", result: "blocked" },
    { id: "AU-90012", ts: "2026-06-27 10:02:36", actor: "Heng Samnang", actorRole: "Super Admin", action: "retention.policy.updated", resource: "Messaging retention", detail: "Direct messages retained 365 days, then auto-archived", ip: "10.20.1.2", result: "success" }
  ];

  /* ── Reported content (moderation queue) ── */
  var REPORTS = [
    { id: "RP-1", type: "message", reporter: "Ratha Sok", reporterRole: "Student", target: "Vuth Dara", targetRole: "Student · Grade 10A", conv: "Grade 10A Study Group", reason: "Inappropriate content", preview: "Message reported by 2 students — contains off-topic spam link", time: "2026-06-28 09:18", status: "pending", severity: "medium" },
    { id: "RP-2", type: "group", reporter: "Mrs. Neary", reporterRole: "Teacher", target: "Exam Answers 2026", targetRole: "Group", conv: "Group chat", reason: "Suspected cheating", preview: "Group named 'Exam Answers 2026' created by unverified student account", time: "2026-06-28 07:55", status: "pending", severity: "high" },
    { id: "RP-3", type: "message", reporter: "Emily Jenkins", reporterRole: "Student", target: "Unknown user", targetRole: "Restricted contact", conv: "Message request", reason: "Harassment", preview: "Repeated messages after being declined — auto-blocked by policy", time: "2026-06-27 18:30", status: "resolved", severity: "high" }
  ];

  /* ── Export ── */
  window.MSG = {
    role: ROLE,
    me: ME[ROLE] || ME.student,
    can: can,
    directory: DIRECTORY,
    campusTree: CAMPUS_TREE,
    channels: CHANNELS,
    announcements: ANNOUNCEMENTS,
    conversations: CONVERSATIONS,
    requests: REQUESTS,
    pinned: PINNED,
    saved: SAVED,
    attachments: ATTACHMENTS,
    searchIndex: SEARCH_INDEX,
    notifCategories: NOTIF_CATEGORIES,
    telegram: TELEGRAM,
    audit: AUDIT_EVENTS,
    reports: REPORTS
  };
})();
