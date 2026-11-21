# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json

candidates = [
    # 1. Calendar
    "calendar", "tear-off-calendar", "calendar-plus", "month-view",
    # 2. Weekly Timetable / Schedule
    "schedule", "timetable", "planner", "time", "clock",
    # 3. My Classes / Class
    "classroom", "class", "training", "conference-call", "school",
    # 4. Assignments / Task list
    "assignment", "task", "tasks", "clipboard", "todo-list", "test-passed",
    # 5. Lessons / E-Learning
    "lesson", "online-lesson", "open-book", "reading", "study",
    # 6. Examinations / Test
    "exam", "quiz", "test", "diploma", "graduation-cap",
    # 7. Grades / Academic score
    "grade", "grading", "score", "star", "medal", "trophy", "a-plus",
    # 8. Attendance / Register
    "attendance", "checked-user", "user-check", "presence", "fingerprint",
    # 9. Announcements / Megaphone / News
    "announcement", "megaphone", "commercial", "speaker", "bell",
    # 10. Student Profile / Student ID
    "student-male", "student-female", "student", "user-male-circle", "id-card",
    # 11. Academic Reports / Analytics
    "report-card", "analytics", "bar-chart", "business-report", "presentation",
    # 12. Documents / Files
    "document", "documents", "folder-invoices", "pdf", "file",
    # 13. Portfolio / Briefcase
    "portfolio", "briefcase", "bag", "backpack", "backpack-travel",
    # 14. Books / Library
    "books", "library", "stack-of-books", "literature", "book-stack",
    # 15. Upcoming Deadlines / Sand clock / Alarm
    "alarm-clock", "hourglass", "sand-timer", "deadline", "urgent",
    # 16. School Events / Celebration
    "confetti", "party-popper", "event-accepted", "stage", "circus",
    # 17. Teachers / Faculty
    "teacher", "lecturer", "professor", "tutor",
    # 18. Curriculum / Syllabus / Compass
    "compass", "education", "courses", "blueprint", "gears",
    # 19. Completed Tasks / Success
    "checkmark", "ok", "double-tick", "approval", "task-completed",
    # 20. Empty Calendar / Nothing / In box / Relax
    "empty-box", "nothing-found", "inbox", "sleeping", "relax", "sparkling"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

found = {}
not_found = []

for slug in candidates:
    url = f"https://img.icons8.com/3d-fluency/94/{slug}.png"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                length = len(response.read())
                if length > 500: # not a 1x1 placeholder
                    found[slug] = {"url": url, "size": length}
                    print(f"[FOUND] {slug} ({length} bytes)")
    except urllib.error.HTTPError as e:
        not_found.append(slug)
    except Exception as e:
        print(f"Error checking {slug}: {e}")

print(f"\nTotal Found: {len(found)}")
print(f"Total Not Found: {len(not_found)}")

with open("scratch/icons8_candidates.json", "w", encoding="utf-8") as f:
    json.dump(found, f, indent=2)
