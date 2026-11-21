"""
============================================================================
 Khmer School Admin Suite — REST API  (/api/timetable/*)
============================================================================
Thin, stateless HTTP layer over timetable_models.TimetableStore.  The browser
mirror (assets/js/khmer-suite-engine.js) implements the same derived logic so
all interactions are optimistic and work even when the server is unavailable.

Conventions
-----------
* Every mutating endpoint returns the canonical `state` plus derived `stats`,
  so the client can reconcile in one round trip.
* Counts are always computed by the model, never supplied by the caller.
* Exports are real .xlsx files with Khmer headers (timetable_xlsx.py).
============================================================================
"""

from __future__ import annotations

import io
import json
import time
import uuid
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

from flask import Blueprint, Response, jsonify, request

import timetable_models as M
from timetable_xlsx import Workbook, build_xlsx, read_xlsx

timetable_bp = Blueprint("timetable", __name__, url_prefix="/api/timetable")

STORE = M.STORE
XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

# Short-lived AI proposals, keyed by an opaque token (Phase 2 stub).
_PROPOSALS: Dict[str, Dict[str, Any]] = {}
_PROPOSAL_TTL = 900  # seconds


# ── helpers ────────────────────────────────────────────────────────────────

def _body() -> Dict[str, Any]:
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def _ok(state: Optional[Dict[str, Any]] = None, **extra: Any) -> Response:
    state = state if state is not None else STORE.state()
    payload: Dict[str, Any] = {
        "success": True,
        "state": state,
        "stats": M.statistics(state),
        "revision": state.get("revision", 0),
        "updated_at": state.get("updated_at"),
    }
    payload.update(extra)
    return jsonify(payload)


def _fail(message_kh: str, status: int = 400, **extra: Any) -> Tuple[Response, int]:
    payload = {"success": False, "error": message_kh, "message": message_kh}
    payload.update(extra)
    return jsonify(payload), status


def _indexed(items: List[Dict[str, Any]], key: str = "id") -> Dict[str, Dict[str, Any]]:
    return {item[key]: item for item in items}


def _actor() -> Optional[str]:
    """Authenticated actor name for audit trails (X-Actor header, set by the
    front-end from the logged-in user)."""
    return (request.headers.get("X-Actor") or "").strip() or None


MONITOR_ROLES = {"admin", "principal", "editor", "super_admin", "superadmin"}
TIMETABLE_EDIT_ROLES = {"admin", "principal", "editor", "super_admin", "superadmin"}
TIMETABLE_PUBLISH_ROLES = {"admin", "super_admin", "superadmin"}


def _resolved_actor_role() -> str:
    role = (request.headers.get("X-Actor-Role") or request.headers.get("X-User-Role") or "").strip().lower()
    if not role:
        auth_hdr = (request.headers.get("Authorization") or "").strip()
        if "mock-jwt-token-" in auth_hdr:
            role = auth_hdr.split("mock-jwt-token-")[-1].strip().lower()
    return role


def _monitor_guard() -> Optional[Tuple[Response, int]]:
    """Backend authorization for monitoring endpoints: only administrative
    roles may read monitoring data or dispatch reminders. Never rely on
    hidden buttons alone."""
    role = _resolved_actor_role()
    if role and role not in MONITOR_ROLES:
        return _fail("សូមទោស — មានត្រណមតែ Admin/Principal ប៉ុណ្ណោះ", 403)
    return None


def _builder_write_guard() -> Optional[Tuple[Response, int]]:
    """Allow authorized academic leaders (Principal, Admin, Super Admin)
    to draft, edit, and manage timetable assignments."""
    role = _resolved_actor_role()
    if role and role not in TIMETABLE_EDIT_ROLES:
        return _fail(
            "Timetable draft editing requires Principal, Admin or Super Admin authorization.",
            403,
            read_only=True,
        )
    return None


def _builder_publish_guard() -> Optional[Tuple[Response, int]]:
    """Final timetable review and publishing is strictly reserved for Admin
    and Super Admin, ensuring executive oversight over live school schedules."""
    from server import _academic_user
    user = _academic_user()
    if not user:
        return _fail("Sign in to review or publish timetables.", 401)
    if user.get("role") not in TIMETABLE_PUBLISH_ROLES:
        return _fail(
            "Final timetable publishing is restricted to Administration. Principals can submit drafts for approval.",
            403,
            publish_restricted=True,
        )
    return None


def _subject_write_guard() -> Optional[Tuple[Response, int]]:
    """Curriculum (subject directory) management guard.

    Unlike timetable drafting — which the read-only monitor guard keeps
    Principal-Portal-only — the subject directory is a curriculum-management
    function shared by Admin and Principal portals. Only administrative roles
    may create or modify subjects; students, teachers, staff and monitoring
    sessions are rejected server-side."""
    role = _resolved_actor_role()
    if role not in MONITOR_ROLES:
        return _fail(
            "Subject management requires Admin, Principal or Super Admin access.",
            403,
            role=role or None,
        )
    return None


@timetable_bp.route("/subjects", methods=["POST"])
def create_subject():
    """Create a subject (+ optional per-class teacher assignments) in the
    authoritative timetable state document. Same store, same file — no
    parallel subject database."""
    denied = _subject_write_guard()
    if denied:
        return denied
    body = _body()
    try:
        result = STORE.add_subject(body.get("subject") or {},
                                   body.get("assignments") or [], actor=_actor())
    except M.SubjectValidationError as exc:
        return _fail(str(exc), 400)
    return _ok(result["state"], saved=True, subject=result["subject"],
               assignments=result["assignments"])


@timetable_bp.route("/subjects/<subject_id>", methods=["DELETE"])
def remove_subject(subject_id: str):
    """Delete a subject (mirrors the existing client-side delete semantics)."""
    denied = _subject_write_guard()
    if denied:
        return denied
    try:
        result = STORE.delete_subject(subject_id, actor=_actor())
    except LookupError as exc:
        return _fail(str(exc), 404)
    return _ok(result["state"], saved=True, subject=result["subject"],
               grid_cells_removed=result["grid_cells_removed"])


@timetable_bp.route("/subjects/<subject_id>", methods=["PUT"])
def update_subject(subject_id: str):
    """Update subject fields and reconcile class assignments (grid-protected)."""
    denied = _subject_write_guard()
    if denied:
        return denied
    body = _body()
    try:
        result = STORE.update_subject(subject_id, body.get("subject") or {},
                                      body.get("assignments"), actor=_actor())
    except M.SubjectValidationError as exc:
        return _fail(str(exc), 400)
    except LookupError as exc:
        return _fail(str(exc), 404)
    return _ok(result["state"], saved=True, subject=result["subject"],
               added=result["added"], removed=result["removed"],
               warnings=result["warnings"])


def _next_id(prefix: str, items: List[Dict[str, Any]], field: str = "id") -> str:
    used = {str(i.get(field, "")) for i in items}
    n = 1
    while f"{prefix}{n}" in used:
        n += 1
    return f"{prefix}{n}"


def _validate_state(state: Any) -> Optional[str]:
    if not isinstance(state, dict):
        return "ទិន្នន័យមិនត្រឹមត្រូវ (state must be an object)"
    required = ("subjects", "teachers", "classes", "assignments", "grid", "settings")
    for key in required:
        if key not in state:
            return f"បាត់ផ្នែកទិន្នន័យ៖ {key}"
        if not isinstance(state[key], (dict, list)):
            return f"ផ្នែកទិន្នន័យមិនត្រឹមត្រូវ៖ {key}"
    if not isinstance(state["grid"], dict):
        return "តារាងម៉ោងមិនត្រឹមត្រូវ"
    if len(state["grid"]) > 20000:
        return "តារាងម៉ោងធំពេក"
    for key in state["grid"]:
        if not isinstance(key, str) or len(key.split("|")) != 4:
            return f"កូដក្រឡាមិនត្រឹមត្រូវ៖ {key}"
    return None


def _clean_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """Only persist known domain keys; never trust client-supplied metadata."""
    base = STORE.state()
    for key in ("institution", "settings", "subjects", "teachers", "classes",
                "assignments", "grid", "records"):
        if key in state:
            base[key] = state[key]
    base.setdefault("history", [])
    return base


def _cell_view(state: Dict[str, Any], key: str, cell: Dict[str, Any]) -> Dict[str, Any]:
    subjects = _indexed(state["subjects"])
    teachers = _indexed(state["teachers"])
    subject = subjects.get(cell.get("subject_id"), {})
    teacher = teachers.get(cell.get("teacher_id"), {})
    return {
        "key": key,
        **cell,
        "subject_name": subject.get("name_kh", ""),
        "subject_code": subject.get("code", ""),
        "short_name": subject.get("short_name", ""),
        "color": subject.get("color", "#E5E7EB"),
        "teacher_code": teacher.get("code", ""),
        "teacher_name": teacher.get("name_kh", ""),
    }


def _state_grid_view(state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {k: _cell_view(state, k, v) for k, v in state["grid"].items()}


# ── state / history ────────────────────────────────────────────────────────

@timetable_bp.route("/health", methods=["GET"])
def health():
    state = STORE.state()
    return jsonify({
        "success": True, "service": "khmer-school-admin-suite",
        "revision": state.get("revision", 0),
        "classes": len(state["classes"]), "subjects": len(state["subjects"]),
        "teachers": len(state["teachers"]), "grid_cells": len(state["grid"]),
    })


@timetable_bp.route("/state", methods=["GET"])
def get_state():
    state = STORE.state()
    return _ok(state, history=STORE.history(), grid_view=_state_grid_view(state))


@timetable_bp.route("/data", methods=["GET"])
def get_data_legacy():
    """Compatibility alias used by the previous static mock pages."""
    state = STORE.state()
    return jsonify({
        "success": True, "data": state,
        "stats": M.statistics(state), "grid_view": _state_grid_view(state),
    })


@timetable_bp.route("/state", methods=["PUT", "POST"])
def put_state():
    """Autosave: replace the whole document, then re-derive every counter.

    Send `base_revision` to enable the concurrent-editor guard: the save is
    rejected with 409 when the server document has moved on, so a stale editor
    can never silently overwrite another editor's work.
    """
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    incoming = body.get("state", body)
    error = _validate_state(incoming)
    if error:
        return _fail(error)
    state = _clean_state(deepcopy(incoming))
    base_revision = body.get("base_revision")
    try:
        saved = STORE.replace(state, body.get("label", "រក្សាទុកដោយស្វ័យប្រវត្តិ"),
                              base_revision=base_revision, actor=_actor())
    except M.RevisionConflict as exc:
        return jsonify({
            "success": False, "error": "save-conflict",
            "message": "Another editor saved a newer version of this draft.",
            "current_revision": exc.current_revision,
        }), 409
    return _ok(saved, saved=True)


@timetable_bp.route("/reset", methods=["POST"])
def reset_state():
    denied = _builder_write_guard()
    if denied:
        return denied
    state = STORE.reset()
    return _ok(state, reset=True)


@timetable_bp.route("/history", methods=["GET"])
def get_history():
    return jsonify({"success": True, "history": STORE.history()})


@timetable_bp.route("/statistics", methods=["GET"])
def get_statistics():
    state = STORE.state()
    return jsonify({
        "success": True, "stats": M.statistics(state),
        "conflicts": M.scan_conflicts(state),
    })


@timetable_bp.route("/chips", methods=["GET"])
def get_chips():
    state = STORE.state()
    class_id = request.args.get("class_id") or None
    return jsonify({
        "success": True,
        "chips": M.unassigned_chips(state, class_id),
        "stats": M.statistics(state),
    })


# ── grid cells ─────────────────────────────────────────────────────────────

@timetable_bp.route("/grid", methods=["GET"])
def get_grid():
    state = STORE.state()
    class_id = request.args.get("class_id")
    grid = _state_grid_view(state)
    if class_id:
        grid = {k: v for k, v in grid.items() if v.get("class_id") == class_id}
    return jsonify({"success": True, "grid": grid, "state": state, "stats": M.statistics(state)})


@timetable_bp.route("/cells", methods=["POST"])
@timetable_bp.route("/grid/assign", methods=["POST"])
def assign_cell():
    """Place (or replace) one lesson. Hard conflicts block unless force=true."""
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    key = body.get("key")
    subject_id = body.get("subject_id")
    teacher_id = body.get("teacher_id")
    if not key or not subject_id or not teacher_id:
        return _fail("សូមបញ្ចូល ក្រឡា / មុខវិជ្ជា / គ្រូបង្រៀន")
    try:
        M.parse_grid_key(key)
    except (ValueError, TypeError):
        return _fail("កូដក្រឡាមិនត្រឹមត្រូវ")

    state = STORE.state()
    replace = bool(body.get("replace"))
    conflicts = M.validate_placement(state, key, subject_id, teacher_id, replace=replace)
    errors = [c for c in conflicts if c["severity"] == "error"]
    if errors and not body.get("force"):
        return _fail(errors[0]["message_kh"], 409, conflicts=conflicts, blocked=True)

    parts = M.parse_grid_key(key)
    cell = {
        "class_id": parts["class_id"], "subject_id": subject_id,
        "teacher_id": teacher_id, "day": parts["day"],
        "shift": parts["shift"], "period": parts["period"],
    }
    saved = STORE.patch_grid(key, cell, body.get("label", "កំណត់ម៉ោង"), actor=_actor())
    return _ok(saved, conflicts=conflicts, cell=_cell_view(saved, key, cell))


@timetable_bp.route("/cells", methods=["DELETE"])
@timetable_bp.route("/grid/clear", methods=["POST"])
def clear_cell():
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    key = body.get("key") or request.args.get("key")
    if not key:
        return _fail("សូមបញ្ចូលកូដក្រឡា")
    state = STORE.state()
    if key not in state["grid"]:
        return _ok(state, cleared=False)
    saved = STORE.patch_grid(key, None, body.get("label", "លុបម៉ោង"), actor=_actor())
    return _ok(saved, cleared=True)


@timetable_bp.route("/cells/batch", methods=["POST"])
def batch_cells():
    """Atomic multi-cell patch used by undo / AI apply / drag edits."""
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    changes = body.get("changes")
    if not isinstance(changes, list) or len(changes) > 5000:
        return _fail("បញ្ជីប្តូរមិនត្រឹមត្រូវ")
    state = STORE.state()
    for change in changes:
        if not isinstance(change, dict) or "key" not in change:
            return _fail("បញ្ជីប្តូរមិនត្រឹមត្រូវ")
        key = change["key"]
        if not isinstance(key, str) or len(key.split("|")) != 4:
            return _fail(f"កូដក្រឡាមិនត្រឹមត្រូវ៖ {key}")
        value = change.get("cell")
        if value is None:
            state["grid"].pop(key, None)
        else:
            parts = M.parse_grid_key(key)
            state["grid"][key] = {
                "class_id": parts["class_id"],
                "subject_id": value.get("subject_id"),
                "teacher_id": value.get("teacher_id"),
                "day": parts["day"], "shift": parts["shift"],
                "period": parts["period"],
            }
    saved = STORE.replace(state, body.get("label", "កែប្រែច្រើនក្រឡា"), actor=_actor())
    return _ok(saved, changed=len(changes))


# ── conflict engine ────────────────────────────────────────────────────────

@timetable_bp.route("/conflicts", methods=["GET"])
def list_conflicts():
    state = STORE.state()
    found = M.scan_conflicts(state)
    return jsonify({
        "success": True, "conflicts": found,
        "error_count": len([c for c in found if c["severity"] == "error"]),
        "warning_count": len([c for c in found if c["severity"] == "warning"]),
    })


@timetable_bp.route("/conflicts/check", methods=["POST"])
def check_conflicts():
    body = _body()
    state = STORE.state()
    if body.get("grid"):
        candidate = deepcopy(state)
        candidate["grid"] = body["grid"]
        return jsonify({"success": True, "conflicts": M.scan_conflicts(candidate),
                        "stats": M.statistics(candidate)})
    key = body.get("key")
    if not key:
        return _fail("សូមបញ្ចូលកូដក្រឡា")
    conflicts = M.validate_placement(
        state, key, body.get("subject_id", ""), body.get("teacher_id", ""),
        replace=bool(body.get("replace")),
    )
    return jsonify({
        "success": True, "conflicts": conflicts,
        "blocked": any(c["severity"] == "error" for c in conflicts),
    })


@timetable_bp.route("/candidates", methods=["GET"])
def teacher_candidates():
    """Ranked teacher picker list: availability, workload, subject match."""
    state = STORE.state()
    key = request.args.get("key", "")
    subject_id = request.args.get("subject_id", "")
    query = (request.args.get("q") or "").strip().lower()
    parts = M.parse_grid_key(key) if key and len(key.split("|")) == 4 else {}
    shift = parts.get("shift", "")
    load = M.teacher_load(state)
    subjects = _indexed(state["subjects"])
    classes = {c["id"]: c["display"] for c in state["classes"]}

    results = []
    for teacher in state["teachers"]:
        if subject_id and teacher["subject_id"] != subject_id:
            continue
        if query and query not in teacher["code"].lower() \
                and query not in teacher["name_kh"].lower() \
                and query not in str(teacher.get("subject_id", "")).lower():
            continue
        used = load.get(teacher["id"], 0)
        target = teacher["target"]
        shift_ok = not shift or shift in teacher.get("shifts", M.SHIFTS)
        busy = False
        for other_key, cell in state["grid"].items():
            if other_key == key or cell.get("teacher_id") != teacher["id"]:
                continue
            p = M.parse_grid_key(other_key)
            if (p["day"] == parts.get("day") and p["shift"] == parts.get("shift")
                    and p["period"] == parts.get("period")):
                busy = True
                break
        score = (100 if busy else 0) + (60 if not shift_ok else 0) \
            - max(0, target - used) + (80 if used >= target else 0)
        results.append({
            "id": teacher["id"], "code": teacher["code"],
            "name_kh": teacher["name_kh"], "name": teacher["name_kh"],
            "subject_id": teacher["subject_id"],
            "subject_code": subjects.get(teacher["subject_id"], {}).get("code", ""),
            "color": subjects.get(teacher["subject_id"], {}).get("color", "#E5E7EB"),
            "assigned": used, "target": target, "remaining": max(0, target - used),
            "shifts": teacher.get("shifts", M.SHIFTS),
            "shift_ok": shift_ok, "busy": busy,
            "available": not busy and shift_ok and used < target,
            "status_kh": "កំពុងគូររៀង" if busy else ("សេរី" if used < target else "ពេញបន្ទុក"),
            "class_hint": classes.get(teacher.get("homeroom_class_id", ""), ""),
            "score": score,
        })
    results.sort(key=lambda r: (r["score"], r["code"]))
    return jsonify({"success": True, "candidates": results, "count": len(results)})


# ── auto-assign / AI stub ──────────────────────────────────────────────────

@timetable_bp.route("/auto-assign", methods=["POST"])
@timetable_bp.route("/generate", methods=["POST"])
def auto_assign():
    """
    Greedy backtracking fill.  When `preview` is true (AI button) the proposed
    grid is returned as a diff without being committed; otherwise it is saved.
    """
    body = _body()
    state = STORE.state()
    preview = bool(body.get("preview")) or body.get("mode") == "preview"
    if not preview:
        denied = _builder_write_guard()
        if denied:
            return denied
    constraints = body.get("constraints") or {}

    working = deepcopy(state)
    for teacher in working["teachers"]:
        if "workload" in constraints:
            try:
                teacher["target"] = max(1, int(constraints["workload"]))
            except (TypeError, ValueError):
                pass
    locked = constraints.get("locked_subjects")
    if isinstance(locked, list):
        locked_ids = set(locked)
        for subject in working["subjects"]:
            subject["is_locked"] = subject["id"] in locked_ids or subject["code"] in locked_ids

    result = M.auto_assign(
        working,
        class_id=body.get("class_id") or None,
        clear_first=bool(body.get("clear_first")),
        seed=int(body.get("seed") or 7),
    )
    proposed = result["state"]
    diff = result["diff"]
    proposal_grid = {k: _cell_view(proposed, k, v) for k, v in proposed["grid"].items()}

    if preview:
        token = uuid.uuid4().hex[:16]
        _PROPOSALS[token] = {"state": proposed, "at": time.time()}
        for old in [t for t, p in _PROPOSALS.items() if time.time() - p["at"] > _PROPOSAL_TTL]:
            _PROPOSALS.pop(old, None)
        return jsonify({
            "success": True, "mode": "preview", "token": token,
            "proposed_grid": proposal_grid, "diff": diff,
            "placed": result["placed"], "requested": result["requested"],
            "skipped": result["skipped"], "nodes": result["nodes"],
            "stats": M.statistics(proposed),
            "conflicts": M.scan_conflicts(proposed),
            "summary_kh": f"AI ស្នើដាក់ {M.khmer_number(result['placed'])} ម៉ោង · "
                          f"នៅសល់ {M.khmer_number(M.statistics(proposed)['unassigned'])} ម៉ោង",
        })

    saved = STORE.replace(proposed, body.get("label", "បង្កើតកាលវិភាគដោយស្វ័យប្រវត្តិ"))
    return _ok(saved, placed=result["placed"], requested=result["requested"],
               diff=diff, skipped=result["skipped"], nodes=result["nodes"],
               mode="apply")


@timetable_bp.route("/generate/apply", methods=["POST"])
def apply_proposal():
    denied = _builder_write_guard()
    if denied:
        return denied
    token = _body().get("token", "")
    proposal = _PROPOSALS.pop(token, None)
    if not proposal or time.time() - proposal["at"] > _PROPOSAL_TTL:
        return _fail("សំណើផុតកំណត់ សូមបង្កើតម្តងទៀត", 410)
    saved = STORE.replace(proposal["state"], "អនុម័តសំណើ AI")
    return _ok(saved, applied=True)


# ── generic entity CRUD ────────────────────────────────────────────────────

def _collection(name: str, prefix: str, required: Tuple[str, ...],
                defaults: Dict[str, Any]) -> None:
    """Register CRUD routes for one top-level collection in `state`."""

    def all_items() -> Response:
        current = STORE.state()
        return jsonify({"success": True, name: current[name],
                        "count": len(current[name])})

    def create():
        body = _body()
        payload = body.get(name[:-1], body)
        if not isinstance(payload, dict):
            return _fail("ទិន្នន័យមិនត្រឹមត្រូវ")
        for field in required:
            if not payload.get(field):
                return _fail(f"សូមបញ្ចូល {field}")
        state = STORE.state()
        item = {**defaults, **payload}
        item.setdefault("id", _next_id(prefix, state[name]))
        if any(x["id"] == item["id"] for x in state[name]):
            return _fail("កូដនេះមានរួចហើយ", 409)
        state[name].append(item)
        saved = STORE.replace(state, f"បង្កើត {name}")
        return _ok(saved, item=item)

    def update(item_id: str):
        body = _body()
        payload = body.get(name[:-1], body)
        state = STORE.state()
        target = next((x for x in state[name] if x["id"] == item_id), None)
        if not target:
            return _fail("រកធាតុមិនឃើញ", 404)
        target.update({k: v for k, v in payload.items() if k != "id"})
        saved = STORE.replace(state, f"កែប្រែ {name}")
        return _ok(saved, item=target)

    def remove(item_id: str):
        state = STORE.state()
        before = len(state[name])
        state[name] = [x for x in state[name] if x["id"] != item_id]
        if len(state[name]) == before:
            return _fail("រកធាតុមិនឃើញ", 404)
        # Cascade: never leave dangling references in assignments / grid.
        field = {"subjects": "subject_id", "teachers": "teacher_id",
                 "classes": "class_id"}.get(name)
        if field:
            state["assignments"] = [a for a in state["assignments"]
                                    if a.get(field) != item_id]
            state["grid"] = {k: v for k, v in state["grid"].items()
                             if v.get(field) != item_id}
        saved = STORE.replace(state, f"លុប {name}")
        return _ok(saved, deleted=item_id)

    endpoint = f"collection_{name}"
    timetable_bp.add_url_rule(f"/{name}", endpoint + "_list", all_items, methods=["GET"])
    timetable_bp.add_url_rule(f"/{name}", endpoint + "_create", create, methods=["POST"])
    timetable_bp.add_url_rule(f"/{name}/<item_id>", endpoint + "_update", update,
                              methods=["PUT", "PATCH"])
    timetable_bp.add_url_rule(f"/{name}/<item_id>", endpoint + "_delete", remove,
                              methods=["DELETE"])


_collection("subjects", "sub_", ("name_kh", "code"), {
    "name_en": "", "short_name": "", "color": "#F7C948",
    "lessons_per_week": 2, "is_locked": False,
})
_collection("teachers", "t_", ("code", "name_kh", "subject_id"), {
    "name_en": "", "target": 17, "shifts": list(M.SHIFTS),
})
_collection("classes", "class_", ("display",), {
    "grade": 7, "section": "A", "shift": "ព្រឹក", "days": 6,
    "capacity": M.CLASS_CAPACITY,
})
_collection("assignments", "asg_", ("class_id", "subject_id", "teacher_id"), {
    "lessons": 2, "shift": "ព្រឹក",
})


@timetable_bp.route("/assignments/bulk", methods=["PUT"])
def bulk_assignments():
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    items = body.get("assignments")
    if not isinstance(items, list):
        return _fail("បញ្ជីទាត់ថ្នាក់មិនត្រឹមត្រូវ")
    state = STORE.state()
    state["assignments"] = items
    saved = STORE.replace(state, "រក្សាទុកការទាត់ថ្នាក់")
    return _ok(saved, count=len(items))


@timetable_bp.route("/institution", methods=["GET", "PUT"])
def institution():
    state = STORE.state()
    if request.method == "GET":
        return jsonify({"success": True, "institution": state["institution"]})
    body = _body()
    state["institution"].update(body.get("institution", body))
    return _ok(STORE.replace(state, "កែប្រែព័ត៌មានសាលា"))


@timetable_bp.route("/settings", methods=["GET", "PUT"])
def settings():
    state = STORE.state()
    if request.method == "GET":
        return jsonify({"success": True, "settings": state["settings"]})
    body = _body()
    state["settings"].update(body.get("settings", body))
    return _ok(STORE.replace(state, "កែប្រែការកំណត់"))


def _records_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    rows = state.get("records", [])
    teachers = [r for r in rows if r.get("type") == "គ្រូបង្រៀង"]
    return {
        "total": len(rows), "teachers": len(teachers),
        "students": len(rows) - len(teachers),
        "hours": sum(1 for _ in state["grid"].values()),
        "revenue_kh": "០", "amount_kh": "៥៩,១៥៥,២០០",
    }


@timetable_bp.route("/records", methods=["GET"])
def records():
    state = STORE.state()
    return jsonify({
        "success": True, "records": state.get("records", []),
        "columns": M.RECORD_COLUMNS,
        "summary": _records_summary(state),
    })


@timetable_bp.route("/records", methods=["PUT", "POST"])
def save_records():
    body = _body()
    rows = body.get("records")
    if not isinstance(rows, list):
        return _fail("បញ្ជីព័ត៌មានមិនត្រឹមត្រូវ")
    state = STORE.state()
    state["records"] = rows
    saved = STORE.replace(state, body.get("label", "រក្សាទុកព័ត៌មាន"))
    return _ok(saved, summary=_records_summary(saved), records=rows)


# ── Excel export ───────────────────────────────────────────────────────────

def _label(cell: Dict[str, Any]) -> str:
    return f"{cell.get('short_name') or cell.get('subject_name', '')} {cell.get('teacher_code', '')}".strip()


def _class_sheet(state: Dict[str, Any], cls: Dict[str, Any]) -> Any:
    days = state["settings"]["days"]
    periods = state["settings"]["periods"]
    view = _state_grid_view(state)
    s = Workbook().sheet(cls["display"], landscape=False, paper_size=9, freeze_rows=3)
    s.columns([15] + [17] * len(days))
    s.title(f"តារាងម៉ោងថ្នាក់ {cls['display']} · វេន{cls.get('shift', 'ព្រឹក')} · {cls.get('days', 6)}ថ្ងៃ",
            len(days) + 1)
    s.subtitle(f"{state['institution']['name_kh']} · {state['institution']['academic_year']}",
               len(days) + 1)
    s.headers(["ម៉ោង / ថ្ងៃ"] + list(days))
    for period in periods:
        row = [f"{period['shift']} {period['number']}  ({period['start']}–{period['end']})"]
        for day in days:
            key = M.grid_key(day, period["shift"], period["number"], cls["id"])
            row.append(_label(view[key]) if key in view else "— សេរី —")
        s.add(row)
        for col, day in enumerate(days, 2):
            key = M.grid_key(day, period["shift"], period["number"], cls["id"])
            if key in view:
                s.cell_fill(len(s.rows), col, view[key]["color"])
    s.blank()
    s.add(["ចំណាំ៖ ពណ៌ក្រឡាតំណាងឱ្យមុខវិជ្ជា · ក្រឡាទំនេរ = ម៉ោងសេរី"], align="left")
    return s


def _master_sheet(state: Dict[str, Any]) -> Any:
    """Full matrix: rows = classes, columns = day × period (60 columns)."""
    days = state["settings"]["days"]
    periods = state["settings"]["periods"]
    view = _state_grid_view(state)
    cols = 1 + len(days) * len(periods)
    s = Workbook().sheet("ម៉ាទ្រីសគ្រប់ថ្នាក់", landscape=True, paper_size=8, freeze_rows=3)
    s.columns([11] + [13] * (cols - 1))
    s.title("ម៉ាទ្រីសកាលវិភាគគ្រប់ថ្នាក់", cols)
    s.subtitle(f"{state['institution']['academic_year']} · សរុប {M.khmer_number(len(state['grid']))} ម៉ោង", cols)
    s.headers(["ថ្នាក់"] + [f"{d} · {p['shift']} {p['number']}"
                            for d in days for p in periods])
    for cls in state["classes"]:
        row = [cls["display"]]
        for day in days:
            for period in periods:
                key = M.grid_key(day, period["shift"], period["number"], cls["id"])
                row.append(f"{view[key]['teacher_code']} {view[key]['short_name']}" if key in view else "")
        s.add(row)
        col = 2
        for day in days:
            for period in periods:
                key = M.grid_key(day, period["shift"], period["number"], cls["id"])
                if key in view:
                    s.cell_fill(len(s.rows), col, view[key]["color"])
                col += 1
    return s


def _records_sheet(state: Dict[str, Any]) -> Any:
    columns = M.RECORD_COLUMNS + [{"key": "type", "kh": "ប្រភេទ", "en": "Type"}]
    rows = state.get("records", [])
    s = Workbook().sheet("ព័ត៌មាន", landscape=True, paper_size=8, freeze_rows=3)
    s.columns([7, 26, 8, 20, 8, 12, 20, 24, 14, 14, 20, 24, 16])
    s.title(f"បញ្ជីព័ត៌មានគ្រូបង្រៀន / សិស្ស · {state['institution']['academic_year']}", len(columns))
    summary = _records_summary(state)
    s.subtitle(f"គ្រូបង្រៀងបាន {M.khmer_number(summary['teachers'])} នាក់ · "
               f"{M.khmer_number(summary['hours'])} ម៉ោង/សប្តាហ៍ · "
               f"ទឹកប្រាក់ {summary['amount_kh']}", len(columns))
    s.headers([c["kh"] for c in columns])
    for row in rows:
        s.add([row.get(c["key"], "") for c in columns])
    return s


def _subjects_sheet(state: Dict[str, Any]) -> Any:
    s = Workbook().sheet("មុខវិជ្ជា", landscape=False, paper_size=9, freeze_rows=3)
    s.columns([7, 26, 18, 10, 14, 18, 14])
    s.title("បញ្ជីមុខវិជ្ជា", 7)
    s.subtitle("មុខវិជ្ជាដែលចាក់សោ មិនត្រូវបានដាក់ដោយស្វ័យប្រវត្តិទេ", 7)
    s.headers(["ល.រ", "ឈ្មោះមុខវិជ្ជា", "ឈ្មោះខ្លី", "កូដ", "ពណ៌",
               "ចំនួន/សប្តាហ៍", "ចាក់សោ"])
    for i, sub in enumerate(state["subjects"], 1):
        s.add([i, sub["name_kh"], sub["short_name"], sub["code"],
               sub["color"], sub["lessons_per_week"],
               "បាទ/ចាស" if sub.get("is_locked") else "ទេ"])
        s.cell_fill(len(s.rows), 5, sub["color"])
    return s


def _teachers_sheet(state: Dict[str, Any]) -> Any:
    load = M.teacher_load(state)
    subjects = _indexed(state["subjects"])
    s = Workbook().sheet("គ្រូបង្រៀង", landscape=False, paper_size=9, freeze_rows=3)
    s.columns([7, 12, 26, 14, 18, 16, 18])
    s.title("បញ្ជីគ្រូបង្រៀង និងបន្ទុកម៉ោង", 7)
    s.subtitle("បន្ទុក / គោលដៅ ម៉ោងក្នុងមួយសប្តាហ៍", 7)
    s.headers(["ល.រ", "កូដ", "គោត្តនាម-នាម", "មុខវិជ្ជា", "គោលដៅ",
               "បានដាក់", "វេន"])
    for i, t in enumerate(state["teachers"], 1):
        s.add([i, t["code"], t["name_kh"],
               subjects.get(t["subject_id"], {}).get("name_kh", ""),
               t["target"], load.get(t["id"], 0),
               " · ".join(t.get("shifts", []))])
        s.cell_fill(len(s.rows), 4, subjects.get(t["subject_id"], {}).get("color", "#FFFFFF"))
        if load.get(t["id"], 0) > t["target"]:
            s.cell_fill(len(s.rows), 6, "#FCA5A5", bold=True)
    return s


def _export_workbook(state: Dict[str, Any], kind: str,
                     class_id: Optional[str] = None) -> bytes:
    wb = Workbook()
    classes = [c for c in state["classes"] if not class_id or c["id"] == class_id] \
        or state["classes"]
    if kind in ("timetable", "all"):
        for cls in classes:
            wb.sheets.append(_class_sheet(state, cls))
    if kind in ("master", "all"):
        wb.sheets.append(_master_sheet(state))
    if kind in ("records", "all"):
        wb.sheets.append(_records_sheet(state))
    if kind in ("subjects", "all"):
        wb.sheets.append(_subjects_sheet(state))
    if kind in ("teachers", "all"):
        wb.sheets.append(_teachers_sheet(state))
    if kind == "unassigned":
        s = Workbook().sheet("មិនទាន់តម្រៀប", freeze_rows=2)
        s.columns([12, 22, 14, 22, 16])
        s.title("មេរៀនដែលមិនទាន់តម្រៀប", 5)
        s.headers(["ថ្នាក់", "មុខវិជ្ជា", "កូដគ្រូ", "ឈ្មោះគ្រូ", "ចំនួន"])
        cls_map = {c["id"]: c["display"] for c in state["classes"]}
        for chip in M.unassigned_chips(state, class_id):
            s.add([cls_map.get(chip["class_id"], chip["class_id"]),
                   chip["subject_name"], chip["teacher_code"],
                   chip["teacher_name"], chip["count"]])
            s.cell_fill(len(s.rows), 2, chip["color"])
        wb.sheets.append(s)
    if not wb.sheets:
        wb.sheets.append(_subjects_sheet(state))
    return wb.bytes()


@timetable_bp.route("/export", methods=["GET", "POST"])
def export_xlsx():
    """Real .xlsx with Khmer headers. ?type=all|timetable|master|records|subjects|teachers|unassigned"""
    args = request.args if request.method == "GET" else _body()
    if args.get("format") == "json":
        state = STORE.state()
        return jsonify({"success": True, "data": state,
                        "stats": M.statistics(state)})
    kind = args.get("type") or args.get("format") or "all"
    if kind not in ("all", "timetable", "master", "records", "subjects",
                    "teachers", "unassigned"):
        kind = "all"
    class_id = args.get("class_id") or None
    state = STORE.state()
    if class_id and any(c["id"] == class_id for c in state["classes"]):
        display = next(c["display"] for c in state["classes"] if c["id"] == class_id)
        filename = f"តារាងម៉ោង_{display}_{datetime.now():%Y%m%d}.xlsx"
    else:
        filename = f"ការគ្រប់គ្រងសាលា_{kind}_{datetime.now():%Y%m%d}.xlsx"
    data = _export_workbook(state, kind, class_id)
    return Response(
        data, mimetype=XLSX_MIME,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename, safe='')}",
            "Content-Length": str(len(data)),
            "Cache-Control": "no-store",
        },
    )


# ── Excel / CSV / JSON import ──────────────────────────────────────────────

_HEADER_ALIASES: Dict[str, str] = {c["kh"]: c["key"] for c in M.RECORD_COLUMNS}
_HEADER_ALIASES.update({c["en"].lower(): c["key"] for c in M.RECORD_COLUMNS})
_HEADER_ALIASES.update({
    "លេខរៀង": "no", "no.": "no", "no": "no", "full name": "name",
    "ឈ្មោះ": "name", "gender": "gender",
    "ប្រភេទ": "type", "type": "type",
})


@timetable_bp.route("/import", methods=["POST"])
def import_records():
    """Import staff/student rows from .xlsx, .csv, .tsv or JSON."""
    state = STORE.state()
    rows: List[List[str]] = []
    if request.files and "file" in request.files:
        uploaded = request.files["file"]
        raw = uploaded.read()
        name = (uploaded.filename or "").lower()
        if name.endswith((".xlsx", ".xlsm")):
            rows = read_xlsx(raw)
        elif name.endswith((".csv", ".tsv")):
            import csv
            delimiter = "\t" if name.endswith(".tsv") else ","
            text = raw.decode("utf-8-sig", errors="replace")
            rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
        elif name.endswith(".json"):
            payload = json.loads(raw.decode("utf-8-sig"))
            records = payload.get("records", payload) if isinstance(payload, dict) else payload
            if isinstance(records, list) and all(isinstance(r, dict) for r in records):
                state["records"] = records
                saved = STORE.replace(state, "បញ្ចូលទិន្នន័យ JSON")
                return _ok(saved, imported=len(records))
    else:
        body = _body()
        if isinstance(body.get("rows"), list):
            rows = body["rows"]
        elif isinstance(body.get("records"), list) and all(
                isinstance(r, dict) for r in body["records"]):
            state["records"] = body["records"]
            saved = STORE.replace(state, "បញ្ចូលទិន្នន័យ")
            return _ok(saved, imported=len(body["records"]))

    if not rows:
        return _fail("ឯកសារទទេ ឬទម្រង់មិនគាំទ្រ")

    header_index = 0
    for i, row in enumerate(rows[:8]):
        joined = " ".join(str(v) for v in row)
        if any(label in joined for label in ("គោត្តនាម", "ល.រ", "Full name")):
            header_index = i
            break
    headers = [str(h).strip() for h in rows[header_index]]
    keys = [_HEADER_ALIASES.get(h.lower(), _HEADER_ALIASES.get(h, "")) for h in headers]
    imported: List[Dict[str, Any]] = []
    for raw_row in rows[header_index + 1:]:
        if not any(str(v).strip() for v in raw_row):
            continue
        item: Dict[str, Any] = {"type": "សិស្ស"}
        for i, key in enumerate(keys):
            if key:
                item[key] = str(raw_row[i]).strip() if i < len(raw_row) else ""
        if not item.get("name"):
            item["name"] = str(raw_row[1]).strip() if len(raw_row) > 1 else ""
        if not item.get("name"):
            continue
        item.setdefault("no", len(imported) + 1)
        imported.append(item)

    mode = request.form.get("mode") or _body().get("mode") or "replace"
    if mode == "append":
        state["records"] = state.get("records", []) + imported
    else:
        state["records"] = imported
    saved = STORE.replace(state, f"បញ្ចូលទិន្នន័យ ({M.khmer_number(len(imported))} ជួរ)")
    return _ok(saved, imported=len(imported), headers=headers,
               summary=_records_summary(saved))


# ── Critical Reassignment Route (Section 8) ────────────────────────────────

@timetable_bp.route("/reassign", methods=["POST"])
def reassign():
    """Section 8 Critical Rule: safely reassign a teacher in a class."""
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    class_id = body.get("class_id")
    subject_id = body.get("subject_id")
    new_teacher_id = body.get("new_teacher_id")
    old_teacher_id = body.get("old_teacher_id")
    if not class_id or not subject_id or not new_teacher_id:
        return _fail("សូមបញ្ជាក់ ថ្នាក់, មុខវិជ្ជា, និងគ្រូថ្មី")
    try:
        result = STORE.reassign(class_id, subject_id, new_teacher_id, old_teacher_id)
        return _ok(result=result)
    except Exception as e:
        return _fail(str(e), 500)


# ── Draft & Approval Lifecycle ──────────────────────────────────────────────

@timetable_bp.route("/submit-approval", methods=["POST"])
def submit_approval():
    """Principal submits active draft timetable for Admin review and approval."""
    from server import _academic_user
    user = _academic_user()
    if not user:
        return _fail("Sign in to submit a timetable draft.", 401)
    if user.get("role") not in {"principal", *TIMETABLE_PUBLISH_ROLES}:
        return _fail("Principal or Administration access is required.", 403)
    body = _body()
    submitted_by = user.get("name") or " ".join(
        user.get(field, "") for field in ("firstName", "lastName")
    ).strip() or user["id"]
    note = body.get("note", "")
    effective_from = body.get("effective_from")
    try:
        result = STORE.submit_for_approval(submitted_by=submitted_by, note=note,
                                           effective_from=effective_from,
                                           base_revision=body.get("base_revision"))
        return _ok(submission=result)
    except M.RevisionConflict as exc:
        return _fail("The draft changed. Reload it before submitting.", 409,
                     current_revision=exc.current_revision)
    except Exception as e:
        return _fail(str(e), 400)


@timetable_bp.route("/approve-draft", methods=["POST"])
def approve_draft():
    """Admin approves a submitted draft timetable."""
    denied = _builder_publish_guard()
    if denied:
        return denied
    from server import _academic_user
    user = _academic_user()
    reviewed_by = user.get("name") or user.get("email") or user["id"]
    try:
        result = STORE.approve_draft(reviewed_by=reviewed_by)
        return _ok(approval=result)
    except Exception as e:
        return _fail(str(e), 400)


@timetable_bp.route("/request-revision", methods=["POST"])
@timetable_bp.route("/reject-draft", methods=["POST"])
def request_revision():
    """Admin requests revisions from the Principal on a submitted draft."""
    denied = _builder_publish_guard()
    if denied:
        return denied
    body = _body()
    from server import _academic_user
    user = _academic_user()
    reviewed_by = user.get("name") or user.get("email") or user["id"]
    note = str(body.get("note") or "").strip()
    if not note:
        return _fail("Enter a reason for returning or rejecting the draft.")
    try:
        result = STORE.request_revision(reviewed_by=reviewed_by, note=note,
                                        rejected=request.path.endswith("/reject-draft"))
        return _ok(revision=result)
    except Exception as e:
        return _fail(str(e), 400)


@timetable_bp.route("/draft-status", methods=["GET"])
def draft_status():
    """Return the current draft lifecycle status and audit metadata."""
    return _ok(draft_metadata=STORE.draft_metadata())


# ── Publishing & Downstream Portals (Section 18) ───────────────────────────

@timetable_bp.route("/publish", methods=["POST"])
def publish():
    """Section 18: Approve and publish active draft timetable.

    Hard conflicts always block. An incomplete timetable (unassigned required
    lessons) publishes only with an explicit `force: true` confirmation from
    the editor, per school policy.
    """
    denied = _builder_publish_guard()
    if denied:
        return denied
    body = _body()
    from server import _academic_user
    user = _academic_user()
    published_by = user.get("name") or user.get("email") or user["id"]
    note = body.get("note", "")
    effective_from = body.get("effective_from")
    force = bool(body.get("force"))
    state = STORE.state()
    if (state.get("draft_metadata") or {}).get("status") in {"submitted", "needs_revision", "rejected"}:
        return _fail("Approve the submitted draft before publishing.", 409)
    conflicts = [c for c in M.scan_conflicts(state) if c["severity"] == "error"]
    if conflicts:
        return _fail("មិនអាចបោះពុម្ពផ្សាយបានទេ ពីព្រោះមានជម្លោះកាលវិភាគ", 409, conflicts=conflicts)
    stats = M.statistics(state)
    unassigned = stats.get("unassigned", 0)
    if unassigned > 0 and not force:
        return jsonify({
            "success": False, "requires_confirmation": True,
            "error": "incomplete-timetable",
            "message": "កាលវិភាគមិនទាន់ពេញលេញ — សូមបញ្ជាក់មុនបោះពុម្ពផ្សាយ",
            "unassigned": unassigned,
        }), 409
    try:
        published = STORE.publish(published_by=published_by, note=note,
                                  effective_from=effective_from)
    except Exception as e:
        return _fail(str(e), 400)
    classes_affected = len(published.get("classes", []))
    teachers_affected = len({c.get("teacher_id") for c in published["grid"].values()
                             if c.get("teacher_id")})
    students_affected = sum(int(c.get("student_count") or 0)
                            for c in published.get("classes", []))
    return _ok(published=published, affected={
        "classes": classes_affected,
        "teachers": teachers_affected,
        "students": students_affected,
    })


@timetable_bp.route("/publication/status", methods=["GET"])
def publication_status():
    """Combined publication state for the sticky action bar & publish modal."""
    state = STORE.state()
    pub = state.get("published")
    stats = M.statistics(state)
    conflicts = [c for c in M.scan_conflicts(state) if c["severity"] == "error"]
    diff = M.diff_publication(state)
    return jsonify({
        "success": True,
        "revision": state.get("revision", 0),
        "updated_at": state.get("updated_at"),
        "institution": state.get("institution", {}),
        "stats": {k: stats.get(k) for k in ("placed", "total_demand", "unassigned", "conflicts")},
        "conflict_count": len(conflicts),
        "published": ({k: pub[k] for k in ("version", "published_at", "published_by",
                                           "effective_from", "note", "academic_year")}
                      if pub else None),
        "diff": {k: diff[k] for k in ("has_published", "changed", "added",
                                      "removed", "modified")},
        "history": STORE.publication_history(),
    })


@timetable_bp.route("/publication/diff", methods=["GET"])
def publication_diff():
    """Per-cell diff between the editable draft and the published snapshot."""
    diff = STORE.publication_diff()
    return jsonify({"success": True, "diff": diff})


@timetable_bp.route("/publication/rollback", methods=["POST"])
def publication_rollback():
    """Audited rollback: republish a previous version and rebase the draft."""
    denied = _builder_write_guard()
    if denied:
        return denied
    body = _body()
    version = body.get("version")
    actor = body.get("published_by", "Admin")
    if not isinstance(version, int):
        return _fail("`version` (int) is required", 400)
    try:
        snapshot = STORE.rollback(version, actor=actor)
    except ValueError as e:
        return _fail(str(e), 404)
    return _ok(published=snapshot, restored_from=version)


@timetable_bp.route("/published", methods=["GET"])
def get_published():
    """Return active published timetable metadata or 404."""
    pub = STORE.published()
    if not pub:
        return jsonify({"success": False, "published": None, "message": "មិនទាន់មានកាលវិភាគបោះពុម្ពផ្សាយនៅឡើយ"})
    return jsonify({"success": True, "published": pub})


@timetable_bp.route("/published/teacher/<teacher_id>", methods=["GET"])
def get_published_teacher(teacher_id: str):
    """Teacher portal read-only view of the published timetable.

    Returns 404 when nothing is published — the portal must never receive
    unpublished draft data as if it were the official schedule.
    """
    use_published = request.args.get("draft", "false").lower() != "true"
    if use_published and not STORE.published():
        return _fail("មិនទាន់មានកាលវិភាគបោះពុម្ពផ្សាយនៅឡើយទេ", 404)
    result = STORE.teacher_timetable(teacher_id, use_published=use_published)
    if not result.get("success"):
        return _fail(result.get("error", "រកគ្រូមិនឃើញ"), 404)
    return jsonify(result)


@timetable_bp.route("/published/class/<class_id>", methods=["GET"])
def get_published_class(class_id: str):
    """Student portal read-only view of the published timetable (404 if none)."""
    use_published = request.args.get("draft", "false").lower() != "true"
    if use_published and not STORE.published():
        return _fail("មិនទាន់មានកាលវិភាគបោះពុម្ពផ្សាយនៅឡើយទេ", 404)
    result = STORE.class_timetable(class_id, use_published=use_published)
    if not result.get("success"):
        return _fail(result.get("error", "រកថ្នាក់មិនឃើញ"), 404)
    return jsonify(result)


# ── Unavailability & Spreadsheet Bulk Import ───────────────────────────────

@timetable_bp.route("/unavailability", methods=["GET", "PUT"])
def handle_unavailability():
    state = STORE.state()
    if request.method == "GET":
        unavail = [
            {"teacher_id": t["id"], "code": t["code"], "name_kh": t["name_kh"], "slots": t.get("unavailable_slots", [])}
            for t in state["teachers"]
        ]
        return jsonify({"success": True, "unavailability": unavail})

    body = _body()
    teacher_id = body.get("teacher_id")
    slots = body.get("slots") if "slots" in body else body.get("unavailable_slots", [])
    target = next((t for t in state["teachers"] if t["id"] == teacher_id), None)
    if not target:
        return _fail("រកគ្រូមិនឃើញ", 404)
    target["unavailable_slots"] = slots if isinstance(slots, list) else []
    saved = STORE.replace(state, f"កំណត់ថ្ងៃឈប់សម្រាកគ្រូ {target['code']}")
    return _ok(saved, teacher_id=teacher_id, slots=target["unavailable_slots"])


@timetable_bp.route("/teachers/bulk-import", methods=["POST"])
def bulk_import_teachers():
    """Section 3.6: Safe teacher import from spreadsheet."""
    body = _body()
    rows = body.get("teachers", [])
    if not isinstance(rows, list) or not rows:
        return _fail("ទិន្នន័យគ្រូមិនត្រឹមត្រូវ")

    state = STORE.state()
    teachers = state["teachers"]
    by_id = {t["id"]: t for t in teachers}
    by_emp = {t.get("employee_id", "").strip(): t for t in teachers if t.get("employee_id")}
    by_code = {t["code"].strip(): t for t in teachers}

    updated_count = 0
    created_count = 0
    errors = []

    for i, r in enumerate(rows, 1):
        if not isinstance(r, dict):
            continue
        name = str(r.get("name_kh", r.get("name", ""))).strip()
        if not name:
            errors.append(f"ជួរទី {i}៖ បាត់ឈ្មោះគ្រូ")
            continue

        tid = str(r.get("id", "")).strip()
        empid = str(r.get("employee_id", "")).strip()
        code = str(r.get("code", "")).strip()

        # Match order: 1. internal ID, 2. employee ID, 3. code
        match = by_id.get(tid) or by_emp.get(empid) or by_code.get(code)

        if match:
            for k in ("name_kh", "name_en", "gender", "phone", "position", "category",
                      "rank", "specialization", "employee_id", "notes"):
                val = r.get(k)
                if val is not None and str(val).strip() != "":
                    match[k] = str(val).strip()
            if r.get("target") is not None:
                try: match["target"] = int(r["target"])
                except (ValueError, TypeError): pass
            if r.get("max_daily") is not None:
                try: match["max_daily"] = int(r["max_daily"])
                except (ValueError, TypeError): pass
            if r.get("start_year") is not None:
                try: match["start_year"] = int(r["start_year"])
                except (ValueError, TypeError): pass
            if code and code != match["code"]:
                match["code"] = code
                if code not in match.setdefault("codes", []):
                    match["codes"].append(code)
            updated_count += 1
        else:
            new_code = code or f"T{len(teachers) + 1}"
            new_id = tid or f"t_{new_code}"
            if new_id in by_id:
                new_id = M._next_id("t_", teachers)
            new_t = {
                "id": new_id,
                "code": new_code,
                "codes": [new_code],
                "name_kh": name,
                "name_en": str(r.get("name_en", "")).strip(),
                "gender": str(r.get("gender", "ប្រុស")).strip(),
                "phone": str(r.get("phone", "")).strip(),
                "position": str(r.get("position", "គ្រូបង្រៀន")).strip(),
                "category": str(r.get("category", "ក្របខ័ណ្ឌរដ្ឋ")).strip(),
                "rank": str(r.get("rank", "គ្រូកម្រិតឧត្តម")).strip(),
                "specialization": str(r.get("specialization", "ទូទៅ")).strip(),
                "subject_id": r.get("subject_id") or "sub_K",
                "subject_ids": [r.get("subject_id") or "sub_K"],
                "target": int(r.get("target", 17)),
                "max_daily": int(r.get("max_daily", 5)),
                "employee_id": empid or f"EMP-{2000 + len(teachers) + 1}",
                "start_year": int(r.get("start_year", 2024)),
                "notes": str(r.get("notes", "")).strip(),
                "shifts": list(M.SHIFTS),
                "unavailable_slots": [],
            }
            teachers.append(new_t)
            by_id[new_id] = new_t
            if new_t["employee_id"]:
                by_emp[new_t["employee_id"]] = new_t
            by_code[new_code] = new_t
            created_count += 1

    saved = STORE.replace(state, f"បញ្ចូលទិន្នន័យគ្រូ ({created_count} ថ្មី, {updated_count} កែប្រែ)")
    return _ok(saved, updated=updated_count, created=created_count, errors=errors)


# ── Oversight & Progress Monitoring ────────────────────────────────────────

@timetable_bp.route("/oversight/status", methods=["GET"])
def oversight_status():
    """Section 2: Authoritative timetable workflow status & monitoring metrics."""
    import timetable_oversight as O
    try:
        data = O.compute_oversight_data()
        return jsonify(data)
    except Exception as e:
        return _fail(f"បរាជ័យក្នុងការទាញយកទិន្នន័យ Oversight: {str(e)}", 500)


@timetable_bp.route("/reminders", methods=["GET"])
def get_reminders_list():
    """Section 8 & 9: List follow-up reminders and delivery statuses."""
    import timetable_oversight as O
    try:
        reminders = O.get_reminders()
        return jsonify({"success": True, "reminders": reminders})
    except Exception as e:
        return _fail(f"បរាជ័យក្នុងការទាញយក Reminder: {str(e)}", 500)


@timetable_bp.route("/reminders", methods=["POST"])
def send_reminder():
    """Section 8: Create and dispatch reminder notification with cooldown check."""
    import timetable_oversight as O
    body = _body()
    try:
        result = O.create_reminder(body)
        status_code = 200 if result.get("success") else (409 if result.get("cooldown_warning") else 400)
        return jsonify(result), status_code
    except Exception as e:
        return _fail(f"បរាជ័យក្នុងការផ្ញើ Reminder: {str(e)}", 500)


@timetable_bp.route("/reminders/<reminder_id>/read", methods=["POST", "PUT"])
def mark_reminder_as_read(reminder_id: str):
    """Section 9: Update reminder read status."""
    import timetable_oversight as O
    try:
        result = O.mark_reminder_read(reminder_id)
        return jsonify(result)
    except Exception as e:
        return _fail(f"បរាជ័យក្នុងការកែប្រែស្ថានភាព Reminder: {str(e)}", 500)


# ── Admin Timetable Monitoring (read-only oversight) ───────────────────────

@timetable_bp.route("/monitoring/classes", methods=["GET"])
def monitoring_classes():
    """Class-level timetable monitoring table.

    Starts from the authoritative class registry (left-join semantics), so
    classes with no timetable records surface as Not Started. All filtering,
    sorting and pagination happen server-side.
    """
    guard = _monitor_guard()
    if guard:
        return guard
    import timetable_monitoring as MON
    state = STORE.state()
    rows = MON.compute_class_rows(state)
    params = {
        "academic_year": request.args.get("academic_year", ""),
        "campus": request.args.get("campus", ""),
        "department": request.args.get("department", ""),
        "grade": request.args.get("grade", ""),
        "class_id": request.args.get("class_id", ""),
        "status": request.args.get("status", ""),
        "completion": request.args.get("completion", ""),
        "search": request.args.get("search", ""),
        "responsible": request.args.get("responsible", ""),
        "sort": request.args.get("sort", "attention"),
        "page": request.args.get("page", 1),
        "page_size": request.args.get("page_size", 10),
    }
    # Enforce campus restriction for campus-scoped roles (e.g. editor)
    user_campus = (request.headers.get("X-User-Campus") or "").strip()
    if user_campus and user_campus.upper() != "ALL" and not params["campus"]:
        params["campus"] = user_campus
    page_data = MON.filter_sort_page(rows, params)
    return jsonify({
        "success": True,
        "summary": MON.compute_summary(rows),
        "meta": MON.filter_options(state, rows),
        "rows": page_data["rows"],
        "pagination": {k: page_data[k] for k in ("total", "page", "page_size", "total_pages")},
    })


@timetable_bp.route("/monitoring/classes/<class_id>", methods=["GET"])
def monitoring_class_detail(class_id: str):
    """Read-only monitoring detail: preparation, publication, audit history
    and draft/published timetable previews. No editing is possible here."""
    guard = _monitor_guard()
    if guard:
        return guard
    import timetable_monitoring as MON
    detail = MON.class_detail(STORE.state(), class_id)
    if detail is None:
        return _fail("រកថ្នាក់មិនឃើញ", 404)
    return jsonify(detail)


@timetable_bp.route("/monitoring/classes/<class_id>/remind", methods=["POST"])
def monitoring_class_remind(class_id: str):
    """Send a follow-up reminder to the recorded timetable owner via the
    existing notification infrastructure (cooldown + audit included)."""
    guard = _monitor_guard()
    if guard:
        return guard
    import timetable_monitoring as MON
    import timetable_oversight as O
    state = STORE.state()
    rows = {r["class_id"]: r for r in MON.compute_class_rows(state)}
    row = rows.get(class_id)
    if row is None:
        return _fail("រកថ្នាក់មិនឃើញ", 404)

    body = _body()
    responsible = row.get("responsible") or dict(MON.TIMETABLE_OWNER)
    status_label = row["status_label"]
    missing_txt = (f"{row['missing_periods']} of {row['required_periods']} periods unplaced"
                   if row["required_periods"] else "timetable incomplete")
    if row["status"] == "not_started":
        missing_txt = "no timetable has been prepared yet"
    default_message = (f"Your timetable for {row['class_display']} has not been published. "
                       f"Please review and complete the timetable preparation process "
                       f"(status: {status_label}"
                       + (f", {missing_txt}" if row["status"] != "published" else "") + ").")

    actor_name = (request.headers.get("X-Actor") or "").strip() or "Admin"
    actor_email = (request.headers.get("X-Actor-Email") or "").strip()
    payload = {
        "recipient_id": responsible.get("id") or "PRIN-2024-001",
        "recipient_name": responsible.get("name") or "Dr. Ly Bunheng",
        "recipient_role": responsible.get("role") or "Principal",
        "recipient_email": responsible.get("email") or "principal@ngis.edu.kh",
        "task_id": f"task_sched_{class_id}",
        "task_name": f"Timetable Monitoring — {row['class_display']}",
        "campus": row["campus"],
        "academic_year": row["academic_year"] or "2026–2027",
        "missing_summary": missing_txt,
        "message": str(body.get("message") or default_message).strip(),
        "deadline": str(body.get("deadline") or "").strip(),
        "authorized_url": f"pages/principal/principal-timetable-builder.html?class={class_id}",
        "force_duplicate": bool(body.get("force_duplicate")),
        "sender_id": (request.headers.get("X-Actor-Id") or "").strip() or actor_email or "ADM-2024-001",
        "sender_name": actor_name,
    }
    result = O.create_reminder(payload)
    status_code = 200 if result.get("success") else (409 if result.get("cooldown_warning") else 400)
    if result.get("success"):
        result["class_id"] = class_id
        result["class_display"] = row["class_display"]
    return jsonify(result), status_code


@timetable_bp.route("/monitoring/export", methods=["GET"])
def monitoring_export():
    """CSV export of the monitoring table (authorized data only)."""
    guard = _monitor_guard()
    if guard:
        return guard
    import csv
    import io
    import timetable_monitoring as MON
    state = STORE.state()
    rows = MON.compute_class_rows(state)
    params = {
        "academic_year": request.args.get("academic_year", ""),
        "campus": request.args.get("campus", ""),
        "department": request.args.get("department", ""),
        "grade": request.args.get("grade", ""),
        "class_id": request.args.get("class_id", ""),
        "status": request.args.get("status", ""),
        "completion": request.args.get("completion", ""),
        "search": request.args.get("search", ""),
        "responsible": request.args.get("responsible", ""),
        "sort": request.args.get("sort", "attention"),
        "page": 1,
        "page_size": 100000,
    }
    rows = MON.filter_sort_page(rows, params)["rows"]

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Class", "Campus", "Department", "Responsible", "Role",
                     "Completion %", "Draft Status", "Publication Status",
                     "Required Periods", "Placed Periods", "Missing Periods",
                     "Last Edited By", "Last Edited", "Published By", "Published At",
                     "Published Version", "Effective From", "Conflicts"])
    for r in rows:
        writer.writerow([
            r["class_display"], r["campus"], r["department"],
            r["responsible_display"], r["responsible_role"],
            r["completion_pct"] if r["completion_pct"] is not None else "Not available",
            r["draft_status_label"],
            r["status_label"],
            r["required_periods"], r["placed_periods"],
            r["missing_periods"] if r["missing_periods"] is not None else "Not available",
            r["last_edited_by"] or "—",
            r["last_edited_at"] or "—",
            r["published_by"] or "—",
            r["published_at"] or "—",
            r["published_version"] or "—",
            r["effective_from"] or "—",
            r["conflicts_count"],
        ])
    data = "\ufeff" + buf.getvalue()  # UTF-8 BOM for Excel compatibility
    resp = Response(data, mimetype="text/csv")
    resp.headers["Content-Disposition"] = "attachment; filename=timetable-monitoring.csv"
    return resp

