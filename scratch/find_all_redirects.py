import os, re

results = []
pattern = re.compile(r'(?:window\.)?location\.(?:href|replace)\s*=\s*[\'"`]([^\'"`]+)[\'"`]')

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                for line_idx, line in enumerate(lines):
                    m = pattern.search(line)
                    if m:
                        target = m.group(1)
                        results.append({
                            'file': p,
                            'line': line_idx + 1,
                            'target': target,
                            'content': line.strip()
                        })

print(f'Total location redirects found: {len(results)}')
# Filter for cross-role redirects (e.g. mentions of teacher, student, admin, etc.)
role_redirects = [r for r in results if any(k in r['target'] or k in r['content'] for k in ['teacher', 'student', 'admin', 'principal', 'staff', 'role'])]
print(f'Role-related redirects: {len(role_redirects)}')
for r in role_redirects:
    print(f"{r['file']}:{r['line']} -> {r['target']} | {r['content'][:80]}")

