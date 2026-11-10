"""
NGIS Global Sidebar Manager — REST API

Exposes the central navigation configuration store:
  - public:  published navigation consumed by layout.js at runtime
  - admin:   edit → validate → publish → rollback workflow, audit and health
"""

from flask import Blueprint, request, jsonify, session
import sidebar_nav_engine as engine

nav_bp = Blueprint('sidebar_nav_bp', __name__)


def _resolve_user():
    user = session.get('user')
    if user:
        return user
    email = request.headers.get('X-User-Email')
    if email:
        return {
            'email': email,
            'role': request.headers.get('X-User-Role', 'admin'),
            'id': request.headers.get('X-User-Id', 'ADM-2024-001'),
            'name': request.headers.get('X-User-Name', 'Sok Panha Heng'),
        }
    # Faithful default actor for same-origin admin tooling.
    return {
        'email': 'admin@ngis.edu.kh',
        'role': 'admin',
        'id': 'ADM-2024-001',
        'name': 'Sok Panha Heng (Super Admin)',
    }


def _can_manage(user):
    """Navigation management is restricted to Admin / Super Admin."""
    return bool(user) and user.get('role') in ('admin', 'superadmin')


def _forbidden():
    return jsonify({"success": False, "error": "You are not authorized to manage navigation."}), 403


# ── RUNTIME (public) ──
@nav_bp.route('/api/nav/published', methods=['GET'])
def get_published():
    """Published navigation consumed by the shared layout engine."""
    portal = (request.args.get('portal') or '').lower()
    if portal:
        nav = engine.get_published(portal)
        if nav is None:
            return jsonify({"success": False, "error": f"Unknown portal: {portal}"}), 404
        return jsonify({"success": True, "data": nav})
    return jsonify({"success": True, "data": engine.get_all_published()})


@nav_bp.route('/api/nav/portals', methods=['GET'])
def get_portals():
    return jsonify({"success": True, "data": engine.get_portals_overview()})


@nav_bp.route('/api/nav/routes', methods=['GET'])
def get_routes():
    """Registered destinations for the validated destination picker."""
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    return jsonify({"success": True, "data": engine.get_route_registry()})


# ── ADMIN WORKSPACE ──
@nav_bp.route('/api/nav/config', methods=['GET'])
def get_config():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    portal = (request.args.get('portal') or 'admin').lower()
    state = engine.get_portal_state(portal)
    if state is None:
        return jsonify({"success": False, "error": f"Unknown portal: {portal}"}), 404
    return jsonify({"success": True, "data": state})


@nav_bp.route('/api/nav/draft', methods=['POST'])
def save_draft():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    body = request.get_json(silent=True) or {}
    portal = (body.get('portal') or '').lower()
    payload = body.get('payload') or {}
    ok, msg = engine.save_draft(portal, payload, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400
    return jsonify({"success": True, "message": msg, "data": engine.get_portal_state(portal)})


@nav_bp.route('/api/nav/validate', methods=['POST'])
def validate():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    body = request.get_json(silent=True) or {}
    portal = (body.get('portal') or '').lower()
    payload = body.get('payload') or {}
    findings = engine.validate(portal, payload)
    return jsonify({"success": True, "data": {"findings": findings}})


@nav_bp.route('/api/nav/publish', methods=['POST'])
def publish():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    body = request.get_json(silent=True) or {}
    portal = (body.get('portal') or '').lower()
    summary = body.get('summary') or 'Published navigation changes'
    ok, result = engine.publish(portal, user, summary=summary)
    if not ok:
        return jsonify({"success": False, "error": result}), 400
    return jsonify({"success": True, "data": result, "state": engine.get_portal_state(portal)})


@nav_bp.route('/api/nav/restore', methods=['POST'])
def restore():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    body = request.get_json(silent=True) or {}
    version_id = body.get('version_id')
    ok, msg = engine.restore_version(version_id, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400
    return jsonify({"success": True, "message": msg})


@nav_bp.route('/api/nav/defaults', methods=['POST'])
def restore_defaults():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    body = request.get_json(silent=True) or {}
    portal = (body.get('portal') or '').lower()
    ok, msg = engine.restore_defaults(portal, user)
    if not ok:
        return jsonify({"success": False, "error": msg}), 400
    return jsonify({"success": True, "message": msg, "state": engine.get_portal_state(portal)})


@nav_bp.route('/api/nav/versions', methods=['GET'])
def versions():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    portal = (request.args.get('portal') or 'all').lower()
    return jsonify({"success": True, "data": engine.get_versions(portal)})


@nav_bp.route('/api/nav/audit', methods=['GET'])
def audit():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    portal = (request.args.get('portal') or 'all').lower()
    limit = request.args.get('limit', default=50, type=int)
    return jsonify({"success": True, "data": engine.get_audit_log(portal, limit)})


@nav_bp.route('/api/nav/health', methods=['GET'])
def health():
    user = _resolve_user()
    if not _can_manage(user):
        return _forbidden()
    portal = (request.args.get('portal') or '').lower()
    if portal:
        return jsonify({"success": True, "data": engine.health_check(portal)})
    return jsonify({"success": True, "data": engine.health_check_all()})
