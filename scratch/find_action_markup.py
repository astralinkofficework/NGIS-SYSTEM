"""Find real action-button markup in tables across pages."""
import glob, re

pages = sorted(glob.glob('pages/**/*.html', recursive=True))

# button/anchor that contains an action glyph OR action-ish class OR aria-label
btn_re = re.compile(
    r'<button\b[^>]*>(?:(?!</button>).)*?(?:visibility|edit|delete|more_vert|download|upload|check_circle|close|search|filter_list|print|content_copy|expand_more|north_east|Done|trash|eye|pencil|👁|✏|🗑|✕|×|✓|&#8942;|&#8226;|&#8230;)(?:(?!</button>).)*?</button>',
    re.I | re.S)

# also grab the td/th "Actions" cell contents
cell_re = re.compile(r'<td\b[^>]*class="[^"]*(?:action|table-action)[^"]*"[^>]*>.*?</td>', re.I | re.S)

shown = 0
for p in pages:
    s = open(p, encoding='utf-8').read()
    hits = btn_re.findall(s)
    cells = cell_re.findall(s)
    if not hits and not cells:
        continue
    print('\n#### %s  (buttons=%d, action-cells=%d)' % (p, len(hits), len(cells)))
    for h in hits[:3]:
        print('  BTN:', re.sub(r'\s+', ' ', h)[:260])
    for c in cells[:2]:
        print('  CELL:', re.sub(r'\s+', ' ', c)[:300])
    shown += 1
    if shown >= 18:
        break
