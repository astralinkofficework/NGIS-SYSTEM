import json

d = json.load(open('data/timetable_state.json', encoding='utf-8'))
for t in d.get('teachers', [])[:10]:
    print(t.get('code'), t.get('name_kh'), t.get('name_en'), t.get('specialization'))

