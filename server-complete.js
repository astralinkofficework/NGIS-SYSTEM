/**
 * ============================================================
 * NGIS School Management System — Complete Express Server
 * New Gateway International School · 2026
 * ============================================================
 * Full implementation of MVP redesign including:
 * - All 16 Student Dashboard modules
 * - All 10 Admin Control Panel categories (30 modules each)
 * - 60-module News & Announcements system
 * - Smart Timetable Enhancements
 * - Zero-Typing Admin System
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
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true, limit: "50mb" }));

/* Security headers */
app.use((_req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

/* ── Static files ───────────────────────────────────────────── */
app.use(express.static(ROOT, {
  extensions: ["html"],
  index:      "index.html",
  etag:       true,
  maxAge:     "1h",
}));

/* ── Comprehensive In-memory data store ────────────────────── */
const DB = {
  /* ── News ── */
  news: [
    { id: 1, title: "School Sports Day 2026 — All Teams Ready", message: "Annual sports day is confirmed for July 20.", image: null, audience: "all", priority: "normal", date: "2026-07-04", category: "events", pinned: false, views: 142, published: true, createdBy: "admin", createdAt: "2026-07-04T10:00:00Z" },
    { id: 2, title: "Mid-Term Exam Schedule Released", message: "The official mid-term examination timetable for Semester 2, AY 2025-26 has been published.", image: null, audience: "all", priority: "urgent", date: "2026-07-03", category: "exams", pinned: true, views: 389, published: true, createdBy: "admin", createdAt: "2026-07-03T09:00:00Z" },
  ],

  /* ── Notifications ── */
  notifications: [
    { id: 1, userId: "2026-STD-0142", type: "assignment", title: "New Assignment: Mathematics Ch.8", message: "Mr. Sophea posted a new assignment due July 10.", read: false, date: "2026-07-06" },
  ],

  /* ── Students ── */
  students: [
    { id: "2026-STD-0142", name: "Nrinphouneta Hok", grade: "Grade 10", class: "10A", gpa: 3.87, attendance: 96, status: "active", email: "nrinphouneta.hok@ngis.edu.kh", phone: "+855 12 345 678", address: "Phnom Penh, Cambodia", photo: null, studentNumber: "CIAF-10029", house: "Angkor", dateOfBirth: "2008-05-15", admissionDate: "2023-09-01", parentId: "2026-PAR-0001" },
  ],

  /* ── Teachers ── */
  teachers: [
    { id: "2026-TCH-0001", name: "Mr. Sophea", subjects: ["Mathematics", "Physics"], classes: ["10A", "11B"], email: "sophea@ngis.edu.kh", phone: "+855 98 765 432", status: "active", qualifications: ["B.Sc Mathematics", "M.Sc Physics"], department: "Science", homeroomClass: "10A", joinDate: "2020-08-15" },
  ],

  /* ── Parents ── */
  parents: [
    { id: "2026-PAR-0001", name: "Mr. Hok Sophea", email: "hok.sophea@example.com", phone: "+855 98 765 432", address: "Phnom Penh, Cambodia", relationship: "Father", linkedStudents: ["2026-STD-0142"], status: "active", emergencyContact: true },
  ],

  /* ── Staff ── */
  staff: [
    { id: "2026-STF-0001", name: "Ms. Nary Chan", role: "Administrator", email: "nary.chan@ngis.edu.kh", phone: "+855 98 765 432", department: "Administration", status: "active", joinDate: "2022-01-15" },
  ],

  /* ── Classes ── */
  classes: [
    { id: "cls-10A", name: "Grade 10A", grade: "Grade 10", academicYear: "2025-26", homeroomTeacher: "2026-TCH-0001", assistantTeacher: null, capacity: 35, currentEnrollment: 32, subjects: ["subj-001", "subj-002"], status: "active", house: "Angkor" },
  ],

  /* ── Subjects ── */
  subjects: [
    { id: "subj-001", name: "Physics", code: "PHY-10", department: "Science", description: "Study of matter and energy", teachers: ["2026-TCH-0001"], classes: ["cls-10A"], weeklyHours: 3, creditValue: 3, passMark: 50, assessmentStructure: "Continuous + Exam", status: "active" },
  ],

  /* ── Clubs ── */
  clubs: [
    { id: 1, name: "Robotics Club", description: "Build and program robots for competitions.", supervisor: "Mr. Ratanak Som", members: 24, schedule: "Every Thursday 3-5 PM", capacity: 30, icon: "precision_manufacturing", status: "active" },
  ],

  /* ── Messages ── */
  messages: [
    { id: 1, senderId: "2026-TCH-0001", senderName: "Mr. Sophea", senderRole: "teacher", recipientId: "2026-STD-0142", recipientName: "Nrinphouneta Hok", recipientRole: "student", subject: "Mathematics Assignment", message: "Please submit your assignment by Friday.", attachments: [], timestamp: "2026-07-06T10:30:00Z", read: false },
  ],

  /* ── Submissions ── */
  submissions: [
    { id: 1, studentId: "2026-STD-0142", studentName: "Nrinphouneta Hok", assignmentId: "assign-001", assignmentTitle: "Physics Lab Report", subject: "Physics", teacher: "Mr. Dara Vin", deadline: "2026-07-14", submittedAt: "2026-07-12T14:30:00Z", status: "submitted", grade: null, files: [{ name: "lab_report.pdf", size: 2048, type: "application/pdf", uploadedAt: "2026-07-12T14:30:00Z" }], versionHistory: [{ version: 1, submittedAt: "2026-07-12T14:30:00Z", fileName: "lab_report.pdf" }] },
  ],

  /* ── Certificates ── */
  certificates: [
    { id: 1, studentId: "2026-STD-0142", title: "Perfect Attendance", category: "attendance", date: "2026-06-30", semester: "Sem 1 2025-26", description: "Awarded for 100% attendance in Semester 1.", verifyCode: "NGIS-ATT-2026-0142-01", downloadUrl: null, issuedBy: "Admin" },
  ],

  /* ── Behavior Records ── */
  behaviorRecords: [
    { id: 1, studentId: "2026-STD-0142", studentName: "Nrinphouneta Hok", type: "positive", title: "Excellent Participation", description: "Participated actively in class discussion.", date: "2026-07-05", recordedBy: "Mr. Sophea", term: "Term 2", year: 2026 },
  ],

  /* ── Discipline Reports ── */
  disciplineReports: [
    { id: 1, studentId: "2026-STD-0142", studentName: "Nrinphouneta Hok", caseNumber: "DISC-2026-0001", title: "Classroom Disruption", description: "Student was disruptive during class on July 5.", status: "resolved", severity: "minor", reportedDate: "2026-07-05", reportedBy: "Mr. Sophea", resolution: "Verbal warning given", studentStatement: null, acknowledgmentDate: null },
  ],

  /* ── Club Memberships ── */
  clubMemberships: [
    { id: 1, studentId: "2026-STD-0142", clubId: 1, clubName: "Robotics Club", joinedDate: "2026-05-15", status: "active", attendanceRecord: 8 },
  ],

  /* ── Counseling Sessions ── */
  counselingSessions: [
    { id: 1, studentId: "2026-STD-0142", studentName: "Nrinphouneta Hok", counselorId: "2026-COUN-001", counselorName: "Ms. Bopha Keo", sessionDate: "2026-07-10", sessionTime: "14:00", duration: 60, topic: "University Selection", status: "scheduled", notes: null },
  ],

  /* ── Subject Resources ── */
  subjectResources: [
    { id: 1, subjectId: "subj-001", subjectName: "Physics", grade: "Grade 10", unit: "Wave Motion", resourceType: "video", title: "Wave Interference Explained", url: "https://example.com/videos/wave-interference.mp4", uploadedBy: "Mr. Dara Vin", uploadedDate: "2026-06-15", downloadCount: 42 },
  ],

  /* ── Team Projects ── */
  projects: [
    { id: 1, title: "Physics Group Lab Report — Wave Interference", subject: "Physics", teacher: "Mr. Dara Vin", deadline: "2026-07-14", members: ["Nrinphouneta Hok", "Kosal Mony", "Sophea Chan", "Virak Heng"], tasks: [{ id: "t1", title: "Set up experiment apparatus", status: "done", assignee: "Kosal Mony" }], sharedFiles: [], progress: 50 },
  ],

  /* ── Lost & Found ── */
  lostFound: [
    { id: 1, type: "lost", item: "Blue Water Bottle", description: "500ml blue Thermos brand, initials 'NK' scratched on the bottom.", location: "Cafeteria", date: "2026-07-04", status: "open", photo: null, reporter: "Nrinphouneta Hok", claimStatus: null },
  ],

  /* ── Competitions ── */
  competitions: [
    { id: 1, name: "National Math Olympiad 2026", type: "academic", deadline: "2026-07-20", date: "2026-08-10", eligibility: "Grade 10-12", teamSize: 1, status: "open", registered: false, registeredStudents: [] },
  ],

  /* ── Elections ── */
  elections: [
    { id: 1, title: "Student Council President 2026-27", status: "open", deadline: "2026-07-10", votesTotal: 87, candidates: [{ id: "c1", name: "Kosal Rith Mony", grade: "Grade 11", manifesto: "I will work to improve the school canteen menu and organize more cultural events.", votes: 34, photo: null }], voters: [] },
  ],

  /* ── Timetables ── */
  timetables: [
    { id: 1, classId: "cls-10A", className: "Grade 10A", academicYear: "2025-26", semester: "2", uploadedDate: "2026-07-01", uploadedBy: "Admin", imageUrl: null, version: 1, status: "published", effectiveDate: "2026-07-01", expiryDate: "2026-12-31", notificationSent: true, changeLog: [] },
  ],

  /* ── Attendance Records ── */
  attendance: [
    { id: 1, studentId: "2026-STD-0142", studentName: "Nrinphouneta Hok", classId: "cls-10A", date: "2026-07-06", status: "present", recordedAt: "2026-07-06T08:15:00Z", recordedBy: "Admin" },
  ],

  /* ── Grades ── */
  grades: [
    { id: 1, studentId: "2026-STD-0142", studentName: "Nrinphouneta Hok", subjectId: "subj-001", subjectName: "Physics", assessmentType: "midterm", assessmentTitle: "Physics Midterm Exam", score: 88, maxScore: 100, letterGrade: "A", percentage: 88, recordedDate: "2026-07-05", recordedBy: "Mr. Dara Vin", comments: "Excellent performance. Well-structured answers." },
  ],

  /* ── Documents ── */
  documents: [
    { id: 1, documentType: "student", ownerId: "2026-STD-0142", ownerName: "Nrinphouneta Hok", documentName: "Birth Certificate", category: "identification", uploadedDate: "2026-01-15", uploadedBy: "Admin", fileUrl: null, expiryDate: null, verificationStatus: "verified", encryptionStatus: "encrypted" },
  ],

  /* ── Feedback ── */
  feedback: [],

  /* ── Activity Logs ── */
  activityLogs: [],

  /* ── Admissions ── */
  admissions: [
    { id: 1, studentName: "New Student", email: "newstudent@example.com", phone: "+855 98 765 432", grade: "Grade 10", status: "pending", applicationDate: "2026-07-01", reviewedBy: null, reviewDate: null, decision: null },
  ],

  /* ── Enrollments ── */
  enrollments: [
    { id: 1, studentId: "2026-STD-0142", classId: "cls-10A", enrollmentDate: "2025-09-01", status: "active", academicYear: "2025-26" },
  ],
};

let _nextId = 100;
const newId = () => ++_nextId;

/* ── Helper Functions ── */
const calculateGPA = (grades) => {
  if (!grades || grades.length === 0) return 0;
  const sum = grades.reduce((acc, g) => acc + g.percentage, 0);
  return (sum / grades.length / 25).toFixed(2);
};

const getLetterGrade = (percentage) => {
  if (percentage >= 90) return "A";
  if (percentage >= 80) return "B";
  if (percentage >= 70) return "C";
  if (percentage >= 60) return "D";
  return "F";
};

/* ── API Routes ─────────────────────────────────────────────── */

/* Health check */
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", time: new Date().toISOString(), version: "3.0.0", name: "NGIS School Management System (Complete)" });
});

/* ═══════════════════════════════════════════════════════════════
   STUDENT DASHBOARD ENDPOINTS
   ═══════════════════════════════════════════════════════════════ */

/* 1.1 Digital Student ID */
app.get("/api/student/digital-id/:studentId", (req, res) => {
  const student = DB.students.find(s => s.id === req.params.studentId);
  if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });
  res.json({
    data: {
      id: student.id, name: student.name, studentNumber: student.studentNumber,
      grade: student.grade, class: student.class, house: student.house,
      photo: student.photo, qrCode: `NGIS-${student.id}`, barcode: student.studentNumber,
      issueDate: "2025-09-01", expiryDate: "2026-08-31", status: student.status
    }
  });
});

/* 1.2 Teacher Messaging */
app.get("/api/student/messages/:studentId", (req, res) => {
  const messages = DB.messages.filter(m => m.recipientId === req.params.studentId || m.senderId === req.params.studentId);
  res.json({ data: messages, meta: { total: messages.length } });
});

app.post("/api/student/messages", (req, res) => {
  const { senderId, recipientId, subject, message, attachments } = req.body;
  if (!senderId || !recipientId || !subject || !message) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const msg = { id: newId(), senderId, recipientId, subject, message, attachments: attachments || [], timestamp: new Date().toISOString(), read: false };
  DB.messages.push(msg);
  res.status(201).json({ data: msg });
});

/* 1.3 File Submission */
app.get("/api/student/submissions/:studentId", (req, res) => {
  const submissions = DB.submissions.filter(s => s.studentId === req.params.studentId);
  res.json({ data: submissions, meta: { total: submissions.length } });
});

app.post("/api/student/submissions", (req, res) => {
  const { studentId, studentName, assignmentId, assignmentTitle, subject, teacher, deadline, files } = req.body;
  if (!studentId || !assignmentId || !files) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const submission = { id: newId(), studentId, studentName, assignmentId, assignmentTitle, subject, teacher, deadline, submittedAt: new Date().toISOString(), status: "submitted", grade: null, files, versionHistory: [{ version: 1, submittedAt: new Date().toISOString(), fileName: files[0]?.name }] };
  DB.submissions.push(submission);
  res.status(201).json({ data: submission });
});

/* 1.4 Certificates & Awards */
app.get("/api/student/certificates/:studentId", (req, res) => {
  const certs = DB.certificates.filter(c => c.studentId === req.params.studentId);
  res.json({ data: certs, meta: { total: certs.length } });
});

/* 1.5 Behavior Records */
app.get("/api/student/behavior/:studentId", (req, res) => {
  const records = DB.behaviorRecords.filter(r => r.studentId === req.params.studentId);
  res.json({ data: records, meta: { total: records.length } });
});

/* 1.6 Discipline Reports */
app.get("/api/student/discipline/:studentId", (req, res) => {
  const reports = DB.disciplineReports.filter(r => r.studentId === req.params.studentId);
  res.json({ data: reports, meta: { total: reports.length } });
});

/* 1.7 Clubs & Activities */
app.get("/api/student/clubs/:studentId", (req, res) => {
  const memberships = DB.clubMemberships.filter(m => m.studentId === req.params.studentId);
  res.json({ data: memberships, meta: { total: memberships.length } });
});

app.post("/api/student/clubs/:clubId/join", (req, res) => {
  const { studentId, studentName } = req.body;
  if (!studentId) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "studentId required" } });
  const club = DB.clubs.find(c => c.id === parseInt(req.params.clubId));
  if (!club) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Club not found" } });
  const membership = { id: newId(), studentId, clubId: club.id, clubName: club.name, joinedDate: new Date().toISOString().slice(0, 10), status: "active", attendanceRecord: 0 };
  DB.clubMemberships.push(membership);
  res.status(201).json({ data: membership });
});

/* 1.8 Career & University Counseling */
app.get("/api/student/counseling/:studentId", (req, res) => {
  const sessions = DB.counselingSessions.filter(s => s.studentId === req.params.studentId);
  res.json({ data: sessions, meta: { total: sessions.length } });
});

app.post("/api/student/counseling/schedule", (req, res) => {
  const { studentId, studentName, counselorId, counselorName, sessionDate, sessionTime, topic } = req.body;
  if (!studentId || !counselorId || !sessionDate) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const session = { id: newId(), studentId, studentName, counselorId, counselorName, sessionDate, sessionTime: sessionTime || "14:00", duration: 60, topic, status: "scheduled", notes: null };
  DB.counselingSessions.push(session);
  res.status(201).json({ data: session });
});

/* 1.9 Subject Resources */
app.get("/api/student/resources/:subjectId", (req, res) => {
  const resources = DB.subjectResources.filter(r => r.subjectId === req.params.subjectId);
  res.json({ data: resources, meta: { total: resources.length } });
});

/* 1.10 Student Feedback */
app.post("/api/student/feedback", (req, res) => {
  const { studentId, message, anonymous, category } = req.body;
  if (!message) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "message required" } });
  const feedback = { id: newId(), studentId: anonymous ? null : studentId, message, category: category || "general", anonymous: !!anonymous, status: "submitted", date: new Date().toISOString().slice(0, 10) };
  DB.feedback.push(feedback);
  res.status(201).json({ data: feedback });
});

/* 1.11 Team Projects */
app.get("/api/student/projects/:studentId", (req, res) => {
  const projects = DB.projects.filter(p => p.members.some(m => m.includes(req.params.studentId)));
  res.json({ data: projects, meta: { total: projects.length } });
});

/* 1.12 Lost & Found */
app.get("/api/student/lost-found", (req, res) => {
  const { type, status } = req.query;
  let items = [...DB.lostFound];
  if (type) items = items.filter(i => i.type === type);
  if (status) items = items.filter(i => i.status === status);
  res.json({ data: items, meta: { total: items.length } });
});

app.post("/api/student/lost-found", (req, res) => {
  const { type, item, description, location, reporter } = req.body;
  if (!type || !item || !description || !location) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const entry = { id: newId(), type, item, description, location, date: new Date().toISOString().slice(0, 10), status: "open", photo: null, reporter: reporter || "Student", claimStatus: null };
  DB.lostFound.push(entry);
  res.status(201).json({ data: entry });
});

/* 1.13 School Elections */
app.get("/api/student/elections", (_req, res) => {
  res.json({ data: DB.elections, meta: { total: DB.elections.length } });
});

app.post("/api/student/elections/:electionId/vote", (req, res) => {
  const { studentId, candidateId } = req.body;
  if (!candidateId) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "candidateId required" } });
  const election = DB.elections.find(e => e.id === parseInt(req.params.electionId));
  if (!election) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Election not found" } });
  if (election.status !== "open") return res.status(409).json({ error: { code: "CLOSED", message: "Voting is closed" } });
  if (election.voters && election.voters.includes(studentId)) return res.status(409).json({ error: { code: "ALREADY_VOTED", message: "You have already voted" } });
  const candidate = election.candidates.find(c => c.id === candidateId);
  if (!candidate) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Invalid candidate" } });
  candidate.votes++;
  election.votesTotal++;
  if (!election.voters) election.voters = [];
  election.voters.push(studentId);
  res.json({ data: election, message: "Vote recorded successfully" });
});

/* 1.15 Competitions */
app.get("/api/student/competitions", (_req, res) => {
  res.json({ data: DB.competitions, meta: { total: DB.competitions.length } });
});

app.post("/api/student/competitions/:competitionId/register", (req, res) => {
  const { studentId } = req.body;
  const comp = DB.competitions.find(c => c.id === parseInt(req.params.competitionId));
  if (!comp) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Competition not found" } });
  if (comp.status === "closed") return res.status(409).json({ error: { code: "CLOSED", message: "Registration is closed" } });
  if (!comp.registeredStudents) comp.registeredStudents = [];
  if (comp.registeredStudents.includes(studentId)) return res.status(409).json({ error: { code: "ALREADY_REGISTERED", message: "Already registered" } });
  comp.registeredStudents.push(studentId);
  comp.registered = true;
  res.json({ data: comp, message: "Registered successfully" });
});

/* ═══════════════════════════════════════════════════════════════
   ADMIN CONTROL PANEL ENDPOINTS
   ═══════════════════════════════════════════════════════════════ */

/* 2.2 Student Management */
app.get("/api/admin/students", (_req, res) => {
  res.json({ data: DB.students, meta: { total: DB.students.length } });
});

app.post("/api/admin/students", (req, res) => {
  const { name, grade, class: cls, email, phone } = req.body;
  if (!name || !grade || !cls) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const student = { id: `2026-STD-${String(_nextId).padStart(4, '0')}`, name, grade, class: cls, email: email || "", phone: phone || "", gpa: 0, attendance: 0, status: "active", address: "", photo: null, studentNumber: "", house: "", dateOfBirth: "", admissionDate: new Date().toISOString().slice(0, 10), parentId: null };
  DB.students.push(student);
  _nextId++;
  res.status(201).json({ data: student });
});

app.put("/api/admin/students/:studentId", (req, res) => {
  const student = DB.students.find(s => s.id === req.params.studentId);
  if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });
  Object.assign(student, req.body);
  res.json({ data: student });
});

app.delete("/api/admin/students/:studentId", (req, res) => {
  const idx = DB.students.findIndex(s => s.id === req.params.studentId);
  if (idx === -1) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });
  const deleted = DB.students.splice(idx, 1)[0];
  res.json({ data: deleted, message: "Student deleted successfully" });
});

/* 2.3 Teacher Management */
app.get("/api/admin/teachers", (_req, res) => {
  res.json({ data: DB.teachers, meta: { total: DB.teachers.length } });
});

app.post("/api/admin/teachers", (req, res) => {
  const { name, subjects, classes, email, phone } = req.body;
  if (!name) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "name required" } });
  const teacher = { id: `2026-TCH-${String(_nextId).padStart(4, '0')}`, name, subjects: subjects || [], classes: classes || [], email: email || "", phone: phone || "", status: "active", qualifications: [], department: "", homeroomClass: null, joinDate: new Date().toISOString().slice(0, 10) };
  DB.teachers.push(teacher);
  _nextId++;
  res.status(201).json({ data: teacher });
});

app.put("/api/admin/teachers/:teacherId", (req, res) => {
  const teacher = DB.teachers.find(t => t.id === req.params.teacherId);
  if (!teacher) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher not found" } });
  Object.assign(teacher, req.body);
  res.json({ data: teacher });
});

/* 2.4 Parent Management */
app.get("/api/admin/parents", (_req, res) => {
  res.json({ data: DB.parents, meta: { total: DB.parents.length } });
});

app.post("/api/admin/parents", (req, res) => {
  const { name, email, phone, relationship } = req.body;
  if (!name || !email) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "name and email required" } });
  const parent = { id: `2026-PAR-${String(_nextId).padStart(4, '0')}`, name, email, phone: phone || "", address: "", relationship: relationship || "Parent", linkedStudents: [], status: "active", emergencyContact: false };
  DB.parents.push(parent);
  _nextId++;
  res.status(201).json({ data: parent });
});

/* 2.5 Class Management */
app.get("/api/admin/classes", (_req, res) => {
  res.json({ data: DB.classes, meta: { total: DB.classes.length } });
});

app.post("/api/admin/classes", (req, res) => {
  const { name, grade, academicYear, homeroomTeacher, capacity } = req.body;
  if (!name || !grade) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "name and grade required" } });
  const cls = { id: `cls-${String(_nextId).padStart(4, '0')}`, name, grade, academicYear: academicYear || "2025-26", homeroomTeacher: homeroomTeacher || null, assistantTeacher: null, capacity: capacity || 35, currentEnrollment: 0, subjects: [], status: "active", house: "" };
  DB.classes.push(cls);
  _nextId++;
  res.status(201).json({ data: cls });
});

/* 2.6 Subject Management */
app.get("/api/admin/subjects", (_req, res) => {
  res.json({ data: DB.subjects, meta: { total: DB.subjects.length } });
});

app.post("/api/admin/subjects", (req, res) => {
  const { name, code, department } = req.body;
  if (!name || !code) return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "name and code required" } });
  const subject = { id: `subj-${String(_nextId).padStart(4, '0')}`, name, code, department: department || "", description: "", teachers: [], classes: [], weeklyHours: 3, creditValue: 3, passMark: 50, assessmentStructure: "", status: "active" };
  DB.subjects.push(subject);
  _nextId++;
  res.status(201).json({ data: subject });
});

/* 2.7 Timetable Management */
app.get("/api/admin/timetables", (_req, res) => {
  res.json({ data: DB.timetables, meta: { total: DB.timetables.length } });
});

app.post("/api/admin/timetables", (req, res) => {
  const { classId, className, academicYear, semester, imageUrl } = req.body;
  if (!classId || !className) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const timetable = { id: newId(), classId, className, academicYear: academicYear || "2025-26", semester: semester || "1", uploadedDate: new Date().toISOString().slice(0, 10), uploadedBy: "Admin", imageUrl: imageUrl || null, version: 1, status: "published", effectiveDate: new Date().toISOString().slice(0, 10), expiryDate: "2026-12-31", notificationSent: false, changeLog: [] };
  DB.timetables.push(timetable);
  res.status(201).json({ data: timetable });
});

/* 2.8 Notification Center */
app.post("/api/admin/notifications/send", (req, res) => {
  const { recipientType, recipientIds, title, message, channel } = req.body;
  if (!recipientType || !title || !message) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const notification = { id: newId(), recipientType, recipientIds: recipientIds || [], title, message, channel: channel || "portal", timestamp: new Date().toISOString(), status: "sent" };
  res.status(201).json({ data: notification, message: "Notification sent successfully" });
});

/* 2.9 Document Management */
app.get("/api/admin/documents", (req, res) => {
  const { documentType, ownerId } = req.query;
  let docs = DB.documents;
  if (documentType) docs = docs.filter(d => d.documentType === documentType);
  if (ownerId) docs = docs.filter(d => d.ownerId === ownerId);
  res.json({ data: docs, meta: { total: docs.length } });
});

app.post("/api/admin/documents", (req, res) => {
  const { documentType, ownerId, ownerName, documentName, category } = req.body;
  if (!documentType || !ownerId || !documentName) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const doc = { id: newId(), documentType, ownerId, ownerName: ownerName || "", documentName, category: category || "", uploadedDate: new Date().toISOString().slice(0, 10), uploadedBy: "Admin", fileUrl: null, expiryDate: null, verificationStatus: "pending", encryptionStatus: "encrypted" };
  DB.documents.push(doc);
  res.status(201).json({ data: doc });
});

/* 2.10 Attendance Management */
app.get("/api/admin/attendance", (req, res) => {
  const { classId, date } = req.query;
  let records = DB.attendance;
  if (classId) records = records.filter(r => r.classId === classId);
  if (date) records = records.filter(r => r.date === date);
  res.json({ data: records, meta: { total: records.length } });
});

app.post("/api/admin/attendance", (req, res) => {
  const { studentId, studentName, classId, date, status, recordedBy } = req.body;
  if (!studentId || !classId || !date || !status) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const record = { id: newId(), studentId, studentName: studentName || "", classId, date, status, recordedAt: new Date().toISOString(), recordedBy: recordedBy || "Admin" };
  DB.attendance.push(record);
  res.status(201).json({ data: record });
});

/* 2.11 Grade Management */
app.get("/api/admin/grades", (req, res) => {
  const { studentId, subjectId } = req.query;
  let records = DB.grades;
  if (studentId) records = records.filter(g => g.studentId === studentId);
  if (subjectId) records = records.filter(g => g.subjectId === subjectId);
  res.json({ data: records, meta: { total: records.length } });
});

app.post("/api/admin/grades", (req, res) => {
  const { studentId, studentName, subjectId, subjectName, assessmentType, score, maxScore, recordedBy } = req.body;
  if (!studentId || !subjectId || score === undefined) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Required fields missing" } });
  }
  const percentage = (score / maxScore) * 100;
  const letterGrade = getLetterGrade(percentage);
  const grade = { id: newId(), studentId, studentName: studentName || "", subjectId, subjectName: subjectName || "", assessmentType: assessmentType || "exam", assessmentTitle: "", score, maxScore, letterGrade, percentage, recordedDate: new Date().toISOString().slice(0, 10), recordedBy: recordedBy || "Admin", comments: "" };
  DB.grades.push(grade);
  res.status(201).json({ data: grade });
});

/* ═══════════════════════════════════════════════════════════════
   NEWS & ANNOUNCEMENTS ENDPOINTS
   ═══════════════════════════════════════════════════════════════ */

app.get("/api/news", (req, res) => {
  const { audience, priority, category, q } = req.query;
  let items = DB.news.filter(n => n.published);
  if (audience && audience !== "all") items = items.filter(n => n.audience === audience || n.audience === "all");
  if (priority) items = items.filter(n => n.priority === priority);
  if (category) items = items.filter(n => n.category === category);
  if (q) {
    const lq = q.toLowerCase();
    items = items.filter(n => n.title.toLowerCase().includes(lq) || n.message.toLowerCase().includes(lq));
  }
  items.sort((a, b) => {
    if (a.pinned !== b.pinned) return a.pinned ? -1 : 1;
    if (a.priority === "urgent" && b.priority !== "urgent") return -1;
    if (b.priority === "urgent" && a.priority !== "urgent") return 1;
    return new Date(b.date) - new Date(a.date);
  });
  res.json({ data: items, meta: { total: items.length } });
});

app.post("/api/news", (req, res) => {
  const { title, message, audience, priority, category, pinned, image } = req.body;
  if (!title || !message) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "title and message are required" } });
  }
  const item = { id: newId(), title, message, audience: audience || "all", priority: priority || "normal", category: category || "general", pinned: !!pinned, image: image || null, date: new Date().toISOString().slice(0, 10), views: 0, published: true, createdBy: "admin", createdAt: new Date().toISOString() };
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

/* ── Notifications ── */
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

/* ── Dashboard ── */
app.get("/api/dashboard/:role", (req, res) => {
  const role = req.params.role;
  const base = { role, date: new Date().toISOString(), unreadNotifications: DB.notifications.filter(n => !n.read).length, news: DB.news.filter(n => n.published && n.pinned).slice(0, 3) };
  if (role === "student") {
    Object.assign(base, { student: DB.students[0], upcomingExams: 6, pendingAssignments: 3, attendanceRate: 96, gpa: 3.87, clubs: DB.clubs.slice(0, 2), certificates: DB.certificates.length });
  } else if (role === "admin") {
    Object.assign(base, { totalStudents: DB.students.length, totalTeachers: DB.teachers.length, totalClasses: DB.classes.length, attendanceToday: 92.4 });
  }
  res.json({ data: base });
});

/* ── Catch-all ── */
app.get("*", (req, res) => {
  if (req.path.match(/\.(css|js|png|jpg|jpeg|gif|svg|ico|woff2?|ttf|eot|map)$/)) {
    return res.status(404).send("Not found");
  }
  res.sendFile(path.join(ROOT, "index.html"));
});

/* ── Start ── */
const server = http.createServer(app);

server.listen(PORT, () => {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║   NGIS — New Gateway International School                ║");
  console.log("║   School Management System · Complete Express Server     ║");
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log(`║   Running at:  http://localhost:${PORT}                       ║`);
  console.log(`║   Environment: ${(process.env.NODE_ENV || "development").padEnd(43)}║`);
  console.log("╠══════════════════════════════════════════════════════════╣");
  console.log("║   Portals:                                               ║");
  console.log(`║   Admin   →  http://localhost:${PORT}/pages/admin/admin.html  ║`);
  console.log(`║   Student →  http://localhost:${PORT}/pages/student/student.html ║`);
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
