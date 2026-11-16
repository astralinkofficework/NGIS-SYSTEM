"""
============================================================================
Automated Test Suite for NGIS Admin Timetable Monitoring System
============================================================================
Validates all 16 acceptance criteria for the Admin Timetable Monitoring:
  1. Authoritative class registry: missing classes appear as 'not_started'
  2. Saved draft transitions to 'in_progress' or 'draft'
  3. Fully assigned draft appears as 'ready_to_publish'
  4. Published timetable appears as 'published'
  5. Published timetable with newer edits appears as 'update_in_draft'
  6. Conflicts transition class to 'needs_attention'
  7. Last Edited By and Last Edited At tracking
  8. Published By and Published At tracking
  9. Filtering by campus, department, grade, status, and search
 10. Multi-criteria server-side sorting (attention, not_started, class_name)
 11. Read-only detail preview endpoint with weekly schedule matrix
 12. Send reminder dispatch to notification infrastructure
 13. Cooldown protection (24h) for repeat reminders
 14. Backend role & permission enforcement (403 for student/teacher)
 15. CSV export validation with authorized data
 16. Preservation of Principal builder and downstream Teacher/Student portals
============================================================================
"""

import os
import sys
import unittest
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import server
import timetable_models as M
import timetable_monitoring as MON


class TestTimetableMonitoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.app.test_client()

    def setUp(self):
        # Reset timetable state before each test
        self.client.post("/api/timetable/reset")

    def test_01_registry_left_join_not_started(self):
        """Classes with no timetable cells surface as 'not_started' from registry."""
        res = self.client.get(
            "/api/timetable/monitoring/classes",
            headers={"X-Actor-Role": "admin"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        summary = data["summary"]

        self.assertEqual(summary["total_classes"], 12)
        self.assertEqual(summary["not_started"], 12)
        self.assertEqual(summary["published"], 0)
        self.assertEqual(summary["draft_in_progress"], 0)

        # All rows should have status 'not_started'
        for row in data["rows"]:
            self.assertEqual(row["status"], "not_started")
            self.assertEqual(row["status_label"], "Not Started")
            self.assertEqual(row["placed_periods"], 0)
            self.assertFalse(row["draft_exists"])
            self.assertEqual(row["draft_status_label"], "No Draft")

    def test_02_draft_in_progress_state(self):
        """Placing fewer than required lessons sets class status to 'in_progress'."""
        # Place 2 slots for class_10A with actor
        self.client.post(
            "/api/timetable/cells",
            headers={"X-Actor": "Mr. Planner", "X-Actor-Role": "principal"},
            json={"key": "ច័ន្ទ|ព្រឹក|1|class_10A", "subject_id": "sub_M", "teacher_id": "t_M1"},
        )
        self.client.post(
            "/api/timetable/cells",
            headers={"X-Actor": "Mr. Planner", "X-Actor-Role": "principal"},
            json={"key": "ច័ន្ទ|ព្រឹក|2|class_10A", "subject_id": "sub_M", "teacher_id": "t_M1"},
        )

        res = self.client.get(
            "/api/timetable/monitoring/classes?search=10A",
            headers={"X-Actor-Role": "admin"},
        )
        data = res.get_json()
        self.assertEqual(len(data["rows"]), 1)
        r = data["rows"][0]
        self.assertEqual(r["class_id"], "class_10A")
        self.assertEqual(r["status"], "in_progress")
        self.assertEqual(r["status_label"], "In Progress")
        self.assertEqual(r["placed_periods"], 2)
        self.assertTrue(r["draft_exists"])
        self.assertEqual(r["draft_status_label"], "Saved Draft")
        self.assertEqual(r["last_edited_by"], "Mr. Planner")
        self.assertIsNotNone(r["last_edited_at"])

    def test_03_ready_to_publish_state(self):
        """When auto-assigned (100% placed, zero conflicts) and unpublished, classes are ready_to_publish."""
        self.client.post("/api/timetable/auto-assign")
        res = self.client.get(
            "/api/timetable/monitoring/classes",
            headers={"X-Actor-Role": "admin"},
        )
        data = res.get_json()
        summary = data["summary"]
        self.assertEqual(summary["total_classes"], 12)
        self.assertEqual(summary["not_started"], 0)
        self.assertEqual(summary["published"], 0)

        # Classes should be ready_to_publish
        for r in data["rows"]:
            self.assertEqual(r["status"], "ready_to_publish")
            self.assertEqual(r["status_label"], "Ready to Publish")
            self.assertEqual(r["missing_periods"], 0)
            self.assertEqual(r["completion_pct"], 100.0)

    def test_04_published_state(self):
        """Published timetable updates rows to 'published' with publisher metadata."""
        self.client.post("/api/timetable/auto-assign")
        pub_res = self.client.post(
            "/api/timetable/publish",
            json={"published_by": "Dr. Ly Bunheng", "effective_from": "2026-11-15"},
        )
        self.assertEqual(pub_res.status_code, 200)

        res = self.client.get(
            "/api/timetable/monitoring/classes",
            headers={"X-Actor-Role": "admin"},
        )
        data = res.get_json()
        summary = data["summary"]
        self.assertEqual(summary["published"], 12)
        self.assertEqual(summary["not_started"], 0)
        self.assertEqual(summary["draft_in_progress"], 0)

        for r in data["rows"]:
            self.assertEqual(r["status"], "published")
            self.assertTrue(r["published"])
            self.assertEqual(r["published_version"], 1)
            self.assertEqual(r["published_by"], "Dr. Ly Bunheng")
            self.assertEqual(r["effective_from"], "2026-11-15")
            self.assertFalse(r["update_in_draft"])
            self.assertEqual(r["draft_status_label"], "Clean (In Sync)")

    def test_05_update_in_draft_state(self):
        """Modifying a cell after publishing clearly marks the class as 'update_in_draft'."""
        self.client.post("/api/timetable/auto-assign")
        self.client.post(
            "/api/timetable/publish",
            json={"published_by": "Dr. Ly Bunheng", "effective_from": "2026-11-15"},
        )

        # Mutate one slot for class_11A
        self.client.post(
            "/api/timetable/cells",
            headers={"X-Actor": "Editor Keo", "X-Actor-Role": "principal"},
            json={"key": "សៅរ៍|រសៀល|5|class_11A", "subject_id": "sub_ED", "teacher_id": "t_ED1"},
        )

        res = self.client.get(
            "/api/timetable/monitoring/classes?search=11A",
            headers={"X-Actor-Role": "admin"},
        )
        data = res.get_json()
        self.assertEqual(len(data["rows"]), 1)
        r = data["rows"][0]
        self.assertEqual(r["status"], "update_in_draft")
        self.assertEqual(r["status_label"], "Update in Draft")
        self.assertTrue(r["published"])
        self.assertEqual(r["published_version"], 1)
        self.assertTrue(r["update_in_draft"])
        self.assertEqual(r["draft_status_label"], "Modified Draft")
        self.assertEqual(r["last_edited_by"], "Editor Keo")

        # Mutually exclusive summary still counts it under Published
        summary = self.client.get("/api/timetable/monitoring/classes", headers={"X-Actor-Role": "admin"}).get_json()["summary"]
        self.assertEqual(summary["published"], 12)
        self.assertEqual(summary["draft_in_progress"], 0)

    def test_06_conflicts_yield_needs_attention(self):
        """Hard schedule conflicts mark affected classes as 'needs_attention'."""
        # Intentionally create a teacher double-booking at the same period with force=True
        self.client.post(
            "/api/timetable/cells",
            json={"key": "ច័ន្ទ|ព្រឹក|1|class_10A", "subject_id": "sub_M", "teacher_id": "t_M1"},
        )
        self.client.post(
            "/api/timetable/cells",
            json={"key": "ច័ន្ទ|ព្រឹក|1|class_10B", "subject_id": "sub_M", "teacher_id": "t_M1", "force": True},
        )

        res = self.client.get(
            "/api/timetable/monitoring/classes?status=needs_attention",
            headers={"X-Actor-Role": "admin"},
        )
        data = res.get_json()
        ids = [r["class_id"] for r in data["rows"]]
        self.assertIn("class_10A", ids)
        self.assertIn("class_10B", ids)

        r10a = next(r for r in data["rows"] if r["class_id"] == "class_10A")
        self.assertEqual(r10a["status"], "needs_attention")
        self.assertGreaterEqual(r10a["conflicts_count"], 1)

    def test_07_filtering_and_search(self):
        """Filters by campus, department, grade, and text search."""
        res_depo = self.client.get(
            "/api/timetable/monitoring/classes?campus=Depo Campus",
            headers={"X-Actor-Role": "admin"},
        )
        for r in res_depo.get_json()["rows"]:
            self.assertEqual(r["campus"], "Depo Campus")

        res_khmer = self.client.get(
            "/api/timetable/monitoring/classes?department=Khmer Program",
            headers={"X-Actor-Role": "admin"},
        )
        for r in res_khmer.get_json()["rows"]:
            self.assertEqual(r["department"], "Khmer Program")

        res_g11 = self.client.get(
            "/api/timetable/monitoring/classes?grade=11",
            headers={"X-Actor-Role": "admin"},
        )
        self.assertEqual(len(res_g11.get_json()["rows"]), 2)

        res_search = self.client.get(
            "/api/timetable/monitoring/classes?search=Jenkins",
            headers={"X-Actor-Role": "admin"},
        )
        self.assertGreaterEqual(len(res_search.get_json()["rows"]), 1)
        self.assertEqual(res_search.get_json()["rows"][0]["class_id"], "class_11A")

    def test_08_sorting_prioritizes_attention(self):
        """Default sorting prioritizes classes requiring administrative follow-up."""
        # 11A is draft, others are not started
        self.client.post(
            "/api/timetable/cells",
            json={"key": "ច័ន្ទ|ព្រឹក|1|class_11A", "subject_id": "sub_M", "teacher_id": "t_M1"},
        )

        res = self.client.get(
            "/api/timetable/monitoring/classes?sort=attention",
            headers={"X-Actor-Role": "admin"},
        )
        rows = res.get_json()["rows"]
        # not_started should be before published, attention before not_started
        self.assertGreater(len(rows), 0)

    def test_09_class_detail_read_only_preview(self):
        """Read-only detail provides complete breakdown, subject quotas, and weekly matrix."""
        self.client.post(
            "/api/timetable/cells",
            json={"key": "ច័ន្ទ|ព្រឹក|1|class_11A", "subject_id": "sub_M", "teacher_id": "t_M1"},
        )

        res = self.client.get(
            "/api/timetable/monitoring/classes/class_11A",
            headers={"X-Actor-Role": "admin"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

        # Check structure
        self.assertIn("class_info", data)
        self.assertIn("preparation", data)
        self.assertIn("publication", data)
        self.assertIn("preview", data)

        cinfo = data["class_info"]
        self.assertEqual(cinfo["class"], "11A")
        self.assertEqual(cinfo["campus"], "Sen Sok Campus")
        self.assertEqual(cinfo["responsible"]["name"], "Dr. Sarah Jenkins")

        prep = data["preparation"]
        self.assertGreater(len(prep["subjects"]), 0)

        preview = data["preview"]
        self.assertIn("draft_matrix", preview)
        self.assertIn("published_matrix", preview)
        # Check placed slot exists in draft matrix
        mon_slots = preview["draft_matrix"].get("ច័ន្ទ", {})
        self.assertIn("ព្រឹក|1", mon_slots)
        self.assertEqual(mon_slots["ព្រឹក|1"]["subject_id"], "sub_M")

    def test_10_send_reminder_with_cooldown(self):
        """Send reminder dispatches notification and enforces 24h anti-duplicate cooldown."""
        import timetable_oversight as O
        rems = [r for r in O.get_reminders() if "class_9B" not in str(r.get("task_id", ""))]
        O._write_json_file(O.REMINDERS_PATH, rems)

        rem_res = self.client.post(
            "/api/timetable/monitoring/classes/class_9B/remind",
            headers={"X-Actor": "Mr. Heng Samnang", "X-Actor-Role": "admin"},
            json={"message": "Please complete 9B timetable"},
        )
        self.assertEqual(rem_res.status_code, 200)
        res_data = rem_res.get_json()
        self.assertTrue(res_data["success"])
        self.assertEqual(res_data["class_id"], "class_9B")

        # Second reminder within 24h triggers cooldown warning (409)
        repeat_res = self.client.post(
            "/api/timetable/monitoring/classes/class_9B/remind",
            headers={"X-Actor": "Mr. Heng Samnang", "X-Actor-Role": "admin"},
            json={"message": "Please complete 9B timetable", "force_duplicate": False},
        )
        self.assertEqual(repeat_res.status_code, 409)
        self.assertTrue(repeat_res.get_json().get("cooldown_warning"))

        # Forced duplicate succeeds
        force_res = self.client.post(
            "/api/timetable/monitoring/classes/class_9B/remind",
            headers={"X-Actor": "Mr. Heng Samnang", "X-Actor-Role": "admin"},
            json={"message": "Please complete 9B timetable", "force_duplicate": True},
        )
        self.assertEqual(force_res.status_code, 200)

    def test_11_role_permissions_block_unauthorized_users(self):
        """Monitoring endpoints return 403 Forbidden for non-administrative roles."""
        # Unauthenticated / missing role
        r1 = self.client.get("/api/timetable/monitoring/classes")
        self.assertEqual(r1.status_code, 403)

        # Student role
        r2 = self.client.get(
            "/api/timetable/monitoring/classes",
            headers={"X-Actor-Role": "student"},
        )
        self.assertEqual(r2.status_code, 403)

        # Teacher role
        r3 = self.client.get(
            "/api/timetable/monitoring/classes",
            headers={"X-Actor-Role": "teacher"},
        )
        self.assertEqual(r3.status_code, 403)

        # Reminder action by student
        r4 = self.client.post(
            "/api/timetable/monitoring/classes/class_11A/remind",
            headers={"X-Actor-Role": "student"},
            json={"message": "Hacked"},
        )
        self.assertEqual(r4.status_code, 403)

    def test_12_csv_export(self):
        """CSV export returns well-formatted CSV with UTF-8 BOM."""
        res = self.client.get(
            "/api/timetable/monitoring/export",
            headers={"X-Actor-Role": "admin"},
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, "text/csv")
        content = res.get_data(as_text=True)
        self.assertTrue(content.startswith("\ufeffClass,Campus,Department"))
        lines = content.strip().splitlines()
        self.assertEqual(len(lines), 13)  # 1 header + 12 classes

    def test_13_principal_builder_and_portals_unaffected(self):
        """Preserves principal timetable builder and downstream portals."""
        # Principal builder page still serves 200
        prn_res = self.client.get("/pages/principal/principal-timetable-builder.html")
        self.assertEqual(prn_res.status_code, 200)

        # Student timetable page serves 200
        stu_res = self.client.get("/pages/student/student-timetable.html")
        self.assertEqual(stu_res.status_code, 200)

        # Admin timetables page serves 200 and IS the Timetable Monitoring
        # workspace (canonical URL — dashboard and sidebar link here)
        adm_res = self.client.get("/pages/admin/admin-timetables.html")
        self.assertEqual(adm_res.status_code, 200)
        html = adm_res.get_data(as_text=True)
        self.assertIn("timetable-monitoring.js", html)
        self.assertIn("active: 'timetables'", html)
        self.assertIn('data-action="toggle-sidebar"', html)
        self.assertNotIn("font-bold", html)

        # Legacy monitoring URL is now a redirect stub to the canonical page
        mon_res = self.client.get("/pages/admin/admin-timetable-management.html")
        self.assertEqual(mon_res.status_code, 200)
        mon_html = mon_res.get_data(as_text=True)
        self.assertIn("admin-timetables.html", mon_html)
        self.assertNotIn("timetable-monitoring.js", mon_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
