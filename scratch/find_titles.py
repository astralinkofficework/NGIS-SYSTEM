import glob, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

for f in sorted(glob.glob('pages/teacher/*.html')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fl:
        c = fl.read()
    # Search for main page title / heading
    m = re.findall(r'<h[12][^>]*>[\s\S]*?</h[12]>', c)
    if m:
        safe_print(f'=== {f} ===')
        for h in m[:2]:
            safe_print('  ' + h.strip().replace('\n', ' '))

