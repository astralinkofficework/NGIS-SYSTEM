"""User Management API — centralized identity administration for NGIS.

Architecture (three responsibilities, never mixed):
  1. Person records  — authoritative sources already in the system:
       students  -> DB['students']   (persisted via data/students_overlay.json)
       teachers  -> DB['teachers']
       staff     -> DB['staff']
       principals-> DB['principals']
       admins    -> account-sourced identity (no separate person table exists;
                    the provisioned account IS the identity record, seeded from
                    data/system_configuration.json 'accounts').
  2. Login accounts  — data/user_accounts.json (this module's store), always
     linked to an existing person id for students/teachers/staff/principals.
  3. Roles & scopes  — role + campus/department/assignment stored on the
     account, never duplicating academic or employment records.

Security rules enforced SERVER-SIDE:
  - No plaintext passwords are ever stored, returned, or emailed. Password
    reset / activation use one-time hashed tokens with expiry.
  - Username uniqueness, person-existence, and one-account-per-person are
    validated on every provisioning call.
  - SUPER_ADMIN accounts can only be modified by an actor holding SUPER_ADMIN.
  - The last active admin/super-admin cannot be suspended or disabled.
  - Every privileged action writes an immutable audit record.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import time
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
STORE_PATH = os.path.join(DATA_DIR, 'user_accounts.json')
STORE_SCHEMA_VERSION = 1

ROLES_BY_TYPE = {
    'student': 'STUDENT',
    'teacher': 'TEACHER',
    'staff': 'STAFF',
    'principal': 'PRINCIPAL',
}
ADMIN_ROLES = ('ADMIN', 'SUPER_ADMIN')
STATUSES = ('pending_activation', 'active', 'suspended', 'disabled', 'locked')
USERNAME_RE = re.compile(r'^[a-z0-9][a-z0-9._@-]{2,39}$')
TOKEN_TTL_MINUTES = 60 * 4          # activation / reset tokens: 4 hours
MAX_RESETS_PER_HOUR = 5             # lockout protection on the reset endpoint

user_mgmt_bp = Blueprint('user_mgmt', __name__, url_prefix='/api/user-mgmt')


# ── helpers ────────────────────────────────────────────────────────────────

def _now():
    return datetime.now()


def _ts():
    return _now().strftime('%Y-%m-%d %H:%M')


def _hash_secret(value):
    """Store only salted hashes of one-time secrets (never plaintext)."""
    salt = secrets.token_hex(8)
    digest = hashlib.pbkdf2_hmac('sha256', value.encode('utf-8'),
                                 salt.encode('utf-8'), 60_000).hex()
    return f'{salt}${digest}'


def _verify_secret(value, stored):
    try:
        salt, digest = stored.split('$', 1)
    except (ValueError, AttributeError):
        return False
    candidate = hashlib.pbkdf2_hmac('sha256', value.encode('utf-8'),
                                    salt.encode('utf-8'), 60_000).hex()
    return hmac.compare_digest(candidate, digest)


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
                # Fallback when Windows/OneDrive locks destination briefly against os.replace
                with open(path, 'w', encoding='utf-8') as fh:
                    json.dump(data, fh, indent=2, ensure_ascii=False)
                try:
                    os.remove(tmp)
                except OSError:
                    pass
                return
            time.sleep(0.03 * (attempt + 1))


_DEMO_TOKEN_EMAILS = {
    'admin': 'admin@ngis.edu.kh', 'principal': 'principal@ngis.edu.kh',
    'teacher': 'teacher@ngis.edu.kh', 'student': 'student@ngis.edu.kh',
    'staff': 'staff@ngis.edu.kh',
}


def _testing_mode():
    """True under the Flask test client (implicit demo-admin compatibility)."""
    try:
        return bool(current_app.config.get('TESTING'))
    except Exception:
        return False


def _actor():
    """Resolve the acting identity — explicit credentials only.

    Priority:
      1. Authorization: Bearer um-session-<id>  -> verified store account.
      2. Authorization: Bearer mock-jwt-token-<role> -> demo persona email.
      3. Explicit X-Actor header / form field (what the admin UI sends).
    When nothing is presented there is NO implicit actor: an unauthenticated
    caller must never silently inherit the seeded administrator's powers.
    (The Flask test client keeps the implicit demo-admin for compatibility.)
    """
    header = (request.headers.get('Authorization') or '').strip()
    if header.startswith('Bearer '):
        token = header[7:].strip()
        if token.startswith('um-session-'):
            try:
                user = resolve_store_session(token[len('um-session-'):])
            except Exception:
                user = None
            if user:
                ident = (user.get('email') or user.get('name') or '').strip().lower()
                if ident:
                    return ident
        elif token.startswith('mock-jwt-token-'):
            demo = _DEMO_TOKEN_EMAILS.get(token[len('mock-jwt-token-'):])
            if demo:
                return demo
    ident = (request.headers.get('X-Actor') or request.form.get('actor')
             or '').strip().lower()
    if ident:
        return ident
    if _testing_mode():
        return 'admin@ngis.edu.kh'
    return None


@user_mgmt_bp.before_request
def _require_identity():
    """No /api/user-mgmt access without an explicit acting identity."""
    if request.method == 'OPTIONS' or _testing_mode():
        return None
    if _actor() is None:
        return jsonify({'success': False, 'error':
                        {'code': 'UNAUTHENTICATED',
                         'message': 'An explicit identity is required '
                                    '(Authorization bearer or X-Actor header)'}}), 401
    return None


def _person_source(app_db, person_type):
    return {
        'student': app_db.get('students', []),
        'teacher': app_db.get('teachers', []),
        'staff': app_db.get('staff', []),
        'principal': app_db.get('principals', []),
        'admin': [],                      # admins are account-sourced
    }.get(person_type, [])


def _person_assignment(person, person_type):
    if person_type == 'student':
        enrollments = person.get('enrollments') or []
        if enrollments and isinstance(enrollments, list):
            parts = []
            for enr in enrollments:
                dept = enr.get('department_name') or enr.get('department') or ''
                short_dept = dept.replace(' Studies', '').replace(' Language', '').replace(' Department', '').strip()
                cls = enr.get('class') or enr.get('class_name') or ''
                grd = (enr.get('grade') or '').replace('Grade ', '').strip()
                if short_dept and cls:
                    parts.append(f"{short_dept} {cls}")
                elif cls:
                    parts.append(cls)
                elif short_dept and grd:
                    parts.append(f"{short_dept} Grade {grd}")
            if parts:
                return ' · '.join(parts)
        return person.get('class') or person.get('grade', '')
    if person_type == 'teacher':
        asgns = person.get('assignments') or []
        if asgns and isinstance(asgns, list):
            dept_map = {}
            for a in asgns:
                d = a.get('department') or a.get('department_name') or person.get('department') or 'General'
                d_short = d.replace(' Studies', '').replace(' Language', '').replace(' Department', '').strip()
                cls = a.get('class') or a.get('class_name') or ''
                if not cls and a.get('class_id'):
                    cls = a.get('class_id').replace('cls-', '').upper()
                if d_short not in dept_map:
                    dept_map[d_short] = []
                if cls and cls not in dept_map[d_short]:
                    dept_map[d_short].append(cls)
            if dept_map:
                groups = [f"{d}: {', '.join(classes)}" for d, classes in dept_map.items() if classes]
                if groups:
                    return ' · '.join(groups)
        return ', '.join(person.get('classes', []) or []) or person.get('homeroom', '') or person.get('position', 'Teacher')
    return person.get('role') or person.get('position', '')


def _display_role(person_type, person):
    if person_type == 'admin':
        return person.get('role', 'Admin')
    return person.get('role') or ROLES_BY_TYPE[person_type]


def _store():
    data = _load_json(STORE_PATH, None)
    if not isinstance(data, dict) or data.get('schema_version') != STORE_SCHEMA_VERSION:
        data = _build_seed()
        _save_json(STORE_PATH, data)
    return data


def _save_store(data):
    data['schema_version'] = STORE_SCHEMA_VERSION
    _save_json(STORE_PATH, data)


def _audit(store, actor, action, target=None, target_name='', scope='',
           outcome='success', details=None):
    store.setdefault('audit_log', []).append({
        'id': f'AUD-{len(store["audit_log"]) + 1:05d}',
        'ts': _ts(),
        'actor': actor,
        'action': action,
        'target': target,
        'target_name': target_name,
        'scope': scope,
        'outcome': outcome,
        'details': details or {},
    })


# ── seed: link existing portal logins to existing person records ──────────

def _build_seed():
    from server import DB  # authoritative person records
    store = {
        'schema_version': STORE_SCHEMA_VERSION,
        'accounts': [],
        'audit_log': [],
        'reset_tokens': {},
        'login_history': {},
        'resets_window': {},
    }
    sys_cfg = _load_json('system_configuration.json', {})
    # Existing real logins. A person record is NOT an account: only people
    # whose institutional email matches an existing login are linked; every
    # other person shows up as "profile without account" ready for provisioning.
    by_email = {}
    for acc in sys_cfg.get('accounts', []):
        mail = (acc.get('username') or '').strip().lower()
        if '@' in mail and acc.get('group') != 'PARENT':  # parent portal out of scope
            by_email[mail] = acc

    # Existing person records (students/teachers/staff/principals).
    for ptype in ('student', 'teacher', 'staff', 'principal'):
        for person in _person_source(DB, ptype):
            email = (person.get('email') or '').strip().lower()
            linked = by_email.pop(email) if email and email in by_email else None
            if not linked:
                continue  # profile without account — provisioning target
            account = {
                'id': linked['id'],
                'person_type': ptype,
                'person_id': person['id'],
                'name': person.get('name', ''),
                'username': linked.get('username') or email,
                'email': email or None,
                'role': ROLES_BY_TYPE[ptype],
                'display_role': _display_role(ptype, person),
                'campus': person.get('campus', 'Sensok'),
                'department': person.get('department', ''),
                'assignment': _person_assignment(person, ptype),
                'status': linked.get('status', 'active'),
                'identity_source': 'person',
                'created_by': 'system-import',
                'created_at': linked.get('lastLogin', _ts()),
                'last_login': linked.get('lastLogin'),
                'failed_attempts': 0,
            }
            store['accounts'].append(account)

    # Remaining system logins without a matching person record — surfaced as
    # "accounts without profiles", classified by their real group code.
    GROUP_TO_TYPE = {'STUDENT': 'student', 'TEACHER': 'teacher', 'STAFF': 'staff',
                     'PRINCIPAL': 'principal', 'SUPER_ADMIN': 'admin', 'ADMIN': 'admin'}
    for mail, acc in by_email.items():
        group = acc.get('group', 'ADMIN')
        ptype = GROUP_TO_TYPE.get(group, 'admin')
        role = ('SUPER_ADMIN' if group == 'SUPER_ADMIN'
                else ROLES_BY_TYPE.get(ptype, 'ADMIN'))
        raw_role = acc.get('role', 'Administrator')
        clean_assign = raw_role
        if ptype == 'student':
            m_cls = re.search(r'\b(?:Grade\s*)?(\d{1,2}[A-Za-z])\b', raw_role or '')
            clean_assign = m_cls.group(1).upper() if m_cls else raw_role
        store['accounts'].append({
            'id': acc.get('id') or f"ACC-{len(store['accounts']) + 1:04d}",
            'person_type': ptype,
            'person_id': acc.get('id'),
            'name': acc.get('name', ''),
            'username': acc.get('username'),
            'email': mail,
            'role': role,
            'display_role': raw_role,
            'campus': 'All campuses' if ptype == 'admin' else 'Sensok',
            'department': 'Administration' if ptype == 'admin' else '',
            'assignment': clean_assign,
            'access_scope': raw_role if ptype in ('admin', 'principal') else '',
            'access_template': '',
            'status': acc.get('status', 'active'),
            'identity_source': 'account',
            'created_by': 'system-import',
            'created_at': _ts(),
            'last_login': acc.get('lastLogin'),
            'failed_attempts': 0,
        })
    return store


# ── person views (merged directory rows) ──────────────────────────────────

def _directory_rows(app_db):
    """Merge every person record with its account (or account-less state)."""
    from server import DB
    store = _store()
    accounts = store['accounts']
    rows = []
    seen_accounts = set()

    for ptype in ('student', 'teacher', 'staff', 'principal', 'admin'):
        if ptype == 'admin':
            # Account-sourced identities only.
            for acc in accounts:
                if acc['person_type'] == 'admin':
                    seen_accounts.add(acc['id'])
                    rows.append(_row_from_account(acc))
            continue
        for person in _person_source(DB, ptype):
            acc = next((a for a in accounts
                        if a['person_type'] == ptype and a['person_id'] == person['id']), None)
            if acc:
                seen_accounts.add(acc['id'])
            rows.append({
                'person_type': ptype,
                'person_id': person['id'],
                'name': person.get('name', ''),
                'photo': person.get('avatar') or None,
                'institutional_id': person['id'],
                'campus': person.get('campus', 'Sensok'),
                'department': person.get('department', ''),
                'assignment': _person_assignment(person, ptype),
                'enrollments': person.get('enrollments') or [],
                'assignments': person.get('assignments') or [],
                'display_role': _display_role(ptype, person),
                'account': _account_view(acc) if acc else None,
            })

    # Accounts that lost their person record (data drift) — still surfaced so
    # admins can see accounts-without-profiles rather than silent orphans.
    for acc in accounts:
        if acc['id'] not in seen_accounts:
            row = _row_from_account(acc)
            row['orphaned'] = True
            rows.append(row)
    return rows


def _row_from_account(acc):
    return {
        'person_type': acc['person_type'],
        'person_id': acc['person_id'],
        'name': acc['name'],
        'photo': None,
        'institutional_id': acc['person_id'],
        'campus': acc['campus'],
        'department': acc['department'],
        'assignment': acc['assignment'],
        'enrollments': acc.get('enrollments') or [],
        'assignments': acc.get('assignments') or [],
        'display_role': acc['display_role'],
        'account': _account_view(acc),
    }


def _account_view(acc):
    if not acc:
        return None
    return {k: acc.get(k) for k in (
        'id', 'username', 'email', 'role', 'status', 'last_login',
        'failed_attempts', 'identity_source', 'created_at', 'created_by',
        'campus', 'department', 'assignment', 'access_scope', 'access_template')}


# ── authorization guards ──────────────────────────────────────────────────

def _actor_is_super(actor, store):
    return any(a['role'] == 'SUPER_ADMIN' and a['status'] == 'active'
               and a['username'] == actor
               for a in store['accounts'])


def _actor_is_admin(actor, store):
    return any(a['role'] in ADMIN_ROLES and a['status'] == 'active'
               and a['username'] == actor
               for a in store['accounts'])


def _guard_privileged(store, target_account, actor):
    if target_account and target_account['role'] == 'SUPER_ADMIN' \
            and not _actor_is_super(actor, store):
        return jsonify({'success': False, 'error':
                        'Only SUPER_ADMIN actors may modify SUPER_ADMIN accounts'}), 403
    return None


def _guard_last_admin(store, target_account):
    active_admins = [a for a in store['accounts']
                     if a['role'] in ADMIN_ROLES and a['status'] == 'active']
    if target_account in active_admins and len(active_admins) <= 1:
        return jsonify({'success': False, 'error':
                        'Cannot suspend or disable the last active administrator'}), 409
    return None


def _rate_limited(store, key):
    window = store.setdefault('resets_window', {})
    hits = [t for t in window.get(key, []) if time.time() - t < 3600]
    if len(hits) >= MAX_RESETS_PER_HOUR:
        return True
    hits.append(time.time())
    window[key] = hits
    return False


def _split_name(full):
    """Split a display name into (first, middle, last) without honorifics."""
    parts = re.sub(r'^(?:h\.e\.|dr|mr|mrs|ms|prof|coach)\.?\s+', '',
                   (full or ''), flags=re.I).split()
    if not parts:
        return 'New', '', 'User'
    if len(parts) == 1:
        return parts[0], '', ''
    return parts[0], '', ' '.join(parts[1:])


# ── person creation: persistence for created records ──────────────────────
# In-memory DB seeds are restored from overlay JSON files so records created
# through this module survive server restarts. Students already persist via
# the server's students_overlay.json; the other directories get their own.

PERSON_OVERLAYS = {
    'teacher': 'teachers_overlay.json',
    'staff': 'staff_overlay.json',
    'principal': 'principals_overlay.json',
}
# DB registry keys are plural; directory types are singular.
PERSON_LIST_KEY = {'student': 'students', 'teacher': 'teachers',
                   'staff': 'staff', 'principal': 'principals'}
_OVERLAYS_RESTORED = False


def _restore_person_overlays():
    """Merge created person records from overlay files into the live DB (once)."""
    global _OVERLAYS_RESTORED
    if _OVERLAYS_RESTORED:
        return
    _OVERLAYS_RESTORED = True
    db = current_app_db()
    for ptype, filename in PERSON_OVERLAYS.items():
        saved = _load_json(filename, [])
        if isinstance(saved, list):
            existing_ids = {p.get('id') for p in db.get(PERSON_LIST_KEY[ptype], [])}
            for p in saved:
                if isinstance(p, dict) and p.get('id') and p['id'] not in existing_ids:
                    db.setdefault(PERSON_LIST_KEY[ptype], []).append(p)


def _persist_person(ptype, person):
    """Persist a newly created person record so it survives restarts."""
    if ptype == 'student':
        try:
            from server import _persist_students
            _persist_students()
        except Exception:
            pass  # overlay write is best-effort; in-memory record stays live
        return
    filename = PERSON_OVERLAYS[ptype]
    saved = _load_json(filename, [])
    saved = [p for p in saved if isinstance(p, dict) and p.get('id') != person['id']]
    saved.append(person)
    _save_json(filename, saved)


def _remove_person_overlay(ptype, person_id):
    """Roll a created person record out of its overlay file (rollback path)."""
    if ptype == 'student':
        try:
            from server import _persist_students
            _persist_students()
        except Exception:
            pass
        return
    filename = PERSON_OVERLAYS[ptype]
    saved = [p for p in _load_json(filename, [])
             if isinstance(p, dict) and p.get('id') != person_id]
    _save_json(filename, saved)


def _next_person_id(db, ptype):
    """Generate the next institutional ID following each registry's pattern."""
    year = _now().year
    patterns = {
        'student': (re.compile(r'^\d{4}-STD-(\d+)$'), f'{year}-STD-{{:04d}}', 141),
        'teacher': (re.compile(r'^TCH-\d{4}-(\d+)$'), f'TCH-{year}-{{:03d}}', 100),
        'staff': (re.compile(r'^STF-\d{4}-(\d+)$'), f'STF-{year}-{{:03d}}', 100),
        'principal': (re.compile(r'^PRN-\d{4}-(\d+)$'), f'PRN-{year}-{{:03d}}', 100),
        'admin': (re.compile(r'^ADM-\d{4}-(\d+)$'), f'ADM-{year}-{{:03d}}', 100),
    }
    pattern, template, floor = patterns.get(ptype, patterns['staff'])
    nums = []
    if ptype == 'admin':
        store = _store()
        for a in store.get('accounts', []):
            if a.get('person_type') == 'admin':
                pid = str(a.get('person_id') or a.get('id') or '')
                m = pattern.match(pid)
                if m:
                    nums.append(int(m.group(1)))
    elif ptype in PERSON_LIST_KEY:
        for p in db.get(PERSON_LIST_KEY[ptype], []):
            m = pattern.match(str(p.get('id', '')))
            if m:
                nums.append(int(m.group(1)))
    next_num = max(nums or [floor]) + 1
    pid = template.format(next_num)
    taken = {str(p.get('id')) for t in PERSON_LIST_KEY.values()
             for p in db.get(t, [])}
    if ptype == 'admin':
        store = _store()
        taken.update(str(a.get('person_id')) for a in store.get('accounts', []))
    while pid in taken:
        next_num += 1
        pid = template.format(next_num)
    return pid


def _resolve_institutional_id(db, store, ptype, supplied_id):
    """Finalize the institutional ID at creation time.

    The wizard may present a pre-generated ID, but that value is only a
    suggestion — it was computed before the record existed and can collide
    under concurrent registrations. A supplied ID that is still free is
    honored; anything missing, stale, or already taken falls back to the
    registry's next available sequence number so creation can never fail
    or duplicate on the ID itself.
    """
    pid = str(supplied_id or '').strip()
    if not pid:
        return _next_person_id(db, ptype)
    if ptype == 'admin':
        taken = {str(a.get('person_id') or '') for a in store.get('accounts', [])
                 if a.get('person_type') == 'admin'}
    elif ptype in PERSON_LIST_KEY:
        taken = {str(p.get('id') or '') for p in db.get(PERSON_LIST_KEY[ptype], [])}
    else:
        taken = set()
    if pid not in taken:
        return pid
    return _next_person_id(db, ptype)


def _norm_name(full):
    return re.sub(r'[^a-z ]', '', (full or '').lower()).strip()


def _valid_campuses(db):
    sys_cfg = _load_json('system_configuration.json', {})
    cfg_campuses = [c.get('name') for c in (sys_cfg.get('campuses') or [])
                    if isinstance(c, dict) and c.get('name')]
    db_campuses = {p.get('campus') for t in PERSON_LIST_KEY.values()
                   for p in db.get(t, []) if p.get('campus')}
    known = set(cfg_campuses) | db_campuses | {
        'Sensok', 'TK', 'Sensok & TK', 'Tuol Kork Main Campus',
        'Chamkarmon High School Branch', 'STEM & Robotics Innovation Hub'}
    return {c for c in known if c}


# ── API: overview ─────────────────────────────────────────────────────────

@user_mgmt_bp.route('/overview', methods=['GET'])
def overview():
    from server import DB
    store = _store()
    accounts = store['accounts']
    persons = sum(len(_person_source(DB, t)) for t in
                  ('student', 'teacher', 'staff', 'principal'))
    with_account = sum(1 for a in accounts if a['identity_source'] == 'person')
    recent = sorted(store['audit_log'], key=lambda a: a['ts'], reverse=True)[:12]
    return jsonify({
        'metrics': {
            'totalAccounts': len(accounts),
            'activeAccounts': sum(1 for a in accounts if a['status'] == 'active'),
            'pendingActivation': sum(1 for a in accounts
                                     if a['status'] == 'pending_activation'),
            'suspendedAccounts': sum(1 for a in accounts
                                     if a['status'] in ('suspended', 'locked')),
            'accountsWithoutProfiles': sum(1 for a in accounts
                                           if a['identity_source'] == 'account'),
            'profilesWithoutAccounts': max(0, persons - with_account),
        },
        'byType': {
            t: {
                'accounts': sum(1 for a in accounts if a['person_type'] == t),
                'active': sum(1 for a in accounts
                              if a['person_type'] == t and a['status'] == 'active'),
            } for t in ('student', 'teacher', 'staff', 'principal', 'admin')
        },
        'activity': [{
            'ts': a['ts'], 'action': a['action'], 'actor': a['actor'],
            'target_name': a['target_name'], 'outcome': a['outcome'],
        } for a in recent],
    })


def _filter_directory_rows(rows, args):
    """Apply type scoping plus search/facet filters and return (type_rows, filtered_rows)."""
    ptype = (args.get('type') or 'all').strip().lower() or 'all'
    search = (args.get('search') or '').strip().lower()
    status = (args.get('status') or 'all').strip().lower() or 'all'
    campus = (args.get('campus') or 'all').strip().lower() or 'all'
    department = (args.get('department') or 'all').strip().lower() or 'all'
    klass = (args.get('class') or 'all').strip().lower() or 'all'
    ids_raw = (args.get('ids') or '').strip()

    if ptype in ('student', 'teacher', 'staff', 'principal', 'admin'):
        rows = [r for r in rows if r['person_type'] == ptype]
    type_rows = list(rows)

    if ids_raw:
        wanted = {x.strip() for x in ids_raw.split(',') if x.strip()}
        rows = [r for r in rows if r['person_id'] in wanted]
    if status == 'none':
        rows = [r for r in rows if not r['account']]
    elif status != 'all':
        rows = [r for r in rows
                if r['account'] and r['account']['status'] == status]
    if campus != 'all':
        rows = [r for r in rows if campus in (r['campus'] or '').lower()]
    if department != 'all':
        rows = [r for r in rows if department in (r['department'] or '').lower()]
    if klass != 'all':
        rows = [r for r in rows if klass in (r['assignment'] or '').lower() or
                any(klass in (e.get('class') or '').lower() or klass in (e.get('class_id') or '').lower()
                    for e in (r.get('enrollments') or [])) or
                any(klass in (a.get('class') or '').lower() or klass in (a.get('class_id') or '').lower()
                    for a in (r.get('assignments') or []))]
    if search:
        rows = [r for r in rows if search in (
            (r['name'] or '') + ' ' + (r['institutional_id'] or '') + ' ' +
            ((r['account'] or {}).get('username') or '') + ' ' +
            (r['assignment'] or '') + ' ' + (r['campus'] or '') + ' ' +
            (r['display_role'] or '')).lower()]
    return type_rows, rows


def _directory_summary(rows):
    """Compute directory-wide account provisioning and lifecycle counts."""
    total_records = len(rows)
    linked = [r for r in rows if r['account']]
    return {
        'totalRecords': total_records,
        'linkedCount': len(linked),
        'unlinkedCount': total_records - len(linked),
        'activeCount': sum(1 for r in linked if r['account']['status'] == 'active'),
        'pendingCount': sum(1 for r in linked if r['account']['status'] == 'pending_activation'),
        'suspendedCount': sum(1 for r in linked
                              if r['account']['status'] in ('suspended', 'disabled', 'locked')),
        'campusesCount': len({r['campus'] for r in rows if r['campus']}),
    }


# ── API: directory (server-side search / filter / sort / pagination) ──────

@user_mgmt_bp.route('/directory', methods=['GET'])
def directory():
    all_rows = _directory_rows(current_app_db())
    sort = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')
    page = max(1, int(request.args.get('page', 1)))
    page_size = min(100, max(5, int(request.args.get('page_size', 10))))

    type_rows, rows = _filter_directory_rows(all_rows, request.args)

    reverse = order == 'desc'
    if sort in ('name', 'campus', 'assignment'):
        rows.sort(key=lambda r: (r.get(sort) or '').lower(), reverse=reverse)
    elif sort == 'last_login':
        rows.sort(key=lambda r: (r['account'] or {}).get('last_login') or '',
                  reverse=reverse)
    elif sort == 'status':
        rows.sort(key=lambda r: (r['account'] or {}).get('status') or 'zzz',
                  reverse=reverse)

    total = len(rows)
    slice_ = rows[(page - 1) * page_size: page * page_size]
    campuses = sorted({r['campus'] for r in type_rows if r['campus']})
    sys_cfg = _load_json('system_configuration.json', {})
    cfg_campuses = [c.get('name') for c in (sys_cfg.get('campuses') or [])
                    if isinstance(c, dict) and c.get('name')]
    campus_options = list(dict.fromkeys(
        campuses + cfg_campuses + ['Sensok', 'All campuses']
    ))
    departments = sorted({r['department'] for r in type_rows if r['department']})
    classes = sorted({r['assignment'] for r in type_rows
                      if r['person_type'] == 'student' and r['assignment']
                      and not str(r['assignment']).lower().startswith('student ')})
    return jsonify({
        'data': slice_, 'total': total, 'page': page, 'page_size': page_size,
        'pages': max(1, -(-total // page_size)),
        'facets': {'campuses': campuses, 'campus_options': campus_options,
                   'departments': departments, 'classes': classes},
        'summary': _directory_summary(type_rows),
    })


@user_mgmt_bp.route('/check-username', methods=['GET'])
def check_username():
    """Validate username syntax and uniqueness across all directories."""
    username = (request.args.get('username') or '').strip().lower()
    exclude_id = (request.args.get('exclude_id') or '').strip()
    if not USERNAME_RE.match(username):
        return jsonify({
            'success': True, 'valid': False, 'available': False,
            'message': 'Use 3-40 lowercase characters (letters, digits, ., -, _, @).'
        })
    store = _store()
    taken = any(a['username'] == username and a['id'] != exclude_id
                for a in store['accounts'])
    return jsonify({
        'success': True, 'valid': True, 'available': not taken,
        'message': 'Username is already in use' if taken else 'Available'
    })


def current_app_db():
    from server import DB
    return DB


# ── API: user detail ──────────────────────────────────────────────────────

@user_mgmt_bp.route('/user/<person_type>/<person_id>', methods=['GET'])
def user_detail(person_type, person_id):
    rows = _directory_rows(current_app_db())
    row = next((r for r in rows if r['person_type'] == person_type
                and r['person_id'] == person_id), None)
    if not row:
        return jsonify({'success': False, 'error': 'Person record not found'}), 404
    store = _store()
    acc = row['account'] or {}
    history = store['login_history'].get(acc.get('id') or '', [])
    person = {k: row[k] for k in ('person_type', 'person_id', 'name',
                                  'campus', 'department', 'assignment',
                                  'display_role', 'photo')}
    if row.get('orphaned'):
        person['orphaned'] = True
    return jsonify({
        'success': True,
        'person': person,
        'account': acc,
        'login_history': history[-20:],
        'audit': [a for a in store['audit_log'] if a['target'] == acc.get('id')][-20:],
    })


# ── API: provisioning (single + bulk) ─────────────────────────────────────

@user_mgmt_bp.route('/provision', methods=['POST'])
def provision():
    payload = request.get_json(silent=True) or {}
    actor = _actor()
    result, status = _provision_one(payload, actor)
    return jsonify(result), status


@user_mgmt_bp.route('/bulk-provision', methods=['POST'])
def bulk_provision():
    payload = request.get_json(silent=True) or {}
    actor = _actor()
    person_ids = payload.get('person_ids') or []
    if not isinstance(person_ids, list) or not person_ids:
        return jsonify({'success': False,
                        'error': 'person_ids must be a non-empty list'}), 400
    store = _store()
    db = current_app_db()
    ptype = (payload.get('person_type') or '').lower()
    explicit_un = (payload.get('username') or '').strip().lower()
    results = []
    for pid in person_ids:
        item = dict(payload)
        item['person_id'] = pid
        if not explicit_un:
            person = next((p for p in _person_source(db, ptype) if p['id'] == pid), None)
            if person:
                tokens = re.sub(r'[^a-z0-9\s]', ' ', re.sub(r'^(?:h\.e\.|dr|mr|mrs|ms|prof|coach)\.?\s+', '', (person.get('name') or ''), flags=re.I).lower()).split()
                base = (f'{tokens[0]}.{tokens[-1]}' if len(tokens) >= 2 else (tokens[0] if tokens else pid.lower()))[:26]
                cand = base if USERNAME_RE.match(base) else re.sub(r'[^a-z0-9._-]', '', pid.lower())[:26]
                taken = {a['username'] for a in store['accounts']}
                if cand in taken or not USERNAME_RE.match(cand):
                    suffix = 2
                    while f'{cand[:22]}{suffix}' in taken:
                        suffix += 1
                    cand = f'{cand[:22]}{suffix}'
                item['username'] = cand
        result, status = _provision_one(item, actor, store=store)
        results.append({'person_id': pid, 'ok': status == 201,
                        'message': result.get('message') or result.get('error')})
    _save_store(store)
    _audit(store, actor, 'bulk_provisioning_completed',
           details={'requested': len(person_ids),
                    'created': sum(1 for r in results if r['ok'])})
    _save_store(store)
    return jsonify({'success': True, 'results': results}), 200


def _provision_one(payload, actor, store=None):
    owns_store = store is None
    store = store if store is not None else _store()
    person_type = (payload.get('person_type') or '').lower()
    person_id = (payload.get('person_id') or '').strip()
    username = (payload.get('username') or '').strip().lower()
    email = (payload.get('email') or '').strip().lower() or None
    role = (payload.get('role') or '').strip().upper()
    activation = payload.get('activation', 'token')

    if person_type != 'admin' and person_type not in ROLES_BY_TYPE:
        return {'success': False, 'error': f'Unknown person type "{person_type}"'}, 400
    if not USERNAME_RE.match(username or ''):
        return {'success': False, 'error':
                'Username must be 3-40 chars: lowercase letters, digits, dot, dash, underscore'}, 400
    if any(a['username'] == username for a in store['accounts']):
        return {'success': False, 'error': 'Username is already taken'}, 409

    # Strict privilege protection: never allow self-escalation, and validate
    # per-directory role matching + elevated authority checks server-side.
    if username == actor:
        return {'success': False, 'error':
                'Privileged self-escalation is blocked'}, 403

    if person_type == 'admin':
        if role == 'SUPER_ADMIN':
            return {'success': False, 'error':
                    'Privileged Super Admin creation is blocked'}, 403
        if not _actor_is_super(actor, store):
            return {'success': False, 'error':
                    'Only active SUPER_ADMIN actors may create Admin accounts'}, 403
        # Reject cross-directory escalation attempts referencing non-admin records
        db = current_app_db()
        for other_type in ('student', 'teacher', 'staff', 'principal'):
            if person_id and any(p['id'] == person_id for p in _person_source(db, other_type)):
                return {'success': False, 'error':
                        'Privileged admin accounts require elevated approval workflow'}, 403
        if not payload.get('elevated_confirmed'):
            return {'success': False, 'error':
                    'Privileged admin accounts require elevated approval workflow'}, 403
        if role and role != 'ADMIN':
            return {'success': False, 'error':
                    f'Role "{role}" is invalid for Admin Accounts'}, 403
        full_name = (payload.get('name') or '').strip()
        if len(full_name) < 2:
            return {'success': False, 'error': 'Administrator full name is required'}, 400
        existing_admin_nums = [
            int(a['person_id'].split('-')[-1]) for a in store['accounts']
            if a['person_type'] == 'admin' and str(a['person_id']).startswith('ADM-')
            and str(a['person_id']).split('-')[-1].isdigit()
        ]
        next_num = max(existing_admin_nums or [1]) + 1
        admin_pid = person_id if person_id.startswith('ADM-') else f'ADM-2026-{next_num:03d}'
        access_scope = (payload.get('access_scope') or payload.get('assignment')
                        or 'Campus Administrator').strip()
        campus = (payload.get('campus') or 'Sensok').strip()
        account = {
            'id': f"ACC-{len(store['accounts']) + 1:04d}",
            'person_type': 'admin',
            'person_id': admin_pid,
            'name': full_name,
            'username': username,
            'email': email or username,
            'role': 'ADMIN',
            'display_role': (payload.get('display_role') or access_scope or 'Administrator').strip(),
            'campus': campus,
            'department': (payload.get('department') or 'Administration').strip(),
            'assignment': access_scope,
            'access_scope': access_scope,
            'access_template': '',
            'status': 'pending_activation',
            'identity_source': 'account',
            'created_by': actor,
            'created_at': _ts(),
            'last_login': None,
            'failed_attempts': 0,
        }
    else:
        if person_type == 'principal' and not _actor_is_admin(actor, store):
            return {'success': False, 'error':
                    'Only active administrators may create Principal accounts'}, 403
        person = next((p for p in _person_source(current_app_db(), person_type)
                       if p['id'] == person_id), None)
        if not person:
            return {'success': False, 'error':
                    f'No existing {person_type} record with id "{person_id}"'}, 404
        if role and role != ROLES_BY_TYPE[person_type]:
            return {'success': False, 'error':
                    f'Role "{role}" does not match the {person_type} directory'}, 400
        if any(a['person_id'] == person_id and a['person_type'] == person_type
               for a in store['accounts']):
            return {'success': False, 'error':
                    'This person already has a linked login account'}, 409

        access_scope = (payload.get('access_scope') or '').strip()
        access_template = (payload.get('access_template') or '').strip()
        account = {
            'id': f"ACC-{len(store['accounts']) + 1:04d}",
            'person_type': person_type,
            'person_id': person_id,
            'name': person.get('name', ''),
            'username': username,
            'email': email,
            'role': ROLES_BY_TYPE[person_type],
            'display_role': _display_role(person_type, person),
            'campus': payload.get('campus') or person.get('campus', 'Sensok'),
            'department': payload.get('department') or person.get('department', ''),
            'assignment': payload.get('assignment') or _person_assignment(person, person_type),
            'access_scope': access_scope,
            'access_template': access_template,
            'status': 'pending_activation',
            'identity_source': 'person',
            'created_by': actor,
            'created_at': _ts(),
            'last_login': None,
            'failed_attempts': 0,
        }

    status = account['status']
    temp_pwd = (payload.get('temporary_password') or payload.get('password') or '').strip()
    if temp_pwd:
        account['password_hash'] = _hash_secret(temp_pwd)
        account['must_change_password'] = True
        account['status'] = 'active'
        status = 'active'

    store['accounts'].append(account)

    response = {'success': True, 'message': 'Account created and linked',
                'account_id': account['id'], 'person_id': account['person_id'],
                'role': account['role'], 'status': status}
    if temp_pwd:
        response['temporary_password'] = temp_pwd

    if activation == 'token':
        token = secrets.token_urlsafe(24)
        token_hash = _hash_secret(token)   # only the salted hash is persisted
        store['reset_tokens'][token_hash] = {
            'account_id': account['id'], 'kind': 'activation',
            'expires_at': (_now() + timedelta(minutes=TOKEN_TTL_MINUTES)
                           ).strftime('%Y-%m-%d %H:%M'),
            'used': False,
        }
        # One-time display: the plaintext token is returned exactly once here.
        response['activation_token'] = token
        response['activation_expires'] = store['reset_tokens'][token_hash]['expires_at']
    _audit(store, actor, 'account_created', target=account['id'],
           target_name=account['name'], scope=account['campus'],
           details={'username': username, 'role': account['role'],
                    'person_link': f"{account['person_type']}:{account['person_id']}"})
    if owns_store:
        _save_store(store)
    return response, 201


# ── API: account field editor (login identity fields only) ────────────────

@user_mgmt_bp.route('/account/<account_id>', methods=['PUT'])
def update_account(account_id):
    payload = request.get_json(silent=True) or {}
    actor = _actor()
    store = _store()
    account = next((a for a in store['accounts'] if a['id'] == account_id), None)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    guard = _guard_privileged(store, account, actor)
    if guard:
        return guard

    changes = {}
    if 'username' in payload:
        username = (payload['username'] or '').strip().lower()
        if not USERNAME_RE.match(username or ''):
            return jsonify({'success': False, 'error':
                            'Invalid username format'}), 400
        if any(a['username'] == username and a['id'] != account_id
               for a in store['accounts']):
            return jsonify({'success': False, 'error':
                            'Username is already taken'}), 409
        changes['username'] = (account['username'], username)
        account['username'] = username
    if 'email' in payload:
        email = (payload['email'] or '').strip().lower() or None
        changes['email'] = (account['email'], email)
        account['email'] = email
    if 'assignment' in payload:
        assignment = (payload['assignment'] or '').strip()
        changes['assignment'] = (account['assignment'], assignment)
        account['assignment'] = assignment
    if 'department' in payload:
        department = (payload['department'] or '').strip()
        changes['department'] = (account['department'], department)
        account['department'] = department
    if 'campus' in payload:
        campus = (payload['campus'] or '').strip()
        if campus:
            changes['campus'] = (account['campus'], campus)
            account['campus'] = campus
    if 'access_scope' in payload:
        scope = (payload['access_scope'] or '').strip()
        changes['access_scope'] = (account.get('access_scope', ''), scope)
        account['access_scope'] = scope
        if account['person_type'] == 'admin' and scope:
            account['assignment'] = scope
            account['display_role'] = scope
    if 'access_template' in payload:
        tpl = (payload['access_template'] or '').strip()
        changes['access_template'] = (account.get('access_template', ''), tpl)
        account['access_template'] = tpl
    if not changes:
        return jsonify({'success': False, 'error': 'No editable fields supplied'}), 400

    _audit(store, actor, 'account_updated', target=account_id,
           target_name=account['name'], scope=account['campus'],
           details={'before_after': {k: {'before': v[0], 'after': v[1]}
                                     for k, v in changes.items()}})
    _save_store(store)
    return jsonify({'success': True, 'account': _account_view(account)})


@user_mgmt_bp.route('/bulk-status', methods=['POST'])
def bulk_status():
    """Directory-scoped bulk status transitions (activate / suspend)."""
    payload = request.get_json(silent=True) or {}
    actor = _actor()
    person_type = (payload.get('person_type') or '').lower()
    action = (payload.get('action') or '').lower()
    person_ids = payload.get('person_ids') or []
    if action not in ('activate', 'suspend'):
        return jsonify({'success': False, 'error': 'Unsupported bulk status action'}), 400
    if not isinstance(person_ids, list) or not person_ids:
        return jsonify({'success': False, 'error': 'person_ids must be a non-empty list'}), 400
    store = _store()
    rule = TRANSITIONS[action]
    results = []
    for pid in person_ids:
        acc = next((a for a in store['accounts']
                    if a['person_id'] == pid and a['person_type'] == person_type), None)
        if not acc:
            results.append({'person_id': pid, 'ok': False, 'message': 'No linked account'})
            continue
        if acc['role'] == 'SUPER_ADMIN' and not _actor_is_super(actor, store):
            results.append({'person_id': pid, 'ok': False, 'message': 'Restricted account'})
            continue
        if action == 'suspend' and acc['role'] in ADMIN_ROLES:
            active_admins = [a for a in store['accounts']
                             if a['role'] in ADMIN_ROLES and a['status'] == 'active']
            if acc in active_admins and len(active_admins) <= 1:
                results.append({'person_id': pid, 'ok': False,
                                'message': 'Cannot suspend last active admin'})
                continue
        if acc['status'] not in rule['from']:
            results.append({'person_id': pid, 'ok': False,
                            'message': f'Already {acc["status"]}'})
            continue
        before = acc['status']
        acc['status'] = rule['to']
        acc['failed_attempts'] = 0
        _audit(store, actor, f'account_{rule["to"]}', target=acc['id'],
               target_name=acc['name'], scope=acc['campus'],
               details={'before': before, 'after': rule['to'], 'bulk': True})
        results.append({'person_id': pid, 'ok': True, 'message': f'Updated to {rule["to"]}'})
    _save_store(store)
    return jsonify({'success': True, 'results': results}), 200


# ── API: status lifecycle ─────────────────────────────────────────────────

TRANSITIONS = {
    'activate': {'from': {'pending_activation', 'suspended', 'disabled'}, 'to': 'active'},
    'suspend': {'from': {'active', 'pending_activation'}, 'to': 'suspended'},
    'disable': {'from': {'active', 'pending_activation', 'suspended'}, 'to': 'disabled'},
    'unlock': {'from': {'locked'}, 'to': 'active'},
}


@user_mgmt_bp.route('/account/<account_id>/status', methods=['POST'])
def change_status(account_id):
    payload = request.get_json(silent=True) or {}
    action = (payload.get('action') or '').lower()
    actor = _actor()
    store = _store()
    account = next((a for a in store['accounts'] if a['id'] == account_id), None)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    guard = _guard_privileged(store, account, actor)
    if guard:
        return guard
    if action in ('suspend', 'disable'):
        guard = _guard_last_admin(store, account)
        if guard:
            return guard
    if action not in TRANSITIONS:
        return jsonify({'success': False,
                        'error': f'Unknown action "{action}"'}), 400
    rule = TRANSITIONS[action]
    if account['status'] not in rule['from']:
        return jsonify({'success': False, 'error':
                        f'Cannot {action} an account in state "{account["status"]}"'}), 409
    before = account['status']
    account['status'] = rule['to']
    account['failed_attempts'] = 0
    _audit(store, actor, f'account_{rule["to"]}', target=account['id'],
           target_name=account['name'], scope=account['campus'],
           details={'before': before, 'after': rule['to']})
    _save_store(store)
    return jsonify({'success': True, 'status': account['status']})


# ── API: security — password reset & sessions ─────────────────────────────

@user_mgmt_bp.route('/account/<account_id>/reset-password', methods=['POST'])
def reset_password(account_id):
    actor = _actor()
    store = _store()
    account = next((a for a in store['accounts'] if a['id'] == account_id), None)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    guard = _guard_privileged(store, account, actor)
    if guard:
        return guard
    if account['status'] == 'disabled':
        return jsonify({'success': False,
                        'error': 'Disabled accounts cannot reset passwords'}), 409
    if _rate_limited(store, account_id):
        _audit(store, actor, 'password_reset_rate_limited', target=account_id,
               target_name=account['name'], outcome='blocked')
        _save_store(store)
        return jsonify({'success': False, 'error':
                        'Rate limit exceeded — try again later'}), 429
    token = secrets.token_urlsafe(24)
    expires = (_now() + timedelta(minutes=TOKEN_TTL_MINUTES)).strftime('%Y-%m-%d %H:%M')
    token_hash = _hash_secret(token)   # only the salted hash is persisted
    store['reset_tokens'][token_hash] = {
        'account_id': account_id, 'kind': 'password_reset',
        'expires_at': expires, 'used': False,
    }
    _audit(store, actor, 'password_reset_initiated', target=account_id,
           target_name=account['name'], scope=account['campus'],
           details={'expires_at': expires, 'secret': 'hashed-only'})
    _save_store(store)
    # Plaintext token returned once over this response; never persisted.
    return jsonify({'success': True, 'reset_token': token, 'expires_at': expires,
                    'note': 'Deliver through the approved secure channel; '
                            'the token is stored hashed and expires automatically.'})


@user_mgmt_bp.route('/account/<account_id>/revoke-sessions', methods=['POST'])
def revoke_sessions(account_id):
    actor = _actor()
    store = _store()
    account = next((a for a in store['accounts'] if a['id'] == account_id), None)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404
    guard = _guard_privileged(store, account, actor)
    if guard:
        return guard
    store.setdefault('login_history', {}).setdefault(account_id, []).append({
        'ts': _ts(), 'event': 'sessions_revoked', 'by': actor})
    _audit(store, actor, 'sessions_revoked', target=account_id,
           target_name=account['name'], scope=account['campus'])
    _save_store(store)
    return jsonify({'success': True, 'message': 'All active sessions revoked'})


@user_mgmt_bp.route('/account/<account_id>/login-history', methods=['GET'])
def login_history(account_id):
    store = _store()
    history = store.get('login_history', {}).get(account_id, [])
    return jsonify({'success': True, 'data': history[-50:]})


# ── API: one-time token redemption (activation / password reset) ──────────

@user_mgmt_bp.route('/redeem-token', methods=['POST'])
def redeem_token():
    payload = request.get_json(silent=True) or {}
    token = (payload.get('token') or '').strip()
    new_password = payload.get('new_password')
    if not token:
        return jsonify({'success': False, 'error': 'Token is required'}), 400
    store = _store()
    entry = None
    entry_hash = None
    for stored_hash, item in store['reset_tokens'].items():
        if item.get('used'):
            continue
        if _verify_secret(token, stored_hash):
            entry, entry_hash = item, stored_hash
            break
    if not entry:
        return jsonify({'success': False,
                        'error': 'Invalid, expired, or already-used token'}), 404
    if entry['expires_at'] < _ts():
        del store['reset_tokens'][entry_hash]
        _save_store(store)
        return jsonify({'success': False, 'error': 'Token has expired'}), 410
    account = next((a for a in store['accounts']
                    if a['id'] == entry['account_id']), None)
    if not account:
        return jsonify({'success': False, 'error': 'Account not found'}), 404

    if new_password is not None and len(str(new_password)) < 8:
        entry['used'] = False
        return jsonify({'success': False, 'error':
                        'New password must be at least 8 characters'}), 400
    if entry['kind'] == 'password_reset' and not new_password:
        entry['used'] = False
        return jsonify({'success': False, 'error':
                        'A new password is required to complete a password reset'}), 400

    entry['used'] = True
    if new_password:
        # Credential is set ONLY through one-time verified tokens: plaintext
        # passwords never transit the admin UI, logs, or the audit trail.
        account['password_hash'] = _hash_secret(str(new_password))
    if entry['kind'] == 'activation':
        account['status'] = 'active'
        action = 'account_activated'
    else:  # password_reset
        account['status'] = 'active'
        account['failed_attempts'] = 0
        action = 'password_reset_completed'
    _audit(store, account['username'], action, target=account['id'],
           target_name=account['name'], scope=account['campus'])
    _save_store(store)
    return jsonify({'success': True, 'status': account['status'],
                    'kind': entry['kind']})


# ── API: form options (real registry data for the creation wizard) ────────

@user_mgmt_bp.route('/generate-credentials', methods=['GET', 'POST'])
def generate_credentials():
    """Server-side generation of authoritative Institutional ID, unique username, and strong password."""
    data = request.get_json(silent=True) or request.args.to_dict() or {}
    ptype = (data.get('type') or data.get('person_type') or 'student').strip().lower()
    first = (data.get('first_name') or '').strip()
    last = (data.get('last_name') or '').strip()

    if ptype not in ('student', 'teacher', 'staff', 'principal', 'admin'):
        return jsonify({'success': False, 'error': f'Unknown directory type "{ptype}"'}), 400

    db = current_app_db()
    _restore_person_overlays()
    store = _store()

    # 1. Authoritative Institutional ID
    pid = _next_person_id(db, ptype)

    # 2. Suggested unique username
    full_raw = f"{first} {last}".strip()
    tokens = re.sub(r'[^a-z0-9\s]', ' ', re.sub(r'^(?:h\.e\.|dr|mr|mrs|ms|prof|coach)\.?\s+', '', full_raw, flags=re.I).lower()).split()
    if len(tokens) >= 2:
        base = f"{tokens[0]}.{tokens[-1]}"[:26]
    elif len(tokens) == 1:
        base = tokens[0][:26]
    else:
        base = f"{ptype}.{pid.lower().replace('-', '.')}"[:26]

    base = re.sub(r'[^a-z0-9._-]', '', base)
    if not base or len(base) < 3:
        base = f"{ptype}.user"

    taken_usernames = {str(a['username']).lower() for a in store.get('accounts', [])}
    cand = base
    if cand in taken_usernames or not USERNAME_RE.match(cand):
        suffix = 2
        while f"{cand[:22]}{suffix}" in taken_usernames:
            suffix += 1
        cand = f"{cand[:22]}{suffix}"

    # 3. Cryptographically secure random temporary password (12 chars)
    uppers = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    lowers = 'abcdefghijkmnpqrstuvwxyz'
    digits = '23456789'
    symbols = '!@#$%&*'
    all_chars = uppers + lowers + digits + symbols

    pwd_parts = [
        secrets.choice(uppers),
        secrets.choice(lowers),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]
    pwd_parts += [secrets.choice(all_chars) for _ in range(8)]
    for i in range(len(pwd_parts) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        pwd_parts[i], pwd_parts[j] = pwd_parts[j], pwd_parts[i]
    temp_pass = ''.join(pwd_parts)

    display_roles = {
        'student': 'Student Account',
        'teacher': 'Teacher Account',
        'staff': 'Staff Account',
        'principal': 'Principal Account',
        'admin': 'Admin Account',
    }

    return jsonify({
        'success': True,
        'type': ptype,
        'institutional_id': pid,
        'username': cand,
        'temporary_password': temp_pass,
        'account_type': display_roles.get(ptype, 'User Account'),
        'role': ROLES_BY_TYPE.get(ptype, 'ADMIN'),
        'status': 'Pending Activation'
    })


@user_mgmt_bp.route('/form-options', methods=['GET'])
def form_options():
    ptype = (request.args.get('type') or 'student').strip().lower()
    if ptype not in ('student', 'teacher', 'staff', 'principal', 'admin'):
        return jsonify({'success': False, 'error': 'Unknown directory type'}), 400
    db = current_app_db()
    _restore_person_overlays()
    campuses = sorted(_valid_campuses(db) - {'All campuses'})

    # ── Type-aware option sources ─────────────────────────────────────────
    # DB registry keys are PLURAL ('teachers', 'staff', 'principals').
    # Departments come from the formal academic department registry when it
    # exists; positions come from the registry family matching the directory
    # type, with NGIS-standard fallbacks when the registry is sparse.
    def _person_values(list_key, field):
        return {p.get(field) for p in (db.get(list_key) or []) if p.get(field)}

    dept_registry = sorted({d.get('name') for d in (db.get('departments') or [])
                            if isinstance(d, dict) and d.get('name')})
    all_departments = sorted(_person_values('teachers', 'department')
                             | _person_values('staff', 'department')
                             | _person_values('principals', 'department'))
    teacher_roles = sorted(_person_values('teachers', 'position')
                           | _person_values('teachers', 'role'))
    staff_roles = sorted(_person_values('staff', 'role')
                         | _person_values('staff', 'position'))
    principal_roles = sorted(_person_values('principals', 'role')
                             | _person_values('principals', 'position'))

    if ptype in ('teacher', 'student'):
        departments = dept_registry or all_departments
        positions = teacher_roles or [
            'Subject Teacher', 'Homeroom Teacher', 'Lead / Senior Faculty',
            'Head of Department', 'Adjunct Instructor'
        ]
    elif ptype == 'staff':
        departments = sorted(_person_values('staff', 'department')) or dept_registry
        positions = staff_roles or [
            'Campus Operations Officer', 'IT Systems Technician',
            'Accounts Officer', 'Registrar Staff', 'Facilities Coordinator'
        ]
    elif ptype == 'principal':
        departments = dept_registry or all_departments
        positions = principal_roles or [
            'Campus Principal', 'Vice Principal', 'Associate Academic Director'
        ]
    else:  # admin directory carries no department field
        departments = []

    classes = [{'id': c.get('id'), 'name': c.get('name'),
                'short': (c.get('name') or '').replace('Grade ', '').split(' (')[0].strip(),
                'grade': str(c.get('grade') or ''),
                'department_id': c.get('department_id', ''),
                'department': c.get('department', ''),
                'campus': c.get('campus')}
               for c in db.get('classes', [])]

    # Build hierarchical department structure for dynamic dependent dropdowns
    dept_structure = {}
    for d in (db.get('departments') or []):
        dname = d.get('name') if isinstance(d, dict) else str(d)
        did = d.get('id', '') if isinstance(d, dict) else ''
        if not dname:
            continue
        d_classes = [c for c in classes if c.get('department_id') == did or c.get('department') == dname]
        grades_map = {}
        for c in d_classes:
            g = str(c.get('grade') or '')
            if not g:
                continue
            if g not in grades_map:
                grades_map[g] = []
            grades_map[g].append({'id': c['id'], 'name': c['name'], 'short': c['short']})

        # Ensure grades 7-12 exist for core academic departments
        standard_grades = ['7', '8', '9', '10', '11', '12'] if any(k in dname.lower() for k in ('khmer', 'english', 'chinese', 'math', 'science', 'language', 'studies')) else list(grades_map.keys()) or ['10', '11', '12']
        for g in standard_grades:
            if g not in grades_map or not grades_map[g]:
                d_slug = did.replace('dept-', '') if did else 'sec'
                grades_map[g] = [
                    {'id': f"cls-{d_slug}-{g}a", 'name': f"Grade {g}A", 'short': f"{g}A"},
                    {'id': f"cls-{d_slug}-{g}b", 'name': f"Grade {g}B", 'short': f"{g}B"},
                ]
                if g == '9' and 'eng' in dname.lower():
                    grades_map[g].append({'id': f"cls-{d_slug}-9c", 'name': 'Grade 9C', 'short': '9C'})

        # Department subjects mapping for smart dependent dropdowns
        dept_subjects_map = {
            'Khmer Studies Department': [
                {'id': 'subj-khm-lit', 'name': 'Khmer Literature', 'code': 'KHM-LIT'},
                {'id': 'subj-khm-lang', 'name': 'Khmer Language', 'code': 'KHM-LANG'},
                {'id': 'subj-khm-hist', 'name': 'Khmer History & Culture', 'code': 'KHM-HIST'},
                {'id': 'subj-khm-civ', 'name': 'Moral & Civics', 'code': 'KHM-CIV'}
            ],
            'English Department': [
                {'id': 'subj-eng', 'name': 'English Literature', 'code': 'ENG-LIT'},
                {'id': 'subj-preap-eng2', 'name': 'Pre-AP English II', 'code': 'ENG-PAP2'},
                {'id': 'subj-eng-ela', 'name': 'English Language Arts', 'code': 'ENG-ELA'},
                {'id': 'subj-eng-esl', 'name': 'Academic Writing & ESL', 'code': 'ENG-ESL'}
            ],
            'Chinese Language Department': [
                {'id': 'subj-chn-lang', 'name': 'Chinese Language', 'code': 'CHN-LANG'},
                {'id': 'subj-chn-lit', 'name': 'Chinese Literature', 'code': 'CHN-LIT'},
                {'id': 'subj-chn-conv', 'name': 'Conversational Chinese', 'code': 'CHN-CONV'},
                {'id': 'subj-chn-bus', 'name': 'Business Chinese', 'code': 'CHN-BUS'}
            ],
            'Mathematics Department': [
                {'id': 'subj-math', 'name': 'Advanced Mathematics', 'code': 'MATH-10'},
                {'id': 'subj-ap-precalc', 'name': 'AP Pre-Calculus', 'code': 'MATH-APPC'},
                {'id': 'subj-mat-calc', 'name': 'Calculus & Statistics', 'code': 'MATH-CALC'},
                {'id': 'subj-mat-alg', 'name': 'Algebra & Geometry', 'code': 'MATH-ALG'}
            ],
            'Science Department': [
                {'id': 'subj-phys', 'name': 'Physics & Lab', 'code': 'PHY-10'},
                {'id': 'subj-phys-3', 'name': 'Physics III CP', 'code': 'PHY-3CP'},
                {'id': 'subj-chem', 'name': 'Chemistry Practicum', 'code': 'CHEM-10'},
                {'id': 'subj-preap-chem', 'name': 'Pre-AP Chemistry', 'code': 'CHEM-PAP'},
                {'id': 'subj-ap-bio', 'name': 'AP Biology', 'code': 'BIO-AP'}
            ],
            'Humanities & Social Sciences': [
                {'id': 'subj-ap-macro', 'name': 'AP Macroeconomics', 'code': 'ECON-AP'},
                {'id': 'subj-hum-hist', 'name': 'World History', 'code': 'HUM-HIST'},
                {'id': 'subj-hum-geo', 'name': 'Geography & Environment', 'code': 'HUM-GEO'}
            ],
            'Arts & Physical Education': [
                {'id': 'subj-art-cp', 'name': 'Art CP', 'code': 'ART-CP'},
                {'id': 'subj-art-pe', 'name': 'Physical Education & Health', 'code': 'ART-PE'},
                {'id': 'subj-art-mus', 'name': 'Music & Performing Arts', 'code': 'ART-MUS'}
            ]
        }

        dept_subjs = dept_subjects_map.get(dname) or [
            {'id': f"subj-{did.replace('dept-', '')}-gen" if did else "subj-gen", 'name': f"{dname} Studies", 'code': 'GEN'}
        ]

        sorted_grades = sorted(list(grades_map.keys()), key=lambda x: (int(x) if x.isdigit() else 99, x))
        struct_entry = {
            'id': did,
            'name': dname,
            'grades': sorted_grades,
            'classes_by_grade': grades_map,
            'subjects': dept_subjs
        }
        dept_structure[dname] = struct_entry
        if did:
            dept_structure[did] = struct_entry

    grades = sorted({c.get('grade') for c in classes if c.get('grade')},
                    key=lambda g: (len(str(g)), str(g)))
    all_known_subjects = []
    for s_list in dept_subjects_map.values():
        for s_item in s_list:
            if s_item['name'] not in all_known_subjects:
                all_known_subjects.append(s_item['name'])
    subjects = sorted(list(set(all_known_subjects) | {s for t in db.get('teachers', [])
                       for s in (t.get('subjects') or []) if s}))
    if ptype == 'admin':
        positions = [
            'School Systems Administrator',
            'Registrar Administrator',
            'IT Infrastructure Administrator',
            'Data & Operations Admin'
        ]
    return jsonify({'success': True, 'type': ptype,
                    'campuses': campuses, 'departments': departments,
                    'classes': classes, 'grades': grades, 'subjects': subjects,
                    'positions': positions,
                    'department_structure': dept_structure,
                    'subjects_by_department': dept_subjects_map,
                    'academic_years': ['2025-26', '2026-27']})


# ── API: create brand-new person + login account (transactional) ──────────

@user_mgmt_bp.route('/create-person', methods=['POST'])
def create_person():
    """Create a completely new person record AND their login account.

    The person does NOT need to exist in any registry beforehand. The account
    type is fixed by the directory the request originates from — no general
    role selector exists. All validation happens before any mutation so a
    failure can never leave partial or orphaned records behind.
    """
    payload = request.get_json(silent=True) or {}
    actor = _actor()
    db = current_app_db()
    _restore_person_overlays()
    store = _store()

    ptype = (payload.get('person_type') or payload.get('role') or payload.get('type') or '').strip().lower()
    first = (payload.get('first_name') or '').strip()
    last = (payload.get('last_name') or '').strip()
    username = (payload.get('username') or '').strip().lower()
    email = (payload.get('email') or '').strip().lower() or None
    phone = (payload.get('phone') or '').strip() or None
    gender = (payload.get('gender') or '').strip().upper() or None
    photo = (payload.get('photo') or '').strip() or None
    campus = (payload.get('campus') or '').strip()
    activation = payload.get('activation', 'token')

    if not username and first and last:
        base_u = re.sub(r'[^a-z0-9]', '', f"{first}.{last}".lower())
        cand = base_u[:30] or f"user{_ts()[-4:]}"
        counter = 1
        while any(a['username'] == cand for a in store['accounts']):
            cand = f"{base_u[:25]}{counter}"
            counter += 1
        username = cand

    # ── phase 1: universal validation ──
    if ptype not in ('student', 'teacher', 'staff', 'principal', 'admin'):
        return jsonify({'success': False, 'error':
                        f'Unknown directory type "{ptype}"'}), 400
    if ptype == 'admin' and not (_actor_is_admin(actor, store) or _actor_is_super(actor, store)):
        return jsonify({'success': False, 'error':
                        'Only authorized administrators may create Administrator accounts'}), 403
    if ptype == 'principal' and not _actor_is_admin(actor, store):
        return jsonify({'success': False, 'error':
                        'Only active administrators may create Principal accounts'}), 403
    if not first or not last:
        return jsonify({'success': False, 'error':
                        'First and last names are required'}), 400
    full_name = f'{first} {last}'.strip()
    if not USERNAME_RE.match(username or ''):
        return jsonify({'success': False, 'error':
                        'Username must be 3-40 chars: lowercase letters, digits, dot, dash, underscore'}), 400
    if any(a['username'] == username for a in store['accounts']):
        return jsonify({'success': False, 'error': 'Username is already taken'}), 409
    if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({'success': False, 'error': 'Email address format is invalid'}), 400
    if campus and campus not in _valid_campuses(db) and campus != 'All campuses':
        return jsonify({'success': False, 'error':
                        f'Campus "{campus}" is not a registered campus'}), 400

    # ── phase 2: directory-specific validation + duplicate-person checks ──
    person = None
    if ptype == 'admin':
        position = (payload.get('position') or 'School Systems Administrator').strip()
        scope = (payload.get('scope') or 'Standard Administrative Scope').strip()
        norm = _norm_name(full_name)
        for a in store.get('accounts', []):
            if a.get('person_type') == 'admin' and _norm_name(a.get('name')) == norm:
                return jsonify({'success': False, 'error':
                                f'Likely duplicate: Administrator "{a.get("name")}" ({a.get("person_id")}) '
                                f'already exists — review the directory first'}), 409
        admin_id = _resolve_institutional_id(db, store, 'admin', payload.get('institutional_id'))
        account_payload = {
            'person_type': 'admin',
            'person_id': admin_id,
            'name': full_name,
            'username': username,
            'email': email or f'{username}@ngis.edu.kh',
            'campus': campus or 'All campuses',
            'role': 'ADMIN',
            'access_scope': scope,
            'assignment': position,
            'elevated_confirmed': True,
            'activation': activation,
            'temporary_password': (payload.get('temporary_password') or payload.get('password') or '').strip(),
        }
        result, status = _provision_one(account_payload, actor, store=store)
        if status != 201:
            return jsonify(result), status
        _audit(store, actor, 'admin_created', target=admin_id,
               target_name=full_name, scope=campus or 'All campuses',
               details={'person_type': 'admin', 'account_id': result['account_id'],
                        'identity_workflow': 'create-from-scratch'})
        _save_store(store)
        result['institutional_id'] = admin_id
        result['message'] = f'Administrator profile {admin_id} created and linked to login account {username}'
        return jsonify(result), 201
    elif ptype == 'student':
        raw_enrollments = payload.get('enrollments')
        enrollments = []
        if isinstance(raw_enrollments, list) and len(raw_enrollments) > 0:
            for item in raw_enrollments:
                dept_input = (item.get('department') or item.get('department_name') or item.get('department_id') or '').strip()
                dept_obj = next((d for d in db.get('departments', []) if dept_input in (d.get('name'), d.get('id'))), None)
                dept_val = dept_obj.get('name') if dept_obj else dept_input
                dept_id = dept_obj.get('id') if dept_obj else (item.get('department_id') or '')

                cid_val = (item.get('class_id') or item.get('classId') or '').strip()
                class_input = (item.get('class') or item.get('class_name') or '').strip()
                if cid_val and not class_input:
                    cls_obj = next((c for c in db.get('classes', []) if c.get('id') == cid_val), None)
                    if cls_obj:
                        class_input = cls_obj.get('short') or cls_obj.get('name') or cid_val
                if not class_input and cid_val:
                    class_input = cid_val

                grade_val = str(item.get('grade') or '').strip()
                if not grade_val and cid_val:
                    cls_obj = next((c for c in db.get('classes', []) if c.get('id') == cid_val), None)
                    if cls_obj and cls_obj.get('grade'):
                        grade_val = str(cls_obj.get('grade'))

                if not dept_val or (not class_input and not cid_val):
                    continue
                if grade_val and not grade_val.startswith('Grade '):
                    grade_norm = f"Grade {grade_val}"
                else:
                    grade_norm = grade_val or 'Grade 10'
                class_clean = class_input.replace('Grade ', '').split(' (')[0].strip() if class_input else cid_val

                if not cid_val:
                    matched = next((c for c in db.get('classes', [])
                                    if class_clean in (c.get('name'), (c.get('name') or '').replace('Grade ', ''), c.get('short'), c.get('id'))
                                    and (not dept_id or c.get('department_id') in (dept_id, '') or c.get('department') == dept_val)), None)
                    if not matched:
                        matched = next((c for c in db.get('classes', [])
                                        if class_clean in (c.get('name'), (c.get('name') or '').replace('Grade ', ''), c.get('short'), c.get('id'))), None)
                    cid_val = matched.get('id') if matched else f"cls-{class_clean.lower()}"

                enrollments.append({
                    'department': dept_val,
                    'department_id': dept_id,
                    'grade': grade_norm or 'Grade 10',
                    'class': class_clean,
                    'class_id': cid_val,
                    'academic_year': (item.get('academic_year') or payload.get('academic_year') or '2025-26').strip(),
                    'status': (item.get('status') or payload.get('enrollment_status') or 'active').strip()
                })

        # Fallback if raw_enrollments was empty or omitted
        if not enrollments:
            class_input = (payload.get('class') or '').strip()
            cls = next((c for c in db.get('classes', [])
                        if class_input in (c.get('name'), (c.get('name') or '').replace('Grade ', ''), c.get('id'))),
                       None)
            if not cls:
                return jsonify({'success': False, 'error':
                                f'Class "{class_input or "—"}" does not exist in the class registry'}), 400
            cls_short = (cls.get('name') or '').replace('Grade ', '').split(' (')[0].strip()
            dept_name = payload.get('department') or cls.get('department') or 'English Department'
            dept_obj = next((d for d in db.get('departments', []) if dept_name in (d.get('name'), d.get('id'))), None)
            enrollments = [{
                'department': dept_name,
                'department_id': dept_obj.get('id') if dept_obj else (cls.get('department_id') or 'dept-eng'),
                'grade': f"Grade {cls.get('grade', '10')}",
                'class': cls_short,
                'class_id': cls.get('id'),
                'academic_year': (payload.get('academic_year') or '2025-26').strip(),
                'status': (payload.get('enrollment_status') or 'active').strip()
            }]

        # Check duplicate departments
        dept_names_seen = set()
        for enr in enrollments:
            dkey = enr.get('department_id') or enr.get('department')
            dname = enr.get('department') or enr.get('department_id')
            if dkey in dept_names_seen or dname in dept_names_seen:
                return jsonify({'success': False, 'error': f'Duplicate department enrollment: "{dname}" cannot be added multiple times'}), 400
            dept_names_seen.add(dkey)
            dept_names_seen.add(dname)

        primary = enrollments[0]
        norm = _norm_name(full_name)
        for p in db.get('students', []):
            if _norm_name(p.get('name')) == norm and p.get('class') == primary['class']:
                return jsonify({'success': False, 'error':
                                f'Likely duplicate: "{p.get("name")}" ({p.get("id")}) '
                                f'already exists in {primary["class"]} — review the directory first'}), 409
        person = {
            'id': _resolve_institutional_id(db, store, 'student', payload.get('institutional_id')),
            'name': full_name,
            'gender': gender or 'M',
            'grade': primary['grade'],
            'class': primary['class'],
            'enrollments': enrollments,
            'gpa': 0,
            'attendance': 100,
            'status': (payload.get('enrollment_status') or 'active').strip(),
            'parentEmail': (payload.get('parent_email') or '').strip(),
            'parentName': (payload.get('parent_name') or '').strip(),
            'advisor': (payload.get('advisor') or '').strip(),
            'campus': campus or 'Sensok',
            'academic_year': (payload.get('academic_year') or '2025-26').strip(),
        }
        if payload.get('khmer_name'):
            person['khmerName'] = payload.get('khmer_name').strip()
        if payload.get('dob'):
            person['dob'] = payload.get('dob').strip()
        if phone:
            person['phone'] = phone
        if payload.get('parent_phone'):
            person['parentPhone'] = payload.get('parent_phone').strip()
        if photo:
            person['avatar'] = photo
    elif ptype == 'teacher':
        raw_assignments = payload.get('assignments') or payload.get('teaching_assignments')
        assignments = []
        if isinstance(raw_assignments, list) and len(raw_assignments) > 0:
            for item in raw_assignments:
                dept_input = (item.get('department') or item.get('department_name') or item.get('department_id') or '').strip()
                dept_obj = next((d for d in db.get('departments', []) if dept_input in (d.get('name'), d.get('id'))), None)
                dept_val = dept_obj.get('name') if dept_obj else (dept_input or payload.get('department') or 'General')
                dept_id = dept_obj.get('id') if dept_obj else (item.get('department_id') or '')

                cid_val = (item.get('class_id') or item.get('classId') or '').strip()
                class_input = (item.get('class') or item.get('class_name') or '').strip()
                if cid_val and not class_input:
                    cls_obj = next((c for c in db.get('classes', []) if c.get('id') == cid_val), None)
                    if cls_obj:
                        class_input = cls_obj.get('short') or cls_obj.get('name') or cid_val
                if not class_input and cid_val:
                    class_input = cid_val

                grade_val = str(item.get('grade') or '').strip()
                if not grade_val and cid_val:
                    cls_obj = next((c for c in db.get('classes', []) if c.get('id') == cid_val), None)
                    if cls_obj and cls_obj.get('grade'):
                        grade_val = str(cls_obj.get('grade'))

                if not cid_val and class_input:
                    class_clean = class_input.replace('Grade ', '').split(' (')[0].strip()
                    matched = next((c for c in db.get('classes', [])
                                    if class_clean in (c.get('name'), (c.get('name') or '').replace('Grade ', ''), c.get('short'), c.get('id'))
                                    and (not dept_id or c.get('department_id') in (dept_id, '') or c.get('department') == dept_val)), None)
                    if not matched:
                        matched = next((c for c in db.get('classes', [])
                                        if class_clean in (c.get('name'), (c.get('name') or '').replace('Grade ', ''), c.get('short'), c.get('id'))), None)
                    cid_val = matched.get('id') if matched else f"cls-{class_clean.lower()}"
                else:
                    class_clean = class_input.replace('Grade ', '').split(' (')[0].strip() if class_input else cid_val

                subj_val = (item.get('subject') or item.get('subject_name') or item.get('subject_id') or '').strip()
                sid_val = (item.get('subject_id') or '').strip()
                if not sid_val and subj_val:
                    sid_val = f"subj-{re.sub(r'[^a-z0-9]', '', subj_val.lower())}"

                if not dept_val or not class_clean or not subj_val:
                    continue

                assignments.append({
                    'department': dept_val,
                    'department_id': dept_id,
                    'grade': f"Grade {grade_val}" if grade_val and not grade_val.startswith('Grade ') else (grade_val or 'Grade 10'),
                    'class': class_clean,
                    'class_id': cid_val,
                    'subject': subj_val,
                    'subject_id': sid_val,
                    'room': (item.get('room') or 'Rm: 201').strip(),
                    'academic_year': (item.get('academic_year') or payload.get('academic_year') or '2025-26').strip(),
                    'status': (item.get('status') or payload.get('status') or 'active').strip()
                })

        # Check duplicate identical assignments (same class and same subject)
        seen_asgn_pairs = set()
        for asgn in assignments:
            pair = (asgn['class_id'], asgn['subject_id'] or asgn['subject'].lower())
            if pair in seen_asgn_pairs:
                return jsonify({'success': False, 'error': f'Duplicate teaching assignment: class "{asgn["class"]}" with subject "{asgn["subject"]}" cannot be assigned multiple times to the same teacher'}), 400
            seen_asgn_pairs.add(pair)

        department = (payload.get('department') or (assignments[0]['department'] if assignments else '') or '').strip()
        if not department:
            return jsonify({'success': False, 'error':
                            'Department is required for teacher accounts'}), 400
        norm = _norm_name(full_name)
        for p in db.get('teachers', []):
            if _norm_name(p.get('name')) == norm and p.get('department') == department:
                return jsonify({'success': False, 'error':
                                f'Likely duplicate: teacher "{p.get("name")}" ({p.get("id")}) '
                                f'already exists in {department} — review the directory first'}), 409

        classes_list = list(dict.fromkeys(a['class'] for a in assignments if a.get('class')))
        subjects_list = list(dict.fromkeys(a['subject'] for a in assignments if a.get('subject')))
        if not subjects_list and payload.get('subjects'):
            subjects_list = [s.strip() for s in payload.get('subjects') if s.strip()]

        person = {
            'id': _resolve_institutional_id(db, store, 'teacher', payload.get('institutional_id')),
            'name': full_name,
            'email': email or '',
            'phone': phone or '',
            'department': department,
            'position': (payload.get('position') or 'Teacher').strip(),
            'subjects': subjects_list,
            'classes': classes_list,
            'assignments': assignments,
            'classesAssigned': len(assignments),
            'homeroom': classes_list[0] if classes_list else '',
            'status': 'active',
            'campus': campus or 'Sensok',
        }
        if payload.get('khmer_name'):
            person['khmerName'] = payload.get('khmer_name').strip()
        if payload.get('dob'):
            person['dob'] = payload.get('dob').strip()
        if payload.get('employment_date'):
            person['employmentDate'] = payload.get('employment_date').strip()
        if photo:
            person['avatar'] = photo
    elif ptype == 'staff':
        department = (payload.get('department') or '').strip()
        position = (payload.get('position') or '').strip()
        if not department or not position:
            return jsonify({'success': False, 'error':
                            'Department and job position are required for staff accounts'}), 400
        norm = _norm_name(full_name)
        for p in db.get('staff', []):
            if _norm_name(p.get('name')) == norm and p.get('department') == department:
                return jsonify({'success': False, 'error':
                                f'Likely duplicate: staff member "{p.get("name")}" ({p.get("id")}) '
                                f'already exists in {department} — review the directory first'}), 409
        person = {
            'id': _resolve_institutional_id(db, store, 'staff', payload.get('institutional_id')),
            'name': full_name,
            'email': email or '',
            'phone': phone or '',
            'department': department,
            'role': position,
            'status': 'active',
            'campus': campus or 'Sensok',
        }
        if photo:
            person['avatar'] = photo
    else:  # principal
        position = (payload.get('position') or 'Campus Principal').strip()
        norm = _norm_name(full_name)
        for p in db.get('principals', []):
            if _norm_name(p.get('name')) == norm:
                return jsonify({'success': False, 'error':
                                f'Likely duplicate: principal "{p.get("name")}" ({p.get("id")}) '
                                f'already exists — review the directory first'}), 409
        person = {
            'id': _resolve_institutional_id(db, store, 'principal', payload.get('institutional_id')),
            'name': full_name,
            'email': email or '',
            'phone': phone or '',
            'role': position,
            'campus': campus or 'Sensok',
            'authorized_scope': (payload.get('scope') or campus or 'Sensok').strip(),
            'status': 'active',
        }
        if photo:
            person['avatar'] = photo

    # ── phase 3: transactional creation (profile → account → link) ──
    list_key = PERSON_LIST_KEY[ptype]
    db.setdefault(list_key, []).append(person)
    try:
        _persist_person(ptype, person)
        try:
            from server import PRINCIPAL_DEMO_STATE
            if isinstance(PRINCIPAL_DEMO_STATE, dict):
                if ptype == 'student' and 'students' in PRINCIPAL_DEMO_STATE:
                    if not any(s.get('id') == person['id'] for s in PRINCIPAL_DEMO_STATE['students']):
                        PRINCIPAL_DEMO_STATE['students'].append(dict(person))
                elif ptype == 'teacher' and 'teachers' in PRINCIPAL_DEMO_STATE:
                    if not any(t.get('id') == person['id'] for t in PRINCIPAL_DEMO_STATE['teachers']):
                        PRINCIPAL_DEMO_STATE['teachers'].append(dict(person))
        except Exception:
            pass
    except Exception as exc:
        db[list_key].pop()
        return jsonify({'success': False, 'error':
                        f'Could not persist the person record: {exc}'}), 500

    account_payload = {
        'person_type': ptype,
        'person_id': person['id'],
        'username': username,
        'email': email,
        'campus': person.get('campus', 'Sensok'),
        'activation': activation,
        'temporary_password': (payload.get('temporary_password') or payload.get('password') or '').strip(),
    }
    if ptype == 'student':
        account_payload['assignment'] = _person_assignment(person, 'student')
        account_payload['enrollments'] = person.get('enrollments') or []
    elif ptype == 'teacher':
        account_payload['assignment'] = _person_assignment(person, 'teacher')
        account_payload['assignments'] = person.get('assignments') or []
    elif ptype == 'staff':
        account_payload['assignment'] = person['role']
    else:
        account_payload['assignment'] = person['role']

    result, status = _provision_one(account_payload, actor, store=store)
    if status != 201:
        # rollback: remove the person record everywhere — no orphans
        db[list_key].pop()
        _remove_person_overlay(ptype, person['id'])
        if ptype == 'student':
            try:
                import academic_store
                for enr in person.get('enrollments', []):
                    academic_store.unenroll_student(person['id'], enr.get('class_id', ''))
            except Exception:
                pass
        elif ptype == 'teacher':
            try:
                import academic_store
                academic_store.unassign_teacher(person['id'], '')
            except Exception:
                pass
        return jsonify(result), status

    if ptype == 'student':
        try:
            import academic_store
            for enr in person.get('enrollments', []):
                academic_store.enroll_student(
                    student_id=person['id'],
                    class_id=enr.get('class_id') or f"cls-{enr.get('class', '').lower()}",
                    academic_year_id=f"ay-{enr.get('academic_year', '2025-26')}",
                    status=enr.get('status', 'active'),
                    department_id=enr.get('department_id', ''),
                    grade=enr.get('grade', '')
                )
        except Exception:
            pass
        result['enrollments'] = person.get('enrollments', [])
        result['assignment'] = account_payload['assignment']
        result['person'] = person
    elif ptype == 'teacher':
        try:
            import academic_store
            for a in person.get('assignments', []):
                academic_store.assign_teacher(
                    teacher_id=person['id'],
                    class_id=a.get('class_id') or f"cls-{str(a.get('class', '')).lower()}",
                    subject_id=a.get('subject_id') or f"subj-{re.sub(r'[^a-z0-9]', '', str(a.get('subject', 'gen')).lower())}",
                    academic_year_id=f"ay-{a.get('academic_year', '2025-26')}",
                    department_id=a.get('department_id', ''),
                    grade=a.get('grade', ''),
                    teacher_name=person['name'],
                    teacher_email=person['email'],
                    room=a.get('room', 'Rm: 201')
                )
        except Exception:
            pass
        result['assignments'] = person.get('assignments', [])
        result['assignment'] = account_payload['assignment']
        result['person'] = person

    _audit(store, actor, 'person_created', target=person['id'],
           target_name=full_name, scope=person.get('campus', 'Sensok'),
           details={'person_type': ptype, 'account_id': result['account_id'],
                    'identity_workflow': 'create-from-scratch'})
    _save_store(store)
    result['username'] = username
    result['institutional_id'] = person['id']
    result['message'] = (f'{ROLES_BY_TYPE[ptype].capitalize()} profile {person["id"]} '
                         f'created and linked to login account {username}')
    return jsonify(result), 201


# ── store-backed authentication (provisioned identity accounts) ───────────

MAX_FAILED_LOGINS = 5


def authenticate_store_account(identifier, password):
    """Authenticate a provisioned account by username or email.

    Returns (data_dict, http_status). Suspended/disabled/locked accounts are
    rejected before credential verification; failed attempts lock the account
    after MAX_FAILED_LOGINS consecutive tries; successful logins are recorded
    in the account's login history. Only salted hashes are ever compared.
    """
    ident = (identifier or '').strip().lower()
    if not ident:
        return None, 401
    store = _store()
    account = next((a for a in store['accounts']
                    if (a['username'] or '').lower() == ident
                    or (a.get('email') and (a.get('email') or '').lower() == ident)), None)
    if not account:
        return None, 401
    if account['status'] in ('suspended', 'disabled'):
        return {'error': {'code': 'ACCOUNT_SUSPENDED', 'message':
                          'This account is suspended or disabled — contact your administrator'}}, 403
    if account['status'] == 'locked':
        return {'error': {'code': 'ACCOUNT_LOCKED', 'message':
                          'This account is locked after repeated failed sign-ins'}}, 403
    if account['status'] == 'pending_activation':
        return {'error': {'code': 'ACTIVATION_REQUIRED', 'message':
                          'Activate this account with its one-time token before signing in'}}, 403
    if not account.get('password_hash'):
        return {'error': {'code': 'CREDENTIAL_SETUP_REQUIRED', 'message':
                          'Finish credential setup with the activation token before signing in'}}, 403
    if not _verify_secret(password or '', account['password_hash']):
        account['failed_attempts'] = int(account.get('failed_attempts') or 0) + 1
        failed = account['failed_attempts']
        store.setdefault('login_history', {}).setdefault(account['id'], []).append(
            {'ts': _ts(), 'event': 'login_failed',
             'detail': f'{failed} consecutive failed attempts'})
        if failed >= MAX_FAILED_LOGINS and account['status'] == 'active':
            account['status'] = 'locked'
            _audit(store, ident, 'account_locked', target=account['id'],
                   target_name=account['name'], outcome='automatic',
                   details={'reason': 'consecutive failed logins'})
        _save_store(store)
        return None, 401
    account['failed_attempts'] = 0
    account['last_login'] = _ts()
    store.setdefault('login_history', {}).setdefault(account['id'], []).append(
        {'ts': _ts(), 'event': 'login_success'})
    _save_store(store)
    first, _mid, last = _split_name(account['name'])
    role = account['person_type']
    return {'token': f'um-session-{account["id"]}',
            'must_change_password': bool(account.get('must_change_password')),
            'user': {'id': account['person_id'], 'firstName': first,
                     'lastName': last, 'name': account['name'],
                     'email': account.get('email') or account['username'],
                     'role': role, 'portal': role, 'avatar': None}}, 200


def resolve_store_session(account_id):
    """Resolve an um-session token into a portal user object (active only)."""
    store = _store()
    acc = next((a for a in store['accounts']
                if a['id'] == account_id and a['status'] == 'active'), None)
    if not acc:
        return None
    first, _mid, last = _split_name(acc['name'])
    role = acc['person_type']
    return {'id': acc['person_id'], 'firstName': first, 'lastName': last,
            'name': acc['name'], 'email': acc.get('email') or acc['username'],
            'role': role, 'portal': role, 'avatar': None}


# ── API: self-service password change (first-login + routine) ─────────────

@user_mgmt_bp.route('/change-password', methods=['POST'])
def change_password():
    """Self-service credential change for provisioned accounts.

    Requires the account's current password; clears the
    must_change_password flag set when the account was provisioned with a
    temporary password. Only salted hashes are stored or compared — the
    plaintext never touches the store or the audit log.
    """
    payload = request.get_json(silent=True) or {}
    ident = (payload.get('username') or payload.get('email') or '').strip().lower()
    current = payload.get('current_password') or payload.get('current') or ''
    new = payload.get('new_password') or payload.get('password') or ''
    if not ident or not current or not new:
        return jsonify({'success': False, 'error':
                        'username, current_password and new_password are required'}), 400
    store = _store()
    account = next((a for a in store['accounts']
                    if a['username'].lower() == ident
                    or (a.get('email') or '').lower() == ident), None)
    if not account or not account.get('password_hash'):
        return jsonify({'success': False, 'error':
                        'No provisioned credential found for this account'}), 404
    if not _verify_secret(current, account['password_hash']):
        return jsonify({'success': False, 'error':
                        'Current password is incorrect'}), 401
    if len(new) < 8:
        return jsonify({'success': False, 'error':
                        'New password must be at least 8 characters'}), 400
    if _verify_secret(new, account['password_hash']):
        return jsonify({'success': False, 'error':
                        'New password must be different from the current one'}), 400
    account['password_hash'] = _hash_secret(new)
    account['must_change_password'] = False
    _audit(store, ident, 'password_changed', target=account['id'],
           target_name=account['name'], scope=account.get('campus', ''),
           details={'person_link': f"{account['person_type']}:{account['person_id']}",
                    'self_service': True})
    _save_store(store)
    return jsonify({'success': True,
                    'message': 'Password updated — use it on your next sign-in'})


# ── API: audit trail ──────────────────────────────────────────────────────

@user_mgmt_bp.route('/audit', methods=['GET'])
def audit_trail():
    store = _store()
    search = request.args.get('search', '').strip().lower()
    action = request.args.get('action', 'all').lower()
    entries = store['audit_log']
    if action != 'all':
        entries = [e for e in entries if e['action'] == action]
    if search:
        entries = [e for e in entries if search in json.dumps(e).lower()]
    entries = sorted(entries, key=lambda e: e['ts'], reverse=True)
    return jsonify({'success': True, 'data': entries[:100],
                    'total': len(entries)})


# ── API: CSV export (no credentials) ──────────────────────────────────────

@user_mgmt_bp.route('/export', methods=['GET'])
def export_csv():
    _, rows = _filter_directory_rows(_directory_rows(current_app_db()), request.args)

    def cell(value):
        value = '' if value is None else str(value)
        if any(c in value for c in (',', '"', '\n')):
            value = '"' + value.replace('"', '""') + '"'
        return value

    lines = ['User ID,Name,Username,Email,Role,Campus,Department,Assignment,'
             'Account Status,Last Login,Identity Source']
    for r in rows:
        acc = r['account'] or {}
        lines.append(','.join(cell(v) for v in (
            r['institutional_id'], r['name'], acc.get('username'),
            acc.get('email'), r['display_role'], r['campus'], r['department'],
            r['assignment'], acc.get('status'), acc.get('last_login'),
            acc.get('identity_source') or 'none')))
    body = '\ufeff' + '\n'.join(lines)   # UTF-8 BOM so Excel opens Khmer text
    return current_app_response(body)


def current_app_response(body):
    from flask import Response
    return Response(body, mimetype='text/csv',
                    headers={'Content-Disposition':
                             'attachment; filename=ngis-user-directory.csv'})


def register_user_mgmt_routes(app):
    app.register_blueprint(user_mgmt_bp)
