"""Smoke-test the PROFILE HUB endpoints added to server.py."""
import io
import json
import urllib.request

BASE = "http://127.0.0.1:3000"
TOKEN = "mock-jwt-token-principal"


def req(method, path, body=None, headers=None, files=None):
    hdrs = {"Authorization": "Bearer " + TOKEN}
    data = None
    if headers:
        hdrs.update(headers)
    if files is not None:
        boundary = "----ngistestboundary"
        parts = []
        for k, v in (body or {}).items():
            parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (boundary, k, v)).encode())
        for k, (fname, blob, mime) in files.items():
            parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n' % (boundary, k, fname, mime)).encode())
            parts.append(blob + b"\r\n")
        parts.append(("--%s--\r\n" % boundary).encode())
        data = b"".join(parts)
        hdrs["Content-Type"] = "multipart/form-data; boundary=" + boundary
    elif body is not None:
        data = json.dumps(body).encode()
        hdrs.setdefault("Content-Type", "application/json")
    r = urllib.request.Request(BASE + path, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}


ok = True


def check(name, cond, detail=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name + ("  " + str(detail)[:160] if detail else ""))
    if not cond:
        ok = False


# roster lists still work
st, body = req("GET", "/api/principal/roster/teachers")
check("roster teachers", st == 200 and body.get("data"), st)
tid = body["data"][0]["id"] if body.get("data") else "T-001"

st, body = req("GET", "/api/principal/roster/students")
sid = body["data"][0]["id"] if body.get("data") else None
check("roster students", st == 200 and sid, st)

# teacher profile detail
st, body = req("GET", "/api/principal/roster/teachers/" + tid)
d = body.get("data", {})
check("teacher profile " + tid, st == 200 and d.get("id") == tid and "documents" in d and "activity" in d,
      "keys=%s docs=%d act=%d" % (sorted(k for k in d if k in ('subjects','classesTaught','homeroom','adviseeCount','phone','employmentType','contractEnd','certifications','pendingGradeRecords')), len(d.get("documents", [])), len(d.get("activity", []))))

# student profile aggregate
st, body = req("GET", "/api/principal/roster/students/" + sid)
d = body.get("data", {})
need = ("grades", "attendance", "guardian", "serviceRequests", "transcripts", "documents", "activity", "advisorName")
check("student profile " + sid, st == 200 and all(k in d for k in need),
      "missing=%s grades=%d att=%s" % ([k for k in need if k not in d], len(d.get("grades", [])), bool(d.get("attendance"))))

# docs: list empty, upload pdf-ish, list, delete
st, body = req("GET", "/api/principal/profile-docs?ownerType=teacher&ownerId=" + tid)
check("docs list", st == 200 and isinstance(body.get("data"), list), st)

pdf_blob = b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF"
st, body = req("POST", "/api/principal/profile-docs",
               body={"ownerType": "teacher", "ownerId": tid, "category": "Contract", "note": "Smoke test"},
               files={"file": ("contract test.pdf", pdf_blob, "application/pdf")})
doc_id = (body.get("data") or {}).get("id")
check("docs upload", st == 200 and doc_id and (body["data"].get("sizeKB", 0) >= 1), body)

st, body = req("GET", "/api/principal/profile-docs?ownerType=teacher&ownerId=" + tid)
check("docs list after upload", st == 200 and any(x.get("id") == doc_id for x in body.get("data", [])), st)

# upload the file URL is downloadable
if doc_id:
    import urllib.request as ur
    url = BASE + next(x["fileUrl"] for x in body.get("data", []) if x.get("id") == doc_id)
    try:
        blob = ur.urlopen(url).read()
        check("doc file served", blob.startswith(b"%PDF"), len(blob))
    except Exception as e:
        check("doc file served", False, e)

# bad extension rejected
st, body = req("POST", "/api/principal/profile-docs",
               body={"ownerType": "teacher", "ownerId": tid},
               files={"file": ("evil.exe", b"MZ", "application/octet-stream")})
check("reject .exe", st != 200 and (body.get("error") or {}).get("code") == "BAD_FILE_TYPE", body)

# oversize rejected
st, body = req("POST", "/api/principal/profile-docs",
               body={"ownerType": "teacher", "ownerId": tid},
               files={"file": ("big.pdf", b"%PDF" + b"0" * (5 * 1024 * 1024), "application/pdf")})
check("reject >5MB", st != 200 and (body.get("error") or {}).get("code") == "FILE_TOO_LARGE", body)

# delete
st, body = req("DELETE", "/api/principal/profile-docs/" + (doc_id or "nope"))
check("docs delete", st == 200, body)

# activity should now include upload/delete audit events
st, body = req("GET", "/api/principal/roster/teachers/" + tid)
acts = [a.get("action") for a in body.get("data", {}).get("activity", [])]
check("audits in activity", "PROFILE_DOCUMENT_UPLOADED" in acts or "PROFILE_DOCUMENT_DELETED" in acts, acts[:6])

# admin token also allowed (RBAC)
st, body = req("GET", "/api/principal/roster/teachers/" + tid, headers={"Authorization": "Bearer mock-jwt-token-admin"})
check("admin role allowed", st == 200, st)

# teacher token forbidden
st, body = req("GET", "/api/principal/roster/teachers/" + tid, headers={"Authorization": "Bearer mock-jwt-token-teacher"})
check("teacher role forbidden", st in (401, 403), st)

# 404 unknown owner
st, body = req("GET", "/api/principal/roster/teachers/T-9999")
check("unknown teacher 404", st == 404, st)

print("\nRESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
