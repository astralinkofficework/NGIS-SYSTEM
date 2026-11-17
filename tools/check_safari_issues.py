import os, re

def check_file(path):
    issues = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        lines = content.splitlines()

    # 1. Lookbehinds in regex (?<= or (?<!
    lookbehind_re = re.compile(r'\(\?\<[=!][^)]*\)')
    for i, line in enumerate(lines, 1):
        if lookbehind_re.search(line):
            issues.append((i, "Regex lookbehind (fails on iOS < 16.4)", line.strip()))

    # 2. querySelector with unescaped / unquoted dynamic attributes: e.g. [data-id=' + or [data-id=" +
    # or querySelector('#' + id) where id might start with a digit
    unquoted_attr = re.compile(r'querySelector(All)?\s*\(\s*[\'"][^\[]*\[\s*[\w\-]+\s*=\s*[\'"]\s*\+')
    for i, line in enumerate(lines, 1):
        if ('querySelector' in line or 'querySelectorAll' in line) and ('[' in line and '=' in line):
            # check if attribute value is quoted: e.g. [data-id=" + id + "] vs [data-id=' + id + '] vs [data-id=' +
            if re.search(r'\[[a-zA-Z\-]+\s*=\s*(\+|(?![\'\"])[a-zA-Z0-9_]+)', line):
                issues.append((i, "Unquoted attribute selector in querySelector", line.strip()))

    # 3. classList.add / remove with variable that might be a multi-class string
    # e.g. el.classList.add(SOME_CLASSES)
    var_classlist = re.compile(r'classList\.(add|remove)\s*\(\s*([a-zA-Z0-9_]+)\s*\)')
    for i, line in enumerate(lines, 1):
        m = var_classlist.search(line)
        if m:
            var_name = m.group(2)
            if any(term in var_name.lower() for term in ['class', 'cls', 'btn', 'style']):
                issues.append((i, f"Variable '{var_name}' passed to classList.{m.group(1)} (could contain spaces)", line.strip()))

    # 4. new Date with non-standard string formats: e.g. new Date(str) where str is 'YYYY-MM-DD HH:mm:ss'
    for i, line in enumerate(lines, 1):
        if 'new Date(' in line and 'replace' not in line and ('/' in line or '-' in line):
            pass

    return issues

all_issues = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.js'):
            path = os.path.join(root, file)
            issues = check_file(path)
            for iss in issues:
                all_issues.append((path, iss[0], iss[1], iss[2]))

print(f"Total findings: {len(all_issues)}")
for path, line_no, desc, line in all_issues[:50]:
    print(f"{path}:{line_no} [{desc}]: {line}")
