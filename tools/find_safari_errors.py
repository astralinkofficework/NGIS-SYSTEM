import os
import re

class_list_space = re.compile(r'classList\.(?:add|remove|toggle)\s*\(\s*[\'"][^\'"]*\s+[^\'"]*[\'"]')
qs_concat = re.compile(r'querySelector(?:All)?\s*\(\s*[\'"][#\.][^\'"]*[\'"]\s*\+')
qs_unquoted_attr = re.compile(r'querySelector(?:All)?\s*\(\s*[\'"]\[[a-zA-Z0-9_-]+=\s*[\'"]\s*\+')

print("=== Scanning for classList with spaces ===")
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', '.system_generated']):
        continue
    for f in files:
        if f.endswith(('.js', '.html')):
            p = os.path.normpath(os.path.join(root, f))
            try:
                with open(p, encoding='utf-8', errors='ignore') as fp:
                    for idx, line in enumerate(fp):
                        if class_list_space.search(line):
                            print(f"{p}:{idx+1}: {line.strip()[:110]}")
            except Exception:
                pass

print("\n=== Scanning for potentially unescaped querySelector concatenations ===")
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['node_modules', '.git', '.gemini', '.system_generated']):
        continue
    for f in files:
        if f.endswith(('.js', '.html')):
            p = os.path.normpath(os.path.join(root, f))
            try:
                with open(p, encoding='utf-8', errors='ignore') as fp:
                    for idx, line in enumerate(fp):
                        if qs_unquoted_attr.search(line):
                            print(f"{p}:{idx+1}: {line.strip()[:110]}")
            except Exception:
                pass
