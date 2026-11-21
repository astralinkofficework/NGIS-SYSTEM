"""Roles & Access Control API — centralized role and permission administration.

Architecture (mirrors user_management_api.py conventions):
  1. Permission registry — a static, server-authoritative definition of every
     REAL module in NGIS-SYSTEM with only the actions each module actually
     implements. Nothing is permission-gated that does not exist.
  2. Core roles (Super Admin / Admin / Principal / Teacher / Staff / Student)
     are protected system identities: their baselines are defined here and can
     never be edited, archived, or escalated through this API. Custom roles
     extend capabilities; they never replace institutional identity.
  3. Custom roles + member assignments persist in data/roles_permissions.json.
     Member assignment stores the account USERNAME reference — the person's
     institutional record and core account type remain untouched.
  4. Every permission save creates a revision (rollback-able) and an audit
     event. Audit records carry before/after values and never contain secrets.

Security model (enforced SERVER-SIDE on every request):
  - Deny by default: write operations require an active ADMIN or SUPER_ADMIN
    actor (resolved against the identity store) or an assigned custom role
    that carries the roles-access manage permission.
  - Only SUPER_ADMIN actors may grant the privilege-chain actions
    (roles-access manage, login-security manage) — an ordinary Admin cannot
    create a role that grants authority over roles or credentials.
  - Self-escalation is blocked: an actor cannot assign a custom role to their
    own account, and SUPER_ADMIN accounts cannot receive custom roles.
  - No client-supplied role id is trusted: ids are generated server-side and
    validated on every reference.
"""
import json
import os
import re
import secrets
import time
import urllib.parse
from datetime import datetime

from flask import Blueprint, jsonify, request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
STORE_PATH = os.path.join(DATA_DIR, 'roles_permissions.json')
STORE_SCHEMA_VERSION = 1

roles_mgmt_bp = Blueprint('roles_mgmt', __name__, url_prefix='/api/roles-mgmt')

# ── permission registry (real modules only) ───────────────────────────────

ACTION_LABELS = {
    'view': 'View', 'create': 'Create', 'edit': 'Edit', 'delete': 'Delete',
    'approve': 'Approve', 'reject': 'Reject', 'publish': 'Publish',
    'upload': 'Upload', 'download': 'Download',
    'export': 'Export', 'import': 'Import', 'manage': 'Manage',
}

PERMISSION_MODULES = {
    'User & Access': {
        'user-management': ('User Management', ['view', 'manage']),
        'account-directories': ('Account Directories', ['view', 'create', 'edit', 'export', 'import', 'manage']),
        'roles-access': ('Roles & Access Control', ['view', 'manage']),
        'login-security': ('Login & Security', ['view', 'manage']),
    },
    'Academic': {
        'student-profiles': ('Student Profiles', ['view', 'create', 'edit', 'export', 'download']),
        'teacher-profiles': ('Teacher Profiles', ['view', 'create', 'edit']),
        'attendance': ('Attendance', ['view', 'create', 'edit', 'export']),
        'absence-stats': ('Absence Statistics', ['view', 'export']),
        'grades': ('Grades', ['view', 'edit', 'approve', 'publish']),
        'report-cards': ('Report Cards', ['view', 'publish', 'export', 'download']),
        'assignments': ('Assignments', ['view', 'create', 'edit', 'delete', 'upload', 'download']),
        'lessons': ('Lessons', ['view', 'create', 'edit', 'upload', 'download']),
        'exams': ('Exams', ['view', 'edit', 'publish']),
        'timetable': ('Timetable', ['view', 'edit', 'approve', 'publish', 'export']),
        'curriculum': ('Curriculum', ['view', 'edit', 'manage']),
        'classes': ('Classes', ['view', 'edit']),
        'departments': ('Departments', ['view', 'edit']),
        'campuses': ('Campuses', ['view', 'edit']),
    },
    'School Operations': {
        'school-information': ('School Information', ['view', 'edit']),
        'announcements': ('Announcements', ['view', 'create', 'edit', 'publish', 'delete', 'download']),
        'news': ('News CMS', ['view', 'create', 'edit', 'publish', 'delete']),
        'dashboard-content': ('Dashboard Content', ['view', 'edit', 'publish']),
        'services': ('Student Services', ['view', 'create', 'edit', 'approve', 'reject', 'upload', 'download']),
        'certificates': ('Certificates', ['view', 'create', 'publish', 'export', 'download']),
        'reports': ('Academic Reports', ['view', 'export', 'download']),
    },
    'System Administration': {
        'audit-logs': ('Audit Logs', ['view', 'export', 'download']),
        'system-configuration': ('System Configuration', ['view', 'edit', 'manage']),
        'system-monitoring': ('System Monitoring', ['view']),
    },
}

# Privilege-chain actions: granting these requires SUPER_ADMIN authority,
# otherwise an ordinary admin could mint a role that controls roles or
# credentials — an escalation path.
PRIVILEGE_CHAIN_RULES = {('roles-access', 'manage'), ('login-security', 'manage')}

ALL_ACTIONS = ['view', 'create', 'edit', 'delete', 'approve', 'reject',
               'publish', 'upload', 'download', 'export', 'import', 'manage']

CORE_ROLES = ('SUPER_ADMIN', 'ADMIN', 'PRINCIPAL', 'TEACHER', 'STAFF', 'STUDENT')

# Baseline capabilities the core roles already hold in the application.
CORE_BASELINES = {
    'SUPER_ADMIN': 'all',
    'ADMIN': {
        'user-management': ['view', 'manage'],
        'account-directories': ['view', 'create', 'edit', 'export', 'import', 'manage'],
        'roles-access': ['view'],
        'login-security': ['view'],
        'student-profiles': ['view', 'create', 'edit', 'export'],
        'teacher-profiles': ['view', 'create', 'edit'],
        'attendance': ['view', 'create', 'edit', 'export'],
        'absence-stats': ['view', 'export'],
        'grades': ['view', 'edit', 'approve', 'publish'],
        'report-cards': ['view', 'publish', 'export'],
        'assignments': ['view', 'create', 'edit', 'delete'],
        'lessons': ['view', 'create', 'edit'],
        'exams': ['view', 'edit', 'publish'],
        'timetable': ['view', 'edit', 'approve', 'publish', 'export'],
        'curriculum': ['view', 'edit', 'manage'],
        'classes': ['view', 'edit'],
        'departments': ['view', 'edit'],
        'campuses': ['view', 'edit'],
        'school-information': ['view', 'edit'],
        'announcements': ['view', 'create', 'edit', 'publish', 'delete'],
        'news': ['view', 'create', 'edit', 'publish', 'delete'],
        'dashboard-content': ['view', 'edit', 'publish'],
        'services': ['view', 'create', 'edit', 'approve', 'reject'],
        'certificates': ['view', 'create', 'publish', 'export'],
        'reports': ['view', 'export'],
        'audit-logs': ['view', 'export'],
        'system-configuration': ['view', 'edit', 'manage'],
        'system-monitoring': ['view'],
    },
    'PRINCIPAL': {
        'student-profiles': ['view', 'edit'],
        'teacher-profiles': ['view', 'edit'],
        'attendance': ['view', 'edit', 'export'],
        'absence-stats': ['view', 'export'],
        'grades': ['view', 'approve', 'publish'],
        'report-cards': ['view', 'publish', 'export'],
        'assignments': ['view'],
        'exams': ['view', 'approve', 'reject', 'publish'],
        'timetable': ['view', 'approve', 'publish'],
        'curriculum': ['view', 'edit'],
        'classes': ['view'],
        'departments': ['view'],
        'campuses': ['view'],
        'school-information': ['view'],
        'announcements': ['view', 'create', 'publish'],
        'dashboard-content': ['view'],
        'services': ['view', 'approve', 'reject'],
        'certificates': ['view', 'publish'],
        'reports': ['view', 'export'],
        'audit-logs': ['view'],
        'system-monitoring': ['view'],
    },
    'TEACHER': {
        'student-profiles': ['view'],
        'attendance': ['view', 'create', 'edit'],
        'grades': ['view', 'edit'],
        'assignments': ['view', 'create', 'edit'],
        'lessons': ['view', 'create', 'edit'],
        'exams': ['view', 'create', 'edit'],
        'timetable': ['view'],
        'curriculum': ['view'],
        'announcements': ['view'],
        'reports': ['view'],
    },
    'STAFF': {
        'student-profiles': ['view'],
        'attendance': ['view'],
        'services': ['view', 'create'],
        'announcements': ['view'],
        'school-information': ['view'],
    },
    'STUDENT': {},
}

SCOPE_OPTIONS = {
    'campuses': ['Sensok', 'TK', 'Sensok & TK', 'Tuol Kork Main Campus',
                 'Chamkarmon High School Branch', 'STEM & Robotics Innovation Hub',
                 'All campuses'],
    'departments': ['Administration', 'Mathematics', 'Science', 'Languages',
                    'Campus Operations', 'ICT & Innovation', 'Physical Education'],
}


# ── store helpers ─────────────────────────────────────────────────────────

def _now():
    return datetime.now()


def _ts():
    return _now().strftime('%Y-%m-%d %H:%M')


def _load_json(filename, default):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, encoding='utf-8') as fh:
                return json.load(fh)
        except (ValueError, OSError):
            pass
    return default


def _save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    tmp = f'{path}.{os.getpid()}.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    for attempt in range(8):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 7:
                with open(path, 'w', encoding='utf-8') as fh:
                    json.dump(data, fh, indent=2, ensure_ascii=False)
                try:
                    os.remove(tmp)
                except OSError:
                    pass
                return
            time.sleep(0.03 * (attempt + 1))


def _actor():
    # Read-only demo browsing falls back to the admin persona so the control
    # centre remains explorable without a login. WRITE paths must never use
    # this fallback — see _explicit_actor() / _guard_write().
    return (request.headers.get('X-Actor') or 'admin@ngis.edu.kh').strip().lower()


def _actor_cookie():
    """Read the first-party identity cookie.

    auth.js / layout.js write it with encodeURIComponent(), so a username such
    as student@ngis.edu.kh is transmitted as student%40ngis.edu.kh. Werkzeug
    does NOT URL-decode cookie values, so failing to unquote here silently
    disables enforcement (the encoded string matches no account). Decode once,
    centrally, for every read path.
    """
    raw = (request.cookies.get('ngis_actor') or '').strip()
    return urllib.parse.unquote(raw).strip().lower()


def _explicit_actor():
    """Caller-supplied identity with NO demo fallback. Mutating endpoints use
    this so an anonymous request can never inherit administrator authority."""
    return (request.headers.get('X-Actor')
            or _actor_cookie() or '').strip().lower()


def _identity_store():
    return _load_json('user_accounts.json', None) or {
        'accounts': [], 'audit_log': [], 'reset_tokens': {},
        'login_history': {}, 'resets_window': {}, 'schema_version': 1}


def _store():
    data = _load_json(os.path.basename(STORE_PATH), None)
    if not isinstance(data, dict) or data.get('schema_version') != STORE_SCHEMA_VERSION:
        data = {'schema_version': STORE_SCHEMA_VERSION,
                'custom_roles': [], 'audit_log': []}
        _save_json(os.path.basename(STORE_PATH), data)
    return data


def _save_store(data):
    data['schema_version'] = STORE_SCHEMA_VERSION
    _save_json(os.path.basename(STORE_PATH), data)


def _audit(store, actor, action, target_role=None, target_role_name='',
           target_user=None, before=None, after=None, outcome='success'):
    store.setdefault('audit_log', []).append({
        'id': f'RP-AUD-{len(store["audit_log"]) + 1:05d}',
        'ts': _ts(),
        'actor': actor,
        'action': action,
        'target_role': target_role,
        'target_role_name': target_role_name,
        'target_user': target_user,
        'before': before,
        'after': after,
        'outcome': outcome,
    })


# ── authorization guards ──────────────────────────────────────────────────

def _account_for(actor, idstore):
    return next((a for a in idstore.get('accounts', [])
                 if a.get('username', '').lower() == actor), None)


def _has_custom_permission(account, module, action):
    for rid in (account or {}).get('custom_roles', []):
        role = next((r for r in _store().get('custom_roles', []) if r['id'] == rid), None)
        if role and role.get('status') == 'active':
            if action in (role.get('permissions') or {}).get(module, []):
                return True
    return False


def _actor_is_super(actor, idstore):
    acc = _account_for(actor, idstore)
    return bool(acc) and acc.get('role') == 'SUPER_ADMIN' and acc.get('status') == 'active'


def _actor_is_admin(actor, idstore):
    acc = _account_for(actor, idstore)
    if acc and acc.get('role') in ('ADMIN', 'SUPER_ADMIN') and acc.get('status') == 'active':
        return True
    return _has_custom_permission(acc, 'roles-access', 'manage')


def _actor_can_read(actor, idstore):
    acc = _account_for(actor, idstore)
    if acc and acc.get('role') in ('ADMIN', 'SUPER_ADMIN') and acc.get('status') == 'active':
        return True
    return _has_custom_permission(acc, 'roles-access', 'view')


def _guard_read(store, idstore):
    actor = _actor()
    if not _actor_can_read(actor, idstore):
        return actor, jsonify({'success': False, 'error':
                               'Only active administrators or delegated roles may access Roles & Access Control'}), 403
    return actor, None, None


def _guard_write(store, idstore):
    actor = _explicit_actor()
    if not actor:
        return actor, jsonify({'success': False, 'error':
                               'An authenticated administrator session is required to modify roles and permissions'}), 401
    if not _actor_is_admin(actor, idstore):
        return actor, jsonify({'success': False, 'error':
                               'Only active administrators or delegated roles may modify roles and permissions'}), 403
    return actor, None, None


def _guard_privilege_chain(payload, actor, idstore):
    """Only SUPER_ADMIN may grant privilege-chain actions to any role."""
    if _actor_is_super(actor, idstore):
        return None
    added = (payload or {}).get('added_permissions') or []
    for item in added:
        if (item.get('module'), item.get('action')) in PRIVILEGE_CHAIN_RULES:
            return jsonify({'success': False, 'error':
                            f'Granting "{item["action"]}" on "{item["module"]}" requires SUPER_ADMIN authority'}), 403
    perms = (payload or {}).get('permissions')
    if isinstance(perms, dict):
        for module, actions in perms.items():
            for action in actions or []:
                if (module, action) in PRIVILEGE_CHAIN_RULES:
                    return jsonify({'success': False, 'error':
                                    f'Granting "{action}" on "{module}" requires SUPER_ADMIN authority'}), 403
    return None


# ── permission validation ─────────────────────────────────────────────────

def _validate_permissions(perms):
    """Validate a permission dict against the registry (deny unknown modules
    and unsupported actions). Returns (clean, error_response)."""
    if not isinstance(perms, dict):
        return {}, jsonify({'success': False, 'error': 'permissions must be an object'}), 400
    clean = {}
    for category, modules in PERMISSION_MODULES.items():
        for module_id, (label, actions) in modules.items():
            wanted = perms.get(module_id)
            if not wanted:
                continue
            if not isinstance(wanted, list):
                return {}, jsonify({'success': False,
                                    'error': f'permissions for "{module_id}" must be a list'}), 400
            unknown = [a for a in wanted if a not in actions]
            if unknown:
                return {}, jsonify({'success': False, 'error':
                                    f'Module "{label}" does not support action(s): {", ".join(unknown)}'}), 400
            deduped = sorted(set(wanted))
            if deduped:
                clean[module_id] = deduped
            # dependency: any non-view action requires view
    for module_id, actions in list(clean.items()):
        if actions != ['view'] and 'view' not in actions:
            clean[module_id] = ['view'] + actions
    return clean, None, None


def _validate_scopes(scopes):
    if not isinstance(scopes, dict):
        return {'campuses': [], 'departments': []}
    campuses = [c for c in (scopes.get('campuses') or []) if c in SCOPE_OPTIONS['campuses']]
    departments = [d for d in (scopes.get('departments') or []) if d in SCOPE_OPTIONS['departments']]
    return {'campuses': campuses, 'departments': departments}


def _next_role_id(store):
    nums = [int(m.group(1)) for r in store['custom_roles']
            for m in [re.match(r'^ROL-(\d+)$', r.get('id', ''))] if m]
    return f'ROL-{max(nums or [0]) + 1:03d}'


def _diff_permissions(before, after):
    added, removed = [], []
    modules = set(list(before.keys()) + list(after.keys()))
    for module in sorted(modules):
        b = set((before or {}).get(module, []))
        a = set((after or {}).get(module, []))
        for action in sorted(a - b):
            added.append({'module': module, 'action': action})
        for action in sorted(b - a):
            removed.append({'module': module, 'action': action})
    return added, removed


def _core_baseline(core_role):
    base = CORE_BASELINES.get(core_role, {})
    if base == 'all':
        out = {}
        for modules in PERMISSION_MODULES.values():
            for module_id, (_label, actions) in modules.items():
                out[module_id] = sorted(actions)
        return out
    return {k: sorted(v) for k, v in (base or {}).items()}


def _effective_for_account(account, idstore):
    """Effective permissions = core baseline ∪ assigned active custom roles.
    This is THE evaluation used by the inspector and the guards alike."""
    core = account.get('role', 'STUDENT')
    effective = _core_baseline(core)
    sources = [{'type': 'core', 'name': core}]
    for rid in account.get('custom_roles', []):
        role = next((r for r in _store().get('custom_roles', [])
                     if r['id'] == rid and r.get('status') == 'active'), None)
        if not role:
            continue
        sources.append({'type': 'custom', 'name': role['name'], 'id': role['id']})
        for module, actions in (role.get('permissions') or {}).items():
            merged = sorted(set(effective.get(module, [])) | set(actions))
            effective[module] = merged
    return {'role': core, 'sources': sources, 'permissions': effective}


# ── API: registry (module inventory for the matrix) ───────────────────────

@roles_mgmt_bp.route('/registry', methods=['GET'])
def registry():
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    return jsonify({'success': True, 'actor': actor,
                    'categories': [{'category': cat,
                                    'modules': [{'id': mid, 'name': label,
                                                 'actions': actions}
                                                for mid, (label, actions) in modules.items()]}
                                   for cat, modules in PERMISSION_MODULES.items()],
                    'actions': ALL_ACTIONS, 'action_labels': ACTION_LABELS,
                    'scope_options': SCOPE_OPTIONS,
                    'core_roles': list(CORE_ROLES)})


# ── API: roles CRUD ───────────────────────────────────────────────────────

def _role_summary(role, idstore):
    members = [a for a in idstore.get('accounts', [])
               if role['id'] in a.get('custom_roles', [])]
    return {'id': role['id'], 'name': role['name'],
            'description': role.get('description', ''),
            'status': role.get('status', 'active'),
            'base_role': role.get('base_role', 'ADMIN'),
            'identifier': role.get('identifier', ''),
            'category': role.get('category', 'custom'),
            'default_portal': role.get('default_portal', ''),
            'portals': role.get('portals', []),
            'updated_at': role.get('updated_at', ''),
            'scopes': role.get('scopes', {'campuses': [], 'departments': []}),
            'module_count': len(role.get('permissions') or {}),
            'action_count': sum(len(v) for v in (role.get('permissions') or {}).values()),
            'members': len(members),
            'created_by': role.get('created_by', ''),
            'created_at': role.get('created_at', ''),
            'updated_at': role.get('updated_at', ''),
            'protected': False,
            'sensitive': any((m, a) in PRIVILEGE_CHAIN_RULES
                             for m, acts in (role.get('permissions') or {}).items()
                             for a in acts)}


@roles_mgmt_bp.route('/roles', methods=['GET'])
def list_roles():
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    store = _store()
    idstore = _identity_store()
    roles = [_role_summary(r, idstore) for r in store['custom_roles']]
    search = (request.args.get('search') or '').strip().lower()
    if search:
        roles = [r for r in roles if search in r['name'].lower()
                 or search in (r['description'] or '').lower()]
    core = [{'id': cr, 'name': cr.replace('_', ' ').title(), 'protected': True,
             'status': 'active', 'members': sum(1 for a in idstore.get('accounts', [])
                                                if a.get('role') == cr),
             'description': 'Protected system role' if cr != 'SUPER_ADMIN'
             else 'Protected system authority — cannot be modified',
             'module_count': len(_core_baseline(cr)),
             'action_count': sum(len(v) for v in _core_baseline(cr).values()),
             'sensitive': cr == 'SUPER_ADMIN'}
            for cr in CORE_ROLES]
    return jsonify({'success': True, 'custom_roles': roles, 'core_roles': core})


@roles_mgmt_bp.route('/roles', methods=['POST'])
def create_role():
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    store = _store()
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    description = (payload.get('description') or '').strip()
    base_role = (payload.get('base_role') or 'ADMIN').strip().upper()
    if len(name) < 2:
        return jsonify({'success': False, 'error': 'Role name must be at least 2 characters'}), 400
    if any(r['name'].lower() == name.lower() and r.get('status') == 'active'
           for r in store['custom_roles']):
        return jsonify({'success': False, 'error': f'A role named "{name}" already exists'}), 409
    if base_role not in CORE_ROLES:
        return jsonify({'success': False, 'error': f'Unknown base role "{base_role}"'}), 400
    perms, perr, pstatus = _validate_permissions(payload.get('permissions') or {})
    if perr:
        return perr, pstatus
    chain = _guard_privilege_chain({'permissions': perms}, actor, _identity_store())
    if chain:
        return chain
    role = {'id': _next_role_id(store), 'name': name, 'description': description,
            'base_role': base_role, 'status': 'active',
            'scopes': _validate_scopes(payload.get('scopes') or {}),
            'permissions': perms, 'revisions': [],
            'created_by': actor, 'created_at': _ts(), 'updated_at': _ts()}
    store['custom_roles'].append(role)
    _audit(store, actor, 'role_created', target_role=role['id'],
           target_role_name=name, after={'permissions': perms,
                                         'base_role': base_role,
                                         'scopes': role['scopes']})
    _save_store(store)
    return jsonify({'success': True, 'message': f'Role "{name}" created',
                    'role': _role_summary(role, _identity_store())}), 201


@roles_mgmt_bp.route('/roles/<role_id>', methods=['PUT'])
def update_role(role_id):
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    store = _store()
    role = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    payload = request.get_json(silent=True) or {}
    before = {'name': role['name'], 'description': role.get('description', ''),
              'status': role.get('status'), 'scopes': role.get('scopes')}
    changes = {}
    if 'name' in payload:
        name = (payload.get('name') or '').strip()
        if len(name) < 2:
            return jsonify({'success': False, 'error': 'Role name must be at least 2 characters'}), 400
        if any(r['name'].lower() == name.lower() and r['id'] != role_id
               and r.get('status') == 'active' for r in store['custom_roles']):
            return jsonify({'success': False, 'error': f'A role named "{name}" already exists'}), 409
        if name != role['name']:
            changes['name'] = name
            role['name'] = name
    if 'description' in payload:
        role['description'] = (payload.get('description') or '').strip()
        changes['description'] = role['description']
    if 'scopes' in payload:
        role['scopes'] = _validate_scopes(payload.get('scopes') or {})
        changes['scopes'] = role['scopes']
    if 'status' in payload:
        if payload['status'] not in ('active', 'archived'):
            return jsonify({'success': False, 'error': 'Invalid status'}), 400
        role['status'] = payload['status']
        changes['status'] = role['status']
    if not changes:
        return jsonify({'success': False, 'error': 'No changes supplied'}), 400
    role['updated_at'] = _ts()
    action = 'role_archived' if changes.get('status') == 'archived' else 'role_updated'
    _audit(store, actor, action, target_role=role['id'],
           target_role_name=role['name'], before=before, after=changes)
    _save_store(store)
    return jsonify({'success': True, 'message': 'Role updated',
                    'role': _role_summary(role, _identity_store())})


@roles_mgmt_bp.route('/roles/<role_id>/duplicate', methods=['POST'])
def duplicate_role(role_id):
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    store = _store()
    source = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not source:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    base_name = f'{source["name"]} (Copy)'
    name = base_name
    n = 2
    taken = {r['name'].lower() for r in store['custom_roles']}
    while name.lower() in taken:
        name = f'{base_name} {n}'
        n += 1
    copy = dict(source)
    copy['id'] = _next_role_id(store)
    copy['name'] = name
    copy['status'] = 'active'
    copy['revisions'] = []
    copy['permissions'] = json.loads(json.dumps(source.get('permissions') or {}))
    copy['scopes'] = json.loads(json.dumps(source.get('scopes') or {}))
    copy['created_by'] = actor
    copy['created_at'] = _ts()
    copy['updated_at'] = _ts()
    store['custom_roles'].append(copy)
    _audit(store, actor, 'role_duplicated', target_role=copy['id'],
           target_role_name=name,
           after={'duplicated_from': source['id'], 'permissions': copy['permissions']})
    _save_store(store)
    return jsonify({'success': True, 'message': f'Role duplicated as "{name}"',
                    'role': _role_summary(copy, _identity_store())}), 201


# ── API: permission matrix ────────────────────────────────────────────────

@roles_mgmt_bp.route('/roles/<role_id>/permissions', methods=['GET'])
def get_permissions(role_id):
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    store = _store()
    if role_id in CORE_ROLES:
        return jsonify({'success': True, 'core_role': role_id,
                        'permissions': _core_baseline(role_id),
                        'protected': True, 'revisions': []})
    role = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    return jsonify({'success': True, 'role_id': role_id,
                    'permissions': role.get('permissions') or {},
                    'protected': False,
                    'revisions': [{'index': i, 'ts': rv.get('ts'),
                                   'actor': rv.get('actor'),
                                   'module_count': len(rv.get('permissions') or {})}
                                  for i, rv in enumerate(role.get('revisions', []))]})


@roles_mgmt_bp.route('/roles/<role_id>/permissions', methods=['PUT'])
def put_permissions(role_id):
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    store = _store()
    if role_id in CORE_ROLES:
        return jsonify({'success': False, 'error':
                        'Core system roles are protected and cannot be modified'}), 403
    role = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    payload = request.get_json(silent=True) or {}
    perms, perr, pstatus = _validate_permissions(payload.get('permissions'))
    if perr:
        return perr, pstatus
    chain = _guard_privilege_chain({'permissions': perms}, actor, idstore)
    if chain:
        return chain
    before = role.get('permissions') or {}
    added, removed = _diff_permissions(before, perms)
    # dependency validation: edit/approve/publish/manage require view
    for module, actions in perms.items():
        if any(a != 'view' for a in actions) and 'view' not in actions:
            return jsonify({'success': False, 'error':
                            f'"{module}" requires View before other actions'}), 400
    members = [a for a in idstore.get('accounts', []) if role_id in a.get('custom_roles', [])]
    # revision history (previous config) — capped
    role.setdefault('revisions', []).append(
        {'ts': _ts(), 'actor': actor, 'permissions': json.loads(json.dumps(before))})
    if len(role['revisions']) > 20:
        role['revisions'] = role['revisions'][-20:]
    role['permissions'] = perms
    role['updated_at'] = _ts()
    _audit(store, actor, 'permissions_updated', target_role=role['id'],
           target_role_name=role['name'],
           before={'permissions': before}, after={'permissions': perms})
    _save_store(store)
    return jsonify({'success': True, 'message': 'Permissions saved',
                    'added': added, 'removed': removed,
                    'affected_users': len(members),
                    'permissions': perms})


@roles_mgmt_bp.route('/roles/<role_id>/rollback', methods=['POST'])
def rollback_role(role_id):
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    store = _store()
    if role_id in CORE_ROLES:
        return jsonify({'success': False, 'error': 'Core roles are protected'}), 403
    role = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    payload = request.get_json(silent=True) or {}
    try:
        index = int(payload.get('revision_index'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'revision_index is required'}), 400
    revisions = role.get('revisions', [])
    if index < 0 or index >= len(revisions):
        return jsonify({'success': False, 'error': 'Revision not found'}), 404
    restore = revisions[index]['permissions']
    before = role.get('permissions') or {}
    added, removed = _diff_permissions(before, restore)
    role.setdefault('revisions', []).append(
        {'ts': _ts(), 'actor': actor, 'permissions': json.loads(json.dumps(before))})
    role['permissions'] = json.loads(json.dumps(restore))
    role['updated_at'] = _ts()
    _audit(store, actor, 'permissions_rolled_back', target_role=role['id'],
           target_role_name=role['name'],
           before={'revision_index': index, 'permissions': before},
           after={'permissions': restore})
    _save_store(store)
    return jsonify({'success': True, 'message': 'Permissions restored from revision',
                    'added': added, 'removed': removed, 'permissions': role['permissions']})


# ── API: members (assign existing accounts) ───────────────────────────────

@roles_mgmt_bp.route('/roles/<role_id>/members', methods=['GET'])
def list_members(role_id):
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    if role_id in CORE_ROLES:
        members = [{'username': a['username'], 'name': a.get('name', ''),
                    'person_id': a.get('person_id'), 'person_type': a.get('person_type'),
                    'campus': a.get('campus', ''), 'status': a.get('status', ''),
                    'assignment': 'core', 'assigned_by': 'system'}
                   for a in idstore.get('accounts', []) if a.get('role') == role_id]
        return jsonify({'success': True, 'core_role': role_id, 'members': members})
    role = next((r for r in _store()['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    members = [{'username': a['username'], 'name': a.get('name', ''),
                'person_id': a.get('person_id'), 'person_type': a.get('person_type'),
                'campus': a.get('campus', ''), 'status': a.get('status', ''),
                'assignment': 'custom', 'assigned_by': a.get('custom_roles_meta', {}).get(role_id, {}).get('assigned_by', '')
                if isinstance(a.get('custom_roles_meta'), dict) else ''}
               for a in idstore.get('accounts', []) if role_id in a.get('custom_roles', [])]
    # eligible accounts for the assign picker (active, not super admin)
    eligible = [{'username': a['username'], 'name': a.get('name', ''),
                 'person_type': a.get('person_type'), 'campus': a.get('campus', ''),
                 'current_role': a.get('role')}
                for a in idstore.get('accounts', [])
                if a.get('status') == 'active' and a.get('role') != 'SUPER_ADMIN'
                and role_id not in a.get('custom_roles', [])]
    return jsonify({'success': True, 'members': members, 'eligible': eligible})


@roles_mgmt_bp.route('/roles/<role_id>/members', methods=['POST'])
def assign_member(role_id):
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    store = _store()
    role = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    if role.get('status') != 'active':
        return jsonify({'success': False, 'error': 'Archived roles cannot receive members'}), 409
    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or '').strip().lower()
    account = next((a for a in idstore.get('accounts', [])
                    if a.get('username', '').lower() == username), None)
    if not account:
        return jsonify({'success': False, 'error': f'No account "{username}" found'}), 404
    if account.get('role') == 'SUPER_ADMIN':
        return jsonify({'success': False, 'error':
                        'Super Admin accounts cannot receive custom roles'}), 403
    if username == actor:
        return jsonify({'success': False, 'error':
                        'Self-assignment of roles is blocked'}), 403
    if role_id in account.get('custom_roles', []):
        return jsonify({'success': False, 'error': 'User already holds this role'}), 409
    account.setdefault('custom_roles', []).append(role_id)
    account.setdefault('custom_roles_meta', {})[role_id] = {
        'assigned_by': actor, 'assigned_at': _ts()}
    _audit_identity(idstore, actor, 'custom_role_assigned', account, role)
    _save_json('user_accounts.json', idstore)
    _audit(store, actor, 'user_assigned', target_role=role['id'],
           target_role_name=role['name'], target_user=username,
           after={'role': role_id})
    _save_store(store)
    return jsonify({'success': True, 'message': f'{username} assigned to {role["name"]}'})


@roles_mgmt_bp.route('/roles/<role_id>/members/remove', methods=['POST'])
def remove_member(role_id):
    actor, err, status = _guard_write(None, _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    store = _store()
    role = next((r for r in store['custom_roles'] if r['id'] == role_id), None)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    payload = request.get_json(silent=True) or {}
    username = (payload.get('username') or '').strip().lower()
    account = next((a for a in idstore.get('accounts', [])
                    if a.get('username', '').lower() == username), None)
    if not account or role_id not in account.get('custom_roles', []):
        return jsonify({'success': False, 'error': 'User does not hold this role'}), 404
    account['custom_roles'].remove(role_id)
    if isinstance(account.get('custom_roles_meta'), dict):
        account['custom_roles_meta'].pop(role_id, None)
    _audit_identity(idstore, actor, 'custom_role_removed', account, role)
    _save_json('user_accounts.json', idstore)
    _audit(store, actor, 'user_removed', target_role=role['id'],
           target_role_name=role['name'], target_user=username,
           before={'role': role_id})
    _save_store(store)
    return jsonify({'success': True, 'message': f'{username} removed from {role["name"]}'})


def _audit_identity(idstore, actor, action, account, role):
    idstore.setdefault('audit_log', []).append({
        'id': f'AUD-{len(idstore["audit_log"]) + 1:05d}',
        'ts': _ts(), 'actor': actor, 'action': action,
        'target': account.get('id'), 'target_name': account.get('name', ''),
        'scope': account.get('campus', ''), 'outcome': 'success',
        'details': {'role_id': role['id'], 'role_name': role['name']},
    })


# ── API: access inspector (same evaluation as the guards) ─────────────────

@roles_mgmt_bp.route('/effective/<username>', methods=['GET'])
def effective_permissions(username):
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    uname = (username or '').strip().lower()
    account = next((a for a in idstore.get('accounts', [])
                    if a.get('username', '').lower() == uname), None)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    eff = _effective_for_account(account, idstore)
    restricted = []
    for cat, modules in PERMISSION_MODULES.items():
        for mid, (label, actions) in modules.items():
            granted = eff['permissions'].get(mid, [])
            if granted:
                restricted.append({'module': mid, 'label': label,
                                   'category': cat,
                                   'actions': granted,
                                   'source': _perm_source(eff['sources'], mid)})
    # Portal / page / action view of the SAME resolver used by the sidebar and
    # the direct-URL gate, so the inspector can never disagree with enforcement.
    store = _store()
    overrides = (store.get('user_overrides') or {}).get(uname, {}) or {}
    resolved = _resolve_access(account, overrides)
    return jsonify({'success': True,
                    'username': account.get('username'),
                    'name': account.get('name', ''),
                    'person_type': account.get('person_type'),
                    'campus': account.get('campus', ''),
                    'department': account.get('department', ''),
                    'core_role': eff['role'],
                    'sources': eff['sources'],
                    'custom_roles': account.get('custom_roles', []),
                    'accessible': restricted,
                    'protected': resolved['protected'],
                    'portals': resolved['portals'],
                    'pages': resolved['pages'],
                    'action_permissions': resolved['permissions'],
                    'hidden_keys': resolved['hidden_keys'],
                    'denied_keys': resolved['denied_keys'],
                    'overrides': overrides})


def _perm_source(sources, module):
    """Return the permission source for a module (core baseline or custom role)."""
    core = _core_baseline(sources[0]['name']) if sources else {}
    custom_names = [s['name'] for s in sources if s.get('type') == 'custom'
                    and module in (next((r for r in _store()['custom_roles']
                                         if r['id'] == s.get('id')), {})
                                   or {}).get('permissions', {})]
    if module in core and custom_names:
        return f'core {sources[0]["name"]} + {", ".join(custom_names)}'
    if custom_names:
        return f'custom role: {", ".join(custom_names)}'
    if module in core:
        return f'core {sources[0]["name"]} baseline'
    return 'not granted'


# ── API: compare roles ────────────────────────────────────────────────────

@roles_mgmt_bp.route('/compare', methods=['GET'])
def compare_roles():
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    a = (request.args.get('a') or '').strip()
    b = (request.args.get('b') or '').strip()
    store = _store()

    def perms_for(rid):
        if rid in CORE_ROLES:
            return _core_baseline(rid), rid
        role = next((r for r in store['custom_roles'] if r['id'] == rid), None)
        if not role:
            return None, rid
        return role.get('permissions') or {}, role['name']

    pa, na = perms_for(a)
    pb, nb = perms_for(b)
    if pa is None or pb is None:
        return jsonify({'success': False, 'error': 'Both roles must exist'}), 404
    modules = {}
    for cat, mods in PERMISSION_MODULES.items():
        for mid, (label, _acts) in mods.items():
            av = sorted(set(pa.get(mid, [])))
            bv = sorted(set(pb.get(mid, [])))
            if av or bv:
                modules.setdefault(cat, []).append(
                    {'module': mid, 'label': label, 'a': av, 'b': bv,
                     'only_a': sorted(set(av) - set(bv)), 'only_b': sorted(set(bv) - set(av))})
    return jsonify({'success': True, 'a': {'id': a, 'name': na},
                    'b': {'id': b, 'name': nb}, 'modules': modules})


# ── API: audit history ────────────────────────────────────────────────────

@roles_mgmt_bp.route('/audit', methods=['GET'])
def audit_history():
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    store = _store()
    entries = list(reversed(store.get('audit_log', [])))
    action = (request.args.get('action') or '').strip()
    role_id = (request.args.get('role') or '').strip()
    search = (request.args.get('search') or '').strip().lower()
    if action:
        entries = [e for e in entries if e['action'] == action]
    if role_id:
        entries = [e for e in entries if e.get('target_role') == role_id]
    if search:
        entries = [e for e in entries if search in json.dumps(e).lower()]
    return jsonify({'success': True, 'data': entries[:100],
                    'total': len(store.get('audit_log', []))})


# ── API: access review overview ───────────────────────────────────────────

@roles_mgmt_bp.route('/overview', methods=['GET'])
def roles_overview():
    actor, err, status = _guard_read(None, _identity_store())
    if err:
        return err, status
    store = _store()
    idstore = _identity_store()
    custom = store['custom_roles']
    members_by_role = {r['id']: [a for a in idstore.get('accounts', [])
                                 if r['id'] in a.get('custom_roles', [])]
                       for r in custom}
    high_privilege = [r for r in custom
                      if any((m, a) in PRIVILEGE_CHAIN_RULES
                             for m, acts in (r.get('permissions') or {}).items()
                             for a in acts)]
    return jsonify({'success': True,
                    'metrics': {'customRoles': len(custom),
                                'activeRoles': sum(1 for r in custom if r.get('status') == 'active'),
                                'archivedRoles': sum(1 for r in custom if r.get('status') == 'archived'),
                                'unassignedRoles': sum(1 for r in custom if not members_by_role[r['id']]),
                                'totalAssignments': sum(len(v) for v in members_by_role.values()),
                                'highPrivilegeRoles': len(high_privilege)},
                    'roles_without_members': [r['name'] for r in custom if not members_by_role[r['id']]],
                    'high_privilege': [{'id': r['id'], 'name': r['name']} for r in high_privilege],
                    'recently_modified': sorted(
                        [{'id': r['id'], 'name': r['name'], 'updated_at': r.get('updated_at', '')}
                         for r in custom], key=lambda x: x['updated_at'], reverse=True)[:5]})


# ── USER ACCESS & VISIBILITY CONTROL ─────────────────────────────────────
# Page inventory is derived from the published sidebar configuration so every
# real page across every portal is manageable. Per-user overrides use a
# tri-state (inherit / allow / deny) and are resolved with a strict
# precedence: explicit deny > explicit allow > custom role > core baseline.
# Protected system restrictions (denied portal, SUPER_ADMIN identity) always
# win. Nothing here is a cosmetic sidebar flag — the same resolver feeds the
# direct-URL gate consumed by protect.js.

NAV_PATH = os.path.join(DATA_DIR, 'sidebar_nav.json')
PORTAL_KEYS = ('admin', 'principal', 'teacher', 'student', 'staff', 'superadmin')
PORTAL_BY_CORE_ROLE = {
    'SUPER_ADMIN': 'superadmin', 'ADMIN': 'admin', 'PRINCIPAL': 'principal',
    'TEACHER': 'teacher', 'STAFF': 'staff', 'STUDENT': 'student',
}
TRISTATE = ('inherit', 'allow', 'deny')
VISIBILITY_STATES = ('inherit', 'visible', 'hidden')
PROTECTED_PORTALS = ('admin', 'principal', 'superadmin')


def _nav_pages():
    """Flatten every real sidebar page from the published nav configuration."""
    try:
        with open(NAV_PATH, 'r', encoding='utf-8') as fh:
            cfg = json.load(fh)
    except Exception:
        return []
    out = []
    seen = set()

    def walk(portal, group, items):
        for item in items or []:
            if item.get('visible') is False:
                continue
            href = item.get('href') or ''
            if href and not href.startswith(('http://', 'https://', '#')):
                key = (portal, item.get('id') or href, href)
                if key not in seen:
                    seen.add(key)
                    clean = href.split('?')[0].split('#')[0].replace('\\', '/')
                    out.append({
                        'id': item.get('id') or '',
                        # Nav ids are only unique WITHIN a portal (e.g. every
                        # portal has a "dashboard"). Qualified keys keep an
                        # admin override from leaking into another portal.
                        'key': portal + ':' + (item.get('id') or href),
                        'label': item.get('label') or '',
                        'portal': portal,
                        'group': group,
                        'href': href,
                        'file': clean.rstrip('/').split('/')[-1],
                    })
            walk(portal, group, item.get('children'))

    for portal, pdata in (cfg.get('portals') or {}).items():
        for group in pdata.get('groups') or []:
            walk(portal, group.get('label') or group.get('id') or '', group.get('links'))
    return out


def _page_index():
    pages = _nav_pages()
    return {p['key']: p for p in pages}, pages


def _session_actor():
    """Only an explicit caller identity activates enforcement. Anonymous demo
    browsing keeps the full published navigation (no silent lockout)."""
    # The first-party cookie is what makes normal browser navigation
    # enforceable: HTML document requests cannot carry an X-Actor header.
    # Header identity still wins so API clients can explicitly impersonate.
    explicit = (request.headers.get('X-Actor')
                or request.headers.get('X-NGIS-Session')
                or request.headers.get('Authorization')
                or _actor_cookie() or '').strip()
    if explicit.lower().startswith('bearer '):
        explicit = explicit[7:].strip()
    return explicit.lower()


def _account_by_username(username, idstore):
    return next((a for a in idstore.get('accounts', [])
                 if str(a.get('username', '')).lower() == str(username).lower()), None)


def _normalize_overrides(payload):
    """Validate and canonicalise an override document. Unknown page ids,
    modules and actions are rejected rather than silently stored."""
    payload = payload if isinstance(payload, dict) else {}
    _, pages = _page_index()
    by_key = {p['key'] for p in pages}
    bare = {}
    for p in pages:
        bare.setdefault(p['id'], []).append(p['key'])
    out = {'portals': {}, 'pages': {}, 'actions': {}}

    for portal, value in (payload.get('portals') or {}).items():
        if portal not in PORTAL_KEYS:
            return None, 'Unknown portal: ' + str(portal)
        if value not in TRISTATE:
            return None, 'Portal state must be inherit, allow or deny'
        if value != 'inherit':
            out['portals'][portal] = value

    for raw_id, rule in (payload.get('pages') or {}).items():
        # Preferred form is "portal:nav-id". Legacy bare ids are accepted only
        # when unambiguous, so hiding "dashboard" can never silently affect
        # four different portals.
        if raw_id in by_key:
            page_key = raw_id
        elif raw_id in bare and len(bare[raw_id]) == 1:
            page_key = bare[raw_id][0]
        elif raw_id in bare:
            return None, ('Ambiguous page id %r; use one of %s'
                          % (raw_id, ', '.join(sorted(bare[raw_id]))))
        else:
            return None, 'Unknown page id: ' + str(raw_id)
        rule = rule if isinstance(rule, dict) else {}
        visibility = rule.get('visibility', 'inherit')
        access = rule.get('access', 'inherit')
        if visibility not in VISIBILITY_STATES:
            return None, 'Page visibility must be inherit, visible or hidden'
        if access not in TRISTATE:
            return None, 'Page access must be inherit, allow or deny'
        if visibility != 'inherit' or access != 'inherit':
            out['pages'][page_key] = {'visibility': visibility, 'access': access}

    for module, actions in (payload.get('actions') or {}).items():
        supported = None
        for group in PERMISSION_MODULES.values():
            if module in group:
                supported = group[module][1]
                break
        if supported is None:
            return None, 'Unknown permission module: ' + str(module)
        for action, value in (actions or {}).items():
            if action not in supported:
                return None, 'Unsupported action %s for %s' % (action, module)
            if value not in TRISTATE:
                return None, 'Action state must be inherit, allow or deny'
            if value != 'inherit':
                out['actions'].setdefault(module, {})[action] = value
    return out, None


def _resolve_access(account, overrides):
    """Single server-side resolution engine used by preview, sidebar filtering
    and direct-URL gating alike. Explicit deny always wins."""
    core = (account or {}).get('role', 'STUDENT')
    is_super = core == 'SUPER_ADMIN'
    protected = is_super or (account or {}).get('status') != 'active'
    effective_ov = {} if is_super else (overrides or {})
    home_portal = PORTAL_BY_CORE_ROLE.get(core, 'student')

    # Portal grants can also come from an ACTIVE custom role assigned to this
    # account. Protected portals in that list can only be written by a
    # SUPER_ADMIN (enforced in roles_permissions_ext). Explicit per-account
    # deny still overrides any role grant below.
    role_portals = set()
    if not is_super:
        store = _store()
        for rid in (account or {}).get('custom_roles', []):
            role = next((r for r in store.get('custom_roles', [])
                         if r.get('id') == rid and r.get('status') == 'active'), None)
            if role:
                role_portals.update(role.get('portals') or [])

    portals = {}
    for portal in PORTAL_KEYS:
        base = 'allow' if (is_super or portal == home_portal or portal in role_portals) else 'deny'
        stated = (effective_ov.get('portals') or {}).get(portal, 'inherit')
        portals[portal] = 'deny' if stated == 'deny' else ('allow' if stated == 'allow' else base)

    _, pages = _page_index()
    page_rules = effective_ov.get('pages') or {}
    page_states = []
    hidden_pages, denied_pages, hidden_files = [], [], []
    hidden_keys, denied_keys = [], []
    for page in pages:
        portal_allowed = portals.get(page['portal']) != 'deny'
        # Qualified key first; the bare id fallback only serves overrides
        # written before portal qualification was introduced.
        rule = page_rules.get(page['key']) or page_rules.get(page['id']) or {}
        visibility = rule.get('visibility', 'inherit')
        access = rule.get('access', 'inherit')
        visible = visibility != 'hidden'
        allowed = portal_allowed and access != 'deny'
        # "Hide & Deny Access" and portal denies are protected restrictions.
        if visibility == 'hidden' and access == 'deny':
            visible, allowed = False, False
        if not portal_allowed:
            allowed = False
        if is_super:
            visible, allowed = True, True
        reason = 'core' if not rule else 'override'
        # An explicit page-level deny is reported ahead of a portal deny so the
        # shared-directory bypass below can never mask a deliberate restriction.
        if access == 'deny':
            reason = 'page_denied'
        elif not portal_allowed:
            reason = 'portal_denied'
        if not visible:
            hidden_pages.append(page['id'])
            hidden_keys.append(page['key'])
            hidden_files.append(page['file'])
        if not allowed:
            denied_pages.append(page['id'])
            denied_keys.append(page['key'])
        page_states.append({
            'id': page['id'], 'key': page['key'], 'label': page['label'],
            'portal': page['portal'], 'group': page['group'],
            'href': page['href'], 'file': page['file'],
            'visible': visible, 'allowed': allowed, 'source': reason,
        })

    # Action-level effective permissions: start from the role engine, then
    # apply per-action overrides (deny > allow > inherit).
    effective = _effective_for_account(account or {}, _identity_store())
    for module, actions in (effective_ov.get('actions') or {}).items():
        current = set(effective['permissions'].get(module, []))
        for action, state in actions.items():
            if state == 'deny':
                current.discard(action)
            elif state == 'allow':
                current.add(action)
        effective['permissions'][module] = sorted(current)

    return {
        'username': (account or {}).get('username', ''),
        'role': core,
        'protected': protected,
        'portals': portals,
        'pages': page_states,
        'hidden_pages': hidden_pages,
        'denied_pages': denied_pages,
        'hidden_keys': hidden_keys,
        'denied_keys': denied_keys,
        'hidden_files': hidden_files,
        'permissions': effective['permissions'],
        'sources': effective['sources'],
        'overrides': effective_ov,
    }


def _current_access():
    """Resolve the access document for the caller. Returns (doc, enforced)."""
    actor = _session_actor()
    if not actor:
        return {'hidden_pages': [], 'denied_pages': [], 'hidden_files': [],
                'hidden_keys': [], 'denied_keys': [],
                'portals': {}, 'pages': [], 'permissions': {}, 'sources': [],
                'overrides': {}, 'username': '', 'role': '', 'protected': False}, False
    idstore = _identity_store()
    account = _account_by_username(actor, idstore)
    if not account:
        # Unknown identity: deny-by-default, but do not break public demo pages.
        return {'hidden_pages': [], 'denied_pages': [], 'hidden_files': [],
                'hidden_keys': [], 'denied_keys': [],
                'portals': {}, 'pages': [], 'permissions': {}, 'sources': [],
                'overrides': {}, 'username': actor, 'role': '', 'protected': False}, False
    store = _store()
    overrides = (store.get('user_overrides') or {}).get(actor, {})
    return _resolve_access(account, overrides), True


@roles_mgmt_bp.route('/pages', methods=['GET'])
def access_pages():
    """Page inventory grouped by portal for the Visibility control UI."""
    actor, err, status = _guard_read(_store(), _identity_store())
    if err:
        return err, status
    _, pages = _page_index()
    grouped = {}
    for page in pages:
        grouped.setdefault(page['portal'], []).append(page)
    return jsonify({'success': True, 'portals': grouped, 'total': len(pages)})


@roles_mgmt_bp.route('/users', methods=['GET'])
def access_users():
    """Login-account directory for the User Access tab. Overrides are keyed by
    username, so this uses the identity store rather than the person directory."""
    actor, err, status = _guard_read(_store(), _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    overrides = _store().get('user_overrides') or {}
    users = []
    for a in idstore.get('accounts', []):
        uname = str(a.get('username', '')).lower()
        users.append({
            'id': a.get('id', ''),
            'username': a.get('username', ''),
            'name': a.get('name', ''),
            'email': a.get('email', ''),
            'role': a.get('role', ''),
            'status': a.get('status', ''),
            'person_type': a.get('person_type', ''),
            'campus': a.get('campus', ''),
            'department': a.get('department', ''),
            'custom_roles': a.get('custom_roles', []),
            'protected': a.get('role') == 'SUPER_ADMIN' or a.get('status') != 'active',
            'has_overrides': bool(overrides.get(uname)),
        })
    users.sort(key=lambda u: (u['role'] != 'SUPER_ADMIN', u['username']))
    return jsonify({'success': True, 'users': users, 'total': len(users)})


@roles_mgmt_bp.route('/access', methods=['GET'])
def access_summary():
    """Server-evaluated visibility/deny lists for the current user.
    The sidebar consumes this ONCE per session; protect.js consumes /my-access
    for direct-URL enforcement. Hiding alone is never the security boundary."""
    doc, enforced = _current_access()
    portal = (request.args.get('portal') or '').strip().lower()
    pages = doc['pages']
    in_portal = lambda p: not portal or p['portal'] == portal
    # Derive the legacy raw-id lists FROM the qualified keys. Deriving them the
    # other way round reintroduces the collision (admin "dashboard" would hide
    # student "dashboard").
    hidden = set(doc['hidden_keys'])
    denied = set(doc['denied_keys'])
    return jsonify({'success': True, 'enforced': enforced,
                    'username': doc['username'], 'role': doc['role'],
                    'portals': doc['portals'], 'portal': portal,
                    'hidden_pages': [p['id'] for p in pages if in_portal(p) and p['key'] in hidden],
                    'denied_pages': [p['id'] for p in pages if in_portal(p) and p['key'] in denied],
                    'hidden_keys': doc['hidden_keys'],
                    'denied_keys': doc['denied_keys'],
                    'hidden_files': [p['file'] for p in pages if in_portal(p) and p['key'] in hidden]})


@roles_mgmt_bp.route('/my-access', methods=['GET'])
def my_access():
    """Direct-URL gate. `page` may be a nav id, a filename or a full path."""
    doc, enforced = _current_access()
    wanted = (request.args.get('page') or '').strip().lower()
    portal = (request.args.get('portal') or '').strip().lower()
    pages = doc['pages']

    matched = None
    if wanted:
        # 1. Exact filename / href is unambiguous and is what the server-side
        #    before_request gate uses, so the two gates agree by construction.
        matched = next((p for p in pages
                        if wanted in (p['file'].lower(), p['href'].lower())
                        and (not portal or p['portal'] == portal)), None)
        if not matched:
            matched = next((p for p in pages
                            if wanted in (p['file'].lower(), p['href'].lower())), None)
        # 2. Bare nav ids collide across portals ("dashboard" exists in four).
        #    Only resolve one inside the requesting portal.
        if not matched:
            matched = next((p for p in pages if p['id'].lower() == wanted
                            and (not portal or p['portal'] == portal)), None)
        # 3. Fully qualified key.
        if not matched:
            matched = next((p for p in pages if p['key'].lower() == wanted), None)
    if not enforced:
        return jsonify({'success': True, 'enforced': False, 'allowed': True,
                        'hidden': False, 'reason': 'anonymous_demo'})
    is_hidden = bool(matched and not matched['visible'])
    # Visibility and access are deliberately independent. A hidden-only page is
    # still reachable by direct URL; real security comes from access=deny (or a
    # portal deny), which is exactly what server.py's before_request gate checks.
    # Conflating the two here would make the client gate disagree with the server
    # gate and turn a presentation change into an unintended access restriction.
    allowed = bool(matched['allowed']) if matched else True
    reason = matched['source'] if matched else 'unlisted_page'
    # A page under /pages/shared/ is a role-agnostic shell. The portal that
    # happens to register the same filename in its nav (e.g. the student portal
    # owns departments.html) must not turn that shared page into a lockout for
    # every other role. An explicit page-level deny still applies.
    if matched and portal == 'shared' and reason == 'portal_denied':
        allowed, reason = True, 'shared_page'
    return jsonify({'success': True, 'enforced': True, 'allowed': allowed,
                    'hidden': is_hidden,
                    'page': matched['key'] if matched else wanted,
                    'reason': reason})


@roles_mgmt_bp.route('/overrides/<username>', methods=['GET'])
def get_overrides(username):
    actor, err, status = _guard_read(_store(), _identity_store())
    if err:
        return err, status
    idstore = _identity_store()
    account = _account_by_username(username, idstore)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    store = _store()
    overrides = (store.get('user_overrides') or {}).get(username.lower(), {})
    return jsonify({'success': True, 'account': {
        'username': account.get('username'), 'role': account.get('role'),
        'status': account.get('status'), 'name': account.get('name')},
        'overrides': overrides, 'effective': _resolve_access(account, overrides)})


@roles_mgmt_bp.route('/overrides/<username>', methods=['PUT'])
def put_overrides(username):
    store = _store()
    idstore = _identity_store()
    actor, err, status = _guard_write(store, idstore)
    if err:
        return err, status
    account = _account_by_username(username, idstore)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    if account.get('role') == 'SUPER_ADMIN':
        return jsonify({'success': False, 'error':
                        'SUPER_ADMIN accounts are protected and cannot receive overrides'}), 403
    if account.get('username', '').lower() == actor:
        return jsonify({'success': False, 'error':
                        'Self-modification of access overrides is blocked'}), 403

    normalized, error = _normalize_overrides(request.get_json(silent=True) or {})
    if error:
        return jsonify({'success': False, 'error': error}), 400

    # Privilege chain: only SUPER_ADMIN may ALLOW a protected portal to a
    # non-admin account. Explicit DENY is always permitted (it reduces access).
    if not _actor_is_super(actor, idstore):
        for portal, state in normalized['portals'].items():
            if state == 'allow' and portal in PROTECTED_PORTALS and account.get('role') not in ('ADMIN', 'SUPER_ADMIN'):
                return jsonify({'success': False, 'error':
                                'Allowing %s portal access requires SUPER_ADMIN authority' % portal}), 403
        for page_key, rule in normalized['pages'].items():
            if rule.get('access') == 'allow':
                _, pages = _page_index()
                page = next((p for p in pages if p['key'] == page_key), None)
                if page and page['portal'] in PROTECTED_PORTALS and account.get('role') not in ('ADMIN', 'SUPER_ADMIN'):
                    return jsonify({'success': False, 'error':
                                    'Allowing protected pages requires SUPER_ADMIN authority'}), 403

    key = username.lower()
    overrides = store.setdefault('user_overrides', {})
    before = overrides.get(key, {})
    if normalized == {k: {} for k in ('portals', 'pages', 'actions')}:
        overrides.pop(key, None)
    else:
        overrides[key] = normalized
    _audit(store, actor, 'update_user_access', target_user=key,
           before=before, after=normalized)
    _save_store(store)
    return jsonify({'success': True, 'overrides': normalized,
                    'effective': _resolve_access(account, normalized)})


@roles_mgmt_bp.route('/preview', methods=['POST'])
def preview_access():
    """Compute the effective permission/visibility document without saving."""
    actor, err, status = _guard_read(_store(), _identity_store())
    if err:
        return err, status
    body = request.get_json(silent=True) or {}
    username = str(body.get('username') or '').lower()
    account = _account_by_username(username, _identity_store())
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    normalized, error = _normalize_overrides(body.get('overrides') or {})
    if error:
        return jsonify({'success': False, 'error': error}), 400
    return jsonify({'success': True, 'effective': _resolve_access(account, normalized)})


def register_roles_mgmt_routes(app):
    app.register_blueprint(roles_mgmt_bp)
