"""NGIS — Roles & Access Control v3 security regression suite.

Covers the enterprise access-management extension:
  * bootstrap / authority / permission-definition inventory
  * custom permission definitions: validation, duplicate keys, unsupported
    actions, honest "Requires Integration" marking, edit + delete
  * custom role lifecycle: rich create, edit, protected core roles, safe
    delete, optimistic concurrency
  * role-level portal access with SUPER_ADMIN-only protected grants and the
    real resolver effect on page access
  * user-role assignment, delegation guard, self-assignment, SUPER_ADMIN
    protection and last-SUPER_ADMIN rule
  * request-level API enforcement (default deny, unknown permission,
    anonymous demo, explicit deny override)
  * server-side pagination for audit log and account directory

Every test snapshots and restores both JSON stores so no audit entries,
roles, overrides or assignments are left in the demo data.
"""
import json
import os
import unittest
from unittest import mock

import roles_permissions_api as rp
import roles_permissions_ext as ext
from server import app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROLES_STORE = rp.STORE_PATH
IDENTITY_STORE = os.path.join(ROOT, 'data', 'user_accounts.json')

SUPER = 'admin@ngis.edu.kh'          # SUPER_ADMIN, active
STUDENT = 'student@ngis.edu.kh'      # STUDENT, active
TEACHER = 'teacher@ngis.edu.kh'
PLAIN_ADMIN = 'plain.admin@ngis.edu.kh'


def hdr(actor):
    return {'X-Actor': actor} if actor else {}


def snapshot(path):
    with open(path, 'rb') as fh:
        return fh.read()


def restore(path, data):
    with open(path, 'wb') as fh:
        fh.write(data)


class V3Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roles_snap = snapshot(ROLES_STORE)
        cls.identity_snap = snapshot(IDENTITY_STORE)

    @classmethod
    def tearDownClass(cls):
        restore(ROLES_STORE, cls.roles_snap)
        restore(IDENTITY_STORE, cls.identity_snap)

    def setUp(self):
        restore(ROLES_STORE, self.roles_snap)
        restore(IDENTITY_STORE, self.identity_snap)
        # Deterministic baseline: permission definitions are keyed by fixed
        # names in these tests, so start from an empty definition registry.
        # tearDownClass still restores the operator's real snapshot verbatim.
        baseline = json.loads(self.roles_snap)
        baseline['permission_definitions'] = []
        baseline['role_portals'] = {}
        restore(ROLES_STORE, json.dumps(baseline, ensure_ascii=False).encode('utf-8'))
        self.client = app.test_client()

    def get(self, path, actor=SUPER):
        return self.client.get(path, headers=hdr(actor))

    def post(self, path, body=None, actor=SUPER):
        return self.client.post(path, json=body or {}, headers=hdr(actor))

    def put(self, path, body=None, actor=SUPER):
        return self.client.put(path, json=body or {}, headers=hdr(actor))

    def delete(self, path, body=None, actor=SUPER):
        return self.client.delete(path, json=body or {}, headers=hdr(actor))

    def make_role(self, name='V3 Regression Role', **extra):
        body = {'name': name, 'description': 'Created by the v3 regression suite',
                'identifier': 'v3-regression-role', 'category': 'academic',
                'default_portal': 'teacher', 'base_role': 'TEACHER',
                'permissions': {'student-profiles': ['view']}, 'portals': ['teacher']}
        body.update(extra)
        r = self.post('/api/roles-mgmt/roles/create', body)
        self.assertEqual(r.status_code, 201, r.get_json())
        return r.get_json()['role']


class TestBootstrapAndDefinitions(V3Base):

    def test_bootstrap_reports_real_counts(self):
        d = self.get('/api/roles-mgmt/bootstrap').get_json()
        self.assertIs(d['success'], True)
        self.assertEqual(d['totals']['total_roles'], 6 + len(rp._store()['custom_roles']))
        self.assertGreaterEqual(d['totals']['registered_permissions'], 100)
        self.assertGreaterEqual(d['totals']['real_pages'], 50)
        self.assertGreaterEqual(d['totals']['accounts'], 200)
        self.assertGreaterEqual(d['totals']['enforced_bindings'], 10)
        self.assertTrue(d['authority']['is_super_admin'])
        self.assertIn('core_roles', d['registry'])
        self.assertEqual(len(d['registry']['core_roles']), 6)

    def test_bootstrap_rejects_low_privilege_reader(self):
        self.assertEqual(self.get('/api/roles-mgmt/bootstrap', STUDENT).status_code, 403)
        self.assertEqual(self.get('/api/roles-mgmt/permissions', STUDENT).status_code, 403)
        self.assertEqual(self.get('/api/roles-mgmt/enforcement', STUDENT).status_code, 403)

    def test_definitions_inventory_marks_enforcement_honestly(self):
        d = self.get('/api/roles-mgmt/permissions').get_json()
        self.assertIs(d['success'], True)
        self.assertGreaterEqual(d['totals']['registered'], 100)
        self.assertTrue(any(x['enforcement'] == 'enforced' for x in d['builtin']))
        self.assertTrue(any(x['enforcement'] == 'registered' for x in d['builtin']))
        for a in d['actions']:
            self.assertIn(a['id'], rp.ALL_ACTIONS)
        for p in d['pages']:
            self.assertIn(':', p)

    def test_create_custom_permission_is_marked_requires_integration(self):
        # A genuinely new module (the documented "Approve Teacher Reports"
        # example) must be stored, but honestly flagged as not yet enforced.
        body = {'name': 'Approve Teacher Reports', 'key': 'teacher-reports.approve',
                'description': 'Approves teacher-authored academic reports',
                'module': 'teacher-reports', 'action': 'approve',
                'portal': 'teacher', 'target_page': 'teacher:reports',
                'scope': 'assigned-campus'}
        r = self.post('/api/roles-mgmt/permissions', body)
        self.assertEqual(r.status_code, 201, r.get_json())
        d = r.get_json()['definition']
        self.assertIs(d['custom_module'], True)
        self.assertEqual(d['enforcement'], 'requires_integration')
        self.assertIs(d['enforceable'], False)
        self.assertIn('Requires Integration', r.get_json()['message'])

        # A definition mapped to a registered, API-bound pair is enforced.
        bound = dict(body, key='teacher-profiles.custom-view',
                     module='teacher-profiles', action='view', target_page='')
        rb = self.post('/api/roles-mgmt/permissions', bound)
        self.assertEqual(rb.status_code, 201, rb.get_json())
        self.assertEqual(rb.get_json()['definition']['enforcement'], 'enforced')

        # An unbound registered pair is likewise flagged honestly.
        body2 = dict(body, key='report-cards.manual-check', module='report-cards',
                     action='download', portal='student', target_page='')
        r2 = self.post('/api/roles-mgmt/permissions', body2)
        self.assertEqual(r2.status_code, 201, r2.get_json())
        self.assertEqual(r2.get_json()['definition']['enforcement'], 'requires_integration')

        listed = self.get('/api/roles-mgmt/permissions').get_json()
        self.assertEqual(listed['totals']['requires_integration'], 2)
        # Not presented as an active security control in the registry.
        boot = self.get('/api/roles-mgmt/bootstrap').get_json()
        self.assertNotIn('teacher-reports.approve',
                         [d['key'] for d in boot['definitions']['custom'] if d['enforceable']])

    def test_unenforced_definition_cannot_be_granted_to_a_role(self):
        self.post('/api/roles-mgmt/permissions', {
            'name': 'Unbound Permission', 'key': 'teacher-reports.approve',
            'module': 'teacher-reports', 'action': 'approve',
            'portal': 'teacher', 'target_page': ''})
        role = self.make_role()
        r = self.put('/api/roles-mgmt/roles/%s/permissions/save' % role['id'], {
            'permissions': {}, 'custom_permission_keys': ['teacher-reports.approve']})
        self.assertEqual(r.status_code, 403)
        self.assertIn('requires backend integration', r.get_json()['error'])

    def test_permission_validation_rejects_forged_input(self):
        cases = [
            ({'name': 'x'}, 'at least 3 characters'),
            ({'key': 'Bad Key'}, 'permission key'),
            ({'key': 'nodothere'}, 'permission key'),
            ({'key': 'x.unknown', 'module': 'NOT A MODULE'}, 'not registered'),
            ({'key': 'x.fakeaction', 'module': 'news', 'action': 'teleport'}, 'Unsupported action'),
            ({'key': 'x.view', 'module': 'news', 'action': 'view', 'portal': 'not-a-portal'}, 'Unknown portal'),
            ({'key': 'x.view', 'module': 'news', 'action': 'view', 'scope': 'everywhere'}, 'Unknown permission scope'),
            ({'key': 'x.view', 'module': 'news', 'action': 'view',
              'target_page': 'admin:does-not-exist'}, 'not a published'),
            ({'key': 'news.view', 'module': 'news', 'action': 'view'}, 'already a registered'),
        ]
        for extra, expected in cases:
            body = {'name': 'Regression Permission', 'module': 'news', 'action': 'view',
                    'key': 'regression.check', 'portal': 'admin'}
            body.update(extra)
            r = self.post('/api/roles-mgmt/permissions', body)
            self.assertEqual(r.status_code in (400, 409), True, (extra, r.status_code))
            self.assertIn(expected.lower(), r.get_json()['error'].lower(), extra)

    def test_duplicate_custom_key_rejected(self):
        body = {'name': 'Duplicate Check', 'key': 'news.duplicate-check',
                'module': 'news', 'action': 'view', 'portal': 'admin'}
        self.assertEqual(self.post('/api/roles-mgmt/permissions', body).status_code, 201)
        dup = self.post('/api/roles-mgmt/permissions', body)
        self.assertEqual(dup.status_code, 409)
        self.assertIn('already exists', dup.get_json()['error'])

    def test_definition_edit_and_delete_are_audited(self):
        self.post('/api/roles-mgmt/permissions', {
            'name': 'Editable Permission', 'key': 'news.editable-check',
            'module': 'news', 'action': 'view', 'portal': 'admin'})
        edited = self.put('/api/roles-mgmt/permissions/news.editable-check',
                          {'name': 'Renamed Permission', 'description': 'Updated',
                           'key': 'news.hacked', 'module': 'system-configuration',
                           'action': 'manage', 'portal': 'admin'})
        self.assertEqual(edited.status_code, 200, edited.get_json())
        self.assertEqual(edited.get_json()['definition']['key'], 'news.editable-check')
        self.assertEqual(edited.get_json()['definition']['module'], 'news')
        self.assertEqual(edited.get_json()['definition']['name'], 'Renamed Permission')
        removed = self.post('/api/roles-mgmt/permissions/news.editable-check/delete')
        self.assertEqual(removed.status_code, 200)
        self.assertEqual(self.put('/api/roles-mgmt/permissions/news.editable-check',
                                  {'name': 'x'}).status_code, 404)
        actions = [e['action'] for e in self.get('/api/roles-mgmt/audit').get_json()['data']]
        self.assertIn('permission_created', actions)
        self.assertIn('permission_updated', actions)
        self.assertIn('permission_deleted', actions)

    def test_anonymous_cannot_create_permission(self):
        self.assertEqual(self.post('/api/roles-mgmt/permissions', {
            'name': 'Anon Permission', 'key': 'news.anon', 'module': 'news',
            'action': 'view'}, actor=None).status_code, 401)

    def test_plain_admin_cannot_define_protected_portal_permission(self):
        patched = _with_plain_admin()
        body = {'name': 'Protected Scope', 'key': 'news.protected-check',
                'module': 'news', 'action': 'view', 'portal': 'superadmin'}
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.post('/api/roles-mgmt/permissions', body, PLAIN_ADMIN)
        self.assertEqual(r.status_code, 403)
        self.assertIn('SUPER_ADMIN', r.get_json()['error'])


class TestRoleLifecycle(V3Base):

    def test_rich_create_edit_and_delete(self):
        role = self.make_role()
        self.assertEqual(role['identifier'], 'v3-regression-role')
        self.assertEqual(role['category'], 'academic')
        self.assertEqual(role['default_portal'], 'teacher')
        self.assertEqual(role['portals'], ['teacher'])
        self.assertTrue(role['updated_at'])

        edited = self.post('/api/roles-mgmt/roles/%s/edit' % role['id'], {
            'name': 'Renamed V3 Role', 'description': 'Edited',
            'category': 'operations', 'expected_updated_at': role['updated_at']})
        self.assertEqual(edited.status_code, 200, edited.get_json())
        self.assertEqual(edited.get_json()['role']['category'], 'operations')

        deleted = self.delete('/api/roles-mgmt/roles/%s' % role['id'])
        self.assertEqual(deleted.status_code, 200, deleted.get_json())
        self.assertNotIn(role['id'], [r['id'] for r in rp._store()['custom_roles']])

    def test_core_roles_cannot_be_edited_or_deleted(self):
        r = self.post('/api/roles-mgmt/roles/ADMIN/edit', {'name': 'Hacked'})
        self.assertEqual(r.status_code, 403)
        self.assertIn('protected', r.get_json()['error'].lower())
        self.assertEqual(self.delete('/api/roles-mgmt/roles/SUPER_ADMIN').status_code, 403)
        self.assertEqual(self.put('/api/roles-mgmt/roles/SUPER_ADMIN/permissions/save',
                                  {'permissions': {}}).status_code, 403)

    def test_stale_write_is_rejected(self):
        role = self.make_role()
        stale = self.put('/api/roles-mgmt/roles/%s/permissions/save' % role['id'], {
            'permissions': {'student-profiles': ['view']},
            'expected_updated_at': '2000-01-01 00:00'})
        self.assertEqual(stale.status_code, 409)
        self.assertEqual(stale.get_json()['code'], 'stale_role')
        self.assertEqual(self.post('/api/roles-mgmt/roles/%s/edit' % role['id'], {
            'name': 'Stale Edit', 'expected_updated_at': '2000-01-01 00:00'}).status_code, 409)

    def test_role_with_members_cannot_be_deleted(self):
        role = self.make_role()
        r = self.post('/api/roles-mgmt/user-roles',
                      {'username': TEACHER, 'role_id': role['id'], 'op': 'assign'})
        self.assertEqual(r.status_code, 200, r.get_json())
        blocked = self.delete('/api/roles-mgmt/roles/%s' % role['id'])
        self.assertEqual(blocked.status_code, 409)
        self.assertIn('Unassign', blocked.get_json()['error'])
        self.assertEqual(self.post('/api/roles-mgmt/user-roles',
                                   {'username': TEACHER, 'role_id': role['id'],
                                    'op': 'revoke'}).status_code, 200)
        self.assertEqual(self.delete('/api/roles-mgmt/roles/%s' % role['id']).status_code, 200)

    def test_privilege_chain_requires_super_admin(self):
        patched = _with_plain_admin()
        body = {'name': 'Escalation Role', 'identifier': 'escalation-role',
                'base_role': 'ADMIN', 'permissions': {'roles-access': ['view', 'manage']}}
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.post('/api/roles-mgmt/roles/create', body, PLAIN_ADMIN)
        self.assertEqual(r.status_code, 403)
        self.assertIn('SUPER_ADMIN', r.get_json()['error'])

    def test_portal_grants_are_enforced_by_the_real_resolver(self):
        role = self.make_role()
        self.post('/api/roles-mgmt/user-roles',
                  {'username': STUDENT, 'role_id': role['id'], 'op': 'assign'})
        idstore = rp._identity_store()
        account = rp._account_by_username(STUDENT, idstore)
        doc = rp._resolve_access(account, {})
        self.assertEqual(doc['portals']['teacher'], 'allow')
        own = next(p for p in doc['pages'] if p['portal'] == 'teacher')
        self.assertIs(own['allowed'], True)
        # An explicit per-account deny still overrides the role grant.
        denied = rp._resolve_access(account, {'portals': {'teacher': 'deny'}})
        self.assertEqual(denied['portals']['teacher'], 'deny')
        self.assertFalse(next(p for p in denied['pages'] if p['portal'] == 'teacher')['allowed'])

    def test_protected_portal_grant_requires_super_admin(self):
        role = self.make_role()
        patched = _with_plain_admin()
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.put('/api/roles-mgmt/roles/%s/portals' % role['id'],
                         {'portals': ['teacher', 'principal']}, PLAIN_ADMIN)
        self.assertEqual(r.status_code, 403)
        self.assertIn('SUPER_ADMIN', r.get_json()['error'])
        ok = self.put('/api/roles-mgmt/roles/%s/portals' % role['id'],
                      {'portals': ['teacher', 'principal']})
        self.assertEqual(ok.status_code, 200, ok.get_json())
        self.assertIn('principal', ok.get_json()['portals'])


class TestEnforcementAndAssignments(V3Base):

    def test_api_gate_denies_unauthorized_explicit_actor(self):
        r = self.post('/api/news', {'title': 'x'}, STUDENT)
        self.assertEqual(r.status_code, 403)
        d = r.get_json()
        self.assertEqual(d['required_permission'], 'news.edit')
        self.assertIn('Permission denied', d['error'])

    def test_api_gate_allows_authorized_actor_and_anonymous_demo(self):
        # SUPER_ADMIN holds every registered action.
        r = self.post('/api/news', {'title': 'Regression probe'}, SUPER)
        self.assertNotEqual(r.status_code, 403)
        # Anonymous demo browsing stays unrestricted (demo-first architecture).
        anon = self.client.post('/api/news', json={'title': 'Anonymous probe'})
        self.assertNotEqual(anon.status_code, 403)

    def test_unknown_permission_is_default_denied(self):
        allowed, reason = ext.enforce_permission('not-a-module', 'view')
        self.assertIs(allowed, False)
        self.assertEqual(reason, 'unknown_permission')
        allowed, reason = ext.enforce_permission('news', 'teleport')
        self.assertIs(allowed, False)
        self.assertEqual(reason, 'unknown_permission')

    def test_explicit_action_deny_blocks_bound_api(self):
        # A SUPER_ADMIN is always unrestricted; use a plain ADMIN account and
        # explicitly deny news.edit through the same override engine.
        patched = _with_plain_admin()
        overrides = {'actions': {'news': {'edit': 'deny'}}}
        with mock.patch.object(rp, '_identity_store', return_value=patched), \
             mock.patch.object(ext, '_store', return_value={'user_overrides': {PLAIN_ADMIN: overrides},
                                                            'custom_roles': [],
                                                            'permission_definitions': [],
                                                            'audit_log': []}):
            allowed, reason = ext.enforce_permission('news', 'edit', PLAIN_ADMIN, patched)
            self.assertIs(allowed, False)
            self.assertEqual(reason, 'denied')

    def test_self_assignment_and_super_admin_protection(self):
        role = self.make_role()
        r = self.post('/api/roles-mgmt/user-roles',
                      {'username': SUPER, 'role_id': role['id'], 'op': 'assign'}, SUPER)
        self.assertEqual(r.status_code, 403)
        r2 = self.post('/api/roles-mgmt/user-roles',
                       {'username': SUPER, 'role_id': role['id'], 'op': 'assign'})
        self.assertEqual(r2.status_code, 403)
        self.assertIn('protected identity', r2.get_json()['error'])

    def test_delegation_guard_blocks_granting_unheld_permission(self):
        role = self.make_role(permissions={
            'student-profiles': ['view'], 'system-configuration': ['view', 'manage']})
        patched = _with_plain_admin()
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            r = self.post('/api/roles-mgmt/user-roles',
                          {'username': TEACHER, 'role_id': role['id'], 'op': 'assign'},
                          PLAIN_ADMIN)
        # PLAIN_ADMIN does hold system-configuration.manage in the ADMIN baseline,
        # so this succeeds; the guard is exercised with an unheld action below.
        self.assertEqual(r.status_code, 200, r.get_json())
        role2 = self.make_role(name='Impossible Delegation',
                               identifier='impossible-delegation',
                               permissions={'roles-access': ['view', 'manage']})
        with mock.patch.object(rp, '_identity_store', return_value=patched):
            denied = self.post('/api/roles-mgmt/user-roles',
                               {'username': STUDENT, 'role_id': role2['id'], 'op': 'assign'},
                               PLAIN_ADMIN)
        self.assertEqual(denied.status_code, 403)

    def test_missing_super_admin_locks_role_changes(self):
        idstore = rp._identity_store()
        broken = json.loads(json.dumps(idstore))
        for a in broken['accounts']:
            if a.get('role') == 'SUPER_ADMIN':
                a['status'] = 'disabled'
        broken['accounts'].append({
            'username': PLAIN_ADMIN, 'name': 'Regression Administrator',
            'email': PLAIN_ADMIN, 'role': 'ADMIN', 'status': 'active',
            'custom_roles': [], 'campus': 'All campuses'})
        with mock.patch.object(rp, '_identity_store', return_value=broken):
            r = self.post('/api/roles-mgmt/roles/create',
                          {'name': 'No Super Role', 'identifier': 'no-super-role'},
                          PLAIN_ADMIN)
        self.assertEqual(r.status_code, 409)
        self.assertIn('SUPER_ADMIN', r.get_json()['error'])


class TestPagination(V3Base):

    def test_audit_is_server_paginated(self):
        first = self.get('/api/roles-mgmt/audit/paged?limit=3&offset=0').get_json()
        self.assertIs(first['success'], True)
        self.assertLessEqual(len(first['data']), 3)
        self.assertEqual(first['limit'], 3)
        self.assertEqual(first['offset'], 0)
        self.assertGreaterEqual(first['total'], 13)
        self.assertTrue(first['has_more'])
        self.assertEqual(first['data'][0]['id'],
                         self.get('/api/roles-mgmt/audit').get_json()['data'][0]['id'])
        second = self.get('/api/roles-mgmt/audit/paged?limit=3&offset=3').get_json()
        self.assertNotEqual(first['data'][0]['id'], second['data'][0]['id'])
        self.assertTrue(second['actions'])

    def test_users_are_server_paginated_and_filterable(self):
        d = self.get('/api/roles-mgmt/users/paged?limit=5&offset=0').get_json()
        self.assertIs(d['success'], True)
        self.assertEqual(len(d['users']), 5)
        self.assertTrue(d['has_more'])
        # Explicit ALL sentinels must not filter anything out (case-normalised).
        explicit = self.get('/api/roles-mgmt/users/paged?limit=5&role=ALL&campus=ALL').get_json()
        self.assertEqual(explicit['total'], d['total'])
        self.assertEqual(len(explicit['users']), 5)
        campus = self.get('/api/roles-mgmt/campuses').get_json()
        self.assertTrue(campus['campuses'])
        filtered = self.get('/api/roles-mgmt/users/paged?limit=5&role=STUDENT').get_json()
        self.assertTrue(all(u['role'] == 'STUDENT' for u in filtered['users']))
        self.assertLess(filtered['total'], d['total'])


class TestFrontendContracts(unittest.TestCase):
    """Static guards for the UI contracts verified in the real browser.

    The dialog is deliberately reparented to document.body; without the
    matching standalone scrim CSS and focus-trap target the global topbar is
    not dimmed and Tab escapes the dialog. These checks stop that regression.
    """

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT, 'assets', 'js', 'ngis-roles.js'), encoding='utf-8') as fh:
            cls.js = fh.read()
        with open(os.path.join(ROOT, 'assets', 'css', 'roles-access.css'), encoding='utf-8') as fh:
            cls.css = fh.read()
        with open(os.path.join(ROOT, 'pages', 'admin', 'admin-roles-permissions.html'),
                  encoding='utf-8') as fh:
            cls.html = fh.read()

    def test_dialog_is_hoisted_to_body_with_standalone_styles(self):
        self.assertIn("document.body.appendChild(scrim)", self.js)
        self.assertIn("scrim.classList.add('ngis-rp', 'rp-v3', 'rp-v3-scrim')", self.js)
        self.assertIn('html body > .rp-v3-scrim.rp-modal-scrim', self.css)

    def test_focus_trap_and_event_delegation_follow_the_hoisted_dialog(self):
        self.assertIn("(S.modalEl || S.root).querySelector('.rp-modal')", self.js)
        self.assertIn('!(S.modalEl && S.modalEl.contains(t))', self.js)

    def test_custom_module_edit_still_shows_its_slug(self):
        self.assertIn("(edit && !d.custom_module) ? d.module : '__new__'", self.js)

    def test_campus_no_filter_label_is_not_a_duplicate_of_a_real_campus(self):
        self.assertIn('Every campus (no filter)', self.js)

    def test_page_loads_versioned_workspace_assets(self):
        self.assertIn('roles-access.css?v=', self.html)
        self.assertIn('ngis-roles.js?v=', self.html)


def _with_plain_admin():
    """Identity store containing a second, non-super ADMIN actor."""
    store = json.loads(json.dumps(rp._identity_store()))
    store['accounts'].append({
        'username': PLAIN_ADMIN, 'name': 'Regression Administrator',
        'email': PLAIN_ADMIN, 'role': 'ADMIN', 'status': 'active',
        'custom_roles': [], 'campus': 'All campuses',
    })
    return store


if __name__ == '__main__':
    unittest.main(verbosity=2)
