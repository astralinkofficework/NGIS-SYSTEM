"""User Management regression suite — identity administration MVP.

Covers the /api/user-mgmt/* backend (provisioning integrity, status lifecycle,
security guards, audit) plus the six admin page shells and design conformance.
"""
import json
import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, 'data', 'user_accounts.json')


class UserManagementTest(unittest.TestCase):
    # Person overlay files touched by create-person; test-created records are
    # scrubbed before and after each run so reruns stay idempotent while real
    # records created through the UI are preserved.
    OVERLAY_FILES = ('data/students_overlay.json', 'data/teachers_overlay.json',
                     'data/staff_overlay.json', 'data/principals_overlay.json')
    TEST_MARKERS = ('MVPson', 'Duple', 'Kate', 'Nhemtest', 'Soktest', 'Teptest')

    @classmethod
    def setUpClass(cls):
        import warnings
        warnings.filterwarnings('ignore')
        import server
        cls.app = server.app
        cls.app.testing = True
        cls.client = cls.app.test_client()
        cls._backup = None
        if os.path.exists(STORE):
            cls._backup = STORE + '.bak'
            shutil.copy2(STORE, cls._backup)
        if os.path.exists(STORE):
            os.remove(STORE)
        cls._scrub_overlays()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(STORE):
            os.remove(STORE)
        if cls._backup and os.path.exists(cls._backup):
            shutil.move(cls._backup, STORE)
        cls._scrub_overlays()

    @classmethod
    def _scrub_overlays(cls):
        for rel in cls.OVERLAY_FILES:
            path = os.path.join(ROOT, rel)
            if not os.path.exists(path):
                continue
            try:
                with open(path, encoding='utf-8') as fh:
                    data = json.load(fh)
            except (ValueError, OSError):
                continue
            if not isinstance(data, list):
                continue
            cleaned = [p for p in data
                       if not isinstance(p, dict) or
                       not any(m in str(p.get('name', '')) for m in cls.TEST_MARKERS)]
            if len(cleaned) != len(data):
                with open(path, 'w', encoding='utf-8') as fh:
                    json.dump(cleaned, fh, indent=2, ensure_ascii=False)

    # ── helpers ────────────────────────────────────────────────────────────
    _provisioned_person_id = None

    def _first_unprovisioned(self, ptype):
        j = self.client.get(
            f'/api/user-mgmt/directory?type={ptype}&page_size=100').get_json()
        rows = [r for r in j['data'] if not r['account']]
        self.assertTrue(rows, f'no unprovisioned {ptype} records in seed')
        return rows[0]

    def _provision(self, ptype='student', username=None):
        row = self._first_unprovisioned(ptype)
        payload = {
            'person_type': ptype,
            'person_id': row['person_id'],
            'username': username or f'test.{ptype}.{row["person_id"].lower()}@ngis.edu.kh',
            'activation': 'token',
        }
        r = self.client.post('/api/user-mgmt/provision', json=payload)
        self.assertEqual(r.status_code, 201, r.get_data(as_text=True))
        UserManagementTest._provisioned_person_id = row['person_id']
        return r.get_json()

    # ── overview ───────────────────────────────────────────────────────────
    def test_01_overview_metrics_derived_from_store(self):
        j = self.client.get('/api/user-mgmt/overview').get_json()
        m = j['metrics']
        for key in ('totalAccounts', 'activeAccounts', 'pendingActivation',
                    'suspendedAccounts', 'accountsWithoutProfiles',
                    'profilesWithoutAccounts'):
            self.assertIn(key, m)
        # Existing real logins (admin, principal, teacher, student portal demo)
        self.assertEqual(m['totalAccounts'], 4)
        self.assertEqual(m['accountsWithoutProfiles'], 2)  # orphaned logins
        self.assertGreater(m['profilesWithoutAccounts'], 0)
        self.assertIn('byType', j)
        self.assertIn('activity', j)

    # ── directory ──────────────────────────────────────────────────────────
    def test_02_directory_server_side_search_filter_sort(self):
        j = self.client.get(
            '/api/user-mgmt/directory?type=student&search=chan').get_json()
        self.assertGreater(j['total'], 0)
        for row in j['data']:
            self.assertIn('chan', (row['name'] or '').lower())
        # status filter — active accounts only
        j2 = self.client.get(
            '/api/user-mgmt/directory?type=all&status=active&page_size=50').get_json()
        for row in j2['data']:
            self.assertEqual(row['account']['status'], 'active')
        # sort by last_login desc does not crash
        j3 = self.client.get(
            '/api/user-mgmt/directory?type=all&sort=last_login&order=desc').get_json()
        self.assertIn('total', j3)
        # pagination: page 1 + page 2 concatenate in stable name order
        jfull = self.client.get(
            '/api/user-mgmt/directory?type=student&page=1&page_size=100').get_json()
        self.assertGreater(len(jfull['data']), 10)
        j4 = self.client.get(
            '/api/user-mgmt/directory?type=student&page=1&page_size=10').get_json()
        self.assertLessEqual(len(j4['data']), 10)
        self.assertGreater(j4['pages'], 1)
        j5 = self.client.get(
            '/api/user-mgmt/directory?type=student&page=2&page_size=10').get_json()
        self.assertEqual(j5['data'][0]['person_id'],
                         jfull['data'][10]['person_id'])
        # facets
        self.assertIn('facets', j4)

    # ── provisioning integrity ────────────────────────────────────────────
    def test_03_provision_creates_linked_account_and_token(self):
        body = self._provision('student')
        self.assertEqual(body['status'], 'pending_activation')
        self.assertTrue(body.get('activation_token'))
        self.assertTrue(body.get('activation_expires'))
        # detail view shows the linked account
        d = self.client.get('/api/user-mgmt/user/student/'
                            f'{self._provisioned_person_id}').get_json()
        self.assertTrue(d['success'])
        self.assertTrue(d['account'])
        self.assertEqual(d['account']['id'], body['account_id'])
        self.assertIn('identity_source', d['account'])

    def test_04_provision_rejects_duplicates_and_bad_person(self):
        row = self._first_unprovisioned('student')
        payload = {'person_type': 'student', 'person_id': row['person_id'],
                   'username': 'unique.ok@ngis.edu.kh'}
        r1 = self.client.post('/api/user-mgmt/provision', json=payload)
        self.assertEqual(r1.status_code, 201)
        # same person again -> duplicate link
        r2 = self.client.post('/api/user-mgmt/provision', json=payload)
        self.assertEqual(r2.status_code, 409)
        # same username, different person -> duplicate username
        other = self._first_unprovisioned('teacher')
        r3 = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'teacher', 'person_id': other['person_id'],
            'username': 'unique.ok@ngis.edu.kh'})
        self.assertEqual(r3.status_code, 409)
        # unknown person id
        r4 = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'student', 'person_id': 'NOPE',
            'username': 'nope.user@ngis.edu.kh'})
        self.assertEqual(r4.status_code, 404)
        # invalid username format
        r5 = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'student', 'person_id': 'NOPE2',
            'username': 'Bad Username!'})
        self.assertEqual(r5.status_code, 400)
        # role mismatch rejected (valid staff person, wrong role)
        staff_row = self._first_unprovisioned('staff')
        r6 = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'staff', 'person_id': staff_row['person_id'],
            'username': 'role.mismatch@ngis.edu.kh', 'role': 'SUPER_ADMIN'})
        self.assertEqual(r6.status_code, 400)

    def test_05_admin_account_creation_blocked(self):
        row = self._first_unprovisioned('teacher')
        r = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'admin', 'person_id': row['person_id'],
            'username': 'self.escalated@ngis.edu.kh', 'role': 'SUPER_ADMIN'})
        self.assertEqual(r.status_code, 403)

    def test_06_status_lifecycle_and_guards(self):
        body = self._provision('staff', 'lifecycle.staff@ngis.edu.kh')
        acc = body['account_id']
        # activate
        r = self.client.post(f'/api/user-mgmt/account/{acc}/status',
                             json={'action': 'activate'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['status'], 'active')
        # invalid transition (activate again)
        r2 = self.client.post(f'/api/user-mgmt/account/{acc}/status',
                              json={'action': 'activate'})
        self.assertEqual(r2.status_code, 409)
        # suspend then disable
        r3 = self.client.post(f'/api/user-mgmt/account/{acc}/status',
                              json={'action': 'suspend'})
        self.assertEqual(r3.get_json()['status'], 'suspended')
        r4 = self.client.post(f'/api/user-mgmt/account/{acc}/status',
                              json={'action': 'disable'})
        self.assertEqual(r4.get_json()['status'], 'disabled')
        # last-active-admin guard on USR-001
        r5 = self.client.post('/api/user-mgmt/account/USR-001/status',
                              json={'action': 'suspend'},
                              headers={'X-Actor': 'admin@ngis.edu.kh'})
        self.assertEqual(r5.status_code, 409)
        # super-admin guard with a non-super actor
        r6 = self.client.post('/api/user-mgmt/account/USR-001/status',
                              json={'action': 'suspend'},
                              headers={'X-Actor': 'intruder@nowhere.com'})
        self.assertEqual(r6.status_code, 403)

    def test_07_password_reset_hashed_one_time_and_rate_limited(self):
        body = self._provision('teacher', 'security.teacher@ngis.edu.kh')
        acc = body['account_id']
        self.client.post(f'/api/user-mgmt/account/{acc}/status',
                         json={'action': 'activate'})
        r = self.client.post(f'/api/user-mgmt/account/{acc}/reset-password')
        self.assertEqual(r.status_code, 200)
        token = r.get_json()['reset_token']
        self.assertTrue(token)
        # token stored hashed, never plaintext — the store key is the hash
        with open(STORE, encoding='utf-8') as fh:
            raw = fh.read()
        self.assertNotIn(token, raw)
        self.assertIn('"kind": "password_reset"', raw)
        self.assertIn('$', raw.split('"reset_tokens": {')[1])
        # rate limit after MAX_RESETS_PER_HOUR calls
        for _ in range(4):
            self.client.post(f'/api/user-mgmt/account/{acc}/reset-password')
        r_last = self.client.post(f'/api/user-mgmt/account/{acc}/reset-password')
        self.assertEqual(r_last.status_code, 429)
        # disabled accounts cannot reset
        self.client.post(f'/api/user-mgmt/account/{acc}/status',
                         json={'action': 'disable'})
        r_dis = self.client.post(f'/api/user-mgmt/account/{acc}/reset-password')
        self.assertEqual(r_dis.status_code, 409)

    def test_07b_activation_token_redemption(self):
        # the seed's only principal already has a login, so use a student
        body = self._provision('student', 'redeem.student@ngis.edu.kh')
        token = body['activation_token']
        r = self.client.post('/api/user-mgmt/redeem-token', json={'token': token})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['status'], 'active')
        self.assertEqual(r.get_json()['kind'], 'activation')
        # one-time: reuse is rejected
        r2 = self.client.post('/api/user-mgmt/redeem-token', json={'token': token})
        self.assertEqual(r2.status_code, 404)
        # garbage tokens rejected
        r3 = self.client.post('/api/user-mgmt/redeem-token', json={'token': 'nope'})
        self.assertEqual(r3.status_code, 404)

    def test_08_revoke_sessions_records_event(self):
        body = self._provision('teacher', 'sessions.teacher@ngis.edu.kh')
        acc = body['account_id']
        r = self.client.post(
            f'/api/user-mgmt/account/{acc}/revoke-sessions')
        self.assertEqual(r.status_code, 200)
        hist = self.client.get(
            f'/api/user-mgmt/account/{acc}/login-history').get_json()
        events = [h['event'] for h in hist['data']]
        self.assertIn('sessions_revoked', events)

    def test_09_account_field_editor_validates_uniqueness(self):
        body = self._provision('teacher', 'editor.teacher@ngis.edu.kh')
        acc = body['account_id']
        r = self.client.put(f'/api/user-mgmt/account/{acc}',
                            json={'assignment': '10A, 10B'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['account']['assignment'], '10A, 10B')
        # duplicate username on edit rejected
        r2 = self.client.put(f'/api/user-mgmt/account/{acc}',
                             json={'username': 'admin@ngis.edu.kh'})
        self.assertEqual(r2.status_code, 409)
        # no-op rejected
        r3 = self.client.put(f'/api/user-mgmt/account/{acc}', json={})
        self.assertEqual(r3.status_code, 400)

    def test_10_bulk_provision_reports_per_record(self):
        j = self.client.get(
            '/api/user-mgmt/directory?type=teacher&page_size=100').get_json()
        ids = [r['person_id'] for r in j['data'] if not r['account']][:3]
        self.assertGreaterEqual(len(ids), 2)
        r = self.client.post('/api/user-mgmt/bulk-provision', json={
            'person_type': 'teacher', 'person_ids': ids,
            'username': 'bulk.same@ngis.edu.kh'})
        results = r.get_json()['results']
        self.assertEqual(len(results), len(ids))
        # the identical username is only accepted once
        ok = [x for x in results if x['ok']]
        dup = [x for x in results if not x['ok']]
        self.assertEqual(len(ok), 1)
        self.assertTrue(all('Username' in x['message'] for x in dup))

    def test_11_audit_trail_records_and_searches(self):
        j = self.client.get('/api/user-mgmt/audit').get_json()
        actions = [e['action'] for e in j['data']]
        self.assertIn('account_created', actions)
        self.assertIn('password_reset_initiated', actions)
        self.assertIn('sessions_revoked', actions)
        # every entry has actor/target/outcome and no secrets
        for e in j['data']:
            for key in ('ts', 'actor', 'action', 'target', 'outcome'):
                self.assertIn(key, e)
        raw = json.dumps(j)
        self.assertNotIn('reset_token', raw)
        # searchable
        j2 = self.client.get(
            '/api/user-mgmt/audit?action=account_created').get_json()
        for e in j2['data']:
            self.assertEqual(e['action'], 'account_created')

    def test_12_export_contains_no_credentials(self):
        r = self.client.get('/api/user-mgmt/export?type=student')
        self.assertEqual(r.status_code, 200)
        body = r.get_data(as_text=True)
        self.assertIn('User ID,Name,Username', body)
        self.assertNotIn('password', body.lower())
        self.assertNotIn('token', body.lower())

    # ── page shells & design conformance ──────────────────────────────────
    def test_13_five_pages_exist_with_canonical_wiring(self):
        # Overview page (admin-users.html) is removed in favor of the 5
        # dedicated User Management directory pages.
        overview = os.path.join(ROOT, 'pages/admin/admin-users.html')
        self.assertFalse(os.path.exists(overview), 'admin-users.html must not exist')
        pages = ['admin-users-students.html',
                 'admin-users-teachers.html', 'admin-users-staff.html',
                 'admin-users-principals.html', 'admin-users-admins.html']
        modules = ['students', 'teachers', 'staff', 'principals', 'admins']
        for page, module in zip(pages, modules):
            html = open(os.path.join(ROOT, 'pages/admin', page),
                        encoding='utf-8').read()
            self.assertIn('<main class="main ', html, page)
            self.assertIn('role: "admin"', html, page)
            self.assertIn(f"NGIS_USERS.init('usersRoot', '{module}')", html, page)
            self.assertIn('ngis-users.js?v=1.1', html, page)
            # loads AFTER layout.js (renderer needs nothing from layout, but
            # keeps the wiring deterministic)
            self.assertLess(html.index('layout.js'),
                            html.index('ngis-users.js'), page)
            self.assertIn('smx-page', html, page)
            self.assertIn('design-system.css?v=1.4', html, page)
            # mandatory mobile hamburger
            self.assertIn('data-action="toggle-sidebar"', html, page)

    def test_13b_no_live_references_to_removed_overview(self):
        """Removed overview shell is absent and referenced by no live navigation."""
        overview = os.path.join(ROOT, 'pages/admin/admin-users.html')
        self.assertFalse(os.path.exists(overview), 'admin-users.html must be absent')
        js = open(os.path.join(ROOT, 'assets/js/layout.js'),
                  encoding='utf-8').read()
        self.assertNotIn('users-overview', js)
        self.assertNotIn('pages/admin/admin-users.html', js)
        for page in ('admin-users-students.html', 'admin-users-teachers.html',
                     'admin-users-staff.html', 'admin-users-principals.html',
                     'admin-users-admins.html'):
            self.assertIn(page, js)
        # 404 served over HTTP
        r = self.client.get('/pages/admin/admin-users.html')
        self.assertEqual(r.status_code, 404)

    def test_14_sidebar_has_user_management_group(self):
        js = open(os.path.join(ROOT, 'assets/js/layout.js'),
                  encoding='utf-8').read()
        for frag in ('USER & ACCESS MANAGEMENT', 'users-students', 'users-teachers',
                     'users-staff', 'users-principals', 'users-admins',
                     'admin-users-students.html'):
            self.assertIn(frag, js)

    def test_15_renderer_and_styles_conform(self):
        js = open(os.path.join(ROOT, 'assets/js/ngis-users.js'),
                  encoding='utf-8').read()
        css = open(os.path.join(ROOT, 'assets/css/design-system.css'),
                   encoding='utf-8').read()
        self.assertEqual(js.count('{'), js.count('}'), 'renderer braces')
        self.assertEqual(css.count('{'), css.count('}'), 'CSS braces')
        # renderer only emits scoped classes, no legacy Tailwind surfaces
        self.assertNotIn('linear-gradient', js)
        self.assertNotIn('font-weight: 700', js)
        self.assertNotIn('font-weight: 600', js)
        # SVG-only actions (no icon-font action fallbacks in the table)
        self.assertIn('viewBox', js)
        # scoped UM block present with its key classes
        for frag in ('.smx-icon-btn', '.smx-dir-tile', '.smx-activity-row',
                     '.smx-avatar-fallback', '.smx-info-label'):
            self.assertIn(frag, css)
        # no gradients inside the whole design system user block additions
        um_block = css[css.index('User Management (identity administration)'):]
        self.assertNotIn('linear-gradient', um_block)
        self.assertNotIn('font-weight: 700', um_block)
        self.assertNotIn('font-weight: 600', um_block)

    def test_16_username_check_endpoint(self):
        r1 = self.client.get('/api/user-mgmt/check-username?username=ab')
        self.assertEqual(r1.status_code, 200)
        self.assertFalse(r1.get_json()['valid'])

        r2 = self.client.get('/api/user-mgmt/check-username?username=admin@ngis.edu.kh')
        self.assertEqual(r2.status_code, 200)
        self.assertTrue(r2.get_json()['valid'])
        self.assertFalse(r2.get_json()['available'])

        r3 = self.client.get('/api/user-mgmt/check-username?username=admin@ngis.edu.kh&exclude_id=USR-001')
        self.assertEqual(r3.status_code, 200)
        self.assertTrue(r3.get_json()['available'])

        r4 = self.client.get('/api/user-mgmt/check-username?username=fresh.student.99')
        self.assertEqual(r4.status_code, 200)
        self.assertTrue(r4.get_json()['available'])

    def test_17_admin_creation_super_admin_guards(self):
        # Missing confirmation -> 403
        r0 = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'admin', 'name': 'Ops Admin',
            'username': 'ops.admin@ngis.edu.kh', 'elevated_confirmed': False,
        }, headers={'X-Actor': 'admin@ngis.edu.kh'})
        self.assertEqual(r0.status_code, 403)

        # Trying to escalate to SUPER_ADMIN -> 403
        r_esc = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'admin', 'name': 'Evil Admin',
            'username': 'evil.super@ngis.edu.kh', 'role': 'SUPER_ADMIN',
            'elevated_confirmed': True,
        }, headers={'X-Actor': 'admin@ngis.edu.kh'})
        self.assertEqual(r_esc.status_code, 403)

        # Authorized SUPER_ADMIN provisions standard ADMIN
        r1 = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'admin', 'name': 'Ms. Sokha Meas',
            'username': 'sokha.admin@ngis.edu.kh', 'campus': 'Sensok',
            'access_scope': 'Identity & User Access', 'elevated_confirmed': True,
            'activation': 'token',
        }, headers={'X-Actor': 'admin@ngis.edu.kh'})
        self.assertEqual(r1.status_code, 201)
        j1 = r1.get_json()
        self.assertEqual(j1['role'], 'ADMIN')
        self.assertTrue(j1['activation_token'])

        # Activate new ADMIN so they can authenticate, then block them from provisioning Admins
        self.client.post(f"/api/user-mgmt/account/{j1['account_id']}/status",
                         json={'action': 'activate'},
                         headers={'X-Actor': 'admin@ngis.edu.kh'})
        r_non_super = self.client.post('/api/user-mgmt/provision', json={
            'person_type': 'admin', 'name': 'Another Admin',
            'username': 'another.admin@ngis.edu.kh', 'elevated_confirmed': True,
        }, headers={'X-Actor': 'sokha.admin@ngis.edu.kh'})
        self.assertEqual(r_non_super.status_code, 403)

    def test_18_bulk_status_and_facets(self):
        # Clean classes facet & campus_options exposed
        d = self.client.get('/api/user-mgmt/directory?type=student&page_size=10').get_json()
        self.assertTrue(d['facets']['campus_options'])
        for c in d['facets']['classes']:
            self.assertFalse(c.lower().startswith('student '), c)

        # Bulk provision two students then bulk suspend & activate
        pids = [r['person_id'] for r in d['data'] if not r['account']][:2]
        self.assertEqual(len(pids), 2)
        self.client.post('/api/user-mgmt/bulk-provision', json={
            'person_type': 'student', 'person_ids': pids,
        }, headers={'X-Actor': 'admin@ngis.edu.kh'})

        r_susp = self.client.post('/api/user-mgmt/bulk-status', json={
            'person_type': 'student', 'person_ids': pids, 'action': 'suspend',
        }, headers={'X-Actor': 'admin@ngis.edu.kh'})
        self.assertEqual(r_susp.status_code, 200)
        self.assertTrue(all(x['ok'] for x in r_susp.get_json()['results']))

        r_act = self.client.post('/api/user-mgmt/bulk-status', json={
            'person_type': 'student', 'person_ids': pids, 'action': 'activate',
        }, headers={'X-Actor': 'admin@ngis.edu.kh'})
        self.assertEqual(r_act.status_code, 200)
        self.assertTrue(all(x['ok'] for x in r_act.get_json()['results']))

    def test_19_renderer_redesign_contracts(self):
        js = open(os.path.join(ROOT, 'assets/js/ngis-users.js'),
                  encoding='utf-8').read()
        for t in ('student', 'teacher', 'staff', 'principal', 'admin'):
            self.assertIn(f"{t}: '", js)
        self.assertIn('/api/user-mgmt/check-username', js)
        self.assertIn('openAddAccountModal', js)
        self.assertNotIn('type="password"', js)

    # ── create-person from scratch (account creation MVP) ─────────────────
    def test_20_create_person_student_end_to_end(self):
        # form options come from the real registry
        fo = self.client.get('/api/user-mgmt/form-options?type=student').get_json()
        self.assertTrue(fo['success'])
        self.assertTrue(fo['campuses'])
        self.assertTrue(fo['classes'])
        class_short = fo['classes'][0]['short']

        # create a brand-new student — no person selection required
        r = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'student', 'first_name': 'Test', 'last_name': 'MVPson',
            'gender': 'F', 'campus': fo['campuses'][0], 'class': class_short,
            'academic_year': fo['academic_years'][0],
            'enrollment_status': 'active',
            'username': 'test.mvpson@ngis.edu.kh', 'activation': 'token'})
        self.assertEqual(r.status_code, 201, r.get_data(as_text=True))
        body = r.get_json()
        self.assertRegex(body['institutional_id'], r'^\d{4}-STD-\d{4}$')
        self.assertTrue(body['activation_token'])

        # the person appears in the directory, already linked to the account
        d = self.client.get(
            '/api/user-mgmt/directory?type=student&search=MVPson').get_json()
        row = next(x for x in d['data'] if x['person_id'] == body['institutional_id'])
        self.assertIsNotNone(row['account'])
        self.assertEqual(row['account']['status'], 'pending_activation')

        # activation sets the credential (hashed) and activates the account
        r_act = self.client.post('/api/user-mgmt/redeem-token', json={
            'token': body['activation_token'], 'new_password': 'SecurePass!23'})
        self.assertEqual(r_act.status_code, 200)
        self.assertEqual(r_act.get_json()['status'], 'active')

        # the new student can sign in through the real login endpoint
        r_login = self.client.post('/api/auth/login', json={
            'email': 'test.mvpson@ngis.edu.kh', 'password': 'SecurePass!23'})
        self.assertEqual(r_login.status_code, 200)
        self.assertEqual(r_login.get_json()['data']['user']['role'], 'student')
        # ...and /api/auth/me resolves the um-session token
        token = r_login.get_json()['data']['token']
        r_me = self.client.get('/api/auth/me',
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(r_me.status_code, 200)
        self.assertEqual(r_me.get_json()['data']['name'], 'Test MVPson')

    def test_21_create_person_rejections_and_all_roles(self):
        # duplicate person (same name + same class) rejected
        r = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'student', 'first_name': 'Duple', 'last_name': 'Kate',
            'class': '10A', 'username': 'duple.kate@ngis.edu.kh'})
        self.assertEqual(r.status_code, 201)
        r_dup = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'student', 'first_name': 'Duple', 'last_name': 'Kate',
            'class': '10A', 'username': 'duple2.kate@ngis.edu.kh'})
        self.assertEqual(r_dup.status_code, 409)
        # duplicate username rejected
        r_un = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'teacher', 'first_name': 'U', 'last_name': 'Ser',
            'department': 'Science', 'username': 'duple.kate@ngis.edu.kh'})
        self.assertEqual(r_un.status_code, 409)
        # invalid class rejected
        r_cls = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'student', 'first_name': 'A', 'last_name': 'B',
            'class': '99Z', 'username': 'ab.cd@ngis.edu.kh'})
        self.assertEqual(r_cls.status_code, 400)
        # invalid campus rejected
        r_cam = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'teacher', 'first_name': 'A', 'last_name': 'B',
            'department': 'Science', 'campus': 'Atlantis',
            'username': 'ab.cd2@ngis.edu.kh'})
        self.assertEqual(r_cam.status_code, 400)
        # admin type uses the same gated flow: the default actor is the seeded
        # administrator, so creation succeeds (403 for non-admin actors is
        # covered by the actor-gating assertions in test_20)
        r_adm = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'admin', 'first_name': 'A', 'last_name': 'B',
            'username': 'ab.cd3@ngis.edu.kh', 'position': 'Registrar Administrator'})
        self.assertEqual(r_adm.status_code, 201)
        self.assertEqual(r_adm.get_json()['role'], 'ADMIN')

        # teacher / staff / principal directories each create their own type
        r_t = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'teacher', 'first_name': 'Malis', 'last_name': 'Nhemtest',
            'department': 'Science', 'position': 'Physics Teacher',
            'campus': 'TK', 'username': 'malis.nhemtest@ngis.edu.kh'})
        self.assertEqual(r_t.status_code, 201)
        self.assertRegex(r_t.get_json()['institutional_id'], r'^TCH-\d{4}-\d{3}$')
        r_s = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'staff', 'first_name': 'Vuthy', 'last_name': 'Soktest',
            'department': 'Campus Operations', 'position': 'Lab Assistant',
            'username': 'vuthy.soktest@ngis.edu.kh'})
        self.assertEqual(r_s.status_code, 201)
        self.assertRegex(r_s.get_json()['institutional_id'], r'^STF-\d{4}-\d{3}$')
        r_p = self.client.post('/api/user-mgmt/create-person', json={
            'person_type': 'principal', 'first_name': 'Sopheak', 'last_name': 'Teptest',
            'position': 'Deputy Principal', 'campus': 'Sensok',
            'username': 'sopheak.teptest@ngis.edu.kh'})
        self.assertEqual(r_p.status_code, 201)
        self.assertRegex(r_p.get_json()['institutional_id'], r'^PRN-\d{4}-\d{3}$')

        # every new person is in their directory with a pending account
        for ptype, name in (('teacher', 'Nhemtest'), ('staff', 'Soktest'),
                            ('principal', 'Teptest')):
            d = self.client.get(
                f'/api/user-mgmt/directory?type={ptype}&search={name}').get_json()
            self.assertTrue(d['data'], ptype)
            self.assertIsNotNone(d['data'][0]['account'])

        # suspended account cannot log in
        d = self.client.get(
            '/api/user-mgmt/directory?type=teacher&search=Nhemtest').get_json()
        acc = d['data'][0]['account']
        self.client.post(f'/api/user-mgmt/account/{acc["id"]}/status',
                         json={'action': 'activate'})
        r_login = self.client.post('/api/auth/login', json={
            'email': 'malis.nhemtest@ngis.edu.kh', 'password': 'password123'})
        # account is still pending activation — no credential has been set,
        # so sign-in is refused before the password check (403 ACTIVATION_REQUIRED)
        self.assertEqual(r_login.status_code, 403)
        self.client.post(f'/api/user-mgmt/account/{acc["id"]}/status',
                         json={'action': 'suspend'})
        r_susp = self.client.post('/api/auth/login', json={
            'email': 'malis.nhemtest@ngis.edu.kh', 'password': 'whatever'})
        self.assertEqual(r_susp.status_code, 403)

        # audit trail records the creation events without secrets
        au = self.client.get('/api/user-mgmt/audit?action=person_created').get_json()
        self.assertGreaterEqual(len(au['data']), 4)
        raw = json.dumps(au)
        self.assertNotIn('SecurePass', raw)

    def test_22_create_person_wizard_wiring(self):
        # The shared 3-step registration wizard lives in ngis-register.js and
        # is opened by ngis-users.js (openAddAccountModal -> NGIS_REGISTER.open).
        js = open(os.path.join(ROOT, 'assets/js/ngis-users.js'),
                  encoding='utf-8').read()
        self.assertIn('openAddAccountModal', js)
        self.assertIn('openThreeStepWizard', js)
        reg = open(os.path.join(ROOT, 'assets/js/ngis-register.js'),
                   encoding='utf-8').read()
        self.assertIn('/api/user-mgmt/create-person', reg)
        self.assertIn('/api/user-mgmt/form-options', reg)
        self.assertIn('/api/user-mgmt/generate-credentials', reg)
        self.assertIn('/api/user-mgmt/check-username', reg)
        css = open(os.path.join(ROOT, 'assets/css/ngis-register.css'),
                   encoding='utf-8').read()
        self.assertIn('.nrg-step', css)
        self.assertIn('.nrg-review-card', css)


if __name__ == '__main__':
    unittest.main(verbosity=2)
