"""NGIS Global Sidebar Manager - API lifecycle verification.

Exercises the real backend store: read -> draft -> validate -> publish ->
published view -> versions -> restore -> defaults reset. Fails loudly.
Cleans up afterwards (restores factory defaults for the test portal).
"""
import json
import sys
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:3000"
PORTAL = "admin"

results = []
errors = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    if not cond:
        errors.append(name + (" :: " + detail if detail else ""))


def req(method, path, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}


def main():
    # 0. Baseline
    st, res = req("GET", "/api/nav/portals")
    check("GET /api/nav/portals 200", st == 200, "status=%s" % st)
    portals = [p["portal"] for p in (res.get("data") or [])]
    check("4 portals present", sorted(portals) == sorted(["admin", "principal", "teacher", "student"]),
          "got=%s" % portals)

    st, res = req("GET", "/api/nav/routes")
    check("GET /api/nav/routes 200", st == 200, "status=%s" % st)
    routes = res.get("data") or []
    check("route registry non-empty", len(routes) > 10, "count=%d" % len(routes))
    check("index.html registered", "index.html" in routes)

    st, res = req("GET", "/api/nav/config?portal=" + PORTAL)
    check("GET config 200", st == 200)
    state = res.get("data") or {}
    pub = state.get("published") or {}
    groups0 = pub.get("groups") or []
    check("published groups present", len(groups0) > 0, "groups=%d" % len(groups0))

    # 1. Draft with an extra QA group + a hidden item
    payload = {
        "brand": pub.get("brand", "Admin"),
        "meta": pub.get("meta", ""),
        "groups": json.loads(json.dumps(groups0)),
    }
    payload["groups"].append({
        "id": "qa-grp", "label": "QA Group",
        "links": [
            {"id": "qa-link", "label": "QA Link", "icon": "science",
             "href": "pages/admin/admin.html"},
            {"id": "qa-hidden", "label": "QA Hidden", "visible": False,
             "href": "pages/admin/admin.html"},
        ],
    })
    st, res = req("POST", "/api/nav/draft", {"portal": PORTAL, "payload": payload})
    check("POST draft 200", st == 200, "status=%s body=%s" % (st, res.get("error")))

    st, res = req("GET", "/api/nav/config?portal=" + PORTAL)
    draft = (res.get("data") or {}).get("draft") or {}
    dgroups = draft.get("groups") or []
    check("draft persisted with qa-grp", any(g.get("id") == "qa-grp" for g in dgroups),
          "draft groups=%d" % len(dgroups))

    # 2. Validate
    st, res = req("POST", "/api/nav/validate", {"portal": PORTAL, "payload": payload})
    findings = (res.get("data") or {}).get("findings") or []
    highs = [f for f in findings if f.get("severity") == "high"]
    check("validate no high findings", len(highs) == 0, "highs=%s" % highs)

    # 3. Publish
    st, res = req("POST", "/api/nav/publish", {"portal": PORTAL, "summary": "QA lifecycle test"})
    check("POST publish 200", st == 200, "status=%s body=%s" % (st, res.get("error")))
    version_id = ((res.get("data") or {}).get("version_id"))
    check("publish returns version_id", bool(version_id), "vid=%s" % version_id)

    # 4. Published view reflects the change
    st, res = req("GET", "/api/nav/published?portal=" + PORTAL)
    pg = ((res.get("data") or {}).get("groups") or [])
    check("published contains qa-grp", any(g.get("id") == "qa-grp" for g in pg))
    qa = next((g for g in pg if g.get("id") == "qa-grp"), None)
    if qa:
        check("published preserves hidden flag",
              any(l.get("id") == "qa-hidden" and l.get("visible") is False for l in qa.get("links", [])))

    # 5. Version history
    st, res = req("GET", "/api/nav/versions?portal=" + PORTAL)
    versions = res.get("data") or []
    check("version snapshot recorded", len(versions) >= 1, "versions=%d" % len(versions))

    # 6. Restore previous version (removes qa-grp)
    if version_id:
        st, res = req("POST", "/api/nav/restore", {"version_id": version_id})
        check("POST restore 200", st == 200, "status=%s body=%s" % (st, res.get("error")))
        st, res = req("GET", "/api/nav/published?portal=" + PORTAL)
        pg2 = ((res.get("data") or {}).get("groups") or [])
        check("restore removed qa-grp", not any(g.get("id") == "qa-grp" for g in pg2))

    # 7. Audit log
    st, res = req("GET", "/api/nav/audit?portal=" + PORTAL + "&limit=20")
    audit = res.get("data") or []
    check("audit log has entries", len(audit) >= 1, "entries=%d" % len(audit))

    # 8. Reset to factory defaults (cleanup)
    st, res = req("POST", "/api/nav/defaults", {"portal": PORTAL})
    check("POST defaults 200", st == 200, "status=%s body=%s" % (st, res.get("error")))

    # 9. Health after cleanup
    for p in ["admin", "principal", "teacher", "student"]:
        st, res = req("GET", "/api/nav/health?portal=" + p)
        c = (res.get("data") or {}).get("counts") or {}
        check("health %s high==0" % p, c.get("high", 0) == 0, "counts=%s" % c)

    # 10. Permissions: non-admin cannot manage
    r = urllib.request.Request(BASE + "/api/nav/config?portal=admin", method="GET")
    r.add_header("X-User-Email", "student@ngis.edu.kh")
    r.add_header("X-User-Role", "student")
    try:
        with urllib.request.urlopen(r, timeout=10) as resp:
            st = resp.status
    except urllib.error.HTTPError as e:
        st = e.code
    check("non-admin blocked (403)", st == 403, "status=%s" % st)


main()

print("=" * 60)
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (("  ->  " + detail) if detail and not ok else ""))
print("=" * 60)
print("TOTAL %d  PASSED %d  FAILED %d" % (len(results), sum(1 for _, ok, _ in results if ok), len(errors)))
sys.exit(1 if errors else 0)
