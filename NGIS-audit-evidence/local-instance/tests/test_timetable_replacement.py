"""
Consolidated Automated Test Suite for Cambodian School Timetable Management Replacement
Tests:
  1. Health & Seed Integrity
  2. Teacher Unavailability Constraints in Conflicts & Auto-assign
  3. Section 8 Critical Reassignment with Slot Preservation
  4. Publishing Workflow (Section 18): Zero Hard Conflicts validation & Snapshot
  5. Downstream Student Portal Timetable API & Security (no private fields)
  6. Downstream Teacher Portal Timetable API & Workload
  7. Direct Publishing Propagation Downstream
  8. Excel Bulk Teacher Import with Safe Identity Resolution
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import server
import timetable_models

class TestTimetableReplacement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.app.test_client()

    def setUp(self):
        # Reset state cleanly via API before each test
        self.client.post('/api/timetable/reset')

    def test_01_health_and_extended_models(self):
        res = self.client.get('/api/timetable/state')
        data = res.get_json()
        state = data.get('state', {})
        self.assertGreaterEqual(len(state.get('teachers', [])), 15)
        self.assertGreaterEqual(len(state.get('classes', [])), 12)
        self.assertGreaterEqual(len(state.get('subjects', [])), 13)

        # Check extended teacher fields
        t0 = state['teachers'][0]
        self.assertIn('codes', t0)
        self.assertIn('max_daily', t0)
        self.assertIn('employee_id', t0)
        self.assertIn('unavailable_slots', t0)

        # Check extended class fields
        c0 = state['classes'][0]
        self.assertIn('room', c0)
        self.assertIn('shift', c0)

    def test_02_section_8_reassignment_algorithm(self):
        # Place 2 slots for class_10A with t_M1
        self.client.post('/api/timetable/cells', json={'key': 'ច័ន្ទ|ព្រឹក|1|class_10A', 'subject_id': 'sub_M', 'teacher_id': 't_M1'})
        self.client.post('/api/timetable/cells', json={'key': 'ច័ន្ទ|ព្រឹក|2|class_10A', 'subject_id': 'sub_M', 'teacher_id': 't_M1'})

        # Reassign to t_M2
        re_resp = self.client.post('/api/timetable/reassign', json={'class_id': 'class_10A', 'subject_id': 'sub_M', 'new_teacher_id': 't_M2'})
        self.assertEqual(re_resp.status_code, 200)
        res = re_resp.get_json()
        self.assertTrue(res['success'])
        result = res.get('result', {})
        self.assertEqual(result.get('preserved_count'), 2)
        self.assertEqual(result.get('displaced_count'), 0)

        # Verify slots updated to t_M2
        state = self.client.get('/api/timetable/state').get_json().get('state', {})
        self.assertEqual(state['grid']['ច័ន្ទ|ព្រឹក|1|class_10A']['teacher_id'], 't_M2')
        self.assertEqual(state['grid']['ច័ន្ទ|ព្រឹក|2|class_10A']['teacher_id'], 't_M2')

    def test_03_section_8_reassignment_displaces_conflicts(self):
        # Place slot 1 for class_10A with t_M1, and slot 1 for class_11A with t_M2 (creating future double-booking for t_M2)
        self.client.post('/api/timetable/cells', json={'key': 'ច័ន្ទ|ព្រឹក|1|class_10A', 'subject_id': 'sub_M', 'teacher_id': 't_M1'})
        self.client.post('/api/timetable/cells', json={'key': 'ច័ន្ទ|ព្រឹក|1|class_11A', 'subject_id': 'sub_M', 'teacher_id': 't_M2'})

        # Reassign class_10A sub_M to t_M2
        re_resp = self.client.post('/api/timetable/reassign', json={'class_id': 'class_10A', 'subject_id': 'sub_M', 'new_teacher_id': 't_M2'})
        self.assertEqual(re_resp.status_code, 200)
        res = re_resp.get_json()
        self.assertTrue(res['success'])
        result = res.get('result', {})
        self.assertEqual(result.get('preserved_count'), 0)
        self.assertEqual(result.get('displaced_count'), 1)

        # The conflicting slot for class_10A was removed from placed
        state = self.client.get('/api/timetable/state').get_json().get('state', {})
        self.assertNotIn('ច័ន្ទ|ព្រឹក|1|class_10A', state.get('grid', {}))
        # While class_11A slot remains intact
        self.assertEqual(state['grid']['ច័ន្ទ|ព្រឹក|1|class_11A']['teacher_id'], 't_M2')

    def test_04_publishing_blocks_on_hard_conflicts(self):
        # Place a slot for t_K1
        self.client.post('/api/timetable/cells', json={'key': 'ច័ន្ទ|ព្រឹក|1|class_10A', 'subject_id': 'sub_K', 'teacher_id': 't_K1'})

        # Make t_K1 unavailable at that slot to induce a hard conflict
        self.client.put('/api/timetable/unavailability', json={'teacher_id': 't_K1', 'unavailable_slots': ['ច័ន្ទ|ព្រឹក|1']})

        resp = self.client.post('/api/timetable/publish', json={'published_by': 'Principal', 'term': 'Term 1'})
        self.assertEqual(resp.status_code, 409)
        data = resp.get_json()
        self.assertFalse(data['success'])
        self.assertIn('conflicts', data)

    def test_05_publishing_and_downstream_portals(self):
        # Auto-assign to achieve complete conflict-free timetable
        self.client.post('/api/timetable/auto-assign')

        # Publish
        pub_resp = self.client.post('/api/timetable/publish', json={'published_by': 'Principal Som', 'term': 'AY 2026-2027 Official'})
        self.assertEqual(pub_resp.status_code, 200)
        pub_data = pub_resp.get_json()
        self.assertTrue(pub_data['success'])
        version = pub_data['published']['version']

        # 1. Student Portal Class Query
        student_resp = self.client.get('/api/timetable/published/class/class_10A')
        self.assertEqual(student_resp.status_code, 200)
        student_data = student_resp.get_json()
        self.assertTrue(student_data['success'])
        self.assertEqual(student_data['version'], version)
        self.assertGreater(len(student_data['lessons']), 0)

        # Privacy check: no private employee records exposed
        for lesson in student_data['lessons']:
            self.assertNotIn('phone', lesson)
            self.assertNotIn('salary', lesson)
            self.assertNotIn('notes', lesson)

        # 2. Teacher Portal Teacher Query
        teacher_resp = self.client.get('/api/timetable/published/teacher/t_K1')
        self.assertEqual(teacher_resp.status_code, 200)
        teacher_data = teacher_resp.get_json()
        self.assertTrue(teacher_data['success'])
        self.assertEqual(teacher_data['version'], version)
        self.assertGreater(len(teacher_data['lessons']), 0)

    def test_06_bulk_teacher_import(self):
        import_data = [
            {
                'employee_id': 'EMP-2001',
                'name_kh': 'សុខ ដារ៉ា (Updated Name)',
                'code': 'K1',
                'codes': ['K1', 'K-ADV'],
                'target': 18
            },
            {
                'employee_id': 'EMP-NEW-99',
                'name_kh': 'គ្រូថ្មី ពិសិដ្ឋ',
                'name_en': 'Piseth New',
                'code': 'P99',
                'codes': ['P99'],
                'target': 16
            }
        ]
        resp = self.client.post('/api/timetable/teachers/bulk-import', json={'teachers': import_data})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['updated'], 1)
        self.assertEqual(data['created'], 1)

        # Verify t_K1 was updated non-destructively
        state = self.client.get('/api/timetable/state').get_json().get('state', {})
        t_K1 = next(t for t in state.get('teachers', []) if t['id'] == 't_K1')
        self.assertEqual(t_K1['name_kh'], 'សុខ ដារ៉ា (Updated Name)')
        self.assertEqual(t_K1['target'], 18)

if __name__ == '__main__':
    unittest.main(verbosity=2)
