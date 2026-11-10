"""Quantify data-ngis-icon slots vs remaining raw icon-font actions per page."""
import glob, re, collections

pages = sorted(glob.glob('pages/**/*.html', recursive=True)) + ['index.html']

slot_re = re.compile(r'data-ngis-icon="([a-zA-Z0-9_-]+)"')
# material glyph still inside an action-ish button (not hydrated slot)
mat_in_btn = re.compile(r'<(?:button|a)\b[^>]*class="[^"]*(?:action-icon|icon-btn|btn-|kebab|row-action)[^"]*"[^>]*>(?:(?!</(?:button|a)>).)*?<span[^>]*class="[^"]*material-symbols[^"]*"[^>]*>\s*([a-z_0-9-]+)\s*<', re.I | re.S)
emoji_re = re.compile(r'[👁✏🗑✕✓✖⋮⋯×]')

tot_slots = collections.Counter()
pages_with_slots = 0
pages_missing_engine = []
remaining_mat_actions = 0
remaining_emoji = 0
per_page = []

for p in pages:
    s = open(p, encoding='utf-8').read()
    slots = slot_re.findall(s)
    for n in slots:
        tot_slots[n] += 1
    if slots:
        pages_with_slots += 1
    has_engine = ('action-icons.js' in s)
    if not has_engine:
        pages_missing_engine.append(p)
    mat_act = mat_in_btn.findall(s)
    remaining_mat_actions += len(mat_act)
    # emoji inside action buttons only
    e = len(emoji_re.findall(s))
    remaining_emoji += e
    per_page.append((p, len(slots), len(mat_act), e, has_engine))

print('Pages total:', len(pages))
print('Pages with data-ngis-icon slots:', pages_with_slots)
print('Pages missing engine wire:', len(pages_missing_engine))
print('Total data-ngis-icon slots:', sum(tot_slots.values()))
print('Remaining material glyphs inside action btns:', remaining_mat_actions)
print('Action-ish emoji chars total (loose):', remaining_emoji)
print()
print('=== Top slot icon names ===')
for k, v in tot_slots.most_common(40):
    print('%4d %s' % (v, k))
print()
print('=== Per page (slots / matActions / emoji / hasEngine) — only pages with slots or issues ===')
for p, sl, ma, em, he in per_page:
    if sl or ma or em:
        print('%-46s slots=%-4d mat=%-3d emo=%-3d eng=%s' % (p, sl, ma, em, he))
