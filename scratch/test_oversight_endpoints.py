import sys
sys.path.insert(0, '.')
import unittest
from server import app

class TestOversightEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_oversight_status(self):
        resp = self.client.get('/api/timetable/oversight/status')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertEqual(len(data.get('stages', [])), 6)
        self.assertIn('overall_progress_pct', data)
        self.assertIn('outstanding_tasks', data)

    def test_get_and_post_reminders(self):
        resp = self.client.get('/api/timetable/reminders')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data.get('success'))
        self.assertIsInstance(data.get('reminders'), list)

        # Post a reminder
        post_resp = self.client.post('/api/timetable/reminders', json={
            "recipient_id": "PRIN-2024-001",
            "recipient_name": "Dr. Ly Bunheng",
            "recipient_role": "Principal",
            "recipient_email": "principal@ngis.edu.kh",
            "task_id": "test_task_01",
            "task_name": "Test Timetable Verification",
            "message": "Please review Grade 7 schedule.",
            "force_duplicate": True
        })
        self.assertEqual(post_resp.status_code, 200)
        post_data = post_resp.get_json()
        self.assertTrue(post_data.get('success'))
        rem_id = post_data.get('reminder', {}).get('id')

        # Read reminder
        read_resp = self.client.post(f'/api/timetable/reminders/{rem_id}/read')
        self.assertEqual(read_resp.status_code, 200)
        self.assertTrue(read_resp.get_json().get('success'))

if __name__ == '__main__':
    unittest.main()
