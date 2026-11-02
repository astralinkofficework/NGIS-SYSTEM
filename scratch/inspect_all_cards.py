import re, sys

def safe_print(text):
    sys.stdout.buffer.write((str(text) + '\n').encode('utf-8', errors='replace'))

# Let's inspect pages/admin/admin-departments.html
with open('pages/admin/admin-departments.html', 'r', encoding='utf-8') as f:
    c = f.read()

matches = re.findall(r'<article class="dept-card[^"]*"[^>]*>[\s\S]*?</article>', c)
if matches:
    safe_print('Found dept-card:')
    safe_print(matches[0][:400])

# Let's inspect student-clubs.html
with open('pages/student/student-clubs.html', 'r', encoding='utf-8') as f:
    c = f.read()
matches = re.findall(r'<[^>]+class="[^"]*club-card[^"]*"[^>]*>[\s\S]*?</[^>]+>', c)
if matches:
    safe_print('Found club-card:')
    safe_print(matches[0][:400])

# Let's inspect student-calendar.html
with open('pages/student/student-calendar.html', 'r', encoding='utf-8') as f:
    c = f.read()
matches = re.findall(r'<[^>]+class="[^"]*cal-card[^"]*"[^>]*>[\s\S]*?</[^>]+>', c)
if matches:
    safe_print('Found cal-card:')
    safe_print(matches[0][:400])
