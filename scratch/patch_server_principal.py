import re

departments_data = """
    # ── Departments ──
    'departments': [
        {
            'id': 'dept-mat', 'code': 'MATH', 'name': 'Mathematics Department',
            'head': 'Dr. Sarah Jenkins', 'headId': 'TCH-2024-042', 'teachersCount': 26, 'studentsCount': 890,
            'room': 'Room 301, Admin Bldg A', 'email': 'math.dept@ngis.edu.kh',
            'subjects': ['Advanced Mathematics', 'Calculus I', 'Algebra II', 'Statistics & Probability'],
            'curriculum': 'Cambridge International A-Level & IGCSE Mathematics',
            'status': 'active', 'syllabusCompliance': 100
        },
        {
            'id': 'dept-sci', 'code': 'SCI', 'name': 'Science Department',
            'head': 'Dr. Pov Sophea', 'headId': 'TCH-2024-015', 'teachersCount': 24, 'studentsCount': 780,
            'room': 'Science Wing Lab 2', 'email': 'science.dept@ngis.edu.kh',
            'subjects': ['Physics & Lab', 'Chemistry', 'AP Biology', 'Environmental Systems'],
            'curriculum': 'Cambridge IGCSE & Advanced Science Practical Laboratories',
            'status': 'active', 'syllabusCompliance': 98
        },
        {
            'id': 'dept-eng', 'code': 'ENG', 'name': 'English Department',
            'head': 'Ms. Rin Lina', 'headId': 'TCH-2024-023', 'teachersCount': 28, 'studentsCount': 840,
            'room': 'Building B, Suite 204', 'email': 'english.dept@ngis.edu.kh',
            'subjects': ['English Literature', 'Academic Writing', 'World Literature', 'ESL Bridge'],
            'curriculum': 'Cambridge First Language English & Comparative World Literature',
            'status': 'active', 'syllabusCompliance': 100
        },
        {
            'id': 'dept-khm', 'code': 'KHM', 'name': 'Khmer Studies Department',
            'head': 'Mr. Chhem Sokha', 'headId': 'TCH-2024-031', 'teachersCount': 32, 'studentsCount': 920,
            'room': 'Main Hall, East Wing', 'email': 'khmer.dept@ngis.edu.kh',
            'subjects': ['Khmer Literature', 'Cambodian History & Civics', 'Khmer Composition', 'National Ethics'],
            'curriculum': 'Ministry of Education, Youth and Sport (MoEYS) National Bac II Framework',
            'status': 'active', 'syllabusCompliance': 100
        },
        {
            'id': 'dept-chn', 'code': 'CHN', 'name': 'Chinese Language Department',
            'head': 'Ms. Li Wei', 'headId': 'TCH-2024-055', 'teachersCount': 18, 'studentsCount': 610,
            'room': 'Language Lab 105', 'email': 'chinese.dept@ngis.edu.kh',
            'subjects': ['Mandarin Chinese I-IV', 'HSK 4-6 Preparation', 'Business Chinese', 'Chinese Culture'],
            'curriculum': 'Hanban International HSK Standard Curriculum',
            'status': 'active', 'syllabusCompliance': 96
        },
        {
            'id': 'dept-hum', 'code': 'HUM', 'name': 'Humanities & Social Sciences',
            'head': 'Mr. John Vance', 'headId': 'TCH-2024-067', 'teachersCount': 16, 'studentsCount': 540,
            'room': 'Building A, Room 412', 'email': 'humanities.dept@ngis.edu.kh',
            'subjects': ['Global Perspectives', 'World History', 'Economics & Business', 'Human Geography'],
            'curriculum': 'Cambridge International Global Perspectives & IGCSE Humanities',
            'status': 'active', 'syllabusCompliance': 97
        },
        {
            'id': 'dept-art', 'code': 'ART', 'name': 'Arts & Physical Education',
            'head': 'Coach Samreth Bora', 'headId': 'TCH-2024-082', 'teachersCount': 14, 'studentsCount': 900,
            'room': 'Campus Gymnasium Complex', 'email': 'pe.arts.dept@ngis.edu.kh',
            'subjects': ['Visual Arts & Design', 'Music & Performance', 'Physical Education', 'Athletics & Swimming'],
            'curriculum': 'Holistic Arts & National Interscholastic Athletic Association Framework',
            'status': 'active', 'syllabusCompliance': 100
        }
    ],

    # ── Timetables ──
    'timetables': [
        {'id': 'tt-1', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Monday', 'period': 1, 'time': '08:00 - 08:50', 'subject': 'Advanced Mathematics', 'teacherId': 'TCH-2024-042', 'teacherName': 'Dr. Sarah Jenkins', 'room': 'Room 302'},
        {'id': 'tt-2', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Monday', 'period': 2, 'time': '08:55 - 09:45', 'subject': 'Advanced Mathematics', 'teacherId': 'TCH-2024-042', 'teacherName': 'Dr. Sarah Jenkins', 'room': 'Room 302'},
        {'id': 'tt-3', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Monday', 'period': 3, 'time': '10:05 - 10:55', 'subject': 'Physics & Lab', 'teacherId': 'TCH-2024-015', 'teacherName': 'Dr. Pov Sophea', 'room': 'Science Lab 2'},
        {'id': 'tt-4', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Monday', 'period': 4, 'time': '11:00 - 11:50', 'subject': 'English Literature', 'teacherId': 'TCH-2024-023', 'teacherName': 'Ms. Rin Lina', 'room': 'Room 302'},
        {'id': 'tt-5', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Monday', 'period': 5, 'time': '13:00 - 13:50', 'subject': 'Khmer Literature', 'teacherId': 'TCH-2024-031', 'teacherName': 'Mr. Chhem Sokha', 'room': 'Room 302'},
        {'id': 'tt-6', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Monday', 'period': 6, 'time': '13:55 - 14:45', 'subject': 'World History', 'teacherId': 'TCH-2024-067', 'teacherName': 'Mr. John Vance', 'room': 'Room 412'},
        {'id': 'tt-7', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Tuesday', 'period': 1, 'time': '08:00 - 08:50', 'subject': 'Chemistry', 'teacherId': 'TCH-2024-015', 'teacherName': 'Dr. Pov Sophea', 'room': 'Science Lab 2'},
        {'id': 'tt-8', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Tuesday', 'period': 2, 'time': '08:55 - 09:45', 'subject': 'Advanced Mathematics', 'teacherId': 'TCH-2024-042', 'teacherName': 'Dr. Sarah Jenkins', 'room': 'Room 302'},
        {'id': 'tt-9', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Wednesday', 'period': 1, 'time': '08:00 - 08:50', 'subject': 'Physical Education', 'teacherId': 'TCH-2024-082', 'teacherName': 'Coach Samreth Bora', 'room': 'Gymnasium'},
        {'id': 'tt-10', 'classId': 'cls-10a', 'className': 'Grade 10A', 'day': 'Wednesday', 'period': 2, 'time': '08:55 - 09:45', 'subject': 'English Literature', 'teacherId': 'TCH-2024-023', 'teacherName': 'Ms. Rin Lina', 'room': 'Room 302'},
        {'id': 'tt-11', 'classId': 'cls-11a', 'className': 'Grade 11A', 'day': 'Monday', 'period': 1, 'time': '08:00 - 08:50', 'subject': 'Calculus I', 'teacherId': 'TCH-2024-042', 'teacherName': 'Dr. Sarah Jenkins', 'room': 'Room 201'},
        {'id': 'tt-12', 'classId': 'cls-11b', 'className': 'Grade 11B', 'day': 'Monday', 'period': 3, 'time': '10:05 - 10:55', 'subject': 'AP Biology', 'teacherId': 'TCH-2024-015', 'teacherName': 'Dr. Pov Sophea', 'room': 'Room 203'}
    ],
"""

routes_code = """
# ════════════════════════════════════════════════════════════════════
# PRINCIPAL CENTRAL MANAGEMENT SYSTEM API ROUTES (Highest School Authority)
# ════════════════════════════════════════════════════════════════════

@app.route('/api/classes/<class_id>', methods=['GET', 'PUT'])
def handle_single_class(class_id):
    c = next((item for item in DB['classes'] if item['id'] == class_id), None)
    if not c:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': f'Class {class_id} not found'}}), 404
    
    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        for key in ['name', 'grade', 'section', 'homeroomTeacher', 'room', 'studentCount', 'campus', 'status']:
            if key in data:
                c[key] = data[key]
        return jsonify({'status': 'success', 'message': 'Class details updated successfully', 'data': c})
    
    # Return class with enrolled students
    class_name = c['name'].replace('Grade ', '').strip()
    enrolled = [s for s in DB['students'] if s.get('class') == class_name or s.get('class') == c['name']]
    return jsonify({'data': c, 'students': enrolled, 'meta': {'enrolledTotal': len(enrolled)}})

@app.route('/api/departments', methods=['GET'])
def get_departments():
    depts = DB.get('departments', [])
    return jsonify({'status': 'success', 'data': depts, 'meta': {'total': len(depts)}})

@app.route('/api/departments/<dept_id>', methods=['GET', 'PUT'])
def handle_single_department(dept_id):
    depts = DB.get('departments', [])
    d = next((item for item in depts if item['id'] == dept_id or item.get('code', '').lower() == dept_id.lower()), None)
    if not d:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Department not found'}}), 404
    
    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        for key in ['name', 'head', 'headId', 'room', 'email', 'curriculum', 'status', 'syllabusCompliance']:
            if key in data:
                d[key] = data[key]
        return jsonify({'status': 'success', 'message': 'Department information updated', 'data': d})
    
    # Also find assigned teachers
    dept_teachers = [t for t in DB['teachers'] if t.get('department', '').lower() in d['name'].lower()]
    return jsonify({'data': d, 'teachers': dept_teachers})

@app.route('/api/assignments/<asgn_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_assignment(asgn_id):
    asg = next((a for a in DB['assignments'] if a['id'] == asgn_id), None)
    if not asg:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': 'Assignment not found'}}), 404
    
    if request.method == 'PUT':
        data = request.get_json(silent=True) or {}
        for field in ['title', 'description', 'dueDate', 'due_date', 'maxScore', 'max_score', 'status', 'subject_name', 'class_name']:
            if field in data:
                asg[field] = data[field]
        return jsonify({'status': 'success', 'message': 'Assignment updated successfully', 'data': asg})
    
    if request.method == 'DELETE':
        DB['assignments'] = [a for a in DB['assignments'] if a['id'] != asgn_id]
        return jsonify({'status': 'success', 'message': 'Assignment removed'})
        
    return jsonify({'data': asg})

@app.route('/api/timetables', methods=['GET', 'POST'])
def handle_timetables():
    tt = DB.get('timetables', [])
    class_id = request.args.get('classId')
    teacher_id = request.args.get('teacherId')
    day = request.args.get('day')
    
    filtered = tt
    if class_id and class_id != 'all':
        filtered = [s for s in filtered if s.get('classId') == class_id]
    if teacher_id and teacher_id != 'all':
        filtered = [s for s in filtered if s.get('teacherId') == teacher_id]
    if day and day != 'all':
        filtered = [s for s in filtered if s.get('day').lower() == day.lower()]
        
    return jsonify({'data': filtered, 'meta': {'total': len(filtered)}})

@app.route('/api/timetables/slot', methods=['POST'])
def save_timetable_slot():
    data = request.get_json(silent=True) or {}
    slot_id = data.get('id')
    day = data.get('day')
    period = int(data.get('period', 1))
    class_id = data.get('classId')
    teacher_id = data.get('teacherId')
    room = data.get('room')
    force = data.get('force', False)
    
    tt = DB.get('timetables', [])
    
    # Conflict Detection:
    if not force:
        conflict = next((s for s in tt if s.get('day') == day and s.get('period') == period and s.get('id') != slot_id and (
            (s.get('teacherId') == teacher_id and s.get('classId') != class_id) or
            (s.get('room') == room and s.get('classId') != class_id)
        )), None)
        
        if conflict:
            reason = f"Schedule Conflict: {conflict.get('teacherName')} or {room} is already booked for {conflict.get('className')} during Period {period} on {day}."
            return jsonify({'conflict': True, 'message': reason, 'conflictSlot': conflict}), 409
            
    existing = next((s for s in tt if s.get('id') == slot_id), None)
    if existing:
        for k in ['subject', 'teacherId', 'teacherName', 'room', 'time', 'day', 'period']:
            if k in data:
                existing[k] = data[k]
        saved = existing
    else:
        new_id = f"tt-{len(tt) + 1}"
        saved = {
            'id': new_id,
            'classId': class_id,
            'className': data.get('className', 'Class'),
            'day': day,
            'period': period,
            'time': data.get('time', '08:00 - 08:50'),
            'subject': data.get('subject', 'General Subject'),
            'teacherId': teacher_id,
            'teacherName': data.get('teacherName', 'Faculty Member'),
            'room': room
        }
        tt.append(saved)
        
    return jsonify({'status': 'success', 'message': 'Timetable slot saved successfully', 'data': saved})

@app.route('/api/principal/attendance/correct', methods=['POST'])
def principal_correct_attendance():
    data = request.get_json(silent=True) or {}
    student_id = data.get('studentId')
    date_val = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    new_status = data.get('newStatus', 'present')
    reason = (data.get('reason') or '').strip()
    
    if not reason:
        return jsonify({'error': {'code': 'REASON_REQUIRED', 'message': 'A reason is required to correct official attendance.'}}), 400
        
    existing = next((a for a in DB['attendanceRecords'] if a.get('studentId') == student_id and a.get('date') == date_val), None)
    if existing:
        prev_status = existing['status']
        existing['status'] = new_status
        existing['correctedBy'] = 'Dr. Ly Bunheng (Principal)'
        existing['correctionReason'] = reason
        existing['correctedAt'] = datetime.now().isoformat()
    else:
        prev_status = 'unrecorded'
        student = next((s for s in DB['students'] if s['id'] == student_id), None)
        existing = {
            'studentId': student_id,
            'studentName': student['name'] if student else 'Student',
            'classId': student['class'] if student else '10A',
            'date': date_val,
            'status': new_status,
            'correctedBy': 'Dr. Ly Bunheng (Principal)',
            'correctionReason': reason,
            'correctedAt': datetime.now().isoformat()
        }
        DB['attendanceRecords'].append(existing)
        
    return jsonify({'status': 'success', 'message': f'Attendance updated from {prev_status} to {new_status}', 'data': existing})
"""

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read().replace('\r\n', '\n')

# 1. Insert departments and timetables into DB = {
if "'departments':" not in text:
    target_db_end = "\n    ]\n\n}"
    replacement_db = "\n    ],\n" + departments_data + "\n}"
    if target_db_end in text:
        text = text.replace(target_db_end, replacement_db, 1)
        print("Inserted departments & timetables into DB in server.py")
    else:
        print("target_db_end NOT found")

# 2. Append new routes before if __name__ == '__main__':
if "/api/departments" not in text:
    target_start = "# ── Start ──"
    if target_start in text:
        text = text.replace(target_start, routes_code + "\n\n" + target_start)
        print("Appended principal management routes to server.py")
    else:
        print("target_start NOT found")

with open('server.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("Finished updating server.py")

