import os

targets = [
    'btnAddNewEntry', 'addNewSubjectBtn', 'btnAddTeacher', 'nrg-add-dept-btn',
    'nrg-add-class-btn', 'btnNewExemption', 'btnOpenNewAssign', 'btnIssueAward',
    'btnLogCase', 'btnLogEffort', 'btnAddDept', 'svCreate'
]

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as fp:
                for i, line in enumerate(fp, 1):
                    for t in targets:
                        if t in line:
                            print(f"{path}:{i}: {line.strip()[:110]}")
                            break
