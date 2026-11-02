# ════════════════════════════════════════════════════════════════════
# PRINCIPAL CENTRAL MANAGEMENT & OVERSIGHT API LAYER
# ════════════════════════════════════════════════════════════════════
# Every item in this layer is derived from live records: the SQLite
# academic store (grade workflow + audit_events), the persisted
# transcript and service-request files, and the school rosters. The
# rosters are persisted through overlay JSON files so Principal edits
# survive server restarts. Decisions update the original records,
# notify the submitter, and write a durable audit trail.

SERVICE_REQUESTS_FILE = os.path.join(ROOT, 'data', 'service_requests.json')
STUDENTS_OVERLAY_FILE = os.path.join(ROOT, 'data', 'students_overlay.json')

def _load_json_file(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as exc:
        print(f"Error loading {path}: {exc}")
        return default

def _write_json_file(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

def _persist_service_requests():
    _write_json_file(SERVICE_REQUESTS_FILE, DB['serviceRequests'])

def _persist_students():
    _write_json_file(STUDENTS_OVERLAY_FILE, DB['students'])

# Restore persisted state at startup (overlays win when present).
_saved_sr = _load_json_file(SERVICE_REQUESTS_FILE)
if isinstance(_saved_sr, list) and _saved_sr:
    DB['serviceRequests'] = _saved_sr
_saved_students = _load_json_file(STUDENTS_OVERLAY_FILE)
if isinstance(_saved_students, list) and _saved_students:
    DB['students'] = _saved_students

def _notify_user(user_id, title, message, ntype='general'):
    """Deliver an in-portal notification to a student or teacher account."""
    if not user_id:
        return
    try:
        nid = max([n.get('id', 0) for n in DB['notifications']] or [0]) + 1
    except Exception:
        nid = len(DB['notifications']) + 1
    DB['notifications'].append({
        'id': nid, 'userId': user_id, 'type': ntype, 'title': title,
        'message': message, 'read': False,
        'date': datetime.now().strftime('%Y-%m-%d')
    })

def _actor_label(user):
    return user.get('name') or (f"{user.get('firstName', '')} {user.get('lastName', '')}").strip() or 'Principal'

def _teacher_name(tid):
    t = next((x for x in DB['teachers'] if x.get('id') == tid), None)
    if t:
        return t.get('name', tid)
    u = next((x for x in AUTH_USERS.values() if x.get('id') == tid), None)
    if u:
        return f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()
    return tid

def _class_name(cid):
    c = next((x for x in DB['classes'] if x.get('id') == cid), None)
    return c.get('name', cid) if c else cid

def _period_name(pid):
    row = ACADEMIC.one('SELECT name FROM grading_periods WHERE id=? OR code=?', (pid, pid))
    return row.get('name', pid) if row else pid

def _last_decision(entity_id):
    row = ACADEMIC.one(
        "SELECT reason, actor_id, details_json, created_at FROM audit_events "
        "WHERE entity_type='approval' AND entity_id=? ORDER BY id DESC LIMIT 1", (entity_id,))
    if not row:
        return {'decidedBy': None, 'decisionNote': '', 'decidedAt': None}
    name = ''
    try:
        name = json.loads(row['details_json'] or '{}').get('actorName', '')
    except Exception:
        pass
    return {'decidedBy': name or row['actor_id'], 'decisionNote': row['reason'], 'decidedAt': row['created_at']}

def _grade_submission_groups(pending_only=True):
    """Live gradebook-release queue straight from the grades workflow table."""
    states = ("'draft','submitted','returned'" if pending_only else "'published'")
    return ACADEMIC.query(f"""
        SELECT a.class_id AS class_id, a.grading_period_id AS period_id,
               COUNT(DISTINCT g.assessment_id) AS assessments,
               COUNT(DISTINCT g.student_id) AS student_count,
               COUNT(*) AS records,
               ROUND(AVG(CASE WHEN a.max_score > 0 THEN 100.0 * g.score / a.max_score END), 1) AS avg_pct,
               SUM(CASE WHEN g.workflow='returned' THEN 1 ELSE 0 END) AS returned_ct,
               MAX(g.updated_at) AS last_update,
               GROUP_CONCAT(DISTINCT a.teacher_id) AS teacher_ids
        FROM grades g JOIN assessments a ON a.id = g.assessment_id
        WHERE g.workflow IN ({states}) AND g.score IS NOT NULL
        GROUP BY a.class_id, a.grading_period_id
        ORDER BY last_update DESC""")

def _transcript_approval_status(t):
    if t.get('verified'):
        return 'approved'
    status = (t.get('status') or '').lower()
    if 'reject' in status:
        return 'rejected'
    if 'return' in status or 'revision' in status:
        return 'needs_correction'
    return 'pending'

def build_principal_queue():
    items = []

    # 1 · Teacher gradebook releases (draft / submitted / returned workflow)
    for grp in _grade_submission_groups():
        key = f"grade:{grp['class_id']}:{grp['period_id']}"
        status = 'needs_correction' if grp['returned_ct'] else 'pending'
        teachers = ', '.join(_teacher_name(t) for t in (grp['teacher_ids'] or '').split(',') if t)
        item = {
            'id': key,
            'type': 'grade_submission',
            'category': 'Gradebook Release',
            'title': f"{_class_name(grp['class_id'])} · {_period_name(grp['period_id'])} gradebook release",
            'submittedBy': teachers or 'Faculty',
            'submittedRole': 'Teacher grade submission',
            'submittedAt': grp['last_update'],
            'scope': f"{grp['student_count']} students · {grp['records']} grade records · {grp['assessments']} assessments",
            'classId': grp['class_id'],
            'periodId': grp['period_id'],
            'details': 'Faculty-recorded grades awaiting executive clearance. Authorizing publishes them to the student and parent portals with recomputed GPA.',
            'diffOld': 'Unpublished (draft / submitted)',
            'diffNew': 'Official published gradebook & certified GPA',
            'status': status,
            'studentCount': grp['student_count'],
            'avgScore': f"{grp['avg_pct']}%" if grp['avg_pct'] is not None else '—',
        }
        item.update(_last_decision(key))
        items.append(item)

    # 2 · Student service requests that need an executive decision
    for r in DB['serviceRequests']:
        if r.get('category') not in ('document', 'academic', 'administration'):
            continue
        st = r.get('status')
        status_map = {'open': 'pending', 'pending': 'pending', 'in_progress': 'needs_correction',
                      'completed': 'approved', 'rejected': 'rejected'}
        if st not in status_map:
            continue
        item = {
            'id': f"request:{r['id']}",
            'type': 'service_request',
            'category': 'Student Request',
            'title': f"{r.get('title', 'Request')} · {r.get('studentName', 'Student')}",
            'submittedBy': r.get('studentName', 'Student'),
            'submittedRole': f"Student · {r.get('studentId', '')}",
            'submittedAt': r.get('date'),
            'scope': f"{r.get('category')} / {r.get('type', 'request')} · priority {r.get('priority', 'normal')}",
            'requestId': r['id'],
            'studentId': r.get('studentId'),
            'details': r.get('description', ''),
            'diffOld': f"Request status: {st}",
            'diffNew': 'Approved & fulfilled by the school office',
            'status': status_map[st],
        }
        # Most recent principal/office comment on the request doubles as the decision trail
        comments = r.get('comments') or []
        executive = next((c for c in reversed(comments) if str(c.get('by', '')).lower().startswith(('principal', 'executive'))), None)
        item['decidedBy'] = executive['by'] if executive else None
        item['decisionNote'] = executive['text'] if executive else ''
        item['decidedAt'] = executive['date'] if executive else None
        items.append(item)

    # 3 · Official transcript certifications (persisted upload records)
    for t in load_transcripts():
        item = {
            'id': f"transcript:{t.get('id')}",
            'type': 'transcript_certification',
            'category': 'Official Document',
            'title': f"Official transcript · {t.get('studentName', t.get('studentId', ''))} ({t.get('term', '')})",
            'submittedBy': t.get('uploadedBy', 'Registrar'),
            'submittedRole': f"Uploaded by {t.get('uploadedByRole', 'faculty')}",
            'submittedAt': t.get('uploadedAt'),
            'scope': f"{t.get('studentId', '')} · {t.get('classGrade', '')} · {t.get('fileName', '')}",
            'studentId': t.get('studentId'),
            'transcriptId': t.get('id'),
            'details': t.get('notes') or 'Uploaded academic transcript awaiting executive certification before release to the student portal.',
            'diffOld': 'Pending executive certification',
            'diffNew': 'Certified & digitally sealed by the Principal',
            'status': _transcript_approval_status(t),
        }
        item.update(_last_decision(item['id']))
        items.append(item)

    items.sort(key=lambda x: (0 if x['status'] == 'pending' else 1 if x['status'] == 'needs_correction' else 2, x.get('submittedAt') or ''), )
    return items

def _approval_counts(items):
    return {
        'total': len(items),
        'pending': sum(1 for i in items if i['status'] == 'pending'),
        'approved': sum(1 for i in items if i['status'] == 'approved'),
        'needs_correction': sum(1 for i in items if i['status'] == 'needs_correction'),
        'rejected': sum(1 for i in items if i['status'] == 'rejected'),
    }

_QUEUE_TYPE_BY_CATEGORY = {'grades': 'grade_submission', 'requests': 'service_request',
                           'transcripts': 'transcript_certification', 'clearance': 'service_request'}

@app.route('/api/principal/approvals', methods=['GET'])
def get_principal_approvals():
    user, error = _academic_require(('principal', 'admin'))
    if error: return error

    items = build_principal_queue()
    all_counts = _approval_counts(items)

    status_filter = (request.args.get('status') or 'all').lower()
    category_filter = (request.args.get('category') or 'all').lower()
    if category_filter not in ('all', 'grades', 'requests', 'transcripts', 'clearance'):
        category_filter = 'all'
    if category_filter != 'all':
        items = [i for i in items if i['type'] == _QUEUE_TYPE_BY_CATEGORY[category_filter]]
    if status_filter != 'all':
        items = [i for i in items if i['status'] == status_filter]

    return jsonify({'status': 'success', 'counts': all_counts, 'data': items})

@app.route('/api/principal/approvals/<item_id>/action', methods=['POST'])
def handle_principal_approval_action(item_id):
    user, error = _academic_require(('principal', 'admin'))
    if error: return error

    data = request.get_json(silent=True) or {}
    action = (data.get('action') or '').lower()
    note = (data.get('note') or '').strip()
    if action not in ('approve', 'reject', 'return', 'needs_correction'):
        return _academic_error('INVALID_ACTION', 'Action must be approve, reject, or needs_correction')
    if action in ('reject', 'needs_correction', 'return') and not note:
        return _academic_error('REASON_REQUIRED', 'A written reason is required when rejecting or returning a submission')

    actor_name = _actor_label(user)
    now_iso = ACADEMIC.now()
    prefix, _, rest = item_id.partition(':')

    if prefix == 'grade':
        parts = rest.split(':')
        if len(parts) != 2:
            return _academic_error('NOT_FOUND', 'Malformed gradebook approval id', 404)
        class_id, period_id = parts
        existing = next((g for g in _grade_submission_groups() if g['class_id'] == class_id and g['period_id'] == period_id), None)
        if not existing:
            return _academic_error('NOT_FOUND', 'No pending gradebook group matches this approval', 404)
        teachers = [t for t in (existing['teacher_ids'] or '').split(',') if t]
        new_state = 'published' if action == 'approve' else 'returned'
        ACADEMIC.execute(
            """UPDATE grades SET workflow=?, updated_at=? WHERE score IS NOT NULL AND workflow IN ('draft','submitted','returned')
               AND assessment_id IN (SELECT id FROM assessments WHERE class_id=? AND grading_period_id=?)""",
            (new_state, now_iso, class_id, period_id))
        ACADEMIC.audit(user['id'], user['role'],
                       'PRINCIPAL_PUBLISH_GRADES' if action == 'approve' else 'PRINCIPAL_RETURN_CORRECTION',
                       'approval', item_id, note or f'{action.title()} by {actor_name}',
                       {'actorName': actor_name, 'classId': class_id, 'periodId': period_id})
        for tid in teachers:
            _notify_user(tid, 'Gradebook decision',
                         f"{_class_name(class_id)} ({_period_name(period_id)}): " +
                         ('grades were authorized and published to student portals.' if action == 'approve'
                          else f'grades were returned for revision. Note: {note}'), 'grade')
        for st in ACADEMIC.query("SELECT DISTINCT student_id FROM grades WHERE workflow=? AND assessment_id IN (SELECT id FROM assessments WHERE class_id=? AND grading_period_id=?)",
                                 (new_state, class_id, period_id)):
            _notify_user(st['student_id'], 'Grades updated',
                         f"Your {_class_name(class_id)} results for {_period_name(period_id)} were " +
                         ('published by the Principal.' if action == 'approve' else 'returned by faculty for review.'), 'grade')

    elif prefix == 'request':
        sr_id = rest
        req = next((r for r in DB['serviceRequests'] if r['id'] == sr_id), None)
        if not req:
            return _academic_error('NOT_FOUND', 'Service request not found', 404)
        req['status'] = {'approve': 'completed', 'reject': 'rejected'}.get(action, 'in_progress')
        req['updatedAt'] = datetime.now().strftime('%Y-%m-%d')
        req.setdefault('comments', []).append({'by': f'Principal · {actor_name}', 'text': note or f'Executive decision: {action}', 'date': req['updatedAt']})
        _persist_service_requests()
        ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_REQUEST_DECISION', 'approval', item_id,
                       note or action, {'actorName': actor_name, 'requestId': sr_id, 'resultStatus': req['status']})
        _notify_user(req.get('studentId'), 'Service request update',
                     f"“{req.get('title', 'Request')}” is now: {req['status']}. " + (note or ''), 'general')

    elif prefix == 'transcript':
        tr_id = rest
        transcripts = load_transcripts()
        target = next((t for t in transcripts if t.get('id') == tr_id), None)
        if not target:
            return _academic_error('NOT_FOUND', 'Transcript record not found', 404)
        if action == 'approve':
            target['verified'] = True
            target['status'] = 'Certified & Released'
            target['certifiedBy'] = actor_name
            target['certifiedAt'] = now_iso
        elif action == 'reject':
            target['verified'] = False
            target['status'] = 'Rejected'
        else:
            target['verified'] = False
            target['status'] = 'Returned for Revision'
        target['decisionNote'] = note
        save_transcripts(transcripts)
        ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_TRANSCRIPT_DECISION', 'approval', item_id,
                       note or action, {'actorName': actor_name, 'transcriptId': tr_id,
                                        'studentId': target.get('studentId')})
        _notify_user(target.get('studentId'), 'Official transcript update',
                     f"Your transcript ({target.get('term', 'term')}) was {target['status'].lower()}. " + (note or ''), 'general')

    else:
        return _academic_error('NOT_FOUND', 'Unknown approval item', 404)

    items = build_principal_queue()
    return jsonify({'status': 'success', 'message': f'Approval {item_id} processed ({action})',
                    'counts': _approval_counts(items)})

@app.route('/api/principal/approvals/batch-action', methods=['POST'])
def handle_principal_batch_approvals():
    user, error = _academic_require(('principal', 'admin'))
    if error: return error

    data = request.get_json(silent=True) or {}
    action = (data.get('action') or 'approve').lower()
    if action != 'approve':
        return _academic_error('INVALID_ACTION', 'Batch action supports approve only')

    note = (data.get('note') or 'Batch authorized by Principal').strip()
    now_iso = ACADEMIC.now()
    groups = _grade_submission_groups()
    affected = len(groups)
    if affected:
        ACADEMIC.execute("UPDATE grades SET workflow='published', updated_at=? WHERE workflow IN ('draft','submitted','returned') AND score IS NOT NULL", (now_iso,))
        ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_BATCH_APPROVE', 'approval', 'all-pending', note,
                       {'actorName': _actor_label(user), 'count': affected})
    items = build_principal_queue()
    return jsonify({'status': 'success', 'message': f'Authorized {affected} gradebook group(s)',
                    'affected': affected, 'counts': _approval_counts(items)})

@app.route('/api/principal/audit', methods=['GET'])
def get_principal_audit_log():
    user, error = _academic_require(('principal', 'admin'))
    if error: return error
    limit = min(max(int(request.args.get('limit', 25)), 1), 200)
    role_filter = (request.args.get('role') or '').lower()
    search = (request.args.get('search') or '').lower()
    clauses, args = ['1=1'], []
    if role_filter and role_filter != 'all':
        clauses.append('actor_role=?'); args.append(role_filter)
    if search:
        clauses.append('(LOWER(action) LIKE ? OR LOWER(reason) LIKE ? OR LOWER(entity_id) LIKE ?)')
        like = f'%{search}%'
        args.extend([like, like, like])
    events = ACADEMIC.query(
        f"SELECT * FROM audit_events WHERE {' AND '.join(clauses)} ORDER BY id DESC LIMIT ?", (*args, limit))
    return jsonify({'status': 'success', 'data': [dict(e) for e in events]})

@app.route('/api/principal/stats', methods=['GET'])
def principal_stats():
    user, error = _academic_require(('principal', 'admin'))
    if error: return error

    queue = build_principal_queue()
    counts = _approval_counts(queue)
    att = ACADEMIC.one("SELECT COUNT(*) AS total, SUM(CASE WHEN status IN ('present','tardy','excused') THEN 1 ELSE 0 END) AS present FROM attendance")
    attendance_rate = round((att['present'] / att['total'] * 100), 1) if att and att['total'] else None
    gpas = [ACADEMIC.aggregate_gpa(s['id']) for s in DB['students'][:20]]
    gpas = [g for g in gpas if isinstance(g, (int, float)) and g > 0]
    avg_gpa = round(sum(gpas) / len(gpas), 2) if gpas else None
    recent = ACADEMIC.query("SELECT * FROM audit_events WHERE actor_role IN ('principal','admin') ORDER BY id DESC LIMIT 6")
    return jsonify({
        'status': 'success',
        'data': {
            'totalStudents': len(DB['students']),
            'totalTeachers': len(DB['teachers']),
            'totalClasses': len(DB['classes']),
            'activeServiceRequests': len([r for r in DB['serviceRequests'] if r.get('status') in ('open', 'pending', 'in_progress')]),
            'pendingApprovals': counts['pending'],
            'needsCorrection': counts['needs_correction'],
            'publishedGradeRecords': ACADEMIC.one("SELECT COUNT(*) AS n FROM grades WHERE workflow='published'")['n'],
            'draftGradeRecords': ACADEMIC.one("SELECT COUNT(*) AS n FROM grades WHERE workflow IN ('draft','submitted','returned')")['n'],
            'attendanceRate': attendance_rate,
            'averageGpa': avg_gpa,
            'recentActions': [dict(e) for e in recent],
        }
    })

# ── PRINCIPAL STUDENT RECORDS & AUTHORIZED EDITS ──
@app.route('/api/principal/roster/students', methods=['GET'])
def principal_roster_students():
    user, error = _academic_require(('principal', 'admin'))
    if error: return error
    search = (request.args.get('search') or '').lower()
    class_filter = (request.args.get('class') or '').strip()
    rows = []
    for s in DB['students']:
        if class_filter and s.get('class') != class_filter:
            continue
        if search and search not in str(s.get('name', '')).lower() and search not in str(s.get('id', '')).lower():
            continue
        rows.append({**s,
                     'gpaLive': ACADEMIC.aggregate_gpa(s['id']),
                     'attendancePct': ACADEMIC.attendance_summary(s['id']).get('percentage'),
                     'openRequests': len([r for r in DB['serviceRequests'] if r.get('studentId') == s['id'] and r.get('status') in ('open', 'pending', 'in_progress')])})
    classes = sorted({s.get('class') for s in DB['students'] if s.get('class')})
    return jsonify({'status': 'success', 'data': rows, 'classes': classes, 'meta': {'total': len(rows)}})

STUDENT_EDITABLE_FIELDS = ('name', 'gender', 'grade', 'class', 'status', 'parentEmail', 'parentName', 'advisor')

@app.route('/api/principal/roster/students/<student_id>', methods=['PUT'])
def principal_edit_student(student_id):
    user, error = _academic_require(('principal', 'admin'))
    if error: return error
    data = request.get_json(silent=True) or {}
    reason = (data.get('reason') or '').strip()
    if not reason:
        return _academic_error('REASON_REQUIRED', 'A written reason is mandatory for official record corrections')
    student = _student(student_id)
    if not student:
        return _academic_error('NOT_FOUND', 'Student not found', 404)
    changes = {k: data[k] for k in STUDENT_EDITABLE_FIELDS if k in data and str(data[k]) != str(student.get(k))}
    if not changes:
        return _academic_error('NO_CHANGES', 'No field values actually changed')
    previous = {k: student.get(k) for k in changes}
    student.update(changes)
    _persist_students()
    ACADEMIC.audit(user['id'], user['role'], 'PRINCIPAL_STUDENT_RECORD_EDIT', 'student', student_id, reason,
                   {'actorName': _actor_label(user), 'changes': changes, 'previous': previous})
    return jsonify({'status': 'success', 'data': student, 'message': 'Student record updated and audited'})

# ── PRINCIPAL FACULTY OVERSIGHT ──
@app.route('/api/principal/roster/teachers', methods=['GET'])
def principal_roster_teachers():
    user, error = _academic_require(('principal', 'admin'))
    if error: return error
    pending_by_teacher = {}
    for grp in _grade_submission_groups():
        for tid in (grp['teacher_ids'] or '').split(','):
            if tid:
                pending_by_teacher[tid] = pending_by_teacher.get(tid, 0) + grp['records']
    published_by_teacher = {r['recorded_by']: r['n'] for r in ACADEMIC.query(
        "SELECT recorded_by, COUNT(*) AS n FROM grades WHERE workflow='published' GROUP BY recorded_by")}
    rows = []
    for t in DB['teachers']:
        rows.append({**t,
                     'pendingGradeRecords': pending_by_teacher.get(t.get('id'), 0),
                     'publishedGradeRecords': published_by_teacher.get(t.get('id'), 0)})
    return jsonify({'status': 'success', 'data': rows, 'meta': {'total': len(rows)}})


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
