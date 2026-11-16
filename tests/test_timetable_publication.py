"""Timetable Save Draft & Publish — acceptance tests.

Covers the workflow: Drag & Drop -> Auto-Save Draft -> Validate -> Preview ->
Publish -> Teacher & Student Portals -> Admin Monitoring, per the MVP prompt's
12 acceptance criteria.
"""
import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, 'data', 'timetable_state.json')


class TimetablePublicationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import warnings
        warnings.filterwarnings('ignore')
        import server
        cls.app = server.app
        cls.app.testing = True
        cls.client = cls.app.test_client()
        cls._backup = None
        if os.path.exists(STATE):
            cls._backup = STATE + '.bak'
            shutil.copy2(STATE, cls._backup)

    def setUp(self):
        # The store is an in-process singleton; use the reset endpoint so the
        # in-memory document (not just the file) returns to a clean seed.
        r = self.client.post('/api/timetable/reset')
        assert r.status_code == 200, r.get_data(as_text=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(STATE):
            os.remove(STATE)
        if cls._backup:
            shutil.move(cls._backup, STATE)

    # ── helpers ────────────────────────────────────────────────────────────
    def _auto_assign_and_publish(self, force=False):
        r = self.client.post('/api/timetable/auto-assign')
        self.assertEqual(r.status_code, 200)
        r = self.client.post('/api/timetable/publish', json={
            'published_by': 'Principal', 'note': 'acceptance',
            'effective_from': '2026-11-15', 'force': force})
        return r

    def _state(self):
        return self.client.get('/api/timetable/state').get_json()['state']

    def _replacement_teacher(self, state, victim_key):
        """A teacher id (not a code) free at the victim's slot, so the swap
        stays conflict-free and the lesson stays visible in portal views
        (grid cells store teacher ids, e.g. 't_ED1', not codes like 'K1')."""
        parts = victim_key.split('|')
        busy = {c['teacher_id'] for k, c in state['grid'].items()
                if k.split('|')[:3] == parts[:3]}
        current = state['grid'][victim_key]['teacher_id']
        for t in state['teachers']:
            tid = t['id']
            if tid != current and tid not in busy:
                return tid
        self.fail('no free replacement teacher available')

    # ── criteria 1-3: drag, save, refresh persistence ──────────────────────
    def test_01_drag_save_and_refresh_persists(self):
        """Simulate a drag: move a lesson via the cells API, save the whole
        draft, then a fresh GET (simulating browser restart) still has it."""
        self.client.post('/api/timetable/auto-assign')
        state = self._state()
        revision = state['revision']
        # pick a placed lesson and move it to an empty slot
        src_key = sorted(state['grid'].keys())[0]
        cell = dict(state['grid'][src_key])
        target_key = None
        for day in state['settings']['days']:
            for shift in state['settings']['shifts']:
                for period in range(1, 6):
                    k = f"{day}|{shift}|{period}|{cell['class_id']}"
                    if k not in state['grid'] and k != src_key:
                        target_key = k
                        break
                if target_key:
                    break
            if target_key:
                break
        self.assertIsNotNone(target_key)
        # drag: delete source, place target
        r_del = self.client.delete('/api/timetable/cells', json={'key': src_key})
        self.assertEqual(r_del.status_code, 200)
        r_put = self.client.post('/api/timetable/cells',
                                 json={'key': target_key,
                                       'subject_id': cell['subject_id'],
                                       'teacher_id': cell['teacher_id']})
        self.assertEqual(r_put.status_code, 200)

        # explicit whole-draft save with the current revision
        fresh = self._state()
        r = self.client.put('/api/timetable/state', json={
            'state': fresh, 'base_revision': fresh['revision']})
        self.assertEqual(r.status_code, 200)
        self.assertGreater(r.get_json()['state']['revision'], revision)

        # browser restart: fresh read keeps the moved lesson
        reloaded = self._state()
        self.assertIn(target_key, reloaded['grid'])
        self.assertNotIn(src_key, reloaded['grid'])
        self.assertEqual(reloaded['grid'][target_key]['subject_id'],
                         cell['subject_id'])

    def test_02_concurrent_editor_conflict_rejected(self):
        """Stale revision must never silently overwrite another editor's work."""
        self.client.post('/api/timetable/auto-assign')
        stale_state = self._state()  # revision N
        # another editor saves first (revision moves to N+1)
        r = self.client.put('/api/timetable/state', json={
            'state': self._state(), 'base_revision': stale_state['revision']})
        self.assertEqual(r.status_code, 200)
        # stale editor now saves with its old revision -> 409
        r2 = self.client.put('/api/timetable/state', json={
            'state': stale_state, 'base_revision': stale_state['revision']})
        self.assertEqual(r2.status_code, 409)
        body = r2.get_json()
        self.assertEqual(body['error'], 'save-conflict')
        self.assertGreater(body['current_revision'], stale_state['revision'])

    # ── criteria 4, 11: publish + conflict block ───────────────────────────
    def test_03_publish_blocked_by_teacher_double_booking(self):
        self.client.post('/api/timetable/auto-assign')
        state = self._state()
        # introduce a teacher double-booking: same teacher, same day/shift/period,
        # two different classes
        keys = sorted(state['grid'].keys())
        first_key = keys[0]
        cell = dict(state['grid'][first_key])
        parts = first_key.split('|')
        clash_key = None
        for k in keys[1:]:
            p = k.split('|')
            same_slot = (p[0], p[1], p[2]) == (parts[0], parts[1], parts[2])
            other_class = p[3] != parts[3]
            if same_slot and other_class:
                clash_key = k
                break
        if clash_key:
            state['grid'][clash_key] = {**state['grid'][clash_key],
                                        'teacher_id': cell['teacher_id']}
            r = self.client.put('/api/timetable/state', json={
                'state': state, 'base_revision': state['revision']})
            self.assertEqual(r.status_code, 200)
            r2 = self.client.post('/api/timetable/publish', json={'published_by': 'Principal'})
            self.assertEqual(r2.status_code, 409)
            self.assertTrue(r2.get_json().get('conflicts'))
            return
        self.skipTest('no second class shares a slot with the first placed lesson')

    def test_04_incomplete_timetable_requires_explicit_confirmation(self):
        # fresh seed: most lessons unscheduled
        r = self.client.post('/api/timetable/publish', json={'published_by': 'Principal'})
        self.assertEqual(r.status_code, 409)
        body = r.get_json()
        self.assertTrue(body.get('requires_confirmation'))
        self.assertGreater(body.get('unassigned', 0), 0)
        # explicit confirmation publishes it
        r2 = self.client.post('/api/timetable/publish', json={
            'published_by': 'Principal', 'force': True, 'note': 'partial publish'})
        self.assertEqual(r2.status_code, 200)

    # ── criteria 4-7: publish → portals see correct data ────────────────────
    def test_05_publish_snapshot_and_portal_distribution(self):
        r = self._auto_assign_and_publish()
        self.assertEqual(r.status_code, 200)
        body = r.get_json()
        pub = body['published']
        self.assertEqual(pub['version'], 1)
        self.assertEqual(pub['effective_from'], '2026-11-15')
        self.assertEqual(pub['published_by'], 'Principal')
        aff = body['affected']
        self.assertEqual(aff['classes'], 12)
        self.assertGreater(aff['teachers'], 0)
        self.assertGreater(aff['students'], 0)

        # teacher portal: only their own lessons, with day/time/subject/class/room
        grid_cells = list(pub['grid'].values())
        some_teacher = grid_cells[0]['teacher_id']
        t = self.client.get(
            f'/api/timetable/published/teacher/{some_teacher}').get_json()
        self.assertTrue(t['success'])
        self.assertGreater(len(t['lessons']), 0)
        for lesson in t['lessons']:
            self.assertEqual(lesson['teacher_id'], some_teacher)
            for field in ('day', 'shift', 'period', 'class_display',
                          'subject_name', 'room'):
                self.assertIn(field, lesson)

        # student portal: their class timetable
        some_class = grid_cells[0]['class_id']
        c = self.client.get(f'/api/timetable/published/class/{some_class}').get_json()
        self.assertTrue(c['success'])
        self.assertGreater(len(c['lessons']), 0)
        for lesson in c['lessons']:
            self.assertEqual(lesson['class_id'], some_class)
            self.assertTrue(lesson.get('teacher_name'))

        # another class's portal must NOT contain lessons of other classes
        other = next(cl['id'] for cl in pub['classes'] if cl['id'] != some_class)
        c2 = self.client.get(f'/api/timetable/published/class/{other}').get_json()
        for lesson in c2['lessons']:
            self.assertEqual(lesson['class_id'], other)

    def test_06_no_publication_returns_404_never_draft(self):
        """Portals must never receive unpublished draft data."""
        self.client.post('/api/timetable/auto-assign')  # draft full, unpublished
        state = self._state()
        some_teacher = list(state['grid'].values())[0]['teacher_id']
        some_class = state['classes'][0]['id']
        r1 = self.client.get(f'/api/timetable/published/teacher/{some_teacher}')
        self.assertEqual(r1.status_code, 404)
        r2 = self.client.get(f'/api/timetable/published/class/{some_class}')
        self.assertEqual(r2.status_code, 404)

    # ── criteria 8-9: draft edits don't touch published; update republishes ─
    def test_07_draft_edits_leave_published_untouched_then_update(self):
        self._auto_assign_and_publish()
        state = self._state()
        victim = sorted(state['grid'].keys())[0]
        cell = dict(state['grid'][victim])
        original_teacher = cell['teacher_id']
        cell['teacher_id'] = self._replacement_teacher(state, victim)
        state['grid'][victim] = cell  # write the mutated copy back into the draft grid
        r = self.client.put('/api/timetable/state', json={
            'state': state, 'base_revision': state['revision']})
        self.assertEqual(r.status_code, 200)

        # published view still shows the original teacher for that slot
        t = self.client.get(f'/api/timetable/published/teacher/{original_teacher}').get_json()
        self.assertIn(victim, [l['key'] for l in t['lessons']])

        # draft vs published diff registers the change
        diff = self.client.get('/api/timetable/publication/diff').get_json()['diff']
        self.assertEqual(diff['modified'], 1)
        self.assertEqual(diff['published_version'], 1)

        # publish the update → v2 on portals
        r2 = self.client.post('/api/timetable/publish', json={
            'published_by': 'Principal', 'note': 'swap teacher'})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r2.get_json()['published']['version'], 2)
        t2 = self.client.get(f'/api/timetable/published/teacher/{cell["teacher_id"]}').get_json()
        self.assertIn(victim, [l['key'] for l in t2['lessons']])

    # ── criterion 10: restore an earlier version ────────────────────────────
    def test_08_rollback_restores_previous_version(self):
        self._auto_assign_and_publish()                     # v1
        state = self._state()
        victim = sorted(state['grid'].keys())[0]
        original_teacher = state['grid'][victim]['teacher_id']
        state['grid'][victim]['teacher_id'] = self._replacement_teacher(state, victim)
        self.client.put('/api/timetable/state', json={
            'state': state, 'base_revision': state['revision']})
        self.client.post('/api/timetable/publish', json={'published_by': 'Principal'})  # v2

        # portals now show v2 (teacher changed)
        t_v2 = self.client.get(f'/api/timetable/published/teacher/{original_teacher}').get_json()
        self.assertNotIn(victim, [l['key'] for l in t_v2['lessons']])

        # restore v1 (audited) → portals show v1 again
        r = self.client.post('/api/timetable/publication/rollback',
                             json={'version': 1, 'published_by': 'Principal'})
        self.assertEqual(r.status_code, 200)
        snap = r.get_json()['published']
        self.assertEqual(snap['version'], 3)
        self.assertEqual(snap.get('restored_from'), 1)

        t_restored = self.client.get(
            f'/api/timetable/published/teacher/{original_teacher}').get_json()
        self.assertIn(victim, [l['key'] for l in t_restored['lessons']])

        # draft was rebased on the restored grid too
        fresh = self._state()
        self.assertEqual(fresh['grid'][victim]['teacher_id'], original_teacher)

        # unknown version rejected
        r404 = self.client.post('/api/timetable/publication/rollback',
                                json={'version': 99, 'published_by': 'Principal'})
        self.assertEqual(r404.status_code, 404)

    # ── criterion 12: admin monitoring + audit history ──────────────────────
    def test_09_publication_status_history_and_oversight(self):
        self._auto_assign_and_publish()
        st = self.client.get('/api/timetable/publication/status').get_json()
        self.assertEqual(st['published']['version'], 1)
        self.assertEqual(st['published']['published_by'], 'Principal')
        self.assertEqual(st['published']['effective_from'], '2026-11-15')
        self.assertEqual(len(st['history']), 1)
        self.assertEqual(st['history'][0]['action'], 'publish')
        self.assertIn('published_by', st['history'][0])
        self.assertFalse(st['history'][0].get('snapshot'), 'history metadata must not leak the grid')

        # oversight monitoring includes the publication block
        o = self.client.get('/api/timetable/oversight/status').get_json()
        pub = o.get('publication')
        self.assertTrue(pub)
        self.assertEqual(pub['status'], 'published')
        self.assertEqual(pub['version'], 1)
        self.assertEqual(pub['published_by'], 'Principal')
        self.assertTrue(pub['draft_updated_at'])

    def test_10_publication_status_before_any_publish(self):
        st = self.client.get('/api/timetable/publication/status').get_json()
        self.assertIsNone(st['published'])
        self.assertFalse(st['diff']['has_published'])
        self.assertEqual(st['history'], [])

    # ── page wiring ─────────────────────────────────────────────────────────
    def test_11_builder_pages_load_publication_assets(self):
        html = open(os.path.join(ROOT, 'pages/principal/principal-timetable-builder.html'),
                    encoding='utf-8').read()
        # version-tolerant: the page must reference the shared suite assets
        # (cache-busting query version may evolve independently)
        import re as _re
        for asset in ('khmer-suite-engine\\.js\\?v=[0-9.]+',
                      'khmer-suite-ui\\.js\\?v=[0-9.]+',
                      'khmer-suite\\.css\\?v=[0-9.]+'):
            self.assertRegex(html, asset)
        # Admin portal has NO duplicate timetable editor — monitoring only.
        self.assertFalse(os.path.exists(os.path.join(
            ROOT, 'pages/admin/admin-timetable-builder.html')),
            'admin timetable builder must be removed (monitoring is read-only)')

    def test_12_ui_implementation_covers_workflow(self):
        js = open(os.path.join(ROOT, 'assets/js/khmer-suite-ui.js'),
                  encoding='utf-8').read()
        for frag in ('saveStatusChipHtml', 'compare-publication',
                     'publication-history', 'restore-version',
                     'ks-publish-date', 'ks-publish-force',
                     'ks-mobile-actionbar', 'execute-publish'):
            self.assertIn(frag, js)
        css = open(os.path.join(ROOT, 'assets/css/khmer-suite.css'),
                   encoding='utf-8').read()
        self.assertIn('position: sticky', css)
        self.assertIn('ks-mobile-actionbar', css)
        # student/teacher portals never render draft fallbacks
        for portal in ('pages/student/student-timetable.html',
                       'pages/teacher/teacher-timetable.html'):
            src = open(os.path.join(ROOT, portal), encoding='utf-8').read()
            self.assertNotIn("Fallback to active state", src, portal)
            self.assertIn('Not Published Yet', src, portal)


if __name__ == '__main__':
    unittest.main(verbosity=2)
