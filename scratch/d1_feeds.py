# D1 feed cleanup: strip doomed pages from all_pages_data.json / .js (feeds pages-directory.html)
import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GONE = {'admin-accounts.html','admin-admins.html','admin-audit.html','admin-principals.html',
        'admin-students.html','admin-student-profile.html','admin-teachers.html',
        'teacher-grade.html','teacher-grades.html'}

data = json.load(open('all_pages_data.json', encoding='utf-8'))
items = data if isinstance(data, list) else data.get('pages', data)
print('type:', type(data).__name__, '| entries before:', len(items))
kept = [p for p in items if p.get('name') not in GONE and p.get('path', '').split('/')[-1] not in GONE]
removed = len(items) - len(kept)
json.dump(data if isinstance(data, list) else {**data, ('pages' if 'pages' in data else list(data)[0]): kept},
          open('all_pages_data.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
js = 'const ALL_PAGES = ' + json.dumps(kept, indent=2, ensure_ascii=False) + ';\n'
open('all_pages_data.js', 'w', encoding='utf-8').write(js)
print('removed entries:', removed, '| kept:', len(kept))
# validate
json.load(open('all_pages_data.json', encoding='utf-8'))
print('json valid: OK')
