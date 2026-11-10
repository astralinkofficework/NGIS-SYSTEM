import re

FILES = [
    'pages/principal/principal-assignments.html',
    'pages/principal/principal-attendance.html',
    'pages/principal/principal-departments.html',
    'pages/principal/principal-lost-found.html',
    'pages/principal/principal-services.html',
    'pages/principal/principal-timetables.html',
]

PAT = re.compile(
    r'window\.PAGE\s*=\s*\{.*?\};\s*\n+\s*window\.HERO_CONFIG\s*=\s*\{.*?\};',
    re.S,
)

for f in FILES:
    src = open(f, encoding='utf-8').read()
    m = PAT.search(src)
    if not m:
        print(f, '=> NO adjacent PAGE/HERO_CONFIG block found!')
        continue
    block = m.group(0)
    if '<!-- Shared UI & App Scripts -->' not in src:
        print(f, '=> MARKER NOT FOUND, skipping file unchanged')
        continue
    # remove from the big inline script
    src = src[:m.start()] + src[m.end():]
    # drop leftover blank lines right after removal point
    src = src.replace('<!-- Shared UI & App Scripts -->',
                      '<script>\n' + block + '\n</script>\n<!-- Shared UI & App Scripts -->', 1)
    open(f, 'w', encoding='utf-8').write(src)
    print(f, '=> moved config before hero.js include (%d chars)' % len(block))
