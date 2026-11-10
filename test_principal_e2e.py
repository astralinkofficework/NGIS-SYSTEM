import sys, os
import server

client = server.app.test_client()
failures = []

def test(name, condition, details=""):
    if condition:
        print(f" PASS: {name}")
    else:
        print(f" FAIL: {name} - {details}")
        failures.append((name, details))

print("=" * 60)
print("PRINCIPAL CENTRAL MANAGEMENT SYSTEM - END-TO-END VERIFICATION")
print("=" * 60)

# 1. Page HTTP status tests
pages = [
    '/pages/principal/principal.html',
    '/pages/principal/principal-classes.html',
    '/pages/principal/principal-departments.html',
    '/pages/principal/principal-timetables.html',
    '/pages/principal/principal-attendance.html',
    '/pages/principal/principal-services.html',
    '/pages/principal/principal-lost-found.html',
    '/pages/principal/principal-teacher-profiles.html',
    '/pages/principal/principal-student-profiles.html',
    '/pages/principal/principal-reports.html',
    '/pages/principal/principal-activity.html'
]

for p in pages:
    res = client.get(p)
    test(f"Page Load: {p}", res.status_code == 200, f"Status code: {res.status_code}")

# 2. Classes API (Teacher Portal Oversight: My Class)
res = client.get('/api/classes')
test("GET /api/classes returns 200", res.status_code == 200)
test("GET /api/classes has data", len(res.json.get('data', [])) >= 5)

res_put_cls = client.put('/api/classes/cls-10a', json={'name': 'Grade 10A Honors', 'room': 'Room 302-H'})
test("PUT /api/classes/cls-10a updates class", res_put_cls.status_code == 200)
cls_updated = next((c for c in client.get('/api/classes').json['data'] if c['id'] == 'cls-10a'), None)
test("Class update persisted in DB", cls_updated and cls_updated.get('name') == 'Grade 10A Honors')

# 3. Departments API (Teacher Portal Oversight: Department)
res = client.get('/api/departments')
test("GET /api/departments returns 200", res.status_code == 200)
test("GET /api/departments has 7 divisions", len(res.json.get('data', [])) == 7)

res_put_dept = client.put('/api/departments/dept-mat', json={'head': 'Dr. Sarah Jenkins PhD', 'syllabusCompliance': 99})
test("PUT /api/departments/dept-mat updates department", res_put_dept.status_code == 200)
dept_updated = next((d for d in client.get('/api/departments').json['data'] if d['id'] == 'dept-mat'), None)
test("Department update persisted", dept_updated and dept_updated.get('syllabusCompliance') == 99)

# 4. Assignments API (Teacher Portal Oversight: Assignment Student)
res = client.get('/api/assignments')
test("GET /api/assignments returns 200", res.status_code == 200)
test("GET /api/assignments has data", len(res.json.get('data', [])) >= 3)

res_put_asgn = client.put('/api/assignments/asgn-001', json={'title': 'Math Ch.8: Differential Equations Problem Set (Extended)'})
test("PUT /api/assignments/asgn-001 updates assignment", res_put_asgn.status_code == 200)

# 5. Timetables API (Teacher & Student Timetable Management)
res = client.get('/api/timetables')
test("GET /api/timetables returns 200", res.status_code == 200)

# 5a. Save slot without conflict
res_slot = client.post('/api/timetables/slot', json={
    'classId': 'cls-10a',
    'className': 'Grade 10A',
    'day': 'Friday',
    'period': 6,
    'subject': 'Principal Academic Review',
    'teacherId': 'TCH-2024-045',
    'teacherName': 'Dr. Ly Bunheng',
    'room': 'Conference Hall A'
})
test("POST /api/timetables/slot valid slot", res_slot.status_code == 200)

# 5b. Conflict Guard Check: try booking the same room at the same time for a different class
res_conflict = client.post('/api/timetables/slot', json={
    'classId': 'cls-11b',
    'className': 'Grade 11B',
    'day': 'Friday',
    'period': 6,
    'subject': 'History Discussion',
    'teacherId': 'TCH-2024-043',
    'teacherName': 'Sovannarith Khun',
    'room': 'Conference Hall A'
})
test("POST /api/timetables/slot conflict caught (Room double-booked)", res_conflict.status_code == 409)

# 6. Attendance API (Attendance Oversight & Corrections)
res_att = client.get('/api/attendance?classId=all')
test("GET /api/attendance?classId=all returns student records", res_att.status_code == 200 and len(res_att.json.get('data', [])) >= 27)

res_corr_fail = client.post('/api/principal/attendance/correct', json={
    'studentId': '2026-STD-0142',
    'reason': ''
})
test("POST /api/principal/attendance/correct rejects empty reason", res_corr_fail.status_code == 400)

res_corr_ok = client.post('/api/principal/attendance/correct', json={
    'studentId': '2026-STD-0142',
    'date': '2026-11-03',
    'newStatus': 'excused',
    'reason': 'Medical certification verified by Principal'
})
test("POST /api/principal/attendance/correct updates status with written reason", res_corr_ok.status_code == 200)

# 7. Service Requests API (Student Service Hub)
res_sr = client.get('/api/service-requests')
test("GET /api/service-requests returns 200", res_sr.status_code == 200 and len(res_sr.json.get('data', [])) >= 8)

res_sr_put = client.put('/api/service-requests/SR-1001', json={
    'status': 'approved',
    'comments': [{'by': 'Dr. Ly Bunheng (Principal)', 'date': '2026-11-03', 'text': 'Approved with official school seal.'}]
})
test("PUT /api/service-requests/SR-1001 approves request", res_sr_put.status_code == 200)

# 8. Lost & Found API (Student Portal Oversight: Lost and Found)
res_lf = client.get('/api/lost-found')
test("GET /api/lost-found returns 200", res_lf.status_code == 200 and len(res_lf.json.get('data', [])) >= 10)

first_item_id = res_lf.json['data'][0]['id']
res_lf_put = client.put(f'/api/lost-found/{first_item_id}', json={
    'custodyLocation': 'Principal Office Secure Storage'
})
test(f"PUT /api/lost-found/{first_item_id} updates custody", res_lf_put.status_code == 200)

# Test creating and then deleting an inappropriate post
new_item_res = client.post('/api/lost-found', json={
    'title': 'Test Item To Remove',
    'type': 'lost',
    'category': 'other',
    'campus': 'Sensok',
    'location': 'Hallway',
    'description': 'Test',
    'reporterName': 'Test Student',
    'reporterId': '2026-STD-9999',
    'reporterRole': 'student',
    'contactMethod': 'chat'
})
if new_item_res.status_code in (200, 201):
    test_id = new_item_res.json['data']['id']
    del_res = client.delete(f'/api/lost-found/{test_id}')
    test("DELETE /api/lost-found/<id> removes inappropriate post", del_res.status_code == 200)
else:
    test("DELETE /api/lost-found/<id>", False, "Could not create test post")

print("=" * 60)
if failures:
    print(f"FAILED TESTS: {len(failures)}")
    for f in failures:
        print(f" - {f[0]}: {f[1]}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

