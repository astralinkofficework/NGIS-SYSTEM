# teacher-classes removal: rewire inbound links -> teacher-roster.html + clean feeds
import re, sys, json, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

for f in ['pages/teacher/teacher.html', 'pages/teacher/teacher-departments.html', 'pages/teacher/js/classes.js']:
    t = open(f, encoding='utf-8').read()
    n = t.count('teacher-classes.html')
    t = t.replace('teacher-classes.html', 'teacher-roster.html')
    open(f, 'w', encoding='utf-8').write(t)
    print(f'{f}: {n}x rewired -> teacher-roster.html')

data = json.load(open('all_pages_data.json', encoding='utf-8'))
kept = [p for p in data if p.get('name') != 'teacher-classes.html']
print('feed entries removed:', len(data) - len(kept))
json.dump(kept, open('all_pages_data.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
open('all_pages_data.js', 'w', encoding='utf-8').write('const ALL_PAGES = ' + json.dumps(kept, indent=2, ensure_ascii=False) + ';\n')
json.load(open('all_pages_data.json', encoding='utf-8'))
print('feed json valid: OK | kept:', len(kept))

# any remaining live refs?
live = glob.glob('pages/**/*.html', recursive=True) + glob.glob('pages/**/*.js', recursive=True) + glob.glob('assets/js/*.js') + ['index.html', 'layout.js', 'all_pages_data.js']
left = [f for f in live if 'teacher-classes.html' in open(f, encoding='utf-8', errors='replace').read()]
print('remaining refs:', left or 'NONE')
