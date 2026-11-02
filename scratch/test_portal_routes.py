import urllib.request

urls = [
    'http://127.0.0.1:3000/pages/principal/principal.html',
    'http://127.0.0.1:3000/pages/principal/principal-approvals.html',
    'http://127.0.0.1:3000/pages/principal/principal-reports.html',
    'http://127.0.0.1:3000/pages/principal/principal-profile.html',
    'http://127.0.0.1:3000/pages/teacher/teacher.html',
    'http://127.0.0.1:3000/pages/teacher/teacher-grades.html',
    'http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html',
    'http://127.0.0.1:3000/pages/student/student.html',
    'http://127.0.0.1:3000/pages/student/student-grades.html',
    'http://127.0.0.1:3000/api/principal/stats',
    'http://127.0.0.1:3000/api/principal/audit',
    'http://127.0.0.1:3000/api/academic/gradebook/clearance-status?classId=cls-10a'
]

passed = 0
failed = 0

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'Authorization': 'Bearer mock-jwt-token-principal'})
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print(f"[OK 200] {u}")
                passed += 1
            else:
                print(f"[STATUS {resp.status}] {u}")
                failed += 1
    except Exception as e:
        print(f"[FAIL] {u} -> {e}")
        failed += 1

print(f"\nResult: {passed} passed, {failed} failed out of {len(urls)}.")

