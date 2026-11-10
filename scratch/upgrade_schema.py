import json, os, datetime

CONFIG_PATH = "data/system_configuration.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

# Ensure all required sections exist in system_configuration.json
now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1. Enhanced School Info
school_info = cfg.setdefault("school_info", {})
school_info.setdefault("shortName", "NGIS")
school_info.setdefault("description", "Leading bilingual international school delivering the Cambodian National Curriculum (MoEYS) and Cambridge International Assessment programs.")
school_info.setdefault("provinceCity", "Phnom Penh")
school_info.setdefault("country", "Cambodia")
school_info.setdefault("timezone", "Asia/Phnom_Penh (UTC+07:00)")
school_info.setdefault("primaryLanguage", "Khmer & English")
school_info.setdefault("supportedLanguages", ["Khmer", "English", "Mandarin Chinese"])
school_info.setdefault("academicDirector", "Dr. Pov Sophea")
school_info.setdefault("educationLevels", ["Early Years (Pre-K to K)", "Primary School (Grades 1-6)", "Lower Secondary (Grades 7-9)", "Upper Secondary (Grades 10-12)"])
school_info.setdefault("updatedAt", now_iso)
school_info.setdefault("updatedBy", "ADM-2024-001 (Mr. Heng Samnang)")

# 2. Campuses
if "campuses" not in cfg or not cfg["campuses"]:
    cfg["campuses"] = [
        {
            "id": "CMP-01",
            "code": "TK-MAIN",
            "name": "Tuol Kork Main Campus",
            "type": "Primary & Secondary",
            "address": "Street 289, Sangkat Boeung Kak 1, Khan Tuol Kork, Phnom Penh",
            "phone": "+855 23 888 777",
            "email": "tuolkork@ngis.edu.kh",
            "administrator": "Mr. Heng Samnang",
            "principal": "Dr. Ly Bunheng",
            "status": "active",
            "established": "2016",
            "academicLevels": ["Grades 1-6", "Grades 7-9", "Grades 10-12"],
            "departments": ["dept-mat", "dept-sci", "dept-eng", "dept-khm", "dept-chn", "dept-hum", "dept-art", "dept-ict"],
            "operatingDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "operatingHours": {"open": "07:00", "close": "17:00"},
            "saturdayEnabled": True
        },
        {
            "id": "CMP-02",
            "code": "CKM-SEC",
            "name": "Chamkarmon High School Branch",
            "type": "Upper Secondary & IB",
            "address": "Norodom Blvd, Sangkat Tonle Bassac, Khan Chamkarmon, Phnom Penh",
            "phone": "+855 23 888 778",
            "email": "chamkarmon@ngis.edu.kh",
            "administrator": "Ms. Keo Sreymom",
            "principal": "Dr. Sophal Meas",
            "status": "active",
            "established": "2020",
            "academicLevels": ["Grades 10-12"],
            "departments": ["dept-mat", "dept-sci", "dept-eng", "dept-khm", "dept-hum"],
            "operatingDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "operatingHours": {"open": "07:00", "close": "16:30"},
            "saturdayEnabled": False
        },
        {
            "id": "CMP-03",
            "code": "STEM-CTR",
            "name": "STEM & Robotics Innovation Hub",
            "type": "Specialized Tech Labs",
            "address": "Building C, Tuol Kork Campus, Phnom Penh",
            "phone": "+855 23 888 779",
            "email": "stem@ngis.edu.kh",
            "administrator": "Mr. Muthukumaran Pakkirisamy",
            "principal": "Dr. Ly Bunheng",
            "status": "active",
            "established": "2023",
            "academicLevels": ["Grades 7-12 Tech Electives"],
            "departments": ["dept-ict", "dept-sci"],
            "operatingDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "operatingHours": {"open": "08:00", "close": "17:30"},
            "saturdayEnabled": True
        }
    ]

# 3. Enhanced School Years & Terms
if "school_years" not in cfg or not cfg["school_years"]:
    cfg["school_years"] = [
        {
            "id": "SY-2026",
            "year": "2026–2027",
            "displayName": "Academic Year 2026–2027",
            "status": "active",
            "isCurrent": True,
            "startDate": "2026-09-01",
            "endDate": "2027-06-30",
            "enrollmentStart": "2026-07-01",
            "enrollmentEnd": "2026-08-25",
            "termsCount": 2,
            "terms": [
                {
                    "id": "TRM-2026-S1",
                    "name": "Semester 1 (ឆមាសទី១)",
                    "code": "S1",
                    "sequence": 1,
                    "startDate": "2026-09-01",
                    "endDate": "2027-01-22",
                    "status": "active"
                },
                {
                    "id": "TRM-2026-S2",
                    "name": "Semester 2 (ឆមាសទី២)",
                    "code": "S2",
                    "sequence": 2,
                    "startDate": "2027-02-08",
                    "endDate": "2027-06-30",
                    "status": "upcoming"
                }
            ]
        },
        {
            "id": "SY-2025",
            "year": "2025–2026",
            "displayName": "Academic Year 2025–2026",
            "status": "completed",
            "isCurrent": False,
            "startDate": "2025-09-01",
            "endDate": "2026-06-30",
            "enrollmentStart": "2025-07-01",
            "enrollmentEnd": "2025-08-25",
            "termsCount": 2,
            "terms": [
                { "id": "TRM-2025-S1", "name": "Semester 1", "code": "S1", "sequence": 1, "startDate": "2025-09-01", "endDate": "2026-01-23", "status": "completed" },
                { "id": "TRM-2025-S2", "name": "Semester 2", "code": "S2", "sequence": 2, "startDate": "2026-02-09", "endDate": "2026-06-30", "status": "completed" }
            ]
        },
        {
            "id": "SY-2027",
            "year": "2027–2028",
            "displayName": "Academic Year 2027–2028",
            "status": "draft",
            "isCurrent": False,
            "startDate": "2027-09-01",
            "endDate": "2028-06-30",
            "enrollmentStart": "2027-07-01",
            "enrollmentEnd": "2027-08-25",
            "termsCount": 2,
            "terms": [
                { "id": "TRM-2027-S1", "name": "Semester 1", "code": "S1", "sequence": 1, "startDate": "2027-09-01", "endDate": "2028-01-21", "status": "draft" },
                { "id": "TRM-2027-S2", "name": "Semester 2", "code": "S2", "sequence": 2, "startDate": "2028-02-07", "endDate": "2028-06-30", "status": "draft" }
            ]
        }
    ]

# 4. Operating Days & Hours
cfg["operating_schedule"] = cfg.get("operating_schedule") or {
    "weeklyDays": [
        {"day": "Monday", "khmer": "ច័ន្ទ", "open": True, "openTime": "07:00", "closeTime": "17:00"},
        {"day": "Tuesday", "khmer": "អង្គារ", "open": True, "openTime": "07:00", "closeTime": "17:00"},
        {"day": "Wednesday", "khmer": "ពុធ", "open": True, "openTime": "07:00", "closeTime": "17:00"},
        {"day": "Thursday", "khmer": "ព្រហស្បតិ៍", "open": True, "openTime": "07:00", "closeTime": "17:00"},
        {"day": "Friday", "khmer": "សុក្រ", "open": True, "openTime": "07:00", "closeTime": "17:00"},
        {"day": "Saturday", "khmer": "សៅរ៍", "open": True, "openTime": "07:00", "closeTime": "11:30", "optional": True},
        {"day": "Sunday", "khmer": "អាទិត្យ", "open": False, "openTime": "—", "closeTime": "—"}
    ],
    "shifts": {
        "morning": {"name": "Morning Shift (វេនព្រឹក)", "start": "07:00", "end": "11:10", "periods": 5},
        "recess": {"name": "Morning Recess (សម្រាក)", "start": "08:40", "end": "09:00", "durationMinutes": 20},
        "lunch": {"name": "Mid-day Lunch Break (សម្រាកថ្ងៃត្រង់)", "start": "11:10", "end": "13:00", "durationMinutes": 110},
        "afternoon": {"name": "Afternoon Shift (វេនរសៀល)", "start": "13:00", "end": "17:10", "periods": 5}
    },
    "saturdayEnabled": True,
    "closureDays": ["Sundays", "Gazetted National Holidays", "Severe Weather Warnings"]
}

# 5. Bell Schedule & Class Periods (Standard Cambodian MoEYS 10-Period Format)
cfg["bell_schedule"] = cfg.get("bell_schedule") or {
    "periodsPerDay": 10,
    "periodDurationMinutes": 50,
    "templateName": "MoEYS Standard Secondary Dual-Shift Bell Schedule",
    "periods": [
        {"number": 1, "shift": "morning", "shiftKhmer": "ព្រឹក", "label": "ព្រឹក 1 (Period 1)", "start": "07:00", "end": "07:50", "duration": 50, "isBreak": False},
        {"number": 2, "shift": "morning", "shiftKhmer": "ព្រឹក", "label": "ព្រឹក 2 (Period 2)", "start": "07:50", "end": "08:40", "duration": 50, "isBreak": False},
        {"number": 0, "shift": "recess", "shiftKhmer": "សម្រាក", "label": "សម្រាកព្រឹក (Recess)", "start": "08:40", "end": "09:00", "duration": 20, "isBreak": True},
        {"number": 3, "shift": "morning", "shiftKhmer": "ព្រឹក", "label": "ព្រឹក 3 (Period 3)", "start": "09:00", "end": "09:50", "duration": 50, "isBreak": False},
        {"number": 4, "shift": "morning", "shiftKhmer": "ព្រឹក", "label": "ព្រឹក 4 (Period 4)", "start": "09:50", "end": "10:40", "duration": 50, "isBreak": False},
        {"number": 5, "shift": "morning", "shiftKhmer": "ព្រឹក", "label": "ព្រឹក 5 (Period 5)", "start": "10:40", "end": "11:30", "duration": 50, "isBreak": False},
        {"number": 0, "shift": "lunch", "shiftKhmer": "អាហារថ្ងៃត្រង់", "label": "សម្រាកថ្ងៃត្រង់ (Lunch)", "start": "11:30", "end": "13:00", "duration": 90, "isBreak": True},
        {"number": 6, "shift": "afternoon", "shiftKhmer": "រសៀល", "label": "រសៀល 1 (Period 6)", "start": "13:00", "end": "13:50", "duration": 50, "isBreak": False},
        {"number": 7, "shift": "afternoon", "shiftKhmer": "រសៀល", "label": "រសៀល 2 (Period 7)", "start": "13:50", "end": "14:40", "duration": 50, "isBreak": False},
        {"number": 8, "shift": "afternoon", "shiftKhmer": "រសៀល", "label": "រសៀល 3 (Period 8)", "start": "14:40", "end": "15:30", "duration": 50, "isBreak": False},
        {"number": 9, "shift": "afternoon", "shiftKhmer": "រសៀល", "label": "រសៀល 4 (Period 9)", "start": "15:30", "end": "16:20", "duration": 50, "isBreak": False},
        {"number": 10, "shift": "afternoon", "shiftKhmer": "រសៀល", "label": "រសៀល 5 (Period 10)", "start": "16:20", "end": "17:10", "duration": 50, "isBreak": False}
    ]
}

# 6. Academic Calendar Events
cfg["academic_calendar"] = cfg.get("academic_calendar") or [
    {
        "id": "EVT-2026-001",
        "title": "Faculty Orientation & Planning Week",
        "category": "pd_day",
        "startDate": "2026-08-24",
        "endDate": "2026-08-28",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Annual curriculum alignment and teacher training workshop.",
        "status": "confirmed"
    },
    {
        "id": "EVT-2026-002",
        "title": "First Day of Academic Year 2026–2027",
        "category": "term_start",
        "startDate": "2026-09-01",
        "endDate": "2026-09-01",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Opening ceremony and student cohort onboarding.",
        "status": "confirmed"
    },
    {
        "id": "EVT-2026-003",
        "title": "Pchum Ben Festival (បុណ្យភ្ជុំបិណ្ឌ)",
        "category": "holiday",
        "startDate": "2026-10-10",
        "endDate": "2026-10-14",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Official national public holiday. School closed.",
        "status": "confirmed"
    },
    {
        "id": "EVT-2026-004",
        "title": "Semester 1 Mid-Term Assessments",
        "category": "exam",
        "startDate": "2026-11-09",
        "endDate": "2026-11-14",
        "campuses": ["All Campuses"],
        "grades": ["Grades 7-12"],
        "description": "Standardized mid-semester progress testing.",
        "status": "confirmed"
    },
    {
        "id": "EVT-2026-005",
        "title": "Water Festival (ព្រះរាជពិធីបុណ្យអុំទូក)",
        "category": "holiday",
        "startDate": "2026-11-23",
        "endDate": "2026-11-26",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Traditional Cambodian festival holiday.",
        "status": "confirmed"
    },
    {
        "id": "EVT-2026-006",
        "title": "Semester 1 Final Examinations",
        "category": "exam",
        "startDate": "2027-01-11",
        "endDate": "2027-01-16",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Comprehensive term 1 evaluation.",
        "status": "scheduled"
    },
    {
        "id": "EVT-2026-007",
        "title": "Semester 2 Commencement",
        "category": "term_start",
        "startDate": "2027-02-08",
        "endDate": "2027-02-08",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Second semester instructional start date.",
        "status": "scheduled"
    },
    {
        "id": "EVT-2026-008",
        "title": "Khmer New Year Celebration (ពិធីបុណ្យចូលឆ្នាំខ្មែរ)",
        "category": "holiday",
        "startDate": "2027-04-13",
        "endDate": "2027-04-17",
        "campuses": ["All Campuses"],
        "grades": ["All Grades"],
        "description": "Khmer Traditional New Year break.",
        "status": "scheduled"
    }
]

# 7. Timetable Rules Configuration
cfg["timetable_rules"] = cfg.get("timetable_rules") or {
    "activeAcademicYear": "2026–2027",
    "activeCampus": "TK-MAIN",
    "weeklyPeriodsTarget": 34,
    "maxPeriodsPerDay": 7,
    "maxConsecutiveHoursFaculty": 2,
    "maxConsecutiveHoursSubject": 2,
    "protectMorningRecess": True,
    "strictFacultyDoubleBooking": True,
    "strictRoomDoubleBooking": True,
    "homeroomAnchorDaily": True,
    "allowSplitShiftFaculty": False,
    "minRestBetweenShiftsMinutes": 60,
    "autoConflictResolutionMode": "smart_propose"
}

# 8. Staff & Academic Operational Policies
cfg["staff_policies"] = cfg.get("staff_policies") or {
    "defaultTeacherWorkingDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "maxDailyTeachingPeriods": 6,
    "maxWeeklyTeachingPeriods": 24,
    "minWeeklyPreparationPeriods": 6,
    "attendanceCutoffMorning": "07:15",
    "attendanceCutoffAfternoon": "13:15",
    "lateArrivalGracePeriodMinutes": 10,
    "excusedAbsenceCategories": ["Medical Certificate", "Official School Duty", "Family Bereavement", "Approved MoEYS Representation"],
    "gradeSubmissionDeadlineDaysAfterExam": 5,
    "principalApprovalRequiredForGradeChange": True,
    "timetablePublishAuthority": "Super Admin & Campus Principal"
}

# 9. Permissions & Access Control Matrix (Admin, Principal, Editor)
cfg["permissions_matrix"] = cfg.get("permissions_matrix") or {
    "roles": {
        "admin": {
            "title": "Super Administrator",
            "scope": "All Campuses",
            "sections": {
                "school_overview": {"view": True, "edit": True},
                "school_profile": {"view": True, "edit": True},
                "academic_years": {"view": True, "edit": True, "activate": True},
                "campuses": {"view": True, "edit": True},
                "school_days": {"view": True, "edit": True},
                "bell_schedule": {"view": True, "edit": True},
                "academic_calendar": {"view": True, "edit": True},
                "departments": {"view": True, "edit": True},
                "timetable_rules": {"view": True, "edit": True},
                "staff_policies": {"view": True, "edit": True},
                "permissions_access": {"view": True, "edit": True},
                "change_history": {"view": True, "rollback": True}
            }
        },
        "principal": {
            "title": "Executive Principal / Campus Principal",
            "scope": "Assigned Campuses",
            "sections": {
                "school_overview": {"view": True, "edit": False},
                "school_profile": {"view": True, "edit": True},
                "academic_years": {"view": True, "edit": True, "activate": True},
                "campuses": {"view": True, "edit": True},
                "school_days": {"view": True, "edit": True},
                "bell_schedule": {"view": True, "edit": True},
                "academic_calendar": {"view": True, "edit": True},
                "departments": {"view": True, "edit": True},
                "timetable_rules": {"view": True, "edit": True},
                "staff_policies": {"view": True, "edit": True},
                "permissions_access": {"view": True, "edit": False},
                "change_history": {"view": True, "rollback": False}
            }
        },
        "editor": {
            "title": "Academic Configuration Editor",
            "scope": "Assigned Campus (TK-MAIN)",
            "sections": {
                "school_overview": {"view": True, "edit": False},
                "school_profile": {"view": True, "edit": True},
                "academic_years": {"view": True, "edit": False, "activate": False},
                "campuses": {"view": True, "edit": False},
                "school_days": {"view": True, "edit": True},
                "bell_schedule": {"view": True, "edit": True},
                "academic_calendar": {"view": True, "edit": True},
                "departments": {"view": True, "edit": False},
                "timetable_rules": {"view": True, "edit": False},
                "staff_policies": {"view": True, "edit": False},
                "permissions_access": {"view": False, "edit": False},
                "change_history": {"view": True, "rollback": False}
            }
        }
    },
    "assignedEditors": [
        {
            "id": "USR-006",
            "name": "Ms. Keo Sreymom",
            "email": "sreymom.keo@ngis.edu.kh",
            "role": "Academic Configuration Editor",
            "assignedCampus": "TK-MAIN",
            "permittedSections": ["school_profile", "school_days", "bell_schedule", "academic_calendar"],
            "status": "active",
            "lastActive": "2026-07-08 09:12"
        }
    ]
}

# 10. Audit Log & Change History
cfg["audit_log"] = cfg.get("audit_log") or [
    {
        "id": "AUD-001",
        "timestamp": "2026-07-08 14:10:00",
        "userId": "USR-001",
        "userName": "Mr. Heng Samnang",
        "userRole": "admin",
        "section": "Academic Years",
        "action": "activate_year",
        "previousValue": "2025–2026",
        "newValue": "2026–2027",
        "scope": "School-wide",
        "status": "applied",
        "notes": "Activated AY 2026–2027 as authoritative active school year"
    },
    {
        "id": "AUD-002",
        "timestamp": "2026-07-08 14:15:30",
        "userId": "USR-001",
        "userName": "Mr. Heng Samnang",
        "userRole": "admin",
        "section": "Operating Schedule",
        "action": "update_schedule",
        "previousValue": "Saturday Disabled",
        "newValue": "Saturday Morning Enabled (07:00-11:30)",
        "scope": "TK-MAIN",
        "status": "applied",
        "notes": "Enabled Saturday morning sessions for secondary elective labs"
    },
    {
        "id": "AUD-003",
        "timestamp": "2026-07-08 14:20:00",
        "userId": "USR-002",
        "userName": "Dr. Ly Bunheng",
        "userRole": "principal",
        "section": "Timetable Rules",
        "action": "update_rules",
        "previousValue": "Max consecutive hours = 3",
        "newValue": "Max consecutive hours = 2",
        "scope": "All Secondary Cohorts",
        "status": "applied",
        "notes": "Enforced strict MoEYS rule: maximum 2 consecutive hours per subject"
    }
]

# 11. Pending Critical Change Reviews
cfg["pending_reviews"] = cfg.get("pending_reviews") or []

with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2)

print("Successfully upgraded data/system_configuration.json with complete school configuration schema!")

