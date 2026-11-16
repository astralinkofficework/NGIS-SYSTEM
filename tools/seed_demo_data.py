"""
NGIS-SYSTEM — Demo Data Seeder (NGIS_DEMO_2026)
================================================
Populates every implemented module with realistic, interconnected demo data
using the application's REAL data stores (data/*.json + .data/academic.sqlite3)
and the existing schema — no frontend hardcoding.

Safety:
  - Development-only: refuses to run unless every marker below holds.
  - Reversible:  full backup of every touched file into scratch/demo_backup/<ts>/
  - Idempotent:  purges ONLY its own records (identified by the NGIS_DEMO_2026
                 markers: @demo.ngis.edu.kh e-mails, DMO- id prefixes,
                 created_by == 'NGIS_DEMO_2026') and re-generates deterministically.
  - Deterministic: random.seed(2026) -> stable identities between runs.
  - Existing records are NEVER modified or deleted.

Usage:
    python tools/seed_demo_data.py            # seed (purge own + regenerate)
    python tools/seed_demo_data.py --purge    # remove only NGIS_DEMO_2026 records
    python tools/seed_demo_data.py --verify   # print current demo/real counts

After seeding, restart the Flask server so in-memory overlays reload.
"""
from __future__ import annotations

import json
import os
import random
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
ACADEMIC_DB = os.path.join(ROOT, ".data", "academic.sqlite3")
BACKUP_ROOT = os.path.join(ROOT, "scratch", "demo_backup")

TAG = "NGIS_DEMO_2026"
DEMO_DOMAIN = "demo.ngis.edu.kh"

COUNTS = {"students": 200, "teachers": 30, "staff": 15, "principals": 2, "admins": 5}

random.seed(2026)

# ── Name pools (fictional Cambodian + international mix) ──────────────
GIVEN = ["Sopha", "Dara", "Sokha", "Chantha", "Sreyleak", "Piseth", "Chamroeun",
         "Vichea", "Sophea", "Ratha", "Veasna", "Dary", "Bopha", "Sokhom",
         "Malis", "Kanha", "Vuthy", "Chantrea", "Panha", "Chhorvy", "Sopheak",
         "Visal", "Phalla", "Samnang", "Kagna", "Theara", "Bunchhay", "Kosol",
         "Rachana", "Sovann", "Nimol", "Chenda", "Ravy", "Seila", "Oudom",
         "Pheakdey", "Sreymom", "Dalin", "Vibol", "Kanika"]
SURNAME = ["Kim", "Sok", "Ly", "Pov", "Rin", "Chhem", "Heng", "Meas", "Vannak",
           "Chea", "Khuon", "Ou", "Prak", "Chhay", "Tep", "Nuon", "Yem", "Khieu",
           "Suos", "Thorn", "Im", "Yean", "Phen", "Sou", "Chou", "Lay", "Sar",
           "Keo", "Mao", "Sem"]
INTL_GIVEN = ["Sarah", "James", "Emily", "Daniel", "Grace", "Michael", "Anna",
              "Thomas", "Laura", "Kevin", "Rachel", "Brian", "Nadia", "Peter",
              "Muthukumaran", "Aiko", "Ravi", "Elena"]
INTL_SURNAME = ["Jenkins", "Odom", "Pakkirisamy", "Tanaka", "Miller", "Carter",
                "Nguyen", "Walsh", "Kumar", "Reyes", "Hoffman", "Dubois",
                "Santos", "Bridges", "Ferreira"]

DEPARTMENTS = ["Mathematics", "Science", "English", "Khmer Studies",
               "ICT & Computer Science", "Arts & Physical Education",
               "Social Studies"]
TEACHER_POSITIONS = ["Teacher", "Senior Teacher", "Lead Teacher", "Homeroom Teacher"]
STAFF_ROLES = ["Librarian", "Registrar", "Accountant", "IT Support Officer",
               "School Nurse", "Receptionist", "Security Lead", "Facilities Officer",
               "Admissions Officer", "Student Counselor", "Lab Assistant",
               "Data Entry Clerk", "HR Assistant", "Storekeeper", "Driver Supervisor"]
STAFF_DEPTS = ["Administration Office", "Library & Media", "Finance Office",
               "ICT Support Unit", "Student Affairs", "Facilities & Security",
               "Admissions Office", "Health Services"]


def jload(name, default):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return default
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def jwrite(name, payload):
    p = os.path.join(DATA, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def is_demo(rec: dict) -> bool:
    """True only for records created by this seeder."""
    if not isinstance(rec, dict):
        return False
    email = str(rec.get("email") or rec.get("username") or rec.get("guardianEmail") or "")
    if email.endswith("@" + DEMO_DOMAIN):
        return True
    rid = str(rec.get("id") or rec.get("refId") or "")
    if rid.startswith(("DMO-", "SR-DMO", "REG-DMO", "TAS-DEMO", "TAT-DEMO",
                       "COM-DMO", "DISC-DMO", "LF-2026-DMO", "USR-DMO",
                       "TCH-DEMO", "STF-DEMO", "PRN-DEMO", "ADM-DEMO")):
        return True
    return rec.get("created_by") == TAG


def demo_name(used: set, intl: bool = False) -> str:
    for _ in range(80):
        g = random.choice(INTL_GIVEN if intl else GIVEN)
        s = random.choice(INTL_SURNAME if intl else SURNAME)
        name = f"{g} {s}" if intl else f"{g} {s}"
        if name not in used:
            used.add(name)
            return name
    suffix = len(used)
    name = f"{random.choice(GIVEN)} {random.choice(SURNAME)} {suffix}"
    used.add(name)
    return name


def demo_phone(i: int) -> str:
    return f"+855 11 2{i // 100 % 10}{i % 100:02d} {random.randint(100, 999)}"


def demo_email(name: str, i: int) -> str:
    slug = name.lower().replace(".", "").replace(" ", ".")
    return f"{slug}.{i}@{DEMO_DOMAIN}"


# ── Backup / restore ──────────────────────────────────────────────────
TOUCHED = ["students_overlay.json", "teachers_overlay.json", "staff_overlay.json",
           "principals_overlay.json", "user_accounts.json", "teacher_assignments.json",
           "student_registrations.json", "student_commendations.json",
           "student_discipline.json", "teacher_attendance.json",
           "service_requests.json", "lost_found.json"]


def backup() -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(BACKUP_ROOT, ts)
    os.makedirs(dest, exist_ok=True)
    for name in TOUCHED:
        src = os.path.join(DATA, name)
        if os.path.exists(src):
            shutil.copy2(src, dest)
    if os.path.exists(ACADEMIC_DB):
        shutil.copy2(ACADEMIC_DB, os.path.join(dest, "academic.sqlite3"))
    return dest


# ── Purge (demo-owned records only) ───────────────────────────────────
def purge_json() -> None:
    for name in TOUCHED:
        p = os.path.join(DATA, name)
        if not os.path.exists(p):
            continue
        data = jload(name, None)
        if isinstance(data, list):
            kept = [r for r in data if not is_demo(r)]
            if len(kept) != len(data):
                jwrite(name, kept)
                print(f"  purged {len(data) - len(kept)} demo records from {name}")
        elif isinstance(data, dict) and "accounts" in data:
            accs = data.get("accounts", [])
            kept = [a for a in accs if not is_demo(a)]
            if len(kept) != len(accs):
                data["accounts"] = kept
                jwrite(name, data)
                print(f"  purged {len(accs) - len(kept)} demo accounts from {name}")


def purge_sqlite() -> None:
    if not os.path.exists(ACADEMIC_DB):
        return
    conn = sqlite3.connect(ACADEMIC_DB)
    cur = conn.cursor()
    for sql in [
        "DELETE FROM grades WHERE student_id LIKE 'DMO-%' OR id LIKE 'grd-dmo-%'",
        "DELETE FROM attendance WHERE student_id LIKE 'DMO-%'",
        "DELETE FROM enrollments WHERE student_id LIKE 'DMO-%'",
        "DELETE FROM grades WHERE assessment_id LIKE 'asm-dmo-%'",
        "DELETE FROM assessments WHERE id LIKE 'asm-dmo-%'",
        "DELETE FROM teacher_assignments WHERE teacher_id LIKE 'DMO-%'",
    ]:
        cur.execute(sql)
    conn.commit()
    n = cur.rowcount
    conn.close()
    print(f"  purged demo rows from academic.sqlite3 (last stmt rows={n})")


# ── Generators ────────────────────────────────────────────────────────
def load_reference():
    tt = jload("timetable_state.json", {})
    classes = tt.get("classes", [])
    return classes


def gen_students(classes, teacher_names):
    used = set()
    out = []
    per = len(classes)
    for i in range(1, COUNTS["students"] + 1):
        cls = classes[(i - 1) % per]
        gender = random.choice(["F", "M"])
        name = demo_name(used, intl=random.random() < 0.06)
        first, last = name.split()[0], name.split()[-1]
        parent_first = random.choice(GIVEN)
        gpa = round(random.uniform(1.7, 4.0), 1)
        # a believable spread: a few struggling, many mid, some top
        gpa = min(4.0, max(1.5, round(random.gauss(2.9, 0.55), 1)))
        att = random.choice([random.randint(72, 92), random.randint(90, 98),
                             random.choice([100, 100, 99])])
        status = random.choices(["active", "pending"], weights=[93, 7])[0]
        out.append({
            "id": f"DMO-STD-{i:04d}",
            "name": name,
            "gender": gender,
            "grade": f"Grade {cls['grade']}",
            "class": cls["display"],
            "gpa": gpa,
            "attendance": att,
            "status": status,
            "parentEmail": f"{parent_first.lower()}.{last.lower()}@example.com",
            "parentName": f"{random.choice(SURNAME)} {parent_first}",
            "advisor": random.choice(teacher_names) if teacher_names else "",
            "created_by": TAG,
        })
    return out


def gen_teachers():
    used = set()
    out = []
    for i in range(1, COUNTS["teachers"] + 1):
        intl = random.random() < 0.25
        name = demo_name(used, intl=intl)
        dept = random.choice(DEPARTMENTS)
        email = demo_email(name, i)
        title = random.choice(["Mr.", "Ms.", "Dr."]) if not intl else ""
        full = (title + " " + name).strip()
        out.append({
            "id": f"TCH-DEMO-{i:03d}",
            "name": full,
            "email": email,
            "phone": demo_phone(i),
            "department": dept,
            "position": random.choice(TEACHER_POSITIONS),
            "subjects": [dept if dept in DEPARTMENTS else dept],
            "classes": [],
            "homeroom": "",
            "status": random.choices(["active", "pending"], weights=[95, 5])[0],
            "campus": random.choice(["Tuol Kork Main Campus", "Depo Campus", "Sen Sok Campus"]),
            "created_by": TAG,
        })
    return out


def gen_staff():
    used = set()
    out = []
    for i in range(1, COUNTS["staff"] + 1):
        name = demo_name(used, intl=random.random() < 0.12)
        out.append({
            "id": f"STF-DEMO-{i:03d}",
            "name": name,
            "email": demo_email(name, 1000 + i),
            "phone": demo_phone(1500 + i),
            "department": STAFF_DEPTS[i % len(STAFF_DEPTS)],
            "role": STAFF_ROLES[i % len(STAFF_ROLES)],
            "created_by": TAG,
        })
    return out


def gen_principals():
    used = set()
    titles = ["Lower Secondary Principal", "Upper Secondary Principal"]
    out = []
    for i in range(1, COUNTS["principals"] + 1):
        name = demo_name(used, intl=i == 2)
        out.append({
            "id": f"PRN-DEMO-{i:03d}",
            "name": f"Dr. {name}",
            "email": demo_email(name, 2000 + i),
            "phone": demo_phone(2000 + i),
            "department": "Academic Leadership",
            "position": titles[i - 1],
            "created_by": TAG,
        })
    return out


ROLE_MAP = {"student": "STUDENT", "teacher": "TEACHER", "staff": "STAFF",
            "principal": "PRINCIPAL", "admin": "ADMIN"}


def gen_accounts(students, teachers, staff, principals, admins):
    """Accounts for every demo person — no password hashes, matching the
    app's documented 'seeded demo accounts sign in through AUTH_USERS /
    provision flow' behaviour (user_management_api.authenticate_store_account)."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = []
    seq = 0

    def add(person_type, person_id, name, dept, campus, assignment):
        nonlocal seq
        seq += 1
        status = random.choices(
            ["active", "pending_activation", "suspended", "disabled"],
            weights=[86, 9, 3, 2])[0]
        email = None
        if person_type == "student":
            email = f"{person_id.lower()}@{DEMO_DOMAIN}"
        else:
            email = f"{person_id.lower()}@{DEMO_DOMAIN}"
        out.append({
            "id": f"USR-DMO-{seq:03d}",
            "person_type": person_type,
            "person_id": person_id,
            "name": name,
            "username": email,
            "email": email,
            "role": ROLE_MAP[person_type],
            "display_role": ROLE_MAP[person_type],
            "campus": campus,
            "department": dept,
            "assignment": assignment,
            "status": status,
            "identity_source": "person",
            "created_by": TAG,
            "created_at": now,
            "last_login": "",
            "failed_attempts": 0,
        })

    for s in students:
        add("student", s["id"], s["name"], f"{s['grade']} · {s['class']}",
            "Tuol Kork Main Campus", s["class"])
    for t in teachers:
        add("teacher", t["id"], t["name"], t["department"], t["campus"],
            ", ".join(t["classes"]) or t["department"])
    for p in staff:
        add("staff", p["id"], p["name"], p["department"], "Tuol Kork Main Campus",
            p["role"])
    for p in principals:
        add("principal", p["id"], p["name"], p["department"], "Tuol Kork Main Campus",
            p["position"])
    for a in admins:
        add("admin", a["id"], a["name"], a["department"], "Tuol Kork Main Campus",
            a["position"])
    return out


def gen_admins():
    used = set()
    out = []
    titles = ["System Administrator", "Registrar Administrator",
              "IT Administrator", "Academic Administrator", "Operations Administrator"]
    for i in range(1, COUNTS["admins"] + 1):
        name = demo_name(used, intl=i % 2 == 0)
        out.append({
            "id": f"ADM-DEMO-{i:03d}",
            "name": name,
            "email": demo_email(name, 3000 + i),
            "phone": demo_phone(3000 + i),
            "department": "Central Administration",
            "position": titles[i - 1],
            "created_by": TAG,
        })
    return out


def gen_teacher_assignments(teachers, classes):
    out = []
    subs_by_dept = {
        "Mathematics": ("subj-math", "Advanced Mathematics"),
        "Science": ("subj-phys", "Physics & Lab"),
        "English": ("subj-eng", "English Literature"),
        "Khmer Studies": ("subj-khmer-11", "Khmer Language G11"),
        "ICT & Computer Science": ("subj-ap-macro", "AP Macroeconomics"),
        "Arts & Physical Education": ("subj-art-cp", "Art CP"),
        "Social Studies": ("subj-ap-precalc", "AP Pre-Calculus"),
    }
    for i, t in enumerate(teachers, 1):
        sid, sname = subs_by_dept.get(t["department"], ("subj-math", "Advanced Mathematics"))
        cls = classes[i % len(classes)]
        # 1-2 class sections per teacher
        second = classes[(i + 5) % len(classes)]
        chosen = {cls["display"], second["display"]}
        for j, disp in enumerate(sorted(chosen), 1):
            out.append({
                "id": f"TAS-DEMO-{i:03d}{j}",
                "teacherId": t["id"],
                "teacherName": t["name"],
                "department": t["department"],
                "subjectId": sid,
                "subjectName": sname,
                "classId": f"cls-{disp.lower()}",
                "className": f"Grade {disp}",
                "periodsPerWeek": random.choice([4, 5, 6]),
                "room": f"Room {random.randint(101, 499)}",
                "academicYear": "2025-2026",
                "semester": "Semester 2",
                "status": "active",
            })
        # homeroom for every 3rd teacher
        if i % 3 == 0:
            t["homeroom"] = cls["display"]
            t["classes"] = sorted(chosen)
        else:
            t["classes"] = sorted(chosen)
    return out


# ── SQLite academic store ─────────────────────────────────────────────
def seed_sqlite(students):
    conn = sqlite3.connect(ACADEMIC_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    year = cur.execute("SELECT id FROM academic_years ORDER BY id DESC LIMIT 1").fetchone()[0]
    open_periods = [r[0] for r in cur.execute(
        "SELECT id FROM grading_periods WHERE status='open'")]
    subjects = [dict(r) for r in cur.execute("SELECT id, name FROM subjects WHERE status='active'")]

    # Enroll every demo student (class_id derived from students_overlay class)
    for s in students:
        cur.execute(
            "INSERT OR REPLACE INTO enrollments (student_id, class_id, academic_year_id, status)"
            " VALUES (?,?,?,?)",
            (s["id"], f"cls-{s['class'].lower()}", year, "active"))

    # Class-level assessments for every class (2 open periods x 2 subjects)
    core = subjects[:4]
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    asm_rows, asm_meta = [], []
    for cls in sorted({f"cls-{s['class'].lower()}" for s in students}):
        for period in open_periods[:2]:
            for subj in core[:2]:
                aid = f"asm-dmo-{cls}-{period}-{subj['id']}"
                status = "published" if random.random() < 0.7 else "draft"
                asm_rows.append((aid, cls, subj["id"], period,
                                 f"{period.split('-')[-1].upper()} Demo Assessment — {subj['name']}",
                                 random.choice(["Quiz", "Homework", "Project", "Participation"]),
                                 100.0, 1.0, "TCH-2024-042", status, now, None))
                asm_meta.append((aid, cls, subj["id"], status))
    cur.executemany(
        "INSERT OR REPLACE INTO assessments (id, class_id, subject_id, grading_period_id,"
        " title, category, max_score, weight, teacher_id, status, created_at, due_date)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", asm_rows)

    # Grades for published assessments (varied workflow states)
    grade_rows = []
    att_rows = []
    today = datetime.now()
    grade_seq = 0
    for aid, cls, _sid, status in asm_meta:
        if status != "published":
            continue
        roster = [s["id"] for s in students if f"cls-{s['class'].lower()}" == cls]
        for sid in roster:
            score = min(100.0, max(30.0, random.gauss(76, 14)))
            workflow = random.choices(
                ["published", "submitted", "approved", "rejected"],
                weights=[55, 25, 15, 5])[0]
            grade_seq += 1
            grade_rows.append((f"grd-dmo-{grade_seq:05d}", aid, sid, round(score, 1),
                               "graded", "", workflow, "TCH-2024-042", now, now))

    # Daily attendance: last 15 weekdays per student
    d = today
    weekdays = []
    while len(weekdays) < 15:
        if d.weekday() < 5:
            weekdays.append(d.strftime("%Y-%m-%d"))
        d -= timedelta(days=1)
    for s in students:
        for dt in weekdays:
            st = random.choices(["present", "tardy", "excused", "absent"],
                                weights=[88, 5, 3, 4])[0]
            att_rows.append((f"att-dmo-{s['id']}-{dt}", s["id"],
                             f"cls-{s['class'].lower()}", "", dt, "daily", st,
                             "", "submitted", "TCH-2024-042", now, now))
    cur.executemany(
        "INSERT OR REPLACE INTO grades (id, assessment_id, student_id, score, state,"
        " comments, workflow, recorded_by, recorded_at, updated_at)"
        " VALUES (?,?,?,?,?,?,?,?,?,?)", grade_rows)
    cur.executemany(
        "INSERT OR REPLACE INTO attendance (id, student_id, class_id, subject_id,"
        " attendance_date, session, status, note, workflow, recorded_by, recorded_at, updated_at)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", att_rows)
    conn.commit()
    conn.close()
    print(f"  sqlite: enrollments={len(students)}, assessments={len(asm_rows)},"
          f" grades={len(grade_rows)}, attendance={len(att_rows)}")


def gen_registrations(classes):
    used = set()
    statuses = ["pending", "missing_docs", "approved"]
    docs = ["Birth Certificate", "Grade 9 MoEYS Diploma", "Transcript", "Medical Record"]
    out = []
    for i in range(1, 7):
        name = demo_name(used)
        cls = classes[i % len(classes)]
        st = statuses[i % 3]
        out.append({
            "id": f"REG-DMO-{i:03d}",
            "applicantName": name,
            "gender": random.choice(["F", "M"]),
            "dob": f"{random.randint(2008, 2012)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "appliedGrade": f"Grade {cls['grade']}",
            "appliedCampus": cls["campus"],
            "previousSchool": random.choice([
                "Zaman International School", "Beltei International School",
                " Bak Touk High School", "Wat Koh High School", "IIS Rcanda"]),
            "gpaPrevious": round(random.uniform(2.0, 3.9), 2),
            "guardianName": f"{random.choice(SURNAME)} {random.choice(GIVEN)}",
            "guardianPhone": demo_phone(4000 + i),
            "guardianEmail": f"guardian.dmo{i}@example.com",
            "submittedAt": (datetime.now() - timedelta(days=i * 2)).strftime("%Y-%m-%d"),
            "documents": docs[:random.randint(2, 4)],
            "status": st,
            "interviewScore": f"{random.randint(60, 95)}/100",
            "allocatedClass": cls["display"] if st == "approved" else "",
            "notes": "NGIS_DEMO_2026 demonstration application.",
            "created_by": TAG,
        })
    return out


def gen_service_requests(students):
    cats = [("document", "certificate", "Certificate of Enrollment request"),
            ("document", "transcript", "Official transcript copy request"),
            ("technical", "portal", "Parent portal access reset"),
            ("academic", "records", "Grade record correction request")]
    out = []
    for i, (cat, typ, title) in enumerate(cats, 1):
        s = students[random.randrange(len(students))]
        out.append({
            "id": f"SR-DMO-{i:03d}",
            "studentId": s["id"],
            "studentName": s["name"],
            "role": "student",
            "category": cat,
            "type": typ,
            "title": title,
            "description": "NGIS_DEMO_2026 demonstration service request.",
            "status": random.choices(["open", "completed"], weights=[60, 40])[0],
            "priority": random.choice(["normal", "high"]),
            "campus": random.choice(["Tuol Kork Main Campus", "Sen Sok Campus", "Depo Campus"]),
            "assignee": "Operations & Academic Facilities",
            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            "updatedAt": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            "comments": [],
            "created_by": TAG,
        })
    return out


def gen_lost_found():
    items = [("lost", "Demo — Navy NGIS Hoodie", "clothing", "Covered Walkway B"),
             ("found", "Demo — Scientific Calculator fx-991", "electronics", "Room 210"),
             ("lost", "Demo — Khmer Literature Textbook G11", "books", "Library Reading Hall"),
             ("found", "Demo — Student ID Card (demo holder)", "cards", "Canteen"),
             ("lost", "Demo — Black Water Bottle", "personal", "Basketball Court")]
    out = []
    for i, (typ, title, cat, loc) in enumerate(items, 1):
        d = datetime.now() - timedelta(days=i)
        out.append({
            "id": 9000 + i,
            "refId": f"LF-2026-DMO-{i:03d}",
            "type": typ,
            "title": title,
            "category": cat,
            "campus": random.choice(["Tuol Kork Main Campus", "Sen Sok Campus", "Depo Campus"]),
            "location": loc,
            "date": d.strftime("%Y-%m-%d"),
            "time": f"{random.randint(7, 17):02d}:{random.choice(['05', '15', '30', '45'])} {random.choice(['AM', 'PM'])}",
            "status": random.choice(["active", "matching", "ready_for_collection", "returned"]),
            "description": "NGIS_DEMO_2026 demonstration item — not a real report.",
            "privateDetails": "",
            "custodyLocation": "Lost & Found Office",
            "created_by": TAG,
        })
    return out


def gen_commendations(students):
    cats = [("Academic Excellence", "Demo Honor Citation"),
            ("Leadership", "Demo Student Council Leadership Award"),
            ("Community Service", "Demo Campus Clean-up Volunteer Recognition"),
            ("Improvement", "Demo Most-Improved Student Citation")]
    out = []
    for i, (cat, title) in enumerate(cats, 1):
        s = students[random.randrange(len(students))]
        out.append({
            "id": f"COM-DMO-{i:03d}",
            "studentId": s["id"],
            "studentName": s["name"],
            "class": s["class"],
            "category": cat,
            "title": title,
            "citation": "NGIS_DEMO_2026 demonstration commendation — fictional record for UI inspection.",
            "dateAwarded": (datetime.now() - timedelta(days=i * 3)).strftime("%Y-%m-%d"),
            "awardedBy": "Principal · Dr. Ly Bunheng",
            "status": "official",
            "created_by": TAG,
        })
    return out


def gen_discipline(students):
    rows = [("Attendance & Unauthorized Departure", "Moderate", "reported",
             "Left campus during lunch break without gate pass (demo)."),
            ("Uniform & Dress Code", "Minor", "resolved",
             "Repeated improper uniform during assembly week (demo)."),
            ("Academic Integrity", "Major", "under_review",
             "Suspicion of copied homework in Physics lab report (demo)."),
            ("Mobile Device Usage", "Minor", "investigation",
             "Phone usage during examination review session (demo).")]
    out = []
    for i, (cat, sev, st, desc) in enumerate(rows, 1):
        s = students[random.randrange(len(students))]
        out.append({
            "id": f"DISC-DMO-{i:03d}",
            "studentId": s["id"],
            "studentName": s["name"],
            "class": s["class"],
            "incidentDate": (datetime.now() - timedelta(days=i * 4)).strftime("%Y-%m-%d"),
            "category": cat,
            "severity": sev,
            "reportedBy": "Campus Security & Advisor",
            "description": desc,
            "actionTaken": "Parent notification issued; advisor follow-up scheduled (demo).",
            "status": st,
            "created_by": TAG,
        })
    return out


def gen_teacher_attendance(teachers):
    out = []
    for i, t in enumerate(teachers[:10], 1):
        st = random.choices(["present", "late", "absent"], weights=[88, 8, 4])[0]
        d = datetime.now() - timedelta(days=1)
        out.append({
            "id": f"TAT-DEMO-{i:03d}",
            "date": d.strftime("%Y-%m-%d"),
            "teacherId": t["id"],
            "teacherName": t["name"],
            "department": t["department"],
            "status": st,
            "checkIn": random.choice(["07:35 AM", "07:48 AM", "08:12 AM"]) if st != "absent" else "—",
            "checkOut": random.choice(["04:30 PM", "04:52 PM"]) if st != "absent" else "—",
            "biometricTerminal": f"Terminal Gate {random.randint(1, 3)} (Faculty)",
            "notes": "NGIS_DEMO_2026 demonstration record.",
            "created_by": TAG,
        })
    return out


# ── Orchestration ─────────────────────────────────────────────────────
def verify_environment():
    problems = []
    if not os.path.isdir(DATA):
        problems.append("data/ store not found")
    if os.environ.get("NGIS_PRODUCTION"):
        problems.append("NGIS_PRODUCTION env var is set — refusing")
    for req in ["students_overlay.json", "user_accounts.json", "timetable_state.json"]:
        if not os.path.exists(os.path.join(DATA, req)):
            problems.append(f"missing {req}")
    if problems:
        print("ENVIRONMENT CHECK FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("Environment check OK: local development stores found.")


def main():
    verify_environment()
    args = set(sys.argv[1:])
    if "--verify" in args:
        print_counts()
        return
    backup_dir = backup()
    print(f"Backup written to {backup_dir}")

    print("Purging previous NGIS_DEMO_2026 records (if any)…")
    purge_json()
    purge_sqlite()

    if "--purge" in args:
        print("Purge complete. Demo dataset removed; real records untouched.")
        return

    classes = load_reference()
    if not classes:
        print("No classes found in timetable_state.json — aborting.")
        sys.exit(1)

    print("Generating demo dataset…")
    teachers = gen_teachers()
    teacher_names = [t["name"] for t in teachers]
    students = gen_students(classes, teacher_names)
    staff = gen_staff()
    principals = gen_principals()
    admins = gen_admins()
    accounts = gen_accounts(students, teachers, staff, principals, admins)
    assignments = gen_teacher_assignments(teachers, classes)
    registrations = gen_registrations(classes)
    services = gen_service_requests(students)
    lostfound = gen_lost_found()
    commendations = gen_commendations(students)
    discipline = gen_discipline(students)
    tat = gen_teacher_attendance(teachers)

    # Merge into stores (existing records preserved)
    s = jload("students_overlay.json", [])
    s.extend(students); jwrite("students_overlay.json", s)

    t = jload("teachers_overlay.json", [])
    t.extend(teachers); jwrite("teachers_overlay.json", t)

    sf = jload("staff_overlay.json", [])
    sf.extend(staff); jwrite("staff_overlay.json", sf)

    pr = jload("principals_overlay.json", [])
    pr.extend(principals); jwrite("principals_overlay.json", pr)

    ua = jload("user_accounts.json", {"accounts": []})
    ua.setdefault("accounts", []).extend(accounts)
    jwrite("user_accounts.json", ua)

    ta = jload("teacher_assignments.json", [])
    ta.extend(assignments); jwrite("teacher_assignments.json", ta)

    rg = jload("student_registrations.json", [])
    rg.extend(registrations); jwrite("student_registrations.json", rg)

    srv = jload("service_requests.json", [])
    srv.extend(services); jwrite("service_requests.json", srv)

    lf = jload("lost_found.json", [])
    lf.extend(lostfound); jwrite("lost_found.json", lf)

    cm = jload("student_commendations.json", [])
    cm.extend(commendations); jwrite("student_commendations.json", cm)

    dc = jload("student_discipline.json", [])
    dc.extend(discipline); jwrite("student_discipline.json", dc)

    tatf = jload("teacher_attendance.json", [])
    tatf.extend(tat); jwrite("teacher_attendance.json", tatf)

    seed_sqlite(students)

    print("Seed complete.")
    print(f"  students +{len(students)}  teachers +{len(teachers)}  staff +{len(staff)}"
          f"  principals +{len(principals)}  admins +{len(admins)}  accounts +{len(accounts)}")
    print(f"  teacher assignments +{len(assignments)}  registrations +{len(registrations)}"
          f"  service requests +{len(services)}  lost&found +{len(lostfound)}")
    print("RESTART the Flask server so in-memory overlays reload.")


def print_counts():
    for name in TOUCHED:
        d = jload(name, None)
        if isinstance(d, list):
            demo = sum(1 for r in d if is_demo(r))
            print(f"{name}: total={len(d)} demo={demo}")
        elif isinstance(d, dict) and "accounts" in d:
            accs = d.get("accounts", [])
            demo = sum(1 for r in accs if is_demo(r))
            print(f"{name}: total={len(accs)} demo={demo}")
    if os.path.exists(ACADEMIC_DB):
        conn = sqlite3.connect(ACADEMIC_DB)
        cur = conn.cursor()
        for t in ["enrollments", "grades", "attendance", "assessments"]:
            n = cur.execute(f"SELECT COUNT(*) FROM {t} WHERE {'student_id' if t != 'assessments' else 'id'} LIKE 'DMO-%' OR {'student_id' if t != 'assessments' else 'id'} LIKE '%dmo-%'").fetchone()[0]
            print(f"academic.{t}: demo={n}")
        conn.close()


if __name__ == "__main__":
    main()
