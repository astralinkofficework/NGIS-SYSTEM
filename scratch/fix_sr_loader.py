with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = """if not PRINCIPAL_DEMO_MODE:
    _saved_sr = _load_json_file(SERVICE_REQUESTS_FILE)
    if isinstance(_saved_sr, list) and _saved_sr:
        DB['serviceRequests'] = _saved_sr
    _saved_students = _load_json_file(STUDENTS_OVERLAY_FILE)
    if isinstance(_saved_students, list) and _saved_students:
        DB['students'] = _saved_students"""

replacement = """_saved_sr = _load_json_file(SERVICE_REQUESTS_FILE)
if isinstance(_saved_sr, list) and _saved_sr:
    DB['serviceRequests'] = _saved_sr

if not PRINCIPAL_DEMO_MODE:
    _saved_students = _load_json_file(STUDENTS_OVERLAY_FILE)
    if isinstance(_saved_students, list) and _saved_students:
        DB['students'] = _saved_students"""

content_norm = content.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')

if target_norm in content_norm:
    content_norm = content_norm.replace(target_norm, replacement.replace('\r\n', '\n'), 1)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content_norm.replace('\n', '\r\n'))
    print("SUCCESS: Updated service requests loader in server.py")
else:
    print("ERROR: Target not found")

