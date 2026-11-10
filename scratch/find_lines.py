with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['function recordsHtml', 'function builderHtml', 'function viewerHtml', 'function subjectsAdminHtml']):
        print(f"Line {i+1}: {l.strip()}")
