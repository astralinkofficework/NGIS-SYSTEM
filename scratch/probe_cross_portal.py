"""Probe: does validate() now detect cross-portal exposure?

Visibility is NOT authorization. A student sidebar must never point at an
admin/teacher/principal page, and vice-versa.
"""
import json
import urllib.request

BASE = "http://127.0.0.1:3000"
ROLE_HDR = {"X-User-Email": "admin@ngis.edu.kh", "X-User-Role": "admin",
            "Content-Type": "application/json"}


def validate(portal, links):
    payload = {"groups": [{"id": "g1", "label": "Probe Group", "links": links}]}
    body = json.dumps({"portal": portal, "payload": payload}).encode()
    req = urllib.request.Request(BASE + "/api/nav/validate", data=body,
                                 headers=ROLE_HDR, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read().decode())
    return data["data"]["findings"]


def has(findings, code):
    return [f for f in findings if f.get("code") == code]


results = []

# 1) Student sidebar -> admin page MUST be flagged as cross-portal exposure.
leak = validate("student", [
    {"id": "x1", "label": "Admin Leak", "icon": "ph ph-warning",
     "href": "pages/admin/admin.html"},
])
results.append(("student->admin flagged", len(has(leak, "cross_portal_exposure")) == 1))
results.append(("student->admin is HIGH",
                all(f["severity"] == "high" for f in has(leak, "cross_portal_exposure"))))

# 2) Legit student href MUST NOT be flagged.
legit = validate("student", [
    {"id": "s1", "label": "My Classes", "icon": "ph ph-book",
     "href": "pages/student/student-classes.html"},
])
results.append(("legit student href clean", len(has(legit, "cross_portal_exposure")) == 0))

# 3) Shared pages are allowed across portals.
shared = validate("student", [
    {"id": "sh1", "label": "Profile", "icon": "ph ph-user",
     "href": "pages/shared/profile.html"},
])
results.append(("shared page allowed", len(has(shared, "cross_portal_exposure")) == 0))

# 4) Query/hash + leading slash normalization -> still flagged.
norms = validate("teacher", [
    {"id": "n1", "label": "Deep Link", "icon": "ph ph-link",
     "href": "/pages/principal/principal.html?tab=x#top"},
])
results.append(("normalized deep link flagged", len(has(norms, "cross_portal_exposure")) == 1))

# 5) Teacher->admin flagged too.
t2a = validate("teacher", [
    {"id": "t1", "label": "Admin", "icon": "ph ph-gear",
     "href": "pages/admin/admin.html"},
])
results.append(("teacher->admin flagged", len(has(t2a, "cross_portal_exposure")) == 1))

fails = [n for n, ok in results if not ok]
for n, ok in results:
    print(("PASS " if ok else "FAIL ") + n)
print("\n%d/%d passed" % (len(results) - len(fails), len(results)))
if fails:
    raise SystemExit("FAILURES: " + ", ".join(fails))
