"""
NGIS Dashboard Content Management System (CMS) Engine
Production-ready content management, banner orchestration, hero configuration,
and multi-portal publication engine.
"""

import os
import json
import uuid
import re
from datetime import datetime
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CMS_FILE = os.path.join(DATA_DIR, 'dashboard_cms.json')
VERSIONS_FILE = os.path.join(DATA_DIR, 'dashboard_cms_versions.json')
AUDIT_FILE = os.path.join(DATA_DIR, 'dashboard_cms_audit.json')

BANNERS_UPLOAD_DIR = os.path.join(BASE_DIR, 'assets', 'uploads', 'banners')
os.makedirs(BANNERS_UPLOAD_DIR, exist_ok=True)

MAX_MEDIA_BYTES = 5 * 1024 * 1024  # 5MB max
ALLOWED_IMAGE_FORMATS = {'JPEG', 'PNG', 'WEBP'}

SAMPLE_IDENTITIES = {
    'student': {
        'first_name': 'Nrinphouneta',
        'full_name': 'Nrinphouneta Hok',
        'role': 'Student',
        'id': '2026-STD-0142',
        'campus': 'Phnom Penh Main Campus'
    },
    'teacher': {
        'first_name': 'Sarah',
        'full_name': 'Dr. Sarah Jenkins',
        'role': 'Mathematics Lead',
        'id': 'TCH-2024-042',
        'campus': 'Phnom Penh Main Campus'
    },
    'principal': {
        'first_name': 'Ly Bunheng',
        'full_name': 'Dr. Ly Bunheng',
        'role': 'Executive Principal',
        'id': 'PRN-2024-002',
        'campus': 'Phnom Penh Main Campus'
    },
    'admin': {
        'first_name': 'Panha',
        'full_name': 'Sok Panha Heng',
        'role': 'Super Administrator',
        'id': 'ADM-2024-001',
        'campus': 'Phnom Penh Main Campus'
    }
}


def _load_json(filepath, default):
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[CMS Engine] Error reading {filepath}: {e}")
        return default


def _save_json(filepath, data):
    tmp_path = filepath + f".tmp_{uuid.uuid4().hex[:6]}"
    try:
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, filepath)
        return True
    except Exception as e:
        print(f"[CMS Engine] Error saving {filepath}: {e}")
        if os.path.exists(tmp_path):
            try: os.remove(tmp_path)
            except: pass
        return False


def get_cms_data():
    """Returns the full CMS configuration structure."""
    return _load_json(CMS_FILE, {"version": 1, "portals_config": {}, "media_library": []})


def get_versions(portal=None):
    """Returns version history list."""
    versions = _load_json(VERSIONS_FILE, [])
    if portal and portal != 'all':
        return [v for v in versions if v.get('portal') in (portal, 'all')]
    return versions


def get_audit_log(portal=None, limit=50):
    """Returns chronological audit logs."""
    logs = _load_json(AUDIT_FILE, [])
    if portal and portal != 'all':
        logs = [l for l in logs if l.get('portal') in (portal, 'all')]
    return sorted(logs, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]


def log_audit_event(actor, action, portal='all', campus='all', details='', outcome='SUCCESS'):
    """Records an immutable audit event."""
    logs = _load_json(AUDIT_FILE, [])
    event = {
        "id": f"aud-{int(datetime.now().timestamp())}-{uuid.uuid4().hex[:4]}",
        "timestamp": datetime.now().isoformat() + "Z",
        "actor_id": actor.get('id', 'ADM-2024-001') if isinstance(actor, dict) else 'ADM-2024-001',
        "actor_email": actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor),
        "actor_name": actor.get('name', 'Sok Panha Heng') if isinstance(actor, dict) else 'Admin',
        "action": action,
        "portal": portal,
        "campus": campus,
        "details": details,
        "outcome": outcome
    }
    logs.insert(0, event)
    _save_json(AUDIT_FILE, logs)
    return event


def resolve_dynamic_variables(template_str, user_info=None, portal='student', campus_name='Phnom Penh Main Campus'):
    """
    Safely resolves template tokens:
    {first_name}, {full_name}, {role}, {school_name}, {campus_name}, {academic_year}
    """
    if not template_str:
        return ""

    user = user_info or SAMPLE_IDENTITIES.get(portal, SAMPLE_IDENTITIES['student'])
    
    first_name = user.get('first_name') or user.get('name', '').split(' ')[0] or 'Scholar'
    full_name = user.get('full_name') or user.get('name') or 'Distinguished Member'
    role = user.get('role') or portal.capitalize()
    school_name = "New Gateway International School"
    academic_year = "2026–2027"

    replacements = {
        '{first_name}': first_name,
        '{full_name}': full_name,
        '{role}': role,
        '{school_name}': school_name,
        '{campus_name}': campus_name,
        '{academic_year}': academic_year
    }

    result = template_str
    for token, val in replacements.items():
        result = result.replace(token, val)
    return result


def format_dynamic_date(date_config=None, target_dt=None):
    """Formats live date string according to date_config."""
    dt = target_dt or datetime.now()
    cfg = date_config or {}
    fmt = cfg.get('format', 'full')

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    if fmt == 'iso':
        return dt.strftime('%Y-%m-%d')
    elif fmt == 'short':
        return f"{months[dt.month-1][:3]} {dt.day}, {dt.year}"
    else:  # full
        weekday = days[dt.weekday()]
        month = months[dt.month-1]
        return f"{weekday}, {month} {dt.day}, {dt.year}"


def get_portal_content(portal='student', campus='all', mode='published', user=None):
    """
    Returns sanitized, active content for client dashboards or preview rendering.
    """
    data = get_cms_data()
    portal_cfg = data.get('portals_config', {}).get(portal)
    if not portal_cfg:
        portal_cfg = data.get('portals_config', {}).get('student', {})

    target_cfg = portal_cfg
    if mode == 'draft' and 'draft' in portal_cfg:
        target_cfg = portal_cfg['draft']

    # 1. Hero Resolution
    hero_raw = target_cfg.get('hero', {})
    date_cfg = hero_raw.get('date_config', {})
    greeting_tmpl = hero_raw.get('greeting_template', 'Hello, {first_name}!')
    greeting_resolved = resolve_dynamic_variables(greeting_tmpl, user_info=user, portal=portal)
    date_formatted = format_dynamic_date(date_cfg)

    hero_rendered = {
        "title": hero_raw.get('title', 'Welcome to your dashboard'),
        "description": hero_raw.get('description', ''),
        "greeting": greeting_resolved,
        "greeting_template": greeting_tmpl,
        "date": date_formatted,
        "date_visible": date_cfg.get('visible', True),
        "visible": hero_raw.get('visible', True),
        "text_alignment": hero_raw.get('text_alignment', 'left'),
        "appearance": hero_raw.get('appearance', {})
    }

    # 2. Banners Resolution (filtered by campus, status, date window)
    raw_banners = target_cfg.get('banners', [])
    active_banners = []
    now_iso = datetime.now().isoformat()

    for b in raw_banners:
        if mode == 'published' and not b.get('active', True):
            continue
        if mode == 'published' and b.get('status') != 'published':
            continue

        # Campus check
        b_campuses = b.get('target_campuses', ['all'])
        if campus != 'all' and 'all' not in b_campuses and campus not in b_campuses:
            continue

        # Date window check
        s_date = b.get('start_date')
        e_date = b.get('end_date')
        if s_date and s_date > now_iso:
            continue
        if e_date and e_date < now_iso:
            continue

        # Sanitize button url
        btn_url = b.get('button_url', '')
        if btn_url.lower().startswith('javascript:'):
            btn_url = '#'

        active_banners.append({
            "id": b.get('id'),
            "name": b.get('name'),
            "heading": b.get('heading', ''),
            "subtitle": b.get('subtitle', ''),
            "description": b.get('description', ''),
            "image_url": b.get('image_url', ''),
            "alt_text": b.get('alt_text', ''),
            "button_label": b.get('button_label', ''),
            "button_url": btn_url,
            "target_portals": b.get('target_portals', [portal]),
            "target_campuses": b.get('target_campuses', ['all']),
            "order": b.get('order', 99),
            "status": b.get('status', 'published'),
            "active": b.get('active', True)
        })

    active_banners.sort(key=lambda x: x.get('order', 99))

    # 3. Carousel Settings
    carousel = target_cfg.get('carousel_settings', {
        "autoplay": True,
        "interval_seconds": 6,
        "show_arrows": True,
        "show_dots": True,
        "pause_on_hover": True,
        "respect_reduced_motion": True
    })

    # 4. Page Sections
    sections = target_cfg.get('page_sections', [])
    sections_sorted = sorted(sections, key=lambda s: s.get('order', 99))

    return {
        "portal": portal,
        "campus": campus,
        "mode": mode,
        "status": target_cfg.get('status', 'published'),
        "last_published": target_cfg.get('last_published'),
        "published_by": target_cfg.get('published_by'),
        "has_draft": 'draft' in portal_cfg,
        "hero": hero_rendered,
        "banners": active_banners,
        "carousel": carousel,
        "page_sections": sections_sorted
    }


def save_draft(portal, draft_payload, actor):
    """Saves unpublished draft content for a portal."""
    data = get_cms_data()
    if portal not in data.get('portals_config', {}):
        return False, f"Unknown portal: {portal}"

    portal_cfg = data['portals_config'][portal]
    portal_cfg['draft'] = draft_payload
    portal_cfg['draft_updated_at'] = datetime.now().isoformat() + "Z"
    portal_cfg['draft_updated_by'] = actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor)

    data['last_updated'] = datetime.now().isoformat() + "Z"
    data['updated_by'] = portal_cfg['draft_updated_by']
    
    saved = _save_json(CMS_FILE, data)
    if saved:
        log_audit_event(actor, "draft_saved", portal=portal, details="Saved dashboard content draft.")
        return True, "Draft saved successfully."
    return False, "Failed to persist draft."


def publish_content(portal, payload, actor, summary="Published dashboard content"):
    """
    Atomically publishes content to live dashboard, creates version snapshot,
    and updates audit journal.
    """
    data = get_cms_data()
    if portal not in data.get('portals_config', {}):
        return False, f"Unknown portal: {portal}"

    portal_cfg = data['portals_config'][portal]

    # Pre-publication snapshot for rollback
    prev_snapshot = json.loads(json.dumps(portal_cfg))

    # Apply published state
    now_ts = datetime.now().isoformat() + "Z"
    actor_email = actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor)

    if 'hero' in payload:
        portal_cfg['hero'] = payload['hero']
    if 'banners' in payload:
        portal_cfg['banners'] = payload['banners']
    if 'carousel_settings' in payload:
        portal_cfg['carousel_settings'] = payload['carousel_settings']
    if 'page_sections' in payload:
        portal_cfg['page_sections'] = payload['page_sections']

    portal_cfg['status'] = 'published'
    portal_cfg['last_published'] = now_ts
    portal_cfg['published_by'] = actor_email
    
    # Remove draft flag if payload represents full draft promotion
    if 'draft' in portal_cfg:
        del portal_cfg['draft']

    data['last_updated'] = now_ts
    data['updated_by'] = actor_email

    saved = _save_json(CMS_FILE, data)
    if not saved:
        return False, "Failed to write published changes to persistent store."

    # Create immutable version record
    versions = _load_json(VERSIONS_FILE, [])
    version_id = f"ver-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:4]}"
    v_record = {
        "version_id": version_id,
        "portal": portal,
        "timestamp": now_ts,
        "author": actor_email,
        "author_name": actor.get('name', 'Admin') if isinstance(actor, dict) else 'Admin',
        "summary": summary,
        "snapshot": portal_cfg
    }
    versions.insert(0, v_record)
    _save_json(VERSIONS_FILE, versions)

    log_audit_event(actor, "content_published", portal=portal, details=f"Version {version_id}: {summary}")
    return True, {"version_id": version_id, "timestamp": now_ts}


def schedule_content(portal, scheduled_time_iso, payload, actor):
    """Schedules content for automatic publication."""
    data = get_cms_data()
    if portal not in data.get('portals_config', {}):
        return False, "Invalid portal"

    portal_cfg = data['portals_config'][portal]
    portal_cfg['scheduled_payload'] = payload
    portal_cfg['scheduled_at'] = scheduled_time_iso
    portal_cfg['scheduled_by'] = actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor)
    portal_cfg['status'] = 'scheduled'

    _save_json(CMS_FILE, data)
    log_audit_event(actor, "content_scheduled", portal=portal, details=f"Publication scheduled for {scheduled_time_iso}")
    return True, f"Content scheduled for {scheduled_time_iso}"


def restore_version(version_id, actor):
    """Rolls back portal configuration to a previously published version snapshot."""
    versions = _load_json(VERSIONS_FILE, [])
    target_v = next((v for v in versions if v.get('version_id') == version_id), None)
    if not target_v:
        return False, "Version snapshot not found"

    portal = target_v.get('portal')
    snapshot = target_v.get('snapshot')
    if not portal or not snapshot:
        return False, "Corrupted snapshot in version record"

    data = get_cms_data()
    data['portals_config'][portal] = json.loads(json.dumps(snapshot))
    data['last_updated'] = datetime.now().isoformat() + "Z"
    data['updated_by'] = actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor)

    _save_json(CMS_FILE, data)
    log_audit_event(actor, "version_restored", portal=portal, details=f"Restored configuration from version {version_id}")
    return True, f"Successfully restored version {version_id} for {portal} portal."


def save_media_file(file_storage, meta, actor):
    """
    Validates true file header/format via PIL, checks file size,
    saves file to banners upload directory, and tracks in media library.
    """
    if not file_storage or not file_storage.filename:
        return False, "No file provided"

    # Enforce file size limit
    file_storage.seek(0, os.SEEK_END)
    size_bytes = file_storage.tell()
    file_storage.seek(0)

    if size_bytes > MAX_MEDIA_BYTES:
        return False, f"File size ({size_bytes / 1024 / 1024:.1f}MB) exceeds 5MB limit"

    # Header inspection via PIL
    try:
        img = Image.open(file_storage)
        img_format = img.format.upper()
        if img_format not in ALLOWED_IMAGE_FORMATS:
            return False, f"Invalid image format: {img_format}. Only JPEG, PNG, and WebP are accepted."
        width, height = img.size
    except Exception as e:
        return False, f"Invalid or corrupted image: {e}"

    # Reset stream pointer
    file_storage.seek(0)

    # Safe unique filename
    ext = 'jpg' if img_format == 'JPEG' else img_format.lower()
    clean_base = re.sub(r'[^a-zA-Z0-9_-]', '_', os.path.splitext(file_storage.filename)[0])[:30]
    safe_filename = f"ban_{clean_base}_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:4]}.{ext}"
    dest_path = os.path.join(BANNERS_UPLOAD_DIR, safe_filename)

    file_storage.save(dest_path)
    relative_url = f"assets/uploads/banners/{safe_filename}"

    # Record in media library
    data = get_cms_data()
    media_lib = data.setdefault('media_library', [])

    media_id = f"med-{uuid.uuid4().hex[:6]}"
    media_item = {
        "id": media_id,
        "filename": safe_filename,
        "url": relative_url,
        "alt_text": meta.get('alt_text', clean_base.replace('_', ' ')),
        "width": width,
        "height": height,
        "size_kb": round(size_bytes / 1024, 1),
        "format": img_format,
        "uploaded_at": datetime.now().isoformat() + "Z",
        "uploaded_by": actor.get('email', 'admin@ngis.edu.kh') if isinstance(actor, dict) else str(actor),
        "used_in": []
    }
    media_lib.insert(0, media_item)
    _save_json(CMS_FILE, data)

    log_audit_event(actor, "media_uploaded", details=f"Uploaded banner image: {safe_filename} ({width}x{height}px)")
    return True, media_item


def delete_media(media_id, actor):
    """
    Deletes media from library with referential integrity check.
    Prevents deletion if referenced in any active banner.
    """
    data = get_cms_data()
    media_lib = data.get('media_library', [])
    item = next((m for m in media_lib if m['id'] == media_id), None)
    if not item:
        return False, "Media item not found"

    # Check references across all portals
    item_url = item.get('url')
    references = []
    for p_name, p_cfg in data.get('portals_config', {}).items():
        for b in p_cfg.get('banners', []):
            if b.get('image_url') == item_url or item['id'] in b.get('id', ''):
                references.append(f"{p_name}: {b.get('name')}")

    if references:
        return False, f"Cannot delete media in use by: {', '.join(references)}"

    # Delete physical file if local
    if item_url.startswith('assets/uploads/banners/'):
        phys_path = os.path.join(BASE_DIR, item_url.replace('/', os.sep))
        if os.path.exists(phys_path):
            try: os.remove(phys_path)
            except: pass

    data['media_library'] = [m for m in media_lib if m['id'] != media_id]
    _save_json(CMS_FILE, data)
    log_audit_event(actor, "media_deleted", details=f"Deleted media asset {media_id} ({item.get('filename')})")
    return True, "Media deleted successfully."

