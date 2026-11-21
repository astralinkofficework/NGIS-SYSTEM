import json
from collections import defaultdict

with open('tools/component_scan_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== MODALS INVENTORY ===')
modal_id_to_pages = defaultdict(list)
for page, info in data['modals'].items():
    for mid in info['ids']:
        modal_id_to_pages[mid].append(page)

for mid, pgs in sorted(modal_id_to_pages.items()):
    print(f"Modal: {mid:35} | Pages count: {len(pgs)} ({', '.join([p.split('/')[-1] for p in pgs[:3]])})")

print('\n=== DRAWERS INVENTORY ===')
for page, drawers in data['drawers'].items():
    print(f"{page.split('/')[-1]}: {drawers}")

print('\n=== TABS INVENTORY ===')
for page, tabinfo in list(data['tabs'].items())[:15]:
    print(f"{page.split('/')[-1]}: count={tabinfo['count']}, ids={tabinfo['ids'][:3]}")
