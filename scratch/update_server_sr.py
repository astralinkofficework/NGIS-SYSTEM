with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """@app.route('/api/service-requests', methods=['GET'])
def get_service_requests():
    status = request.args.get('status')
    category = request.args.get('category')
    type_ = request.args.get('type')
    campus = request.args.get('campus')
    student_id = request.args.get('studentId')
    
    items = DB['serviceRequests']
    if status and status != 'all':
        items = [r for r in items if r['status'] == status]
    if category:
        items = [r for r in items if r['category'] == category]
    if type_:
        items = [r for r in items if r['type'] == type_]
    if campus:
        items = [r for r in items if r['campus'] == campus]
    if student_id:
        items = [r for r in items if r['studentId'] == student_id]
    
    items.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    return jsonify({'data': items, 'meta': {'total': len(items)}})

@app.route('/api/service-requests/<id>', methods=['GET'])
def get_service_request(id):
    item = next((r for r in DB['serviceRequests'] if r['id'] == id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Service request not found'}}), 404
    return jsonify({'data': item})

@app.route('/api/service-requests', methods=['POST'])
def create_service_request():
    data = request.get_json()
    student_id = data.get('studentId')
    student_name = data.get('studentName')
    category = data.get('category')
    type_ = data.get('type')
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    campus = data.get('campus')
    
    if not student_id or not category or not type_ or not title:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'studentId, category, type, and title are required'}}), 400
    
    id = f"SR-{1000 + len(DB['serviceRequests']) + 1}"
    entry = {
        'id': id,
        'studentId': student_id,
        'studentName': student_name or 'Student',
        'category': category,
        'type': type_,
        'title': title,
        'description': description or '',
        'status': 'open',
        'priority': priority or 'normal',
        'campus': campus or 'Sensok',
        'assignee': '',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'updatedAt': datetime.now().strftime('%Y-%m-%d'),
        'comments': []
    }
    DB['serviceRequests'].append(entry)
    return jsonify({'data': entry, 'message': 'Service request submitted'}), 201"""

replacement = """@app.route('/api/service-requests', methods=['GET'])
def get_service_requests():
    status = request.args.get('status')
    category = request.args.get('category')
    type_ = request.args.get('type')
    campus = request.args.get('campus')
    student_id = request.args.get('studentId') or request.args.get('userId') or request.args.get('requesterId')
    role = request.args.get('role')
    
    items = DB['serviceRequests']
    if status and status != 'all':
        items = [r for r in items if r.get('status') == status]
    if category and category != 'all':
        items = [r for r in items if r.get('category') == category]
    if type_ and type_ != 'all':
        items = [r for r in items if r.get('type') == type_]
    if campus and campus != 'all':
        items = [r for r in items if r.get('campus') == campus]
    if student_id and student_id != 'all':
        items = [r for r in items if r.get('studentId') == student_id]
    if role and role != 'all':
        items = [r for r in items if r.get('role') == role or (role == 'teacher' and str(r.get('studentId', '')).startswith('TCH')) or (role == 'student' and str(r.get('studentId', '')).startswith('2026-STD'))]
    
    items.sort(key=lambda x: datetime.strptime(x.get('date', '2026-01-01'), '%Y-%m-%d'), reverse=True)
    return jsonify({'data': items, 'meta': {'total': len(items)}})

@app.route('/api/service-requests/<id>', methods=['GET'])
def get_service_request(id):
    item = next((r for r in DB['serviceRequests'] if r['id'] == id), None)
    if not item:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Service request not found'}}), 404
    return jsonify({'data': item})

@app.route('/api/service-requests', methods=['POST'])
def create_service_request():
    data = request.get_json() or {}
    student_id = data.get('studentId') or data.get('requesterId') or data.get('userId') or 'TCH-2024-042'
    student_name = data.get('studentName') or data.get('requesterName') or data.get('userName') or 'Dr. Sarah Jenkins'
    role = data.get('role') or data.get('requesterRole') or ('teacher' if str(student_id).startswith('TCH') else 'student')
    category = data.get('category')
    type_ = data.get('type')
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority') or 'normal'
    campus = data.get('campus') or 'Sensok'
    
    if not student_id or not category or not type_ or not title:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'studentId, category, type, and title are required'}}), 400
    
    id = f"SR-{1000 + len(DB['serviceRequests']) + 1}"
    entry = {
        'id': id,
        'studentId': student_id,
        'studentName': student_name,
        'role': role,
        'category': category,
        'type': type_,
        'title': title,
        'description': description or '',
        'status': 'open',
        'priority': priority,
        'campus': campus,
        'assignee': 'Operations & Academic Facilities',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'updatedAt': datetime.now().strftime('%Y-%m-%d'),
        'comments': [
            {'by': student_name, 'text': f'Submitted service request for {title}.', 'date': datetime.now().strftime('%Y-%m-%d')}
        ]
    }
    DB['serviceRequests'].append(entry)
    try:
        _persist_service_requests()
    except Exception as e:
        pass
    return jsonify({'data': entry, 'message': 'Service request submitted'}), 201"""

content_norm = content.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')

if target_norm in content_norm:
    content_norm = content_norm.replace(target_norm, replacement.replace('\r\n', '\n'), 1)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content_norm.replace('\n', '\r\n'))
    print("SUCCESS: Updated service requests API in server.py")
else:
    print("ERROR: Target not found in server.py")

