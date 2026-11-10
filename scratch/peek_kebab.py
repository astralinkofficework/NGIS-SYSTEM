import re
s = open('pages/admin/admin.html', encoding='utf-8').read()
# find the more trigger and surrounding button + any following menu
for m in re.finditer(r'<button[^>]*>(?:(?!</button>).){0,120}?data-ngis-icon="more".{0,40}?</button>', s, re.S):
    print(re.sub(r'\s+', ' ', m.group(0))[:300])
    print('---')
# find kebab handler names
print('\nhandlers mentioning kebab/more/menu:')
for m in re.finditer(r'(onclick|data-action)="([^"]*(?:kebab|more|RowMenu|rowMenu|openMenu|toggleMenu|dropdown)[^"]*)"', s, re.I):
    print('  ', m.group(0)[:120])
# how many more-triggers and are they inside action-dropdown?
print('\ntotal data-ngis-icon=more:', s.count('data-ngis-icon="more"'))
print('action-dropdown blocks:', s.count('action-dropdown'))
