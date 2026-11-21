import re

target_files = [
    'pages/admin/admin-campus.html',
    'pages/principal/principal-requests.html',
    'assets/js/academic-requests.js',
    'pages/principal/principal-subjects.html',
    'pages/admin/admin-lost-found.html',
    'pages/admin/admin-student-assign.html',
    'assets/js/khmer-suite-ui.js'
]

competing_re = re.compile(r'\b(?:bg|text|border)-(?:purple|indigo|pink|violet|fuchsia|cyan)-[0-9]{2,3}\b')

for fpath in target_files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"\n=== {fpath} ===")
        for i, line in enumerate(lines):
            matches = competing_re.findall(line)
            if matches:
                print(f"  Line {i+1:4d} [{', '.join(matches)}]: {line.strip()[:100]}")
    except Exception as e:
        print(f"Error {fpath}: {e}")
