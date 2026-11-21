#!/usr/bin/env python3
"""Automated tests for NGIS Teacher Portal — My Class Workspace."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

DB_FILE = tempfile.NamedTemporaryFile(prefix='ngis-teacher-myclass-', suffix='.sqlite3', delete=False).name
os.environ['NGIS_ACADEMIC_DB'] = DB_FILE
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server  # noqa: E402


class TeacherMyClassWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.app.config['TESTING'] = True
        cls.client = server.app.test_client()

    def token(self, email):
        res = self.client.post('/api/auth/login', json={'email': email, 'password': 'password123'})
        self.assertEqual(res.status_code, 200)
        return res.get_json()['data']['token']

    def h(self, token):
        return {'Authorization': 'Bearer ' + token}

    def test_teacher_assigned_classes_list(self):
        """Teacher can fetch assigned classes with live summary metrics."""
        teacher_token = self.token('teacher@ngis.edu.kh')
        res = self.client.get('/api/teacher/classes', headers=self.h(teacher_token))
        self.assertEqual(res.status_code, 200)
        classes = res.get_json()['data']
        self.assertGreaterEqual(len(classes), 3)

        class_ids = [c['id'] for c in classes]
        self.assertIn('cls-10a', class_ids)
        self.assertIn('cls-11b', class_ids)
        self.assertIn('cls-11c', class_ids)

        c10a = next(c for c in classes if c['id'] == 'cls-10a')
        self.assertTrue(c10a['isHomeroom'])
        self.assertIn('studentCount', c10a)
        self.assertIn('attendanceRate', c10a)
        self.assertIn('pendingSubmissions', c10a)

    def test_class_workspace_data_and_kpis(self):
        """Teacher can load comprehensive workspace data for assigned class."""
        teacher_token = self.token('teacher@ngis.edu.kh')
        res = self.client.get('/api/teacher/classes/cls-10a/workspace', headers=self.h(teacher_token))
        self.assertEqual(res.status_code, 200)
        ws = res.get_json()['data']

        # Class details
        self.assertEqual(ws['class']['id'], 'cls-10a')
        self.assertEqual(ws['class']['name'], 'Grade 10A')
        self.assertTrue(ws['class']['isHomeroom'])

        # Overview KPIs
        ov = ws['overview']
        self.assertIn('enrolledStudents', ov)
        self.assertIn('attendanceToday', ov)
        self.assertIn('pendingSubmissions', ov)
        self.assertIn('activeAssignments', ov)
        self.assertIn('gradebookCompletion', ov)

        # Roster
        self.assertGreaterEqual(len(ws['students']), 1)
        student_names = [s['name'] for s in ws['students']]
        self.assertIn('Nrinphouneta Hok', student_names)

        # Assignments & Submissions
        self.assertIsInstance(ws['assignments'], list)
        self.assertIsInstance(ws['submissions'], list)

    def test_security_teacher_cannot_access_unassigned_class(self):
        """Security: teacher cannot access unassigned class workspace."""
        teacher_token = self.token('teacher@ngis.edu.kh')
        # cls-10b is assigned to Dr. Pov Sophea, not Dr. Sarah Jenkins
        res = self.client.get('/api/teacher/classes/cls-10b/workspace', headers=self.h(teacher_token))
        self.assertEqual(res.status_code, 403)
        self.assertIn('FORBIDDEN', res.get_json()['error']['code'])

        res_students = self.client.get('/api/teacher/classes/cls-10b/students', headers=self.h(teacher_token))
        self.assertEqual(res_students.status_code, 403)

    def test_student_and_unauthenticated_forbidden(self):
        """Students or unauthenticated callers cannot access teacher workspace."""
        # Unauthenticated
        res = self.client.get('/api/teacher/classes/cls-10a/workspace')
        self.assertEqual(res.status_code, 401)

        # Student role
        student_token = self.token('student@ngis.edu.kh')
        res_student = self.client.get('/api/teacher/classes/cls-10a/workspace', headers=self.h(student_token))
        self.assertEqual(res_student.status_code, 403)

    def test_submission_review_and_grading_flow(self):
        """Teacher can review and grade student assignment submissions directly."""
        teacher_token = self.token('teacher@ngis.edu.kh')
        asgn_id = 'asgn-001'
        student_id = '2026-STD-0142'

        # Grade the submission
        grade_res = self.client.post(
            f'/api/assignments/{asgn_id}/grade',
            headers=self.h(teacher_token),
            json={
                'studentId': student_id,
                'score': 95.5,
                'feedback': 'Excellent mathematical reasoning and clear derivation steps.'
            }
        )
        self.assertEqual(grade_res.status_code, 200)
        sub_data = grade_res.get_json()['data']
        self.assertEqual(sub_data['score'], 95.5)
        self.assertEqual(sub_data['status'], 'graded')

        # Check that submissions list reflects the graded submission
        subs_res = self.client.get('/api/teacher/classes/cls-10a/submissions', headers=self.h(teacher_token))
        self.assertEqual(subs_res.status_code, 200)
        submissions = subs_res.get_json()['data']
        matching = next((s for s in submissions if s['assignmentId'] == asgn_id and s['studentId'] == student_id), None)
        self.assertIsNotNone(matching)
        self.assertEqual(matching['score'], 95.5)
        self.assertEqual(matching['status'], 'graded')


if __name__ == '__main__':
    unittest.main()
