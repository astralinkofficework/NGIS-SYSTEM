import glob, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

for f in ['pages/teacher/teacher-classes.html', 'pages/teacher/teacher-attendance.html', 'pages/teacher/teacher-reports.html', 'pages/teacher/teacher-services.html', 'pages/teacher/teacher-lost-found.html']:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fl:
        c = fl.read()
    m = re.search(r'<header[^>]*>[\s\S]*?</header>|<section class="[^"]*(?:header|masthead|mb-5)[^"]*"[^>]*>[\s\S]*?</section>', c)
    if m:
        headings = re.findall(r'<h[12][^>]*>[\s\S]*?</h[12]>', m.group(0))
        safe_print(f'{f}: {headings}')

