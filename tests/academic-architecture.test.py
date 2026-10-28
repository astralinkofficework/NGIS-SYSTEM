#!/usr/bin/env python3
"""End-to-end tests for the complete NGIS Grades & Attendance System MVP."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

DB_FILE = tempfile.NamedTemporaryFile(prefix='ngis-academic-arch-', suffix='.sqlite3', delete=False).name
os.environ['NGIS_ACADEMIC_DB'] = DB_FILE
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server  # noqa: E402


class AcademicArchitectureTests(unittest.TestCase):
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

    def test_attendance_by_class_reference_architecture(self):
        """Validates that attendance-by-class returns the exact useful academic architecture from reference portal."""
        student_token = self.token('student@ngis.edu.kh')
        res = self.client.get('/api/academic/attendance-by-class', headers=self.h(student_token))
        self.assertEqual(res.status_code, 200)
        data = res.get_json()['data']

        # 1. Structure
        self.assertIn('student', data)
        self.assertEqual(data['student']['id'], '2026-STD-0142')
        self.assertIn('courses', data)
        self.assertGreaterEqual(len(data['courses']), 9)

        # 2. Check reference courses exist
        course_names = [c['courseName'] for c in data['courses']]
        self.assertIn('Homeroom 11', course_names)
        self.assertIn('AP Biology', course_names)
        self.assertIn('AP Macroeconomics', course_names)
        self.assertIn('Physics III CP', course_names)
        self.assertIn('Art CP', course_names)
        self.assertIn('Pre-AP Chemistry', course_names)
        self.assertIn('AP Pre-Calculus', course_names)
        self.assertIn('Pre-AP English II', course_names)
        self.assertIn('Khmer Language G11', course_names)

        # 3. Check grading periods: P1, Q1, P2, Q2, P3, Q3, P4, Q4
        for p in ['P1', 'Q1', 'P2', 'Q2', 'P3', 'Q3', 'P4', 'Q4']:
            self.assertIn(p, data['gradingPeriods'])

        # 4. Check Pre-AP English II has 'UT' on Thursday (H) matching reference screenshot
        eng_course = next(c for c in data['courses'] if c['courseName'] == 'Pre-AP English II')
        self.assertEqual(eng_course['thisWeek']['H'], 'UT')
        self.assertEqual(eng_course['grades']['Q1'], 'A')
        self.assertEqual(eng_course['room'], 'Rm: 401 (11C)')

        # 5. Check AP Biology teacher and room
        bio_course = next(c for c in data['courses'] if c['courseName'] == 'AP Biology')
        self.assertIn('Pakkirisamy', bio_course['teacherName'])
        self.assertEqual(bio_course['room'], 'Rm: 407 (11C)')
        self.assertEqual(bio_course['grades']['Q1'], 'B+')

        # 6. Check Weighted GPA
        self.assertGreater(data['currentWeightedGpa'], 3.0)

    def test_course_details_breakdown_modal(self):
        """Validates that clicking a grade returns all individual assessments with weights, scores, and feedback."""
        student_token = self.token('student@ngis.edu.kh')
        res = self.client.get('/api/academic/course-details?subjectId=subj-ap-bio', headers=self.h(student_token))
        self.assertEqual(res.status_code, 200)
        data = res.get_json()['data']
        self.assertIn('assessments', data)
        self.assertGreaterEqual(len(data['assessments']), 1)
        first = data['assessments'][0]
        self.assertIn('maxScore', first)
        self.assertIn('score', first)
        self.assertIn('percentage', first)
        self.assertIn('letterGrade', first)

    def test_attendance_by_day_calendar(self):
        """Validates daily attendance log."""
        student_token = self.token('student@ngis.edu.kh')
        res = self.client.get('/api/academic/attendance-by-day', headers=self.h(student_token))
        self.assertEqual(res.status_code, 200)
        data = res.get_json()['data']
        self.assertIn('records', data)
        self.assertIn('summary', data)
        self.assertGreater(len(data['records']), 0)
        rec = data['records'][0]
        self.assertIn('date', rec)
        self.assertIn('day', rec)
        self.assertIn('status', rec)

    def test_teacher_gradebook_and_batch_entry(self):
        """Validates teacher gradebook roster fetching and batch score saving."""
        teacher_token = self.token('teacher@ngis.edu.kh')
        # Load gradebook
        res = self.client.get('/api/academic/gradebook?classId=cls-10a&subjectId=subj-math&periodId=gp-q1', headers=self.h(teacher_token))
        self.assertEqual(res.status_code, 200)
        data = res.get_json()['data']
        self.assertIn('students', data)
        self.assertIn('assessments', data)

        # Create new assessment
        asm_res = self.client.post('/api/academic/assessments', headers=self.h(teacher_token), json={
            'classId': 'cls-10a', 'subjectId': 'subj-math', 'title': 'Mid-Term Exam',
            'category': 'Exam', 'maxScore': 100, 'weight': 2.0, 'gradingPeriodId': 'gp-q1'
        })
        self.assertEqual(asm_res.status_code, 201)
        asm_id = asm_res.get_json()['data']['id']

        # Batch save grades for roster
        batch_res = self.client.post('/api/academic/gradebook/batch', headers=self.h(teacher_token), json={
            'classId': 'cls-10a', 'subjectId': 'subj-math', 'periodId': 'gp-q1', 'workflow': 'submitted',
            'grades': [
                {'studentId': '2026-STD-0142', 'assessmentId': asm_id, 'score': 94, 'comments': 'Great work'},
                {'studentId': '2026-STD-0144', 'assessmentId': asm_id, 'score': 85, 'comments': 'Solid effort'}
            ]
        })
        self.assertEqual(batch_res.status_code, 200)

        # Student cannot modify gradebook
        student_token = self.token('student@ngis.edu.kh')
        self.assertEqual(self.client.post('/api/academic/gradebook/batch', headers=self.h(student_token), json={}).status_code, 403)

    def test_admin_oversight_and_grade_override(self):
        """Validates admin/principal oversight, bulk publishing, and grade override with audit trail."""
        admin_token = self.token('admin@ngis.edu.kh')

        # Oversight metrics
        oversight = self.client.get('/api/academic/admin/oversight', headers=self.h(admin_token))
        self.assertEqual(oversight.status_code, 200)
        self.assertIn('pendingGrades', oversight.get_json()['data'])
        self.assertIn('distribution', oversight.get_json()['data'])

        # Bulk publish
        pub_res = self.client.post('/api/academic/admin/publish-grades', headers=self.h(admin_token), json={'classId': 'cls-10a'})
        self.assertEqual(pub_res.status_code, 200)

        # Override grade
        grade_row = server.ACADEMIC.one("SELECT id, score FROM grades LIMIT 1")
        self.assertIsNotNone(grade_row)
        override_res = self.client.post('/api/academic/admin/override-grade', headers=self.h(admin_token), json={
            'gradeId': grade_row['id'], 'score': 98, 'reason': 'Administrative grade appeal review approved by academic committee'
        })
        self.assertEqual(override_res.status_code, 200)

        # Missing reason must be rejected
        fail_res = self.client.post('/api/academic/admin/override-grade', headers=self.h(admin_token), json={
            'gradeId': grade_row['id'], 'score': 99, 'reason': ''
        })
        self.assertEqual(fail_res.status_code, 400)

        # Audit event recorded for grade override
        audits = self.client.get('/api/academic/audit?limit=5', headers=self.h(admin_token))
        self.assertEqual(audits.status_code, 200)
        actions = [a['action'] for a in audits.get_json()['data']]
        self.assertIn('GRADE_OVERRIDE', actions)

        # Attendance override test
        att_row = server.ACADEMIC.one("SELECT id, status FROM attendance LIMIT 1")
        self.assertIsNotNone(att_row)
        att_override = self.client.post('/api/academic/admin/override-attendance', headers=self.h(admin_token), json={
            'attendanceId': att_row['id'], 'status': 'excused', 'reason': 'Medical note verified by school nurse'
        })
        self.assertEqual(att_override.status_code, 200)

        # Missing reason must be rejected
        att_fail = self.client.post('/api/academic/admin/override-attendance', headers=self.h(admin_token), json={
            'attendanceId': att_row['id'], 'status': 'present', 'reason': ''
        })
        self.assertEqual(att_fail.status_code, 400)

        # Audit event recorded for attendance correction
        audits = self.client.get('/api/academic/audit?limit=5', headers=self.h(admin_token))
        actions = [a['action'] for a in audits.get_json()['data']]
        self.assertIn('ATTENDANCE_CORRECTION', actions)

    def test_parent_child_scoping(self):
        """Validates that parents can only access verified children."""
        parent_token = self.token('parent@ngis.edu.kh')
        # Linked child
        res = self.client.get('/api/academic/attendance-by-class?studentId=2026-STD-0142', headers=self.h(parent_token))
        self.assertEqual(res.status_code, 200)

        # Unlinked child -> 403 Forbidden
        res_unlinked = self.client.get('/api/academic/attendance-by-class?studentId=2026-STD-0144', headers=self.h(parent_token))
        self.assertEqual(res_unlinked.status_code, 403)


if __name__ == '__main__':
    unittest.main()
