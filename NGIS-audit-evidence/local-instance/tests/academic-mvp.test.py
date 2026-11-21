#!/usr/bin/env python3
"""Security and contract tests for the persistent Grades & Attendance MVP."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

DB_FILE = tempfile.NamedTemporaryFile(prefix='ngis-academic-', suffix='.sqlite3', delete=False).name
os.environ['NGIS_ACADEMIC_DB'] = DB_FILE
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server  # noqa: E402


class AcademicMvpTests(unittest.TestCase):
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

    def test_auth_is_exact_and_academic_routes_require_it(self):
        self.assertEqual(self.client.get('/api/academic/config').status_code, 401)
        self.assertEqual(self.client.post('/api/auth/login', json={'email': 'teacher@evil.example', 'password': 'password123'}).status_code, 401)
        self.assertEqual(self.client.post('/api/auth/login', json={'email': 'teacher@ngis.edu.kh', 'password': 'wrong'}).status_code, 401)
        self.assertEqual(self.client.get('/api/academic/config', headers=self.h(self.token('student@ngis.edu.kh'))).status_code, 200)

    def test_student_cannot_write_and_parent_is_link_scoped(self):
        student = self.token('student@ngis.edu.kh')
        parent = self.token('parent@ngis.edu.kh')
        payload = {'studentId': '2026-STD-0142', 'classId': 'cls-10a', 'subjectId': 'subj-math', 'assessmentTitle': 'Nope', 'score': 90, 'maxScore': 100}
        self.assertEqual(self.client.post('/api/academic/grades', headers=self.h(student), json=payload).status_code, 403)
        self.assertEqual(self.client.get('/api/academic/grades?studentId=2026-STD-0144', headers=self.h(parent)).status_code, 403)

    def test_teacher_grade_and_attendance_workflows(self):
        teacher = self.token('teacher@ngis.edu.kh')
        grade = self.client.post('/api/academic/grades', headers=self.h(teacher), json={
            'studentId': '2026-STD-0142', 'classId': 'cls-10a', 'subjectId': 'subj-math',
            'assessmentTitle': 'Term 2 Quiz', 'assessmentType': 'quiz', 'score': 92, 'maxScore': 100,
        })
        self.assertEqual(grade.status_code, 201, grade.get_json())
        self.assertEqual(grade.get_json()['data']['letter_grade'], 'A')
        attendance = self.client.post('/api/academic/attendance', headers=self.h(teacher), json={
            'classId': 'cls-10a', 'date': '2026-10-23', 'records': [
                {'studentId': '2026-STD-0142', 'status': 'present'},
                {'studentId': '2026-STD-0144', 'status': 'late'},
            ]
        })
        self.assertEqual(attendance.status_code, 201, attendance.get_json())
        again = self.client.post('/api/academic/attendance', headers=self.h(teacher), json={
            'classId': 'cls-10a', 'date': '2026-10-23', 'records': [{'studentId': '2026-STD-0142', 'status': 'absent'}]
        })
        self.assertEqual(again.status_code, 201)
        records = self.client.get('/api/academic/attendance?studentId=2026-STD-0142', headers=self.h(self.token('student@ngis.edu.kh'))).get_json()['data']
        self.assertEqual(len([r for r in records if r['date'] == '2026-10-23']), 1)
        self.assertEqual(records[0]['status'], 'absent')

    def test_report_card_and_audit_are_derived_from_records(self):
        student = self.token('student@ngis.edu.kh')
        report = self.client.get('/api/academic/report-cards', headers=self.h(student))
        self.assertEqual(report.status_code, 200)
        body = report.get_json()['data']
        self.assertIn('grades', body)
        self.assertIn('attendance', body)
        admin = self.token('admin@ngis.edu.kh')
        audit = self.client.get('/api/academic/audit?limit=10', headers=self.h(admin))
        self.assertEqual(audit.status_code, 200)
        self.assertIsInstance(audit.get_json()['data'], list)


if __name__ == '__main__':
    unittest.main()
