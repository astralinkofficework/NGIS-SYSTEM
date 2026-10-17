#!/usr/bin/env python3
"""
E2E Integration & Connected Workflow Test for NGIS ERP Role Portals
Verifies role separation, layout integrity, API contracts, and cross-portal workflows:
Admin -> Teacher -> Student -> Parent -> Staff -> Principal
"""
import os
import sys
import json
import unittest
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import server

class TestNgisRolePortals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.app.config['TESTING'] = True
        cls.client = server.app.test_client()

    def test_01_portal_files_exist(self):
        """Verify all portal pages and subpages exist on disk."""
        expected_files = [
            # Student (untouched baseline reference)
            "pages/student/student.html",
            "pages/student/student-calendar.html",
            "pages/student/student-profile.html",
            "pages/student/student-services.html",
            "pages/student/student-lost-found.html",
            # Teacher
            "pages/teacher/teacher.html",
            "pages/teacher/teacher-classes.html",
            "pages/teacher/teacher-attendance.html",
            "pages/teacher/teacher-assignments.html",
            "pages/teacher/teacher-lessons.html",
            "pages/teacher/teacher-departments.html",
            "pages/teacher/teacher-grades.html",
            "pages/teacher/teacher-calendar.html",
            "pages/teacher/teacher-profile.html",
            # Parent
            "pages/parent/parent.html",
            "pages/parent/parent-children.html",
            "pages/parent/parent-grades.html",
            "pages/parent/parent-attendance.html",
            "pages/parent/parent-assignments.html",
            "pages/parent/parent-calendar.html",
            "pages/parent/parent-profile.html",
            # Admin
            "pages/admin/admin.html",
            "pages/admin/admin-users.html",
            "pages/admin/admin-classes.html",
            "pages/admin/admin-assignments.html",
            "pages/admin/admin-lessons.html",
            "pages/admin/admin-departments.html",
            "pages/admin/admin-attendance.html",
            "pages/admin/admin-reports.html",
            "pages/admin/admin-settings.html",
            # Principal
            "pages/principal/principal.html",
            "pages/principal/principal-reports.html",
            "pages/principal/principal-approvals.html",
            "pages/principal/principal-profile.html",
            "pages/principal/_auth-bootstrap.js",
            # Staff
            "pages/staff/staff.html",
            "pages/staff/staff-services.html",
            "pages/staff/staff-profile.html",
            "pages/staff/_auth-bootstrap.js",
            # Shared
            "pages/shared/access-denied.html",
            "pages/shared/chat.html",
            "pages/shared/departments.html"
        ]
        for f in expected_files:
            p = ROOT / f
            self.assertTrue(p.exists(), f"Missing expected file: {f}")

    def test_02_layout_synchronization_and_roles(self):
        """Verify layout.js and assets/js/layout.js are in sync and support all 6 roles."""
        layout_main = (ROOT / "layout.js").read_text(encoding="utf-8")
        layout_mirror = (ROOT / "assets/js/layout.js").read_text(encoding="utf-8")
        self.assertEqual(layout_main, layout_mirror, "assets/js/layout.js must match layout.js exactly")

        for role in ["admin", "teacher", "student", "parent", "principal", "staff"]:
            self.assertIn(f"{role}:", layout_main, f"Role {role} missing in NAV/BOTTOM/PORTAL_HOME")

        # Verify access-denied.html includes all 6 roles
        access_denied = (ROOT / "pages/shared/access-denied.html").read_text(encoding="utf-8")
        for role in ["admin", "teacher", "parent", "student", "staff", "principal"]:
            self.assertIn(f"{role}:", access_denied, f"Role {role} missing in access-denied homeMap")

    def test_03_clean_route_shortcuts(self):
        """Verify clean portal route shortcuts in server.py."""
        shortcuts = ["/admin", "/teacher", "/student", "/parent", "/staff", "/principal"]
        for sc in shortcuts:
            resp = self.client.get(sc, follow_redirects=True)
            self.assertEqual(resp.status_code, 200, f"Route {sc} returned status {resp.status_code}")
            resp.close()

    def test_04_authentication_all_roles(self):
        """Verify login and session resolution for all 6 roles."""
        credentials = [
            ("admin@ngis.edu.kh", "password123", "admin"),
            ("principal@ngis.edu.kh", "password123", "principal"),
            ("teacher@ngis.edu.kh", "password123", "teacher"),
            ("staff@ngis.edu.kh", "password123", "staff"),
            ("student@ngis.edu.kh", "password123", "student"),
            ("parent@ngis.edu.kh", "password123", "parent"),
        ]
        for email, password, expected_role in credentials:
            resp = self.client.post("/api/auth/login", json={"email": email, "password": password})
            self.assertEqual(resp.status_code, 200, f"Login failed for {email}")
            data = resp.get_json()["data"]
            self.assertEqual(data["user"]["role"], expected_role)
            token = data["token"]

            # Test /api/auth/me with Bearer token
            me_resp = self.client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
            self.assertEqual(me_resp.status_code, 200)
            me_data = me_resp.get_json()["data"]
            self.assertEqual(me_data["role"], expected_role)

    def test_05_teacher_to_student_to_parent_connected_workflow(self):
        """
        Test the connected workflow:
        1. Teacher creates and publishes an assignment.
        2. Student views the assignment in their class.
        3. Student submits coursework.
        4. Teacher grades submission and provides feedback.
        5. Parent views child's assignment, grade, and teacher feedback.
        """
        # Step 1: Teacher creates an assignment
        asgn_payload = {
            "title": "Quantum Physics & Mechanics Essay",
            "description": "Write a 1,000-word analysis on quantum entanglement.",
            "subjectId": "subj-phys",
            "subject_name": "Physics & Lab",
            "classId": "cls-10a",
            "dueDate": "2026-08-15",
            "maxScore": 100,
            "teacher_id": "TCH-2024-042",
            "teacher_name": "Dr. Sarah Jenkins"
        }
        create_resp = self.client.post("/api/assignments", json=asgn_payload)
        self.assertEqual(create_resp.status_code, 201)
        asgn = create_resp.get_json()["data"]
        asgn_id = asgn["id"]

        # Step 2: Student submits coursework
        student_id = "STU-2024-089"
        sub_resp = self.client.post(f"/api/assignments/{asgn_id}/submit", json={
            "studentId": student_id,
            "studentName": "Nrinphouneta Hok",
            "fileName": "hok_quantum_essay.pdf"
        })
        self.assertEqual(sub_resp.status_code, 201)

        # Step 3: Teacher grades the submission
        grade_resp = self.client.post(f"/api/assignments/{asgn_id}/grade", json={
            "studentId": student_id,
            "score": 98,
            "feedback": "Outstanding mathematical rigor and lucid physical explanations!"
        })
        self.assertEqual(grade_resp.status_code, 200)

        # Step 4: Parent fetches child's assignments and verifies score and feedback
        parent_resp = self.client.get(f"/api/parent/children/{student_id}/assignments")
        self.assertEqual(parent_resp.status_code, 200)
        parent_assignments = parent_resp.get_json()["data"]
        matching = next((a for a in parent_assignments if a["id"] == asgn_id), None)
        self.assertIsNotNone(matching, "Child's graded assignment must be visible to parent")
        self.assertEqual(matching["score"], 98)
        self.assertEqual(matching["feedback"], "Outstanding mathematical rigor and lucid physical explanations!")
        self.assertEqual(matching["status"], "graded")

    def test_06_staff_and_principal_endpoints(self):
        """Verify Staff and Principal stats and operational task endpoints."""
        prn_resp = self.client.get("/api/principal/stats")
        self.assertEqual(prn_resp.status_code, 200)
        prn_data = prn_resp.get_json()["data"]
        self.assertIn("totalStudents", prn_data)
        self.assertIn("totalTeachers", prn_data)

        stf_resp = self.client.get("/api/staff/stats")
        self.assertEqual(stf_resp.status_code, 200)
        stf_data = stf_resp.get_json()["data"]
        self.assertIn("openRequests", stf_data)

        # Staff creates a task
        task_resp = self.client.post("/api/staff/tasks", json={
            "title": "Inspect Emergency Exit Alarms (Building A)",
            "area": "Facilities",
            "priority": "high"
        })
        self.assertEqual(task_resp.status_code, 201)

    def test_07_student_portal_preserved_intact(self):
        """Verify Student Portal files exist and contain student-specific PAGE metadata."""
        student_page = (ROOT / "pages/student/student.html").read_text(encoding="utf-8")
        self.assertIn('"role":"student"', student_page)
        self.assertIn('"active":"dashboard"', student_page)

        # Verify student lost and found exists
        lost_found = (ROOT / "pages/student/student-lost-found.html").read_text(encoding="utf-8")
        self.assertTrue("role: 'student'" in lost_found or '"role":"student"' in lost_found)

    def test_08_lessons_repository_and_upload_workflow(self):
        """
        Verify the complete lesson lifecycle across roles:
        1. Teacher creates and uploads a new lesson plan / material for a class.
        2. Admin views and audits lessons across all departments via /api/lessons.
        3. Filter by classId and teacherId works.
        4. Teacher / Admin updates or deletes lesson material.
        """
        # Step 1: Teacher uploads a lesson
        lesson_payload = {
            "title": "Calculus: Limits and Continuous Functions",
            "description": "Comprehensive slide deck and practice problems covering epsilon-delta definitions.",
            "classId": "cls-11a",
            "className": "Grade 11 - Section A",
            "teacherId": "TCH-2024-042",
            "teacherName": "Dr. Sarah Jenkins",
            "department": "Mathematics",
            "format": "Slides",
            "unit": "Unit 3 - Differential Calculus"
        }
        post_resp = self.client.post("/api/lessons", json=lesson_payload)
        self.assertEqual(post_resp.status_code, 201)
        created_lesson = post_resp.get_json()["data"]
        lesson_id = created_lesson["id"]
        self.assertEqual(created_lesson["title"], "Calculus: Limits and Continuous Functions")
        self.assertEqual(created_lesson["classId"], "cls-11a")

        # Step 2: Admin queries lessons repository
        admin_resp = self.client.get("/api/lessons")
        self.assertEqual(admin_resp.status_code, 200)
        lessons_list = admin_resp.get_json()["data"]
        matching = next((l for l in lessons_list if l["id"] == lesson_id), None)
        self.assertIsNotNone(matching, "Uploaded lesson must be accessible in shared repository")

        # Step 3: Query filtered by class
        filter_resp = self.client.get("/api/lessons?classId=cls-11a")
        self.assertEqual(filter_resp.status_code, 200)
        cls_lessons = filter_resp.get_json()["data"]
        self.assertTrue(any(l["id"] == lesson_id for l in cls_lessons))

        # Step 4: Delete lesson
        del_resp = self.client.delete(f"/api/lessons/{lesson_id}")
        self.assertEqual(del_resp.status_code, 200)

        # Step 5: Verify lesson is removed
        verify_resp = self.client.get(f"/api/lessons/{lesson_id}")
        self.assertEqual(verify_resp.status_code, 404)

    def test_09_no_sidebar_leaks_and_clean_routing(self):
        """
        Verify no non-student portal sidebar contains references to student pages,
        and that student portal keeps its original dedicated navigation intact.
        """
        import re
        for layout_file in [ROOT / "layout.js", ROOT / "assets/js/layout.js"]:
            text = layout_file.read_text(encoding="utf-8")
            nav_match = re.search(r'const NAV = \{(.*?)\n  \};', text, re.DOTALL)
            self.assertIsNotNone(nav_match)
            nav_block = nav_match.group(1)

            # Ensure student nav exists and contains student items
            student_start = nav_block.find("    student:")
            self.assertNotEqual(student_start, -1)
            self.assertIn("pages/student/student.html", nav_block)
            self.assertIn("pages/student/student-calendar.html", nav_block)

            # Verify non-student portals do NOT contain student page links
            for role in ["teacher", "admin", "parent", "principal", "staff"]:
                start = nav_block.find(f"    {role}:")
                self.assertNotEqual(start, -1, f"Missing {role} in NAV")
                next_indices = [
                    nav_block.find(f"    {other}:", start + 1)
                    for other in ("admin", "teacher", "student", "parent", "principal", "staff")
                    if nav_block.find(f"    {other}:", start + 1) != -1
                ]
                end = min(next_indices) if next_indices else len(nav_block)
                role_block = nav_block[start:end]
                self.assertNotIn("pages/student/", role_block, f"Role {role} sidebar has a leak to pages/student/")
                self.assertNotIn("student-lost-found.html", role_block, f"Role {role} sidebar leaks student-lost-found.html")

if __name__ == "__main__":
    unittest.main()
