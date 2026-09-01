/**
 * NGIS School ERP — Attendance Routes
 *
 * Teacher/Admin: mark attendance for a class/date
 * Student: view own records
 * Parent: view linked child's records
 */

"use strict";

const express = require("express");
const { v4: uuidv4 } = require("uuid");
const { getDb } = require("../db/connection");
const { authenticate, requireRole } = require("../middleware/auth");

const router = express.Router();

const VALID_STATUS = new Set(["present", "absent", "late", "excused"]);

/**
 * GET /api/attendance
 * Query:
 *   - studentId (parent required; student optional own)
 *   - classId + date (teacher roster view)
 *   - from / to (date range)
 */
router.get("/", authenticate, (req, res) => {
  const db = getDb();
  const role = req.user.role;
  const { studentId, classId, date, from, to } = req.query;

  // Teacher/Admin: class roster for a date
  if ((role === "teacher" || role === "admin") && classId) {
    const targetDate = date || new Date().toISOString().slice(0, 10);

    const students = db.prepare(`
      SELECT s.id as student_id, s.student_number, s.grade,
             u.first_name, u.last_name,
             a.id as attendance_id, a.status, a.notes, a.date
      FROM students s
      JOIN users u ON u.id = s.user_id
      LEFT JOIN attendance a ON a.student_id = s.id AND a.class_id = ? AND a.date = ?
      WHERE s.class_id = ? AND s.status = 'active'
      ORDER BY u.last_name, u.first_name
    `).all(classId, targetDate, classId);

    return res.json({
      data: students,
      meta: { classId, date: targetDate, total: students.length },
    });
  }

  // Student: own attendance
  if (role === "student") {
    const student = db.prepare(`SELECT id, class_id FROM students WHERE user_id = ?`).get(req.user.id);
    if (!student) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Student not found" } });

    let sql = `SELECT * FROM attendance WHERE student_id = ?`;
    const params = [student.id];
    if (from) { sql += ` AND date >= ?`; params.push(from); }
    if (to) { sql += ` AND date <= ?`; params.push(to); }
    sql += ` ORDER BY date DESC LIMIT 100`;

    const rows = db.prepare(sql).all(...params);
    const summary = summarize(rows);
    return res.json({ data: rows, meta: { total: rows.length, ...summary } });
  }

  // Parent: linked child
  if (role === "parent") {
    if (!studentId) {
      return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "studentId required" } });
    }
    const parent = db.prepare(`SELECT id FROM parents WHERE user_id = ?`).get(req.user.id);
    if (!parent) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Parent not found" } });

    const link = db.prepare(`SELECT 1 FROM parent_students WHERE parent_id = ? AND student_id = ?`).get(parent.id, studentId);
    if (!link) return res.status(403).json({ error: { code: "FORBIDDEN", message: "Access denied" } });

    let sql = `SELECT * FROM attendance WHERE student_id = ?`;
    const params = [studentId];
    if (from) { sql += ` AND date >= ?`; params.push(from); }
    if (to) { sql += ` AND date <= ?`; params.push(to); }
    sql += ` ORDER BY date DESC LIMIT 100`;

    const rows = db.prepare(sql).all(...params);
    return res.json({ data: rows, meta: { total: rows.length, ...summarize(rows) } });
  }

  // Admin: optional student filter
  if (role === "admin" && studentId) {
    const rows = db.prepare(`SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC LIMIT 100`).all(studentId);
    return res.json({ data: rows, meta: { total: rows.length, ...summarize(rows) } });
  }

  return res.status(400).json({
    error: { code: "VALIDATION_ERROR", message: "Provide classId (teacher) or use student/parent role endpoints" },
  });
});

/**
 * POST /api/attendance
 * Teacher/Admin mark one or many records
 *
 * Body (single):
 *   { studentId, classId, date, status, notes? }
 * Body (bulk):
 *   { classId, date, records: [{ studentId, status, notes? }] }
 */
router.post("/", authenticate, requireRole("teacher", "admin"), (req, res) => {
  const db = getDb();
  const body = req.body || {};

  let teacherId = null;
  if (req.user.role === "teacher") {
    const teacher = db.prepare(`SELECT id FROM teachers WHERE user_id = ?`).get(req.user.id);
    if (!teacher) return res.status(404).json({ error: { code: "NOT_FOUND", message: "Teacher profile not found" } });
    teacherId = teacher.id;
  }

  // Bulk mode
  if (Array.isArray(body.records)) {
    const { classId, date } = body;
    if (!classId || !date) {
      return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "classId and date required for bulk" } });
    }

    const upsert = db.prepare(`
      INSERT INTO attendance (id, student_id, class_id, date, status, marked_by, notes)
      VALUES (@id, @student_id, @class_id, @date, @status, @marked_by, @notes)
      ON CONFLICT(student_id, class_id, date) DO UPDATE SET
        status = excluded.status,
        notes = excluded.notes,
        marked_by = excluded.marked_by,
        updated_at = datetime('now')
    `);

    const tx = db.transaction((records) => {
      for (const r of records) {
        if (!VALID_STATUS.has(r.status)) continue;
        upsert.run({
          id: uuidv4(),
          student_id: r.studentId,
          class_id: classId,
          date,
          status: r.status,
          marked_by: teacherId,
          notes: r.notes || null,
        });
      }
    });

    tx(body.records);

    // Refresh attendance rates for affected students
    for (const r of body.records) {
      refreshAttendanceRate(db, r.studentId);
    }

    return res.status(201).json({ message: "Attendance saved", meta: { count: body.records.length, classId, date } });
  }

  // Single mode
  const { studentId, classId, date, status, notes } = body;
  if (!studentId || !classId || !date || !status) {
    return res.status(400).json({
      error: { code: "VALIDATION_ERROR", message: "studentId, classId, date, and status are required" },
    });
  }
  if (!VALID_STATUS.has(status)) {
    return res.status(400).json({ error: { code: "VALIDATION_ERROR", message: "Invalid status" } });
  }

  const id = uuidv4();
  db.prepare(`
    INSERT INTO attendance (id, student_id, class_id, date, status, marked_by, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(student_id, class_id, date) DO UPDATE SET
      status = excluded.status,
      notes = excluded.notes,
      marked_by = excluded.marked_by,
      updated_at = datetime('now')
  `).run(id, studentId, classId, date, status, teacherId, notes || null);

  refreshAttendanceRate(db, studentId);

  const row = db.prepare(`SELECT * FROM attendance WHERE student_id = ? AND class_id = ? AND date = ?`).get(studentId, classId, date);
  res.status(201).json({ data: row });
});

function summarize(rows) {
  const total = rows.length;
  const present = rows.filter(r => r.status === "present").length;
  const late = rows.filter(r => r.status === "late").length;
  const absent = rows.filter(r => r.status === "absent").length;
  const excused = rows.filter(r => r.status === "excused").length;
  const rate = total ? Math.round(((present + late + excused) / total) * 100) : 0;
  return { present, late, absent, excused, rate };
}

function refreshAttendanceRate(db, studentId) {
  const stats = db.prepare(`
    SELECT
      COUNT(*) as total,
      SUM(CASE WHEN status IN ('present','late','excused') THEN 1 ELSE 0 END) as good
    FROM attendance WHERE student_id = ?
  `).get(studentId);

  if (stats && stats.total > 0) {
    const rate = Math.round((stats.good / stats.total) * 100);
    db.prepare(`UPDATE students SET attendance_rate = ?, updated_at = datetime('now') WHERE id = ?`).run(rate, studentId);
  }
}

module.exports = router;
