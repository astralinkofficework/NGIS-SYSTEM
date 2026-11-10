with open('timetable_api.py', 'r', encoding='utf-8') as f:
    text = f.read()
idx = text.find('@timetable_bp.route("/grid"')
print(text[idx:idx+800])

