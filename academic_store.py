"""Persistent academic records store for the NGIS Grades & Attendance MVP.

The existing application is a static/demo ERP. This module provides one small,
transactional SQLite source of truth for the academic domain without replacing
unrelated portal data. It is intentionally dependency-free.
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("NGIS_ACADEMIC_DB", str(ROOT / ".data" / "academic.sqlite3")))
_LOCK = threading.RLock()

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS academic_years (
  id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, is_current INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS grading_periods (
  id TEXT PRIMARY KEY, academic_year_id TEXT NOT NULL REFERENCES academic_years(id),
  name TEXT NOT NULL, sequence_no INTEGER NOT NULL, starts_on TEXT, ends_on TEXT,
  status TEXT NOT NULL DEFAULT 'open', UNIQUE(academic_year_id, name)
);
CREATE TABLE IF NOT EXISTS subjects (
  id TEXT PRIMARY KEY, code TEXT, name TEXT NOT NULL, credit_value REAL NOT NULL DEFAULT 1,
  pass_mark REAL NOT NULL DEFAULT 50, status TEXT NOT NULL DEFAULT 'active'
);
CREATE TABLE IF NOT EXISTS teacher_assignments (
  teacher_id TEXT NOT NULL, class_id TEXT NOT NULL, subject_id TEXT NOT NULL,
  academic_year_id TEXT NOT NULL, PRIMARY KEY(teacher_id, class_id, subject_id, academic_year_id)
);
CREATE TABLE IF NOT EXISTS enrollments (
  student_id TEXT NOT NULL, class_id TEXT NOT NULL, academic_year_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active', PRIMARY KEY(student_id, academic_year_id)
);
CREATE TABLE IF NOT EXISTS grading_rules (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, version INTEGER NOT NULL, max_gpa REAL NOT NULL DEFAULT 4,
  rules_json TEXT NOT NULL, is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS assessments (
  id TEXT PRIMARY KEY, class_id TEXT NOT NULL, subject_id TEXT NOT NULL,
  grading_period_id TEXT NOT NULL REFERENCES grading_periods(id), title TEXT NOT NULL,
  category TEXT NOT NULL, max_score REAL NOT NULL, weight REAL NOT NULL DEFAULT 1,
  teacher_id TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'draft', created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS grades (
  id TEXT PRIMARY KEY, assessment_id TEXT NOT NULL REFERENCES assessments(id),
  student_id TEXT NOT NULL, score REAL, state TEXT NOT NULL DEFAULT 'missing',
  comments TEXT NOT NULL DEFAULT '', workflow TEXT NOT NULL DEFAULT 'draft',
  recorded_by TEXT NOT NULL, recorded_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  UNIQUE(assessment_id, student_id)
);
CREATE TABLE IF NOT EXISTS attendance (
  id TEXT PRIMARY KEY, student_id TEXT NOT NULL, class_id TEXT NOT NULL,
  subject_id TEXT, attendance_date TEXT NOT NULL, session TEXT NOT NULL DEFAULT 'daily',
  status TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', workflow TEXT NOT NULL DEFAULT 'submitted',
  recorded_by TEXT NOT NULL, recorded_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  UNIQUE(student_id, class_id, subject_id, attendance_date, session)
);
CREATE TABLE IF NOT EXISTS report_cards (
  id TEXT PRIMARY KEY, student_id TEXT NOT NULL, grading_period_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft', published_at TEXT, published_by TEXT,
  UNIQUE(student_id, grading_period_id)
);
CREATE TABLE IF NOT EXISTS audit_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT, actor_id TEXT NOT NULL, actor_role TEXT NOT NULL,
  action TEXT NOT NULL, entity_type TEXT NOT NULL, entity_id TEXT NOT NULL,
  reason TEXT NOT NULL DEFAULT '', details_json TEXT NOT NULL DEFAULT '{}', created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_grades_student ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student_date ON attendance(student_id, attendance_date);
CREATE INDEX IF NOT EXISTS idx_audit_entity ON audit_events(entity_type, entity_id);
"""


def _now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _id(prefix: str) -> str:
    import uuid
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def init(seed: dict[str, Any]) -> None:
    with _LOCK:
        conn = _conn()
        conn.executescript(SCHEMA)
        if conn.execute("SELECT 1 FROM academic_years LIMIT 1").fetchone():
            conn.close()
            return
        now = _now()
        conn.execute("INSERT INTO academic_years VALUES (?, ?, 1, ?)", ("ay-2025-26", "2025–26", now))
        conn.executemany("INSERT INTO grading_periods VALUES (?, ?, ?, ?, ?, ?, ?)", [
            ("gp-term-1", "ay-2025-26", "Term 1", 1, "2025-09-01", "2025-12-20", "closed"),
            ("gp-term-2", "ay-2025-26", "Term 2", 2, "2026-01-05", "2026-06-30", "open"),
        ])
        subjects = seed.get("subjects") or [
            {"id": "subj-math", "name": "Advanced Mathematics", "code": "MATH-10"},
            {"id": "subj-phys", "name": "Physics & Lab", "code": "PHY-10"},
            {"id": "subj-eng", "name": "English Literature", "code": "ENG-10"},
        ]
        conn.executemany("INSERT OR IGNORE INTO subjects(id, code, name, credit_value, pass_mark) VALUES (?, ?, ?, ?, ?)", [
            (s.get("id"), s.get("code", ""), s.get("name") or s.get("subject_name"), float(s.get("creditValue", 3)), float(s.get("passMark", 50))) for s in subjects
        ])
        conn.execute("INSERT INTO grading_rules VALUES (?, ?, ?, ?, ?, 1)", (
            "rule-default-v1", "NGIS 4.0 scale", 1, 4.0,
            json.dumps({"A": [90, 4.0], "B+": [85, 3.5], "B": [80, 3.0], "C+": [75, 2.5], "C": [70, 2.0], "D": [60, 1.0], "F": [0, 0.0]})
        ))
        class_rows = seed.get("classes", [])
        students = seed.get("students", [])
        teachers = seed.get("teachers", [])
        class_by_name = {str(c.get("name", "")).replace("Grade ", ""): c.get("id") for c in class_rows}
        for student in students:
            cls = class_by_name.get(student.get("class"))
            if cls:
                conn.execute("INSERT OR IGNORE INTO enrollments VALUES (?, ?, ?, 'active')", (student["id"], cls, "ay-2025-26"))
        for teacher in teachers:
            teacher_id = teacher.get("id")
            for cls_name in teacher.get("classes", []):
                cls_id = class_by_name.get(cls_name)
                for subject_name in teacher.get("subjects", []):
                    row = conn.execute("SELECT id FROM subjects WHERE name = ?", (subject_name,)).fetchone()
                    if cls_id and row:
                        conn.execute("INSERT OR IGNORE INTO teacher_assignments VALUES (?, ?, ?, ?)", (teacher_id, cls_id, row["id"], "ay-2025-26"))
        conn.commit()
        conn.close()


def rowdict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def query(sql: str, args: Iterable[Any] = ()) -> list[dict[str, Any]]:
    with _LOCK:
        c = _conn()
        rows = [dict(r) for r in c.execute(sql, tuple(args)).fetchall()]
        c.close()
        return rows


def one(sql: str, args: Iterable[Any] = ()) -> dict[str, Any] | None:
    rows = query(sql, args)
    return rows[0] if rows else None


def execute(sql: str, args: Iterable[Any] = ()) -> None:
    with _LOCK:
        c = _conn(); c.execute(sql, tuple(args)); c.commit(); c.close()


def transaction(statements: list[tuple[str, tuple[Any, ...]]]) -> None:
    with _LOCK:
        c = _conn()
        try:
            c.execute("BEGIN")
            for sql, args in statements:
                c.execute(sql, args)
            c.commit()
        except Exception:
            c.rollback(); raise
        finally:
            c.close()


def audit(actor_id: str, actor_role: str, action: str, entity_type: str, entity_id: str, reason: str = "", details: dict[str, Any] | None = None) -> None:
    execute("INSERT INTO audit_events(actor_id, actor_role, action, entity_type, entity_id, reason, details_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (actor_id, actor_role, action, entity_type, entity_id, reason, json.dumps(details or {}), _now()))


def grade_band(score: float | None) -> tuple[str, float]:
    if score is None: return ("—", 0.0)
    for letter, threshold, points in [("A", 90, 4.0), ("B+", 85, 3.5), ("B", 80, 3.0), ("C+", 75, 2.5), ("C", 70, 2.0), ("D", 60, 1.0)]:
        if score >= threshold: return letter, points
    return "F", 0.0


def aggregate_gpa(student_id: str, period_id: str | None = None) -> float:
    args: list[Any] = [student_id]
    period_filter = ""
    if period_id:
        period_filter = " AND a.grading_period_id = ?"; args.append(period_id)
    rows = query("""SELECT g.score, a.max_score, s.credit_value FROM grades g
                    JOIN assessments a ON a.id=g.assessment_id JOIN subjects s ON s.id=a.subject_id
                    WHERE g.student_id=? AND g.workflow='published' AND g.state='graded'""" + period_filter, args)
    total_points = total_credits = 0.0
    for r in rows:
        pct = (float(r["score"]) / float(r["max_score"]) * 100) if r["max_score"] else 0
        _, points = grade_band(pct); credits = float(r["credit_value"] or 1)
        total_points += points * credits; total_credits += credits
    return round(total_points / total_credits, 2) if total_credits else 0.0


def attendance_summary(student_id: str, period_start: str | None = None, period_end: str | None = None) -> dict[str, Any]:
    args: list[Any] = [student_id]; where = "student_id=?"
    if period_start: where += " AND attendance_date>=?"; args.append(period_start)
    if period_end: where += " AND attendance_date<=?"; args.append(period_end)
    rows = query(f"SELECT status, COUNT(*) AS n FROM attendance WHERE {where} GROUP BY status", args)
    counts = {r["status"]: int(r["n"]) for r in rows}
    total = sum(counts.values()); counted = total - counts.get("excused", 0)
    present = counts.get("present", 0) + counts.get("tardy", 0)
    return {"present": present, "absent": counts.get("absent", 0), "tardy": counts.get("tardy", 0), "excused": counts.get("excused", 0), "total": total, "percentage": round((present / counted * 100), 1) if counted else 0.0}


def now() -> str:
    return _now()


def new_id(prefix: str) -> str:
    return _id(prefix)
