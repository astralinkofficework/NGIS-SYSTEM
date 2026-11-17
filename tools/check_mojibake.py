import os

extensions = ('.html', '.js', '.css')
mojibake_chars = ['\ufffd', '\u00e2\u20ac\u201d', '\u00e2\u20ac\u201c', '\u00e2\u20ac\u00a6', '\u00c3\u00a2']

results = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or '.gemini' in root or 'tools' in root or '.system_generated' in root:
        continue
    for file in files:
        if file.endswith(extensions):
            path = os.path.normpath(os.path.join(root, file))
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                for m in mojibake_chars:
                    if m in content:
                        results.append((path, repr(m), content.count(m)))
            except Exception as e:
                pass

for path, m, count in sorted(set(results)):
    print(f"{path}: {count} occurrences of {m}")
