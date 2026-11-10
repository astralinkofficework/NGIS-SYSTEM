import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

modal_instances = []
for p in html_files:
    if 'scratch' in p or 'test' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Check for modals: role="dialog", class="*modal*", id="*modal*", id="*Modal*"
    matches = re.findall(r'(<(?:div|dialog|section)[^>]*(?:role=["\']dialog["\']|id=["\'][^"\']*[Mm]odal[^"\']*["\']|class=["\'][^"\']*(?:modal|dialog|popup)[^"\']*["\'])[^>]*>)', c)
    if matches:
        modal_instances.append((p, len(matches), matches))

print(f'{len(modal_instances)} files have modals/dialogs:')
for p, count, m in modal_instances:
    print(f'=== {p} ({count} modals) ===')
    for tag in m[:3]:
        print('  ', tag[:120])

