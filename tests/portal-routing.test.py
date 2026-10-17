#!/usr/bin/env python3
"""Static regression checks for NGIS portal routing and retired messaging cleanup."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

for layout_path in (ROOT / "layout.js", ROOT / "assets/js/layout.js"):
    layout = layout_path.read_text(encoding="utf-8")
    assert "function resolvePortalRole" in layout, layout_path
    assert "ngis_user" in layout, layout_path
    assert "pathRole" in layout, layout_path
    assert "window.location.replace" not in layout, layout_path
    assert not re.search(r'id:"messaging", label:"Messaging", icon:"forum", collapsible:true', layout), layout_path
    for retired in ("messaging-dashboard", "saved", "attachments", "notification-preferences", "message-search"):
        assert f'id:"{retired}"' not in layout, (layout_path, retired)
    for retired_route in (
        "pages/messaging/messaging-dashboard.html",
        "pages/messaging/search.html",
    ):
        assert retired_route not in layout, (layout_path, retired_route)
    assert 'href:"pages/teacher/teacher-departments.html"' in layout, f"Missing teacher departments route in {layout_path}"
    assert 'href:"pages/teacher/teacher-lessons.html"' in layout, f"Missing teacher lessons route in {layout_path}"

# Verify no non-student sidebar links to pages/student/
for layout_path in (ROOT / "layout.js", ROOT / "assets/js/layout.js"):
    layout = layout_path.read_text(encoding="utf-8")
    nav_match = re.search(r'const NAV = \{(.*?)\n  \};', layout, re.DOTALL)
    assert nav_match, f"Could not find const NAV in {layout_path}"
    nav_block = nav_match.group(1)
    for non_student in ("teacher", "admin", "parent", "principal", "staff"):
        start = nav_block.find(f"    {non_student}:")
        assert start != -1, f"Could not find NAV.{non_student} in {layout_path}"
        next_indices = [
            nav_block.find(f"    {other}:", start + 1)
            for other in ("admin", "teacher", "student", "parent", "principal", "staff")
            if nav_block.find(f"    {other}:", start + 1) != -1
        ]
        end = min(next_indices) if next_indices else len(nav_block)
        role_block = nav_block[start:end]
        assert "pages/student/" not in role_block, f"Found leak of pages/student/ in NAV.{non_student} ({layout_path})"
        assert "student-lost-found.html" not in role_block, f"Found leak of student-lost-found.html in NAV.{non_student} ({layout_path})"

for retired_file in (
    "pages/messaging/messaging-dashboard.html",
    "pages/messaging/saved.html",
    "pages/messaging/attachments.html",
    "pages/messaging/notification-preferences.html",
    "pages/messaging/search.html",
):
    assert not (ROOT / retired_file).exists(), retired_file

messaging_data = (ROOT / "assets/js/messaging-data.js").read_text(encoding="utf-8")
for retired_symbol in (
    "SAVED", "ATTACHMENTS", "NOTIF_CATEGORIES", "SEARCH_INDEX",
    "saved:", "attachments:", "notifCategories:", "searchIndex:",
):
    assert retired_symbol not in messaging_data, retired_symbol

# Verify teacher-departments.html file exists and has proper attributes
teacher_dept_file = ROOT / "pages/teacher/teacher-departments.html"
assert teacher_dept_file.exists(), "pages/teacher/teacher-departments.html must exist"
teacher_dept_html = teacher_dept_file.read_text(encoding="utf-8")
assert 'data-role="teacher"' in teacher_dept_html, "Missing data-role='teacher' in teacher-departments.html"
assert 'data-page="departments"' in teacher_dept_html, "Missing data-page='departments' in teacher-departments.html"

# Verify teacher-lessons.html file exists and has proper attributes
teacher_lessons_file = ROOT / "pages/teacher/teacher-lessons.html"
assert teacher_lessons_file.exists(), "pages/teacher/teacher-lessons.html must exist"
teacher_lessons_html = teacher_lessons_file.read_text(encoding="utf-8")
assert 'data-role="teacher"' in teacher_lessons_html, "Missing data-role='teacher' in teacher-lessons.html"
assert 'data-page="lessons"' in teacher_lessons_html, "Missing data-page='lessons' in teacher-lessons.html"

# Verify cross-portal protections on shared department pages
shared_depts = (ROOT / "pages/shared/departments.html").read_text(encoding="utf-8")
assert "teacher-departments.html" in shared_depts, "shared departments.html must route teachers to teacher-departments.html"

shared_dept = (ROOT / "pages/shared/department.html").read_text(encoding="utf-8")
assert "teacher-departments.html" in shared_dept, "shared department.html must route teachers to teacher-departments.html"

# Verify all main portal dashboards implement the dual-view architecture and Digital ID modal
dashboards = {
    "student": ROOT / "pages/student/student.html",
    "teacher": ROOT / "pages/teacher/teacher.html",
    "admin": ROOT / "pages/admin/admin.html",
    "parent": ROOT / "pages/parent/parent.html",
    "principal": ROOT / "pages/principal/principal.html",
    "staff": ROOT / "pages/staff/staff.html",
}

for role, path in dashboards.items():
    assert path.exists(), f"Dashboard missing for {role}: {path}"
    content = path.read_text(encoding="utf-8")
    assert f"{role}-desktop-view" in content, f"Missing {role}-desktop-view in {path}"
    assert f"{role}-mobile-view" in content, f"Missing {role}-mobile-view in {path}"
    assert "idModal" in content, f"Missing idModal Digital ID modal in {path}"
    assert "dash-overlap" in content, f"Missing dash-overlap layout grid in {path}"
    assert "ov-profile" in content, f"Missing ov-profile in {path}"
    assert "ov-upcoming" in content, f"Missing ov-upcoming in {path}"
    assert "ov-deadlines" in content, f"Missing ov-deadlines in {path}"

# Verify floating mobile bottom nav dock support in layout.js
for layout_path in (ROOT / "layout.js", ROOT / "assets/js/layout.js"):
    layout = layout_path.read_text(encoding="utf-8")
    assert "MOB_NAV_TABS" in layout, f"Missing MOB_NAV_TABS in {layout_path}"
    assert "mob-bottomnav" in layout, f"Missing mob-bottomnav class in {layout_path}"
    assert "mob-bn-slider" in layout, f"Missing mob-bn-slider in {layout_path}"
    for role in ("student", "teacher", "admin", "parent", "principal", "staff"):
        assert f"{role}:" in layout, f"Missing role {role} tabs in MOB_NAV_TABS in {layout_path}"

print("portal-routing.test.py: PASS")


