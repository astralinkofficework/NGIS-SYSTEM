import unittest
import json
import io
from server import app
import dashboard_cms_engine as engine


class TestDashboardCMS(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_01_runtime_content_endpoint(self):
        resp = self.app.get('/api/cms/dashboard/content?portal=student')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data['success'])
        self.assertIn('hero', data['data'])
        self.assertIn('banners', data['data'])
        self.assertIn('carousel', data['data'])
        self.assertIn('page_sections', data['data'])

        # Verify dynamic token substitution in greeting
        greeting = data['data']['hero']['greeting']
        self.assertIn('Nrinphouneta', greeting)
        self.assertNotIn('{first_name}', greeting)

    def test_02_portal_role_targeting(self):
        # Teacher portal
        resp = self.app.get('/api/cms/dashboard/content?portal=teacher')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('Sarah', data['data']['hero']['greeting'])

        # Principal portal
        resp_prn = self.app.get('/api/cms/dashboard/content?portal=principal')
        self.assertEqual(resp_prn.status_code, 200)
        data_prn = json.loads(resp_prn.data)
        self.assertIn('Ly Bunheng', data_prn['data']['hero']['greeting'])

    def test_03_cms_config_endpoint(self):
        resp = self.app.get('/api/cms/dashboard/config')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data['success'])
        self.assertIn('portals_config', data['data'])
        self.assertIn('media_library', data['data'])

    def test_04_save_draft_and_read(self):
        draft_payload = {
            'portal': 'student',
            'draft': {
                'hero': {
                    'title': 'Test Draft Heading',
                    'description': 'Test Draft Description',
                    'greeting_template': 'Hello, {first_name}! Good luck on exams.',
                    'text_alignment': 'center',
                    'visible': True,
                    'date_config': {'visible': True, 'format': 'short'}
                },
                'banners': [
                    {
                        'id': 'ban-draft-001',
                        'name': 'Draft Banner',
                        'heading': 'Draft Banner Heading',
                        'subtitle': 'Draft subtitle',
                        'image_url': 'https://example.com/banner.jpg',
                        'order': 1,
                        'active': True,
                        'status': 'draft'
                    }
                ],
                'carousel_settings': {'autoplay': False, 'interval_seconds': 5},
                'page_sections': [{'id': 'sec-hero', 'name': 'Hero', 'visible': True, 'order': 1}]
            }
        }
        resp = self.app.post('/api/cms/dashboard/draft',
                             data=json.dumps(draft_payload),
                             content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertTrue(data['success'])

        # Verify draft is returned when requested with mode=draft
        resp_draft = self.app.get('/api/cms/dashboard/content?portal=student&mode=draft')
        self.assertEqual(resp_draft.status_code, 200)
        draft_data = json.loads(resp_draft.data)
        self.assertEqual(draft_data['data']['hero']['title'], 'Test Draft Heading')

        # Verify live published remains unchanged from the draft
        resp_pub = self.app.get('/api/cms/dashboard/content?portal=student&mode=published')
        self.assertEqual(resp_pub.status_code, 200)
        pub_data = json.loads(resp_pub.data)
        self.assertNotEqual(pub_data['data']['hero']['title'], 'Test Draft Heading')

    def test_05_publish_and_versioning(self):
        payload = {
            'portal': 'student',
            'summary': 'Unit test publication release',
            'payload': {
                'hero': {
                    'title': 'Published Test Heading',
                    'description': 'Active verified description',
                    'greeting_template': 'Hello, {first_name}! Welcome back.',
                    'text_alignment': 'left',
                    'visible': True,
                    'date_config': {'visible': True, 'format': 'full'}
                },
                'banners': [
                    {
                        'id': 'ban-std-001',
                        'name': 'Empowering Future Leaders',
                        'heading': 'Empowering Future Leaders',
                        'subtitle': 'Explore learning',
                        'image_url': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=320&fit=crop',
                        'order': 1,
                        'active': True,
                        'status': 'published'
                    }
                ],
                'carousel_settings': {'autoplay': True, 'interval_seconds': 6},
                'page_sections': [{'id': 'sec-hero', 'name': 'Hero', 'visible': True, 'order': 1}]
            }
        }
        resp = self.app.post('/api/cms/dashboard/publish',
                             data=json.dumps(payload),
                             content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        res = json.loads(resp.data)
        self.assertTrue(res['success'])
        version_id = res['version']['version_id']

        # Verify versions endpoint
        v_resp = self.app.get('/api/cms/dashboard/versions?portal=student')
        self.assertEqual(v_resp.status_code, 200)
        v_data = json.loads(v_resp.data)
        v_ids = [v['version_id'] for v in v_data['data']]
        self.assertIn(version_id, v_ids)

    def test_06_restore_version(self):
        # Fetch versions
        v_resp = self.app.get('/api/cms/dashboard/versions?portal=student')
        v_data = json.loads(v_resp.data)
        first_version = v_data['data'][0]['version_id']

        # Restore
        r_resp = self.app.post('/api/cms/dashboard/restore',
                               data=json.dumps({'version_id': first_version}),
                               content_type='application/json')
        self.assertEqual(r_resp.status_code, 200)
        r_data = json.loads(r_resp.data)
        self.assertTrue(r_data['success'])

    def test_07_media_upload_validation(self):
        # Text file pretending to be jpg
        fake_file = (io.BytesIO(b'NOT AN IMAGE CONTENT'), 'fake.jpg')
        resp = self.app.post('/api/cms/dashboard/media/upload',
                             data={'file': fake_file, 'alt_text': 'Fake'},
                             content_type='multipart/form-data')
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertFalse(data['success'])
        self.assertIn('Invalid', data['error'])

    def test_08_media_referential_integrity(self):
        # Attempt to delete media used in active banner
        cfg = engine.get_cms_data()
        used_media = next((m for m in cfg['media_library'] if m.get('used_in')), None)
        if used_media:
            resp = self.app.delete(f"/api/cms/dashboard/media/{used_media['id']}")
            self.assertEqual(resp.status_code, 400)
            data = json.loads(resp.data)
            self.assertFalse(data['success'])
            self.assertIn('Cannot delete media in use', data['error'])

    def test_09_html_page_loads(self):
        resp = self.app.get('/pages/admin/admin-dashboard-content.html')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode('utf-8')
        self.assertIn('Dashboard Content Manager', html)
        self.assertIn('data-action="toggle-sidebar"', html)
        self.assertIn('cms-preview-viewport', html)


if __name__ == '__main__':
    unittest.main()
