"""Extract inline <script> blocks from a page and node --check each to find the parse error."""
import re, subprocess, sys, tempfile, os

path = sys.argv[1] if len(sys.argv) > 1 else 'pages/shared/exams.html'
s = open(path, encoding='utf-8').read()
blocks = re.findall(r'<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>', s, re.S | re.I)
print('inline script blocks:', len(blocks))
tmp = tempfile.mkdtemp()
for i, b in enumerate(blocks):
    if not b.strip():
        continue
    f = os.path.join(tmp, 'blk%d.js' % i)
    open(f, 'w', encoding='utf-8').write(b)
    # estimate starting line number in the original file
    start_line = s[:s.find(b)].count('\n') + 1
    r = subprocess.run(['node', '--check', f], capture_output=True, text=True)
    if r.returncode != 0:
        print('\n=== BLOCK %d HAS ERROR (starts near file line %d) ===' % (i, start_line))
        print(r.stderr[:800])
        # print the offending lines
        lines = b.splitlines()
        m = re.search(r'blk%d\.js:(\d+)' % i, r.stderr)
        if m:
            ln = int(m.group(1))
            for k in range(max(0, ln-3), min(len(lines), ln+2)):
                print('   %4d| %s' % (k+1, lines[k][:160]))
print('done')
