"""Fix injection position: relocate the engine block to the FIRST </head>.

The earlier injector used rfind('</head>'), which on pages that embed a full
printable HTML document inside a JS string (exams/transcript/lifecycle) landed
inside that string and broke it. The real document head always closes before any
body content, so the FIRST </head> is the correct anchor for every page.

Idempotent: strips any existing injected block first, then re-inserts once.
"""
import glob, re

MARK = '<!-- NGIS global action-icon engine -->'
STRIP = re.compile(
    r'\n?' + re.escape(MARK) +
    r'\s*<link[^>]*assets/css/action-icons\.css">\s*'
    r'<script[^>]*assets/js/action-icons\.js"[^>]*></script>\s*',
    re.I)

pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']
multi_head = []
fixed = 0
for p in pages:
    s = open(p, encoding='utf-8').read()
    s = STRIP.sub('\n', s)                       # remove any prior injection everywhere
    heads = [m.start() for m in re.finditer(r'</head>', s, re.I)]
    if len(heads) > 1:
        multi_head.append((p, len(heads)))
    depth = p.replace('\\', '/').count('/')
    prefix = '../' * depth if depth else './'
    block = (
        '%s\n<link rel="stylesheet" href="%sassets/css/action-icons.css">\n'
        '<script src="%sassets/js/action-icons.js" defer></script>\n'
        % (MARK, prefix, prefix)
    )
    idx = s.lower().find('</head>')
    if idx == -1:
        print('!! no </head> in', p); continue
    s = s[:idx] + block + s[idx:]
    open(p, 'w', encoding='utf-8').write(s)
    fixed += 1

print('Re-injected %d pages at first </head>.' % fixed)
print('Pages with multiple </head> (print templates):')
for p, n in multi_head:
    print('   %-46s %d' % (p, n))
