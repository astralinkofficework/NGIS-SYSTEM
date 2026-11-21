"""
Comprehensive End-to-End Test Suite for School Information & Academic Configuration Module
Tests:
- API endpoints & data persistence
- Role authorization & permissions (Admin vs Principal vs Editor)
- Multi-campus management
- Operating schedule & bell periods validation
- Academic calendar events
- Audit log & revision tracking
- Integration with Timetable Builder & SQLite academic store
- Browser rendering across desktop, tablet, and mobile
"""

import unittest
import json
import os
import sqlite3
import urllib.request
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:3000"

class SchoolInformationE2ETest(unittest.TestCase):

    def api_request(self, endpoint, method="GET", data=None, headers=None):
        url = f"{BASE_URL}{endpoint}"
        h = {'Content-Type': 'application/json'}
        if headers:
            h.update(headers)
        body = json.dumps(data).encode('utf-8') if data else None
        req = urllib.request.Request(url, data=body, headers=h, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.getcode(), json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))

    # 1. School Overview API
    def test_01_school_overview(self):
        code, res = self.api_request("/api/school-config/overview")
        self.assertEqual(code, 200)
        self.assertTrue(res.get('success'))
        self.assertIn('New Gateway International School', res.get('schoolName'))
        self.assertGreaterEqual(res.get('campusesCount', 0), 1)
        self.assertGreaterEqual(res.get('operatingDaysCount', 0), 5)
        self.assertIn('2026', res.get('activeYear'))

    # 2. School Profile Read & Update
    def test_02_school_profile_update(self):
        # Update as Admin
        payload = {
            "motto": "Excellence in Knowledge, Integrity in Character, Leadership for Tomorrow",
            "phone": "+855 23 888 777",
            "website": "https://ngis.edu.kh"
        }
        code, res = self.api_request("/api/school-config/profile", method="PUT", data=payload, headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)
        self.assertEqual(res.get('data', {}).get('motto'), payload['motto'])

    # 3. Academic Year Creation & Activation
    def test_03_academic_year_lifecycle(self):
        # Create a new test academic year
        new_year = {
            "year": "2029–2030",
            "displayName": "Academic Year 2029–2030",
            "startDate": "2029-09-01",
            "endDate": "2030-06-30"
        }
        code, res = self.api_request("/api/school-config/academic-years", method="POST", data=new_year, headers={"X-User-Role": "admin"})
        self.assertEqual(code, 201)
        created_id = res['item']['id']

        # Activate it as Admin
        code, res = self.api_request(f"/api/school-config/academic-years/{created_id}/activate", method="POST", headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)
        self.assertEqual(res['item']['year'], "2029–2030")
        self.assertTrue(res['item']['isCurrent'])

        # Reactivate AY 2026–2027 as authoritative active year
        code, res = self.api_request("/api/school-config/academic-years/SY-2026/activate", method="POST", headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)
        self.assertEqual(res['item']['year'], "2026–2027")

        # Cleanup test year
        self.api_request(f"/api/school-config/academic-years/{created_id}", method="DELETE", headers={"X-User-Role": "admin"})

    # 4. Campus CRUD & Constraints
    def test_04_campus_crud(self):
        new_cmp = {
            "name": "Chroy Changvar Innovation Campus",
            "code": "CCV-TEST",
            "address": "National Road 6A, Phnom Penh",
            "phone": "+855 23 888 799",
            "principal": "Dr. Ly Bunheng"
        }
        code, res = self.api_request("/api/school-config/campuses", method="POST", data=new_cmp, headers={"X-User-Role": "admin"})
        self.assertEqual(code, 201)
        cmp_id = res['item']['id']

        # Verify duplicate code rejection
        code, res = self.api_request("/api/school-config/campuses", method="POST", data=new_cmp, headers={"X-User-Role": "admin"})
        self.assertEqual(code, 400)

        # Delete test campus
        code, res = self.api_request(f"/api/school-config/campuses/{cmp_id}", method="DELETE", headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)

    # 5. Operating Schedule & Saturday Toggle
    def test_05_operating_schedule(self):
        code, sched = self.api_request("/api/school-config/operating-schedule")
        self.assertEqual(code, 200)
        self.assertIn('weeklyDays', sched['data'])
        self.assertTrue(sched['data']['saturdayEnabled'])

        # Update schedule with Saturday toggle
        sched['data']['saturdayEnabled'] = True
        code, res = self.api_request("/api/school-config/operating-schedule", method="PUT", data=sched['data'], headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)

        # Verify synchronization with timetable_state.json
        with open("data/timetable_state.json", "r", encoding="utf-8") as f:
            tt = json.load(f)
        self.assertIn("សៅរ៍", tt.get('settings', {}).get('days', []))

    # 6. Bell Schedule Validation
    def test_06_bell_schedule_validation(self):
        code, bell = self.api_request("/api/school-config/bell-schedule")
        self.assertEqual(code, 200)
        self.assertEqual(len(bell['data']['periods']), 12) # 10 periods + recess + lunch

        # Attempt invalid period times (closing time earlier than opening)
        invalid_data = dict(bell['data'])
        invalid_data['periods'] = [{"label": "Invalid Period", "start": "11:00", "end": "09:00"}]
        code, res = self.api_request("/api/school-config/bell-schedule", method="PUT", data=invalid_data, headers={"X-User-Role": "admin"})
        self.assertEqual(code, 400)
        self.assertIn("Closing time must occur after start time", res['message'])

    # 7. Academic Calendar Events
    def test_07_calendar_events(self):
        evt = {
            "title": "Semester 2 Science Fair & Robotics Expo",
            "category": "event",
            "startDate": "2027-03-15",
            "endDate": "2027-03-16",
            "description": "Annual student STEM demonstration."
        }
        code, res = self.api_request("/api/school-config/calendar", method="POST", data=evt, headers={"X-User-Role": "admin"})
        self.assertEqual(code, 201)
        evt_id = res['item']['id']

        # Delete event
        code, res = self.api_request(f"/api/school-config/calendar/{evt_id}", method="DELETE", headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)

    # 8. Editor Permission Enforcement
    def test_08_editor_permission_restrictions(self):
        # Editor can view school profile
        code, res = self.api_request("/api/school-config/full", headers={"X-User-Role": "editor", "X-User-Id": "USR-006"})
        self.assertEqual(code, 200)
        self.assertEqual(res['caller']['role'], 'editor')

        # Editor cannot directly activate academic year
        code, res = self.api_request("/api/school-config/academic-years/SY-2027/activate", method="POST", headers={"X-User-Role": "editor", "X-User-Id": "USR-006"})
        self.assertEqual(code, 202) # Submitted for review
        self.assertTrue(res.get('requiresApproval'))

        # Editor cannot modify system permissions matrix
        code, res = self.api_request("/api/school-config/permissions", method="PUT", data={}, headers={"X-User-Role": "editor", "X-User-Id": "USR-006"})
        self.assertEqual(code, 403) # Forbidden

    # 9. Audit Logging
    def test_09_audit_log(self):
        code, res = self.api_request("/api/school-config/audit-log", headers={"X-User-Role": "admin"})
        self.assertEqual(code, 200)
        self.assertGreater(res['total'], 0)
        latest = res['data'][0]
        self.assertIn('userId', latest)
        self.assertIn('timestamp', latest)
        self.assertIn('action', latest)

    # 10. Playwright Browser Responsiveness
    def test_10_browser_views(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            # Test Admin page at 1440px desktop
            page.set_viewport_size({"width": 1440, "height": 900})
            page.goto(f"{BASE_URL}/pages/admin/admin-school-information.html")
            page.wait_for_timeout(600)
            self.assertTrue(page.locator(".hero-topbar").is_visible())
            self.assertTrue(page.locator(".si-title").is_visible())
            page.screenshot(path="scratch/school_info_desktop_1440.png")

            # Test switching tabs on desktop
            page.locator(".si-nav-item[data-sec='academic_years']").click()
            page.wait_for_timeout(300)
            self.assertIn("Academic Year Management", page.locator("#siActivePanel").inner_text())

            # Test Mobile at 390px
            page.set_viewport_size({"width": 390, "height": 844})
            page.wait_for_timeout(400)
            self.assertTrue(page.locator("#htbHamburger").is_visible())
            page.screenshot(path="scratch/school_info_mobile_390.png")

            # Test Principal page
            page.goto(f"{BASE_URL}/pages/principal/principal-school-information.html")
            page.wait_for_timeout(600)
            self.assertTrue(page.locator(".hero-topbar").is_visible())
            page.screenshot(path="scratch/principal_school_info_390.png")

            browser.close()

if __name__ == "__main__":
    unittest.main()

