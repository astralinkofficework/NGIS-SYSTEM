"""Audit icon usage across all portal pages.
Categorises: phosphor icons, material symbols, emoji/unicode action chars, inline SVGs,
and table action-column markup patterns.
"""
import glob, re, json, collections

PAGES = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']

EMOJI_ACTION = {
    '\U0001F441': 'eye', '\U0001F58B': 'pin', '\U0001F4DD': 'memo', '\U0001F5D1': 'trash',
    '\u270E': 'pencil', '\u270F': 'pencil', '\u2714': 'check', '\u2717': 'cross',
    '\u2716': 'cross', '\u25CF': 'dot', '\u22EE': 'vert-ellipsis', '\u22EF': 'horiz-ellipsis',
    '\u2022': 'bullet', '\u00D7': 'multiply-x', '\u2715': 'close-x', '\u21BA': 'back',
    '\u25B8': 'tri-right', '\u25BE': 'tri-down', '\u25C0': 'tri-left', '\u25B6': 'tri-right2',
    '\u21BB': 'refresh', '\u23F3': 'hourglass', '\u2699': 'gear', '\u2691': 'flag',
    '\u2764': 'heart', '\u2B50': 'star', '\u2605': 'star', '\u2708': 'plane',
    '\u2709': 'envelope', '\u2702': 'scissors', '\u2611': 'checkbox', '\u2610': 'checkbox-empty',
    '\u2192': 'arrow-right', '\u2190': 'arrow-left', '\u2194': 'arrow-lr',
    '\u2913': 'download', '\u2912': 'upload', '\u2922': 'ne-arrow',
}
# More emoji ranges commonly used as action icons (faces, objects)
EMOJI_RANGES = [(0x1F300, 0x1FAFF), (0x2600, 0x27BF), (0x2190, 0x21FF), (0x2B00, 0x2BFF)]

def is_emoji_cp(cp):
    return any(lo <= cp <= hi for lo, hi in EMOJI_RANGES)

report = {}
total = collections.Counter()

for page in PAGES:
    try:
        src = open(page, encoding='utf-8').read()
    except Exception as e:
        report[page] = {'error': str(e)}
        continue
    d = {}
    d['phosphor'] = len(re.findall(r'class="[^"]*\bph[- ]', src))
    d['material'] = len(re.findall(r'material-symbols(?:-outlined)?', src))
    d['fontawesome'] = len(re.findall(r'\bfa-(?:solid|regular|brands)|fa-[a-z]', src))
    d['inline_svg'] = len(re.findall(r'<svg\b', src))
    d['table-action-td'] = len(re.findall(r'<td[^>]*>', src)) and len(re.findall(r'Actions', src))
    d['action_btn_heuristics'] = len(re.findall(r'(?:btn-action|action-btn|table-actions|action-group|icon-btn)', src))
    # emoji/unicode chars used in text nodes
    uni = collections.Counter()
    for ch in src:
        if ch in EMOJI_ACTION:
            uni[EMOJI_ACTION[ch]] += 1
        elif is_emoji_cp(ord(ch)) and ord(ch) not in EMOJI_ACTION:
            uni['emoji:%04X' % ord(ch)] += 1
    d['unicode_action'] = dict(uni)
    d['confirm_alerts'] = len(re.findall(r'\bconfirm\(', src))
    d['more_menus'] = len(re.findall(r'more-options|more_menu|moreMenu|kebab|kebab-btn|dropdown-toggle|dropdownToggle', src, re.I))
    report[page] = d
    for k in ('phosphor', 'material', 'fontawesome', 'inline_svg', 'action_btn_heuristics', 'more_menus'):
        total[k] += d[k]
    for name, n in uni.items():
        total['unicode:' + name] += n

print(json.dumps({'totals': dict(total)}, indent=2))
print()
# Per-page detail for pages with unicode/emoji or material usage
for page, d in report.items():
    if 'error' in d:
        print(page, 'ERROR', d['error']); continue
    interesting = d['unicode_action'] or d['material'] or d['fontawesome']
    if interesting:
        print('%-48s ph=%-4d mat=%-4d fa=%-3d svg=%-3d uni=%s' % (
            page, d['phosphor'], d['material'], d['fontawesome'], d['inline_svg'],
            json.dumps(d['unicode_action'])))
