"""
============================================================================
 Khmer School Admin Suite (ការគ្រប់គ្រងសាលា)
 NGIS — Timetable domain model, conflict engine and auto-assign algorithm
============================================================================
Single source of truth for the timetable domain.  Everything is persisted as
one JSON document (data/timetable_state.json) so the Flask app stays stateless
between restarts and the frontend can mirror the exact same logic offline.

Design rules
------------
* Every count shown in the UI is derived from `state`, never hard-coded.
* Grid key: "<day>|<shift>|<period>|<class_id>" (identical in JS).
* A "lesson" is one grid cell.  `assignments` define the demand; `grid` the supply.
* Hard conflicts block a placement, soft conflicts only warn.
============================================================================
"""

from __future__ import annotations

import json
import os
import random
import sys
import threading
from copy import deepcopy

# The DFS visits one frame per lesson (12 classes x 34 lessons = 408 by default).
sys.setrecursionlimit(10000)
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(ROOT, "data", "timetable_state.json")
# Bump whenever the seed shape changes; old documents are rebuilt on load so a
# stale file can never leave the UI with impossible counts.
SCHEMA_VERSION = 4

# ── Static configuration ───────────────────────────────────────────────────

DAYS: List[str] = ["ច័ន្ទ", "អង្គារ", "ពុធ", "ព្រហស្បតិ៍", "សុក្រ", "សៅរ៍"]
SHIFTS: List[str] = ["ព្រឹក", "រសៀល"]

MORNING_STARTS = ["07:00", "07:50", "08:40", "09:30", "10:20"]
AFTERNOON_STARTS = ["13:00", "13:50", "14:40", "15:30", "16:20"]

# (code, khmer name, english name, short name, hex colour, lessons/week)
SUBJECT_DEFS: List[Tuple[str, str, str, str, str, int]] = [
    ("K",  "ខ្មែរ",        "Khmer",            "ខ្មែរ",  "#FED766", 6),
    ("M",  "គណិតវិទ្យា",  "Mathematics",      "គណិត",  "#93C5FD", 6),
    ("EN", "អង់គ្លេស",     "English",          "អង់",    "#99F6E4", 4),
    ("P",  "រូបវិទ្យា",    "Physics",          "រូប",    "#DDD6FE", 2),
    ("C",  "គីមីវិទ្យា",   "Chemistry",        "គីមី",  "#FBCFE8", 2),
    ("B",  "ជីវវិទ្យា",    "Biology",          "ជីវ",    "#A7F3D0", 2),
    ("ES", "ភូមិវិទ្យា",   "Earth Science",    "ភូមិ",  "#FED7AA", 2),
    ("G",  "កុំព្យូទ័រ",   "Computer Studies", "កុំព្យូ", "#BAE6FD", 2),
    ("H",  "ប្រវត្តិវិទ្យា", "History",         "ប្រវត្តិ","#FDE68A", 2),
    ("I",  "ពលរដ្ឋ",       "Civics",           "ពល",    "#C7D2FE", 2),
    ("IT", "កីឡា",         "Physical Education", "កីឡា", "#FECDD3", 2),
    ("ED", "អប់រំសីលធម៌", "Moral Education",  "សីលធម៌", "#FEF3C7", 2),
    ("SH", "ភាសា",         "Social Language",  "ភាសា",   "#E9D5FF", 0),
]

# Realistic Khmer staff names, cycled for the generated teacher pool.
TEACHER_NAMES: List[str] = [
    "សុខ ដារ៉ា", "តាន់ ធីតា", "ហេង វីរៈ", "ជើន ម៉ារី", "ណុង សុធា",
    "យ៉ុក សុីន", "ប៉ុក សុភី", "អ៊ុក ចាន់ថា", "លី សុភាព", "ម៉ៅ ដារ៉ាវី",
    "គឹម ស្រីពេជ្រ", "ចាន់ សុខលី", "ប្រាក់ មុនី", "អ៊ឹង រិទ្ធី", "ស៊ុន ច័ន្ទណ៍",
    "ទូច សុភក្ត្រា", "វ៉ាន់ សុភ័ក្ត្រ", "រស់ សុគន្ធា", "ខូវ ចាន់ដារ៉ា", "ឈឹម ស្រីល័ក្ខ",
    "នូ សុខហេង", "គង់ សុភាវី", "ឡុង ចាន់ថុល", "ប៉ែន សុភាវី", "អន សុខរិទ្ធ",
    "សេង ដារ៉ាវុធ", "ហ៊ុន មាលី", "ជា សុភីរិទ្ធ", "ផន ចាន់សុភា", "ប៊ុន ស្រីមុំ",
    "វង្ស សុខាន់", "តេង សុភ័ក្ត្រ",
]

CURRICULUM: Dict[str, int] = {code: lessons for code, *_rest, lessons in SUBJECT_DEFS}
CLASS_CAPACITY = 60  # 6 days x (5 morning + 5 afternoon) periods

RECORD_COLUMNS: List[Dict[str, str]] = [
    {"key": "no", "kh": "ល.រ", "en": "No."},
    {"key": "name", "kh": "គោត្តនាម-នាម", "en": "Full name"},
    {"key": "gender", "kh": "ភេទ", "en": "Gender"},
    {"key": "dob", "kh": "ថ្ងៃខែឆ្នាំកំណើត", "en": "Date of birth"},
    {"key": "grade", "kh": "ឆ្នាំ", "en": "Grade"},
    {"key": "code", "kh": "កូដ", "en": "Code"},
    {"key": "birth_place", "kh": "ទីកន្លែងកំណើត", "en": "Place of birth"},
    {"key": "address", "kh": "អាសយដ្ឋាន", "en": "Address"},
    {"key": "language", "kh": "ភាសា៖ ទូទាត់", "en": "Language"},
    {"key": "id_number", "kh": "អត្តលេខ", "en": "ID number"},
    {"key": "registered_at", "kh": "កាលបរិច្ឆេទចុះឈ្មោះ", "en": "Registered"},
    {"key": "homeroom", "kh": "គ្រូបង្រៀន", "en": "Homeroom teacher"},
]

KH_DIGITS = str.maketrans("0123456789", "០១២៣៤៥៦៧៨៩")


def khmer_number(value: Any) -> str:
    """Render a number with Khmer numerals (used by exports / print views)."""
    return str(value).translate(KH_DIGITS)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def grid_key(day: str, shift: str, period: int, class_id: str) -> str:
    return f"{day}|{shift}|{period}|{class_id}"


def parse_grid_key(key: str) -> Dict[str, Any]:
    day, shift, period, class_id = key.split("|")
    return {"day": day, "shift": shift, "period": int(period), "class_id": class_id}


def build_periods() -> List[Dict[str, Any]]:
    periods: List[Dict[str, Any]] = []
    for shift, starts in (("ព្រឹក", MORNING_STARTS), ("រសៀល", AFTERNOON_STARTS)):
        for i, start in enumerate(starts, 1):
            h, m = (int(x) for x in start.split(":"))
            total = h * 60 + m + 50
            end = f"{total // 60:02d}:{total % 60:02d}"
            periods.append({
                "number": i, "shift": shift, "start": start, "end": end,
                "label": f"{shift} {i}",
            })
    return periods


PERIODS: List[Dict[str, Any]] = build_periods()


# ── Seed data ──────────────────────────────────────────────────────────────

def _seed_subjects() -> List[Dict[str, Any]]:
    dept_map = {
        "K": "ភាសាខ្មែរ", "M": "គណិតវិទ្យា", "EN": "ភាសាបរទេស",
        "P": "វិទ្យាសាស្ត្រពិត", "C": "វិទ្យាសាស្ត្រពិត", "B": "វិទ្យាសាស្ត្រពិត", "ES": "វិទ្យាសាស្ត្រពិត",
        "G": "វិទ្យាសាស្ត្រសង្គម", "H": "វិទ្យាសាស្ត្រសង្គម", "I": "វិទ្យាសាស្ត្រសង្គម",
        "IT": "បច្ចេកវិទ្យា", "ED": "អប់រំកាយ", "SH": "សុខភាព"
    }
    return [
        {
            "id": f"sub_{code}", "name_kh": name_kh, "name_en": name_en,
            "short_name": short, "code": code, "color": color,
            "lessons_per_week": lessons, "is_locked": False,
            "consecutive_preference": "preferred" if lessons >= 4 else "none",
            "department": dept_map.get(code, "ទូទៅ"),
            "active": True,
        }
        for code, name_kh, name_en, short, color, lessons in SUBJECT_DEFS
    ]


def _seed_classes() -> List[Dict[str, Any]]:
    classes = []
    for grade in range(7, 13):
        for section in ("A", "B"):
            classes.append({
                "id": f"class_{grade}{section}",
                "grade": grade,
                "section": section,
                "display": f"{grade}{section}",
                # Display label only — every class uses both sessions in the grid.
                "shift": "ព្រឹក" if section == "A" else "រសៀល",
                "days": 6,
                "capacity": CLASS_CAPACITY,
                "room": f"បន្ទប់ {grade * 10 + (1 if section == 'A' else 2)}",
                "student_count": 32,
                "campus": "Sensok",
                "department": "មធ្យមសិក្សា",
            })
    return classes


def _seed_teachers() -> List[Dict[str, Any]]:
    """Create a teacher pool whose weekly capacity covers the whole curriculum."""
    pool: List[Dict[str, Any]] = []
    name_index = 0
    for code, _kh, _en, _short, _color, lessons in SUBJECT_DEFS:
        if lessons == 0:
            continue
        demand = lessons * 12  # 12 classes
        target = 17 if code in ("K", "M", "EN") else 15
        # Assignments are atomic chunks of `lessons` hours, so a teacher can
        # hold at most floor(target / lessons) classes without exceeding target.
        per_teacher = (target // lessons) * lessons
        capacity = per_teacher or target
        count = max(1, -(-demand // capacity))
        for i in range(1, count + 1):
            name = TEACHER_NAMES[name_index % len(TEACHER_NAMES)]
            name_index += 1
            # A few part-time staff are morning-only — exercises shift rules.
            morning_only = i == count and code in ("ES", "G", "H", "IT", "ED")
            emp_num = f"{1000 + name_index}"
            sub_def = next((s for s in SUBJECT_DEFS if s[0] == code), None)
            spec_name = sub_def[1] if sub_def else "ទូទៅ"
            pool.append({
                "id": f"t_{code}{i}",
                "code": f"{code}{i}",
                "codes": [f"{code}{i}"],
                "name_kh": name,
                "name_en": f"Teacher {code}{i}",
                "gender": "ប្រុស" if i % 2 == 1 else "ស្រី",
                "phone": f"+855 12 {800 + i:03d} {name_index:02d}",
                "position": "គ្រូបង្រៀន",
                "category": "ក្របខ័ណ្ឌរដ្ឋ",
                "rank": "គ្រូកម្រិតឧត្តម",
                "specialization": spec_name,
                "subject_id": f"sub_{code}",
                "subject_ids": [f"sub_{code}"],
                "target": target,
                "max_daily": 5,
                "employee_id": f"EMP-{emp_num}",
                "start_year": 2018 + (i % 6),
                "notes": "",
                "shifts": ["ព្រឹក"] if morning_only else list(SHIFTS),
                "unavailable_slots": [],
            })
    return pool


def _seed_assignments(classes: List[Dict[str, Any]],
                      teachers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Bind a teacher to each (class, subject) demand, respecting workload targets."""
    by_subject: Dict[str, List[Dict[str, Any]]] = {}
    for teacher in teachers:
        by_subject.setdefault(teacher["subject_id"], []).append(teacher)
    load: Dict[str, int] = {t["id"]: 0 for t in teachers}

    assignments: List[Dict[str, Any]] = []
    for cls in classes:
        for subject_code, lessons in CURRICULUM.items():
            if lessons <= 0:
                continue
            subject_id = f"sub_{subject_code}"
            pool = by_subject.get(subject_id, [])
            if not pool:
                continue
            # Pick the least-loaded teacher who still has room for this chunk.
            feasible = [t for t in pool if load[t["id"]] + lessons <= t["target"]]
            teacher = min(feasible or pool, key=lambda t: (load[t["id"]], t["code"]))
            load[teacher["id"]] += lessons
            assignments.append({
                "id": f"asg_{cls['id']}_{subject_code}",
                "class_id": cls["id"],
                "subject_id": subject_id,
                "teacher_id": teacher["id"],
                "lessons": lessons,
                "shift": cls["shift"],
            })
    return assignments


def _seed_records() -> List[Dict[str, Any]]:
    """A small staff/student roster so the records module is not empty."""
    rows = []
    for i, name in enumerate(TEACHER_NAMES[:12], 1):
        rows.append({
            "no": i, "name": name, "gender": "ស" if i % 2 else "ប",
            "dob": f"១៩៨{5 + i % 4}·០{i % 9 + 1}·១២", "grade": "១០",
            "code": f"ST{2000 + i}", "birth_place": "ភ្នំពេញ",
            "address": "រាជធានីភ្នំពេញ", "language": "ខ្មែរ",
            "id_number": f"០០{i:04d}", "registered_at": "២០២៦·០៩·០១",
            "homeroom": TEACHER_NAMES[(i + 3) % len(TEACHER_NAMES)],
            "type": "គ្រូបង្រៀង" if i % 3 == 0 else "សិស្ស",
        })
    return rows


def build_seed_state() -> Dict[str, Any]:
    classes = _seed_classes()
    teachers = _seed_teachers()
    return {
        "schema_version": SCHEMA_VERSION,
        "institution": {
            "name_kh": "វិទ្យាល័យ ហ្គេតវ៉េ អន្តរជាតិថ្មី",
            "name_en": "New Gateway International School",
            "academic_year": "ឆ្នាំសិក្សា ២០២៦–២០២៧",
            "package": "ស្តង់ដារ",
        },
        "settings": {
            "days": list(DAYS), "shifts": list(SHIFTS), "periods": PERIODS,
            "khmer_numerals": True, "auto_save": True,
        },
        "subjects": _seed_subjects(),
        "teachers": teachers,
        "classes": classes,
        "assignments": _seed_assignments(classes, teachers),
        "grid": {},
        "records": _seed_records(),
        "history": [],
        "revision": 1,
        "updated_at": utc_now(),
    }


# ── Derived statistics ─────────────────────────────────────────────────────

def _index(state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {
        "subjects": {s["id"]: s for s in state["subjects"]},
        "teachers": {t["id"]: t for t in state["teachers"]},
        "classes": {c["id"]: c for c in state["classes"]},
    }


def teacher_load(state: Dict[str, Any]) -> Dict[str, int]:
    load: Dict[str, int] = {t["id"]: 0 for t in state["teachers"]}
    for cell in state["grid"].values():
        tid = cell.get("teacher_id")
        if tid in load:
            load[tid] += 1
    return load


def assigned_count(state: Dict[str, Any], class_id: Optional[str] = None) -> Dict[Tuple[str, str], int]:
    """Placed lessons keyed by (class_id, subject_id)."""
    counts: Dict[Tuple[str, str], int] = {}
    for cell in state["grid"].values():
        if class_id and cell.get("class_id") != class_id:
            continue
        key = (cell.get("class_id"), cell.get("subject_id"))
        counts[key] = counts.get(key, 0) + 1
    return counts


def unassigned_chips(state: Dict[str, Any], class_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Every count in the UI is derived here: demand minus placed cells."""
    idx = _index(state)
    placed = assigned_count(state, class_id)
    chips: Dict[str, Dict[str, Any]] = {}
    for asg in state["assignments"]:
        if class_id and asg["class_id"] != class_id:
            continue
        key = (asg["class_id"], asg["subject_id"])
        remaining = asg["lessons"] - placed.get(key, 0)
        if remaining <= 0:
            continue
        subject = idx["subjects"].get(asg["subject_id"])
        teacher = idx["teachers"].get(asg["teacher_id"])
        if not subject or not teacher:
            continue
        ck = f"{asg['class_id']}|{asg['subject_id']}|{asg['teacher_id']}"
        if ck not in chips:
            chips[ck] = {
                "id": ck,
                "class_id": asg["class_id"],
                "subject_id": asg["subject_id"],
                "teacher_id": asg["teacher_id"],
                "subject_name": subject["name_kh"],
                "subject_code": subject["code"],
                "color": subject["color"],
                "teacher_code": teacher["code"],
                "teacher_name": teacher["name_kh"],
                "shift": asg.get("shift", "ព្រឹក"),
                "count": 0,
            }
        chips[ck]["count"] += remaining
    return sorted(chips.values(), key=lambda c: (-c["count"], c["subject_code"]))


def statistics(state: Dict[str, Any]) -> Dict[str, Any]:
    chips = unassigned_chips(state)
    load = teacher_load(state)
    idx = _index(state)
    total_demand = sum(a["lessons"] for a in state["assignments"])
    placed = len(state["grid"])
    per_class = []
    for cls in state["classes"]:
        assigned = sum(1 for c in state["grid"].values() if c.get("class_id") == cls["id"])
        remaining = sum(c["count"] for c in chips if c["class_id"] == cls["id"])
        per_class.append({
            "id": cls["id"], "display": cls["display"], "shift": cls["shift"],
            "assigned": assigned, "capacity": cls["capacity"],
            "remaining": remaining,
        })
    teachers = []
    for t in state["teachers"]:
        teachers.append({
            "id": t["id"], "code": t["code"], "name_kh": t["name_kh"],
            "subject_id": t["subject_id"],
            "subject_code": idx["subjects"].get(t["subject_id"], {}).get("code", ""),
            "color": idx["subjects"].get(t["subject_id"], {}).get("color", "#E5E7EB"),
            "target": t["target"], "assigned": load.get(t["id"], 0),
            "remaining": max(0, t["target"] - load.get(t["id"], 0)),
            "overloaded": load.get(t["id"], 0) > t["target"],
            "shifts": t.get("shifts", list(SHIFTS)),
        })
    return {
        "total_demand": total_demand,
        "placed": placed,
        "unassigned": sum(c["count"] for c in chips),
        "conflicts": len([c for c in scan_conflicts(state) if c["severity"] == "error"]),
        "per_class": per_class,
        "teachers": teachers,
        "chips": chips,
    }


# ── Conflict engine ────────────────────────────────────────────────────────

def validate_placement(state: Dict[str, Any], key: str, subject_id: str,
                       teacher_id: str, *, replace: bool = False) -> List[Dict[str, Any]]:
    """Return conflicts for a proposed placement.  `error` blocks, `warning` warns."""
    idx = _index(state)
    parts = parse_grid_key(key)
    day, shift, period, class_id = parts["day"], parts["shift"], parts["period"], parts["class_id"]
    conflicts: List[Dict[str, Any]] = []

    def add(kind: str, severity: str, kh: str, en: str) -> None:
        conflicts.append({
            "type": kind, "severity": severity, "key": key,
            "teacher_id": teacher_id, "class_id": class_id,
            "message_kh": kh, "message_en": en,
        })

    existing = state["grid"].get(key)
    if existing and not replace:
        add("class_double_booked", "error",
            "ថ្នាក់នេះមានមេរៀនរួចហើយក្នុងម៉ោងនេះ",
            "This class already has a lesson in this period")

    for other_key, cell in state["grid"].items():
        if other_key == key or cell.get("teacher_id") != teacher_id:
            continue
        p = parse_grid_key(other_key)
        if p["day"] == day and p["shift"] == shift and p["period"] == period:
            add("teacher_double_booked", "error",
                "គ្រូកំពុងបង្រៀនថ្នាក់ផ្សេងក្នុងម៉ោងនេះ",
                "Teacher is already teaching another class this period")
            break

    teacher = idx["teachers"].get(teacher_id)
    subject = idx["subjects"].get(subject_id)
    if not teacher:
        add("unknown_teacher", "error", "រកគ្រូមិនឃើញ", "Teacher not found")
        return conflicts
    if shift not in teacher.get("shifts", list(SHIFTS)):
        add("shift_mismatch", "error",
            f"គ្រូ {teacher['code']} មិនអាចបង្រៀនវេន{shift} បានទេ",
            f"Teacher {teacher['code']} is not available for the {shift} shift")

    unavail = teacher.get("unavailable_slots", [])
    if key in unavail or f"{day}|{shift}|{period}" in unavail or f"{day}|{period}" in unavail:
        add("teacher_unavailable", "error",
            f"គ្រូ {teacher['code']} ឈប់សម្រាកក្នុងម៉ោងនេះ",
            f"Teacher {teacher['code']} is unavailable in this period")

    load = teacher_load(state)
    if existing and existing.get("teacher_id") == teacher_id:
        load[teacher_id] = max(0, load.get(teacher_id, 0) - 1)
    if load.get(teacher_id, 0) + 1 > teacher["target"]:
        add("workload_exceeded", "warning",
            f"គ្រូ {teacher['code']} លើស {teacher['target']} ម៉ោង/សប្តាហ៍",
            f"Teacher {teacher['code']} exceeds weekly target of {teacher['target']}")

    if subject and subject.get("is_locked"):
        add("subject_locked", "warning",
            f"មុខវិជ្ជា {subject['name_kh']} ត្រូវបានចាក់សោ",
            f"Subject {subject['name_kh']} is locked")
    return conflicts


def scan_conflicts(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Whole-grid audit: double bookings, shift mismatches and overloads."""
    idx = _index(state)
    found: List[Dict[str, Any]] = []
    teacher_slots: Dict[Tuple[str, str, str, int], str] = {}
    for key, cell in state["grid"].items():
        p = parse_grid_key(key)
        tkey = (cell.get("teacher_id", ""), p["day"], p["shift"], p["period"])
        if cell.get("teacher_id") and tkey in teacher_slots:
            found.append({
                "type": "teacher_double_booked", "severity": "error", "key": key,
                "message_kh": "គ្រូកំពុងបង្រៀនពីរថ្នាក់ក្នុងម៉ោងតែមួយ",
                "message_en": "Teacher double-booked in this period",
            })
        else:
            teacher_slots[tkey] = key
        teacher = idx["teachers"].get(cell.get("teacher_id"))
        if teacher:
            if p["shift"] not in teacher.get("shifts", list(SHIFTS)):
                found.append({
                    "type": "shift_mismatch", "severity": "error", "key": key,
                    "message_kh": f"គ្រូ {teacher['code']} មិនមានវេន{p['shift']}",
                    "message_en": f"Teacher {teacher['code']} unavailable for {p['shift']}",
                })
            unavail = teacher.get("unavailable_slots", [])
            if key in unavail or f"{p['day']}|{p['shift']}|{p['period']}" in unavail:
                found.append({
                    "type": "teacher_unavailable", "severity": "error", "key": key,
                    "message_kh": f"គ្រូ {teacher['code']} ឈប់សម្រាកក្នុងម៉ោងនេះ",
                    "message_en": f"Teacher {teacher['code']} unavailable in this period",
                })
    load = teacher_load(state)
    for teacher in state["teachers"]:
        if load.get(teacher["id"], 0) > teacher["target"]:
            found.append({
                "type": "workload_exceeded", "severity": "warning",
                "teacher_id": teacher["id"],
                "message_kh": f"គ្រូ {teacher['code']} លើសបន្ទុក ({load[teacher['id']]}/{teacher['target']})",
                "message_en": f"Teacher {teacher['code']} overloaded ({load[teacher['id']]}/{teacher['target']})",
            })
    return found


# ── Auto-assign: greedy + limited backtracking ─────────────────────────────

def all_cells(state: Dict[str, Any], class_id: str) -> List[str]:
    """Every (day x period) cell of a class, interleaved across days."""
    buckets: Dict[str, List[str]] = {d: [] for d in state["settings"]["days"]}
    for day in state["settings"]["days"]:
        for period in state["settings"]["periods"]:
            buckets[day].append(grid_key(day, period["shift"], period["number"], class_id))
    ordered: List[str] = []
    for i in range(len(state["settings"]["periods"])):
        for day in state["settings"]["days"]:
            ordered.append(buckets[day][i])
    return ordered


def auto_assign(state: Dict[str, Any], *, class_id: Optional[str] = None,
                clear_first: bool = False, seed: int = 7,
                max_nodes: int = 60000) -> Dict[str, Any]:
    """
    Fill unassigned chips into free cells using greedy placement + bounded DFS
    backtracking.  Hard constraints: teacher double-booking, class double-booking,
    shift availability, teacher weekly workload, locked subjects.  Soft heuristic:
    spread a subject over the week (never twice on the same day where avoidable).

    Occupancy indexes are maintained incrementally so each candidate check is O(1).
    Returns the new state plus a diff suitable for the AI "preview changes" view.
    """
    working = deepcopy(state)
    before_keys = set(working["grid"].keys())
    if clear_first:
        if class_id:
            for k in [k for k in working["grid"] if parse_grid_key(k)["class_id"] == class_id]:
                del working["grid"][k]
        else:
            working["grid"] = {}

    idx = _index(working)
    rng = random.Random(seed)
    load = teacher_load(working)
    teacher_busy: set = set()
    subject_day: Dict[Tuple[str, str, str], int] = {}
    class_day: Dict[Tuple[str, str], int] = {}
    teacher_day: Dict[Tuple[str, str], int] = {}
    for key, cell in working["grid"].items():
        p = parse_grid_key(key)
        tid, cid, sid, day = cell.get("teacher_id"), p["class_id"], cell.get("subject_id"), p["day"]
        teacher_busy.add((tid, day, p["shift"], p["period"]))
        subject_day[(cid, sid, day)] = subject_day.get((cid, sid, day), 0) + 1
        class_day[(cid, day)] = class_day.get((cid, day), 0) + 1
        teacher_day[(tid, day)] = teacher_day.get((tid, day), 0) + 1

    tasks: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    for chip in unassigned_chips(working, class_id):
        subject = idx["subjects"].get(chip["subject_id"], {})
        if subject.get("is_locked"):
            skipped.append({"reason": "subject_locked", "chip": chip["id"], "count": chip["count"]})
            continue
        teacher = idx["teachers"].get(chip["teacher_id"], {})
        for _ in range(chip["count"]):
            tasks.append({
                "class_id": chip["class_id"], "subject_id": chip["subject_id"],
                "teacher_id": chip["teacher_id"], "subject_code": chip["subject_code"],
                "teacher_code": chip.get("teacher_code", ""),
                "cells": all_cells(working, chip["class_id"]),
                "capacity": max(0, teacher.get("target", 17) - load.get(chip["teacher_id"], 0)),
            })
    # Most constrained first: teachers with the least spare capacity.
    rng.shuffle(tasks)
    tasks.sort(key=lambda t: (t["capacity"], t["class_id"], t["subject_code"]))
    total_tasks = len(tasks)

    nodes = 0
    backtracks = 0

    def rank(task: Dict[str, Any]) -> List[str]:
        """Order free cells by a spreading heuristic; O(n log n) per task."""
        cid, sid, tid = task["class_id"], task["subject_id"], task["teacher_id"]
        teacher = idx["teachers"][tid]
        options = []
        for key in task["cells"]:
            p = parse_grid_key(key)
            if key in working["grid"]:
                continue
            if p["shift"] not in teacher.get("shifts", list(SHIFTS)):
                continue
            unavail = teacher.get("unavailable_slots", [])
            if key in unavail or f"{p['day']}|{p['shift']}|{p['period']}" in unavail:
                continue
            if (tid, p["day"], p["shift"], p["period"]) in teacher_busy:
                continue
            score = (
                subject_day.get((cid, sid, p["day"]), 0) * 10
                + class_day.get((cid, p["day"]), 0) * 0.5
                + teacher_day.get((tid, p["day"]), 0) * 0.3
                + (0 if p["shift"] == "ព្រឹក" else 0.15)
                + rng.random() * 0.2
            )
            options.append((score, key))
        options.sort(key=lambda x: x[0])
        return [k for _s, k in options[:28]]  # cap branching factor

    def place(task: Dict[str, Any], key: str) -> None:
        p = parse_grid_key(key)
        cid, sid, tid, day = task["class_id"], task["subject_id"], task["teacher_id"], p["day"]
        working["grid"][key] = {
            "class_id": cid, "subject_id": sid, "teacher_id": tid,
            "day": day, "shift": p["shift"], "period": p["period"],
        }
        load[tid] = load.get(tid, 0) + 1
        teacher_busy.add((tid, day, p["shift"], p["period"]))
        subject_day[(cid, sid, day)] = subject_day.get((cid, sid, day), 0) + 1
        class_day[(cid, day)] = class_day.get((cid, day), 0) + 1
        teacher_day[(tid, day)] = teacher_day.get((tid, day), 0) + 1

    def unplace(task: Dict[str, Any], key: str) -> None:
        p = parse_grid_key(key)
        cid, sid, tid, day = task["class_id"], task["subject_id"], task["teacher_id"], p["day"]
        working["grid"].pop(key, None)
        load[tid] = max(0, load.get(tid, 0) - 1)
        teacher_busy.discard((tid, day, p["shift"], p["period"]))
        subject_day[(cid, sid, day)] = max(0, subject_day.get((cid, sid, day), 0) - 1)
        class_day[(cid, day)] = max(0, class_day.get((cid, day), 0) - 1)
        teacher_day[(tid, day)] = max(0, teacher_day.get((tid, day), 0) - 1)

    def solve(i: int) -> bool:
        nonlocal nodes, backtracks
        if i >= total_tasks:
            return True
        nodes += 1
        if nodes > max_nodes:
            return False
        task = tasks[i]
        teacher = idx["teachers"][task["teacher_id"]]
        if load.get(task["teacher_id"], 0) >= teacher["target"]:
            return solve(i + 1)  # skip: workload cap reached
        for key in rank(task):
            place(task, key)
            if solve(i + 1):
                return True
            unplace(task, key)
            backtracks += 1
            if nodes > max_nodes:
                return False
        # Soft failure: leave this lesson unassigned, continue with the rest.
        skipped.append({"reason": "no_free_cell", "teacher_id": task["teacher_id"],
                        "class_id": task["class_id"], "subject_id": task["subject_id"]})
        return solve(i + 1)

    solve(0)

    after_keys = set(working["grid"].keys())
    diff = {
        "added": sorted(after_keys - before_keys),
        "removed": sorted(before_keys - after_keys),
        "unchanged": len(before_keys & after_keys),
    }
    return {
        "state": working,
        "placed": len(diff["added"]),
        "requested": total_tasks,
        "skipped": skipped[:50],
        "backtracks": backtracks,
        "nodes": nodes,
        "diff": diff,
        "stats": statistics(working),
    }


# ── Critical Reassignment Engine (Section 8) ──────────────────────────────

def reassign_teacher_in_class(state: Dict[str, Any], class_id: str, subject_id: str,
                              new_teacher_id: str, old_teacher_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Section 8: When class already has scheduled lessons and assigned teacher changes:
    Preserve valid timetable placements whenever possible.
    If valid, retain slot and replace teacher with new_teacher_id.
    If invalid (conflict), remove that lesson from draft grid and return to unscheduled pool.
    Recalculate counters and explain affected lessons.
    """
    idx = _index(state)
    new_teacher = idx["teachers"].get(new_teacher_id)
    if not new_teacher:
        raise ValueError(f"Teacher not found: {new_teacher_id}")

    # 1. Update assignment records
    asg_found = False
    for a in state["assignments"]:
        if a["class_id"] == class_id and a["subject_id"] == subject_id:
            if old_teacher_id is None or a.get("teacher_id") == old_teacher_id:
                old_tid = a.get("teacher_id")
                a["teacher_id"] = new_teacher_id
                asg_found = True
    if not asg_found:
        sub = idx["subjects"].get(subject_id)
        lessons = sub["lessons_per_week"] if sub else 2
        state["assignments"].append({
            "id": f"asg_{class_id}_{subject_id}_{new_teacher_id}",
            "class_id": class_id,
            "subject_id": subject_id,
            "teacher_id": new_teacher_id,
            "lessons": lessons,
            "shift": "ព្រឹក",
        })

    # 2. Inspect existing placed lessons for this class & subject
    preserved_keys = []
    displaced_keys = []
    affected_cells = []

    grid_items = list(state["grid"].items())
    for key, cell in grid_items:
        if cell.get("class_id") == class_id and cell.get("subject_id") == subject_id:
            if old_teacher_id is not None and cell.get("teacher_id") != old_teacher_id:
                continue
            
            p = parse_grid_key(key)
            day, shift, period = p["day"], p["shift"], p["period"]

            # Conflict checks for new_teacher:
            # (a) Is new_teacher busy elsewhere?
            is_busy = False
            for ok, other_cell in state["grid"].items():
                if ok != key and other_cell.get("teacher_id") == new_teacher_id:
                    op = parse_grid_key(ok)
                    if op["day"] == day and op["shift"] == shift and op["period"] == period:
                        is_busy = True
                        break
            
            # (b) Shift mismatch
            shift_ok = shift in new_teacher.get("shifts", list(SHIFTS))

            # (c) Unavailability
            unavail = new_teacher.get("unavailable_slots", [])
            is_unavail = (key in unavail) or (f"{day}|{shift}|{period}" in unavail) or (f"{day}|{period}" in unavail)

            if not is_busy and shift_ok and not is_unavail:
                # PRESERVED
                cell["teacher_id"] = new_teacher_id
                preserved_keys.append(key)
                affected_cells.append({
                    "key": key, "status": "preserved", "day": day, "shift": shift, "period": period,
                    "reason_kh": f"បានរក្សាទុកម៉ោងបង្រៀន · គ្រូថ្មី {new_teacher['code']} ទំនេរ",
                    "reason_en": f"Preserved slot: new teacher {new_teacher['code']} is available",
                })
            else:
                # DISPLACED
                state["grid"].pop(key, None)
                displaced_keys.append(key)
                reasons = []
                if is_busy:
                    reasons.append("គ្រូថ្មីជាប់បង្រៀនថ្នាក់ផ្សេង")
                if not shift_ok:
                    reasons.append(f"គ្រូថ្មីមិនមានវេន{shift}")
                if is_unavail:
                    reasons.append("គ្រូថ្មីឈប់សម្រាកក្នុងម៉ោងនេះ")
                affected_cells.append({
                    "key": key, "status": "displaced", "day": day, "shift": shift, "period": period,
                    "reason_kh": f"បានដកចេញទៅបញ្ជីមិនទាន់តម្រៀប៖ {', '.join(reasons)}",
                    "reason_en": f"Displaced to unscheduled pool due to conflicts: {', '.join(reasons)}",
                })

    return {
        "class_id": class_id,
        "subject_id": subject_id,
        "new_teacher_id": new_teacher_id,
        "old_teacher_id": old_teacher_id,
        "preserved_count": len(preserved_keys),
        "displaced_count": len(displaced_keys),
        "preserved_keys": preserved_keys,
        "displaced_keys": displaced_keys,
        "details": affected_cells,
        "stats": statistics(state),
    }


# ── Timetable Publishing & Downstream Queries (Section 18) ────────────────

def publish_timetable(state: Dict[str, Any], published_by: str = "Admin", note: str = "") -> Dict[str, Any]:
    """
    Publish the active draft timetable to live Teacher and Student portals.
    Blocks if hard conflicts exist. Records version history.
    """
    conflicts = [c for c in scan_conflicts(state) if c["severity"] == "error"]
    if conflicts:
        raise ValueError(f"Cannot publish with {len(conflicts)} hard conflict(s)")

    current_pub = state.get("published")
    next_ver = (current_pub.get("version", 0) + 1) if current_pub else 1

    snapshot = {
        "version": next_ver,
        "published_at": utc_now(),
        "published_by": published_by,
        "note": note,
        "academic_year": state.get("institution", {}).get("academic_year", "ឆ្នាំសិក្សា ២០២៦–២០២៧"),
        "grid": deepcopy(state.get("grid", {})),
        "assignments": deepcopy(state.get("assignments", [])),
        "subjects": deepcopy(state.get("subjects", [])),
        "teachers": deepcopy(state.get("teachers", [])),
        "classes": deepcopy(state.get("classes", [])),
        "settings": deepcopy(state.get("settings", {})),
        "institution": deepcopy(state.get("institution", {})),
        "stats": statistics(state),
    }
    state["published"] = snapshot
    pub_history = state.setdefault("published_history", [])
    pub_history.append({
        "version": next_ver,
        "published_at": snapshot["published_at"],
        "published_by": published_by,
        "note": note,
        "placed": len(snapshot["grid"]),
        "unassigned": snapshot["stats"]["unassigned"],
    })
    return snapshot


def get_published_timetable(state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return state.get("published")


def get_teacher_timetable(state: Dict[str, Any], teacher_id_or_code: str, use_published: bool = True) -> Dict[str, Any]:
    source = state.get("published") if (use_published and state.get("published")) else state
    if not source:
        source = state
    idx = _index(source)
    teacher = idx["teachers"].get(teacher_id_or_code)
    if not teacher:
        for t in source["teachers"]:
            if t.get("code") == teacher_id_or_code or t.get("employee_id") == teacher_id_or_code or t.get("name_kh") == teacher_id_or_code:
                teacher = t
                break
    if not teacher:
        return {"success": False, "error": "Teacher not found", "lessons": []}

    tid = teacher["id"]
    lessons = []
    for key, cell in source["grid"].items():
        if cell.get("teacher_id") == tid:
            p = parse_grid_key(key)
            cls = idx["classes"].get(cell.get("class_id"), {})
            sub = idx["subjects"].get(cell.get("subject_id"), {})
            lessons.append({
                "key": key,
                "day": p["day"],
                "shift": p["shift"],
                "period": p["period"],
                "class_id": cell.get("class_id"),
                "class_display": cls.get("display", cell.get("class_id")),
                "subject_id": cell.get("subject_id"),
                "subject_name": sub.get("name_kh", cell.get("subject_id")),
                "subject_code": sub.get("code", ""),
                "color": sub.get("color", "#F7C948"),
                "teacher_id": tid,
                "teacher_code": teacher["code"],
                "teacher_name": teacher["name_kh"],
                "room": cell.get("room", cls.get("room", "")),
            })
    return {
        "success": True,
        "teacher": teacher,
        "lessons": lessons,
        "total_lessons": len(lessons),
        "target": teacher.get("target", 17),
        "version": source.get("version", 1),
    }


def get_class_timetable(state: Dict[str, Any], class_id_or_display: str, use_published: bool = True) -> Dict[str, Any]:
    source = state.get("published") if (use_published and state.get("published")) else state
    if not source:
        source = state
    idx = _index(source)
    cls = idx["classes"].get(class_id_or_display)
    if not cls:
        for c in source["classes"]:
            if c.get("display") == class_id_or_display:
                cls = c
                break
    if not cls:
        return {"success": False, "error": "Class not found", "lessons": []}

    cid = cls["id"]
    lessons = []
    for key, cell in source["grid"].items():
        if cell.get("class_id") == cid:
            p = parse_grid_key(key)
            sub = idx["subjects"].get(cell.get("subject_id"), {})
            tch = idx["teachers"].get(cell.get("teacher_id"), {})
            lessons.append({
                "key": key,
                "day": p["day"],
                "shift": p["shift"],
                "period": p["period"],
                "class_id": cid,
                "class_display": cls["display"],
                "subject_id": cell.get("subject_id"),
                "subject_name": sub.get("name_kh", cell.get("subject_id")),
                "subject_code": sub.get("code", ""),
                "color": sub.get("color", "#F7C948"),
                "teacher_id": cell.get("teacher_id"),
                "teacher_code": tch.get("code", ""),
                "teacher_name": tch.get("name_kh", ""),
                "room": cell.get("room", cls.get("room", "")),
            })
    return {
        "success": True,
        "class": cls,
        "lessons": lessons,
        "total_lessons": len(lessons),
        "version": source.get("version", 1),
    }


# ── Persistent store ───────────────────────────────────────────────────────

class TimetableStore:
    """Thread-safe JSON document store with an append-only change log."""

    def __init__(self, path: str = STATE_PATH):
        self.path = path
        self._lock = threading.RLock()
        self._state: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        with self._lock:
            if os.path.isfile(self.path):
                try:
                    with open(self.path, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                    if (isinstance(data, dict) and "grid" in data and "subjects" in data
                            and data.get("schema_version") == SCHEMA_VERSION):
                        self._state = data
                        return self.state()
                except (json.JSONDecodeError, OSError):
                    pass
            self._state = build_seed_state()
            self._persist()
            return self.state()

    def state(self) -> Dict[str, Any]:
        return deepcopy(self._state)

    def _persist(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self._state, fh, ensure_ascii=False, separators=(",", ":"))
        os.replace(tmp, self.path)

    def replace(self, state: Dict[str, Any], label: str = "រក្សាទុក") -> Dict[str, Any]:
        with self._lock:
            self._state = deepcopy(state)
            self._state["revision"] = int(self._state.get("revision", 0)) + 1
            self._state["updated_at"] = utc_now()
            self._log(label)
            self._persist()
            return self.state()

    def patch_grid(self, key: str, cell: Optional[Dict[str, Any]],
                   label: str = "កំណត់ម៉ោង") -> Dict[str, Any]:
        with self._lock:
            if cell is None:
                self._state["grid"].pop(key, None)
            else:
                self._state["grid"][key] = cell
            self._state["revision"] = int(self._state.get("revision", 0)) + 1
            self._state["updated_at"] = utc_now()
            self._log(label, {"key": key, "cell": cell})
            self._persist()
            return self.state()

    def _log(self, label: str, detail: Optional[Dict[str, Any]] = None) -> None:
        history = self._state.setdefault("history", [])
        history.append({
            "id": f"h{len(history) + 1}", "at": utc_now(),
            "label": label, "detail": detail or {},
        })
        del history[:-100]  # keep the last 100 changes

    def history(self) -> List[Dict[str, Any]]:
        return list(reversed(self._state.get("history", [])))

    def reassign(self, class_id: str, subject_id: str, new_teacher_id: str,
                 old_teacher_id: Optional[str] = None) -> Dict[str, Any]:
        with self._lock:
            result = reassign_teacher_in_class(self._state, class_id, subject_id, new_teacher_id, old_teacher_id)
            self._state["revision"] = int(self._state.get("revision", 0)) + 1
            self._state["updated_at"] = utc_now()
            self._log(f"ប្តូរគ្រូបង្រៀន {class_id}", result)
            self._persist()
            return result

    def publish(self, published_by: str = "Admin", note: str = "") -> Dict[str, Any]:
        with self._lock:
            published = publish_timetable(self._state, published_by=published_by, note=note)
            self._state["revision"] = int(self._state.get("revision", 0)) + 1
            self._state["updated_at"] = utc_now()
            self._log(f"បោះពុម្ពផ្សាយកាលវិភាគ v{published['version']}", {"published_by": published_by})
            self._persist()
            return published

    def published(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            return get_published_timetable(self._state)

    def teacher_timetable(self, teacher_id_or_code: str, use_published: bool = True) -> Dict[str, Any]:
        with self._lock:
            return get_teacher_timetable(self._state, teacher_id_or_code, use_published=use_published)

    def class_timetable(self, class_id_or_display: str, use_published: bool = True) -> Dict[str, Any]:
        with self._lock:
            return get_class_timetable(self._state, class_id_or_display, use_published=use_published)

    def reset(self) -> Dict[str, Any]:
        with self._lock:
            self._state = build_seed_state()
            self._persist()
            return self.state()


STORE = TimetableStore()
TIMETABLE_STORE = STORE  # alias for backwards-compatible imports
