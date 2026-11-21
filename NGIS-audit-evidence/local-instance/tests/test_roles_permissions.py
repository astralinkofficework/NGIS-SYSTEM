"""NGIS — Roles & Access Control / User Access & Visibility regression suite.

Covers the whole stack built for the User Access, Portal Visibility &
Permission Control extension:

  1. API contract           registry, roles, overview, audit, pages, users,
                            compare, effective, overrides, preview
  2. Authorization          read guard, anonymous/low-privilege writes, cookie
                            identity, SUPER_ADMIN protection, self-modification,
                            privilege-chain restrictions
  3. Override validation    portal-qualified keys, ambiguous bare ids, unknown
                            modules/actions, non-persisting preview, clearing
  4. Resolution/enforcement tri-state precedence, cross-portal isolation,
                            hidden != denied, sidebar access document, and the
                            server-side direct-URL before_request gate
  5. Frontend wiring        page, renderer, scoped CSS, nav entry, layout copies

The suite snapshots data/roles_permissions.json before running and restores it
after every test, so mutating endpoint coverage never leaves audit entries or
access overrides behind in the demo data.
"""
import json
import os
import unittest
import urllib.parse
from unittest import mock

import roles_permissions_api as rp
from server import app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = rp.STORE_PATH

ADMIN = 'admin@ngis.edu.kh'          # SUPER_ADMIN, active
STUDENT = 'student@ngis.edu.kh'      # STUDENT, active
TEACHER = 'teacher@ngis.edu.kh'      # TEACHER, active
TARGET = STUDENT
TEMP_ADMIN = 'temp.regression.admin@ngis.edu.kh'


def hdr(actor):
    return {'X-Actor': actor} if actor else {}


def store_snapshot():
    if os.path.exists(STORE):
        with open(STORE, 'rb') as fh:
            return fh.read()
    return None


def restore_store(snapshot):
    if snapshot is None:
        if os.path.exists(STORE):
            os.remove(STORE)
    else:
        with open(STORE, 'wb') as fh:
            fh.write(snapshot)


class RolesPermissionsTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = store_snapshot()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        restore_store(cls.snapshot)

    def setUp(self):
        # Each test starts from the pristine demo store.
        restore_store(self.snapshot)
        self.client = app.test_client()

    def get(self, path, actor=None, **kw):
        return self.client.get(path, headers=hdr(actor), **kw)

    def post(self, path, body=None, actor=None):
        return self.client.post(path, json=body or {}, headers=hdr(actor))

    def put_overrides(self, username, overrides, actor=ADMIN, client=None):
        c = client or self.client
        return c.put('/api/roles-mgmt/overrides/' + username,
                     json=overrides, headers=hdr(actor))

    def cookie_client(self, actor):
        # Real browsers receive the value written by auth.js, which uses
        # encodeURIComponent(); '@' therefore arrives as '%40'. Exercises the
        # server-side decode rather than an idealized raw cookie value.
        c = app.test_client()
        c.set_cookie('ngis_actor', urllib.parse.quote(actor, safe=''))
        return c

    def student_page(self, nav_id):
        doc = self.get('/api/roles-mgmt/pages', ADMIN).get_json()
        return next(p for p in doc['portals']['student'] if p['id'] == nav_id)

    @staticmethod
    def document(client, path, headers=None):
        """Fetch an HTML document and close its file wrapper. Flask streams
        static pages from disk; leaving the response open emits ResourceWarning
        noise during the test run."""
        r = client.get(path, headers=headers or {})
        try:
            return r.status_code, r.headers.get('Location', '')
        finally:
            r.close()


# ── 1. API contract ────────────────────────────────────────────────────────

class TestApiContract(RolesPermissionsTestBase):

    def test_registry_contract(self):
        r = self.get('/api/roles-mgmt/registry', ADMIN)
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        self.assertIs(d['success'], True)
        self.assertIn('SUPER_ADMIN', d['core_roles'])
        self.assertIn('view', d['actions'])
        self.assertIn('manage', d['actions'])
        self.assertTrue(d['categories'])
        self.assertIn('roles-access', str(d['categories']))
        self.assertIn('campuses', d['scope_options'])

    def test_roles_contract_and_protected_core_roles(self):
        d = self.get('/api/roles-mgmt/roles', ADMIN).get_json()
        self.assertIs(d['success'], True)
        self.assertEqual(len(d['core_roles']), 6)
        self.assertTrue(all(r['protected'] for r in d['core_roles']))
        self.assertTrue(all(r['status'] == 'active' for r in d['core_roles']))
        sup = next(r for r in d['core_roles'] if r['id'] == 'SUPER_ADMIN')
        self.assertIs(sup['sensitive'], True)
        self.assertIsInstance(d['custom_roles'], list)

    def test_overview_and_audit_contract(self):
        overview = self.get('/api/roles-mgmt/overview', ADMIN).get_json()
        self.assertIs(overview['success'], True)
        for key in ('activeRoles', 'customRoles', 'totalAssignments',
                    'highPrivilegeRoles', 'unassignedRoles'):
            self.assertIn(key, overview['metrics'])
        audit = self.get('/api/roles-mgmt/audit', ADMIN).get_json()
        self.assertIs(audit['success'], True)
        self.assertEqual(audit['total'], len(audit['data']))
        for row in audit['data']:
            self.assertIn('id', row)
            self.assertIn('actor', row)
            self.assertIn('action', row)
            self.assertNotIn('password', row)
            self.assertNotIn('password_hash', row)

    def test_pages_inventory_uses_portal_qualified_keys(self):
        d = self.get('/api/roles-mgmt/pages', ADMIN).get_json()
        self.assertIs(d['success'], True)
        self.assertGreater(d['total'], 50)
        all_pages = [p for group in d['portals'].values() for p in group]
        self.assertEqual(len(all_pages), d['total'])
        keys = [p['key'] for p in all_pages]
        self.assertEqual(len(keys), len(set(keys)), 'page keys must be unique')
        for p in all_pages:
            self.assertTrue(p['key'].startswith(p['portal'] + ':'), p['key'])
            self.assertTrue(p['file'].endswith('.html'), p['file'])
        # "dashboard" exists in several portals; qualification keeps them apart.
        self.assertIn('admin:dashboard', keys)
        self.assertIn('student:dashboard', keys)
        self.assertIn('teacher:dashboard', keys)
        self.assertIn('admin:roles-permissions', keys)
        self.assertIn('admin:verify-teacher', keys)

    def test_users_directory_flags_protected_super_admin(self):
        d = self.get('/api/roles-mgmt/users', ADMIN).get_json()
        self.assertIs(d['success'], True)
        self.assertEqual(d['total'], len(d['users']))
        self.assertGreaterEqual(d['total'], 4)
        sup = next(u for u in d['users'] if u['username'] == ADMIN)
        self.assertIs(sup['protected'], True)
        self.assertIsInstance(sup['has_overrides'], bool)
        for u in d['users']:
            self.assertIn('username', u)
            self.assertIn('role', u)
            self.assertIn('status', u)

    def test_effective_permissions_are_server_resolved(self):
        d = self.get('/api/roles-mgmt/effective/' + STUDENT, ADMIN).get_json()
        self.assertIs(d['success'], True)
        self.assertEqual(d['core_role'], 'STUDENT')
        self.assertIs(d['protected'], False)
        self.assertEqual(d['portals']['student'], 'allow')
        self.assertEqual(d['portals']['admin'], 'deny')
        self.assertIn('admin:dashboard', d['denied_keys'])
        self.assertNotIn('student:dashboard', d['denied_keys'])
        self.assertEqual(d['hidden_keys'], [])
        inventory = self.get('/api/roles-mgmt/pages', ADMIN).get_json()
        self.assertEqual(len(d['pages']), inventory['total'])
        own = next(p for p in d['pages'] if p['key'] == 'student:dashboard')
        self.assertIs(own['allowed'], True)
        self.assertIs(own['visible'], True)

    def test_compare_and_overrides_contract(self):
        d = self.get('/api/roles-mgmt/compare?a=ADMIN&b=TEACHER', ADMIN).get_json()
        self.assertIs(d['success'], True)
        self.assertEqual(d['a']['id'], 'ADMIN')
        self.assertEqual(d['b']['id'], 'TEACHER')
        self.assertTrue(d['modules'])

        o = self.get('/api/roles-mgmt/overrides/' + TARGET, ADMIN).get_json()
        self.assertIs(o['success'], True)
        self.assertEqual(o['account']['username'], TARGET)
        self.assertIn('pages', o['effective'])
        self.assertIn('permissions', o['effective'])

    def test_missing_account_returns_404(self):
        self.assertEqual(
            self.get('/api/roles-mgmt/overrides/not.a.user@ngis.edu.kh', ADMIN).status_code,
            404)
        self.assertEqual(
            self.post('/api/roles-mgmt/preview',
                      {'username': 'not.a.user@ngis.edu.kh', 'overrides': {}}, ADMIN).status_code,
            404)


# ── 2. Authorization ───────────────────────────────────────────────────────

class TestAuthorization(RolesPermissionsTestBase):

    def test_read_guard_rejects_student(self):
        for path in ('/api/roles-mgmt/pages', '/api/roles-mgmt/users',
                     '/api/roles-mgmt/roles', '/api/roles-mgmt/audit',
                     '/api/roles-mgmt/overview'):
            r = self.get(path, STUDENT)
            self.assertEqual(r.status_code, 403, path)

    def test_anonymous_write_returns_401(self):
        # No header and no ngis_actor cookie: the read-only demo fallback must
        # never be allowed to mutate roles or access overrides.
        r = self.client.put('/api/roles-mgmt/overrides/' + TARGET, json={})
        self.assertEqual(r.status_code, 401)
        r = self.client.post('/api/roles-mgmt/roles', json={'name': 'Anon Role'})
        self.assertEqual(r.status_code, 401)

    def test_low_privilege_write_returns_403(self):
        self.assertEqual(self.put_overrides(TARGET, {}, STUDENT).status_code, 403)
        self.assertEqual(self.put_overrides(TARGET, {}, TEACHER).status_code, 403)

    def test_cookie_identity_is_accepted_for_writes(self):
        # Uses the URL-encoded cookie value a browser actually sends.
        c = self.cookie_client(ADMIN)
        r = self.put_overrides(TARGET, {}, actor=None, client=c)
        self.assertEqual(r.status_code, 200)
        self.assertIs(r.get_json()['success'], True)

    def test_encoded_cookie_is_decoded_before_account_lookup(self):
        c = self.cookie_client(STUDENT)
        d = c.get('/api/roles-mgmt/access?portal=student').get_json()
        self.assertIs(d['enforced'], True)
        self.assertEqual(d['username'], STUDENT)
        self.assertEqual(d['role'], 'STUDENT')
        gate = c.get('/api/roles-mgmt/my-access?page=admin.html&portal=admin').get_json()
        self.assertIs(gate['enforced'], True)
        self.assertIs(gate['allowed'], False)

    def test_super_admin_account_cannot_receive_overrides(self):
        r = self.put_overrides(ADMIN, {'portals': {'student': 'deny'}})
        self.assertEqual(r.status_code, 403)
        self.assertIn('protected', r.get_json()['error'].lower())

    def test_self_modification_is_blocked(self):
        patched = self._admin_store()
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.put_overrides(TEMP_ADMIN, {'portals': {'student': 'deny'}},
                                   actor=TEMP_ADMIN)
        self.assertEqual(r.status_code, 403)
        self.assertIn('Self-modification', r.get_json()['error'])

    def test_privilege_chain_requires_super_admin(self):
        patched = self._admin_store()
        payload = {'portals': {'admin': 'allow'}}
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.put_overrides(TARGET, payload, actor=TEMP_ADMIN)
            self.assertEqual(r.status_code, 403)
            self.assertIn('SUPER_ADMIN', r.get_json()['error'])
            # Explicit deny always reduces access and is always permitted.
            denied = self.put_overrides(TARGET, {'portals': {'admin': 'deny'}},
                                        actor=TEMP_ADMIN)
            self.assertEqual(denied.status_code, 200)
            # A SUPER_ADMIN actor may grant the protected portal.
            granted = self.put_overrides(TARGET, payload, actor=ADMIN)
            self.assertEqual(granted.status_code, 200)

    def test_protected_page_allow_requires_super_admin(self):
        patched = self._admin_store()
        payload = {'pages': {'admin:users-students': {'access': 'allow'}}}
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.put_overrides(TARGET, payload, actor=TEMP_ADMIN)
        self.assertEqual(r.status_code, 403)

    @staticmethod
    def _admin_store():
        """A second, non-super ADMIN actor for self/privilege-chain checks."""
        real = rp._identity_store()
        store = json.loads(json.dumps(real))
        store['accounts'].append({
            'username': TEMP_ADMIN, 'name': 'Regression Admin',
            'role': 'ADMIN', 'status': 'active', 'custom_roles': [],
        })
        return store


# ── 3. Override validation ─────────────────────────────────────────────────

class TestOverrideValidation(RolesPermissionsTestBase):

    def test_ambiguous_bare_page_id_is_rejected(self):
        r = self.put_overrides(TARGET, {'pages': {
            'dashboard': {'visibility': 'hidden', 'access': 'deny'}}})
        self.assertEqual(r.status_code, 400)
        self.assertIn('Ambiguous page id', r.get_json()['error'])
        self.assertIn('admin:dashboard', r.get_json()['error'])

    def test_unknown_page_module_action_are_rejected(self):
        cases = [
            {'pages': {'admin:not-a-real-page': {'visibility': 'hidden'}}},
            {'portals': {'not-a-portal': 'deny'}},
            {'portals': {'student': 'maybe'}},
            {'pages': {'admin:dashboard': {'visibility': 'vanish'}}},
            {'pages': {'admin:dashboard': {'access': 'sometimes'}}},
            {'actions': {'not-a-module': {'view': 'deny'}}},
            {'actions': {'user-management': {'delete': 'deny'}}},
        ]
        for payload in cases:
            r = self.put_overrides(TARGET, payload)
            self.assertEqual(r.status_code, 400, payload)

    def test_unambiguous_bare_id_is_normalised_to_qualified_key(self):
        normalized, error = rp._normalize_overrides(
            {'pages': {'roles-permissions': {'visibility': 'hidden'}}})
        self.assertIsNone(error)
        self.assertIn('admin:roles-permissions', normalized['pages'])
        self.assertNotIn('roles-permissions', normalized['pages'])

    def test_inherit_states_are_dropped(self):
        normalized, error = rp._normalize_overrides({
            'portals': {'student': 'inherit', 'admin': 'deny'},
            'pages': {'admin:dashboard': {'visibility': 'inherit', 'access': 'inherit'}},
            'actions': {'user-management': {'view': 'inherit', 'manage': 'deny'}},
        })
        self.assertIsNone(error)
        self.assertEqual(normalized['portals'], {'admin': 'deny'})
        self.assertEqual(normalized['pages'], {})
        self.assertEqual(normalized['actions'], {'user-management': {'manage': 'deny'}})

    def test_preview_computes_without_persisting(self):
        payload = {'username': TARGET, 'overrides': {'pages': {
            'student:dashboard': {'visibility': 'hidden', 'access': 'deny'}}}}
        r = self.post('/api/roles-mgmt/preview', payload, ADMIN)
        self.assertEqual(r.status_code, 200)
        eff = r.get_json()['effective']
        self.assertIn('student:dashboard', eff['hidden_keys'])
        self.assertIn('student:dashboard', eff['denied_keys'])
        # Nothing was written.
        persisted = self.get('/api/roles-mgmt/overrides/' + TARGET, ADMIN).get_json()
        self.assertEqual(persisted['overrides'], {})

    def test_saving_empty_document_clears_override(self):
        payload = {'portals': {'teacher': 'deny'}}
        self.assertEqual(self.put_overrides(TARGET, payload).status_code, 200)
        stored = self.get('/api/roles-mgmt/overrides/' + TARGET, ADMIN).get_json()
        self.assertEqual(stored['overrides']['portals'], {'teacher': 'deny'})
        cleared = self.put_overrides(TARGET, {})
        self.assertEqual(cleared.status_code, 200)
        after = self.get('/api/roles-mgmt/overrides/' + TARGET, ADMIN).get_json()
        self.assertEqual(after['overrides'], {})

    def test_action_override_changes_effective_permissions(self):
        payload = {'username': TARGET, 'overrides': {
            'actions': {'user-management': {'view': 'deny'}}}}
        eff = self.post('/api/roles-mgmt/preview', payload, ADMIN).get_json()['effective']
        self.assertNotIn('view', eff['permissions'].get('user-management', []))


# ── 4. Resolution and enforcement ──────────────────────────────────────────

class TestResolutionAndEnforcement(RolesPermissionsTestBase):

    def test_anonymous_demo_is_unenforced_and_unrestricted(self):
        d = self.client.get('/api/roles-mgmt/access?portal=student').get_json()
        self.assertIs(d['enforced'], False)
        self.assertEqual(d['hidden_pages'], [])
        self.assertEqual(d['denied_pages'], [])
        d2 = self.client.get('/api/roles-mgmt/my-access?page=admin.html').get_json()
        self.assertIs(d2['enforced'], False)
        self.assertIs(d2['allowed'], True)
        self.assertEqual(d2['reason'], 'anonymous_demo')

    def test_qualified_override_does_not_leak_across_portals(self):
        payload = {'pages': {'student:dashboard': {
            'visibility': 'hidden', 'access': 'deny'}}}
        self.assertEqual(self.put_overrides(TARGET, payload).status_code, 200)

        student_doc = self.get('/api/roles-mgmt/access?portal=student', STUDENT).get_json()
        self.assertIs(student_doc['enforced'], True)
        self.assertIn('dashboard', student_doc['hidden_pages'])
        self.assertIn('student.html', student_doc['hidden_files'])
        self.assertIn('student:dashboard', student_doc['hidden_keys'])
        # A different portal with its own "dashboard" is unaffected.
        self.assertNotIn('admin:dashboard', student_doc['hidden_keys'])
        teacher_doc = self.get('/api/roles-mgmt/access?portal=teacher', STUDENT).get_json()
        self.assertEqual(teacher_doc['hidden_pages'], [])
        self.assertEqual(teacher_doc['hidden_files'], [])

        eff = self.get('/api/roles-mgmt/effective/' + TARGET, ADMIN).get_json()
        denied_page = next(p for p in eff['pages'] if p['key'] == 'student:dashboard')
        self.assertIs(denied_page['visible'], False)
        self.assertIs(denied_page['allowed'], False)
        self.assertEqual(denied_page['source'], 'page_denied')
        admin_page = next(p for p in eff['pages'] if p['key'] == 'admin:dashboard')
        self.assertIs(admin_page['visible'], True)

        gate = self.get('/api/roles-mgmt/my-access?page=student.html&portal=student',
                        STUDENT).get_json()
        self.assertIs(gate['allowed'], False)
        self.assertIs(gate['hidden'], True)
        self.assertEqual(gate['page'], 'student:dashboard')

    def test_hidden_only_is_not_treated_as_access_deny(self):
        """Visibility and access are independent: hiding a nav link must not
        become the security boundary. Only access=deny (or a portal deny) does."""
        page = self.student_page('calendar')
        payload = {'pages': {page['key']: {'visibility': 'hidden'}}}
        self.assertEqual(self.put_overrides(TARGET, payload).status_code, 200)

        access = self.get('/api/roles-mgmt/access?portal=student', STUDENT).get_json()
        self.assertIn('calendar', access['hidden_pages'])
        self.assertNotIn('calendar', access['denied_pages'])

        gate = self.get('/api/roles-mgmt/my-access?page=' + page['file'] +
                        '&portal=student', STUDENT).get_json()
        self.assertIs(gate['hidden'], True)
        self.assertIs(gate['allowed'], True, 'hidden-only must remain reachable')

        c = self.cookie_client(STUDENT)
        status, _ = self.document(c, '/' + page['href'])
        self.assertNotEqual(status, 302, 'hidden-only page was blocked by the gate')

    def test_hide_and_deny_blocks_direct_url(self):
        page = self.student_page('calendar')
        payload = {'pages': {page['key']: {
            'visibility': 'hidden', 'access': 'deny'}}}
        self.assertEqual(self.put_overrides(TARGET, payload).status_code, 200)

        gate = self.get('/api/roles-mgmt/my-access?page=' + page['file'] +
                        '&portal=student', STUDENT).get_json()
        self.assertIs(gate['allowed'], False)
        self.assertEqual(gate['reason'], 'page_denied')

        c = self.cookie_client(STUDENT)
        status, location = self.document(c, '/' + page['href'])
        self.assertEqual(status, 302)
        self.assertIn('/pages/shared/access-denied.html', location)
        self.assertIn('reason=access_denied', location)

    def test_portal_deny_blocks_every_page_in_that_portal(self):
        self.assertEqual(self.put_overrides(TARGET, {'portals': {'teacher': 'deny'}}).status_code, 200)
        eff = self.get('/api/roles-mgmt/effective/' + TARGET, ADMIN).get_json()
        self.assertEqual(eff['portals']['teacher'], 'deny')
        teacher_pages = [p for p in eff['pages'] if p['portal'] == 'teacher']
        self.assertTrue(teacher_pages)
        self.assertTrue(all(not p['allowed'] for p in teacher_pages))
        self.assertTrue(all(p['source'] == 'portal_denied' for p in teacher_pages))
        self.assertTrue(all(p['visible'] for p in teacher_pages))

    def test_direct_url_gate_uses_explicit_identity_only(self):
        admin_page = '/pages/admin/admin-teacher-verify.html'
        own_page = '/pages/student/student.html'

        student = self.cookie_client(STUDENT)
        status, location = self.document(student, admin_page)
        self.assertEqual(status, 302)
        self.assertIn('access-denied.html', location)
        self.assertNotEqual(self.document(student, own_page)[0], 302)

        # SUPER_ADMIN is never restricted, even with overrides attempted.
        sup = self.cookie_client(ADMIN)
        self.assertNotEqual(self.document(sup, admin_page)[0], 302)

        # Passive demo browsing stays unrestricted.
        anon = app.test_client()
        self.assertNotEqual(self.document(anon, admin_page)[0], 302)

        # Header identity also activates the gate for non-browser API clients.
        status, _ = self.document(app.test_client(), admin_page, hdr(STUDENT))
        self.assertEqual(status, 302)

    def test_unlisted_or_unknown_actor_is_not_locked_out(self):
        # An unknown identity cannot be resolved to an account, so enforcement
        # is intentionally disabled rather than locking out the public demo.
        unknown = self.get('/api/roles-mgmt/my-access?page=admin.html',
                           'ghost@ngis.edu.kh').get_json()
        self.assertIs(unknown['enforced'], False)
        self.assertIs(unknown['allowed'], True)
        self.assertEqual(unknown['reason'], 'anonymous_demo')
        status, _ = self.document(self.cookie_client('ghost@ngis.edu.kh'),
                                  '/pages/admin/admin.html')
        self.assertNotEqual(status, 302)

        # A known actor asking about a page absent from the nav registry is
        # allowed by default (unlisted pages are not silently denied).
        known = self.get('/api/roles-mgmt/my-access?page=does-not-exist.html',
                         STUDENT).get_json()
        self.assertIs(known['enforced'], True)
        self.assertIs(known['allowed'], True)
        self.assertEqual(known['reason'], 'unlisted_page')

    def test_super_admin_override_resolution_is_always_unrestricted(self):
        eff = self.get('/api/roles-mgmt/effective/' + ADMIN, ADMIN).get_json()
        self.assertIs(eff['protected'], True)
        self.assertEqual(eff['hidden_keys'], [])
        self.assertEqual(eff['denied_keys'], [])
        self.assertTrue(all(p['allowed'] for p in eff['pages']))


# ── 5. Frontend / static wiring ────────────────────────────────────────────

class TestFrontendWiring(unittest.TestCase):

    @staticmethod
    def read(path):
        with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
            return fh.read()

    def test_workspace_page_and_renderer_exist(self):
        page = self.read('pages/admin/admin-roles-permissions.html')
        self.assertIn('rolesRoot', page)
        self.assertIn('NGIS_ROLES.init', page)
        self.assertIn('active: "roles-permissions"', page)
        self.assertIn('assets/js/ngis-roles.js', page)
        self.assertIn('assets/js/auth.js', page)
        self.assertIn('assets/js/layout.js', page)
        self.assertIn('assets/css/app.css', page)
        renderer = self.read('assets/js/ngis-roles.js')
        for endpoint in ('/api/roles-mgmt/registry', '/api/roles-mgmt/users',
                         '/api/roles-mgmt/preview', '/api/roles-mgmt/overrides/'):
            self.assertIn(endpoint, renderer)
        self.assertIn('ngis-nav-access-v2', renderer)
        self.assertIn('NGIS_SIDEBAR.refreshAccess', renderer)

    def test_scoped_styles_and_sidebar_v2_exist(self):
        css = self.read('assets/css/design-system.css')
        self.assertIn('.ngis-rp', css)
        self.assertIn('prefers-reduced-motion', css)
        app_css = self.read('assets/css/app.css')
        self.assertIn('SIDEBAR SYSTEM v2', app_css)
        self.assertIn('--ngis-sb-accent', app_css)
        self.assertIn('body.sidebar-open', app_css)

    def test_nav_entry_is_published_and_fallback_present(self):
        nav = json.loads(self.read('data/sidebar_nav.json'))
        entries = []

        def walk(node):
            if isinstance(node, dict):
                if node.get('id') == 'roles-permissions':
                    entries.append(node)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)
        walk(nav)
        self.assertEqual(len(entries), 2, 'published + defaults nav entries')
        for entry in entries:
            self.assertEqual(entry['href'], 'pages/admin/admin-roles-permissions.html')
        layout = self.read('assets/js/layout.js')
        self.assertIn('"roles-permissions"', layout)
        self.assertIn('ngis-nav-access-v2', layout)

    def test_layout_copies_are_byte_identical(self):
        with open(os.path.join(ROOT, 'layout.js'), 'rb') as fh:
            root_copy = fh.read()
        with open(os.path.join(ROOT, 'assets/js/layout.js'), 'rb') as fh:
            shared_copy = fh.read()
        self.assertEqual(root_copy, shared_copy,
                         'root layout.js must stay in sync with assets/js/layout.js')

    def test_no_hardcoded_permission_bypass(self):
        source = self.read('roles_permissions_api.py')
        self.assertIn('def _explicit_actor()', source)
        self.assertIn("actor = _explicit_actor()", source)
        # The read-only demo fallback must not appear in the write guard.
        guard = source[source.index('def _guard_write'):source.index('def _guard_privilege_chain')]
        self.assertNotIn("'admin@ngis.edu.kh'", guard)
        self.assertIn('401', guard)


if __name__ == '__main__':
    unittest.main(verbosity=2)
