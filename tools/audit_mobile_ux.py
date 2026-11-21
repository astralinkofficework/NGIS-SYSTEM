import glob, os, re
from collections import Counter

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
print(f'Total HTML pages: {len(html_files)}')

css_links = Counter()
js_scripts = Counter()

# Audit checks:
# 1. Inputs without font-size >= 16px protection or inputmode
# 2. Tap highlight settings
# 3. Stuck hover (@media (hover: hover))
# 4. overscroll-behavior
# 5. touch-action: manipulation
# 6. enterkeyhint
# 7. scroll snapping
# 8. email inputs without autocapitalize/spellcheck/autocomplete
# 9. OTP autocomplete
# 10. Forms / inputs summary

input_types = Counter()
missing_email_attrs = 0
total_email_inputs = 0
otp_inputs = 0
search_inputs = 0
phone_inputs = 0

for f in html_files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    # CSS
    hrefs = re.findall(r'<link[^>]+rel=[\"\']stylesheet[\"\'][^>]+href=[\"\']([^\"\']+)[\"\']', c)
    for h in hrefs:
        clean = h.split('?')[0].replace('../../', '').replace('../', '')
        css_links[clean] += 1
        
    # Scripts
    scripts = re.findall(r'<script[^>]+src=[\"\']([^\"\']+)[\"\']', c)
    for s in scripts:
        clean = s.split('?')[0].replace('../../', '').replace('../', '')
        js_scripts[clean] += 1

    # Inputs
    inputs = re.findall(r'<input\b[^>]*>', c, re.IGNORECASE)
    for inp in inputs:
        t_match = re.search(r'type=[\"\']([^\"\']+)[\"\']', inp, re.IGNORECASE)
        itype = t_match.group(1).lower() if t_match else 'text'
        input_types[itype] += 1
        
        if itype == 'email':
            total_email_inputs += 1
            if 'autocapitalize' not in inp.lower() or 'spellcheck' not in inp.lower():
                missing_email_attrs += 1
        elif itype == 'search' or 'search' in inp.lower():
            search_inputs += 1
        elif itype == 'tel' or 'phone' in inp.lower():
            phone_inputs += 1
        elif 'otp' in inp.lower() or 'code' in inp.lower():
            otp_inputs += 1

print('\nTop CSS inclusions:')
for href, count in css_links.most_common(12):
    print(f'  {count}/{len(html_files)}: {href}')

print('\nTop JS inclusions:')
for s, count in js_scripts.most_common(12):
    print(f'  {count}/{len(html_files)}: {s}')

print('\nInput types found in static HTML:')
for itype, count in input_types.most_common(10):
    print(f'  {itype}: {count}')

print(f'\nEmail inputs: {total_email_inputs} (missing autocapitalize/spellcheck: {missing_email_attrs})')
print(f'Search inputs: {search_inputs}')
print(f'Phone inputs: {phone_inputs}')
print(f'OTP/Code inputs: {otp_inputs}')
