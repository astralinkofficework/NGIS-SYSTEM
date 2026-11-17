import os, re

pattern_re = re.compile(r'pattern=[\'"]([^\'"]+)[\'"]')

for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', 'brain', 'tools']):
        continue
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_no, line in enumerate(f, 1):
                    m = pattern_re.search(line)
                    if m:
                        p_val = m.group(1)
                        try:
                            re.compile(p_val)
                            print(f"{path}:{line_no}: pattern='{p_val}' (valid)")
                        except Exception as e:
                            print(f"{path}:{line_no}: pattern='{p_val}' INVALID REGEX: {e}")
