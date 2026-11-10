with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    for act in ['add-teacher-row', 'save-teachers-spreadsheet', 'reset-teachers-data', 'copy-teachers-clipboard', 'cell-edit']:
        if act in line:
            print(f"Line {i+1}: {line.strip()[:100]}")

