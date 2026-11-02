with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
old = """if not PRINCIPAL_DEMO_MODE:\n\n    _saved_sr = _load_json_file(SERVICE_REQUESTS_FILE)\n\n    if isinstance(_saved_sr, list) and _saved_sr:\n\n        DB['serviceRequests'] = _saved_sr\n\n    _saved_students = _load_json_file(STUDENTS_OVERLAY_FILE)\n\n    if isinstance(_saved_students, list) and _saved_students:\n\n        DB['students'] = _saved_students"""

new = """_saved_sr = _load_json_file(SERVICE_REQUESTS_FILE)\nif isinstance(_saved_sr, list) and _saved_sr:\n    DB['serviceRequests'] = _saved_sr\n\nif not PRINCIPAL_DEMO_MODE:\n    _saved_students = _load_json_file(STUDENTS_OVERLAY_FILE)\n    if isinstance(_saved_students, list) and _saved_students:\n        DB['students'] = _saved_students"""

if old in text:
    text = text.replace(old, new, 1)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Updated loader!")
else:
    print("Failed")

