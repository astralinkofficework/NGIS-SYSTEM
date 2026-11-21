"""Regression tests for the simplified examination scheduling workflow.

Run: python -m unittest tests.test_simplified_exams -v
Uses an isolated copy of the academic SQLite database; production demo data
is never modified.
"""
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from flask import Flask

ROOT = Path(__file__).resolve().parent.parent
import exam_management_api as exams_api  # noqa: E402


class SimplifiedExamsWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.mkdtemp(prefix="ngis-exams-test-")
        cls.db_path = Path(cls._tmp) / "academic.sqlite3"
        source = ROOT / ".data" / "academic.sqlite3"
        shutil.copyfile(source, cls.db_path)
        cls.original_db_path = exams_api.DB_PATH
        exams_api.DB_PATH = cls.db_path
        exams_api.init_exam_schema()

        cls.app = Flask(__name__)
        cls.app.testing = True
        cls.app.register_blueprint(exams_api.exam_bp)
        cls.client = cls.app.test_client()
        cls.teacher = {"X-Actor": "teacher@ngis.edu.kh"}
        cls.principal = {"X-Actor": "principal@ngis.edu.kh"}
        cls.admin = {"X-Actor": "uyuityu@ngis.edu.kh"}  # ordinary ADMIN, not SUPER_ADMIN
        cls.student = {"X-Actor": "student@ngis.edu.kh"}

    @classmethod
    def tearDownClass(cls):
        exams_api.DB_PATH = cls.original_db_path
        shutil.rmtree(cls._tmp, ignore_errors=True)

    def _payload(self, **overrides):
        payload = {
            "department_id": "dept-eng",
            "subject_id": "subj-eng",
            "class_ids": ["cls-10a"],
            "exam_type": "class_test",
            "exam_date": "2026-12-28",
            "start_time": "08:00",
            "end_time": "09:00",
        }
        payload.update(overrides)
        return payload

    def _create_submitted(self, **overrides):
        response = self.client.post(
            "/api/exams/simple", json=self._payload(submit_for_review=True, **overrides),
            headers=self.teacher,
        )
        self.assertEqual(response.status_code, 201, response.get_json())
        return response.get_json()["data"]["id"]

    def test_01_identity_resolution(self):
        data = self.client.get("/api/exams/options", headers=self.teacher).get_json()
        self.assertEqual(data["actor"]["role"], "teacher")
        self.assertEqual(data["actor"]["id"], "TCH-2024-042")
        self.assertTrue(any(t["id"] == "class_test" for t in data["exam_types"]))

    def test_02_teacher_options_are_scoped(self):
        data = self.client.get("/api/exams/options", headers=self.teacher).get_json()
        pairs = {(a["subject_id"], a["class_id"]) for a in data["assignments"]}
        self.assertIn(("subj-eng", "cls-10a"), pairs)
        self.assertNotIn(("subj-chem", "cls-khm-12a"), pairs)
        self.assertTrue(all(c["id"] in {p[1] for p in pairs} for c in data["classes"]))

    def test_03_unassigned_subject_or_class_is_rejected(self):
        response = self.client.post(
            "/api/exams/simple",
            json=self._payload(subject_id="subj-ap-bio", class_ids=["cls-10a"]),
            headers=self.teacher,
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("assigned to you", response.get_json()["error"])

    def test_04_full_workflow_and_student_visibility(self):
        exam_id = self._create_submitted()
        self.assertEqual(
            self.client.post("/api/exams/simple/" + exam_id + "/publish", json={}, headers=self.principal).status_code,
            400,
        )
        self.assertEqual(
            self.client.post(
                "/api/exams/simple/" + exam_id + "/review",
                json={"decision": "approve"}, headers=self.principal,
            ).status_code,
            200,
        )
        published = self.client.post(
            "/api/exams/simple/" + exam_id + "/publish", json={}, headers=self.principal
        )
        self.assertEqual(published.status_code, 200, published.get_json())

        student_data = self.client.get("/api/exams/student?portal=student", headers=self.student).get_json()
        self.assertTrue(any(e["id"] == exam_id for e in student_data["exams"]))
        self.assertIn("cls-10a", student_data["enrolled_classes"])
        self.assertTrue(all("score" not in e for e in student_data["exams"]))

    def test_05_student_isolation(self):
        exam_id = self._create_submitted(exam_date="2026-12-29")
        self.client.post(
            "/api/exams/simple/" + exam_id + "/review",
            json={"decision": "approve"}, headers=self.principal,
        )
        self.client.post("/api/exams/simple/" + exam_id + "/publish", json={}, headers=self.principal)
        unrelated = self.client.get(
            "/api/exams/student?student_id=2026-STD-0143", headers=self.principal
        ).get_json()
        self.assertEqual(unrelated["enrolled_classes"], ["cls-11b"])
        self.assertFalse(any(e["id"] == exam_id for e in unrelated["exams"]))

    def test_06_conflict_detection(self):
        first = self._create_submitted(exam_date="2026-12-30", start_time="10:00", end_time="11:00")
        duplicate = self.client.post(
            "/api/exams/simple",
            json=self._payload(exam_date="2026-12-30", start_time="10:30", end_time="11:30"),
            headers=self.teacher,
        )
        self.assertEqual(duplicate.status_code, 409)
        self.assertIn("already has", duplicate.get_json()["error"])
        self.assertTrue(first)

    def test_07_admin_has_no_academic_approval_authority(self):
        exam_id = self._create_submitted(exam_date="2026-12-31")
        self.assertEqual(
            self.client.post(
                "/api/exams/simple/" + exam_id + "/review",
                json={"decision": "approve"}, headers=self.admin,
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                "/api/exams/simple/" + exam_id + "/publish", json={}, headers=self.admin
            ).status_code,
            403,
        )

    def test_08_admin_can_correct_schedule_without_approving(self):
        exam_id = self._create_submitted(exam_date="2027-01-04")
        response = self.client.put(
            "/api/exams/simple/" + exam_id,
            json=self._payload(exam_date="2027-01-05", start_time="13:00", end_time="14:00"),
            headers=self.admin,
        )
        self.assertEqual(response.status_code, 200, response.get_json())
        data = self.client.get("/api/exams/simple?portal=admin", headers=self.admin).get_json()
        exam = next(e for e in data["data"] if e["id"] == exam_id)
        self.assertEqual(exam["exam_date"], "2027-01-05")
        self.assertEqual(exam["status"], "submitted")

    def test_09_filters(self):
        exam_id = self._create_submitted(exam_date="2027-02-11")
        by_type = self.client.get(
            "/api/exams/simple?portal=principal&exam_type=class_test", headers=self.principal
        ).get_json()
        by_month = self.client.get(
            "/api/exams/simple?portal=principal&month=2027-02", headers=self.principal
        ).get_json()
        self.assertTrue(any(e["id"] == exam_id for e in by_type["data"]))
        self.assertTrue(any(e["id"] == exam_id for e in by_month["data"]))
        self.assertFalse(any(e["exam_type"] != "class_test" for e in by_type["data"]))
        self.assertTrue(all(e["exam_date"].startswith("2027-02") for e in by_month["data"]))

    def test_10_cancel_removes_from_students(self):
        exam_id = self._create_submitted(exam_date="2027-03-15")
        self.client.post(
            "/api/exams/simple/" + exam_id + "/review",
            json={"decision": "approve"}, headers=self.principal,
        )
        self.client.post("/api/exams/simple/" + exam_id + "/publish", json={}, headers=self.principal)
        self.assertTrue(any(
            e["id"] == exam_id
            for e in self.client.get("/api/exams/student?portal=student", headers=self.student).get_json()["exams"]
        ))
        cancelled = self.client.post(
            "/api/exams/simple/" + exam_id + "/cancel", json={}, headers=self.principal
        )
        self.assertEqual(cancelled.status_code, 200)
        self.assertFalse(any(
            e["id"] == exam_id
            for e in self.client.get("/api/exams/student?portal=student", headers=self.student).get_json()["exams"]
        ))

    def test_11_activity_log_records_workflow(self):
        exam_id = self._create_submitted(exam_date="2027-04-20")
        self.client.post(
            "/api/exams/simple/" + exam_id + "/review",
            json={"decision": "approve"}, headers=self.principal,
        )
        activity = self.client.get(
            "/api/exams/activity?exam_id=" + exam_id, headers=self.admin
        ).get_json()
        actions = [entry["action"] for entry in activity["data"]]
        self.assertIn("create", actions)
        self.assertIn("submit", actions)
        self.assertIn("approve", actions)


    def test_12_department_context_isolation(self):
        """A department hub must never leak exams from other departments."""
        payload = self._payload(
            department_id="dept-khm", subject_id="subj-khm-lit",
            exam_type="monthly", exam_date="2027-05-10",
            start_time="08:00", end_time="09:15", submit_for_review=True,
        )
        created = self.client.post("/api/exams/simple", json=payload, headers=self.principal)
        self.assertEqual(created.status_code, 201, created.get_json())
        exam_id = created.get_json()["data"]["id"]
        self.client.post(
            "/api/exams/simple/" + exam_id + "/review",
            json={"decision": "approve"}, headers=self.principal,
        )
        self.client.post("/api/exams/simple/" + exam_id + "/publish", json={}, headers=self.principal)

        khmer = self.client.get(
            "/api/exams/student?portal=student&dept=khmer", headers=self.student
        ).get_json()
        english = self.client.get(
            "/api/exams/student?portal=student&dept=english", headers=self.student
        ).get_json()
        self.assertTrue(any(e["id"] == exam_id for e in khmer["exams"]))
        self.assertTrue(all(e["department_id"] == "dept-khm" for e in khmer["exams"]))
        self.assertFalse(any(e["id"] == exam_id for e in english["exams"]))
        self.assertTrue(all(e["department_id"] != "dept-khm" for e in english["exams"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
