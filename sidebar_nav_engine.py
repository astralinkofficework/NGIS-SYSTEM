"""
NGIS Global Sidebar Manager — Navigation Configuration Engine

Central store and controlled workflow (edit → validate → publish → rollback)
for every portal sidebar in NGIS-SYSTEM. Backed by a single JSON store so the
portal sidebars have exactly one source of truth.

Schema (per portal):
  portal -> {
     brand, meta, status,
     last_published, published_by,
     groups: [ { id, label, icon, links: [ item ] } ],
     draft?: { brand, meta, groups: [...] }   # present only when a draft exists
  }

Navigation item:
  { id, label, subtitle?, icon?, href, badge?, hasChevron?,
    visible?, locked?, roles?: [...], scope?: [campus ids],
    collapsible?: bool, children?: [ item ] }
"""

import os
import json
import uuid
import copy
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
NAV_FILE = os.path.join(DATA_DIR, 'sidebar_nav.json')
NAV_VERSIONS_FILE = os.path.join(DATA_DIR, 'sidebar_nav_versions.json')
NAV_AUDIT_FILE = os.path.join(DATA_DIR, 'sidebar_nav_audit.json')

PORTALS = ['admin', 'principal', 'teacher', 'student']
PORTAL_LABELS = {
    'admin': 'Admin Sidebar',
    'principal': 'Principal Sidebar',
    'teacher': 'Teacher Sidebar',
    'student': 'Student Sidebar',
}
PORTAL_OWNERS = {
    'admin': 'admin',
    'principal': 'principal',
    'teacher': 'teacher',
    'student': 'student',
}
MAX_VERSIONS = 60


# ── IO helpers (atomic, mirroring the CMS engine) ──
def _load_json(filepath, default):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Nav Engine] Error reading {filepath}: {e}")
        return default


def _save_json(filepath, data):
    tmp_path = filepath + f".tmp_{uuid.uuid4().hex[:6]}"
    try:
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, filepath)
        return True
    except Exception as e:
        print(f"[Nav Engine] Error saving {filepath}: {e}")
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        return False


def _now():
    return datetime.now().isoformat() + "Z"


def _actor_email(actor):
    return actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor)


def _actor_name(actor):
    return actor.get('name', 'Admin') if isinstance(actor, dict) else 'Admin'


def _actor_role(actor):
    if isinstance(actor, dict):
        return actor.get('role', 'admin')
    return 'admin'


def _ensure_seeded():
    """Loads the store, seeding defaults on first run so nothing is lost."""
    data = _load_json(NAV_FILE, None)
    if not data or 'portals' not in data:
        data = {"version": 1, "last_updated": _now(), "updated_by": "system", "portals": {}}
    if 'defaults' not in data:
        data['defaults'] = copy.deepcopy(data.get('portals', {}))
        _save_json(NAV_FILE, data)
    return data


def get_nav_data():
    return _ensure_seeded()


def _published_view(portal_cfg):
    """Strips draft-only metadata to expose the live published navigation."""
    return {
        "brand": portal_cfg.get('brand', ''),
        "meta": portal_cfg.get('meta', ''),
        "groups": copy.deepcopy(portal_cfg.get('groups', [])),
    }


def get_published(portal):
    """Returns the live published navigation for one portal."""
    data = get_nav_data()
    cfg = data.get('portals', {}).get(portal)
    if not cfg:
        return None
    return _published_view(cfg)


def get_all_published():
    """Returns { portal: published nav } for every configured portal (layout.js)."""
    data = get_nav_data()
    return {p: _published_view(c) for p, c in data.get('portals', {}).items()}


def get_portal_state(portal):
    """Returns published + draft + metadata for the manager UI."""
    data = get_nav_data()
    cfg = data.get('portals', {}).get(portal)
    if not cfg:
        return None
    return {
        "portal": portal,
        "label": PORTAL_LABELS.get(portal, portal.title()),
        "brand": cfg.get('brand', ''),
        "meta": cfg.get('meta', ''),
        "status": 'draft' if cfg.get('draft') else cfg.get('status', 'published'),
        "last_published": cfg.get('last_published'),
        "published_by": cfg.get('published_by'),
        "draft_updated_at": cfg.get('draft_updated_at'),
        "draft_updated_by": cfg.get('draft_updated_by'),
        "published": _published_view(cfg),
        "draft": copy.deepcopy(cfg.get('draft')) if cfg.get('draft') else None,
    }


def get_portals_overview():
    """Lightweight list for the portal selector."""
    data = get_nav_data()
    out = []
    for p in PORTALS:
        cfg = data.get('portals', {}).get(p)
        if not cfg:
            continue
        out.append({
            "portal": p,
            "label": PORTAL_LABELS.get(p, p.title()),
            "brand": cfg.get('brand', ''),
            "status": 'draft' if cfg.get('draft') else cfg.get('status', 'published'),
            "item_count": _count_items(cfg.get('groups', [])),
        })
    return out


def _count_items(groups):
    total = 0
    for g in groups or []:
        for l in g.get('links', []):
            total += _count_item(l)
    return total


def _count_item(item):
    n = 1
    for c in item.get('children', []) or []:
        n += _count_item(c)
    return n


# ── Validation (real checks, no invented scores) ──
def _route_registered(href):
    """A route is 'registered' when its target file exists in the project."""
    if not href:
        return False
    path = href.split('?')[0].split('#')[0].strip()
    if not path or path.startswith('http://') or path.startswith('https://'):
        return True  # external links are permitted and not part of the file registry
    fs_path = os.path.join(BASE_DIR, path.replace('/', os.sep))
    return os.path.exists(fs_path)


def _collect_items(groups, parent_id=None):
    """Yields (item, parent_id, depth, group_id)."""
    for g in groups or []:
        for l in g.get('links', []):
            yield from _walk(l, g.get('id'), 1)
    yield from ()


def _walk(item, parent_id, depth):
    yield (item, parent_id, depth)
    for c in item.get('children', []) or []:
        yield from _walk(c, item.get('id'), depth + 1)


def validate(portal, nav):
    """Returns a list of real findings for a navigation payload."""
    findings = []
    if portal not in PORTALS:
        findings.append({"severity": "high", "code": "unknown_portal",
                         "message": f'"{portal}" is not an authorized portal.', "item": None})
        return findings

    if not isinstance(nav, dict) or not isinstance(nav.get('groups'), list):
        findings.append({"severity": "high", "code": "invalid_structure",
                         "message": "Navigation payload must contain a groups array.", "item": None})
        return findings

    seen_ids = {}
    owner = PORTAL_OWNERS[portal]
    locked_found = set()

    for gi, g in enumerate(nav.get('groups', [])):
        if not g.get('label'):
            findings.append({"severity": "medium", "code": "missing_group_label",
                             "message": f"Group #{gi + 1} has no label.", "item": g.get('id')})
        if not g.get('links'):
            findings.append({"severity": "low", "code": "orphan_group",
                             "message": f'Group "{g.get("label", gi)}" contains no items.', "item": g.get('id')})

        for item, parent_id, depth in _walk_many(g.get('links', [])):
            iid = item.get('id')
            if not iid:
                findings.append({"severity": "high", "code": "missing_id",
                                 "message": f'Item "{item.get("label", "?")}" has no stable id.', "item": None})
            else:
                seen_ids.setdefault(iid, 0)
                seen_ids[iid] += 1

            if not item.get('label'):
                findings.append({"severity": "medium", "code": "missing_label",
                                 "message": f'Item "{iid or "?"}" has no display label.', "item": iid})

            href = item.get('href')
            if not item.get('children'):
                if not href:
                    findings.append({"severity": "high", "code": "missing_destination",
                                     "message": f'"{item.get("label", iid)}" has no destination.', "item": iid})
                elif not _route_registered(href):
                    findings.append({"severity": "high", "code": "broken_route",
                                     "message": f'"{item.get("label", iid)}" points to an unregistered route: {href}', "item": iid})

            if not item.get('icon') and not item.get('children') and depth == 1:
                findings.append({"severity": "low", "code": "missing_icon",
                                 "message": f'"{item.get("label", iid)}" has no icon.', "item": iid})

            # Cross-portal exposure guard (visibility is NOT authorization).
            if href and isinstance(href, str):
                clean = href.split('?', 1)[0].split('#', 1)[0].strip('/')
                if clean.startswith('pages/') and not clean.startswith('pages/shared/'):
                    parts = clean.split('/')
                    seg = parts[1].lower() if len(parts) > 1 else ''
                    if seg in PORTALS and seg != owner:
                        findings.append({"severity": "high", "code": "cross_portal_exposure",
                                         "message": f'"{item.get("label", iid)}" exposes the {seg} portal from the {portal} sidebar.',
                                         "item": iid})

            if item.get('locked'):
                locked_found.add(iid)
                if depth > 1:
                    findings.append({"severity": "medium", "code": "locked_not_top_level",
                                     "message": f'Mandatory item "{item.get("label", iid)}" is nested; keep it top-level.',
                                     "item": iid})

    for iid, n in seen_ids.items():
        if n > 1:
            findings.append({"severity": "high", "code": "duplicate_id",
                             "message": f'Duplicate item id "{iid}" appears {n} times.', "item": iid})

    # Mandatory navigation must survive.
    defaults = _ensure_seeded().get('defaults', {}).get(portal, {})
    for d_item, _p, _d in _walk_many([l for g in defaults.get('groups', []) for l in g.get('links', [])]):
        if d_item.get('locked'):
            live = seen_ids.get(d_item.get('id'))
            if not live:
                findings.append({"severity": "high", "code": "mandatory_removed",
                                 "message": f'Mandatory item "{d_item.get("label")}" is missing from the published navigation.',
                                 "item": d_item.get('id')})
    return findings


def _walk_many(links):
    for l in links or []:
        yield from _walk(l, None, 1)


def health_check(portal):
    """Runs validation against the current published navigation."""
    nav = get_published(portal)
    if nav is None:
        return {"portal": portal, "findings": [
            {"severity": "high", "code": "unknown_portal",
             "message": f'No navigation configuration found for "{portal}".', "item": None}]}
    findings = validate(portal, nav)
    return {
        "portal": portal,
        "label": PORTAL_LABELS.get(portal, portal.title()),
        "findings": findings,
        "counts": {
            "high": sum(1 for f in findings if f['severity'] == 'high'),
            "medium": sum(1 for f in findings if f['severity'] == 'medium'),
            "low": sum(1 for f in findings if f['severity'] == 'low'),
        },
    }


def health_check_all():
    return [health_check(p) for p in PORTALS if get_published(p) is not None]


def get_route_registry():
    """Real, filesystem-backed list of registered destinations for the picker."""
    routes = []
    index_path = os.path.join(BASE_DIR, 'index.html')
    if os.path.exists(index_path):
        routes.append('index.html')
    pages_dir = os.path.join(BASE_DIR, 'pages')
    for root, _dirs, files in os.walk(pages_dir):
        for fn in files:
            if fn.lower().endswith('.html'):
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, BASE_DIR).replace(os.sep, '/')
                routes.append(rel)
    return sorted(set(routes))


# ── Audit + versions ──
def log_audit_event(actor, action, portal='all', details='', outcome='SUCCESS'):
    logs = _load_json(NAV_AUDIT_FILE, [])
    event = {
        "id": f"naud-{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:4]}",
        "timestamp": _now(),
        "actor_id": actor.get('id', 'ADM-2024-001') if isinstance(actor, dict) else 'ADM-2024-001',
        "actor_email": _actor_email(actor),
        "actor_name": _actor_name(actor),
        "action": action,
        "portal": portal,
        "details": details,
        "outcome": outcome,
    }
    logs.insert(0, event)
    _save_json(NAV_AUDIT_FILE, logs[:400])
    return event


def get_audit_log(portal=None, limit=50):
    logs = _load_json(NAV_AUDIT_FILE, [])
    if portal and portal != 'all':
        logs = [l for l in logs if l.get('portal') in (portal, 'all')]
    return sorted(logs, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]


def get_versions(portal=None):
    versions = _load_json(NAV_VERSIONS_FILE, [])
    if portal and portal != 'all':
        versions = [v for v in versions if v.get('portal') == portal]
    return versions


# ── Mutations ──
def save_draft(portal, payload, actor):
    if portal not in PORTALS:
        return False, f"Unknown portal: {portal}"
    data = _ensure_seeded()
    cfg = data.get('portals', {}).get(portal)
    if not cfg:
        return False, f"No configuration for portal: {portal}"

    draft = {
        "brand": payload.get('brand', cfg.get('brand', '')),
        "meta": payload.get('meta', cfg.get('meta', '')),
        "groups": copy.deepcopy(payload.get('groups', [])),
    }
    cfg['draft'] = draft
    cfg['draft_updated_at'] = _now()
    cfg['draft_updated_by'] = _actor_email(actor)
    data['last_updated'] = _now()
    data['updated_by'] = _actor_email(actor)

    if _save_json(NAV_FILE, data):
        log_audit_event(actor, "nav_draft_saved", portal=portal,
                        details=f"Saved navigation draft for {PORTAL_LABELS.get(portal, portal)}.")
        return True, "Navigation draft saved."
    return False, "Failed to persist navigation draft."


def publish(portal, actor, summary="Published navigation changes"):
    if portal not in PORTALS:
        return False, f"Unknown portal: {portal}"
    data = _ensure_seeded()
    cfg = data.get('portals', {}).get(portal)
    if not cfg:
        return False, f"No configuration for portal: {portal}"

    draft = cfg.get('draft')
    if not draft:
        return False, "No draft to publish. Save a draft first."

    # Validate before publishing (never publish broken navigation).
    findings = validate(portal, draft)
    blockers = [f for f in findings if f['severity'] == 'high']
    if blockers:
        return False, {"message": "Navigation failed validation.", "findings": blockers}

    # Snapshot the current published state for rollback.
    versions = _load_json(NAV_VERSIONS_FILE, [])
    version_id = f"nver-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4]}"
    versions.insert(0, {
        "version_id": version_id,
        "portal": portal,
        "timestamp": _now(),
        "author": _actor_email(actor),
        "author_name": _actor_name(actor),
        "summary": summary,
        "snapshot": _published_view(cfg),
    })
    _save_json(NAV_VERSIONS_FILE, versions[:MAX_VERSIONS])

    cfg['brand'] = draft.get('brand', cfg.get('brand', ''))
    cfg['meta'] = draft.get('meta', cfg.get('meta', ''))
    cfg['groups'] = copy.deepcopy(draft.get('groups', []))
    cfg['status'] = 'published'
    cfg['last_published'] = _now()
    cfg['published_by'] = _actor_email(actor)
    cfg.pop('draft', None)
    cfg.pop('draft_updated_at', None)
    cfg.pop('draft_updated_by', None)

    data['last_updated'] = _now()
    data['updated_by'] = _actor_email(actor)
    if not _save_json(NAV_FILE, data):
        return False, "Failed to write published navigation."

    log_audit_event(actor, "nav_published", portal=portal,
                    details=f"Version {version_id}: {summary}")
    return True, {"version_id": version_id, "timestamp": _now()}


def restore_version(version_id, actor):
    versions = _load_json(NAV_VERSIONS_FILE, [])
    target = next((v for v in versions if v.get('version_id') == version_id), None)
    if not target:
        return False, "Version snapshot not found."
    portal = target.get('portal')
    snapshot = target.get('snapshot')
    if portal not in PORTALS or not snapshot:
        return False, "Corrupted snapshot in version record."

    data = _ensure_seeded()
    cfg = data.get('portals', {}).get(portal)
    if not cfg:
        return False, f"No configuration for portal: {portal}"

    cfg['brand'] = snapshot.get('brand', cfg.get('brand', ''))
    cfg['meta'] = snapshot.get('meta', cfg.get('meta', ''))
    cfg['groups'] = copy.deepcopy(snapshot.get('groups', []))
    cfg['status'] = 'published'
    cfg['last_published'] = _now()
    cfg['published_by'] = _actor_email(actor)
    cfg.pop('draft', None)

    data['last_updated'] = _now()
    data['updated_by'] = _actor_email(actor)
    _save_json(NAV_FILE, data)
    log_audit_event(actor, "nav_version_restored", portal=portal,
                    details=f"Restored navigation from version {version_id}")
    return True, f"Restored {PORTAL_LABELS.get(portal, portal)} from {version_id}."


def restore_defaults(portal, actor):
    if portal not in PORTALS:
        return False, f"Unknown portal: {portal}"
    data = _ensure_seeded()
    defaults = data.get('defaults', {}).get(portal)
    if not defaults:
        return False, "No default configuration stored for this portal."
    cfg = data['portals'][portal]
    cfg['brand'] = defaults.get('brand', cfg.get('brand', ''))
    cfg['meta'] = defaults.get('meta', cfg.get('meta', ''))
    cfg['groups'] = copy.deepcopy(defaults.get('groups', []))
    cfg['status'] = 'published'
    cfg['last_published'] = _now()
    cfg['published_by'] = _actor_email(actor)
    cfg.pop('draft', None)
    data['last_updated'] = _now()
    data['updated_by'] = _actor_email(actor)
    _save_json(NAV_FILE, data)
    log_audit_event(actor, "nav_defaults_restored", portal=portal,
                    details=f"Restored factory navigation for {PORTAL_LABELS.get(portal, portal)}.")
    return True, f"Restored factory defaults for {PORTAL_LABELS.get(portal, portal)}."
