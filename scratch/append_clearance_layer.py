endpoints = '''

# ── TEACHER / PRINCIPAL GRADEBOOK CLEARANCE SYNC ──
@app.route('/api/academic/gradebook/clearance-status', methods=['GET'])
def academic_gradebook_clearance_status():
    class_id = request.args.get('classId', 'cls-10a')
    period_id = request.args.get('periodId', 'gp-q1')

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
    period_id = data.get('periodId', 'gp-q1')

    ACADEMIC.execute("""
        UPDATE grades SET workflow='submitted', updated_at=? 
        WHERE assessment_id IN (SELECT id FROM assessments WHERE class_id=?)
    """, (ACADEMIC.now(), class_id))

    ACADEMIC.audit('tch-jenkins', 'teacher', 'TEACHER_SUBMIT_CLEARANCE', 'gradebook', class_id, 'Submitted gradebook for Principal clearance', {'classId': class_id, 'periodId': period_id})

    return jsonify({'status': 'pending', 'workflow': 'submitted', 'message': 'Gradebook submitted to Academic Principal for Executive Clearance.'}), 200
'''

with open('scratch/new_principal_layer.py', 'a', encoding='utf-8') as f:
    f.write(endpoints)

print('Appended clearance routes to new_principal_layer.py')

