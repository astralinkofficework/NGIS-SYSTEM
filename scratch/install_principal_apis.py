import re

principal_api_code = '''# ════════════════════════════════════════════════════════════════════
# PRINCIPAL CENTRAL MANAGEMENT & OVERSIGHT API LAYER
# ════════════════════════════════════════════════════════════════════

PRINCIPAL_APPROVALS = [
    {
        'id': 'appr-grd-10a',
        'type': 'grade_submission',
        'category': 'Academic Grades',
        'title': 'Grade 10-A · Pure Mathematics Assessment Battery',
        'submittedBy': 'Dr. Sarah Jenkins',
        'submittedRole': 'Senior Faculty · Mathematics',
        'submittedAt': '2026-11-01T14:20:00Z',
        'scope': 'Grade 10-A · 32 Students · Room 302',
        'classId': 'cls-10a',
        'subjectId': 'subj-math',
        'details': 'Semester 1 Assessment battery (Quadratics Quiz, Problem Set 1, Midterm Exam). Average class score: 86.4%. Requires Executive clearance before grades and GPA calculations become visible in Student and Parent portals.',
        'diffOld': 'Unpublished (Draft / Submitted Gradebook)',
        'diffNew': 'Official Published Gradebook & Certified GPA',
        'status': 'pending',
        'decisionNote': '',
        'decidedAt': None,
        'decidedBy': None,
        'studentCount': 32,
        'avgScore': '86.4%'
    },
    {
        'id': 'appr-amd-001',
        'type': 'grade_amendment',
        'category': 'Grade Amendment',
        'title': 'Calculus Midterm Assessment Rescore · Sokha Chan',
        'submittedBy': 'Dr. Sarah Jenkins',
        'submittedRole': 'Senior Faculty · Mathematics',
        'submittedAt': '2026-11-02T09:15:00Z',
        'scope': 'Student: Sokha Chan (2026-STD-0142) · Grade 11-A',
        'studentId': '2026-STD-0142',
        'details': 'Section 4 calculation error verified during departmental moderation. Question 4B rubric score adjusted from 12/20 to 18/20 following faculty re-check.',
        'diffOld': '74% (C+)',
        'diffNew': '88% (A)',
        'status': 'pending',
        'decisionNote': '',
        'decidedAt': None,
        'decidedBy': None,
        'studentCount': 1,
        'avgScore': '88.0%'
    },
    {
        'id': 'appr-att-002',
        'type': 'attendance_correction',
        'category': 'Attendance Correction',
        'title': 'Excused Absence Adjustment · Dara Rin',
        'submittedBy': 'Mr. Chea Sophea',
        'submittedRole': 'Homeroom Teacher · Grade 11-B',
        'submittedAt': '2026-11-02T10:30:00Z',
        'scope': 'Student: Dara Rin (2026-STD-0144) · Grade 11-B',
        'studentId': '2026-STD-0144',
        'details': 'Official medical certificate from Pasteur Institute received and verified by campus infirmary. Status amended from Unexcused Absent to Medical Excused.',
        'diffOld': 'Unexcused Absent (Oct 28)',
        'diffNew': 'Medical Excused (Pasteur Cert #88219)',
        'status': 'pending',
        'decisionNote': '',
        'decidedAt': None,
        'decidedBy': None,
        'studentCount': 1,
        'avgScore': '—'
    },
    {
        'id': 'appr-trn-003',
        'type': 'transcript_certification',
        'category': 'Official Certification',
        'title': 'Official Cambridge AS-Level Transcript Issuance',
        'submittedBy': 'Registrar Office / Student Request',
        'submittedRole': 'Central Registrar',
        'submittedAt': '2026-11-02T11:00:00Z',
        'scope': 'Student: Nrinphouneta Hok (2026-STD-0142) · Cambridge AS-Level',
        'studentId': '2026-STD-0142',
        'details': 'Official Academic Transcript with Embossed School Seal requested for university application to National University of Singapore (NUS). All term credits verified.',
        'diffOld': 'Pending Executive Certification',
        'diffNew': 'Certified & Digitally Signed with Principal Seal',
        'status': 'pending',
        'decisionNote': '',
        'decidedAt': None,
        'decidedBy': None,
        'studentCount': 1,
        'avgScore': 'GPA 3.92'
    },
    {
        'id': 'appr-clr-004',
        'type': 'leave_clearance',
        'category': 'Administrative Clearance',
        'title': 'Extended Academic Leave Request · International Olympiad',
        'submittedBy': 'Student Affairs / Dr. Sarah Jenkins',
        'submittedRole': 'Department Head',
        'submittedAt': '2026-11-02T12:00:00Z',
        'scope': 'Student: Vicheka Pich (2026-STD-0145) · Nov 10 – Nov 18',
        'studentId': '2026-STD-0145',
        'details': 'Representing NGIS at the Southeast Asian Mathematical Olympiad (SEAMO) in Singapore. Independent study syllabus and examination rescheduling agreed with teachers.',
        'diffOld': 'Pending Principal Leave Approval',
        'diffNew': 'Executive Academic Leave Granted',
        'status': 'pending',
        'decisionNote': '',
        'decidedAt': None,
        'decidedBy': None,
        'studentCount': 1,
        'avgScore': '—'
    }
]

def _get_principal_actor():
    u = _academic_user()
    if u and u.get('role') in ('principal', 'admin'):
        return u['id'], u.get('name', 'Dr. Elena Vance'), u['role']
    return 'PRIN-2026-001', 'Dr. Elena Vance (Principal)', 'principal'

@app.route('/api/principal/approvals', methods=['GET'])
def get_principal_approvals():
    status_filter = request.args.get('status', 'all').lower()
    category_filter = request.args.get('category', 'all').lower()

    items = list(PRINCIPAL_APPROVALS)

    if status_filter != 'all':
        items = [i for i in items if i.get('status', '').lower() == status_filter]
    if category_filter != 'all':
        items = [i for i in items if category_filter in i.get('category', '').lower() or category_filter in i.get('type', '').lower()]

    # Calculate live counts across the whole store
    pending_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'pending')
    approved_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'approved')
    needs_correction_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'needs_correction')
    rejected_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'rejected')

    return jsonify({
        'status': 'success',
        'counts': {
            'total': len(PRINCIPAL_APPROVALS),
            'pending': pending_cnt,
            'approved': approved_cnt,
            'needs_correction': needs_correction_cnt,
            'rejected': rejected_cnt
        },
        'data': items
    })

@app.route('/api/principal/approvals/<item_id>/action', methods=['POST'])
def handle_principal_approval_action(item_id):
    actor_id, actor_name, actor_role = _get_principal_actor()
    data = request.get_json(silent=True) or {}
    action = data.get('action', '').lower()
    note = data.get('note', '').strip()

    if action not in ('approve', 'reject', 'return', 'needs_correction'):
        return jsonify({'error': {'code': 'INVALID_ACTION', 'message': 'Action must be approve, reject, or needs_correction'}}), 400

    item = next((i for i in PRINCIPAL_APPROVALS if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Approval item not found'}}), 404

    now_iso = ACADEMIC.now()
    item['decidedAt'] = now_iso
    item['decidedBy'] = actor_name
    item['decisionNote'] = note

    if action == 'approve':
        item['status'] = 'approved'
        # Live synchronization with academic database
        if item.get('type') == 'grade_submission':
            class_id = item.get('classId')
            if class_id:
                try:
                    ACADEMIC.execute("UPDATE grades SET workflow='published', updated_at=? WHERE assessment_id IN (SELECT id FROM assessments WHERE class_id=?)", (now_iso, class_id))
                except Exception:
                    pass
            ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_PUBLISH_GRADES', 'grades', item_id, note or 'Approved by Principal', {'classId': class_id})
        elif item.get('type') == 'grade_amendment':
            student_id = item.get('studentId')
            ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_GRADE_AMENDMENT_APPROVE', 'grade', item_id, note or 'Grade amendment approved by Principal', {'studentId': student_id, 'newScore': item.get('diffNew')})
        elif item.get('type') == 'attendance_correction':
            student_id = item.get('studentId')
            ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_ATTENDANCE_CORRECTION_APPROVE', 'attendance', item_id, note or 'Attendance amendment approved by Principal', {'studentId': student_id})
        elif item.get('type') == 'transcript_certification':
            student_id = item.get('studentId')
            ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_TRANSCRIPT_CERTIFY', 'transcript', item_id, note or 'Transcript certified with Principal Seal', {'studentId': student_id})
        else:
            ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_APPROVE', 'approval', item_id, note or 'Approved by Principal', {'title': item.get('title')})

    elif action in ('return', 'needs_correction'):
        item['status'] = 'needs_correction'
        ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_RETURN_CORRECTION', 'approval', item_id, note or 'Returned for faculty correction', {'title': item.get('title')})

    elif action == 'reject':
        item['status'] = 'rejected'
        ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_REJECT', 'approval', item_id, note or 'Rejected by Principal', {'title': item.get('title')})

    # Return updated counts
    pending_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'pending')
    approved_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'approved')
    needs_correction_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'needs_correction')
    rejected_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'rejected')

    return jsonify({
        'status': 'success',
        'message': f'Item {item_id} marked as {item["status"]}',
        'item': item,
        'counts': {
            'total': len(PRINCIPAL_APPROVALS),
            'pending': pending_cnt,
            'approved': approved_cnt,
            'needs_correction': needs_correction_cnt,
            'rejected': rejected_cnt
        }
    })

@app.route('/api/principal/approvals/batch-action', methods=['POST'])
def handle_principal_batch_approvals():
    actor_id, actor_name, actor_role = _get_principal_actor()
    data = request.get_json(silent=True) or {}
    action = data.get('action', 'approve').lower()
    item_ids = data.get('itemIds', [])
    note = data.get('note', 'Batch authorized by Principal').strip()

    now_iso = ACADEMIC.now()
    affected = 0

    for item in PRINCIPAL_APPROVALS:
        if (not item_ids or item['id'] in item_ids) and item['status'] == 'pending':
            if action == 'approve':
                item['status'] = 'approved'
                item['decidedAt'] = now_iso
                item['decidedBy'] = actor_name
                item['decisionNote'] = note
                # Synchronize if grade submission
                if item.get('type') == 'grade_submission' and item.get('classId'):
                    try:
                        ACADEMIC.execute("UPDATE grades SET workflow='published', updated_at=? WHERE assessment_id IN (SELECT id FROM assessments WHERE class_id=?)", (now_iso, item['classId']))
                    except Exception:
                        pass
                affected += 1

    ACADEMIC.audit(actor_id, actor_role, 'PRINCIPAL_BATCH_APPROVE', 'batch', 'all-pending', note, {'count': affected})

    pending_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'pending')
    approved_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'approved')
    needs_correction_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'needs_correction')
    rejected_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'rejected')

    return jsonify({
        'status': 'success',
        'message': f'Successfully updated {affected} items',
        'affected': affected,
        'counts': {
            'total': len(PRINCIPAL_APPROVALS),
            'pending': pending_cnt,
            'approved': approved_cnt,
            'needs_correction': needs_correction_cnt,
            'rejected': rejected_cnt
        }
    })

@app.route('/api/principal/audit', methods=['GET'])
def get_principal_audit_log():
    limit = int(request.args.get('limit', 25))
    try:
        events = ACADEMIC.query(f"SELECT * FROM audit_events ORDER BY created_at DESC LIMIT {limit}")
        return jsonify({'status': 'success', 'data': [dict(e) for e in events]})
    except Exception as exc:
        return jsonify({'status': 'success', 'data': []})

@app.route('/api/principal/stats', methods=['GET'])
def principal_stats():
    pending_cnt = sum(1 for i in PRINCIPAL_APPROVALS if i.get('status') == 'pending')
    return jsonify({
        'data': {
            'totalStudents': 1250,
            'totalTeachers': 86,
            'totalClasses': 48,
            'dailyAttendanceRate': 95.4,
            'overallSchoolGpa': 3.62,
            'honorsRate': '24.2%',
            'pendingApprovals': pending_cnt,
            'departments': [
                {'name': 'Mathematics', 'head': 'Dr. Sarah Jenkins', 'faculty': 14, 'avgScore': 87.2, 'status': 'Optimal'},
                {'name': 'Science', 'head': 'Dr. Pov Sophea', 'faculty': 18, 'avgScore': 85.8, 'status': 'Optimal'},
                {'name': 'English', 'head': 'Ms. Rin Lina', 'faculty': 16, 'avgScore': 88.4, 'status': 'Optimal'},
                {'name': 'Khmer Studies', 'head': 'Mr. Chea Sambath', 'faculty': 12, 'avgScore': 89.1, 'status': 'Optimal'},
                {'name': 'Computer Science', 'head': 'Mr. Heng Samnang', 'faculty': 10, 'avgScore': 84.6, 'status': 'Optimal'},
            ]
        }
    })
'''

with open('server.py', 'r', encoding='utf-8') as f:
    server_content = f.read()

# Replace the old static principal_stats with the comprehensive new Principal API layer
old_target = """# ── PRINCIPAL OVERSIGHT APIS ──
@app.route('/api/principal/stats', methods=['GET'])
def principal_stats():
    return jsonify({
        'data': {
            'totalStudents': 1250,
            'totalTeachers': 86,
            'totalClasses': 48,
            'dailyAttendanceRate': 95.4,
            'overallSchoolGpa': 3.62,
            'honorsRate': '24.2%',
            'pendingApprovals': 4,
            'departments': [
                {'name': 'Mathematics', 'head': 'Dr. Sarah Jenkins', 'faculty': 14, 'avgScore': 87.2, 'status': 'Optimal'},
                {'name': 'Science', 'head': 'Dr. Pov Sophea', 'faculty': 18, 'avgScore': 85.8, 'status': 'Optimal'},
                {'name': 'English', 'head': 'Ms. Rin Lina', 'faculty': 16, 'avgScore': 88.4, 'status': 'Optimal'},
                {'name': 'Khmer Studies', 'head': 'Mr. Chea Sambath', 'faculty': 12, 'avgScore': 89.1, 'status': 'Optimal'},
                {'name': 'Computer Science', 'head': 'Mr. Heng Samnang', 'faculty': 10, 'avgScore': 84.6, 'status': 'Optimal'},
            ]
        }
    })"""

norm_server = server_content.replace('\r\n', '\n')
norm_old = old_target.replace('\r\n', '\n')

if norm_old in norm_server:
    norm_server = norm_server.replace(norm_old, principal_api_code)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(norm_server)
    print('Principal API endpoints installed successfully in server.py!')
else:
    print('Target principal_stats not found in server.py!')

