import json

data = json.load(open('tools/comprehensive_page_audit.json', encoding='utf-8'))

print("=== PAGES WITH CONSOLE ERRORS ===")
for r in data:
    if r['console_errors']:
        print(r['file'], "->", r['console_errors'])

print("\n=== PORTAL PAGES MISSING HAMBURGER ===")
for r in data:
    if not r['hamburger_present_mobile'] and r['portal'] in ['admin', 'teacher', 'student', 'principal', 'shared']:
        print(r['file'], "-> portal:", r['portal'])

print("\n=== PAGES WITH ENCODING OR SPECIAL CHARACTERS IN TITLE ===")
for r in data:
    if '' in r['title'] or '?' in r['title'] and '?' not in r['file']:
        print(r['file'], "-> title:", r['title'])
