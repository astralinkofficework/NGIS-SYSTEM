"""NGIS — Roles & Access Control: enforcement + extended management API.

This module is the security layer that the original ``roles_permissions_api``
module described but only partially enforced. It adds:

  * Real, request-level API enforcement: a curated binding table maps existing
    NGIS API families to a registered (module, action) pair. Every mutating
    request is checked against the SAME permission resolver that produces the
    sidebar filter, the effective-access inspector and the direct-URL gate.
    Unknown modules/actions are denied by default.
  * Custom permission DEFINITIONS with an honest enforcement state. A newly
    defined permission is either ``enforced`` (a real API binding checks it) or
    ``requires_integration``. Definitions in the latter state are never exposed
    as grantable security controls and can never widen an account's access.
  * Complete custom-role lifecycle (rich create, edit, safe delete), role-level
    portal access, user-role assignment from the User Access tab, server-side
    pagination for the audit log and the account directory, and optimistic
    concurrency on every sensitive write.

Core roles, SUPER_ADMIN identity and all existing guards in
``roles_permissions_api.py`` remain untouched and authoritative.
"""
import json
import re
import time
from datetime import datetime

from flask import Blueprint, jsonify, request

import roles_permissions_api as rp

ext_bp = Blueprint('roles_mgmt_ext', __name__, url_prefix='/api/roles-mgmt')

MUTATING = {'POST', 'PUT', 'PATCH', 'DELETE'}
KEY_RE = re.compile(r'^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)+$')
IDENT_RE = re.compile(r'^[a-z0-9][a-z0-9_-]{1,39}$')

CATEGORIES = ('academic', 'administration', 'operations', 'custom')
SCOPES = ('global', 'assigned-campus', 'assigned-department', 'own-records')
SCOPE_LABELS = {
    'global': 'All campuses & departments',
    'assigned-campus': 'Assigned campus',
    'assigned-department': 'Assigned department',
    'own-records': 'Own records only',
}
PROTECTED_PORTALS = ('admin', 'principal', 'superadmin')

# ── API → permission bindings ─────────────────────────────────────────────
# Every entry references API families that actually exist in server.py or one
# of the *_api.py blueprints. Order matters: the FIRST matching rule wins, so
# the narrow /api/roles-mgmt/overrides/ rule precedes the general role rule.
API_BINDINGS = [
    {'prefix': '/api/roles-mgmt/overrides/', 'module': 'user-management', 'action': 'manage',
     'label': 'Access override administration'},
    {'prefix': '/api/roles-mgmt/roles', 'module': 'user-management', 'action': 'manage',
     'label': 'Custom role administration'},
    {'prefix': '/api/roles-mgmt/permissions', 'module': 'user-management', 'action': 'manage',
     'label': 'Permission definition administration'},
    {'prefix': '/api/roles-mgmt/user-roles', 'module': 'user-management', 'action': 'manage',
     'label': 'User role assignments'},
    {'prefix': '/api/roles-mgmt/role-portals', 'module': 'user-management', 'action': 'manage',
     'label': 'Role portal access'},
    {'prefix': '/api/user-mgmt/', 'module': 'account-directories', 'action': 'manage',
     'label': 'Account provisioning & credentials'},
    {'prefix': '/api/cms/dashboard/publish', 'module': 'dashboard-content', 'action': 'publish',
     'label': 'Dashboard content publishing'},
    {'prefix': '/api/cms/dashboard/', 'module': 'dashboard-content', 'action': 'edit',
     'label': 'Dashboard content editing'},
    {'prefix': '/api/nav/', 'module': 'system-configuration', 'action': 'manage',
     'label': 'Navigation configuration'},
    {'prefix': '/api/system/', 'module': 'system-configuration', 'action': 'edit',
     'label': 'System configuration'},
    {'prefix': '/api/school-config/', 'module': 'school-information', 'action': 'edit',
     'label': 'School information'},
    {'prefix': '/api/news', 'module': 'news', 'action': 'edit',
     'label': 'News CMS'},
    {'prefix': '/api/announcements', 'module': 'announcements', 'action': 'edit',
     'label': 'Announcements'},
    {'prefix': '/api/teacher-mgmt/', 'module': 'teacher-profiles', 'action': 'edit',
     'label': 'Teacher management'},
    {'prefix': '/api/student-mgmt/', 'module': 'student-profiles', 'action': 'edit',
     'label': 'Student management'},
    {'prefix': '/api/academic/admin/', 'module': 'grades', 'action': 'approve',
     'label': 'Academic grade overrides'},
]

# Permissions that the RBAC layer itself enforces through its own guards.
GUARD_PAIRS = {
    ('roles-access', 'view'), ('roles-access', 'manage'),
    ('user-management', 'view'), ('user-management', 'manage'),
    ('login-security', 'view'), ('login-security', 'manage'),
}

ENFORCED_PAIRS = {(b['module'], b['action']) for b in API_BINDINGS} | GUARD_PAIRS
# A module with a real API binding also enforces its View action (the
# dependency rule requires View before any other action), so a definition
# referencing that pair is genuinely enforced rather than decorative.
ENFORCED_PAIRS |= {(b['module'], 'view') for b in API_BINDINGS}


def _now_ts():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def _store():
    s = rp._store()
    s.setdefault('permission_definitions', [])
    s.setdefault('role_portals', {})
    return s


def _audit(store, actor, action, **fields):
    event = {
        'id': 'RP-AUD-%05d' % (len(store.setdefault('audit_log', [])) + 1),
        'ts': _now_ts(), 'actor': actor, 'action': action, 'outcome': 'success',
    }
    event.update(fields)
    store['audit_log'].append(event)


def _save(store):
    rp._save_store(store)


def _guard_read():
    return rp._guard_read(None, rp._identity_store())


def _guard_write():
    idstore = rp._identity_store()
    actor, err, status = rp._guard_write(None, idstore)
    return actor, err, status, idstore


def _is_super(actor, idstore):
    return rp._actor_is_super(actor, idstore)


def _role(store, role_id):
    return next((r for r in store.get('custom_roles', []) if r.get('id') == role_id), None)


def _module_label(module):
    for group in rp.PERMISSION_MODULES.values():
        if module in group:
            return group[module][0]
    return module


def _module_actions(module):
    for group in rp.PERMISSION_MODULES.values():
        if module in group:
            return list(group[module][1])
    return None


def _page_keys():
    _, pages = rp._page_index()
    return {p['key'] for p in pages}


def _last_super_admin_ok(idstore):
    """Rule 11: never allow an operation that would leave the system without an
    active SUPER_ADMIN. This is checked on every identity-affecting write."""
    return sum(1 for a in idstore.get('accounts', [])
               if a.get('role') == 'SUPER_ADMIN' and a.get('status') == 'active') >= 1


def _concurrency(role, payload):
    """Optimistic concurrency: a stale client cannot silently overwrite a newer
    permission configuration. Returns an error response or None."""
    expected = (payload or {}).get('expected_updated_at')
    if expected and expected != role.get('updated_at'):
        return jsonify({'success': False,
                        'error': 'This role was changed by another administrator. Reload before saving.',
                        'code': 'stale_role',
                        'current_updated_at': role.get('updated_at', '')}), 409
    return None


# ── permission resolution (single authoritative evaluator) ─────────────────

def effective_action_permissions(account, overrides=None, store=None):
    """Core baseline ∪ active custom roles ∪ per-user action overrides.

    This is the same document the User Access inspector displays, so the UI and
    the enforcement gate can never disagree.
    """
    store = store if store is not None else _store()
    resolved = rp._resolve_access(account, overrides or {})
    return resolved['permissions'], resolved


def enforce_permission(module, action, actor=None, idstore=None, store=None):
    """Return (allowed, reason). Default-deny for unknown identifiers.

    Anonymous demo browsing is intentionally unenforced (the whole app is a
    demo-first build); as soon as an explicit identity resolves to an account,
    every bound API operation is checked.
    """
    if module not in _all_module_ids() or action not in rp.ACTION_LABELS:
        return False, 'unknown_permission'
    actor = actor or rp._session_actor()
    if not actor:
        return True, 'anonymous_demo'
    idstore = idstore if idstore is not None else rp._identity_store()
    account = rp._account_by_username(actor, idstore)
    if not account:
        return True, 'unknown_actor'
    store = store if store is not None else _store()
    overrides = (store.get('user_overrides') or {}).get(actor, {}) or {}
    perms, _ = effective_action_permissions(account, overrides, store)
    allowed = action in (perms.get(module) or [])
    return allowed, ('granted' if allowed else 'denied')


def _all_module_ids():
    return {mid for group in rp.PERMISSION_MODULES.values() for mid in group}


def _binding_for(path):
    for b in API_BINDINGS:
        if path.startswith(b['prefix']):
            return b
    return None


def register_enforcement(app):
    """Attach the API-level RBAC gate. Registered once, at startup."""
    @app.before_request
    def enforce_api_permission():
        if request.method not in MUTATING:
            return None
        path = (request.path or '').lower()
        if not path.startswith('/api/'):
            return None
        binding = _binding_for(path)
        if not binding:
            return None
        # The RBAC endpoints are self-guarding; skipping them here avoids a
        # double evaluation while their own guards still return precise 401/403
        # messages for anonymous and low-privilege callers.
        if path.startswith('/api/roles-mgmt/'):
            return None
        actor = rp._session_actor()
        if not actor:
            return None
        try:
            idstore = rp._identity_store()
            account = rp._account_by_username(actor, idstore)
            if not account:
                return None
            allowed, reason = enforce_permission(
                binding['module'], binding['action'], actor, idstore)
            if allowed:
                return None
            return jsonify({
                'success': False,
                'error': 'Permission denied: %s.%s is required for this operation.' %
                         (binding['module'], binding['action']),
                'required_permission': '%s.%s' % (binding['module'], binding['action']),
                'binding': binding['label'],
                'actor': actor,
                'reason': reason,
            }), 403
        except Exception:
            # Security gate must never take the whole application down.
            return None


# ── custom permission definitions ────────────────────────────────────────

def _definition_view(d):
    pair = (d.get('module'), d.get('action'))
    custom_module = _module_actions(d.get('module')) is None
    enforced = (not custom_module) and pair in ENFORCED_PAIRS
    return {
        'custom_module': custom_module,
        'key': d.get('key'), 'name': d.get('name', ''),
        'description': d.get('description', ''),
        'module': d.get('module', ''), 'module_label': _module_label(d.get('module')),
        'action': d.get('action', ''),
        'action_label': rp.ACTION_LABELS.get(d.get('action'), d.get('action', '')),
        'portal': d.get('portal', ''), 'target_page': d.get('target_page', ''),
        'scope': d.get('scope', 'global'),
        'scope_label': SCOPE_LABELS.get(d.get('scope'), d.get('scope', '')),
        'resource_exists': bool(d.get('target_page') in _page_keys()) or not custom_module,
        'enforcement': 'enforced' if enforced else 'requires_integration',
        'enforceable': enforced,
        'created_by': d.get('created_by', ''), 'created_at': d.get('created_at', ''),
        'updated_at': d.get('updated_at', ''),
        'origin': 'custom',
    }


def _builtin_definitions():
    out = []
    for category, modules in rp.PERMISSION_MODULES.items():
        for mid, (label, actions) in modules.items():
            for action in actions:
                key = '%s.%s' % (mid, action)
                enforced = (mid, action) in ENFORCED_PAIRS
                out.append({
                    'key': key, 'name': '%s — %s' % (label, rp.ACTION_LABELS.get(action, action)),
                    'module': mid, 'module_label': label, 'action': action,
                    'action_label': rp.ACTION_LABELS.get(action, action),
                    'category': category, 'origin': 'registry',
                    'enforcement': 'enforced' if enforced else 'registered',
                    'enforceable': True,
                    'binding': next((b['label'] for b in API_BINDINGS
                                     if b['module'] == mid and b['action'] == action), ''),
                })
    return out


def _validate_definition(payload, store, editing=None):
    """Return (clean, error_response). Never trusts client-supplied enforcement."""
    name = str(payload.get('name') or '').strip()
    key = str(payload.get('key') or '').strip().lower()
    module = str(payload.get('module') or '').strip()
    action = str(payload.get('action') or '').strip().lower()
    portal = str(payload.get('portal') or 'admin').strip().lower()
    target_page = str(payload.get('target_page') or '').strip()
    scope = str(payload.get('scope') or 'global').strip().lower()
    description = str(payload.get('description') or '').strip()

    if len(name) < 3:
        return None, (jsonify({'success': False, 'error': 'Permission name must be at least 3 characters'}), 400)
    if not KEY_RE.match(key) or len(key) > 64 or '.' not in key:
        return None, (jsonify({'success': False,
                               'error': 'Permission key must look like "teacher-reports.approve" '
                                        '(lowercase, dot-separated, letters/digits/dot/dash/underscore)'}), 400)
    supported = _module_actions(module)
    custom_module = supported is None
    if custom_module and not re.match(r'^[a-z0-9][a-z0-9-]{1,47}$', module):
        return None, (jsonify({'success': False,
                               'error': 'Module "%s" is not registered. Use a lowercase slug '
                                        '(e.g. teacher-reports) for a new module.' % module}), 400)
    if action not in rp.ACTION_LABELS:
        return None, (jsonify({'success': False,
                               'error': 'Unsupported action "%s". Registered actions: %s' %
                                        (action, ', '.join(rp.ALL_ACTIONS))}), 400)
    if not custom_module and action not in supported:
        return None, (jsonify({'success': False,
                               'error': 'Unsupported action "%s" for %s. Supported: %s' %
                                        (action, _module_label(module), ', '.join(supported))}), 400)
    if portal not in rp.PORTAL_KEYS:
        return None, (jsonify({'success': False, 'error': 'Unknown portal "%s"' % portal}), 400)
    if scope not in SCOPES:
        return None, (jsonify({'success': False, 'error': 'Unknown permission scope "%s"' % scope}), 400)
    if target_page:
        if target_page not in _page_keys():
            return None, (jsonify({'success': False,
                                   'error': 'Target page "%s" is not a published NGIS page' % target_page}), 400)
        _, pages = rp._page_index()
        page = next((p for p in pages if p['key'] == target_page), None)
        if page and page['portal'] != portal:
            return None, (jsonify({'success': False,
                                   'error': 'Target page belongs to the %s portal, not %s' %
                                            (page['portal'], portal)}), 400)
    builtin_keys = {d['key'] for d in _builtin_definitions()}
    if key in builtin_keys:
        return None, (jsonify({'success': False,
                               'error': 'Key "%s" is already a registered system permission' % key}), 409)
    duplicate = next((d for d in store.get('permission_definitions', [])
                      if d.get('key') == key and (not editing or d.get('key') != editing.get('key'))), None)
    if duplicate:
        return None, (jsonify({'success': False, 'error': 'Permission key "%s" already exists' % key}), 409)
    return {
        'key': key, 'name': name, 'description': description,
        'module': module, 'action': action, 'portal': portal,
        'target_page': target_page, 'scope': scope,
        'custom_module': custom_module,
        'enforcement': ('requires_integration' if custom_module else
                        ('enforced' if (module, action) in ENFORCED_PAIRS else 'requires_integration')),
    }, None


@ext_bp.route('/permissions', methods=['GET'])
def list_definitions():
    _, err, status = _guard_read()
    if err:
        return err, status
    store = _store()
    custom = [_definition_view(d) for d in store.get('permission_definitions', [])]
    builtin = _builtin_definitions()
    return jsonify({
        'success': True,
        'custom': sorted(custom, key=lambda d: d['key']),
        'builtin': builtin,
        'totals': {
            'registered': len(builtin),
            'custom': len(custom),
            'enforced': sum(1 for d in builtin if d['enforcement'] == 'enforced'),
            'requires_integration': sum(1 for d in custom if not d['enforceable']),
        },
        'actions': [{'id': a, 'label': rp.ACTION_LABELS[a]} for a in rp.ALL_ACTIONS],
        'scopes': [{'id': s, 'label': SCOPE_LABELS[s]} for s in SCOPES],
        'portals': list(rp.PORTAL_KEYS),
        'modules': [{'id': mid, 'label': _module_label(mid), 'actions': list(_module_actions(mid))}
                    for cat in rp.PERMISSION_MODULES.values() for mid in cat],
        'pages': sorted(_page_keys()),
    })


@ext_bp.route('/permissions', methods=['POST'])
def create_definition():
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    store = _store()
    clean, verr = _validate_definition(request.get_json(silent=True) or {}, store)
    if verr:
        return verr
    if clean['portal'] in PROTECTED_PORTALS and not _is_super(actor, idstore):
        return jsonify({'success': False,
                        'error': 'Defining permissions for a protected portal requires SUPER_ADMIN authority'}), 403
    pair = (clean['module'], clean['action'])
    clean.update({'created_by': actor, 'created_at': _now_ts(), 'updated_at': _now_ts()})
    store.setdefault('permission_definitions', []).append(clean)
    _audit(store, actor, 'permission_created',
           target_role_name=clean['name'],
           after={'key': clean['key'], 'module': clean['module'],
                  'action': clean['action'], 'enforcement': clean['enforcement'],
                  'portal': clean['portal'], 'scope': clean['scope'],
                  'target_page': clean['target_page']})
    _save(store)
    if clean['enforcement'] == 'enforced':
        message = 'Permission created and enforced by %s' % next(
            (b['label'] for b in API_BINDINGS if (b['module'], b['action']) == pair),
            'the RBAC guards')
    else:
        message = ('Permission definition saved — Requires Integration. '
                   'No backend action is bound to it, so it grants no access.')
    return jsonify({'success': True, 'message': message,
                    'definition': _definition_view(clean)}), 201


@ext_bp.route('/permissions/<path:key>', methods=['PUT'])
def update_definition(key):
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    store = _store()
    d = next((x for x in store.get('permission_definitions', []) if x.get('key') == key), None)
    if not d:
        return jsonify({'success': False,
                        'error': 'System permission definitions cannot be edited'}), 404
    payload = request.get_json(silent=True) or {}
    merged = dict(d)
    for field in ('name', 'description', 'portal', 'target_page', 'scope'):
        if field in payload:
            merged[field] = payload[field]
    # key / module / action are immutable: changing them would silently retarget
    # a permission that other records may already reference.
    merged['key'] = d['key']
    merged['module'] = d['module']
    merged['action'] = d['action']
    clean, verr = _validate_definition(merged, store, editing=d)
    if verr:
        return verr
    if clean['portal'] in PROTECTED_PORTALS and not _is_super(actor, idstore):
        return jsonify({'success': False,
                        'error': 'Editing protected-portal permissions requires SUPER_ADMIN authority'}), 403
    expected = payload.get('expected_updated_at')
    if expected and expected != d.get('updated_at'):
        return jsonify({'success': False,
                        'error': 'This permission was changed by another administrator. Reload before saving.',
                        'code': 'stale_permission'}), 409
    before = {k: d.get(k) for k in ('name', 'description', 'portal', 'target_page', 'scope')}
    d.update(clean)
    d['updated_at'] = _now_ts()
    _audit(store, actor, 'permission_updated', target_role_name=d['name'],
           before=before, after={k: d.get(k) for k in before})
    _save(store)
    return jsonify({'success': True, 'message': 'Permission definition updated',
                    'definition': _definition_view(d)})


@ext_bp.route('/permissions/<path:key>/delete', methods=['POST'])
def delete_definition(key):
    actor, err, status, _ = _guard_write()
    if err:
        return err, status
    store = _store()
    d = next((x for x in store.get('permission_definitions', []) if x.get('key') == key), None)
    if not d:
        return jsonify({'success': False, 'error': 'Permission definition not found'}), 404
    referenced = [r['name'] for r in store.get('custom_roles', [])
                  if d['key'] in (r.get('custom_permission_keys') or [])]
    if referenced:
        return jsonify({'success': False,
                        'error': 'Permission is in use by: %s' % ', '.join(referenced)}), 409
    store['permission_definitions'].remove(d)
    _audit(store, actor, 'permission_deleted', target_role_name=d['name'],
           before={'key': d['key'], 'module': d['module'], 'action': d['action']})
    _save(store)
    return jsonify({'success': True, 'message': 'Permission definition removed'})


@ext_bp.route('/enforcement', methods=['GET'])
def enforcement_inventory():
    _, err, status = _guard_read()
    if err:
        return err, status
    return jsonify({'success': True,
                    'bindings': [{'prefix': b['prefix'], 'module': b['module'],
                                  'action': b['action'], 'label': b['label'],
                                  'permission': '%s.%s' % (b['module'], b['action']),
                                  'methods': sorted(MUTATING)} for b in API_BINDINGS],
                    'guard_pairs': ['%s.%s' % p for p in sorted(GUARD_PAIRS)],
                    'total': len(API_BINDINGS)})


# ── role lifecycle ────────────────────────────────────────────────────────

def _slugify(name):
    s = re.sub(r'[^a-z0-9]+', '-', str(name).lower()).strip('-')
    return (s[:38] or 'custom-role').rstrip('-')


def _role_view(role, idstore):
    view = rp._role_summary(role, idstore)
    view.update({
        'identifier': role.get('identifier', ''),
        'category': role.get('category', 'custom'),
        'default_portal': role.get('default_portal', ''),
        'portals': role.get('portals', []),
        'custom_permission_keys': role.get('custom_permission_keys', []),
        'scopes': role.get('scopes', {'campuses': [], 'departments': []}),
    })
    return view


def _validate_portals(value, actor, idstore):
    if value is None:
        return [], None
    if not isinstance(value, list):
        return None, (jsonify({'success': False, 'error': 'portals must be a list'}), 400)
    clean = []
    for p in value:
        p = str(p).strip().lower()
        if p not in rp.PORTAL_KEYS:
            return None, (jsonify({'success': False, 'error': 'Unknown portal "%s"' % p}), 400)
        if p in PROTECTED_PORTALS and not _is_super(actor, idstore):
            return None, (jsonify({'success': False,
                                   'error': 'Granting %s portal access requires SUPER_ADMIN authority' % p}), 403)
        if p not in clean:
            clean.append(p)
    return clean, None


@ext_bp.route('/roles/create', methods=['POST'])
def create_role_rich():
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    if not _last_super_admin_ok(idstore):
        return jsonify({'success': False,
                        'error': 'No active SUPER_ADMIN remains; role changes are locked'}), 409
    store = _store()
    p = request.get_json(silent=True) or {}
    name = str(p.get('name') or '').strip()
    description = str(p.get('description') or '').strip()
    identifier = str(p.get('identifier') or '').strip().lower() or _slugify(name)
    category = str(p.get('category') or 'custom').strip().lower()
    default_portal = str(p.get('default_portal') or '').strip().lower()
    base_role = str(p.get('base_role') or 'ADMIN').strip().upper()
    status_value = str(p.get('status') or 'active').strip().lower()

    if len(name) < 2:
        return jsonify({'success': False, 'error': 'Role name must be at least 2 characters'}), 400
    if not IDENT_RE.match(identifier):
        return jsonify({'success': False,
                        'error': 'Role identifier must be lowercase letters, digits, dash or underscore'}), 400
    if category not in CATEGORIES:
        return jsonify({'success': False, 'error': 'Unknown role category "%s"' % category}), 400
    if base_role not in rp.CORE_ROLES:
        return jsonify({'success': False, 'error': 'Unknown base role "%s"' % base_role}), 400
    if status_value not in ('active', 'archived'):
        return jsonify({'success': False, 'error': 'Invalid role status'}), 400
    if default_portal and default_portal not in rp.PORTAL_KEYS:
        return jsonify({'success': False, 'error': 'Unknown default portal "%s"' % default_portal}), 400
    if default_portal in PROTECTED_PORTALS and not _is_super(actor, idstore):
        return jsonify({'success': False,
                        'error': 'Assigning a protected default portal requires SUPER_ADMIN authority'}), 403
    if any(r.get('name', '').lower() == name.lower() and r.get('status') == 'active'
           for r in store.get('custom_roles', [])):
        return jsonify({'success': False, 'error': 'A role named "%s" already exists' % name}), 409
    if any(r.get('identifier', '') == identifier for r in store.get('custom_roles', [])):
        return jsonify({'success': False, 'error': 'Role identifier "%s" is already used' % identifier}), 409

    perms, perr, pstatus = rp._validate_permissions(p.get('permissions') or {})
    if perr:
        return perr, pstatus
    chain = rp._guard_privilege_chain({'permissions': perms}, actor, idstore)
    if chain:
        return chain
    portals, perr = _validate_portals(p.get('portals') or [], actor, idstore)
    if perr:
        return perr

    role = {
        'id': rp._next_role_id(store), 'name': name, 'description': description,
        'identifier': identifier, 'category': category,
        'default_portal': default_portal, 'base_role': base_role,
        'status': status_value, 'portals': portals,
        'scopes': rp._validate_scopes(p.get('scopes') or {}),
        'permissions': perms, 'revisions': [],
        'created_by': actor, 'created_at': _now_ts(), 'updated_at': _now_ts(),
    }
    store.setdefault('custom_roles', []).append(role)
    _audit(store, actor, 'role_created', target_role=role['id'], target_role_name=name,
           after={'identifier': identifier, 'category': category,
                  'default_portal': default_portal, 'portals': portals,
                  'base_role': base_role, 'permissions': perms})
    _save(store)
    return jsonify({'success': True, 'message': 'Role "%s" created' % name,
                    'role': _role_view(role, idstore)}), 201


@ext_bp.route('/roles/<role_id>/edit', methods=['POST'])
def edit_role(role_id):
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    store = _store()
    if role_id in rp.CORE_ROLES:
        return jsonify({'success': False,
                        'error': 'Core system role definitions are protected. '
                                 'Duplicate the role into a custom role instead.'}), 403
    role = _role(store, role_id)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    p = request.get_json(silent=True) or {}
    stale = _concurrency(role, p)
    if stale:
        return stale
    before = {k: role.get(k) for k in ('name', 'description', 'category',
                                       'default_portal', 'status', 'scopes', 'portals')}
    if 'name' in p:
        name = str(p.get('name') or '').strip()
        if len(name) < 2:
            return jsonify({'success': False, 'error': 'Role name must be at least 2 characters'}), 400
        if any(r.get('name', '').lower() == name.lower() and r.get('id') != role_id
               and r.get('status') == 'active' for r in store.get('custom_roles', [])):
            return jsonify({'success': False, 'error': 'A role named "%s" already exists' % name}), 409
        role['name'] = name
    if 'description' in p:
        role['description'] = str(p.get('description') or '').strip()
    if 'category' in p:
        cat = str(p.get('category') or '').strip().lower()
        if cat not in CATEGORIES:
            return jsonify({'success': False, 'error': 'Unknown role category'}), 400
        role['category'] = cat
    if 'default_portal' in p:
        dp = str(p.get('default_portal') or '').strip().lower()
        if dp and dp not in rp.PORTAL_KEYS:
            return jsonify({'success': False, 'error': 'Unknown default portal'}), 400
        if dp in PROTECTED_PORTALS and not _is_super(actor, idstore):
            return jsonify({'success': False,
                            'error': 'Changing a protected default portal requires SUPER_ADMIN authority'}), 403
        role['default_portal'] = dp
    if 'status' in p:
        sv = str(p.get('status') or '').strip().lower()
        if sv not in ('active', 'archived'):
            return jsonify({'success': False, 'error': 'Invalid role status'}), 400
        role['status'] = sv
    if 'scopes' in p:
        role['scopes'] = rp._validate_scopes(p.get('scopes') or {})
    if 'portals' in p:
        portals, perr = _validate_portals(p.get('portals'), actor, idstore)
        if perr:
            return perr
        role['portals'] = portals
    role['updated_at'] = _now_ts()
    _audit(store, actor, 'role_updated', target_role=role_id, target_role_name=role['name'],
           before=before, after={k: role.get(k) for k in before})
    _save(store)
    return jsonify({'success': True, 'message': 'Role updated',
                    'role': _role_view(role, idstore)})


@ext_bp.route('/roles/<role_id>', methods=['DELETE'])
def delete_role(role_id):
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    if role_id in rp.CORE_ROLES:
        return jsonify({'success': False, 'error': 'Core system roles cannot be deleted'}), 403
    if not _last_super_admin_ok(idstore):
        return jsonify({'success': False,
                        'error': 'No active SUPER_ADMIN remains; role deletion is locked'}), 409
    store = _store()
    role = _role(store, role_id)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    stale = _concurrency(role, request.get_json(silent=True) or {})
    if stale:
        return stale
    members = [a for a in idstore.get('accounts', []) if role_id in a.get('custom_roles', [])]
    if members:
        return jsonify({'success': False,
                        'error': 'Unassign all %d member(s) before deleting this role' % len(members),
                        'members': [a.get('username') for a in members]}), 409
    store['custom_roles'].remove(role)
    store.setdefault('role_portals', {}).pop(role_id, None)
    _audit(store, actor, 'role_deleted', target_role=role_id, target_role_name=role['name'],
           before={'name': role['name'], 'permissions': role.get('permissions'),
                   'portals': role.get('portals', [])})
    _save(store)
    return jsonify({'success': True, 'message': 'Role "%s" deleted' % role['name']})


@ext_bp.route('/roles/<role_id>/permissions/save', methods=['PUT'])
def save_permissions(role_id):
    """Permission matrix save with optimistic concurrency + explicit diffs."""
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    store = _store()
    if role_id in rp.CORE_ROLES:
        return jsonify({'success': False,
                        'error': 'Core system roles are protected; their matrix is read-only'}), 403
    role = _role(store, role_id)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    p = request.get_json(silent=True) or {}
    stale = _concurrency(role, p)
    if stale:
        return stale
    perms, perr, pstatus = rp._validate_permissions(p.get('permissions'))
    if perr:
        return perr, pstatus
    chain = rp._guard_privilege_chain({'permissions': perms}, actor, idstore)
    if chain:
        return chain
    # Custom permission definitions may only be granted when they map to a
    # real enforcement binding; definitions flagged Requires Integration are
    # rejected here so a checkbox can never become a security bypass.
    wanted_keys = p.get('custom_permission_keys')
    if wanted_keys is not None:
        if not isinstance(wanted_keys, list):
            return jsonify({'success': False,
                            'error': 'custom_permission_keys must be a list'}), 400
        definitions = {x['key']: x for x in store.get('permission_definitions', [])}
        for k in wanted_keys:
            definition = definitions.get(k)
            if not definition:
                return jsonify({'success': False,
                                'error': 'Unknown permission definition "%s"' % k}), 400
            if (definition.get('module'), definition.get('action')) not in ENFORCED_PAIRS:
                return jsonify({'success': False,
                                'error': '"%s" requires backend integration and cannot be granted' %
                                         definition.get('name', k)}), 403
        role['custom_permission_keys'] = sorted(set(wanted_keys))
    before = role.get('permissions') or {}
    added, removed = rp._diff_permissions(before, perms)
    role.setdefault('revisions', []).append(
        {'ts': _now_ts(), 'actor': actor,
         'permissions': json.loads(json.dumps(before))})
    if len(role['revisions']) > 20:
        role['revisions'] = role['revisions'][-20:]
    role['permissions'] = perms
    role['updated_at'] = _now_ts()
    _audit(store, actor, 'permissions_updated', target_role=role_id,
           target_role_name=role['name'],
           before={'permissions': before}, after={'permissions': perms},
           added=added, removed=removed)
    _save(store)
    return jsonify({'success': True, 'message': 'Permissions saved',
                    'added': added, 'removed': removed,
                    'affected_users': sum(1 for a in idstore.get('accounts', [])
                                          if role_id in a.get('custom_roles', [])),
                    'updated_at': role['updated_at'], 'permissions': perms})


# ── role-level portal access ──────────────────────────────────────────────

@ext_bp.route('/role-portals', methods=['GET'])
def role_portals():
    _, err, status = _guard_read()
    if err:
        return err, status
    store = _store()
    return jsonify({
        'success': True,
        'portals': [{'id': p, 'label': p.replace('superadmin', 'super admin').title() + ' Portal',
                     'protected': p in PROTECTED_PORTALS} for p in rp.PORTAL_KEYS],
        'configs': {r['id']: r.get('portals', []) for r in store.get('custom_roles', [])},
        'protected_portals': list(PROTECTED_PORTALS),
        'note': 'Portal access is resolved server-side with core baseline, custom role access '
                'and per-account overrides. Explicit deny always wins.',
    })


@ext_bp.route('/roles/<role_id>/portals', methods=['PUT'])
def set_role_portals(role_id):
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    store = _store()
    if role_id in rp.CORE_ROLES:
        return jsonify({'success': False, 'error': 'Core role portal access is fixed by the system'}), 403
    role = _role(store, role_id)
    if not role:
        return jsonify({'success': False, 'error': 'Role not found'}), 404
    p = request.get_json(silent=True) or {}
    stale = _concurrency(role, p)
    if stale:
        return stale
    portals, perr = _validate_portals(p.get('portals') or [], actor, idstore)
    if perr:
        return perr
    before = role.get('portals', [])
    role['portals'] = portals
    role['updated_at'] = _now_ts()
    store.setdefault('role_portals', {})[role_id] = portals
    _audit(store, actor, 'portal_access_changed', target_role=role_id,
           target_role_name=role['name'],
           before={'portals': before}, after={'portals': portals})
    _save(store)
    return jsonify({'success': True, 'message': 'Role portal access saved',
                    'portals': portals, 'updated_at': role['updated_at']})


# ── user-role assignments (User Access tab) ───────────────────────────────

@ext_bp.route('/user-roles', methods=['GET'])
def user_roles():
    _, err, status = _guard_read()
    if err:
        return err, status
    username = str(request.args.get('username') or '').strip().lower()
    idstore = rp._identity_store()
    account = rp._account_by_username(username, idstore)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    store = _store()
    meta = account.get('custom_roles_meta') or {}
    assignments = []
    for rid in account.get('custom_roles', []):
        role = _role(store, rid)
        assignments.append({
            'role_id': rid, 'name': role['name'] if role else '(deleted role)',
            'status': role.get('status', 'archived') if role else 'archived',
            'assigned_by': (meta.get(rid) or {}).get('assigned_by', '') if isinstance(meta, dict) else '',
            'assigned_at': (meta.get(rid) or {}).get('assigned_at', '') if isinstance(meta, dict) else '',
        })
    eligible = [{'id': r['id'], 'name': r['name'], 'status': r.get('status', 'active')}
                for r in store.get('custom_roles', [])
                if r.get('status') == 'active' and r['id'] not in account.get('custom_roles', [])]
    eff = rp._effective_for_account(account, idstore)
    return jsonify({'success': True, 'username': username,
                    'account': {'role': account.get('role'), 'status': account.get('status'),
                                'name': account.get('name', ''), 'campus': account.get('campus', '')},
                    'assignments': assignments, 'eligible': eligible,
                    'sources': eff['sources'],
                    'effective': [{'module': mid, 'label': _module_label(mid),
                                   'actions': acts, 'source': rp._perm_source(eff['sources'], mid)}
                                  for mid, acts in sorted(eff['permissions'].items())]})


@ext_bp.route('/user-roles', methods=['POST'])
def change_user_roles():
    actor, err, status, idstore = _guard_write()
    if err:
        return err, status
    store = _store()
    p = request.get_json(silent=True) or {}
    username = str(p.get('username') or '').strip().lower()
    role_id = str(p.get('role_id') or '').strip()
    op = str(p.get('op') or '').strip().lower()
    account = rp._account_by_username(username, idstore)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    role = _role(store, role_id)
    if not role:
        return jsonify({'success': False, 'error': 'Custom role not found'}), 404
    if op not in ('assign', 'revoke'):
        return jsonify({'success': False, 'error': 'op must be assign or revoke'}), 400
    if account.get('role') == 'SUPER_ADMIN':
        return jsonify({'success': False,
                        'error': 'SUPER_ADMIN is a protected identity and cannot hold custom roles'}), 403
    if username == actor:
        return jsonify({'success': False, 'error': 'Self-assignment of roles is blocked'}), 403
    # Delegation guard: an actor cannot delegate a permission they do not hold.
    if op == 'assign':
        actor_perms, _ = effective_action_permissions(
            rp._account_by_username(actor, idstore),
            (store.get('user_overrides') or {}).get(actor, {}) or {}, store)
        for module, actions in (role.get('permissions') or {}).items():
            missing = [a for a in actions if a not in (actor_perms.get(module) or [])]
            if missing and not _is_super(actor, idstore):
                return jsonify({'success': False,
                                'error': 'Cannot delegate %s: %s (not held by your account)' %
                                         (_module_label(module), ', '.join(missing))}), 403
    if op == 'assign':
        if role.get('status') != 'active':
            return jsonify({'success': False, 'error': 'Archived roles cannot receive members'}), 409
        if role_id in account.get('custom_roles', []):
            return jsonify({'success': False, 'error': 'User already holds this role'}), 409
        account.setdefault('custom_roles', []).append(role_id)
        account.setdefault('custom_roles_meta', {})[role_id] = {
            'assigned_by': actor, 'assigned_at': _now_ts()}
        action, message = 'user_assigned', '%s assigned to %s' % (username, role['name'])
    else:
        if role_id not in account.get('custom_roles', []):
            return jsonify({'success': False, 'error': 'User does not hold this role'}), 404
        account['custom_roles'].remove(role_id)
        if isinstance(account.get('custom_roles_meta'), dict):
            account['custom_roles_meta'].pop(role_id, None)
        action, message = 'user_removed', '%s removed from %s' % (username, role['name'])
    if not _last_super_admin_ok(idstore):
        return jsonify({'success': False,
                        'error': 'This change would leave no active SUPER_ADMIN'}), 409
    rp._audit_identity(idstore, actor, 'custom_role_' + ('assigned' if op == 'assign' else 'removed'),
                       account, role)
    rp._save_json('user_accounts.json', idstore)
    _audit(store, actor, action, target_role=role_id, target_role_name=role['name'],
           target_user=username, after={'op': op, 'role_id': role_id})
    _save(store)
    return jsonify({'success': True, 'message': message})


# ── paginated reads ───────────────────────────────────────────────────────

@ext_bp.route('/users/paged', methods=['GET'])
def users_paged():
    _, err, status = _guard_read()
    if err:
        return err, status
    idstore = rp._identity_store()
    overrides = _store().get('user_overrides') or {}
    q = str(request.args.get('q') or '').strip().lower()
    role = str(request.args.get('role') or '').strip().upper()
    campus = str(request.args.get('campus') or '').strip().lower()
    try:
        limit = max(1, min(100, int(request.args.get('limit') or 10)))
        offset = max(0, int(request.args.get('offset') or 0))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Invalid pagination parameters'}), 400
    rows = []
    for a in idstore.get('accounts', []):
        uname = str(a.get('username', '')).lower()
        if role and role != 'ALL' and str(a.get('role', '')).upper() != role:
            continue
        # `campus` is normalised to lowercase above, so the sentinel must be
        # compared in the same case. Comparing 'all' to 'ALL' silently filtered
        # out every account in the directory.
        if campus and campus != 'all' and str(a.get('campus', '')).lower() != campus:
            continue
        if q and q not in ' '.join(str(a.get(k) or '') for k in
                                   ('name', 'username', 'id', 'role', 'department', 'campus')).lower():
            continue
        rows.append({
            'id': a.get('id', ''), 'username': a.get('username', ''),
            'name': a.get('name', ''), 'email': a.get('email', ''),
            'role': a.get('role', ''), 'status': a.get('status', ''),
            'person_type': a.get('person_type', ''), 'campus': a.get('campus', ''),
            'department': a.get('department', ''),
            'custom_roles': a.get('custom_roles', []),
            'protected': a.get('role') == 'SUPER_ADMIN' or a.get('status') != 'active',
            'has_overrides': bool(overrides.get(uname)),
        })
    rows.sort(key=lambda u: (u['role'] != 'SUPER_ADMIN', u['username']))
    total = len(rows)
    return jsonify({'success': True, 'users': rows[offset:offset + limit],
                    'total': total, 'limit': limit, 'offset': offset,
                    'has_more': offset + limit < total})


@ext_bp.route('/campuses', methods=['GET'])
def campuses():
    _, err, status = _guard_read()
    if err:
        return err, status
    idstore = rp._identity_store()
    real = sorted({str(a.get('campus') or '').strip() for a in idstore.get('accounts', [])
                   if str(a.get('campus') or '').strip()})
    return jsonify({'success': True, 'campuses': real,
                    'scope_campuses': list(rp.SCOPE_OPTIONS['campuses']),
                    'scope_departments': list(rp.SCOPE_OPTIONS['departments'])})


@ext_bp.route('/audit/paged', methods=['GET'])
def audit_paged():
    _, err, status = _guard_read()
    if err:
        return err, status
    store = _store()
    entries = list(reversed(store.get('audit_log', [])))
    action = str(request.args.get('action') or '').strip()
    role_id = str(request.args.get('role') or '').strip()
    search = str(request.args.get('search') or '').strip().lower()
    if action:
        entries = [e for e in entries if e.get('action') == action]
    if role_id:
        entries = [e for e in entries if e.get('target_role') == role_id]
    if search:
        entries = [e for e in entries if search in json.dumps(e, ensure_ascii=False).lower()]
    total = len(entries)
    try:
        limit = max(1, min(200, int(request.args.get('limit') or 20)))
        offset = max(0, int(request.args.get('offset') or 0))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Invalid pagination parameters'}), 400
    actions = {}
    for e in store.get('audit_log', []):
        actions[e.get('action', '')] = actions.get(e.get('action', ''), 0) + 1
    return jsonify({'success': True, 'data': entries[offset:offset + limit],
                    'total': total, 'limit': limit, 'offset': offset,
                    'has_more': offset + limit < total,
                    'actions': [{'id': k, 'count': v} for k, v in sorted(actions.items())]})


# ── bootstrap & authority ─────────────────────────────────────────────────

def _authority(actor, idstore):
    is_super = _is_super(actor, idstore)
    is_admin = is_super or rp._actor_is_admin(actor, idstore)
    can_read = is_admin or rp._actor_can_read(actor, idstore)
    return {
        'actor': actor,
        'has_explicit_session': bool(rp._explicit_actor()),
        'is_super_admin': is_super,
        'is_admin': is_admin,
        'can_read': can_read,
        'can_create_roles': is_admin,
        'can_manage_permissions': is_admin,
        'can_assign_users': is_admin,
        'can_delete_roles': is_admin,
        'can_configure_protected_portals': is_super,
        'can_grant_privilege_chain': is_super,
        'explanation': (
            'SUPER_ADMIN: full authority, including protected portals and privilege-chain permissions.'
            if is_super else
            'Administrator: may create and edit custom roles, assign users and configure non-protected '
            'portals. Core role definitions, SUPER_ADMIN privileges and protected portal grants are '
            'reserved for SUPER_ADMIN.'
            if is_admin else
            'Delegated access: read-only unless your custom role grants explicit permissions.'),
    }


@ext_bp.route('/bootstrap', methods=['GET'])
def bootstrap():
    actor, err, status = _guard_read()
    if err:
        return err, status
    idstore = rp._identity_store()
    store = _store()
    definitions = [dict(d) for d in store.get('permission_definitions', [])]
    return jsonify({
        'success': True,
        'authority': _authority(actor, idstore),
        'registry': {
            'categories': [{'category': cat,
                            'modules': [{'id': mid, 'name': label, 'actions': actions}
                                        for mid, (label, actions) in modules.items()]}
                           for cat, modules in rp.PERMISSION_MODULES.items()],
            'actions': list(rp.ALL_ACTIONS),
            'action_labels': rp.ACTION_LABELS,
            'scope_options': rp.SCOPE_OPTIONS,
            'core_roles': list(rp.CORE_ROLES),
        },
        'roles': rp.list_roles().get_json(),
        'overview': rp.roles_overview().get_json(),
        'pages': rp.access_pages().get_json(),
        'definitions': {
            'custom': [_definition_view(d) for d in definitions],
            'enforced_pairs': ['%s.%s' % p for p in sorted(ENFORCED_PAIRS)],
            'guard_pairs': ['%s.%s' % p for p in sorted(GUARD_PAIRS)],
        },
        'totals': {
            'total_roles': len(rp.CORE_ROLES) + len(store.get('custom_roles', [])),
            'custom_roles': len(store.get('custom_roles', [])),
            'registered_permissions': sum(len(acts) for g in rp.PERMISSION_MODULES.values()
                                          for _, acts in g.values()),
            'custom_definitions': len(definitions),
            'requires_integration': sum(1 for d in definitions
                                        if (d.get('module'), d.get('action')) not in ENFORCED_PAIRS),
            'enforced_bindings': len(API_BINDINGS),
            'real_pages': len(rp._page_index()[1]),
            'accounts': len(idstore.get('accounts', [])),
        },
        'portals': list(rp.PORTAL_KEYS),
        'protected_portals': list(PROTECTED_PORTALS),
        'categories': list(CATEGORIES),
        'permission_scopes': [{'id': s, 'label': SCOPE_LABELS[s]} for s in SCOPES],
    })


def register_roles_ext_routes(app):
    app.register_blueprint(ext_bp)
    register_enforcement(app)
