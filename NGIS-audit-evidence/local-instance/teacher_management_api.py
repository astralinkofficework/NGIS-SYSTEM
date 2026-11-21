"""
Teacher Management API module for NGIS ERP.
Powers the 8 Teacher Management sub-modules for Admin and Principal portals:
1. Teacher Profile (Directory & Profile View)
2. Verify Teacher Update (Profile Change Verification & Diff Audit)
3. Teaching Assignment (Subject & Class Allocations, Workload Balancer)
4. Homeroom Teacher Assign (Homeroom Allocation, Student Roster & Conflict Check)
5. Teacher Attendance (Administrative Attendance, Terminal Logs & Excuses)
6. Commendation (Faculty Awards, Honors & Issuing Authority Citations)
7. Discipline (Confidential Conduct Cases, Severity Levels & Hearings)
8. Input Teacher Efforts (Documented Contributions, Extra Duties & Point Logging)
"""

import os
import json
from datetime import datetime
from flask import request, jsonify

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def _load_json(filename, default):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default

def _save_json(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

# Base enriched faculty roster
FALLBACK_TEACHERS = [
    {
        "id": "TCH-2024-042",
        "name": "Dr. Sarah Jenkins",
        "email": "teacher@ngis.edu.kh",
        "phone": "+855 12 888 999",
        "department": "Mathematics",
        "position": "Head of Mathematics Department",
        "subjects": ["Advanced Mathematics", "Calculus I", "AP Biology"],
        "classes": ["10A", "11B", "11C"],
        "homeroom": "10A",
        "status": "active",
        "avatar": "https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-015",
        "name": "Dr. Pov Sophea",
        "email": "p.sophea@ngis.edu.kh",
        "phone": "+855 12 777 666",
        "department": "Science",
        "position": "Head of Science Department",
        "subjects": ["Physics & Lab", "AP Physics"],
        "classes": ["10A", "10B", "11A"],
        "homeroom": "10B",
        "status": "active",
        "avatar": "https://images.pexels.com/photos/3769021/pexels-photo-3769021.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-023",
        "name": "Ms. Rin Lina",
        "email": "r.lina@ngis.edu.kh",
        "phone": "+855 11 555 444",
        "department": "English",
        "position": "Head of English Department",
        "subjects": ["English Literature", "AP English"],
        "classes": ["9A", "10A", "11A"],
        "homeroom": "11A",
        "status": "active",
        "avatar": "https://images.pexels.com/photos/1181685/pexels-photo-1181685.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-031",
        "name": "Mr. Chhem Sokha",
        "email": "c.sokha@ngis.edu.kh",
        "phone": "+855 12 444 333",
        "department": "Khmer Studies",
        "position": "Head of Khmer Studies Department",
        "subjects": ["Khmer Studies", "Khmer Literature"],
        "classes": ["10A", "11B"],
        "homeroom": "11B",
        "status": "active",
        "avatar": "https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-055",
        "name": "Ms. Li Wei",
        "email": "l.wei@ngis.edu.kh",
        "phone": "+855 12 333 222",
        "department": "Chinese Language",
        "position": "Head of Chinese Department",
        "subjects": ["Mandarin Chinese I", "Mandarin Chinese II", "HSK Prep"],
        "classes": ["10A", "10B"],
        "homeroom": None,
        "status": "active",
        "avatar": "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-068",
        "name": "Mr. John Vance",
        "email": "j.vance@ngis.edu.kh",
        "phone": "+855 12 222 111",
        "department": "Humanities & Social Sciences",
        "position": "Head of Humanities Department",
        "subjects": ["World History", "Economics", "Sociology"],
        "classes": ["10B", "11A"],
        "homeroom": None,
        "status": "active",
        "avatar": "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-074",
        "name": "Coach Samreth Bora",
        "email": "s.bora@ngis.edu.kh",
        "phone": "+855 12 111 000",
        "department": "Arts & Physical Education",
        "position": "Head of Arts & Physical Education",
        "subjects": ["Physical Education", "Athletics & Fitness"],
        "classes": ["10A", "10B", "11A"],
        "homeroom": None,
        "status": "active",
        "avatar": "https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=80"
    },
    {
        "id": "TCH-2024-089",
        "name": "Muthukumaran Pakkirisamy",
        "email": "m.pakkirisamy@ngis.edu.kh",
        "phone": "+855 12 666 555",
        "department": "ICT & Computer Science",
        "position": "Head of ICT & Computer Science",
        "subjects": ["Computer Science & Coding", "Robotics & AI"],
        "classes": ["10A", "11C"],
        "homeroom": "11C",
        "status": "active",
        "avatar": "https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=80"
    }
]

def register_teacher_mgmt_routes(app, DB):
    """Register all REST endpoints for Teachers Management."""

    # Ensure DB['teachers'] contains full faculty list
    existing_ids = {t['id'] for t in DB.get('teachers', [])}
    for fb in FALLBACK_TEACHERS:
        if fb['id'] not in existing_ids:
            DB.setdefault('teachers', []).append(fb)

    # 1. Overview Telemetry
    @app.route('/api/teacher-mgmt/overview', methods=['GET'])
    def teacher_mgmt_overview():
        teachers = DB.get('teachers', [])
        updates = _load_json('teacher_update_requests.json', [])
        pending_updates = len([u for u in updates if u.get('status') == 'pending'])
        
        assignments = _load_json('teacher_assignments.json', [])
        attendance = _load_json('teacher_attendance.json', [])
        today_present = len([a for a in attendance if a.get('status') == 'present'])
        today_total = len(attendance) or 1
        att_rate = round((today_present / today_total) * 100, 1) if attendance else 98.2

        discipline = _load_json('teacher_discipline.json', [])
        active_disc = len([d for d in discipline if d.get('status') in ('under_review', 'hearing_scheduled')])

        commendations = _load_json('teacher_commendations.json', [])
        efforts = _load_json('teacher_efforts.json', [])
        total_effort_hrs = sum(e.get('hoursSpent', 0) for e in efforts)

        return jsonify({
            'totalTeachers': len(teachers),
            'pendingUpdates': pending_updates,
            'totalAssignments': len(assignments),
            'todayAttendanceRate': att_rate,
            'activeDisciplineCases': active_disc,
            'totalCommendations': len(commendations),
            'totalEffortHours': total_effort_hrs
        })

    # 2. Teacher Directory Roster
    @app.route('/api/teacher-mgmt/teachers', methods=['GET'])
    def teacher_mgmt_list():
        teachers = DB.get('teachers', [])
        dept = request.args.get('department', '').strip().lower()
        search = request.args.get('search', '').strip().lower()

        res = []
        for t in teachers:
            if dept and dept != 'all' and dept not in (t.get('department') or '').lower():
                continue
            if search:
                name_match = search in (t.get('name') or '').lower()
                dept_match = search in (t.get('department') or '').lower()
                id_match = search in (t.get('id') or '').lower()
                subj_match = any(search in s.lower() for s in t.get('subjects', []))
                if not (name_match or dept_match or id_match or subj_match):
                    continue
            res.append(t)

        return jsonify({'data': res, 'total': len(res)})

    # 3. Verify Teacher Updates
    @app.route('/api/teacher-mgmt/verify', methods=['GET'])
    def teacher_mgmt_verify_list():
        items = _load_json('teacher_update_requests.json', [])
        status = request.args.get('status', '').strip().lower()
        search = request.args.get('search', '').strip().lower()

        res = []
        for item in items:
            if status and status != 'all' and item.get('status') != status:
                continue
            if search:
                match = (search in item.get('teacherName', '').lower() or
                         search in item.get('teacherId', '').lower() or
                         search in item.get('department', '').lower() or
                         search in item.get('fieldChanged', '').lower())
                if not match:
                    continue
            res.append(item)

        return jsonify({'data': res, 'total': len(res)})

    @app.route('/api/teacher-mgmt/verify/<id>/action', methods=['POST'])
    def teacher_mgmt_verify_action(id):
        items = _load_json('teacher_update_requests.json', [])
        req_item = next((i for i in items if i['id'] == id), None)
        if not req_item:
            return jsonify({'success': False, 'message': 'Update request not found'}), 404

        body = request.get_json() or {}
        action = body.get('action')  # approve, reject, correct
        reviewer = body.get('reviewer', 'Executive Principal')
        comments = body.get('comments', '')

        if action == 'approve':
            req_item['status'] = 'approved'
            req_item['reviewedBy'] = reviewer
            req_item['reviewedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            req_item['comments'] = comments or 'Approved by administration.'

            # Apply change to DB['teachers']
            tid = req_item.get('teacherId')
            field = req_item.get('fieldChanged', '').lower()
            val = req_item.get('proposedValue')
            t_obj = next((t for t in DB.get('teachers', []) if t['id'] == tid), None)
            if t_obj and val:
                if 'phone' in field:
                    t_obj['phone'] = val
                elif 'qualification' in field or 'degree' in field:
                    t_obj.setdefault('qualifications', []).append(val)
                elif 'certification' in field:
                    t_obj.setdefault('certifications', []).append(val)
                elif 'address' in field:
                    t_obj['address'] = val

        elif action == 'reject':
            req_item['status'] = 'rejected'
            req_item['reviewedBy'] = reviewer
            req_item['reviewedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            req_item['comments'] = comments or 'Rejected.'

        elif action == 'correct':
            req_item['status'] = 'needs_correction'
            req_item['reviewedBy'] = reviewer
            req_item['reviewedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            req_item['comments'] = comments or 'Please provide further documentation.'

        _save_json('teacher_update_requests.json', items)
        return jsonify({'success': True, 'item': req_item})

    # 4. Teaching Assignments
    @app.route('/api/teacher-mgmt/assignments', methods=['GET', 'POST'])
    def teacher_mgmt_assignments():
        assignments = _load_json('teacher_assignments.json', [])
        if request.method == 'GET':
            tid = request.args.get('teacherId')
            cid = request.args.get('classId')
            res = assignments
            if tid:
                res = [a for a in res if a.get('teacherId') == tid]
            if cid:
                res = [a for a in res if a.get('classId') == cid]

            # Calculate workloads per teacher
            workload_map = {}
            for t in DB.get('teachers', []):
                workload_map[t['id']] = {
                    'teacherId': t['id'],
                    'teacherName': t['name'],
                    'department': t['department'],
                    'assignedPeriods': 0,
                    'classes': set(),
                    'subjects': set(),
                    'maxCapacity': 22,
                    'status': 'optimal'
                }

            for a in assignments:
                t_id = a.get('teacherId')
                if t_id in workload_map:
                    workload_map[t_id]['assignedPeriods'] += int(a.get('periodsPerWeek', 4))
                    workload_map[t_id]['classes'].add(a.get('className'))
                    workload_map[t_id]['subjects'].add(a.get('subjectName'))

            workloads = []
            for item in workload_map.values():
                item['classes'] = sorted(list(item['classes']))
                item['subjects'] = sorted(list(item['subjects']))
                if item['assignedPeriods'] > 22:
                    item['status'] = 'heavy'
                elif item['assignedPeriods'] < 12:
                    item['status'] = 'light'
                else:
                    item['status'] = 'optimal'
                workloads.append(item)

            return jsonify({
                'assignments': res,
                'workloads': workloads,
                'total': len(res)
            })

        # POST: Create assignment
        data = request.get_json() or {}
        new_id = f"TAS-2026-{len(assignments) + 1:03d}"
        assignment = {
            "id": new_id,
            "teacherId": data.get('teacherId'),
            "teacherName": data.get('teacherName'),
            "department": data.get('department'),
            "subjectId": data.get('subjectId', 'subj-gen'),
            "subjectName": data.get('subjectName'),
            "classId": data.get('classId'),
            "className": data.get('className'),
            "periodsPerWeek": int(data.get('periodsPerWeek', 5)),
            "room": data.get('room', 'Room 101'),
            "academicYear": data.get('academicYear', '2025-2026'),
            "semester": data.get('semester', 'Semester 2'),
            "status": "active"
        }
        assignments.append(assignment)
        _save_json('teacher_assignments.json', assignments)
        return jsonify({'success': True, 'assignment': assignment}), 201

    @app.route('/api/teacher-mgmt/assignments/<id>', methods=['DELETE'])
    def teacher_mgmt_delete_assignment(id):
        assignments = _load_json('teacher_assignments.json', [])
        filtered = [a for a in assignments if a['id'] != id]
        _save_json('teacher_assignments.json', filtered)
        return jsonify({'success': True, 'deletedId': id})

    # 5. Homeroom Assignments
    @app.route('/api/teacher-mgmt/homeroom', methods=['GET'])
    def teacher_mgmt_homeroom_list():
        classes = DB.get('classes', [])
        teachers = DB.get('teachers', [])

        homeroom_records = []
        for c in classes:
            code = c.get('code') or c.get('id')
            name = c.get('name')
            hr_teacher = c.get('homeroomTeacher') or 'Unassigned'
            # Find matching teacher object
            t_obj = next((t for t in teachers if t['name'] == hr_teacher or t.get('homeroom') == code.replace('cls-', '').upper()), None)
            
            # Count enrolled students
            class_std_count = len([s for s in DB.get('students', []) if s.get('class') in (code, name, code.replace('cls-', '').upper())])
            
            homeroom_records.append({
                'classId': code,
                'className': name,
                'grade': c.get('grade', 'Grade 10'),
                'room': c.get('room', 'Room 201'),
                'homeroomTeacher': hr_teacher,
                'teacherId': t_obj['id'] if t_obj else None,
                'teacherEmail': t_obj['email'] if t_obj else None,
                'studentCount': class_std_count or c.get('studentCount', 28),
                'academicYear': '2025-2026',
                'status': 'assigned' if hr_teacher != 'Unassigned' else 'vacant'
            })

        return jsonify({'data': homeroom_records, 'total': len(homeroom_records)})

    @app.route('/api/teacher-mgmt/homeroom/<class_id>', methods=['POST'])
    def teacher_mgmt_assign_homeroom(class_id):
        body = request.get_json() or {}
        new_teacher_name = body.get('teacherName')
        new_teacher_id = body.get('teacherId')

        # Update class homeroom teacher
        classes = DB.get('classes', [])
        target_class = next((c for c in classes if (c.get('code') == class_id or c.get('id') == class_id)), None)
        if not target_class:
            return jsonify({'success': False, 'message': 'Class not found'}), 404

        target_class['homeroomTeacher'] = new_teacher_name

        # Update teacher homeroom record in DB['teachers']
        clean_code = class_id.replace('cls-', '').upper()
        for t in DB.get('teachers', []):
            if t['id'] == new_teacher_id or t['name'] == new_teacher_name:
                t['homeroom'] = clean_code

        return jsonify({
            'success': True,
            'classId': class_id,
            'homeroomTeacher': new_teacher_name
        })

    # 6. Teacher Attendance
    @app.route('/api/teacher-mgmt/attendance', methods=['GET', 'POST'])
    def teacher_mgmt_attendance():
        records = _load_json('teacher_attendance.json', [])
        if request.method == 'GET':
            date_filter = request.args.get('date', '').strip()
            dept_filter = request.args.get('department', '').strip().lower()
            status_filter = request.args.get('status', '').strip().lower()

            res = []
            for r in records:
                if date_filter and r.get('date') != date_filter:
                    continue
                if dept_filter and dept_filter != 'all' and dept_filter not in r.get('department', '').lower():
                    continue
                if status_filter and status_filter != 'all' and r.get('status') != status_filter:
                    continue
                res.append(r)

            # Telemetry stats
            present = len([r for r in records if r.get('status') == 'present'])
            late = len([r for r in records if r.get('status') == 'late'])
            excused = len([r for r in records if r.get('status') == 'excused'])
            duty = len([r for r in records if r.get('status') == 'duty'])
            absent = len([r for r in records if r.get('status') == 'absent'])
            total = len(records) or 1

            return jsonify({
                'data': res,
                'total': len(res),
                'summary': {
                    'presentRate': round((present / total) * 100, 1),
                    'presentCount': present,
                    'lateCount': late,
                    'excusedCount': excused,
                    'dutyCount': duty,
                    'absentCount': absent,
                    'totalRecorded': len(records)
                }
            })

        # POST: Record / correct attendance
        data = request.get_json() or {}
        new_id = f"TAT-2026-{len(records) + 1:03d}"
        rec = {
            "id": new_id,
            "date": data.get('date', datetime.now().strftime('%Y-%m-%d')),
            "teacherId": data.get('teacherId'),
            "teacherName": data.get('teacherName'),
            "department": data.get('department'),
            "status": data.get('status', 'present'),
            "checkIn": data.get('checkIn', '07:45 AM'),
            "checkOut": data.get('checkOut', '04:30 PM'),
            "biometricTerminal": data.get('terminal', 'Admin Manual Override'),
            "notes": data.get('notes', 'Administrative entry.')
        }
        records.append(rec)
        _save_json('teacher_attendance.json', records)
        return jsonify({'success': True, 'record': rec}), 201

    # 7. Commendations
    @app.route('/api/teacher-mgmt/commendations', methods=['GET', 'POST'])
    def teacher_mgmt_commendations():
        records = _load_json('teacher_commendations.json', [])
        if request.method == 'GET':
            search = request.args.get('search', '').strip().lower()
            dept = request.args.get('department', '').strip().lower()
            res = []
            for r in records:
                if dept and dept != 'all' and dept not in r.get('department', '').lower():
                    continue
                if search:
                    match = (search in r.get('teacherName', '').lower() or
                             search in r.get('title', '').lower() or
                             search in r.get('category', '').lower() or
                             search in r.get('issuingAuthority', '').lower())
                    if not match:
                        continue
                res.append(r)
            return jsonify({'data': res, 'total': len(res)})

        data = request.get_json() or {}
        new_id = f"TCM-2026-{len(records) + 1:03d}"
        rec = {
            "id": new_id,
            "teacherId": data.get('teacherId'),
            "teacherName": data.get('teacherName'),
            "department": data.get('department'),
            "category": data.get('category', 'Pedagogical Excellence'),
            "title": data.get('title'),
            "description": data.get('description'),
            "issuingAuthority": data.get('issuingAuthority', 'Executive Principal'),
            "dateAwarded": data.get('dateAwarded', datetime.now().strftime('%Y-%m-%d')),
            "citation": data.get('citation', ''),
            "certificateRef": f"CERT-{data.get('teacherId', 'FAC')}-2026.pdf"
        }
        records.append(rec)
        _save_json('teacher_commendations.json', records)
        return jsonify({'success': True, 'item': rec}), 201

    # 8. Discipline (Confidential Conduct & Compliance)
    @app.route('/api/teacher-mgmt/discipline', methods=['GET', 'POST'])
    def teacher_mgmt_discipline():
        records = _load_json('teacher_discipline.json', [])
        if request.method == 'GET':
            status = request.args.get('status', '').strip().lower()
            res = []
            for r in records:
                if status and status != 'all' and r.get('status') != status:
                    continue
                res.append(r)
            return jsonify({'data': res, 'total': len(res)})

        data = request.get_json() or {}
        new_id = f"TDS-2026-{len(records) + 1:03d}"
        case_no = f"CAS-2026-{100 + len(records) + 1:04d}"
        rec = {
            "id": new_id,
            "caseNumber": case_no,
            "teacherId": data.get('teacherId'),
            "teacherName": data.get('teacherName'),
            "department": data.get('department'),
            "category": data.get('category', 'Policy Compliance'),
            "severity": data.get('severity', 'Level 1 - Formal Reminder'),
            "incidentDate": data.get('incidentDate', datetime.now().strftime('%Y-%m-%d')),
            "description": data.get('description'),
            "evidenceDocs": data.get('evidenceDocs', []),
            "hearingDate": data.get('hearingDate'),
            "status": "under_review",
            "decisionSummary": "Pending administrative review.",
            "confidentialLevel": "Restricted - Admin / Principal Oversight"
        }
        records.append(rec)
        _save_json('teacher_discipline.json', records)
        return jsonify({'success': True, 'item': rec}), 201

    @app.route('/api/teacher-mgmt/discipline/<id>/adjudicate', methods=['POST'])
    def teacher_mgmt_discipline_adjudicate(id):
        records = _load_json('teacher_discipline.json', [])
        item = next((r for r in records if r['id'] == id), None)
        if not item:
            return jsonify({'success': False, 'message': 'Case not found'}), 404

        data = request.get_json() or {}
        item['status'] = data.get('status', item['status'])
        item['decisionSummary'] = data.get('decisionSummary', item['decisionSummary'])
        if data.get('hearingDate'):
            item['hearingDate'] = data.get('hearingDate')

        _save_json('teacher_discipline.json', records)
        return jsonify({'success': True, 'item': item})

    # 9. Teacher Efforts (Documented Contributions beyond Teaching)
    @app.route('/api/teacher-mgmt/efforts', methods=['GET', 'POST'])
    def teacher_mgmt_efforts():
        records = _load_json('teacher_efforts.json', [])
        if request.method == 'GET':
            category = request.args.get('category', '').strip().lower()
            status = request.args.get('status', '').strip().lower()
            search = request.args.get('search', '').strip().lower()

            res = []
            for r in records:
                if category and category != 'all' and category not in r.get('category', '').lower():
                    continue
                if status and status != 'all' and r.get('status') != status:
                    continue
                if search:
                    match = (search in r.get('teacherName', '').lower() or
                             search in r.get('title', '').lower() or
                             search in r.get('department', '').lower() or
                             search in r.get('description', '').lower())
                    if not match:
                        continue
                res.append(r)
            return jsonify({'data': res, 'total': len(res)})

        data = request.get_json() or {}
        new_id = f"TEF-2026-{len(records) + 1:03d}"
        rec = {
            "id": new_id,
            "teacherId": data.get('teacherId'),
            "teacherName": data.get('teacherName'),
            "department": data.get('department'),
            "category": data.get('category', 'School Activities'),
            "title": data.get('title'),
            "description": data.get('description'),
            "hoursSpent": int(data.get('hoursSpent', 4)),
            "dateLogged": datetime.now().strftime('%Y-%m-%d'),
            "supportingDocument": data.get('supportingDocument', 'Activity_Log.pdf'),
            "status": "logged",
            "endorsedBy": None
        }
        records.append(rec)
        _save_json('teacher_efforts.json', records)
        return jsonify({'success': True, 'item': rec}), 201

    @app.route('/api/teacher-mgmt/efforts/<id>/action', methods=['POST'])
    def teacher_mgmt_efforts_action(id):
        records = _load_json('teacher_efforts.json', [])
        item = next((r for r in records if r['id'] == id), None)
        if not item:
            return jsonify({'success': False, 'message': 'Record not found'}), 404

        data = request.get_json() or {}
        action = data.get('action')  # verify, endorse
        reviewer = data.get('reviewer', 'Executive Principal')

        if action == 'verify':
            item['status'] = 'verified'
            item['endorsedBy'] = reviewer
        elif action == 'endorse':
            item['status'] = 'endorsed'
            item['endorsedBy'] = reviewer

        _save_json('teacher_efforts.json', records)
        return jsonify({'success': True, 'item': item})

    print("Teacher Management routes registered successfully.")

