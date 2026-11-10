import re, subprocess, os, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'pages/admin/admin-lifecycle.html'
src = open(path, encoding='utf-8', errors='replace').read()
# match inline scripts (those without src=)
for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', src, re.S | re.I):
    body = m.group(1)
    if 'type="application/json"' in m.group(0) or 'application/ld' in m.group(0):
        continue
    start_line = src[:m.start()].count('\n') + 1
    tmp = 'scratch/_inline_%d.js' % start_line
    open(tmp, 'w', encoding='utf-8').write(body)
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    if r.returncode != 0:
        print('SYNTAX ERROR in inline script starting at line', start_line)
        print(r.stderr[:800])
        os.remove(tmp)
    else:
        print('ok  line', start_line, '(%d chars)' % len(body.strip()))
        os.remove(tmp)
