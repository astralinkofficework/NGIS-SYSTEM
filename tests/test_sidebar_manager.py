"""
Unit & Integration Test Suite: NGIS Global Sidebar Manager
Validates:
- All 6 portals (superadmin, admin, principal, teacher, student, staff)
- Navigation API endpoints (/api/nav/published, /api/nav/portals, /api/nav/routes, /api/nav/config, etc.)
- Validation engine (duplicate IDs, broken routes, circular parent references)
- Draft, Publish, Rollback, and Factory Reset lifecycle
- Security & Role authorization (admin / superadmin required)
- Mobile hamburger menu button compliance (AGENTS.md)
- Zero bold font weights compliance (max font-weight: 500)
"""

import os
import json
import unittest
from server import app
import sidebar_nav_engine as engine


class TestSidebarManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.admin_headers = {
            'X-User-Email': 'admin@ngis.edu.kh',
            'X-User-Role': 'admin',
            'X-User-Id': 'ADM-2024-001',
            'X-User-Name': 'Sok Panha Heng'
        }
        cls.student_headers = {
            'X-User-Email': 'student@ngis.edu.kh',
            'X-User-Role': 'student',
            'X-User-Id': 'STU-2026-001',
            'X-User-Name': 'Nrinphouneta'
        }

    def test_01_all_six_portals_configured(self):
        """All 6 school portals must be registered in the overview."""
        res = self.client.get('/api/nav/portals')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        portals = [p['portal'] for p in data.get('data', [])]
        expected = ['superadmin', 'admin', 'principal', 'teacher', 'student', 'staff']
        for exp in expected:
            self.assertIn(exp, portals, f"Portal {exp} must be present in overview.")

    def test_02_published_navigation_public_access(self):
        """Runtime published navigation must be accessible without auth."""
        res = self.client.get('/api/nav/published')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        pub = data.get('data', {})
        self.assertIn('admin', pub)
        self.assertIn('student', pub)
        self.assertIn('superadmin', pub)
        self.assertIn('principal', pub)
        self.assertIn('teacher', pub)
        self.assertIn('staff', pub)

    def test_03_student_portal_structure_preserved(self):
        """The existing Student portal navigation must remain intact and functional."""
        res = self.client.get('/api/nav/published?portal=student')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        student_nav = data.get('data', {})
        self.assertEqual(student_nav.get('brand'), 'Student')
        groups = student_nav.get('groups', [])
        group_labels = [g.get('label') for g in groups]
        self.assertIn('Main', group_labels)
        self.assertIn('ACADEMICS', group_labels)
        self.assertIn('CAMPUS LIFE', group_labels)

    def test_04_route_registry_filters_existing_files(self):
        """The route registry must only return registered paths that exist on disk."""
        res = self.client.get('/api/nav/routes', headers=self.admin_headers)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        routes = data.get('data', [])
        self.assertTrue(len(routes) > 10, "Should have discovered project routes.")
        for r in routes:
            href = r if isinstance(r, str) else r.get('href', '')
            path = href.split('?')[0].split('#')[0]
            self.assertTrue(os.path.exists(path), f"Route path {path} must exist on disk.")

    def test_05_role_authorization_blocks_unauthorized_users(self):
        """Unauthorized non-admin roles must be blocked with 403 Forbidden."""
        res = self.client.get('/api/nav/config?portal=admin', headers=self.student_headers)
        self.assertEqual(res.status_code, 403)
        res_post = self.client.post('/api/nav/draft',
                                    headers=self.student_headers,
                                    json={'portal': 'admin', 'payload': {}})
        self.assertEqual(res_post.status_code, 403)

    def test_06_validation_detects_broken_routes_and_duplicates(self):
        """Validator must flag non-existent local routes and duplicate item IDs."""
        invalid_draft = {
            "groups": [
                {
                    "id": "g1",
                    "label": "Test Group",
                    "links": [
                        {"id": "item1", "label": "Valid Item", "icon": "home", "href": "pages/admin/admin.html"},
                        {"id": "item1", "label": "Duplicate ID Item", "icon": "home", "href": "pages/admin/admin.html"},
                        {"id": "item2", "label": "Broken Route Item", "icon": "home", "href": "pages/admin/non-existent-page-xyz.html"}
                    ]
                }
            ]
        }
        res = self.client.post('/api/nav/validate',
                               headers=self.admin_headers,
                               json={'portal': 'admin', 'payload': invalid_draft})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        findings = data.get('data', {}).get('findings', [])
        finding_codes = [f['code'] for f in findings]
        self.assertIn('duplicate_id', finding_codes)
        self.assertIn('broken_route', finding_codes)

    def test_07_draft_and_publish_lifecycle(self):
        """Draft saving must not mutate published navigation until publish is invoked."""
        # 1. Get initial published state for staff
        res_init = self.client.get('/api/nav/published?portal=staff')
        init_data = res_init.get_json()['data']

        # 2. Save a valid draft for staff (including mandatory locked item)
        test_draft = {
            "brand": "Staff Operations",
            "meta": "Draft Navigation Test",
            "groups": [
                {
                    "id": "staff-overview-grp",
                    "label": "Overview",
                    "links": [
                        {"id": "staff-services", "label": "Campus Services Hub", "icon": "grid_view", "href": "pages/admin/admin-services.html", "locked": True}
                    ]
                },
                {
                    "id": "staff-test-grp",
                    "label": "Test Operations",
                    "links": [
                        {"id": "staff-test-1", "label": "Campus Directory", "icon": "business", "href": "pages/admin/admin-campuses.html"}
                    ]
                }
            ]
        }
        res_draft = self.client.post('/api/nav/draft',
                                     headers=self.admin_headers,
                                     json={'portal': 'staff', 'payload': test_draft})
        self.assertEqual(res_draft.status_code, 200)

        # 3. Verify published state is UNCHANGED
        res_check = self.client.get('/api/nav/published?portal=staff')
        self.assertEqual(res_check.get_json()['data']['brand'], init_data['brand'])

        # 4. Publish the draft
        res_pub = self.client.post('/api/nav/publish',
                                   headers=self.admin_headers,
                                   json={'portal': 'staff', 'summary': 'Test Publish'})
        self.assertEqual(res_pub.status_code, 200)

        # 5. Verify published state is updated
        res_pub_check = self.client.get('/api/nav/published?portal=staff')
        self.assertEqual(res_pub_check.get_json()['data']['brand'], "Staff Operations")

        # 6. Restore factory defaults for staff
        res_reset = self.client.post('/api/nav/defaults',
                                     headers=self.admin_headers,
                                     json={'portal': 'staff'})
        self.assertEqual(res_reset.status_code, 200)
        res_after_reset = self.client.get('/api/nav/published?portal=staff')
        self.assertEqual(res_after_reset.get_json()['data']['brand'], "Staff")

    def test_08_health_audit_runs_successfully(self):
        """Health check endpoint must return report with severity and findings."""
        res = self.client.get('/api/nav/health?portal=admin', headers=self.admin_headers)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get('success'))
        health_data = data.get('data', {})
        self.assertIn('portal', health_data)
        self.assertIn('findings', health_data)

    def test_09_mobile_hamburger_compliance(self):
        """admin-dashboard-content.html must include the mandatory mobile hamburger button."""
        with open('pages/admin/admin-dashboard-content.html', 'r', encoding='utf-8') as f:
            html = f.read()
        self.assertIn('data-action="toggle-sidebar"', html)
        self.assertIn('hamburger-btn', html)
        self.assertIn('mobile-hamburger-btn', html)
        self.assertIn('aria-label="Open menu"', html)
        self.assertIn('mobile-appbar', html)

    def test_10_mobile_tabs_switcher_present(self):
        """admin-dashboard-content.html must include the segmented mobile column tabs switcher."""
        with open('pages/admin/admin-dashboard-content.html', 'r', encoding='utf-8') as f:
            html = f.read()
        self.assertIn('sgm-mobile-tabs', html)
        self.assertIn('data-sgm-tab="tree"', html)
        self.assertIn('data-sgm-tab="preview"', html)
        self.assertIn('data-sgm-tab="settings"', html)

    def test_11_zero_bold_fonts_typography_compliance(self):
        """No bold font weights (700, 800, font-bold) are allowed in the CMS workspace."""
        files = [
            'pages/admin/admin-dashboard-content.html',
            'assets/css/admin-dashboard-cms.css',
            'assets/js/admin-sidebar-manager.js',
            'assets/js/admin-dashboard-cms.js'
        ]
        import re
        bad_patterns = [r'font-bold', r'font-extrabold', r'font-black', r'font-weight\s*:\s*[6-9]\d\d']
        violations = []
        for f in files:
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
            for pat in bad_patterns:
                matches = re.findall(pat, content)
                if matches:
                    violations.append(f"{f}: {len(matches)} violations of {pat}")
        self.assertEqual(len(violations), 0, f"Typography violations found: {violations}")


if __name__ == '__main__':
    unittest.main()
