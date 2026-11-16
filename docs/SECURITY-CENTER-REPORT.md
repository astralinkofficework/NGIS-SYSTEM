# NGIS-SYSTEM — Admin Security Center & Threat Monitoring (MVP)

**Status:** Complete and validated · 2026-11-16
**Page:** `pages/admin/admin-security.html` · **Backend:** `security_api.py` (+ `server.py` wiring)

---

## 1. What was built

### Backend — `security_api.py` (blueprint `/api/security` + `data/security.sqlite3`)

| Capability | Implementation |
|---|---|
| **User restrictions** | Suspend (1–72h numeric or presets `1h/24h/7d/30d`/custom/indefinite) and permanent **ban** (SUPER_ADMIN only), stored in the **authoritative** `data/user_accounts.json` (`status: suspended` + `security_restriction` meta + preserved `restriction_history`). Enforced by existing sign-in gate *before* credential checks. |
| **Restore (unban)** | Lifts only security-center restrictions. `disabled` / `locked` / `pending_activation` lifecycle states are never overridden — those belong to User Management. |
| **Automatic expiry** | Throttled (60s) sweep in app `before_request` restores elapsed suspensions; retention sweep prunes events older than `event_retention_days`. |
| **Security events** | SQLite `security_events` with a **documented severity taxonomy** (`EVENT_RULES`): `auth.login_failed` (low), `auth.account_rejected` (medium), `auth.unauthorized` (low), `auth.permission_denied` (medium), `rate_limit.violation` (medium), `ip.blocked` (high), `restriction.applied/removed/auto_expired`, `security.setting_changed` (informational), `auth.login_success` (informational). **Unknown event types are never recorded.** |
| **Rate limiting** | First in codebase. Most-specific-prefix-wins per-IP counters, thread-safe, in-memory: `auth-login` 30/5min (+8/5min **per identifier** brute-force guard, NAT-safe), `auth-other` 30/min, `write-api` 600/min, `security-api` 240/min → **429 + `Retry-After`** + violation event. |
| **IP restrictions** | Short-lived (default 24h, max 72h), reason required, IPv4-validated. Blocks skip `/api/security` so admins can always undo. `trust_proxy` setting gates `X-Forwarded-For` (off by default — anti-spoofing). |
| **Suspicious detection** | Rule-based only: recent event counts per account/IP (failed logins, rate hits), surfaced as "recent activity" chips. **No automatic account lockouts** beyond the pre-existing 5-failed-login lock. |
| **Audit history** | Append-only `security_audit` table — actor, role, action, target, reason, before/after JSON (capped/redacted), outcome, correlation id. |
| **Settings** | `GET` any admin; `PUT` **SUPER_ADMIN only**, range-validated, audited. `trust_proxy` toggle, per-rule budgets, retention, thresholds. |
| **Privacy** | Passwords/tokens/cookies never logged; keys matching `password|token|secret|cookie|authorization|session` redacted; 400-char caps. |

### Server wiring — `server.py`
- `security_api.install(app)` after schema init (fail-soft with console notice).
- Store-path login outcomes instrumented: success → `auth.login_success`; invalid credentials → `auth.login_failed`; suspended/locked/pending rejections → `auth.account_rejected`. Demo-path logins intentionally not logged (noise avoidance).

### Frontend — `pages/admin/admin-security.html`
7 tabs (Overview · User Restrictions · Security Events · Rate Limiting · IP Activity · Audit History · Security Settings), hero banner, server-side pagination everywhere, search/role/status/type/severity/action filters, restrict & restore dialogs with **required reason**, account detail drawer (restriction meta + history + sign-ins + related events), event detail modal (explanation + correlated events), settings form with SUPER_ADMIN gating (read-only + lock banner for others), NGIS semantic severity/status badges, toasts, empty/loading states, responsive 320–1920 (no horizontal overflow), reduced-motion support.

### Navigation
- Admin sidebar → SYSTEM & SECURITY → **Security Center** (`assets/js/layout.js`)
- Super Admin sidebar → GOVERNANCE & SECURITY → **Security Center**

---

## 2. Test results (all passing)

**Permission guards (403s verified live):**
- Demo admin restricting own account → `Administrators cannot restrict their own account`
- Regular ADMIN → ADMIN/PRINCIPAL targets → `Only SUPER_ADMIN actors may restrict Admin accounts`
- Regular ADMIN ban type → `Permanent bans require SUPER_ADMIN authorization`
- Student/teacher demo tokens on any `/api/security` endpoint → `FORBIDDEN`
- Demo admin `PUT /settings` → SUPER_ADMIN only; SUPER_ADMIN via `X-Actor` → 200 + audited
- Missing reason → 400; last-active-admin guard present (`_guard_last_admin` semantics)

**Restriction lifecycle:**
suspend USR-DMO-107 → store `status: suspended` + meta written → sign-in attempt → **403 ACCOUNT_SUSPENDED** (checked *before* credentials) → `auth.account_rejected` event recorded → restore → `active`, restriction cleared, history preserved. SUPER_ADMIN ban → `banned`, no expiry → restore OK.

**Rate limiting:** exactly 30×200 then **429** with `Retry-After: 60`; each breach logged (`rule auth-other limit 30/60s — observed N`); monitor tab shows rules + live counters + violations24h.

**IP restrictions:** block `203.0.113.66` (TEST-NET) → `/api/health` 403 `IP_RESTRICTED`, `/api/security` still 200 (undo path), `ip.blocked` (high) event, unrestrict → 200 again.

**UI E2E (browser):** tabs switch, facets hydrate, search/pagination (302 accounts / 38 pages), restrict dialog → row flips to `suspended` with Restore button → restore → `active`; event detail modal with explanation; settings gated for ADMIN viewer (fields + save disabled).

**Responsive:** no horizontal overflow at 320 / 768 / 1440 on Overview, Users, Settings; screenshots in `.testshots/`.

---

## 3. Bugs found & fixed during validation

1. **`set_setting` stale-cache bug** — `_settings_cache = None` without `global` declaration was a local no-op; settings writes appeared ignored until process restart. Fixed with `global _settings_cache`.
2. **Numeric duration crash** — `duration.lower()` on an int payload → `AttributeError` 500. Endpoint now normalizes via `str(...)`, and `apply_restriction` accepts numeric hours (1–72) alongside presets.
3. **Environment:** two stale `python server.py` instances were both bound to :3000, splitting requests between old and new code — killed and restarted single instance with log capture (`server-dev.log`).
4. UI: restrict dialog now sends `Number(duration)` (backend also accepts numeric — both sides fixed).

---

## 4. Implemented vs. missing infrastructure (honesty ledger)

**Greenfield (did not exist before this task):** IP capture (`remote_addr` was never used), rate limiting (none existed), centralized security events, IP restrictions, security-specific audit store, suspension expiry.

**Documented limitations:**
- **Rate limiter is single-process in-memory.** Multi-process/horizontal scaling requires a shared store (Redis). Surfaced verbatim in the Rate Limiting tab banner and API.
- **IP "first seen" is derived from recorded security events** — an IP with no security events yet has no history row; this is event-derived analytics, not full request logging (deliberately avoided for privacy/size).
- **Session revocation for restricted accounts is ceremonial**: tokens are stateless `um-session-<id>` re-resolved per request, so a suspended account's token dies instantly at next use anyway — the separate "revoke sessions" step adds an audit record rather than a technical invalidation.
- **Suspicious detection is rule-based only**; automatic responses are limited to the pre-existing 5-failure lockout plus restriction expiry. No auto-IP-blocking (avoided: shared campus NAT false positives).
- Real (non-demo) SUPER_ADMIN sign-in requires a provisioned credential (`password_hash`); today only `admin@ngis.edu.kh` (USR-001) exists and signs in via the demo persona, which the Security Center treats as ADMIN-but-not-ban-capable unless acting through the store identity (`X-Actor` / `um-session-`). Ban capability is therefore exercised via the store-identity path in tests.

---

## 5. Key files

- `security_api.py` — blueprint, hooks, store integration, events/audit/ratelimit/IP/settings
- `server.py` — install wiring + login outcome instrumentation
- `pages/admin/admin-security.html` — the 7-tab center
- `assets/js/layout.js` — sidebar entries (admin + superadmin)
- `data/security.sqlite3` (`.data/`) — events / audit / ip_restrictions / settings
- `.testshots/sec-*.png` — validation screenshots
