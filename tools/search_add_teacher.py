import os

print("=== Searching for 'Add Teacher' ===")
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', '.system_generated']):
        continue
    for f in files:
        if f.endswith(('.js', '.html')):
            p = os.path.normpath(os.path.join(root, f))
            try:
                with open(p, encoding='utf-8', errors='ignore') as fp:
                    for idx, line in enumerate(fp):
                        if 'add teacher' in line.lower() or 'add-teacher' in line.lower():
                            print(f"{p}:{idx+1}: {line.strip()[:120]}")
            except Exception:
                pass
