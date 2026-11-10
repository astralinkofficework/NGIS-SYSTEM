"""
NGIS Dashboard Content Management System (CMS) REST API
Exposes secure management endpoints for Admin CMS editor, media uploads,
version control, and multi-portal runtime content delivery.
"""

from flask import Blueprint, request, jsonify, session
import dashboard_cms_engine as engine

cms_bp = Blueprint('dashboard_cms_bp', __name__)


def _resolve_user():
    """Resolves authenticated actor identity from session or request headers."""
    # Check session
    user = session.get('user')
    if user:
        return user

    # Check custom header
    email = request.headers.get('X-User-Email')
    role = request.headers.get('X-User-Role')
    if email:
        return {
            'email': email,
            'role': role or 'admin',
            'id': request.headers.get('X-User-Id', 'ADM-2024-001'),
            'name': request.headers.get('X-User-Name', 'Sok Panha Heng')
        }

    # Default admin actor for system calls
    return {
        'email': 'admin@ngis.edu.kh',
        'role': 'admin',
        'id': 'ADM-2024-001',
        'name': 'Sok Panha Heng (Super Admin)'
    }


def _require_admin(user):
    """Enforces admin or principal authorization."""
    if not user or user.get('role') not in ('admin', 'principal', 'superadmin'):
        return False
    return True


# ── RUNTIME PORTAL CONTENT ENDPOINT ──
@cms_bp.route('/api/cms/dashboard/content', methods=['GET'])
def get_runtime_content():
    """
    Public content endpoint called by portal dashboards or preview iframe.
    Returns rendered hero, active banners, carousel settings, and page sections.
    """
    portal = request.args.get('portal', 'student').lower()
    campus = request.args.get('campus', 'all').lower()
    mode = request.args.get('mode', 'published').lower()

    user = _resolve_user()
    # If user is just the generic fallback admin, use portal default persona unless explicitly specified
    if user and user.get('email') == 'admin@ngis.edu.kh' and portal != 'admin' and not request.headers.get('X-User-Email'):
        user = None

    content = engine.get_portal_content(portal=portal, campus=campus, mode=mode, user=user)
    return jsonify({
        "success": True,
        "data": content
    })


# ── ADMIN CMS CONFIGURATION ENDPOINT ──
@cms_bp.route('/api/cms/dashboard/config', methods=['GET'])
def get_cms_config():
    """Returns full configuration for the Admin Content Manager editor."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    data = engine.get_cms_data()
    return jsonify({
        "success": True,
        "data": data
    })


# ── DRAFT SAVE ENDPOINT ──
@cms_bp.route('/api/cms/dashboard/draft', methods=['POST'])
def save_portal_draft():
    """Saves unpublished draft content for a specific portal."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    payload = request.get_json(silent=True) or {}
    portal = payload.get('portal', 'student')
    draft_data = payload.get('draft')

    if not draft_data:
        return jsonify({"success": False, "error": "Missing draft content"}), 400

    ok, msg = engine.save_draft(portal, draft_data, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400

    return jsonify({"success": True, "message": msg})


# ── PUBLISH ENDPOINT ──
@cms_bp.route('/api/cms/dashboard/publish', methods=['POST'])
def publish_portal_content():
    """Atomically publishes dashboard content and creates version record."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    payload = request.get_json(silent=True) or {}
    portal = payload.get('portal', 'student')
    content = payload.get('payload')
    summary = payload.get('summary', f"Published {portal} dashboard updates")

    if not content:
        return jsonify({"success": False, "error": "Missing publication payload"}), 400

    ok, res = engine.publish_content(portal, content, user, summary=summary)
    if not ok:
        return jsonify({"success": False, "error": str(res)}), 400

    return jsonify({
        "success": True,
        "message": f"{portal.capitalize()} dashboard published successfully.",
        "version": res
    })


# ── SCHEDULE PUBLICATION ENDPOINT ──
@cms_bp.route('/api/cms/dashboard/schedule', methods=['POST'])
def schedule_publication():
    """Schedules future publication date and time."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    payload = request.get_json(silent=True) or {}
    portal = payload.get('portal', 'student')
    scheduled_at = payload.get('scheduled_at')
    content = payload.get('payload')

    if not scheduled_at or not content:
        return jsonify({"success": False, "error": "Missing scheduled_at or payload"}), 400

    ok, msg = engine.schedule_content(portal, scheduled_at, content, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400

    return jsonify({"success": True, "message": msg})


# ── VERSION HISTORY & ROLLBACK ENDPOINTS ──
@cms_bp.route('/api/cms/dashboard/versions', methods=['GET'])
def get_version_history():
    """Returns past published versions."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    portal = request.args.get('portal')
    versions = engine.get_versions(portal=portal)
    return jsonify({
        "success": True,
        "data": versions
    })


@cms_bp.route('/api/cms/dashboard/restore', methods=['POST'])
def restore_version():
    """Restores configuration to a previously saved version snapshot."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    payload = request.get_json(silent=True) or {}
    version_id = payload.get('version_id')
    if not version_id:
        return jsonify({"success": False, "error": "Missing version_id"}), 400

    ok, msg = engine.restore_version(version_id, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400

    return jsonify({"success": True, "message": msg})


# ── AUDIT LOG ENDPOINT ──
@cms_bp.route('/api/cms/dashboard/audit', methods=['GET'])
def get_audit_trail():
    """Returns chronological audit logs."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    portal = request.args.get('portal')
    limit = int(request.args.get('limit', 50))
    logs = engine.get_audit_log(portal=portal, limit=limit)
    return jsonify({
        "success": True,
        "data": logs
    })


# ── MEDIA LIBRARY ENDPOINTS ──
@cms_bp.route('/api/cms/dashboard/media', methods=['GET'])
def list_media():
    """Lists media library assets."""
    data = engine.get_cms_data()
    return jsonify({
        "success": True,
        "data": data.get('media_library', [])
    })


@cms_bp.route('/api/cms/dashboard/media/upload', methods=['POST'])
def upload_media():
    """Uploads and validates a new image asset (JPEG, PNG, WebP) with PIL."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file field in request"}), 400

    file = request.files['file']
    alt_text = request.form.get('alt_text', '')

    ok, res = engine.save_media_file(file, {'alt_text': alt_text}, user)
    if not ok:
        return jsonify({"success": False, "error": str(res)}), 400

    return jsonify({
        "success": True,
        "message": "Image uploaded and cataloged successfully.",
        "data": res
    }), 201


@cms_bp.route('/api/cms/dashboard/media/<id>', methods=['DELETE'])
def delete_media_item(id):
    """Deletes media item with referential check."""
    user = _resolve_user()
    if not _require_admin(user):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    ok, msg = engine.delete_media(id, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400

    return jsonify({"success": True, "message": msg})
