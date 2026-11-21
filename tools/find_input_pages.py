import glob, re

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
email_pages = []
pwd_pages = []
phone_pages = []
otp_pages = []

for f in html_files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    inps = re.findall(r'<input\b[^>]*>', c, re.IGNORECASE)
    for inp in inps:
        low = inp.lower()
        if 'type="email"' in low or 'type=\'email\'' in low or ('email' in low and 'type=' not in low):
            email_pages.append((f, inp))
        if 'type="password"' in low or 'type=\'password\'' in low:
            pwd_pages.append((f, inp))
        if 'type="tel"' in low or 'phone' in low:
            phone_pages.append((f, inp))
        if 'otp' in low or 'one-time' in low or 'code' in low:
            otp_pages.append((f, inp))

print(f'Email inputs found: {len(email_pages)}')
for f, inp in email_pages:
    print(f'  {f}: {inp}')

print(f'\nPassword inputs found: {len(pwd_pages)}')
for f, inp in pwd_pages:
    print(f'  {f}: {inp}')

print(f'\nPhone inputs found: {len(phone_pages)}')
for f, inp in phone_pages:
    print(f'  {f}: {inp}')

print(f'\nOTP inputs found: {len(otp_pages)}')
for f, inp in otp_pages:
    print(f'  {f}: {inp}')
