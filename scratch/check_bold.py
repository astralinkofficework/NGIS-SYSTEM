import re

def check_bold(filepath):
    content = open(filepath, 'r', encoding='utf-8').read()
    bold_patterns = [
        r'\bfont-bold\b',
        r'\bfont-semibold\b',
        r'\bfont-extrabold\b',
        r'\bfont-black\b',
        r'font-weight\s*:\s*[6-9]\d\d',
        r'fontWeight\s*:\s*["\'][6-9]\d\d["\']'
    ]
    issues = []
    for pat in bold_patterns:
        matches = re.findall(pat, content)
        if matches:
            issues.append((pat, len(matches)))
    return issues

files_to_check = [
    'pages/principal/principal-timetables.html',
    'pages/admin/admin-timetables.html'
]

for f in files_to_check:
    res = check_bold(f)
    print(f, "Issues:", res)
