"""
NGIS Security & Access Control Center — backend
Blueprint: /api/security (admin-only, enforced server-side).

Integrates with EXISTING infrastructure (no duplicate account store):
  · data/user_accounts.json   — authoritative accounts (user_management_api owns it);
                                restrictions are recorded there as status + security_restriction
  · user_management_api       — store load/save + login rejection semantics
  · roles_permissions         · login-security:view / login-security:manage are the
                                existing permission keys guarding this module

New (greenfield, per audit):
  · data/security.sqlite3     — append-only security_events + security_audit (+ ip_restrictions, settings)
  · lightweight per-endpoint-class rate limiter (in-memory counters, thread-safe; single-process
    deployment — a shared store is required before horizontal scaling; see report)
  · IP capture (request.remote_addr; X-Forwarded-For only when settings.trust_proxy is enabled)
  · automatic restriction expiry sweep + retention sweep (tick, throttled)

PRIVACY: passwords/tokens/cookies/request bodies are never written to the event store;
detail fields are built from a fixed whitelist of safe attributes only.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from flask import Blueprint, Response, g, jsonify, request

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("NGIS_SECURITY_DB", str(ROOT / ".data" / "security.sqlite3")))

security_bp = Blueprint("security_api", __name__, url_prefix="/api/security")

# ── module state ────────────────────────────────────────────────────────────
_LOCK = threading.RLock()
_counters = {}          # rate limiter: rule_id → {ip_or_key: [timestamps]}
_last_sweep = 0.0
_settings_cache = None

DEFAULT_SETTINGS = {
    "trust_proxy": False,                 # honor X-Forwarded-For only when behind a trusted proxy
    "login_ip_limit": 30,                 # per IP per 5 min (generous: shared campus NAT)
    "login_identifier_limit": 8,          # per targeted account per 5 min (brute force)
    "auth_ip_limit": 30,                  # /api/auth/* other endpoints per IP per minute
    "write_api_limit": 600,               # mutating /api/* per IP per minute (school-wide NAT safe)
    "security_api_limit": 240,            # /api/security per IP per minute
    "ip_restriction_default_hours": 24,   # short-lived by default
    "event_retention_days": 90,
    "suspicious_failed_login_threshold": 5
}

# Documented severity classification (Phase 6/10) — event_type → (base severity, description)
EVENT_RULES = {
    "auth.login_failed":        ("low",          "A sign-in attempt with invalid credentials was rejected."),
    "auth.account_rejected":    ("medium",       "A sign-in attempt targeted an account that is suspended, banned, locked or awaiting activation."),
    "auth.login_success":       ("informational", "A sign-in succeeded."),
    "auth.unauthorized":        ("low",          "A request arrived without a valid session."),
    "auth.permission_denied":   ("medium",       "An authenticated caller attempted an operation its role does not permit."),
    "rate_limit.violation":     ("medium",       "A client exceeded a documented rate-limit rule and received HTTP 429."),
    "ip.blocked":               ("high",         "A request from an actively restricted source IP was blocked."),
    "restriction.applied":      ("informational", "An administrator applied an account restriction (see audit history)."),
    "restriction.removed":      ("informational", "An account restriction was lifted (see audit history)."),
    "restriction.auto_expired": ("informational", "A temporary restriction reached its expiry and was lifted automatically."),
    "security.setting_changed": ("informational", "A security setting was changed (see audit history).")
}

SEVERITY_ORDER = {"informational": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}

# ── database ────────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS security_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  event_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  actor_account TEXT DEFAULT '',
  actor_role TEXT DEFAULT '',
  source_ip TEXT DEFAULT '',
  user_agent TEXT DEFAULT '',
  method TEXT DEFAULT '',
  endpoint TEXT DEFAULT '',
  status_code INTEGER DEFAULT 0,
  outcome TEXT DEFAULT '',
  detail TEXT DEFAULT '',
  correlation_id TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sev_ts ON security_events(ts);
CREATE INDEX IF NOT EXISTS idx_sev_type ON security_events(event_type);
CREATE INDEX IF NOT EXISTS idx_sev_ip ON security_events(source_ip);

CREATE TABLE IF NOT EXISTS security_audit (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  actor TEXT NOT NULL,
  actor_role TEXT NOT NULL,
  action TEXT NOT NULL,
  target TEXT DEFAULT '',
  target_name TEXT DEFAULT '',
  reason TEXT DEFAULT '',
  before_json TEXT DEFAULT '{}',
  after_json TEXT DEFAULT '{}',
  outcome TEXT DEFAULT 'success',
  correlation_id TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_saud_ts ON security_audit(ts);

CREATE TABLE IF NOT EXISTS ip_restrictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ip TEXT NOT NULL,
  mode TEXT NOT NULL DEFAULT 'restrict',   -- restrict | allow (monitored exception)
  reason TEXT NOT NULL,
  created_by TEXT NOT NULL,
  created_at TEXT NOT NULL,
  expires_at TEXT,
  active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS security_settings (
  key TEXT PRIMARY KEY,
  value_json TEXT NOT NULL
);
"""


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    with _connect() as conn:
        conn.executescript(SCHEMA)


_init_db()


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


# ── settings ────────────────────────────────────────────────────────────────
def get_settings():
    global _settings_cache
    with _LOCK:
        if _settings_cache is not None:
            return dict(_settings_cache)
        merged = dict(DEFAULT_SETTINGS)
        with _connect() as conn:
            for row in conn.execute("SELECT key, value_json FROM security_settings"):
                try:
                    merged[row["key"]] = json.loads(row["value_json"])
                except Exception:
                    pass
        _settings_cache = merged
        return dict(merged)


def set_setting(key: str, value) -> None:
    global _settings_cache
    allowed = set(DEFAULT_SETTINGS.keys())
    if key not in allowed:
        raise ValueError(f"unknown setting: {key}")
    with _LOCK:
        _settings_cache = None
        with _connect() as conn:
            conn.execute(
                "INSERT INTO security_settings(key, value_json) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value_json = excluded.value_json",
                (key, json.dumps(value)),
            )


# ── actor resolution ────────────────────────────────────────────────────────
def resolve_actor():
    """Resolve the calling identity → {id, name, role, username, account|None}.

    Mirrors the app's established identity conventions:
      · Authorization: Bearer um-session-<account_id>  (provisioned store session)
      · Authorization: Bearer mock-jwt-token-<role>    (demo persona; only 'admin'
        is a valid security-center identity — demo role maps to ADMIN)
      · X-Actor: <username or email>                   (trusted header, matches
        the roles/user-mgmt modules' actor model)
    """
    auth = request.headers.get("Authorization", "").strip()
    store = None
    if auth.startswith("Bearer um-session-"):
        account_id = auth[len("Bearer um-session-"):]
        store = _store()
        acc = next((a for a in store["accounts"] if a["id"] == account_id), None)
        if acc and acc.get("status") == "active":
            return _actor_from_account(acc)
        return None
    if auth.startswith("Bearer mock-jwt-token-"):
        role = auth[len("Bearer mock-jwt-token-"):].strip().lower()
        if role == "admin":
            return {"id": "demo-admin", "name": "Sok Panha (demo admin)", "role": "ADMIN",
                    "username": "admin@ngis.edu.kh", "account": None, "demo": True}
        return None  # student/teacher/principal/parent/staff demos are NOT security admins
    actor = (request.headers.get("X-Actor") or "").strip().lower()
    if actor:
        store = _store()
        acc = next((a for a in store["accounts"]
                    if a.get("status") == "active" and
                    (str(a.get("username", "")).lower() == actor or str(a.get("email", "")).lower() == actor)), None)
        if acc:
            return _actor_from_account(acc)
    return None


def _actor_from_account(acc):
    return {"id": acc["id"], "name": acc.get("name", ""), "role": acc.get("role", ""),
            "username": acc.get("username", ""), "account": acc, "demo": False}


def _is_super(actor) -> bool:
    return bool(actor) and actor.get("role") == "SUPER_ADMIN"


def _is_admin(actor) -> bool:
    return bool(actor) and actor.get("role") in ("ADMIN", "SUPER_ADMIN")


def _demo_admins() -> int:
    """Demo admin persona exists outside the store; guard-last-admin counts it."""
    return 1


# ── event + audit writers (append-only) ─────────────────────────────────────
_REDACT_KEYS = re.compile(r"password|token|secret|cookie|authorization|session", re.I)


def _redact(value) -> str:
    """Safe string builder — collapses anything that could carry credentials."""
    text = str(value or "")
    if len(text) > 400:
        text = text[:400] + "…"
    return text


def log_event(event_type: str, *, actor_account="", actor_role="", status_code=0,
              outcome="", detail="", ip=None, user_agent=None, endpoint=None,
              method=None, severity=None) -> None:
    rule = EVENT_RULES.get(event_type)
    if rule is None:
        return  # unknown event types are never recorded (documented taxonomy only)
    sev = severity or rule[0]
    ip = ip if ip is not None else client_ip()
    user_agent = _redact(user_agent if user_agent is not None else request.headers.get("User-Agent", ""))[:200]
    endpoint = _redact(endpoint if endpoint is not None else request.path)
    method = method or request.method
    cid = getattr(g, "correlation_id", "") if request else ""
    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO security_events(ts, event_type, severity, actor_account, actor_role,"
                " source_ip, user_agent, method, endpoint, status_code, outcome, detail, correlation_id)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (_now(), event_type, sev, _redact(actor_account)[:80], _redact(actor_role)[:40],
                 _redact(ip)[:64], user_agent, method, endpoint, int(status_code or 0),
                 _redact(outcome)[:40], _redact(detail)[:400], cid),
            )
    except Exception:
        pass  # monitoring must never break the request path


def write_audit(actor, action: str, target="", target_name="", reason="",
                before=None, after=None, outcome="success") -> None:
    cid = getattr(g, "correlation_id", "") if request else ""
    try:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO security_audit(ts, actor, actor_role, action, target, target_name,"
                " reason, before_json, after_json, outcome, correlation_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (_now(), _redact(actor.get("id") if actor else "system"),
                 _redact(actor.get("role") if actor else "system"),
                 _redact(action)[:60], _redact(target)[:80], _redact(target_name)[:120],
                 _redact(reason)[:400], json.dumps(before or {}, default=str)[:800],
                 json.dumps(after or {}, default=str)[:800], _redact(outcome)[:40], cid),
            )
    except Exception:
        pass


# ── client IP (proxy-safe) ──────────────────────────────────────────────────
def client_ip() -> str:
    if get_settings().get("trust_proxy"):
        fwd = request.headers.get("X-Forwarded-For", "")
        if fwd:
            return fwd.split(",")[0].strip()[:64]
    return (request.remote_addr or "")[:64]


# ── account restriction (uses the authoritative store) ──────────────────────
def _store():
    from user_management_api import _store as um_store
    return um_store()


def _save_store(data):
    from user_management_api import _save_store as um_save
    um_save(data)
RESTRICTION_TYPES = ("suspend", "ban")
DURATIONS = {"1h": 1, "24h": 24, "7d": 24 * 7, "30d": 24 * 30}


def _directory_view(acc) -> dict:
    r = acc.get("security_restriction") or {}
    status = acc.get("status")
    display = status
    if status == "suspended" and r.get("type") == "ban":
        display = "banned"
    elif status == "suspended" and r.get("type") == "suspend":
        display = "suspended"
    elif status == "suspended":
        display = "suspended"
    return {
        "id": acc.get("id"), "name": acc.get("name", ""), "role": acc.get("role", ""),
        "personType": acc.get("person_type", ""), "username": acc.get("username", ""),
        "email": acc.get("email", ""), "campus": acc.get("campus", ""),
        "department": acc.get("department", ""), "assignment": acc.get("assignment", ""),
        "status": status, "displayStatus": display,
        "lastLogin": acc.get("last_login", ""), "failedAttempts": acc.get("failed_attempts", 0),
        "restriction": r if status == "suspended" else {},
        "restrictionHistory": acc.get("restriction_history", []),
    }


def _recent_event_count(account_id_or_name: str, minutes: int = 60) -> int:
    cutoff = (datetime.utcnow() - timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        with _connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) c FROM security_events WHERE ts >= ? AND (actor_account = ? OR actor_account = ?)"
                " AND event_type IN ('auth.login_failed','auth.account_rejected','rate_limit.violation')",
                (cutoff, account_id_or_name, account_id_or_name),
            ).fetchone()
            return int(row["c"])
    except Exception:
        return 0


def apply_restriction(target: dict, rtype: str, reason: str, duration: str,
                      custom_until: str, notes: str, actor: dict) -> dict:
    store = _store()
    acc = next((a for a in store["accounts"] if a["id"] == target["id"]), None)
    if not acc:
        raise LookupError("account not found")

    before = {"status": acc.get("status"), "restriction": acc.get("security_restriction") or None}
    now = datetime.utcnow()
    until = None
    if rtype == "suspend":
        # numeric hours (int or numeric string, 1–72) are accepted alongside presets
        try:
            hours_num = float(duration)
        except (TypeError, ValueError):
            hours_num = None
        if hours_num is not None and 1 <= hours_num <= 72:
            until = (now + timedelta(hours=hours_num)).strftime("%Y-%m-%dT%H:%M:%SZ")
        elif duration == "custom":
            if not custom_until:
                raise ValueError("custom duration requires an expiration date")
            until = custom_until
        elif duration in DURATIONS:
            until = (now + timedelta(hours=DURATIONS[duration])).strftime("%Y-%m-%dT%H:%M:%SZ")
        elif duration != "indefinite":
            raise ValueError("invalid duration")
        if duration == "indefinite":
            rtype = "ban"  # indefinite suspension == permanent ban (policy requires it be explicit)

    restriction = {
        "type": rtype, "reason": reason, "notes": notes or "",
        "until": until, "by": actor["id"], "by_name": actor.get("name", ""),
        "at": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": "security-center",
    }
    acc["status"] = "suspended"
    acc["failed_attempts"] = 0
    acc["security_restriction"] = restriction
    hist = acc.setdefault("restriction_history", [])
    hist.append(dict(restriction))
    _save_store(store)

    after = {"status": acc["status"], "restriction": restriction}
    write_audit(actor, "account_restricted" if rtype == "suspend" else "account_banned",
                target=acc["id"], target_name=acc.get("name", ""), reason=reason,
                before=before, after=after)
    log_event("restriction.applied", actor_account=acc["id"], actor_role=actor.get("role", ""),
              outcome="applied", detail=f"{rtype} on {acc.get('name','')}: {reason[:120]}")
    # status flip instantly invalidates store sessions: resolve_store_session
    # only resolves accounts with status 'active'.
    return _directory_view(acc)


def lift_restriction(target_id: str, reason: str, actor: dict, automatic=False) -> dict:
    store = _store()
    acc = next((a for a in store["accounts"] if a["id"] == target_id), None)
    if not acc:
        raise LookupError("account not found")
    r = acc.get("security_restriction") or {}
    before = {"status": acc.get("status"), "restriction": r or None}
    # Unban must NOT override unrelated lifecycle states:
    if acc.get("status") != "suspended":
        raise ValueError(f"account status is '{acc.get('status')}' — no security restriction to lift "
                         f"(disabled/locked/pending states belong to their own workflows)")
    if not r:
        raise ValueError("no security-center restriction recorded on this account "
                         "(suspensions applied elsewhere must be lifted through User Management)")
    acc["status"] = "active"
    acc["failed_attempts"] = 0
    lifted = dict(r)
    lifted["lifted_at"] = _now_iso()
    lifted["lifted_by"] = "system (auto-expiry)" if automatic else actor["id"]
    lifted["lift_reason"] = reason or ("auto-expiry" if automatic else "manual unban")
    acc.setdefault("restriction_history", []).append(lifted)
    acc["security_restriction"] = None
    _save_store(store)
    after = {"status": "active", "restriction": None}
    write_audit("system" if automatic else actor, "account_unrestricted",
                target=acc["id"], target_name=acc.get("name", ""), reason=reason,
                before=before, after=after)
    log_event("restriction.auto_expired" if automatic else "restriction.removed",
              actor_account=acc["id"], outcome="lifted", detail=f"{acc.get('name','')} restriction lifted")
    return _directory_view(acc)


def sweep_due_restrictions() -> int:
    """Lift temporary restrictions whose expiry has passed. Returns count."""
    store = _store()
    changed = 0
    now_iso = _now_iso()
    for acc in store["accounts"]:
        r = acc.get("security_restriction") or {}
        if acc.get("status") == "suspended" and r.get("type") == "suspend" and r.get("until"):
            if str(r["until"]) <= now_iso:
                try:
                    lift_restriction(acc["id"], "temporary restriction expired", None, automatic=True)
                    changed += 1
                except Exception:
                    pass
    if changed:
        _save_store(store)
    return changed


# ── rate limiter (per-endpoint-class rules, thread-safe, per-IP) ────────────
def _rules():
    s = get_settings()
    return [
        {"id": "auth-login", "prefix": "/api/auth/login", "methods": {"POST"},
         "limit": int(s["login_ip_limit"]), "window": 300,
         "note": "Sign-in attempts per source IP (generous for shared campus networks)"},
        {"id": "auth-other", "prefix": "/api/auth/", "methods": None,
         "limit": int(s["auth_ip_limit"]), "window": 60,
         "note": "Other authentication endpoints per source IP"},
        {"id": "security-api", "prefix": "/api/security", "methods": None,
         "limit": int(s["security_api_limit"]), "window": 60,
         "note": "Security Center API per source IP"},
        {"id": "write-api", "prefix": "/api/", "methods": {"POST", "PUT", "DELETE", "PATCH"},
         "limit": int(s["write_api_limit"]), "window": 60,
         "note": "Mutating API requests per source IP (school-wide NAT safe)"},
    ]


def _hit(rule, key, now) -> int:
    bucket = _counters.setdefault(rule["id"], {})
    window = rule["window"]
    stamps = [t for t in bucket.get(key, []) if now - t < window]
    stamps.append(now)
    bucket[key] = stamps
    if len(bucket) > 5000:  # bounded memory
        for k in list(bucket.keys())[:1000]:
            bucket.pop(k, None)
    return len(stamps)


def rate_limit_check():
    """Returns (rule, count) when a rule is violated, else None."""
    s = get_settings()
    ip = client_ip()
    if not ip:
        return None
    now = time.time()
    matched = None
    for rule in _rules():
        if not request.path.startswith(rule["prefix"]):
            continue
        if rule["methods"] is not None and request.method not in rule["methods"]:
            continue
        if matched is None or len(rule["prefix"]) > len(matched["prefix"]):
            matched = rule  # most specific rule wins
    if matched is None:
        return None
    with _LOCK:
        count = _hit(matched, ip, now)
    if count > int(matched["limit"]):
        return matched, count
    # per-identifier brute-force guard on login (does NOT punish the shared IP)
    if matched["id"] == "auth-login" and request.method == "POST":
        body = request.get_json(silent=True) or {}
        ident = (body.get("email") or body.get("username") or "").strip().lower()
        if ident:
            with _LOCK:
                c2 = _hit({"id": "auth-login-id", "window": 300}, ident, now)
            if c2 > int(s["login_identifier_limit"]):
                return {"id": "auth-login-id", "limit": int(s["login_identifier_limit"]),
                        "window": 300, "note": "Repeated failed sign-ins targeting one account"}, c2
    return None


# ── app-level hooks ─────────────────────────────────────────────────────────
def install(app):
    """Register the security blueprint + app-wide hooks on the Flask app."""

    def _before():
        g.correlation_id = uuid.uuid4().hex[:12]
        global _last_sweep
        now = time.time()
        if now - _last_sweep > 60:
            _last_sweep = now
            try:
                sweep_due_restrictions()
                _retention_sweep()
            except Exception:
                pass
        # IP restriction enforcement (admin undo path stays open)
        ip = client_ip()
        if ip and request.path.startswith("/api/") and not request.path.startswith("/api/security"):
            with _connect() as conn:
                row = conn.execute(
                    "SELECT id, reason FROM ip_restrictions WHERE ip = ? AND mode = 'restrict' AND active = 1"
                    " AND (expires_at IS NULL OR expires_at > ?) ORDER BY id DESC LIMIT 1",
                    (ip, _now_iso()),
                ).fetchone()
            if row:
                log_event("ip.blocked", outcome="blocked", status_code=403,
                          detail=f"restricted IP ({row['reason'][:100]})")
                return jsonify({"error": {"code": "IP_RESTRICTED",
                                          "message": "Requests from this network are temporarily restricted. Contact your administrator."}}), 403
        violated = rate_limit_check()
        if violated:
            rule, count = violated
            log_event("rate_limit.violation", status_code=429, outcome="blocked",
                      detail=f"rule {rule['id']} limit {rule['limit']}/{rule['window']}s — observed {count}")
            resp = jsonify({"error": {"code": "RATE_LIMITED",
                                      "message": "Too many requests — please slow down.",
                                      "rule": rule["id"], "limit": rule["limit"],
                                      "window_seconds": rule["window"], "observed": count}})
            resp.status_code = 429
            resp.headers["Retry-After"] = str(rule["window"])
            return resp
        return None

    def _after(resp):
        try:
            if request.path.startswith("/api/"):
                code = resp.status_code
                if code == 429:
                    pass  # already logged by the limiter
                elif code == 403 and not request.path.startswith("/api/auth/"):
                    log_event("auth.permission_denied", status_code=403, outcome="denied")
                elif code == 401 and not request.path.startswith(("/api/auth/me", "/api/auth/login")):
                    log_event("auth.unauthorized", status_code=401, outcome="rejected")
        except Exception:
            pass
        return resp

    app.before_request(_before)
    app.after_request(_after)
    app.register_blueprint(security_bp)


def _retention_sweep() -> None:
    days = int(get_settings().get("event_retention_days", 90))
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        with _connect() as conn:
            conn.execute("DELETE FROM security_events WHERE ts < ?", (cutoff,))
    except Exception:
        pass


# ════════════════════════════════════════════════════════════════════════════
# Endpoints
# ════════════════════════════════════════════════════════════════════════════
def _deny(code, message, http=403):
    return jsonify({"error": {"code": code, "message": message}}), http


def _require_admin():
    actor = resolve_actor()
    if not actor:
        return None, _deny("FORBIDDEN", "Administrator identity required for the Security Center")
    if not _is_admin(actor):
        return None, _deny("FORBIDDEN", "Only ADMIN or SUPER_ADMIN actors may access the Security Center")
    return actor, None


def _require_super():
    actor, err = _require_admin()
    if err:
        return None, err
    if not _is_super(actor):
        return None, _deny("FORBIDDEN", "Only SUPER_ADMIN actors may perform this action")
    return actor, None


@security_bp.get("/overview")
def overview():
    actor, err = _require_admin()
    if err:
        return err
    hours = max(1, min(24 * 30, int(request.args.get("hours", 24))))
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    store = _store()
    accounts = store["accounts"]
    active = sum(1 for a in accounts if a.get("status") == "active")
    restricted = sum(1 for a in accounts if a.get("status") == "suspended" and (a.get("security_restriction") or {}).get("source") == "security-center")
    locked = sum(1 for a in accounts if a.get("status") == "locked")
    with _connect() as conn:
        def count(sql, args=()):
            return int(conn.execute(sql, args).fetchone()["c"])
        failed = count("SELECT COUNT(*) c FROM security_events WHERE ts >= ? AND event_type='auth.login_failed'", (cutoff,))
        rejected = count("SELECT COUNT(*) c FROM security_events WHERE ts >= ? AND event_type='auth.account_rejected'", (cutoff,))
        ratelimited = count("SELECT COUNT(*) c FROM security_events WHERE ts >= ? AND event_type='rate_limit.violation'", (cutoff,))
        denied = count("SELECT COUNT(*) c FROM security_events WHERE ts >= ? AND event_type='auth.permission_denied'", (cutoff,))
        suspicious = count("SELECT COUNT(*) c FROM security_events WHERE ts >= ? AND severity IN ('medium','high','critical') AND event_type NOT LIKE 'restriction.%'", (cutoff,))
        iprows = conn.execute("SELECT COUNT(*) c FROM ip_restrictions WHERE active=1 AND mode='restrict' AND (expires_at IS NULL OR expires_at > ?)", (_now_iso(),)).fetchone()
    return jsonify({"data": {
        "rangeHours": hours,
        "activeAccounts": active,
        "restrictedAccounts": restricted,
        "securityLocked": locked,
        "failedLogins": failed + rejected,
        "rateLimited": ratelimited,
        "permissionDenied": denied,
        "suspiciousEvents": suspicious,
        "activeIncidents": int(iprows["c"]) + locked,
        "labels": {
            "activeAccounts": "lifetime (current)", "restrictedAccounts": "lifetime (current)",
            "securityLocked": "lifetime (current)", "failedLogins": f"last {hours}h",
            "rateLimited": f"last {hours}h", "permissionDenied": f"last {hours}h",
            "suspiciousEvents": f"last {hours}h", "activeIncidents": "current"
        }
    }})


@security_bp.get("/users")
def list_users():
    actor, err = _require_admin()
    if err:
        return err
    args = request.args
    try:
        page = max(1, int(args.get("page", 1)))
        size = min(100, max(5, int(args.get("page_size", 20))))
    except ValueError:
        return _deny("BAD_REQUEST", "invalid pagination", 400)
    search = (args.get("search") or "").strip().lower()
    role = (args.get("role") or "").strip().upper()
    campus = (args.get("campus") or "").strip()
    status = (args.get("status") or "").strip().lower()  # display-status aware
    sort = args.get("sort", "name")
    order = "desc" if args.get("order", "asc").lower() == "desc" else "asc"

    store = _store()
    rows = [_directory_view(a) for a in store["accounts"]]
    if search:
        rows = [r for r in rows if search in f"{r['name']} {r['username']} {r['email']} {r['id']}".lower()]
    if role:
        rows = [r for r in rows if r["role"] == role]
    if campus:
        rows = [r for r in rows if (r["campus"] or "").lower() == campus.lower()]
    if status:
        rows = [r for r in rows if r["displayStatus"] == status or (status == "all")]
    keymap = {"name": lambda r: (r["name"] or "").lower(), "role": lambda r: r["role"],
              "campus": lambda r: (r["campus"] or "").lower(), "status": lambda r: r["displayStatus"],
              "last_login": lambda r: r["lastLogin"] or ""}
    rows.sort(key=keymap.get(sort, keymap["name"]), reverse=(order == "desc"))
    total = len(rows)
    pages = max(1, (total + size - 1) // size)
    page = min(page, pages)
    slice_ = rows[(page - 1) * size: page * size]
    # recent security activity (last 60 min) for the visible page only — bounded
    for r in slice_:
        n = _recent_event_count(r["id"]) + _recent_event_count((r["username"] or "").lower())
        r["recentSecurityActivity"] = n
    campuses = sorted({(a.get("campus") or "") for a in store["accounts"] if a.get("campus")})
    return jsonify({"data": {"rows": slice_, "total": total, "page": page, "pageSize": size,
                             "pages": pages,
                             "facets": {"roles": sorted({a.get("role") for a in store["accounts"] if a.get("role")}),
                                         "campuses": campuses,
                                         "statuses": ["active", "suspended", "banned", "locked", "disabled", "pending_activation"]}},
                    "viewerRole": actor["role"]})


@security_bp.get("/users/<account_id>")
def user_detail(account_id):
    actor, err = _require_admin()
    if err:
        return err
    store = _store()
    acc = next((a for a in store["accounts"] if a["id"] == account_id), None)
    if not acc:
        return _deny("NOT_FOUND", "account not found", 404)
    view = _directory_view(acc)
    view["recentEvents"] = _recent_event_count(acc["id"]) + _recent_event_count((acc.get("username") or "").lower())
    hist = store.get("login_history", {}).get(account_id, [])[-10:]
    view["loginHistory"] = list(reversed(hist))
    try:
        with _connect() as conn:
            ev = [dict(r) for r in conn.execute(
                "SELECT id, ts, event_type, severity, source_ip, endpoint, outcome, detail FROM security_events"
                " WHERE actor_account = ? OR actor_account = ? ORDER BY id DESC LIMIT 10",
                (acc["id"], (acc.get("username") or "").lower()))]
        view["securityEvents"] = ev
    except Exception:
        view["securityEvents"] = []
    view["canManage"] = _can_manage_target(actor, acc)[0]
    view["viewerRole"] = actor["role"]
    return jsonify({"data": view})


def _can_manage_target(actor, target_acc) -> tuple[bool, str]:
    """Server-side authorization for restriction actions (Phase 5)."""
    if target_acc["id"] == actor["id"] or (
            actor.get("username") and target_acc.get("username") == actor["username"]):
        return False, "Administrators cannot restrict their own account"
    trole = target_acc.get("role")
    if trole == "SUPER_ADMIN" and not _is_super(actor):
        return False, "Only SUPER_ADMIN actors may restrict SUPER_ADMIN accounts"
    if trole in ("ADMIN", "PRINCIPAL") and not _is_super(actor):
        return False, f"Only SUPER_ADMIN actors may restrict {trole.title()} accounts"
    # last-active-admin guard (mirrors user_management._guard_last_admin)
    if trole in ("ADMIN", "SUPER_ADMIN") and target_acc.get("status") == "active":
        store = _store()
        active_admins = [a for a in store["accounts"]
                         if a.get("role") in ("ADMIN", "SUPER_ADMIN") and a.get("status") == "active"]
        if len(active_admins) <= 1:
            return False, "Cannot restrict the last active administrator account"
    return True, ""


@security_bp.post("/users/<account_id>/restrict")
def restrict_user(account_id):
    actor, err = _require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    rtype = (body.get("type") or "").lower()
    reason = (body.get("reason") or "").strip()
    duration = str(body.get("duration") or "24h").strip().lower()
    custom_until = (body.get("customUntil") or "").strip()
    notes = (body.get("notes") or "").strip()
    if rtype not in RESTRICTION_TYPES:
        return _deny("BAD_REQUEST", "type must be 'suspend' or 'ban'", 400)
    if not reason:
        return _deny("BAD_REQUEST", "A reason is required for every restriction", 400)
    store = _store()
    acc = next((a for a in store["accounts"] if a["id"] == account_id), None)
    if not acc:
        return _deny("NOT_FOUND", "account not found", 404)
    allowed, why = _can_manage_target(actor, acc)
    if not allowed:
        return _deny("FORBIDDEN", why)
    if rtype == "ban" and not _is_super(actor):
        return _deny("FORBIDDEN", "Permanent bans require SUPER_ADMIN authorization")
    if acc.get("status") == "locked":
        return _deny("CONFLICT", "Account is security-locked; use User Management unlock workflow", 409)
    try:
        view = apply_restriction(acc, rtype, reason, duration, custom_until, notes, actor)
    except (LookupError, ValueError) as e:
        return _deny("BAD_REQUEST", str(e), 400)
    return jsonify({"data": view})


@security_bp.post("/users/<account_id>/unrestrict")
def unrestrict_user(account_id):
    actor, err = _require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    reason = (body.get("reason") or "").strip() or "unbanned via Security Center"
    store = _store()
    acc = next((a for a in store["accounts"] if a["id"] == account_id), None)
    if not acc:
        return _deny("NOT_FOUND", "account not found", 404)
    allowed, why = _can_manage_target(actor, acc)
    if not allowed:
        return _deny("FORBIDDEN", why)
    try:
        view = lift_restriction(acc["id"], reason, actor)
    except (LookupError, ValueError) as e:
        return _deny("CONFLICT", str(e), 409)
    return jsonify({"data": view})


@security_bp.post("/users/<account_id>/revoke-sessions")
def revoke_sessions(account_id):
    actor, err = _require_admin()
    if err:
        return err
    store = _store()
    acc = next((a for a in store["accounts"] if a["id"] == account_id), None)
    if not acc:
        return _deny("NOT_FOUND", "account not found", 404)
    allowed, why = _can_manage_target(actor, acc)
    if not allowed:
        return _deny("FORBIDDEN", why)
    # Store sessions are stateless (um-session-<id> re-resolved per request against
    # active status) — recording the revocation event documents the intent; a
    # restriction change is what actually kills access.
    acc.setdefault("login_history", []).append({"ts": _now(), "event": "sessions_revoked",
                                                "detail": f"revoked by {actor['id']}"})
    _save_store(store)
    write_audit(actor, "sessions_revoked", target=acc["id"], target_name=acc.get("name", ""),
                reason="security center session revocation")
    return jsonify({"data": {"ok": True, "message": "Store sessions re-resolve against account status; "
                                                  "combine with a restriction to fully cut access."}})


# ── security events ─────────────────────────────────────────────────────────
@security_bp.get("/events")
def list_events():
    actor, err = _require_admin()
    if err:
        return err
    args = request.args
    try:
        page = max(1, int(args.get("page", 1)))
        size = min(100, max(5, int(args.get("page_size", 25))))
    except ValueError:
        return _deny("BAD_REQUEST", "invalid pagination", 400)
    where, vals = ["1=1"], []
    for field, col in (("type", "event_type"), ("severity", "severity"), ("ip", "source_ip")):
        v = (args.get(field) or "").strip()
        if v:
            where.append(f"{col} = ?")
            vals.append(v)
    hours = args.get("hours")
    if hours:
        try:
            cutoff = (datetime.utcnow() - timedelta(hours=max(1, min(24 * 30, int(hours))))).strftime("%Y-%m-%d %H:%M:%S")
            where.append("ts >= ?")
            vals.append(cutoff)
        except ValueError:
            pass
    q = (args.get("q") or "").strip()
    if q:
        where.append("(actor_account LIKE ? OR endpoint LIKE ? OR detail LIKE ? OR source_ip LIKE ?)")
        vals += [f"%{q}%"] * 4
    wsql = " AND ".join(where)
    with _connect() as conn:
        total = int(conn.execute(f"SELECT COUNT(*) c FROM security_events WHERE {wsql}", vals).fetchone()["c"])
        rows = [dict(r) for r in conn.execute(
            f"SELECT * FROM security_events WHERE {wsql} ORDER BY id DESC LIMIT ? OFFSET ?",
            vals + [size, (page - 1) * size])]
    return jsonify({"data": {"rows": rows, "total": total, "page": page, "pageSize": size,
                             "pages": max(1, (total + size - 1) // size)}})


@security_bp.get("/events/<int:event_id>")
def event_detail(event_id):
    actor, err = _require_admin()
    if err:
        return err
    with _connect() as conn:
        row = conn.execute("SELECT * FROM security_events WHERE id = ?", (event_id,)).fetchone()
    if not row:
        return _deny("NOT_FOUND", "event not found", 404)
    ev = dict(row)
    rule = EVENT_RULES.get(ev["event_type"])
    ev["explanation"] = rule[1] if rule else "Recorded security event."
    with _connect() as conn:
        ev["related"] = [dict(r) for r in conn.execute(
            "SELECT id, ts, event_type, severity, source_ip, actor_account FROM security_events"
            " WHERE (correlation_id != '' AND correlation_id = ?) OR (source_ip = ? AND event_type = ?)"
            " ORDER BY id DESC LIMIT 10",
            (ev.get("correlation_id") or "-", ev["source_ip"], ev["event_type"]))]
    return jsonify({"data": ev})


# ── rate limiting monitor ───────────────────────────────────────────────────
@security_bp.get("/ratelimit")
def ratelimit():
    actor, err = _require_admin()
    if err:
        return err
    rules = _rules()
    with _connect() as conn:
        cutoff24 = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        total24 = int(conn.execute("SELECT COUNT(*) c FROM security_events WHERE event_type='rate_limit.violation' AND ts >= ?",
                                   (cutoff24,)).fetchone()["c"])
        top_rules = [dict(r) for r in conn.execute(
            "SELECT detail, COUNT(*) c FROM security_events WHERE event_type='rate_limit.violation' AND ts >= ?"
            " GROUP BY detail ORDER BY c DESC LIMIT 5", (cutoff24,))]
        recent = [dict(r) for r in conn.execute(
            "SELECT id, ts, source_ip, actor_account, endpoint, detail, outcome FROM security_events"
            " WHERE event_type='rate_limit.violation' ORDER BY id DESC LIMIT 25")]
        top_ips = [dict(r) for r in conn.execute(
            "SELECT source_ip, COUNT(*) c FROM security_events WHERE event_type='rate_limit.violation' AND ts >= ?"
            " GROUP BY source_ip ORDER BY c DESC LIMIT 8", (cutoff24,))]
    live = {}
    with _LOCK:
        for rid, bucket in _counters.items():
            rule = next((r for r in rules if r["id"] == rid), None)
            if rule:
                live[rid] = {"activeSources": len(bucket),
                             "limit": rule["limit"], "window": rule["window"]}
    return jsonify({"data": {"rules": [{"id": r["id"], "prefix": r["prefix"], "methods": sorted(r["methods"]) if r["methods"] else "ALL",
                                        "limit": r["limit"], "windowSeconds": r["window"], "note": r["note"],
                                        "live": live.get(r["id"])} for r in rules],
                              "violations24h": total24, "topRules": top_rules, "recent": recent,
                              "topIps": top_ips,
                              "deployment": "single-process in-memory counters; use a shared store (e.g. Redis) before scaling horizontally"}})


# ── IP activity ─────────────────────────────────────────────────────────────
@security_bp.get("/ip")
def ip_activity():
    actor, err = _require_admin()
    if err:
        return err
    with _connect() as conn:
        rows = [dict(r) for r in conn.execute(
            "SELECT source_ip ip, COUNT(*) requests, MIN(ts) firstSeen, MAX(ts) lastSeen,"
            " SUM(CASE WHEN event_type='auth.login_failed' THEN 1 ELSE 0 END) failedAuth,"
            " SUM(CASE WHEN event_type='rate_limit.violation' THEN 1 ELSE 0 END) rateViolations,"
            " SUM(CASE WHEN severity IN ('medium','high','critical') THEN 1 ELSE 0 END) suspicious"
            " FROM security_events WHERE source_ip != '' GROUP BY source_ip ORDER BY requests DESC LIMIT 100")]
        active = [dict(r) for r in conn.execute(
            "SELECT * FROM ip_restrictions WHERE active = 1 ORDER BY id DESC")]
    for r in rows:
        with _connect() as conn:
            accs = conn.execute(
                "SELECT DISTINCT actor_account FROM security_events WHERE source_ip = ? AND actor_account != '' LIMIT 10",
                (r["ip"],)).fetchall()
        r["relatedAccounts"] = [a["actor_account"] for a in accs]
        restr = next((x for x in active if x["ip"] == r["ip"] and x["mode"] == "restrict"), None)
        r["mitigation"] = {"restricted": bool(restr), "expiresAt": restr["expires_at"] if restr else None,
                           "reason": restr["reason"] if restr else None}
    return jsonify({"data": {"rows": rows, "activeRestrictions": active}})


@security_bp.post("/ip/restrict")
def ip_restrict():
    actor, err = _require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    ip = (body.get("ip") or "").strip()
    reason = (body.get("reason") or "").strip()
    hours = body.get("hours", get_settings()["ip_restriction_default_hours"])
    mode = (body.get("mode") or "restrict").lower()
    if mode not in ("restrict", "allow"):
        return _deny("BAD_REQUEST", "mode must be restrict or allow", 400)
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        return _deny("BAD_REQUEST", "valid IPv4 address required", 400)
    if mode == "restrict" and not reason:
        return _deny("BAD_REQUEST", "A reason is required for every IP restriction", 400)
    try:
        hours = min(72, max(1, int(hours)))  # short-lived by design (shared networks)
    except (TypeError, ValueError):
        return _deny("BAD_REQUEST", "hours must be a number", 400)
    expires = (datetime.utcnow() + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ") if mode == "restrict" else None
    with _connect() as conn:
        if mode == "restrict":
            conn.execute("UPDATE ip_restrictions SET active = 0 WHERE ip = ? AND mode = 'restrict'", (ip,))
        conn.execute("INSERT INTO ip_restrictions(ip, mode, reason, created_by, created_at, expires_at, active)"
                     " VALUES (?,?,?,?,?,?,1)", (ip, mode, reason or "monitored exception",
                                                 actor["id"], _now(), expires))
    write_audit(actor, f"ip_{mode}", target=ip, target_name=ip, reason=reason,
                after={"mode": mode, "expiresAt": expires})
    return jsonify({"data": {"ok": True, "ip": ip, "mode": mode, "expiresAt": expires}})


@security_bp.post("/ip/unrestrict")
def ip_unrestrict():
    actor, err = _require_admin()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    ip = (body.get("ip") or "").strip()
    with _connect() as conn:
        cur = conn.execute("UPDATE ip_restrictions SET active = 0 WHERE ip = ? AND active = 1", (ip,))
        changed = cur.rowcount
    if changed:
        write_audit(actor, "ip_unrestricted", target=ip, target_name=ip, reason=body.get("reason", ""))
    return jsonify({"data": {"ok": True, "removed": changed}})


# ── audit history ───────────────────────────────────────────────────────────
@security_bp.get("/audit")
def audit_history():
    actor, err = _require_admin()
    if err:
        return err
    args = request.args
    try:
        page = max(1, int(args.get("page", 1)))
        size = min(100, max(5, int(args.get("page_size", 25))))
    except ValueError:
        return _deny("BAD_REQUEST", "invalid pagination", 400)
    where, vals = ["1=1"], []
    q = (args.get("q") or "").strip()
    if q:
        where.append("(actor LIKE ? OR target LIKE ? OR target_name LIKE ? OR reason LIKE ? OR action LIKE ?)")
        vals += [f"%{q}%"] * 5
    action = (args.get("action") or "").strip()
    if action:
        where.append("action = ?")
        vals.append(action)
    wsql = " AND ".join(where)
    with _connect() as conn:
        total = int(conn.execute(f"SELECT COUNT(*) c FROM security_audit WHERE {wsql}", vals).fetchone()["c"])
        rows = [dict(r) for r in conn.execute(
            f"SELECT * FROM security_audit WHERE {wsql} ORDER BY id DESC LIMIT ? OFFSET ?",
            vals + [size, (page - 1) * size])]
        actions = [r["action"] for r in conn.execute("SELECT DISTINCT action FROM security_audit")]
    return jsonify({"data": {"rows": rows, "total": total, "page": page, "pageSize": size,
                             "pages": max(1, (total + size - 1) // size), "actions": sorted(actions)}})


# ── settings ────────────────────────────────────────────────────────────────
@security_bp.get("/settings")
def read_settings():
    actor, err = _require_admin()
    if err:
        return err
    return jsonify({"data": {"settings": get_settings(), "defaults": DEFAULT_SETTINGS,
                             "canEdit": _is_super(actor), "viewerRole": actor["role"]}})


@security_bp.put("/settings")
def write_settings():
    actor, err = _require_super()
    if err:
        return err
    body = request.get_json(silent=True) or {}
    changes = {}
    for key, value in (body.get("settings") or {}).items():
        if key not in DEFAULT_SETTINGS:
            return _deny("BAD_REQUEST", f"unknown setting: {key}", 400)
        before = get_settings().get(key)
        try:
            if key == "trust_proxy":
                value = bool(value)
            else:
                value = int(value)
                if key.startswith(("login", "auth", "write", "security")):
                    if value < 1 or value > 100000:
                        raise ValueError
                elif key == "ip_restriction_default_hours":
                    if value < 1 or value > 72:
                        raise ValueError
                elif key == "event_retention_days":
                    if value < 7 or value > 365:
                        raise ValueError
                elif key == "suspicious_failed_login_threshold":
                    if value < 3 or value > 50:
                        raise ValueError
        except (TypeError, ValueError):
            return _deny("BAD_REQUEST", f"invalid value for {key}", 400)
        set_setting(key, value)
        changes[key] = {"before": before, "after": value}
    if changes:
        write_audit(actor, "security_settings_changed", target="security-settings",
                    target_name="Security Center settings", reason=body.get("reason", ""),
                    before={k: v["before"] for k, v in changes.items()},
                    after={k: v["after"] for k, v in changes.items()})
        log_event("security.setting_changed", actor_account=actor["id"], outcome="updated",
                  detail=", ".join(changes.keys()))
    return jsonify({"data": {"settings": get_settings(), "changed": list(changes.keys())}})
