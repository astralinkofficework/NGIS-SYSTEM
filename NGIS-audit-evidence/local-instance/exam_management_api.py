"""
============================================================
NGIS School Management System — Examination Management API
New Gateway International School · 2026
============================================================
Unified, persistent, four-portal Examination Management Engine.
Powers:
  1. Student Portal   — View assigned exams, prep materials, schedules, and authorized published results
  2. Teacher Portal   — Create exams, manage assigned classes, conflict check, record attendance, enter marks, submit results
  3. Principal Portal — Review exam proposals, approve/correct/reject, monitor results, authorize publication
  4. Admin Portal     — Institutional scheduling, conflict resolution, room capacity & readiness, audit logs
============================================================
"""

import os
import re
import json
import uuid
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from flask import Blueprint, request, jsonify

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("NGIS_ACADEMIC_DB", str(ROOT / ".data" / "academic.sqlite3")))
_LOCK = threading.RLock()

exam_bp = Blueprint('exam_mgmt', __name__)

# Simplified examination scheduling (student-visible timetable only).
# These are the only exam categories exposed by the four portal workspaces.
EXAM_TYPES = {
    'monthly': 'Monthly Examination',
    'midterm': 'Midterm Examination',
    'semester': 'Semester Examination',
    'final': 'Final Examination',
    'class_test': 'Class Test',
}
EXAM_TYPE_ALIASES = {
    'monthly examination': 'monthly', 'monthly': 'monthly',
    'midterm examination': 'midterm', 'mid-term': 'midterm', 'midterm': 'midterm',
    'semester examination': 'semester', 'semester': 'semester',
    'final examination': 'final', 'final': 'final',
    'class test': 'class_test', 'class-test': 'class_test', 'class_test': 'class_test',
    # Legacy demo records are displayed as Class Test without mutating stored data.
    'mock': 'class_test', 'practical': 'class_test', 'quiz': 'class_test',
}
STAFF_ROLES = ('teacher', 'principal', 'admin', 'superadmin')
ACADEMIC_APPROVER_ROLES = ('principal', 'superadmin')

def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def _read_json(relative_path, fallback):
    path = ROOT / relative_path
    try:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as fh:
                return json.load(fh)
    except Exception:
        pass
    return fallback

def _normalise_role(value):
    role = str(value or '').strip().lower()
    if role in ('super_admin', 'super-admin'):
        return 'superadmin'
    if role == 'editor':
        return 'admin'
    return role

DEPARTMENT_NAMES = {
    'dept-eng': 'English Department', 'english': 'English Department', 'eng': 'English Department',
    'dept-mat': 'Mathematics Department', 'math': 'Mathematics Department', 'maths': 'Mathematics Department',
    'dept-sci': 'Science Department', 'science': 'Science Department', 'phys': 'Science Department',
    'dept-khm': 'Khmer Department', 'khmer': 'Khmer Department',
    'dept-chn': 'Chinese Department', 'chinese': 'Chinese Department',
    'dept-hum': 'Social Studies Department', 'history': 'Social Studies Department',
    'dept-art': 'Fine Arts Department', 'art': 'Fine Arts Department',
    'dept-ict': 'ICT Department', 'ict': 'ICT Department',
}

def _canonical_department_id(value):
    raw = str(value or '').strip()
    key = raw.lower()
    if key in DEPARTMENT_NAMES:
        return key
    for dept_id, dept_name in DEPARTMENT_NAMES.items():
        if key == dept_name.lower():
            return dept_id
    return raw

def _department_name(dept_id, fallback=''):
    key = str(dept_id or '').strip().lower()
    return DEPARTMENT_NAMES.get(key) or fallback or key

def _canonical_exam_type(value):
    key = str(value or '').strip().lower().replace('_', ' ').replace('-', ' ')
    if key in EXAM_TYPE_ALIASES:
        return EXAM_TYPE_ALIASES[key]
    compact = key.replace(' ', '_')
    return compact if compact in EXAM_TYPES else 'class_test'

def _exam_type_label(value):
    return EXAM_TYPES.get(_canonical_exam_type(value), 'Class Test')

STATUS_LABELS = {
    'draft': 'Draft', 'submitted': 'Pending review', 'pending': 'Pending review',
    'needs_correction': 'Changes requested', 'rejected': 'Rejected',
    'approved': 'Approved', 'published': 'Published', 'cancelled': 'Cancelled',
    'completed': 'Completed', 'results_processing': 'Published',
    'results_published': 'Completed',
}

def _status_label(status, row=None):
    if row and str(row.get('status') or '') == 'cancelled':
        return 'Cancelled'
    return STATUS_LABELS.get(str(status or '').lower(), str(status or 'Draft').replace('_', ' ').title())

def _identity_index():
    data = _read_json('data/user_accounts.json', {})
    accounts = data.get('accounts', []) if isinstance(data, dict) else []
    index = {}
    for account in accounts:
        if not isinstance(account, dict):
            continue
        for key in (account.get('email'), account.get('username')):
            if key:
                index[str(key).strip().lower()] = account
    return index

def _resolve_identity(value):
    """Resolve a browser actor (email/username) to a real academic person record."""
    account = _identity_index().get(str(value or '').strip().lower())
    if not account:
        return None
    role = _normalise_role(account.get('role') or account.get('display_role'))
    person_id = str(account.get('person_id') or account.get('id') or '')
    student_ids = set()
    try:
        conn = _conn()
        student_ids = {r['student_id'] for r in conn.execute('SELECT student_id FROM enrollments')}
        conn.close()
    except Exception:
        pass
    if role == 'student' and person_id not in student_ids:
        # Demo student account has no person_id; use the canonical enrolled id.
        person_id = '2026-STD-0142'
    return {
        'id': person_id or str(account.get('id') or ''),
        'role': role,
        'name': account.get('name') or person_id,
        'email': str(account.get('email') or value).strip().lower(),
        'campus': account.get('campus') or '',
        'department': account.get('department') or '',
    }

def _directory_maps(conn):
    """Build department / subject / class / campus lookup data from real stores."""
    config = _read_json('data/system_configuration.json', {})
    campuses = [
        {'id': c.get('id'), 'name': c.get('name')}
        for c in (config.get('campuses') or []) if isinstance(c, dict) and c.get('id')
    ]
    departments = []
    seen = set()
    assignments = conn.execute(
        "SELECT DISTINCT department_id, grade, class_id FROM teacher_assignments "
        "WHERE status='active' OR status='' OR status IS NULL"
    ).fetchall()
    for row in assignments:
        did = _canonical_department_id(row['department_id'])
        if did and did not in seen:
            seen.add(did)
            departments.append({'id': did, 'name': _department_name(did)})
    if not departments:
        departments = [{'id': k, 'name': v} for k, v in DEPARTMENT_NAMES.items() if k.startswith('dept-')]

    subjects = []
    for row in conn.execute("SELECT id, code, name FROM subjects WHERE status='active' OR status='' ORDER BY name"):
        subjects.append({'id': row['id'], 'code': row['code'] or '', 'name': row['name']})

    classes = {}
    for row in assignments:
        cid = row['class_id']
        if not cid:
            continue
        grade = row['grade'] or ''
        label = grade if grade.lower().startswith('grade') else ''
        if not label:
            m = re.match(r'cls-(?:eng-|khm-|chn-|art-|sci-)?(\d+)([a-z]+)', cid, re.I)
            label = ('Grade ' + m.group(1) + m.group(2).upper()) if m else cid
        classes.setdefault(cid, {'id': cid, 'name': label, 'department_id': _canonical_department_id(row['department_id'])})
    for row in conn.execute("SELECT DISTINCT class_id FROM enrollments"):
        cid = row['class_id']
        if cid and cid not in classes:
            classes[cid] = {'id': cid, 'name': cid.upper(), 'department_id': ''}
    return {
        'departments': departments,
        'subjects': subjects,
        'classes': sorted(classes.values(), key=lambda x: x['name']),
        'campuses': campuses,
    }

def _teacher_assignments(conn, teacher_id):
    rows = conn.execute(
        "SELECT class_id, subject_id, department_id, grade FROM teacher_assignments "
        "WHERE teacher_id=? AND (status='active' OR status='' OR status IS NULL)",
        (teacher_id,),
    ).fetchall()
    return {
        'pairs': {(r['subject_id'], r['class_id']) for r in rows},
        'subjects': {r['subject_id'] for r in rows},
        'classes': {r['class_id'] for r in rows},
        'departments': {_canonical_department_id(r['department_id']) for r in rows if r['department_id']},
    }

def _simplified_exam(row, conflict=False):
    """Project a stored exam row to the small schedule shape used by the UI."""
    d = dict(row)
    class_ids = _json_list(d.get('class_ids'))
    class_names = _json_list(d.get('class_names'))
    dept_id = d.get('department_id') or ''
    return {
        'id': d.get('id'),
        'title': d.get('title') or (d.get('subject_name', '') + ' — ' + _exam_type_label(d.get('exam_type'))),
        'subject_id': d.get('subject_id') or '',
        'subject': d.get('subject_name') or '',
        'exam_type': _canonical_exam_type(d.get('exam_type')),
        'exam_type_label': _exam_type_label(d.get('exam_type')),
        'department_id': dept_id,
        'department': d.get('department_name') or _department_name(dept_id),
        'class_ids': class_ids,
        'classes': class_names,
        'exam_date': d.get('exam_date') or '',
        'start_time': d.get('start_time') or '',
        'end_time': d.get('end_time') or '',
        'status': d.get('status') or 'draft',
        'status_label': _status_label(d.get('status'), d),
        'academic_status': d.get('academic_status') or '',
        'teacher_id': d.get('teacher_id') or '',
        'teacher': d.get('teacher_name') or '',
        'campus_id': d.get('campus_id') or '',
        'campus': d.get('campus_name') or '',
        'correction_notes': d.get('correction_notes') or '',
        'created_at': d.get('created_at') or '',
        'updated_at': d.get('updated_at') or '',
        'published_at': d.get('published_at') or '',
        'conflict': bool(conflict),
    }

def _json_list(value):
    if isinstance(value, (list, tuple)):
        return list(value)
    try:
        parsed = json.loads(value or '[]')
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []

# ── DATABASE SCHEMA INITIALIZATION & MIGRATIONS ─────────────────────────────
def init_exam_schema():
    with _LOCK:
        conn = _conn()
        try:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                exam_type TEXT NOT NULL DEFAULT 'midterm',
                academic_year_id TEXT NOT NULL DEFAULT 'ay-2025-26',
                term TEXT NOT NULL DEFAULT 'Semester 2',
                campus_id TEXT NOT NULL DEFAULT 'cam-tk',
                campus_name TEXT NOT NULL DEFAULT 'Tuol Kork Main Campus',
                department_id TEXT NOT NULL,
                department_name TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                subject_name TEXT NOT NULL,
                teacher_id TEXT NOT NULL,
                teacher_name TEXT NOT NULL,
                class_ids TEXT NOT NULL,
                class_names TEXT NOT NULL,
                exam_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                duration_mins INTEGER NOT NULL DEFAULT 90,
                room_id TEXT NOT NULL DEFAULT 'room-hall-b',
                room_name TEXT NOT NULL DEFAULT 'Hall B · Desk #42',
                seating_capacity INTEGER NOT NULL DEFAULT 40,
                instructions TEXT NOT NULL DEFAULT '',
                max_marks REAL NOT NULL DEFAULT 100.0,
                passing_marks REAL NOT NULL DEFAULT 60.0,
                weight_pct REAL NOT NULL DEFAULT 30.0,
                syllabus TEXT NOT NULL DEFAULT '',
                prep_resources_json TEXT NOT NULL DEFAULT '[]',
                attachments_json TEXT NOT NULL DEFAULT '[]',
                status TEXT NOT NULL DEFAULT 'draft',
                academic_status TEXT NOT NULL DEFAULT 'draft',
                operational_status TEXT NOT NULL DEFAULT 'pending',
                result_status TEXT NOT NULL DEFAULT 'not_started',
                correction_notes TEXT NOT NULL DEFAULT '',
                internal_notes TEXT NOT NULL DEFAULT '',
                created_by TEXT NOT NULL,
                updated_by TEXT NOT NULL,
                approved_by TEXT NOT NULL DEFAULT '',
                approved_at TEXT NOT NULL DEFAULT '',
                published_by TEXT NOT NULL DEFAULT '',
                published_at TEXT NOT NULL DEFAULT '',
                results_published_by TEXT NOT NULL DEFAULT '',
                results_published_at TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS exam_student_results (
                id TEXT PRIMARY KEY,
                exam_id TEXT NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
                student_id TEXT NOT NULL,
                student_name TEXT NOT NULL,
                class_id TEXT NOT NULL,
                class_name TEXT NOT NULL,
                attendance_status TEXT NOT NULL DEFAULT 'present',
                score REAL,
                max_marks REAL NOT NULL DEFAULT 100.0,
                percentage REAL,
                letter_grade TEXT NOT NULL DEFAULT '',
                gpa_points REAL DEFAULT 0.0,
                teacher_feedback TEXT NOT NULL DEFAULT '',
                correction_history_json TEXT NOT NULL DEFAULT '[]',
                is_locked INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(exam_id, student_id)
            );
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS exam_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                actor_role TEXT NOT NULL,
                actor_name TEXT NOT NULL,
                action TEXT NOT NULL,
                previous_state TEXT NOT NULL DEFAULT '',
                new_state TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                details_json TEXT NOT NULL DEFAULT '{}',
                timestamp TEXT NOT NULL
            );
            """)

            conn.execute("""
            CREATE TABLE IF NOT EXISTS exam_locations (
                id TEXT PRIMARY KEY,
                campus_id TEXT NOT NULL,
                campus_name TEXT NOT NULL,
                name TEXT NOT NULL,
                building TEXT NOT NULL DEFAULT '',
                floor TEXT NOT NULL DEFAULT '',
                capacity INTEGER NOT NULL DEFAULT 35,
                is_active INTEGER NOT NULL DEFAULT 1,
                amenities TEXT NOT NULL DEFAULT ''
            );
            """)

            conn.execute("CREATE INDEX IF NOT EXISTS idx_exams_dept ON exams(department_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_exams_date ON exams(exam_date);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_exams_status ON exams(status);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_exam_res_student ON exam_student_results(student_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_exam_audit_exam ON exam_audit_log(exam_id);")

            # Seed Locations if empty
            loc_count = conn.execute("SELECT COUNT(*) FROM exam_locations").fetchone()[0]
            if loc_count == 0:
                _seed_locations(conn)

            # Seed Exams if empty
            exam_count = conn.execute("SELECT COUNT(*) FROM exams").fetchone()[0]
            if exam_count == 0:
                _seed_exams(conn)

        finally:
            conn.close()

def _seed_locations(conn: sqlite3.Connection):
    locations = [
        ('room-hall-a', 'cam-tk', 'Tuol Kork Main Campus', 'Hall A — Main Auditorium', 'Academic Wing A', 'Ground Floor', 120, 'AV Equipment, Dual Projectors, Air Conditioned, Sound System'),
        ('room-hall-b', 'cam-tk', 'Tuol Kork Main Campus', 'Hall B — Examination Hall', 'Academic Wing A', '1st Floor', 80, 'Audio Broadcast, Individual Desks, Air Conditioned'),
        ('room-101', 'cam-tk', 'Tuol Kork Main Campus', 'Room 101 — Bilingual Classroom', 'Building B', '1st Floor', 35, 'Projector, Whiteboard, Air Conditioned'),
        ('room-102', 'cam-tk', 'Tuol Kork Main Campus', 'Room 102 — Bilingual Classroom', 'Building B', '1st Floor', 35, 'Projector, Whiteboard, Air Conditioned'),
        ('room-201', 'cam-tk', 'Tuol Kork Main Campus', 'Room 201 — Science Lab', 'Science Building', '2nd Floor', 30, 'Lab Benches, Chemical Safety Station, Projector'),
        ('room-202', 'cam-tk', 'Tuol Kork Main Campus', 'Room 202 — Physics & Optics Lab', 'Science Building', '2nd Floor', 30, 'Optics Equipment, Power Outlets, Smart Board'),
        ('room-301', 'cam-tk', 'Tuol Kork Main Campus', 'Room 301 — Humanities Lecture Room', 'Academic Wing C', '3rd Floor', 35, 'Smart TV, Air Conditioned, Whiteboard'),
        ('room-302', 'cam-tk', 'Tuol Kork Main Campus', 'Room 302 — Mathematics Wing', 'Academic Wing C', '3rd Floor', 35, 'Scientific Graphing Calculators, Individual Desks'),
        ('room-304', 'cam-stem', 'STEM & Robotics Innovation Hub', 'Room 304 — Computer Lab', 'Innovation Tower', '3rd Floor', 32, 'Workstations, High-Speed LAN, Power Backup'),
        ('room-401', 'cam-ckm', 'Chamkarmon High School Branch', 'Room 401 — Language Lab', 'East Wing', '4th Floor', 30, 'Audio Headsets, Recording Stations, Air Conditioned'),
    ]
    for loc in locations:
        conn.execute("""
            INSERT OR REPLACE INTO exam_locations (id, campus_id, campus_name, name, building, floor, capacity, amenities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, loc)

def _calc_grade_and_points(score, max_marks):
    if score is None or max_marks <= 0:
        return 0.0, 'N/A', 0.0
    pct = round((score / max_marks) * 100.0, 1)
    if pct >= 93: return pct, 'A', 4.0
    if pct >= 90: return pct, 'A-', 3.7
    if pct >= 87: return pct, 'B+', 3.3
    if pct >= 83: return pct, 'B', 3.0
    if pct >= 80: return pct, 'B-', 2.7
    if pct >= 77: return pct, 'C+', 2.3
    if pct >= 73: return pct, 'C', 2.0
    if pct >= 70: return pct, 'C-', 1.7
    if pct >= 65: return pct, 'D+', 1.3
    if pct >= 60: return pct, 'D', 1.0
    return pct, 'F', 0.0

def _seed_exams(conn: sqlite3.Connection):
    now_ts = _now()

    # 1. English Literature Mid-Term (Published with Results Published)
    # Student 2026-STD-0142 is in Grade 10A (cls-10a)
    exam_1_id = "EXM-2026-ENG-01"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_1_id,
        "English Literature — Mid-Term Examination",
        "midterm", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "english", "English Department", "subj-eng", "English Literature",
        "TCH-2024-042", "Dr. Sarah Jenkins", json.dumps(["cls-10a", "cls-11b"]), json.dumps(["Grade 10A", "Grade 11B"]),
        "2026-07-14", "08:30", "10:30", 120,
        "room-hall-a", "Hall A — Main Auditorium", 120,
        "Two comparative essays of 800 and 1000 words. Section A: Victorian Poetry (40 marks). Section B: Modern Drama (60 marks). Closed-book examination. Blue or black ink pens only.",
        100.0, 60.0, 30.0,
        "Units 4–8: Victorian Poetic Movements, Post-Colonial Drama & Critical Analysis.",
        json.dumps([
            {"id": "lit-syllabus", "title": "English Literature Exam Syllabus", "type": "syllabus", "size": "1.8 MB"},
            {"id": "past-paper-2025", "title": "Past Examination Paper (AY 2024-25)", "type": "past_paper", "size": "2.4 MB"},
            {"id": "rubric-marking", "title": "Essay Grading Rubric & Band Descriptors", "type": "rubric", "size": "780 KB"}
        ]),
        json.dumps([
            {"name": "ENG_Lit_Midterm_Paper_Spec.pdf", "size": "420 KB"}
        ]),
        "results_published", "approved", "confirmed", "published",
        "", "All academic quality benchmarks met for Cambridge Secondary alignment.",
        "TCH-2024-042", "PRN-2024-002", "PRN-2024-002", "2026-06-10T08:00:00Z",
        "ADM-2024-001", "2026-06-12T09:30:00Z", "PRN-2024-002", "2026-07-16T14:00:00Z",
        "2026-06-01T08:00:00Z", now_ts
    ))

    # Seed student results for Exam 1
    students_10a = [
        ("2026-STD-0142", "Nrinphouneta Hok", 92.5, "present", "Excellent comparative textual analysis and sustained critical perspective throughout both essays."),
        ("2026-STD-0144", "Vicheka Meas", 86.0, "present", "Strong synthesis of poetic devices. Work on transitions in Section B."),
        ("2026-STD-0145", "Virak Heng", 78.5, "present", "Good understanding of core themes; provide more specific citations from the text."),
        ("2026-STD-0148", "Kosal Rith Mony", 88.0, "present", "Very cohesive essays with thoughtful thematic structure."),
        ("2026-STD-0151", "Sreylin Vuth", 94.0, "present", "Outstanding thesis argument and stylistic maturity."),
        ("2026-STD-0155", "Heng Piseth", 74.0, "present", "Satisfactory effort. Needs closer adherence to the comparative prompt."),
        ("2026-STD-0160", "Emily Jenkins", 96.0, "present", "Exemplary critical essay. Masterful engagement with literary context."),
        ("2026-STD-0168", "Linda Chea", 89.5, "present", "Well-argued interpretations supported by direct textual evidence."),
    ]
    for st_id, st_name, score, att, fback in students_10a:
        pct, letter, pts = _calc_grade_and_points(score, 100.0)
        conn.execute("""
            INSERT OR REPLACE INTO exam_student_results (
                id, exam_id, student_id, student_name, class_id, class_name,
                attendance_status, score, max_marks, percentage, letter_grade, gpa_points,
                teacher_feedback, is_locked, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"res-{exam_1_id}-{st_id}", exam_1_id, st_id, st_name, "cls-10a", "Grade 10A",
            att, score, 100.0, pct, letter, pts, fback, 1, "2026-07-15T10:00:00Z", now_ts
        ))

    # 2. Physics Mid-Term Examination (Upcoming Next Exam - Published)
    exam_2_id = "EXM-2026-PHY-02"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_2_id,
        "Physics — Mid-Term Examination",
        "midterm", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "science", "Science Department", "subj-phys", "Physics & Lab",
        "TCH-2024-042", "Dr. Sarah Jenkins", json.dumps(["cls-10a", "cls-11b"]), json.dumps(["Grade 10A", "Grade 11B"]),
        "2026-06-29", "09:00", "11:30", 150,
        "room-hall-b", "Hall B · Desk #42", 80,
        "Paper 1 (Multiple Choice, 40 marks, 45 mins) & Paper 2 (Structured Theory & Lab Data, 60 marks, 105 mins). Scientific non-programmable calculators permitted. Formula sheet provided.",
        100.0, 60.0, 30.0,
        "Senior Secondary STEM • Waves, Wave Optics, Mechanics & Classical Dynamics.",
        json.dumps([
            {"id": "physics-formulae", "title": "Formulae & Physical Constants Sheet", "type": "formula_sheet", "size": "850 KB"},
            {"id": "physics-past-paper", "title": "Physics Specimen Paper 2026", "type": "specimen", "size": "3.1 MB"},
            {"id": "physics-lab-guide", "title": "Practical Lab Data Analysis Revision Guide", "type": "guide", "size": "1.2 MB"}
        ]),
        json.dumps([
            {"name": "PHY_Exam_Permitted_Calculators_List.pdf", "size": "190 KB"}
        ]),
        "published", "approved", "confirmed", "not_started",
        "", "Approved by Academic Committee for STEM senior track.",
        "TCH-2024-042", "ADM-2024-001", "PRN-2024-002", "2026-06-05T10:00:00Z",
        "ADM-2024-001", "2026-06-08T11:00:00Z", "", "",
        "2026-05-28T09:00:00Z", now_ts
    ))

    # 3. Advanced Mathematics Mid-Term (Upcoming - Approved & Published)
    exam_3_id = "EXM-2026-MTH-03"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_3_id,
        "Advanced Mathematics — Mid-Term Evaluation",
        "midterm", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "math", "Mathematics Department", "subj-math", "Advanced Mathematics",
        "TCH-2024-042", "Dr. Sarah Jenkins", json.dumps(["cls-10a"]), json.dumps(["Grade 10A"]),
        "2026-07-02", "08:30", "10:30", 120,
        "room-302", "Room 302 — Mathematics Wing", 35,
        "Chapters 7–10: Calculus Theorems, Series Convergence & Differential Equations. Standard approved graphing calculators permitted.",
        100.0, 60.0, 25.0,
        "Advanced Differential Calculus & Integration Methods.",
        json.dumps([
            {"id": "maths-formulae", "title": "Calculus & Series Formula Booklet", "type": "formula_sheet", "size": "650 KB"},
            {"id": "maths-practice-set", "title": "Comprehensive Mock Problem Set #4", "type": "practice_set", "size": "1.5 MB"}
        ]),
        json.dumps([]),
        "published", "approved", "confirmed", "not_started",
        "", "Mathematics faculty consensus approval.",
        "TCH-2024-042", "ADM-2024-001", "PRN-2024-002", "2026-06-12T14:00:00Z",
        "ADM-2024-001", "2026-06-15T09:00:00Z", "", "",
        "2026-06-02T11:00:00Z", now_ts
    ))

    # 4. Khmer Literature Final Written Test (Submitted & Pending Principal Review)
    exam_4_id = "EXM-2026-KHM-04"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_4_id,
        "Khmer Literature — Semester Written Examination",
        "final", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "khmer", "Khmer Department", "subj-khm-lit", "Khmer Literature",
        "TCH-2024-023", "Mr. Chea Sophea", json.dumps(["cls-10a", "cls-11b"]), json.dumps(["Grade 10A", "Grade 11B"]),
        "2026-07-09", "08:00", "10:30", 150,
        "room-101", "Room 101 — Bilingual Classroom", 35,
        "Essay questions on Tum Teav and Classical Khmer Epics. MoEYS national standards applied.",
        100.0, 60.0, 40.0,
        "Khmer Literary Classics, Poetry Analysis & Essay Composition.",
        json.dumps([
            {"id": "khmer-lit-guide", "title": "Khmer Poetry Metrical Analysis Guide", "type": "guide", "size": "950 KB"}
        ]),
        json.dumps([
            {"name": "Khmer_Literature_Question_Matrix.pdf", "size": "340 KB"}
        ]),
        "submitted", "pending", "pending", "not_started",
        "", "Awaiting Executive clearance and curriculum alignment verification from Principal Dr. Ly Bunheng.",
        "TCH-2024-023", "TCH-2024-023", "", "",
        "", "", "", "",
        "2026-06-18T14:30:00Z", now_ts
    ))

    # 5. Chinese HSK Level 3 Mock Exam (Grades Submitted & Awaiting Principal Approval)
    exam_5_id = "EXM-2026-CHN-05"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_5_id,
        "Chinese Language — HSK Level 3 Benchmark Mock Examination",
        "mock", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "chinese", "Chinese Department", "subj-chn-lang", "Chinese Language",
        "TCH-2026-096", "Ms. Lin Meiling", json.dumps(["cls-10a"]), json.dumps(["Grade 10A"]),
        "2026-07-20", "13:00", "14:30", 90,
        "room-401", "Room 401 — Language Lab", 30,
        "Listening section (35 mins) & Reading section (55 mins). Audio played through central laboratory headsets.",
        100.0, 60.0, 20.0,
        "HSK 3 Standard Vocabulary (600 characters) & Grammatical Sentence Patterns.",
        json.dumps([
            {"id": "hsk3-vocab", "title": "HSK 3 Complete Vocabulary List & Audio Reference", "type": "vocab", "size": "2.2 MB"}
        ]),
        json.dumps([]),
        "results_processing", "approved", "confirmed", "submitted",
        "", "Teacher completed grading. Marks submitted for Principal executive review and release authorization.",
        "TCH-2026-096", "TCH-2026-096", "PRN-2024-002", "2026-06-20T10:00:00Z",
        "ADM-2024-001", "2026-06-22T08:00:00Z", "", "",
        "2026-06-15T09:00:00Z", now_ts
    ))

    # Seed unapproved grades for Exam 5 (students awaiting publication)
    students_chn = [
        ("2026-STD-0142", "Nrinphouneta Hok", 88.0, "present", "Excellent auditory comprehension in dialogue sections."),
        ("2026-STD-0144", "Vicheka Meas", 81.5, "present", "Sound vocabulary; improve reading speed on longer paragraphs."),
        ("2026-STD-0145", "Virak Heng", 76.0, "present", "Good listening retention. Review measure words."),
        ("2026-STD-0148", "Kosal Rith Mony", 91.0, "present", "High accuracy across both listening and reading portions."),
        ("2026-STD-0151", "Sreylin Vuth", 95.0, "present", "Near-perfect score; commended for accurate character recognition."),
    ]
    for st_id, st_name, score, att, fback in students_chn:
        pct, letter, pts = _calc_grade_and_points(score, 100.0)
        conn.execute("""
            INSERT OR REPLACE INTO exam_student_results (
                id, exam_id, student_id, student_name, class_id, class_name,
                attendance_status, score, max_marks, percentage, letter_grade, gpa_points,
                teacher_feedback, is_locked, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f"res-{exam_5_id}-{st_id}", exam_5_id, st_id, st_name, "cls-10a", "Grade 10A",
            att, score, 100.0, pct, letter, pts, fback, 0, "2026-07-21T11:00:00Z", now_ts
        ))

    # 6. World History Examination (Needs Correction - Principal Requested Change)
    exam_6_id = "EXM-2026-HIS-06"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_6_id,
        "World History — Modern Geopolitical Systems Evaluation",
        "midterm", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "history", "Social Studies Department", "subj-hum-hist", "World History",
        "TCH-2024-042", "Dr. Sarah Jenkins", json.dumps(["cls-10a", "cls-11b"]), json.dumps(["Grade 10A", "Grade 11B"]),
        "2026-07-24", "10:00", "12:00", 120,
        "room-301", "Room 301 — Humanities Lecture Room", 35,
        "Part A: Source Document Analysis (30 marks). Part B: Evaluative Essay on Cold War Treaties (70 marks).",
        100.0, 60.0, 25.0,
        "20th Century Treaties, Decolonization & Global Institutions.",
        json.dumps([]),
        json.dumps([]),
        "needs_correction", "needs_correction", "pending", "not_started",
        "Please provide the full primary source document appendix and revise Section B question phrasing to specify the rubric weighting for historical evidence.",
        "Returned to Dr. Sarah Jenkins for document appendix addition.",
        "TCH-2024-042", "PRN-2024-002", "", "",
        "", "", "", "",
        "2026-06-10T11:00:00Z", now_ts
    ))

    # 7. Chemistry Practicum Evaluation (Teacher Draft)
    exam_7_id = "EXM-2026-CHM-07"
    conn.execute("""
        INSERT OR REPLACE INTO exams (
            id, title, exam_type, academic_year_id, term, campus_id, campus_name,
            department_id, department_name, subject_id, subject_name,
            teacher_id, teacher_name, class_ids, class_names,
            exam_date, start_time, end_time, duration_mins,
            room_id, room_name, seating_capacity, instructions,
            max_marks, passing_marks, weight_pct, syllabus,
            prep_resources_json, attachments_json,
            status, academic_status, operational_status, result_status,
            correction_notes, internal_notes,
            created_by, updated_by, approved_by, approved_at,
            published_by, published_at, results_published_by, results_published_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        exam_7_id,
        "Chemistry Practicum & Titration Lab Exam",
        "practical", "ay-2025-26", "Semester 2", "cam-tk", "Tuol Kork Main Campus",
        "science", "Science Department", "subj-chem", "Chemistry Practicum",
        "TCH-2024-042", "Dr. Sarah Jenkins", json.dumps(["cls-10a"]), json.dumps(["Grade 10A"]),
        "2026-07-28", "08:30", "10:30", 120,
        "room-201", "Room 201 — Science Lab", 30,
        "Acid-base titration lab stations. Lab goggles, closed-toe shoes, and lab notebooks mandatory.",
        50.0, 30.0, 20.0,
        "Volumetric Analysis, Stoichiometric Calculations & Laboratory Safety Protocols.",
        json.dumps([]),
        json.dumps([]),
        "draft", "draft", "pending", "not_started",
        "", "Draft in preparation by Dr. Sarah Jenkins.",
        "TCH-2024-042", "TCH-2024-042", "", "",
        "", "", "", "",
        "2026-06-25T15:00:00Z", now_ts
    ))

    # Seed Initial Audit Log
    audit_events = [
        (exam_1_id, "TCH-2024-042", "teacher", "Dr. Sarah Jenkins", "create", "", "draft", "Draft examination created.", now_ts),
        (exam_1_id, "TCH-2024-042", "teacher", "Dr. Sarah Jenkins", "submit", "draft", "submitted", "Submitted to Principal for academic review.", now_ts),
        (exam_1_id, "PRN-2024-002", "principal", "Dr. Ly Bunheng", "approve", "submitted", "approved", "Approved academic syllabus and exam specifications.", now_ts),
        (exam_1_id, "ADM-2024-001", "admin", "Sok Panha Heng", "confirm_operations", "pending", "confirmed", "Hall A reservation and audio broadcast verified.", now_ts),
        (exam_1_id, "ADM-2024-001", "admin", "Sok Panha Heng", "publish_exam", "approved", "published", "Official exam schedule published to student and teacher portals.", now_ts),
        (exam_1_id, "TCH-2024-042", "teacher", "Dr. Sarah Jenkins", "submit_grades", "draft", "submitted", "Entered student marks and submitted for results clearance.", now_ts),
        (exam_1_id, "PRN-2024-002", "principal", "Dr. Ly Bunheng", "publish_results", "submitted", "published", "Authorized publication of student marks and feedback.", now_ts),
        (exam_4_id, "TCH-2024-023", "teacher", "Mr. Chea Sophea", "submit", "draft", "submitted", "Submitted Khmer Literature final test for review.", now_ts),
        (exam_6_id, "PRN-2024-002", "principal", "Dr. Ly Bunheng", "request_correction", "submitted", "needs_correction", "Requested primary source document appendix.", now_ts),
    ]
    for ev in audit_events:
        conn.execute("""
            INSERT INTO exam_audit_log (exam_id, actor_id, actor_role, actor_name, action, previous_state, new_state, notes, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ev)

def _get_current_actor(req):
    """Resolve actor from the real identity store, with a demo-portal fallback.

    Browser pages send X-Actor (or persist ngis_actor) with the signed-in email.
    We resolve that through user_accounts.json so permissions follow the actual
    teacher / student / principal record instead of a shared demo identifier.
    """
    identity_value = (
        req.headers.get('X-Actor')
        or req.cookies.get('ngis_actor')
        or req.args.get('actor')
        or ''
    )
    resolved = _resolve_identity(identity_value)
    if resolved:
        return resolved

    auth_h = req.headers.get('Authorization', '')
    token = auth_h[7:].strip() if auth_h.startswith('Bearer ') else ''
    if token.startswith('mock-jwt-token-'):
        token_role = _normalise_role(token[len('mock-jwt-token-'):])
        token_identity = _resolve_identity(token_role + '@ngis.edu.kh')
        if token_identity:
            return token_identity

    actor_role = _normalise_role(
        req.headers.get('X-Actor-Role') or req.args.get('portal') or req.args.get('role') or ''
    )
    actor_id = req.headers.get('X-Actor-Id') or req.args.get('actor_id') or ''

    names = {
        'admin': ('ADM-2024-001', 'Sok Panha Heng'),
        'principal': ('PRN-2024-002', 'Dr. Ly Bunheng'),
        'teacher': ('TCH-2024-042', 'Dr. Sarah Jenkins'),
        'student': ('2026-STD-0142', 'Nrinphouneta Hok'),
        'superadmin': ('SUP-2024-001', 'Sok Panha Heng'),
    }
    default_id, default_name = names.get(actor_role, ('ADM-2024-001', 'Sok Panha Heng'))
    if not actor_role:
        actor_role = 'admin'
    return {
        'id': actor_id or default_id,
        'role': actor_role if actor_role in names else 'admin',
        'name': default_name,
        'email': '',
        'campus': '',
        'department': '',
    }

def _log_audit(exam_id, actor, action, prev_state, new_state, notes="", details=None):
    try:
        conn = _conn()
        conn.execute("""
            INSERT INTO exam_audit_log (exam_id, actor_id, actor_role, actor_name, action, previous_state, new_state, notes, details_json, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            exam_id, actor['id'], actor['role'], actor['name'],
            action, prev_state, new_state, notes,
            json.dumps(details or {}), _now()
        ))
        conn.close()
    except Exception as e:
        print(f"Error logging exam audit event: {e}")

# ── API ROUTES ──────────────────────────────────────────────────────────────

@exam_bp.route('/api/exams', methods=['GET'])
def list_exams():
    """Retrieve exams filtered by search, department, class, status, or role."""
    init_exam_schema()
    actor = _get_current_actor(request)
    dept = request.args.get('dept', '').strip().lower()
    status = request.args.get('status', '').strip().lower()
    campus = request.args.get('campus', '').strip().lower()
    q = request.args.get('q', '').strip().lower()

    conn = _conn()
    try:
        sql = "SELECT * FROM exams WHERE 1=1"
        args = []

        # Role-based visibility
        if actor['role'] == 'student':
            # Students only see published, completed, results_processing, or results_published
            sql += " AND status IN ('published', 'completed', 'results_processing', 'results_published')"
        elif actor['role'] == 'teacher':
            # Teachers see exams they created or for classes/subjects they teach
            sql += " AND (teacher_id = ? OR class_ids LIKE ?)"
            args.extend([actor['id'], f'%"{actor["id"]}"%'])

        if dept and dept != 'all':
            sql += " AND (LOWER(department_id) = ? OR LOWER(department_name) LIKE ?)"
            args.extend([dept, f"%{dept}%"])

        if status and status != 'all':
            sql += " AND LOWER(status) = ?"
            args.append(status)

        if campus and campus != 'all':
            sql += " AND (LOWER(campus_id) = ? OR LOWER(campus_name) LIKE ?)"
            args.extend([campus, f"%{campus}%"])

        sql += " ORDER BY exam_date ASC, start_time ASC"
        rows = conn.execute(sql, args).fetchall()

        results = []
        for r in rows:
            d = dict(r)
            d['class_ids'] = json.loads(d.get('class_ids') or '[]')
            d['class_names'] = json.loads(d.get('class_names') or '[]')
            d['prep_resources'] = json.loads(d.get('prep_resources_json') or '[]')
            d['attachments'] = json.loads(d.get('attachments_json') or '[]')

            # Search filter
            if q:
                match_txt = f"{d['title']} {d['subject_name']} {d['department_name']} {d['room_name']}".lower()
                if q not in match_txt:
                    continue

            # Student guard: Don't leak raw marks unless results are officially published
            if actor['role'] == 'student' and d['result_status'] != 'published':
                d['has_published_results'] = False
            else:
                d['has_published_results'] = (d['result_status'] == 'published')

            results.append(d)

        # Overview statistics
        all_exams = conn.execute("SELECT status, academic_status, operational_status, result_status FROM exams").fetchall()
        stats = {
            'total': len(all_exams),
            'published': sum(1 for e in all_exams if e['status'] in ('published', 'completed', 'results_published')),
            'draft': sum(1 for e in all_exams if e['status'] == 'draft'),
            'pending_review': sum(1 for e in all_exams if e['academic_status'] == 'pending'),
            'needs_correction': sum(1 for e in all_exams if e['academic_status'] == 'needs_correction'),
            'awaiting_grading': sum(1 for e in all_exams if e['status'] in ('published', 'completed') and e['result_status'] in ('not_started', 'draft')),
            'results_pending_approval': sum(1 for e in all_exams if e['result_status'] == 'submitted'),
            'results_published': sum(1 for e in all_exams if e['result_status'] == 'published'),
            'conflicts': sum(1 for e in all_exams if e['operational_status'] == 'conflict_detected')
        }

        return jsonify({'success': True, 'data': results, 'stats': stats, 'actor': actor})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>', methods=['GET'])
def get_exam_detail(exam_id):
    """Retrieve full details, enrolled roster, grading, and audit log."""
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': f"Exam '{exam_id}' not found."}), 404

        exam = dict(row)
        exam['class_ids'] = json.loads(exam.get('class_ids') or '[]')
        exam['class_names'] = json.loads(exam.get('class_names') or '[]')
        exam['prep_resources'] = json.loads(exam.get('prep_resources_json') or '[]')
        exam['attachments'] = json.loads(exam.get('attachments_json') or '[]')

        # Role restrictions
        if actor['role'] == 'student':
            if exam['status'] not in ('published', 'completed', 'results_processing', 'results_published'):
                return jsonify({'success': False, 'error': "This examination is not currently published."}), 403

        # Retrieve enrolled student results
        results_rows = conn.execute("""
            SELECT * FROM exam_student_results WHERE exam_id = ? ORDER BY class_name ASC, student_name ASC
        """, (exam_id,)).fetchall()

        if len(results_rows) == 0:
            cids = json.loads(exam.get('class_ids') or '[]')
            _populate_exam_roster(conn, exam_id, cids, float(exam.get('max_marks') or 100.0))
            results_rows = conn.execute("""
                SELECT * FROM exam_student_results WHERE exam_id = ? ORDER BY class_name ASC, student_name ASC
            """, (exam_id,)).fetchall()

        results_list = []
        for r in results_rows:
            rd = dict(r)
            rd['correction_history'] = json.loads(rd.get('correction_history_json') or '[]')

            # If actor is student, only return their own record, and only if results are published
            if actor['role'] == 'student':
                if rd['student_id'] == actor['id']:
                    if exam['result_status'] == 'published':
                        results_list.append(rd)
                    else:
                        # Redact marks if unpublished
                        rd['score'] = None
                        rd['percentage'] = None
                        rd['letter_grade'] = ''
                        rd['gpa_points'] = None
                        rd['teacher_feedback'] = ''
                        results_list.append(rd)
            else:
                results_list.append(rd)

        exam['results'] = results_list

        # Retrieve audit trail
        audit_rows = conn.execute("""
            SELECT * FROM exam_audit_log WHERE exam_id = ? ORDER BY id DESC
        """, (exam_id,)).fetchall()
        exam['audit_log'] = [dict(a) for a in audit_rows]

        return jsonify({'success': True, 'data': exam, 'actor': actor})
    finally:
        conn.close()

@exam_bp.route('/api/exams', methods=['POST'])
def create_exam():
    """Create a new exam (Teacher or Admin)."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ('teacher', 'admin', 'principal'):
        return jsonify({'success': False, 'error': "Permission denied: only teachers or administrators may create exams."}), 403

    data = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'success': False, 'error': "Examination title is required."}), 400

    exam_date = data.get('exam_date') or ''
    start_time = data.get('start_time') or '09:00'
    end_time = data.get('end_time') or '10:30'
    room_id = data.get('room_id') or 'room-hall-b'
    room_name = data.get('room_name') or 'Hall B · Desk #42'
    class_ids = data.get('class_ids') or ['cls-10a']
    class_names = data.get('class_names') or ['Grade 10A']
    submit_for_review = bool(data.get('submit_for_review', False))

    # Conflict check
    conflict = _check_schedule_conflict(None, exam_date, start_time, end_time, room_id, class_ids)
    if conflict:
        return jsonify({'success': False, 'error': f"Scheduling conflict: {conflict}"}), 409

    now_ts = _now()
    exam_id = f"EXM-{datetime.now().year}-{data.get('department_id', 'GEN')[:3].upper()}-{int(datetime.now().timestamp()) % 100000:05d}"

    status = 'submitted' if submit_for_review else 'draft'
    academic_status = 'pending' if submit_for_review else 'draft'

    conn = _conn()
    try:
        conn.execute("""
            INSERT INTO exams (
                id, title, exam_type, academic_year_id, term, campus_id, campus_name,
                department_id, department_name, subject_id, subject_name,
                teacher_id, teacher_name, class_ids, class_names,
                exam_date, start_time, end_time, duration_mins,
                room_id, room_name, seating_capacity, instructions,
                max_marks, passing_marks, weight_pct, syllabus,
                prep_resources_json, attachments_json,
                status, academic_status, operational_status, result_status,
                correction_notes, internal_notes,
                created_by, updated_by, created_at, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            exam_id, title, data.get('exam_type', 'midterm'),
            data.get('academic_year_id', 'ay-2025-26'), data.get('term', 'Semester 2'),
            data.get('campus_id', 'cam-tk'), data.get('campus_name', 'Tuol Kork Main Campus'),
            data.get('department_id', 'english'), data.get('department_name', 'English Department'),
            data.get('subject_id', 'subj-eng'), data.get('subject_name', 'English Literature'),
            actor['id'], actor['name'],
            json.dumps(class_ids), json.dumps(class_names),
            exam_date, start_time, end_time, int(data.get('duration_mins', 90)),
            room_id, room_name, int(data.get('seating_capacity', 35)),
            data.get('instructions', ''),
            float(data.get('max_marks', 100.0)), float(data.get('passing_marks', 60.0)),
            float(data.get('weight_pct', 25.0)), data.get('syllabus', ''),
            json.dumps(data.get('prep_resources', [])), json.dumps(data.get('attachments', [])),
            status, academic_status, 'pending', 'not_started',
            '', '',
            actor['id'], actor['id'], now_ts, now_ts
        ))

        # Auto-enroll students belonging to selected class_ids into exam_student_results
        _populate_exam_roster(conn, exam_id, class_ids, float(data.get('max_marks', 100.0)))

        _log_audit(exam_id, actor, 'create', '', status, "Exam created in system.", {'title': title, 'classes': class_names})
        if submit_for_review:
            _log_audit(exam_id, actor, 'submit', 'draft', 'submitted', "Submitted directly to Principal for academic oversight.")

        return jsonify({'success': True, 'data': {'id': exam_id, 'status': status, 'academic_status': academic_status}}), 201
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>', methods=['PUT'])
def update_exam(exam_id):
    """Update exam details."""
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404

        current = dict(row)
        # Check permissions: teacher can only edit own drafts/needs_correction; admin can edit; principal can edit
        if actor['role'] == 'teacher':
            if current['teacher_id'] != actor['id']:
                return jsonify({'success': False, 'error': "You can only edit examinations you authored."}), 403
            if current['academic_status'] in ('approved', 'rejected') and current['status'] == 'published':
                return jsonify({'success': False, 'error': "Cannot silently modify an approved and published examination."}), 400

        data = request.get_json(silent=True) or {}
        now_ts = _now()

        # Check schedule conflict if date/time/room changed
        exam_date = data.get('exam_date', current['exam_date'])
        start_time = data.get('start_time', current['start_time'])
        end_time = data.get('end_time', current['end_time'])
        room_id = data.get('room_id', current['room_id'])
        class_ids = data.get('class_ids', json.loads(current.get('class_ids') or '[]'))

        if exam_date != current['exam_date'] or start_time != current['start_time'] or room_id != current['room_id']:
            conflict = _check_schedule_conflict(exam_id, exam_date, start_time, end_time, room_id, class_ids)
            if conflict:
                return jsonify({'success': False, 'error': f"Scheduling conflict: {conflict}"}), 409

        conn.execute("""
            UPDATE exams SET
                title = ?, exam_type = ?, term = ?, campus_id = ?, campus_name = ?,
                department_id = ?, department_name = ?, subject_id = ?, subject_name = ?,
                class_ids = ?, class_names = ?,
                exam_date = ?, start_time = ?, end_time = ?, duration_mins = ?,
                room_id = ?, room_name = ?, seating_capacity = ?, instructions = ?,
                max_marks = ?, passing_marks = ?, weight_pct = ?, syllabus = ?,
                prep_resources_json = ?, attachments_json = ?,
                updated_by = ?, updated_at = ?
            WHERE id = ?
        """, (
            data.get('title', current['title']),
            data.get('exam_type', current['exam_type']),
            data.get('term', current['term']),
            data.get('campus_id', current['campus_id']),
            data.get('campus_name', current['campus_name']),
            data.get('department_id', current['department_id']),
            data.get('department_name', current['department_name']),
            data.get('subject_id', current['subject_id']),
            data.get('subject_name', current['subject_name']),
            json.dumps(class_ids),
            json.dumps(data.get('class_names', json.loads(current.get('class_names') or '[]'))),
            exam_date, start_time, end_time,
            int(data.get('duration_mins', current['duration_mins'])),
            room_id, data.get('room_name', current['room_name']),
            int(data.get('seating_capacity', current['seating_capacity'])),
            data.get('instructions', current['instructions']),
            float(data.get('max_marks', current['max_marks'])),
            float(data.get('passing_marks', current['passing_marks'])),
            float(data.get('weight_pct', current['weight_pct'])),
            data.get('syllabus', current['syllabus']),
            json.dumps(data.get('prep_resources', json.loads(current.get('prep_resources_json') or '[]'))),
            json.dumps(data.get('attachments', json.loads(current.get('attachments_json') or '[]'))),
            actor['id'], now_ts, exam_id
        ))

        _log_audit(exam_id, actor, 'update', current['status'], current['status'], "Exam specification updated.")
        return jsonify({'success': True, 'message': "Examination updated successfully."})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    """Delete or archive an examination (Admin only, or Teacher for draft)."""
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        if current['result_status'] == 'published':
            return jsonify({'success': False, 'error': "Cannot delete an examination with published student results."}), 400

        conn.execute("DELETE FROM exams WHERE id = ?", (exam_id,))
        conn.execute("DELETE FROM exam_student_results WHERE exam_id = ?", (exam_id,))
        _log_audit(exam_id, actor, 'delete', current['status'], 'deleted', "Exam record deleted by administrator.")
        return jsonify({'success': True, 'message': f"Exam '{exam_id}' deleted successfully."})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/unpublish', methods=['POST'])
def unpublish_exam(exam_id):
    """Admin unpublishes an exam back to draft (if results not yet published)."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ('admin', 'principal', 'superadmin'):
        return jsonify({'success': False, 'error': "Permission denied."}), 403
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)
        if current['result_status'] == 'published':
            return jsonify({'success': False, 'error': "Cannot unpublish an exam whose results are officially published."}), 400

        now_ts = _now()
        conn.execute("UPDATE exams SET status = 'draft', updated_at = ? WHERE id = ?", (now_ts, exam_id))
        _log_audit(exam_id, actor, 'unpublish', current['status'], 'draft', "Exam timetable unpublished by administrator.")
        return jsonify({'success': True, 'message': f"Exam '{exam_id}' unpublished."})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/submit', methods=['POST'])
def submit_exam_for_review(exam_id):
    """Teacher submits draft or corrected exam to Principal for academic review."""
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        if actor['role'] == 'teacher' and current['teacher_id'] != actor['id']:
            return jsonify({'success': False, 'error': "You can only submit examinations you authored."}), 403

        now_ts = _now()
        conn.execute("""
            UPDATE exams SET
                status = 'submitted',
                academic_status = 'pending',
                updated_by = ?,
                updated_at = ?
            WHERE id = ?
        """, (actor['id'], now_ts, exam_id))

        _log_audit(exam_id, actor, 'submit', current['status'], 'submitted', "Examination submitted to Principal for academic review.")
        return jsonify({'success': True, 'message': "Examination submitted for Principal review."})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/review', methods=['POST'])
def principal_review_exam(exam_id):
    """Principal approves, requests correction, or rejects an exam proposal."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': "Only the Principal may approve academic examination content."}), 403

    data = request.get_json(silent=True) or {}
    decision = (data.get('decision') or '').strip().lower() # 'approve', 'request_correction', 'reject'
    reason = (data.get('reason') or '').strip()
    internal_notes = (data.get('internal_notes') or '').strip()

    if decision in ('request_correction', 'reject') and not reason:
        return jsonify({'success': False, 'error': "A documented reason is mandatory when requesting corrections or rejecting an examination."}), 400

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        now_ts = _now()
        if decision == 'approve':
            new_status = 'approved'
            academic_status = 'approved'
            notes = reason or "Approved academic syllabus and exam specifications."
            conn.execute("""
                UPDATE exams SET
                    status = ?, academic_status = ?, approved_by = ?, approved_at = ?,
                    internal_notes = ?, updated_by = ?, updated_at = ?
                WHERE id = ?
            """, (new_status, academic_status, actor['id'], now_ts, internal_notes, actor['id'], now_ts, exam_id))
        elif decision == 'request_correction':
            new_status = 'needs_correction'
            academic_status = 'needs_correction'
            notes = reason
            conn.execute("""
                UPDATE exams SET
                    status = ?, academic_status = ?, correction_notes = ?, internal_notes = ?,
                    updated_by = ?, updated_at = ?
                WHERE id = ?
            """, (new_status, academic_status, reason, internal_notes, actor['id'], now_ts, exam_id))
        elif decision == 'reject':
            new_status = 'rejected'
            academic_status = 'rejected'
            notes = reason
            conn.execute("""
                UPDATE exams SET
                    status = ?, academic_status = ?, correction_notes = ?, internal_notes = ?,
                    updated_by = ?, updated_at = ?
                WHERE id = ?
            """, (new_status, academic_status, reason, internal_notes, actor['id'], now_ts, exam_id))
        else:
            return jsonify({'success': False, 'error': f"Invalid decision '{decision}'. Use 'approve', 'request_correction', or 'reject'."}), 400

        _log_audit(exam_id, actor, decision, current['academic_status'], academic_status, notes, {'internal_notes': internal_notes})
        return jsonify({'success': True, 'message': f"Academic decision '{decision}' recorded successfully.", 'academic_status': academic_status})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/operational-check', methods=['POST'])
def admin_operational_check(exam_id):
    """Admin confirms operational readiness and resolves room/session allocations."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ('admin', 'principal', 'superadmin'):
        return jsonify({'success': False, 'error': "Permission denied: admin role required for operational readiness."}), 403

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        class_ids = json.loads(current.get('class_ids') or '[]')
        conflict = _check_schedule_conflict(exam_id, current['exam_date'], current['start_time'], current['end_time'], current['room_id'], class_ids)

        now_ts = _now()
        if conflict:
            conn.execute("UPDATE exams SET operational_status = 'conflict_detected', updated_at = ? WHERE id = ?", (now_ts, exam_id))
            _log_audit(exam_id, actor, 'conflict_detected', current['operational_status'], 'conflict_detected', conflict)
            return jsonify({'success': False, 'conflict': conflict, 'operational_status': 'conflict_detected'})

        conn.execute("UPDATE exams SET operational_status = 'confirmed', updated_at = ? WHERE id = ?", (now_ts, exam_id))
        _log_audit(exam_id, actor, 'confirm_operations', current['operational_status'], 'confirmed', "Room allocation, seating, and invigilator readiness verified.")
        return jsonify({'success': True, 'message': "Operational readiness confirmed without conflict.", 'operational_status': 'confirmed'})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/publish', methods=['POST'])
def publish_exam(exam_id):
    """Publish examination schedule to students (Requires Principal approval!)."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': "Only the Principal may publish examination schedules."}), 403

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        # STRICT ACADEMIC CONSTRAINT: Cannot publish without Principal academic approval!
        if current['academic_status'] != 'approved':
            return jsonify({'success': False, 'error': "Cannot publish examination: Principal academic approval is required before release."}), 400

        now_ts = _now()
        conn.execute("""
            UPDATE exams SET
                status = 'published',
                operational_status = 'confirmed',
                published_by = ?,
                published_at = ?,
                updated_by = ?,
                updated_at = ?
            WHERE id = ?
        """, (actor['id'], now_ts, actor['id'], now_ts, exam_id))

        _log_audit(exam_id, actor, 'publish_exam', current['status'], 'published', "Official exam timetable published to student and teacher portals.")
        return jsonify({'success': True, 'message': "Examination timetable published successfully."})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/grades', methods=['GET'])
def get_exam_grades(exam_id):
    """Retrieve enrolled student roster and recorded marks."""
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        exam = dict(row)

        # Retrieve student results
        results = conn.execute("""
            SELECT * FROM exam_student_results WHERE exam_id = ? ORDER BY class_name ASC, student_name ASC
        """, (exam_id,)).fetchall()

        if len(results) == 0:
            cids = json.loads(exam.get('class_ids') or '[]')
            _populate_exam_roster(conn, exam_id, cids, float(exam.get('max_marks') or 100.0))
            results = conn.execute("""
                SELECT * FROM exam_student_results WHERE exam_id = ? ORDER BY class_name ASC, student_name ASC
            """, (exam_id,)).fetchall()

        roster = [dict(r) for r in results]
        return jsonify({'success': True, 'exam': exam, 'data': roster})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/grades', methods=['POST', 'PUT'])
def save_exam_grades(exam_id):
    """Teacher records attendance and enters student exam marks."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ('teacher', 'principal', 'admin', 'superadmin'):
        return jsonify({'success': False, 'error': "Permission denied: teacher role required to record examination grades."}), 403

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        if current['result_status'] == 'published' and actor['role'] == 'teacher':
            return jsonify({'success': False, 'error': "Results have been published and locked. Contact the Principal to reopen grading."}), 400

        data = request.get_json(silent=True) or {}
        grades_list = data.get('grades') or []
        submit_results = bool(data.get('submit_for_approval', False))

        now_ts = _now()
        max_marks = float(current['max_marks'])

        for g in grades_list:
            st_id = g.get('student_id')
            if not st_id: continue
            att = g.get('attendance_status', 'present')
            raw_score = g.get('score')
            score = float(raw_score) if raw_score is not None and str(raw_score).strip() != '' else None
            if score is not None:
                score = min(max(0.0, score), max_marks)
            feedback = g.get('teacher_feedback', '').strip()

            pct, letter, pts = _calc_grade_and_points(score, max_marks)

            conn.execute("""
                UPDATE exam_student_results SET
                    attendance_status = ?,
                    score = ?,
                    percentage = ?,
                    letter_grade = ?,
                    gpa_points = ?,
                    teacher_feedback = ?,
                    updated_at = ?
                WHERE exam_id = ? AND student_id = ?
            """, (att, score, pct, letter, pts, feedback, now_ts, exam_id, st_id))

        new_result_status = 'submitted' if submit_results else 'draft'
        new_lifecycle = 'results_processing' if submit_results else current['status']

        conn.execute("""
            UPDATE exams SET
                result_status = ?,
                status = ?,
                updated_by = ?,
                updated_at = ?
            WHERE id = ?
        """, (new_result_status, new_lifecycle, actor['id'], now_ts, exam_id))

        action_name = 'submit_grades' if submit_results else 'record_grades'
        _log_audit(exam_id, actor, action_name, current['result_status'], new_result_status,
                   "Exam grades and attendance records updated.", {'count': len(grades_list), 'submitted': submit_results})

        return jsonify({'success': True, 'message': "Grades saved successfully.", 'result_status': new_result_status})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/approve-results', methods=['POST'])
def approve_exam_results(exam_id):
    """Principal approves teacher-submitted results or returns for correction."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': "Only the Principal may approve examination results."}), 403

    data = request.get_json(silent=True) or {}
    decision = (data.get('decision') or 'approve').strip().lower()
    reason = (data.get('reason') or '').strip()

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        now_ts = _now()
        if decision == 'approve':
            new_status = 'approved'
            conn.execute("UPDATE exams SET result_status = 'approved', updated_at = ? WHERE id = ?", (now_ts, exam_id))
            _log_audit(exam_id, actor, 'approve_grades', current['result_status'], 'approved', "Principal approved grade completeness and class distribution.")
        elif decision == 'request_correction':
            new_status = 'needs_correction'
            conn.execute("UPDATE exams SET result_status = 'needs_correction', correction_notes = ?, updated_at = ? WHERE id = ?", (reason, now_ts, exam_id))
            _log_audit(exam_id, actor, 'return_grades', current['result_status'], 'needs_correction', reason)
        else:
            return jsonify({'success': False, 'error': "Invalid decision."}), 400

        return jsonify({'success': True, 'result_status': new_status})
    finally:
        conn.close()

@exam_bp.route('/api/exams/<exam_id>/publish-results', methods=['POST'])
def publish_exam_results(exam_id):
    """Authorize release of grades to student and parent portals."""
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': "Only the Principal may publish examination results."}), 403

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id = ?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': "Exam not found."}), 404
        current = dict(row)

        now_ts = _now()
        conn.execute("""
            UPDATE exams SET
                result_status = 'published',
                status = 'results_published',
                results_published_by = ?,
                results_published_at = ?,
                updated_by = ?,
                updated_at = ?
            WHERE id = ?
        """, (actor['id'], now_ts, actor['id'], now_ts, exam_id))

        # Lock student result rows
        conn.execute("UPDATE exam_student_results SET is_locked = 1 WHERE exam_id = ?", (exam_id,))

        _log_audit(exam_id, actor, 'publish_results', current['result_status'], 'published', "Results released to student portal.")
        return jsonify({'success': True, 'message': "Examination results published successfully."})
    finally:
        conn.close()

@exam_bp.route('/api/exams/student', methods=['GET'])
def get_student_exams():
    """Personal examination calendar: published exams for real enrolled classes only."""
    init_exam_schema()
    actor = _get_current_actor(request)
    requested_id = (request.args.get('student_id') or '').strip()
    if requested_id and requested_id != actor['id'] and actor['role'] not in STAFF_ROLES:
        return jsonify({'success': False, 'error': 'You may only view your own examination schedule.'}), 403
    student_id = requested_id or actor['id']

    exam_type = (request.args.get('exam_type') or request.args.get('type') or '').strip().lower()
    month = (request.args.get('month') or '').strip()
    dept_raw = str(request.args.get('dept') or '').strip().lower()
    dept_canonical = _canonical_department_id(dept_raw).lower()

    conn = _conn()
    try:
        enrollments = conn.execute(
            "SELECT class_id FROM enrollments WHERE student_id=? AND (status='active' OR status='' OR status IS NULL)",
            (student_id,),
        ).fetchall()
        enrolled_class_ids = [r['class_id'] for r in enrollments]

        rows = conn.execute(
            "SELECT * FROM exams WHERE status IN "
            "('published', 'completed', 'results_processing', 'results_published') "
            "ORDER BY exam_date ASC, start_time ASC"
        ).fetchall()

        now_dt = datetime.now()
        exams = []
        for row in rows:
            data = _simplified_exam(row)
            class_ids = data['class_ids']
            if not any(cid in enrolled_class_ids for cid in class_ids):
                continue
            if exam_type and exam_type != 'all' and data['exam_type'] != _canonical_exam_type(exam_type):
                continue
            if month and month != 'all' and not str(data['exam_date']).startswith(month):
                continue
            if dept_raw and dept_raw != 'all':
                row_dept = str(data['department_id'] or '').lower()
                row_dept_canonical = _canonical_department_id(row_dept).lower()
                haystack = (row_dept + ' ' + row_dept_canonical + ' ' +
                            data['department'] + ' ' + data['subject']).lower()
                wanted = {dept_raw, dept_canonical}
                if not (wanted & {row_dept, row_dept_canonical}) and not any(token in haystack for token in wanted):
                    continue

            try:
                exam_dt = datetime.strptime(data['exam_date'] + ' ' + data['end_time'], '%Y-%m-%d %H:%M')
            except Exception:
                try:
                    exam_dt = datetime.strptime(data['exam_date'], '%Y-%m-%d')
                except Exception:
                    exam_dt = None
            data['completed'] = bool(exam_dt and exam_dt < now_dt)
            exams.append(data)

        upcoming = [e for e in exams if not e['completed']]
        completed = [e for e in exams if e['completed']]
        months = sorted({e['exam_date'][:7] for e in exams if e['exam_date']})

        student_name = actor['name'] if actor['id'] == student_id else student_id
        if actor['id'] != student_id:
            try:
                profile = conn.execute("SELECT name FROM students WHERE id=?", (student_id,)).fetchone()
                if profile:
                    student_name = profile['name']
            except Exception:
                pass

        return jsonify({
            'success': True,
            'student_id': student_id,
            'student_name': student_name,
            'enrolled_classes': enrolled_class_ids,
            'exams': exams,
            'upcoming': upcoming,
            'completed': completed,
            'months': months,
            'types': [{'id': k, 'label': v} for k, v in EXAM_TYPES.items()],
            'next_exam': upcoming[0] if upcoming else None,
            'roadmap': exams,          # legacy key for older bookmarks
            'published_results': [],   # result data is intentionally not part of this workspace
            'total_count': len(exams),
        })
    finally:
        conn.close()

# ── SIMPLIFIED EXAMINATION SCHEDULING WORKSPACE ──────────────────────────
# Teachers create schedules, Principals review/publish, Admins monitor,
# students only see published schedules for their own enrolled classes.

def _simple_conflict(conn, exam_id, exam_date, start_time, end_time, class_ids, subject_id, exam_type):
    if not (exam_date and start_time and end_time):
        return None
    rows = conn.execute(
        "SELECT id, title, class_ids, subject_id, exam_type, start_time, end_time "
        "FROM exams WHERE exam_date=? AND status NOT IN ('cancelled', 'rejected')",
        (exam_date,),
    ).fetchall()
    for row in rows:
        if exam_id and row['id'] == exam_id:
            continue
        if not (start_time < row['end_time'] and end_time > row['start_time']):
            continue
        shared = set(class_ids or []).intersection(set(_json_list(row['class_ids'])))
        if shared:
            return "Class {0} already has '{1}' at {2}–{3}.".format(
                sorted(shared)[0], row['title'], row['start_time'], row['end_time'])
        if subject_id and row['subject_id'] == subject_id and _canonical_exam_type(row['exam_type']) == exam_type:
            return "A {0} for this subject is already scheduled on this date.".format(EXAM_TYPES[exam_type])
    return None

def _validate_simple_payload(conn, data, actor):
    if actor['role'] not in ('teacher', 'principal', 'superadmin', 'admin'):
        return None, (jsonify({'success': False, 'error': 'Permission denied.'}), 403)

    department_id = _canonical_department_id(data.get('department_id'))
    subject_id = str(data.get('subject_id') or '').strip()
    exam_type = _canonical_exam_type(data.get('exam_type'))
    exam_date = str(data.get('exam_date') or '').strip()
    start_time = str(data.get('start_time') or '').strip()
    end_time = str(data.get('end_time') or '').strip()
    class_ids = [str(c).strip() for c in (data.get('class_ids') or []) if str(c).strip()]

    if exam_type not in EXAM_TYPES:
        return None, (jsonify({'success': False, 'error': 'Unsupported examination type.'}), 400)
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', exam_date):
        return None, (jsonify({'success': False, 'error': 'A valid examination date is required.'}), 400)
    if not re.fullmatch(r'\d{2}:\d{2}', start_time) or not re.fullmatch(r'\d{2}:\d{2}', end_time):
        return None, (jsonify({'success': False, 'error': 'Valid start and end times are required.'}), 400)
    if start_time >= end_time:
        return None, (jsonify({'success': False, 'error': 'End time must be after start time.'}), 400)
    if not class_ids:
        return None, (jsonify({'success': False, 'error': 'Select at least one class.'}), 400)

    subject = conn.execute("SELECT id, name FROM subjects WHERE id=?", (subject_id,)).fetchone()
    if not subject:
        return None, (jsonify({'success': False, 'error': 'Select a valid subject from the school catalogue.'}), 400)

    directory = _directory_maps(conn)
    class_names = {c['id']: c['name'] for c in directory['classes']}
    missing = [c for c in class_ids if c not in class_names]
    if missing:
        return None, (jsonify({'success': False, 'error': 'Unknown class: ' + ', '.join(missing)}), 400)

    if actor['role'] == 'teacher':
        scope = _teacher_assignments(conn, actor['id'])
        unauthorised = [(sid, cid) for sid, cid in ((subject_id, c) for c in class_ids)
                        if (sid, cid) not in scope['pairs']]
        if unauthorised:
            return None, (jsonify({
                'success': False,
                'error': 'You can only schedule examinations for subjects and classes assigned to you.'
            }), 403)
        if department_id and scope['departments'] and department_id not in scope['departments']:
            return None, (jsonify({'success': False, 'error': 'This department is outside your assignment.'}), 403)

    if actor['role'] == 'principal':
        own_dept = _canonical_department_id(actor.get('department')).lower()
        if own_dept and department_id and department_id.lower() not in own_dept and _department_name(department_id).lower() not in own_dept:
            return None, (jsonify({'success': False, 'error': 'This department is outside your assigned scope.'}), 403)

    dept_name = _department_name(department_id)
    campus_id = str(data.get('campus_id') or '').strip()
    campus_name = ''
    for campus in directory['campuses']:
        if campus_id and str(campus['id']).lower() == campus_id.lower():
            campus_name = campus['name']
            break
    if not campus_name and campus_id:
        campus_name = campus_id
    if not campus_id and actor.get('campus'):
        for campus in directory['campuses']:
            if str(campus['name']).lower() == str(actor['campus']).lower():
                campus_id, campus_name = campus['id'], campus['name']
                break

    try:
        datetime.strptime(exam_date, '%Y-%m-%d')
    except Exception:
        return None, (jsonify({'success': False, 'error': 'Invalid examination date.'}), 400)

    return {
        'title': '{0} — {1}'.format(subject['name'], EXAM_TYPES[exam_type]),
        'exam_type': exam_type,
        'department_id': department_id,
        'department_name': dept_name,
        'subject_id': subject_id,
        'subject_name': subject['name'],
        'class_ids': class_ids,
        'class_names': [class_names[c] for c in class_ids],
        'exam_date': exam_date,
        'start_time': start_time,
        'end_time': end_time,
        'campus_id': campus_id,
        'campus_name': campus_name,
    }, None

def _simple_query(conn, actor, args):
    role = actor['role']
    if role not in STAFF_ROLES:
        return None, (jsonify({'success': False, 'error': 'This workspace is not available to students.'}), 403)

    sql = "SELECT * FROM exams WHERE status NOT IN ('deleted')"
    params = []
    if role == 'teacher':
        scope = _teacher_assignments(conn, actor['id'])
        if not scope['pairs']:
            return [], None
        sql += " AND teacher_id=?"
        params.append(actor['id'])
    elif role == 'principal':
        own_dept = _canonical_department_id(actor.get('department')).lower()
        if own_dept:
            sql += " AND (LOWER(department_id)=? OR LOWER(department_name) LIKE ?)"
            params.extend([own_dept, '%' + own_dept + '%'])

    q = str(args.get('q') or '').strip().lower()
    exam_type = str(args.get('exam_type') or args.get('type') or '').strip().lower()
    status = str(args.get('status') or '').strip().lower()
    month = str(args.get('month') or '').strip()
    dept = _canonical_department_id(args.get('dept')).lower()
    campus = str(args.get('campus') or '').strip().lower()
    class_id = str(args.get('class_id') or '').strip()

    if exam_type and exam_type != 'all':
        sql += " AND exam_type=?"
        params.append(_canonical_exam_type(exam_type))
    if status and status != 'all':
        if status == 'pending':
            sql += " AND academic_status='pending'"
        else:
            sql += " AND status=?"
            params.append(status)
    if month and month != 'all':
        sql += " AND substr(exam_date,1,7)=?"
        params.append(month)
    if dept and dept != 'all':
        sql += " AND (LOWER(department_id)=? OR LOWER(department_name) LIKE ?)"
        params.extend([dept, '%' + dept + '%'])
    if campus and campus != 'all':
        sql += " AND (LOWER(campus_id)=? OR LOWER(campus_name) LIKE ?)"
        params.extend([campus, '%' + campus + '%'])
    sql += " ORDER BY exam_date ASC, start_time ASC"
    rows = conn.execute(sql, params).fetchall()

    all_rows = [dict(r) for r in rows]
    if class_id and class_id != 'all':
        all_rows = [r for r in all_rows if class_id in _json_list(r.get('class_ids'))]
    if q:
        all_rows = [r for r in all_rows if q in (
            str(r.get('subject_name') or '') + ' ' + str(r.get('title') or '') + ' ' +
            str(r.get('department_name') or '') + ' ' +
            ' '.join(_json_list(r.get('class_names')))
        ).lower()]
    return all_rows, None

@exam_bp.route('/api/exams/options', methods=['GET'])
def get_exam_options():
    """Catalogue options for the create/edit form, scoped to the current actor."""
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        directory = _directory_maps(conn)
        if actor['role'] == 'teacher':
            scope = _teacher_assignments(conn, actor['id'])
            allowed_subjects = scope['subjects']
            allowed_classes = scope['classes']
            directory['subjects'] = [s for s in directory['subjects'] if s['id'] in allowed_subjects]
            directory['classes'] = [c for c in directory['classes'] if c['id'] in allowed_classes]
            directory['departments'] = [
                d for d in directory['departments'] if d['id'] in scope['departments']
            ] or directory['departments']
        elif actor['role'] == 'principal' and actor.get('department'):
            own_dept = _canonical_department_id(actor['department']).lower()
            directory['departments'] = [
                d for d in directory['departments']
                if own_dept in d['id'].lower() or own_dept in d['name'].lower()
            ] or directory['departments']
        assignments = []
        if actor['role'] == 'teacher':
            assignments = [
                {'subject_id': s, 'class_id': c}
                for s, c in sorted(_teacher_assignments(conn, actor['id'])['pairs'])
            ]
        return jsonify({
            'success': True,
            'actor': actor,
            'exam_types': [{'id': k, 'label': v} for k, v in EXAM_TYPES.items()],
            'assignments': assignments,
            **directory,
        })
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple', methods=['GET'])
def list_simple_exams():
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        rows, error = _simple_query(conn, actor, request.args)
        if error:
            return error
        conflict_ids = set()
        data = []
        for row in rows:
            exam = _simplified_exam(row)
            conflict = _simple_conflict(
                conn, row['id'], row['exam_date'], row['start_time'], row['end_time'],
                exam['class_ids'], row['subject_id'], exam['exam_type'])
            exam['conflict'] = bool(conflict)
            exam['conflict_message'] = conflict or ''
            if conflict:
                conflict_ids.add(row['id'])
            data.append(exam)

        counts = {}
        for exam in data:
            counts[exam['status']] = counts.get(exam['status'], 0) + 1
        stats = {
            'total': len(data),
            'draft': counts.get('draft', 0),
            'pending_review': sum(1 for e in data if e['status'] == 'submitted' or e['academic_status'] == 'pending'),
            'changes_requested': counts.get('needs_correction', 0),
            'approved': counts.get('approved', 0),
            'published': counts.get('published', 0),
            'rejected': counts.get('rejected', 0),
            'cancelled': counts.get('cancelled', 0),
            'conflicts': len(conflict_ids),
        }
        return jsonify({
            'success': True,
            'data': data,
            'stats': stats,
            'actor': actor,
            'months': sorted({e['exam_date'][:7] for e in data if e['exam_date']}),
            'exam_types': [{'id': k, 'label': v} for k, v in EXAM_TYPES.items()],
        })
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple', methods=['POST'])
def create_simple_exam():
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ('teacher', 'principal', 'superadmin'):
        return jsonify({'success': False, 'error': 'Only teachers and principals may create examination schedules.'}), 403
    data = request.get_json(silent=True) or {}
    conn = _conn()
    try:
        payload, error = _validate_simple_payload(conn, data, actor)
        if error:
            return error
        conflict = _simple_conflict(
            conn, None, payload['exam_date'], payload['start_time'], payload['end_time'],
            payload['class_ids'], payload['subject_id'], payload['exam_type'])
        if conflict:
            return jsonify({'success': False, 'error': conflict, 'code': 'CONFLICT'}), 409

        submit_now = bool(data.get('submit_for_review'))
        status = 'submitted' if submit_now else 'draft'
        academic = 'pending' if submit_now else 'draft'
        exam_id = 'EXM-{0}-{1}-{2}'.format(
            datetime.now().year,
            re.sub(r'[^A-Z0-9]', '', payload['department_id'].upper())[:4] or 'GEN',
            uuid.uuid4().hex[:6].upper(),
        )
        now_ts = _now()
        conn.execute("""
            INSERT INTO exams (
                id, title, exam_type, academic_year_id, term, campus_id, campus_name,
                department_id, department_name, subject_id, subject_name,
                teacher_id, teacher_name, class_ids, class_names,
                exam_date, start_time, end_time, duration_mins,
                room_id, room_name, seating_capacity, instructions,
                max_marks, passing_marks, weight_pct, syllabus,
                prep_resources_json, attachments_json,
                status, academic_status, operational_status, result_status,
                correction_notes, internal_notes,
                created_by, updated_by, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            exam_id, payload['title'], payload['exam_type'], 'ay-2025-26', 'Semester 2',
            payload['campus_id'], payload['campus_name'],
            payload['department_id'], payload['department_name'],
            payload['subject_id'], payload['subject_name'],
            actor['id'], actor['name'], json.dumps(payload['class_ids']), json.dumps(payload['class_names']),
            payload['exam_date'], payload['start_time'], payload['end_time'], 0,
            '', '', 0, '', 0, 0, 0, '', '[]', '[]',
            status, academic, 'pending', 'not_started', '', '',
            actor['id'], actor['id'], now_ts, now_ts,
        ))
        _log_audit(exam_id, actor, 'create', '', status, 'Examination schedule created.')
        if submit_now:
            _log_audit(exam_id, actor, 'submit', 'draft', 'submitted', 'Submitted to Principal for review.')
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        return jsonify({'success': True, 'data': _simplified_exam(row)}), 201
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple/<exam_id>', methods=['PUT'])
def update_simple_exam(exam_id):
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Examination not found.'}), 404
        current = dict(row)
        if actor['role'] == 'teacher':
            if current['teacher_id'] != actor['id']:
                return jsonify({'success': False, 'error': 'You can only edit schedules you created.'}), 403
            if current['status'] == 'published':
                return jsonify({'success': False, 'error': 'A published schedule can only be corrected by the Principal or an administrator.'}), 403
        elif actor['role'] not in ('principal', 'superadmin', 'admin'):
            return jsonify({'success': False, 'error': 'Permission denied.'}), 403

        payload, error = _validate_simple_payload(conn, request.get_json(silent=True) or {}, actor)
        if error:
            return error
        conflict = _simple_conflict(
            conn, exam_id, payload['exam_date'], payload['start_time'], payload['end_time'],
            payload['class_ids'], payload['subject_id'], payload['exam_type'])
        if conflict:
            return jsonify({'success': False, 'error': conflict, 'code': 'CONFLICT'}), 409

        was_published = current['status'] == 'published'
        new_status = current['status']
        new_academic = current['academic_status']
        if actor['role'] == 'teacher' and current['academic_status'] == 'approved':
            new_status, new_academic = 'submitted', 'pending'
        now_ts = _now()
        conn.execute("""
            UPDATE exams SET
                title=?, exam_type=?, campus_id=?, campus_name=?,
                department_id=?, department_name=?, subject_id=?, subject_name=?,
                class_ids=?, class_names=?, exam_date=?, start_time=?, end_time=?,
                status=?, academic_status=?, updated_by=?, updated_at=?
            WHERE id=?
        """, (
            payload['title'], payload['exam_type'], payload['campus_id'], payload['campus_name'],
            payload['department_id'], payload['department_name'], payload['subject_id'], payload['subject_name'],
            json.dumps(payload['class_ids']), json.dumps(payload['class_names']),
            payload['exam_date'], payload['start_time'], payload['end_time'],
            new_status, new_academic, actor['id'], now_ts, exam_id,
        ))
        _log_audit(exam_id, actor, 'update', current['status'], new_status, 'Examination schedule corrected.')
        if was_published:
            _log_audit(exam_id, actor, 'notify_students', 'published', 'published',
                       'Published schedule changed; affected students are notified on their calendar.')
        updated = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        return jsonify({'success': True, 'data': _simplified_exam(updated)})
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple/<exam_id>/submit', methods=['POST'])
def submit_simple_exam(exam_id):
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Examination not found.'}), 404
        current = dict(row)
        if actor['role'] == 'teacher' and current['teacher_id'] != actor['id']:
            return jsonify({'success': False, 'error': 'You can only submit schedules you created.'}), 403
        if actor['role'] not in ('teacher', 'principal', 'superadmin'):
            return jsonify({'success': False, 'error': 'Permission denied.'}), 403
        if current['status'] not in ('draft', 'needs_correction'):
            return jsonify({'success': False, 'error': 'This schedule cannot be submitted in its current state.'}), 400
        now_ts = _now()
        conn.execute("UPDATE exams SET status='submitted', academic_status='pending', updated_by=?, updated_at=? WHERE id=?",
                     (actor['id'], now_ts, exam_id))
        _log_audit(exam_id, actor, 'submit', current['status'], 'submitted', 'Submitted to Principal for review.')
        return jsonify({'success': True, 'message': 'Submitted for Principal review.'})
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple/<exam_id>/cancel', methods=['POST'])
def cancel_simple_exam(exam_id):
    init_exam_schema()
    actor = _get_current_actor(request)
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Examination not found.'}), 404
        current = dict(row)
        if actor['role'] == 'teacher':
            if current['teacher_id'] != actor['id']:
                return jsonify({'success': False, 'error': 'You can only cancel schedules you created.'}), 403
            if current['status'] == 'published':
                return jsonify({'success': False, 'error': 'Only the Principal may cancel a published schedule.'}), 403
        elif actor['role'] not in ('principal', 'superadmin', 'admin'):
            return jsonify({'success': False, 'error': 'Permission denied.'}), 403
        if current['status'] == 'cancelled':
            return jsonify({'success': False, 'error': 'This schedule is already cancelled.'}), 400
        now_ts = _now()
        conn.execute("UPDATE exams SET status='cancelled', academic_status='cancelled', updated_by=?, updated_at=? WHERE id=?",
                     (actor['id'], now_ts, exam_id))
        _log_audit(exam_id, actor, 'cancel', current['status'], 'cancelled', 'Examination schedule cancelled.')
        if current['status'] == 'published':
            _log_audit(exam_id, actor, 'notify_students', 'published', 'cancelled',
                       'Cancelled published schedule removed from student calendars.')
        return jsonify({'success': True, 'message': 'Examination schedule cancelled.'})
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple/<exam_id>/review', methods=['POST'])
def review_simple_exam(exam_id):
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': 'Only the Principal may review examination schedules.'}), 403
    data = request.get_json(silent=True) or {}
    decision = str(data.get('decision') or '').strip().lower()
    if decision == 'request-changes':
        decision = 'request_correction'
    reason = str(data.get('reason') or '').strip()
    if decision not in ('approve', 'reject', 'request_correction'):
        return jsonify({'success': False, 'error': 'Invalid review decision.'}), 400
    if decision in ('reject', 'request_correction') and not reason:
        return jsonify({'success': False, 'error': 'A reason is required for rejection or requested changes.'}), 400

    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Examination not found.'}), 404
        current = dict(row)
        if current['status'] != 'submitted':
            return jsonify({'success': False, 'error': 'Only schedules pending review can be reviewed.'}), 400
        now_ts = _now()
        mapping = {
            'approve': ('approved', 'approved'),
            'reject': ('rejected', 'rejected'),
            'request_correction': ('needs_correction', 'needs_correction'),
        }
        status, academic = mapping[decision]
        approved_by = actor['id'] if decision == 'approve' else ''
        approved_at = now_ts if decision == 'approve' else ''
        notes = reason or ''
        conn.execute("""
            UPDATE exams SET status=?, academic_status=?, approved_by=?, approved_at=?,
                correction_notes=?, updated_by=?, updated_at=? WHERE id=?
        """, (status, academic, approved_by, approved_at, notes, actor['id'], now_ts, exam_id))
        _log_audit(exam_id, actor, decision, current['academic_status'], academic,
                   notes or 'Principal approved the examination schedule.')
        return jsonify({'success': True, 'status': status, 'message': 'Review decision recorded.'})
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple/<exam_id>/publish', methods=['POST'])
def publish_simple_exam(exam_id):
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': 'Only the Principal may publish examination schedules.'}), 403
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Examination not found.'}), 404
        current = dict(row)
        if current['academic_status'] != 'approved':
            return jsonify({'success': False, 'error': 'Principal approval is required before publication.'}), 400
        if current['status'] == 'published':
            return jsonify({'success': False, 'error': 'This schedule is already published.'}), 400
        conflict = _simple_conflict(
            conn, exam_id, current['exam_date'], current['start_time'], current['end_time'],
            _json_list(current['class_ids']), current['subject_id'], _canonical_exam_type(current['exam_type']))
        if conflict:
            return jsonify({'success': False, 'error': conflict, 'code': 'CONFLICT'}), 409
        now_ts = _now()
        conn.execute("""
            UPDATE exams SET status='published', operational_status='confirmed',
                published_by=?, published_at=?, updated_by=?, updated_at=? WHERE id=?
        """, (actor['id'], now_ts, actor['id'], now_ts, exam_id))
        _log_audit(exam_id, actor, 'publish', current['status'], 'published', 'Schedule published to student calendars.')
        _log_audit(exam_id, actor, 'notify_students', current['status'], 'published',
                   'Published examination is now visible to affected students.')
        return jsonify({'success': True, 'message': 'Examination schedule published.'})
    finally:
        conn.close()

@exam_bp.route('/api/exams/simple/<exam_id>/unpublish', methods=['POST'])
def unpublish_simple_exam(exam_id):
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in ACADEMIC_APPROVER_ROLES:
        return jsonify({'success': False, 'error': 'Only the Principal may unpublish a schedule.'}), 403
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM exams WHERE id=?", (exam_id,)).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Examination not found.'}), 404
        current = dict(row)
        if current['status'] != 'published':
            return jsonify({'success': False, 'error': 'This schedule is not published.'}), 400
        now_ts = _now()
        conn.execute("""UPDATE exams SET status='approved', updated_by=?, updated_at=? WHERE id=?""",
                     (actor['id'], now_ts, exam_id))
        _log_audit(exam_id, actor, 'unpublish', 'published', 'approved', 'Schedule withdrawn from student calendars.')
        _log_audit(exam_id, actor, 'notify_students', 'published', 'approved',
                   'Students were notified that the schedule was withdrawn.')
        return jsonify({'success': True, 'message': 'Schedule withdrawn from student calendars.'})
    finally:
        conn.close()

@exam_bp.route('/api/exams/activity', methods=['GET'])
def get_exam_activity():
    init_exam_schema()
    actor = _get_current_actor(request)
    if actor['role'] not in STAFF_ROLES:
        return jsonify({'success': False, 'error': 'Permission denied.'}), 403
    exam_id = str(request.args.get('exam_id') or '').strip()
    action = str(request.args.get('action') or '').strip().lower()
    actor_id = str(request.args.get('actor_id') or '').strip()
    try:
        limit = max(1, min(int(request.args.get('limit') or 100), 500))
    except Exception:
        limit = 100
    sql = "SELECT * FROM exam_audit_log WHERE 1=1"
    params = []
    if exam_id:
        sql += " AND exam_id=?"
        params.append(exam_id)
    if action and action != 'all':
        sql += " AND LOWER(action)=?"
        params.append(action)
    if actor_id and actor_id != 'all':
        sql += " AND actor_id=?"
        params.append(actor_id)
    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    conn = _conn()
    try:
        rows = conn.execute(sql, params).fetchall()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})
    finally:
        conn.close()

@exam_bp.route('/api/exams/locations', methods=['GET'])
def get_exam_locations():
    """Retrieve available examination halls and classrooms."""
    init_exam_schema()
    conn = _conn()
    try:
        rows = conn.execute("SELECT * FROM exam_locations WHERE is_active = 1 ORDER BY campus_name ASC, name ASC").fetchall()
        return jsonify({'success': True, 'data': [dict(r) for r in rows]})
    finally:
        conn.close()

@exam_bp.route('/api/exams/conflict-check', methods=['POST'])
def check_exam_conflicts():
    """Check if proposed exam date, time, room, or class conflicts with existing scheduled sessions."""
    init_exam_schema()
    data = request.get_json(silent=True) or {}
    exam_id = data.get('exam_id')
    exam_date = data.get('exam_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    room_id = data.get('room_id')
    class_ids = data.get('class_ids') or []

    conflict = _check_schedule_conflict(exam_id, exam_date, start_time, end_time, room_id, class_ids)
    return jsonify({
        'success': True,
        'has_conflict': bool(conflict),
        'conflict_message': conflict or "No scheduling conflicts detected."
    })

# ── HELPER FUNCTIONS ────────────────────────────────────────────────────────

def _check_schedule_conflict(exam_id, exam_date, start_time, end_time, room_id, class_ids):
    if not (exam_date and start_time and end_time and room_id):
        return None

    conn = _conn()
    try:
        sql = """
            SELECT id, title, room_id, room_name, class_ids, start_time, end_time
            FROM exams
            WHERE exam_date = ? AND status NOT IN ('cancelled', 'archived')
        """
        args = [exam_date]
        if exam_id:
            sql += " AND id != ?"
            args.append(exam_id)

        rows = conn.execute(sql, args).fetchall()
        for r in rows:
            # Overlap in time: (StartA < EndB) and (EndA > StartB)
            if (start_time < r['end_time']) and (end_time > r['start_time']):
                # 1. Room conflict
                if r['room_id'] == room_id:
                    return f"Room conflict: '{r['room_name']}' is already reserved for '{r['title']}' ({r['start_time']}–{r['end_time']})."

                # 2. Class conflict
                r_classes = json.loads(r['class_ids'] or '[]')
                for cid in class_ids:
                    if cid in r_classes:
                        return f"Class conflict: Class '{cid}' is already taking examination '{r['title']}' ({r['start_time']}–{r['end_time']})."
        return None
    finally:
        conn.close()

def _get_student_name_map():
    st_map = {}
    try:
        p = Path(__file__).resolve().parent / "data" / "students_overlay.json"
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                arr = json.load(f)
                for item in arr:
                    if isinstance(item, dict) and 'id' in item and 'name' in item:
                        st_map[item['id']] = item['name']
    except Exception:
        pass
    return st_map

def _populate_exam_roster(conn: sqlite3.Connection, exam_id: str, class_ids: list, max_marks: float):
    """Enroll students belonging to class_ids into exam_student_results."""
    now_ts = _now()
    st_name_map = _get_student_name_map()
    class_name_map = {
        'cls-10a': 'Grade 10A',
        'cls-11b': 'Grade 11B',
        'cls-11c': 'Grade 11C',
        'cls-eng-9c': 'Grade 9C',
        'cls-chn-9a': 'Grade 9A'
    }

    for cid in class_ids:
        c_label = class_name_map.get(cid, cid.upper())
        st_rows = conn.execute("""
            SELECT student_id FROM enrollments WHERE class_id = ?
        """, (cid,)).fetchall()

        if not st_rows and cid == 'cls-10a':
            sample_ids = [
                ("2026-STD-0142", "Nrinphouneta Hok"),
                ("2026-STD-0144", "Vicheka Meas"),
                ("2026-STD-0145", "Virak Heng"),
                ("2026-STD-0148", "Kosal Rith Mony"),
                ("2026-STD-0151", "Sreylin Vuth"),
                ("2026-STD-0155", "Heng Piseth"),
                ("2026-STD-0160", "Emily Jenkins"),
                ("2026-STD-0168", "Linda Chea")
            ]
            for s_id, s_name in sample_ids:
                conn.execute("""
                    INSERT OR IGNORE INTO exam_student_results (
                        id, exam_id, student_id, student_name, class_id, class_name,
                        attendance_status, score, max_marks, is_locked, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 'present', NULL, ?, 0, ?, ?)
                """, (f"res-{exam_id}-{s_id}", exam_id, s_id, s_name, cid, c_label, max_marks, now_ts, now_ts))
        else:
            for sr in st_rows:
                s_id = sr['student_id']
                s_name = st_name_map.get(s_id, f"Student {s_id}")
                conn.execute("""
                    INSERT OR IGNORE INTO exam_student_results (
                        id, exam_id, student_id, student_name, class_id, class_name,
                        attendance_status, score, max_marks, is_locked, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 'present', NULL, ?, 0, ?, ?)
                """, (f"res-{exam_id}-{s_id}", exam_id, s_id, s_name, cid, c_label, max_marks, now_ts, now_ts))

def register_exam_mgmt_routes(app):
    """Mount blueprint on the application."""
    init_exam_schema()
    app.register_blueprint(exam_bp)
