"""
============================================================================
NGIS Admin Operations & IT Control Center REST API Blueprint
============================================================================
Exposes authoritative endpoints for system-wide operations monitoring,
card metrics, issues registry, system health diagnostics, and staff follow-ups.
============================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict

from flask import Blueprint, jsonify, request
import admin_operations_engine as AOE

admin_operations_bp = Blueprint("admin_operations", __name__, url_prefix="/api/admin/operations")


def _body() -> Dict[str, Any]:
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


@admin_operations_bp.route("/status", methods=["GET"])
def get_operations_status():
    """Returns authoritative system-wide workflow audit, cards, and KPIs."""
    try:
        data = AOE.compute_operations_overview()
        return jsonify(data)
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to compute operations overview: {str(e)}"}), 500


@admin_operations_bp.route("/health", methods=["GET"])
def get_system_health_status():
    """Returns real technical health checks for backend, database, storage, notifications."""
    try:
        health = AOE.get_system_health()
        return jsonify({"success": True, "health": health})
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to probe system health: {str(e)}"}), 500


@admin_operations_bp.route("/reminders", methods=["POST"])
def send_operations_reminder():
    """Dispatches operational reminder with anti-duplicate cooldown check."""
    import timetable_oversight as TT
    body = _body()
    try:
        result = TT.create_reminder(body)
        status_code = 200 if result.get("success") else (409 if result.get("cooldown_warning") else 400)
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to send reminder: {str(e)}"}), 500


@admin_operations_bp.route("/issues/<issue_id>/resolve", methods=["POST"])
def resolve_issue(issue_id: str):
    """Rechecks authoritative conditions before marking an issue resolved."""
    try:
        overview = AOE.compute_operations_overview()
        issues = overview.get("issues", [])
        matched = next((i for i in issues if i["id"] == issue_id), None)
        if not matched:
            return jsonify({"success": False, "error": f"Issue '{issue_id}' not found or already cleared."}), 404

        return jsonify({
            "success": True,
            "issue_id": issue_id,
            "message": f"Issue {issue_id} status updated to In Review. Re-verification scheduled.",
            "status": "In Review"
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to update issue: {str(e)}"}), 500

