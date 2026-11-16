"""
============================================================================
NGIS — Admin Timetable Monitoring Engine
============================================================================
Read-only monitoring of per-class timetable preparation and publication.

Design rules enforced here:
- The authoritative class registry (state["classes"]) is the starting point:
  classes with no timetable records surface as "not_started".
- Publication status comes ONLY from actual publication records
  (state["published"] snapshot), never inferred from grid cells.
- Completion is computed from real curriculum requirements
  (state["assignments"] lesson quotas); when no requirements exist the
  completion is reported as unavailable rather than invented.
- Editors are only reported when explicitly recorded (class_meta audit
  metadata or the class record's assigned_editor); never inferred from
  the class teacher.
============================================================================
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import timetable_models as M

# The recorded timetable owner in the school's oversight workflow
# (explicitly recorded responsibility — NOT inferred from class teachers).
TIMETABLE_OWNER = {
    "id": "PRIN-2024-001",
    "name": "Dr. Ly Bunheng",
    "role": "Principal",
    "email": "principal@ngis.edu.kh",
}

STATUS_LABELS = {
    "not_started": "Not Started",
    "draft": "Draft",
    "in_progress": "In Progress",
    "ready_to_publish": "Ready to Publish",
    "published": "Published",
    "update_in_draft": "Update in Draft",
    "needs_attention": "Needs Attention",
}

# Lower number = more urgent; drives the default "attention first" sort.
STATUS_URGENCY = {
    "needs_attention": 0,
    "not_started": 1,
    "in_progress": 2,
    "draft": 3,
    "ready_to_publish": 4,
    "update_in_draft": 5,
    "published": 6,
}


def _class_id_from_key(key: str) -> Optional[str]:
    parts = key.split("|")
    return parts[3] if len(parts) == 4 else None


def _class_conflicts(state: Dict[str, Any], class_id: str) -> List[Dict[str, Any]]:
    conflicts = []
    for c in M.scan_conflicts(state):
        if c.get("severity") != "error":
            continue
        k = c.get("key", "")
        alt_k = c.get("conflicting_key", "")
        if _class_id_from_key(k) == class_id or (_class_id_from_key(alt_k) == class_id if alt_k else False):
            conflicts.append(c)
    return conflicts


def _class_grid_cells(grid: Dict[str, Any], class_id: str) -> Dict[str, Dict[str, Any]]:
    return {k: v for k, v in grid.items()
            if isinstance(k, str) and _class_id_from_key(k) == class_id}


def _differs(draft: Dict[str, Any], published: Dict[str, Any],
             class_id: str) -> bool:
    """True when the class's draft cells differ from its published cells."""
    d = _class_grid_cells(draft, class_id)
    p = _class_grid_cells(published, class_id)
    if set(d.keys()) != set(p.keys()):
        return True
    return any(d[k] != p[k] for k in d)


def _class_required(state: Dict[str, Any], class_id: str) -> int:
    return sum(a.get("lessons", 0) for a in state.get("assignments", [])
               if a.get("class_id") == class_id)


def compute_class_rows(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build one monitoring row per registered class (left-join semantics).

    Missing timetables are detected because we iterate the class registry,
    not the timetable records.
    """
    published = state.get("published") or {}
    pub_grid = published.get("grid") or {}
    meta = state.get("class_meta", {}) or {}
    rows: List[Dict[str, Any]] = []

    for cls in state.get("classes", []):
        if cls.get("active") is False or cls.get("archived") is True:
            continue
        cid = cls["id"]
        required = _class_required(state, cid)
        draft_cells = _class_grid_cells(state.get("grid", {}), cid)
        pub_cells = _class_grid_cells(pub_grid, cid)
        conflicts = _class_conflicts(state, cid)
        missing = max(required - len(draft_cells), 0)
        has_pub = len(pub_cells) > 0 and bool(published.get("version"))
        pending_draft = has_pub and _differs(state.get("grid", {}), pub_grid, cid)

        # ── Status derivation (mutually exclusive) ──────────────────────
        if conflicts:
            status = "needs_attention"
        elif has_pub and pending_draft:
            status = "update_in_draft"
        elif has_pub:
            status = "published"
        elif len(draft_cells) == 0:
            status = "not_started"
        elif required > 0 and missing == 0:
            status = "ready_to_publish"
        elif required > 0 and missing > 0:
            status = "in_progress"
        else:
            # Draft cells exist but curriculum defines no requirements
            status = "draft"

        completion_pct = None
        if required > 0:
            completion_pct = round(min(len(draft_cells) / required, 1.0) * 100, 1)

        # Draft status label
        if not draft_cells:
            draft_status_label = "No Draft"
        elif pending_draft:
            draft_status_label = "Modified Draft"
        elif has_pub:
            draft_status_label = "Clean (In Sync)"
        else:
            draft_status_label = "Saved Draft"

        # Responsible person check (explicitly recorded only)
        cls_meta = meta.get(cid, {}) or {}
        assigned = cls.get("assigned_editor") or cls_meta.get("assigned_editor")
        if assigned and isinstance(assigned, dict):
            responsible = dict(assigned)
            responsible_recorded = True
            responsible_display = responsible.get("name", "Unassigned")
            responsible_role = responsible.get("role", "—")
        else:
            responsible = None
            responsible_recorded = False
            responsible_display = "Unassigned"
            responsible_role = "—"

        row = {
            "class_id": cid,
            "class_display": cls.get("display", cid),
            "grade": cls.get("grade"),
            "section": cls.get("section"),
            "campus": cls.get("campus", ""),
            "department": cls.get("department", ""),
            "shift": cls.get("shift", ""),
            "room": cls.get("room", ""),
            "student_count": cls.get("student_count", 0),
            "academic_year": (state.get("institution", {}) or {}).get("academic_year", ""),
            "status": status,
            "status_label": STATUS_LABELS[status],
            "required_periods": required,
            "placed_periods": len(draft_cells),
            "missing_periods": missing if required > 0 else None,
            "completion_pct": completion_pct,
            "completion_available": required > 0,
            "conflicts_count": len(conflicts),
            "draft_exists": len(draft_cells) > 0,
            "draft_status_label": draft_status_label,
            "update_in_draft": pending_draft,
            "published": has_pub,
            "published_version": published.get("version") if has_pub else None,
            "published_by": published.get("published_by") if has_pub else None,
            "published_at": published.get("published_at") if has_pub else None,
            "effective_from": published.get("effective_from") if has_pub else None,
            "responsible": responsible,
            "responsible_recorded": responsible_recorded,
            "responsible_display": responsible_display,
            "responsible_role": responsible_role,
            "last_edited_by": cls_meta.get("last_edited_by"),
            "last_edited_at": cls_meta.get("last_edited_at"),
        }
        rows.append(row)
    return rows


def compute_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Four mutually exclusive, mathematically consistent KPIs.

    A class with a published version AND a pending draft counts under
    Published (with the pending draft reported separately per row).
    Total = Published + (Draft / In Progress) + Not Started.
    """
    total = len(rows)
    published = sum(1 for r in rows if r["published"])
    not_started = sum(1 for r in rows if r["status"] == "not_started")
    draft_in_progress = total - published - not_started
    return {
        "total_classes": total,
        "published": published,
        "draft_in_progress": draft_in_progress,
        "not_started": not_started,
        "breakdown": {
            "published": sum(1 for r in rows if r["status"] == "published"),
            "update_in_draft": sum(1 for r in rows if r["status"] == "update_in_draft"),
            "ready_to_publish": sum(1 for r in rows if r["status"] == "ready_to_publish"),
            "in_progress": sum(1 for r in rows if r["status"] == "in_progress"),
            "draft": sum(1 for r in rows if r["status"] == "draft"),
            "needs_attention": sum(1 for r in rows if r["status"] == "needs_attention"),
            "not_started": not_started,
        },
    }


def filter_sort_page(rows: List[Dict[str, Any]], params: Dict[str, Any]) -> Dict[str, Any]:
    """Server-side filter, sort and pagination over monitoring rows."""
    campus = (params.get("campus") or "").strip()
    department = (params.get("department") or "").strip()
    grade = (params.get("grade") or "").strip()
    class_id = (params.get("class_id") or "").strip()
    academic_year = (params.get("academic_year") or "").strip()
    status = (params.get("status") or "").strip()
    completion = (params.get("completion") or "").strip().lower()
    search = (params.get("search") or "").strip().lower()
    responsible = (params.get("responsible") or "").strip().lower()

    out = rows
    if academic_year:
        out = [r for r in out if (r.get("academic_year") or "").lower() == academic_year.lower()]
    if campus:
        out = [r for r in out if r["campus"].lower() == campus.lower()]
    if department:
        out = [r for r in out if r["department"].lower() == department.lower()]
    if grade:
        out = [r for r in out if str(r["grade"]) == grade]
    if class_id:
        out = [r for r in out if r["class_id"].lower() == class_id.lower() or r["class_display"].lower() == class_id.lower()]
    if status:
        out = [r for r in out if r["status"] == status]
    if completion:
        if completion == "0":
            out = [r for r in out if int(r.get("completion_pct", 0)) == 0]
        elif completion == "partial":
            out = [r for r in out if 0 < int(r.get("completion_pct", 0)) < 100]
        elif completion in ("100", "complete"):
            out = [r for r in out if int(r.get("completion_pct", 0)) >= 100]
        elif completion == "incomplete":
            out = [r for r in out if int(r.get("completion_pct", 0)) < 100]
    if responsible:
        if responsible == "unassigned":
            out = [r for r in out if not r.get("responsible_recorded")]
        else:
            out = [r for r in out if responsible in (r.get("responsible_display") or "").lower()
                   or responsible in (r.get("responsible_role") or "").lower()]
    if search:
        def _match(r: Dict[str, Any]) -> bool:
            hay = " ".join([
                r["class_display"],
                r["class_id"],
                r.get("campus", ""),
                r.get("department", ""),
                r.get("responsible_display") or "",
                r.get("responsible_role") or "",
                r.get("last_edited_by") or ""
            ]).lower()
            return search in hay
        out = [r for r in out if _match(r)]

    sort = (params.get("sort") or "attention").strip()
    if sort == "not_started_first":
        key = lambda r: (0 if r["status"] == "not_started" else 1, r["class_display"])
    elif sort == "draft_first":
        key = lambda r: (0 if r["status"] in ("in_progress", "draft", "ready_to_publish")
                         else 1, r["class_display"])
    elif sort == "attention":
        key = lambda r: (STATUS_URGENCY.get(r["status"], 9), r["class_display"])
    else:  # class_name
        key = lambda r: r["class_display"]

    if sort == "recently_edited":
        edited = [r for r in out if r.get("last_edited_at")]
        unedited = sorted([r for r in out if not r.get("last_edited_at")],
                          key=lambda r: r["class_display"])
        out = sorted(edited, key=lambda r: r["last_edited_at"], reverse=True) + unedited
    elif sort == "recently_published":
        published_rows = [r for r in out if r.get("published_at")]
        unpublished = sorted([r for r in out if not r.get("published_at")],
                             key=lambda r: r["class_display"])
        out = sorted(published_rows, key=lambda r: r["published_at"], reverse=True) + unpublished
    else:
        out = sorted(out, key=key)

    try:
        page = max(int(params.get("page", 1)), 1)
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = max(min(int(params.get("page_size", 10)), 100), 1)
    except (TypeError, ValueError):
        page_size = 10
    total = len(out)
    start = (page - 1) * page_size
    return {
        "rows": out[start:start + page_size],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max((total + page_size - 1) // page_size, 1),
    }


def filter_options(state: Dict[str, Any], rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    inst_year = (state.get("institution", {}) or {}).get("academic_year", "")
    years = sorted({r.get("academic_year") for r in rows if r.get("academic_year")})
    if inst_year and inst_year not in years:
        years.append(inst_year)
    return {
        "academic_years": years,
        "campuses": sorted({r["campus"] for r in rows if r["campus"]}),
        "departments": sorted({r["department"] for r in rows if r["department"]}),
        "grades": sorted({str(r["grade"]) for r in rows if r["grade"] is not None}, key=lambda g: int(g) if g.isdigit() else 0),
        "classes": [{"value": r["class_id"], "label": r["class_display"]} for r in sorted(rows, key=lambda x: str(x["class_display"]))],
        "responsibles": sorted({r["responsible_display"] for r in rows if r.get("responsible_recorded") and r.get("responsible_display")}),
        "statuses": [{"value": k, "label": v} for k, v in STATUS_LABELS.items()],
        "completions": [
            {"value": "incomplete", "label": "Incomplete (< 100%)"},
            {"value": "0", "label": "0% (Empty)"},
            {"value": "partial", "label": "1–99% (In Progress)"},
            {"value": "100", "label": "100% (Complete)"},
        ],
        "academic_year": inst_year,
        "sorts": [
            {"value": "attention", "label": "Needs attention first"},
            {"value": "not_started_first", "label": "Not started first"},
            {"value": "draft_first", "label": "Draft first"},
            {"value": "recently_edited", "label": "Recently edited"},
            {"value": "recently_published", "label": "Recently published"},
            {"value": "class_name", "label": "Class name"},
        ],
    }


def _subject_breakdown(state: Dict[str, Any], class_id: str) -> List[Dict[str, Any]]:
    """Subject requirements vs placed periods for a given class."""
    idx = M._index(state)
    assigned = [a for a in state.get("assignments", []) if a.get("class_id") == class_id]
    grid_cells = _class_grid_cells(state.get("grid", {}), class_id)
    placed_counts: Dict[str, int] = {}
    for cell in grid_cells.values():
        sub_id = cell.get("subject_id")
        if sub_id:
            placed_counts[sub_id] = placed_counts.get(sub_id, 0) + 1

    breakdown = []
    for a in assigned:
        sub_id = a.get("subject_id")
        sub = idx["subjects"].get(sub_id, {})
        teacher = idx["teachers"].get(a.get("teacher_id"), {})
        req = a.get("lessons", 0)
        placed = placed_counts.get(sub_id, 0)
        missing = max(req - placed, 0)
        breakdown.append({
            "subject_id": sub_id,
            "subject_name": sub.get("name_en") or sub.get("name_kh", sub_id),
            "subject_code": sub.get("code", ""),
            "color": sub.get("color", "#2563eb"),
            "assigned_teacher": teacher.get("name_en") or teacher.get("name_kh") or "Unassigned",
            "required": req,
            "placed": placed,
            "missing": missing,
            "complete": missing == 0,
            "status": "Complete" if missing == 0 else ("Unplaced" if placed == 0 else "Partial"),
        })
    return breakdown


def _build_weekly_matrix(idx: Dict[str, Any], cls: Dict[str, Any],
                         cells_dict: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Structure lessons into days and periods for read-only preview."""
    days = ["ច័ន្ទ", "អង្គារ", "ពុធ", "ព្រហស្បតិ៍", "សុក្រ", "សៅរ៍"]
    matrix: Dict[str, Dict[str, Any]] = {d: {} for d in days}
    for key, cell in cells_dict.items():
        p = M.parse_grid_key(key)
        day = p["day"]
        slot_key = f"{p['shift']}|{p['period']}"
        sub = idx["subjects"].get(cell.get("subject_id"), {})
        tch = idx["teachers"].get(cell.get("teacher_id"), {})
        if day in matrix:
            matrix[day][slot_key] = {
                "key": key,
                "day": day,
                "shift": p["shift"],
                "period": p["period"],
                "slot_key": slot_key,
                "subject_id": cell.get("subject_id"),
                "subject_name": sub.get("name_kh", cell.get("subject_id")),
                "subject_code": sub.get("code", ""),
                "color": sub.get("color", "#2563eb"),
                "teacher_id": cell.get("teacher_id"),
                "teacher_name": tch.get("name_kh", ""),
                "teacher_code": tch.get("code", ""),
                "room": cell.get("room", cls.get("room", "")),
            }
    return matrix


def class_detail(state: Dict[str, Any], class_id: str) -> Optional[Dict[str, Any]]:
    """Full read-only monitoring detail for one class."""
    rows = {r["class_id"]: r for r in compute_class_rows(state)}
    row = rows.get(class_id)
    if row is None:
        return None

    cls = next((c for c in state.get("classes", []) if c["id"] == class_id), {})
    idx = M._index(state)
    published = state.get("published") or {}
    pub_grid = published.get("grid") or {}

    # ── Activity history (real audit records only) ──────────────────────
    events: List[Dict[str, Any]] = []
    for h in state.get("history", []):
        detail = h.get("detail", {}) or {}
        key = detail.get("key", "")
        if _class_id_from_key(key) != class_id:
            continue
        events.append({
            "at": h.get("at"),
            "action": h.get("label", "Timetable edited"),
            "actor": h.get("actor") or "Unrecorded",
            "type": "draft",
            "detail": key,
        })
    for entry in reversed(state.get("published_history", [])):
        snap = entry.get("snapshot", {}) or {}
        grid = snap.get("grid", {}) or {}
        if _class_grid_cells(grid, class_id):
            events.append({
                "at": entry.get("published_at"),
                "action": f"Timetable published (v{entry.get('version')})"
                          + (" — rollback" if entry.get("action") == "rollback" else ""),
                "actor": entry.get("published_by") or "Unrecorded",
                "type": "publication",
                "detail": f"{len(_class_grid_cells(grid, class_id))} periods",
            })
    import timetable_oversight as O
    for rem in O.get_reminders():
        if class_id in str(rem.get("task_id", "")):
            events.append({
                "at": rem.get("created_at"),
                "action": "Reminder sent",
                "actor": rem.get("sender_name") or "Unrecorded",
                "type": "reminder",
                "detail": rem.get("message", ""),
            })
    events.sort(key=lambda e: str(e.get("at") or ""), reverse=True)

    # ── Read-only previews ──────────────────────────────────────────────
    draft_cells = _class_grid_cells(state.get("grid", {}), class_id)
    pub_cells = _class_grid_cells(pub_grid, class_id)

    def _lesson_view(key: str, cell: Dict[str, Any]) -> Dict[str, Any]:
        p = M.parse_grid_key(key)
        sub = idx["subjects"].get(cell.get("subject_id"), {})
        teacher = idx["teachers"].get(cell.get("teacher_id"), {})
        return {
            "key": key, "day": p["day"], "shift": p["shift"],
            "period": p["period"],
            "subject": sub.get("name_kh", cell.get("subject_id", "")),
            "subject_short": sub.get("code", ""),
            "color": sub.get("color", "#2563eb"),
            "teacher": teacher.get("name_kh", cell.get("teacher_id", "")),
            "teacher_code": teacher.get("code", ""),
            "room": cls.get("room", ""),
        }

    draft_lessons = [_lesson_view(k, c) for k, c in sorted(draft_cells.items(), key=lambda kv: kv[0])]
    published_lessons = [_lesson_view(k, c) for k, c in sorted(pub_cells.items(), key=lambda kv: kv[0])]

    conflicts = _class_conflicts(state, class_id)
    subject_reqs = _subject_breakdown(state, class_id)
    missing = row["missing_periods"] or 0

    return {
        "success": True,
        "row": row,
        "class_info": {
            "class": cls.get("display", class_id),
            "class_id": class_id,
            "campus": cls.get("campus", ""),
            "department": cls.get("department", ""),
            "grade": cls.get("grade"),
            "section": cls.get("section"),
            "shift": cls.get("shift", ""),
            "room": cls.get("room", ""),
            "student_count": cls.get("student_count", 0),
            "academic_year": row["academic_year"],
            "responsible": row["responsible"],
            "responsible_display": row["responsible_display"],
            "responsible_role": row["responsible_role"],
        },
        "preparation": {
            "draft_exists": row["draft_exists"],
            "draft_status_label": row["draft_status_label"],
            "status": row["status"],
            "status_label": row["status_label"],
            "completion_pct": row["completion_pct"],
            "completion_available": row["completion_available"],
            "required_periods": row["required_periods"],
            "placed_periods": row["placed_periods"],
            "missing_periods": row["missing_periods"],
            "subjects": subject_reqs,
            "conflicts": [
                {"type": c.get("type"), "severity": c.get("severity"),
                 "key": c.get("key"), "message_en": c.get("message_en") or c.get("message")}
                for c in conflicts
            ],
            "validation": {
                "passed": len(conflicts) == 0 and missing == 0 and row["required_periods"] > 0,
                "has_conflicts": len(conflicts) > 0,
                "has_missing": missing > 0,
            }
        },
        "publication": {
            "has_publication": bool(published.get("version")),
            "version": published.get("version"),
            "published_by": published.get("published_by"),
            "published_at": published.get("published_at"),
            "effective_from": published.get("effective_from"),
            "class_in_publication": row["published"],
            "update_pending": row["update_in_draft"],
        },
        "activity_history": events[:30],
        "preview": {
            "draft": draft_lessons,
            "published": published_lessons,
            "draft_matrix": _build_weekly_matrix(idx, cls, draft_cells),
            "published_matrix": _build_weekly_matrix(idx, cls, pub_cells),
        },
    }
