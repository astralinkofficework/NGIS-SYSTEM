import json
from collections import Counter

with open('tools/deep_modal_results.json', 'r', encoding='utf-8') as f:
    modals = json.load(f)

print(f"Total modals analyzed: {len(modals)}")

# Group by inner class patterns / widths
widths = []
for m in modals:
    ic = m['inner_classes']
    w_match = [w for w in ic.split() if w.startswith('max-w-') or w.startswith('w-')]
    widths.append(' '.join(w_match) if w_match else 'no-width-class')

print("\nInner Box Width Distribution:")
for w, c in Counter(widths).most_common(15):
    print(f"  {w:30} : {c}")

print(f"\nModals with internal tabs: {sum(1 for m in modals if m['has_tabs'])}")
for m in modals:
    if m['has_tabs']:
        print(f"  - {m['page'].split('/')[-1]}: {m['modal_id']}")
