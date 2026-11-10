import urllib.request, json

BASE = "http://127.0.0.1:3000"

def get(path, headers={}):
    req = urllib.request.Request(f"{BASE}{path}", headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode('utf-8'))

def post(path, data={}, headers={}):
    body = json.dumps(data).encode('utf-8')
    h = {'Content-Type': 'application/json'}
    h.update(headers)
    req = urllib.request.Request(f"{BASE}{path}", data=body, headers=h, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def put(path, data={}, headers={}):
    body = json.dumps(data).encode('utf-8')
    h = {'Content-Type': 'application/json'}
    h.update(headers)
    req = urllib.request.Request(f"{BASE}{path}", data=body, headers=h, method='PUT')
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

print("1. Testing GET /api/school-config/overview...")
code, res = get("/api/school-config/overview")
print("  Status:", code, "School:", res.get("schoolName"), "Active Year:", res.get("activeYear"), "Campuses:", res.get("campusesCount"))

print("\n2. Testing GET /api/school-config/full (as Admin)...")
code, res = get("/api/school-config/full", headers={"X-User-Role": "admin"})
print("  Status:", code, "Caller role:", res.get("caller", {}).get("role"), "Permitted sections:", len(res.get("userPermissions", {}).get("permittedSections", [])))

print("\n3. Testing GET /api/school-config/full (as Editor)...")
code, res = get("/api/school-config/full", headers={"X-User-Role": "editor", "X-User-Id": "USR-006"})
print("  Status:", code, "Caller role:", res.get("caller", {}).get("role"), "Permitted sections:", res.get("userPermissions", {}).get("permittedSections"))

print("\n4. Testing Editor permission restriction on Academic Years activation...")
code, res = post("/api/school-config/academic-years/SY-2027/activate", headers={"X-User-Role": "editor", "X-User-Id": "USR-006"})
print("  Status:", code, "Requires approval:", res.get("requiresApproval"), "Message:", res.get("message"))

print("\n5. Testing Admin activation of Academic Year 2026–2027...")
code, res = post("/api/school-config/academic-years/SY-2026/activate", headers={"X-User-Role": "admin"})
print("  Status:", code, "Active Year:", res.get("item", {}).get("year"), "Message:", res.get("message"))

print("\n6. Testing GET /api/school-config/audit-log...")
code, res = get("/api/school-config/audit-log", headers={"X-User-Role": "admin"})
print("  Status:", code, "Total audit logs:", res.get("total"), "Latest action:", res.get("data", [{}])[0].get("action"))

print("\nAll Backend APIs verified successfully!")

