import os

replacements = {
    r'.\assets\css\ui-states.css': [
        ('#163c2c', '#193DAA')
    ],
    r'.\assets\js\academic-live.js': [
        ('#13829b', '#2455D6')
    ],
    r'.\pages\admin\admin-lifecycle.html': [
        ('background: #163c2c;', 'background: #193DAA;')
    ],
    r'.\pages\admin\css\dashboard.css': [
        ('#2f4550', '#2455D6'),
        ('#b8dbd9', '#E5EAF2'),
        ('#586f7c', '#64748B')
    ],
    r'.\pages\student\css\base.css': [
        ('--charcoal-blue: #2f4550;', '--charcoal-blue: #2455D6;'),
        ('--blue-slate:    #586f7c;', '--blue-slate:    #64748B;'),
        ('--light-blue:    #b8dbd9;', '--light-blue:    #EAF2FF;'),
        ('background-color: #13829b;', 'background-color: #2455D6;')
    ],
    r'.\pages\student\css\calendar.css': [
        ('#2f4550', '#2455D6')
    ],
    r'.\pages\student\css\hero.css': [
        ('#13829b', '#2455D6'),
        ('#2f4550', '#243247'),
        ('#2F4550', '#243247'),
        ('#b8dbd9', '#EAF2FF'),
        ('#B8DBD9', '#EAF2FF')
    ],
    r'.\pages\student\css\modal.css': [
        ('#2f4550', '#2455D6'),
        ('#b8dbd9', '#E5EAF2')
    ],
    r'.\pages\student\css\overlap.css': [
        ('#586f7c', '#64748B'),
        ('#13829b', '#2455D6'),
        ('linear-gradient(135deg, #0e7490 0%, #13829b 50%, #1e3a8a 100%)', 'linear-gradient(135deg, #193DAA 0%, #2455D6 100%)')
    ],
    r'.\pages\student\css\responsive.css': [
        ('#b8dbd9', '#E5EAF2')
    ],
    r'.\pages\student\css\service-hub.css': [
        ('#b8dbd9', '#E5EAF2'),
        ('#2f4550', '#2455D6'),
        ('#586f7c', '#64748B')
    ],
    r'.\pages\student\css\student-inline.css': [
        ('#2f4550', '#2455D6'),
        ('#b8dbd9', '#E5EAF2'),
        ('#586f7c', '#64748B')
    ],
    r'.\pages\student\js\hero.js': [
        ("color: '#2f4550', bg: 'rgba(47,69,80,0.1)'", "color: '#2455D6', bg: 'rgba(36,85,214,0.1)'")
    ],
    r'.\pages\teacher\teacher-gradebook.html': [
        ("hover: '#163c2c'", "hover: '#193DAA'")
    ],
    r'.\pages\teacher\teacher-grades.html': [
        ("hover: '#163c2c'", "hover: '#193DAA'")
    ],
    r'.\pages\teacher\teacher-reports.html': [
        ("500: '#2d6a4f'", "500: '#2455D6'")
    ],
    r'.\pages\teacher\js\attendance.js': [
        ('#13829b', '#2455D6')
    ],
    r'.\pages\teacher\js\calendar.js': [
        ('#13829b', '#2455D6')
    ],
    r'.\pages\teacher\js\classes.js': [
        ('#13829b', '#2455D6')
    ]
}

modified = 0
for fpath, rules in replacements.items():
    if not os.path.exists(fpath):
        print(f'File not found: {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as fp:
        content = fp.read()
    orig = content
    for old, new in rules:
        content = content.replace(old, new)
    if content != orig:
        with open(fpath, 'w', encoding='utf-8', newline='\r\n') as fp:
            fp.write(content)
        modified += 1
        print(f'Updated {fpath}')
    else:
        print(f'No change in {fpath}')

print(f'Completed. Total files updated: {modified}')

