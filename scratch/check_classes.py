import json

d = json.load(open('data/timetable_state.json', encoding='utf-8'))
classes = d.get('classes', [])
print("Classes sample:", classes[:4])

