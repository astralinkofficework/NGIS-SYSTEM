path = 'server.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the clearance endpoints with robust versions using build_principal_queue & ACADEMIC
old_block = '''# ── TEACHER / PRINCIPAL GRADEBOOK CLEARANCE SYNC ──
@app.route('/api/academic/gradebook/clearance-status', methods=['GET'])
def academic_gradebook_clearance_status():
    class_id = request.args.get('classId', 'cls-10a')
    subject_id = request.args.get('subjectId', 'subj-math')
    
    matching_appr = next((a for a in PRINCIPAL_APPROVALS if (a.get('classId') == class_id or a.get('id') == 'appr-grd-10a')), None)
    
    row = ACADEMIC.one("SELECT workflow, updated_at FROM grades JOIN assessments ON assessments.id=grades.assessment_id WHERE assessments.class_id=? ORDER BY grades.updated_at DESC LIMIT 1", (class_id,))
    
    workflow = 'draft'
    status = 'draft'
    decision_note = ''
    decided_by = ''
    decided_at = ''

    if matching_appr:
        status = matching_appr.get('status', 'pending')
        decision_note = matching_appr.get('decisionNote', '')
        decided_by = matching_appr.get('decidedBy', '')
        decided_at = matching_appr.get('decidedAt', '')
        if status == 'approved':
            workflow = 'published'
        elif status == 'needs_correction':
            workflow = 'returned'
        elif status == 'pending':
            workflow = 'submitted'
    elif row and row.get('workflow'):
        workflow = row['workflow']
        status = 'approved' if workflow == 'published' else ('needs_correction' if workflow == 'returned' else ('pending' if workflow == 'submitted' else 'draft'))

    labels = {
        'published': 'Verified & Published by Academic Principal',
        'submitted': 'Pending Principal Clearance',
        'returned': 'Revisions Requested by Principal',
        'draft': 'Draft · Not Yet Submitted for Clearance'
    }

    return jsonify({
        'status': status,
        'workflow': workflow,
        'label': labels.get(workflow, 'Draft'),
        'decisionNote': decision_note,
        'decidedBy': decided_by or 'Dr. Ly Bunheng',
        'decidedAt': decided_at,
        'classId': class_id,
        'subjectId': subject_id
    }), 200

@app.route('/api/academic/gradebook/submit-clearance', methods=['POST'])
def academic_gradebook_submit_clearance():
    data = request.get_json(silent=True) or {}
    class_id = data.get('classId', 'cls-10a')
    subject_id = data.get('subjectId', 'subj-math')
    teacher_name = data.get('teacherName', 'Dr. Sarah Jenkins')

    ACADEMIC.execute("UPDATE grades SET workflow='submitted', updated_at=? WHERE workflow != 'published'", (ACADEMIC.now(),))
    
    matching_appr = next((a for a in PRINCIPAL_APPROVALS if (a.get('classId') == class_id or a.get('id') == 'appr-grd-10a')), None)
    if matching_appr:
        matching_appr['status'] = 'pending'
        matching_appr['submittedAt'] = ACADEMIC.now()
        matching_appr['decisionNote'] = ''
    else:
        PRINCIPAL_APPROVALS.insert(0, {
            'id': f'appr-grd-{class_id}',
            'type': 'grade_submission',
            'category': 'Academic Grades',
            'title': f'{class_id.upper()} Assessment Battery Submission',
            'submittedBy': teacher_name,
            'submittedRole': 'Faculty',
            'submittedAt': ACADEMIC.now(),
            'scope': f'{class_id.upper()} · All Enrolled Students',
            'classId': class_id,
            'subjectId': subject_id,
            'details': 'Submitted by faculty for Executive Clearance and Portal Publication.',
            'diffOld': 'Draft / Submitted Gradebook',
            'diffNew': 'Official Published Gradebook & Certified GPA',
            'status': 'pending',
            'decisionNote': '',
            'decidedAt': None,
            'decidedBy': None,
            'studentCount': 32,
            'avgScore': '86.4%'
        })

    ACADEMIC.audit('tch-jenkins', 'teacher', 'TEACHER_SUBMIT_CLEARANCE', 'gradebook', class_id, 'Submitted gradebook for Principal clearance', {'classId': class_id, 'subjectId': subject_id})

    return jsonify({'status': 'pending', 'workflow': 'submitted', 'message': 'Gradebook submitted to Academic Principal for Executive Clearance.'}), 200'''

new_block = '''# ── TEACHER / PRINCIPAL GRADEBOOK CLEARANCE SYNC ──
@app.route('/api/academic/gradebook/clearance-status', methods=['GET'])
def academic_gradebook_clearance_status():
    class_id = request.args.get('classId', 'cls-10a')
    subject_id = request.args.get('subjectId', 'subj-math')
    period_id = request.args.get('periodId', 'gp-sem2')

    queue = build_principal_queue()
    matching_item = next((it for it in queue if it.get('classId') == class_id or it.get('id') == f"grade:{class_id}:{period_id}"), None)

    row = ACADEMIC.one("""
        SELECT g.workflow, g.updated_at 
        FROM grades g 
        JOIN assessments a ON a.id = g.assessment_id 
        WHERE a.class_id = ? 
        ORDER BY g.updated_at DESC LIMIT 1
    """, (class_id,))

    workflow = (row and row.get('workflow')) or 'draft'
    status = 'draft'
    decision_note = ''
    decided_by = 'Dr. Ly Bunheng'
    decided_at = ''

    if matching_item:
        status = matching_item.get('status', 'pending')
        decision_note = matching_item.get('decisionNote', '')
        decided_by = matching_item.get('decidedBy', 'Dr. Ly Bunheng')
        decided_at = matching_item.get('decidedAt', '')
        if status == 'approved':
            workflow = 'published'
        elif status == 'needs_correction':
            workflow = 'returned'
        elif status == 'pending':
            workflow = 'submitted'
    else:
        if workflow == 'published':
            status = 'approved'
        elif workflow == 'returned':
            status = 'needs_correction'
        elif workflow == 'submitted':
            status = 'pending'

    labels = {
        'published': 'Verified & Published by Academic Principal',
        'submitted': 'Pending Principal Clearance',
        'returned': 'Revisions Requested by Principal',
        'draft': 'Draft · Not Yet Submitted for Clearance'
    }

    return jsonify({
        'status': status,
        'workflow': workflow,
        'label': labels.get(workflow, 'Draft'),
        'decisionNote': decision_note,
        'decidedBy': decided_by,
        'decidedAt': decided_at,
        'classId': class_id,
        'periodId': period_id
    }), 200

@app.route('/api/academic/gradebook/submit-clearance', methods=['POST'])
def academic_gradebook_submit_clearance():
    data = request.get_json(silent=True) or {}
    class_id = data.get('classId', 'cls-10a')
    period_id = data.get('periodId', 'gp-sem2')

    ACADEMIC.execute("""
        UPDATE grades SET workflow='submitted', updated_at=? 
        WHERE assessment_id IN (SELECT id FROM assessments WHERE class_id=?)
    """, (ACADEMIC.now(), class_id))

    ACADEMIC.audit('tch-jenkins', 'teacher', 'TEACHER_SUBMIT_CLEARANCE', 'gradebook', class_id, 'Submitted gradebook for Principal clearance', {'classId': class_id, 'periodId': period_id})

    return jsonify({'status': 'pending', 'workflow': 'submitted', 'message': 'Gradebook submitted to Academic Principal for Executive Clearance.'}), 200'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed clearance endpoints in server.py.")
else:
    print("Could not find exact old block.")

