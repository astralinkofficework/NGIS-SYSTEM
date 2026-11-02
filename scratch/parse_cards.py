from bs4 import BeautifulSoup
import os

pages = [
    'pages/student/student.html',
    'pages/teacher/teacher.html',
    'pages/principal/principal.html',
    'pages/admin/admin.html'
]

for p in pages:
    with open(p, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # find all elements that look like cards
    cards = soup.select('.card, .portal-card, .stat-card, .module-card, .dept-card, .hub-card, .ws-card, .ov-profile, .ov-upcoming, .ov-deadlines, .ov-inner-panel, .ql-card, .quick, .ann-card, [class*="card"]')
    print(f'=== {p} ===: {len(cards)} card elements found')
    for c in cards[:5]:
        classes = ' '.join(c.get('class', []))
        tag = c.name
        print(f'  <{tag} class="{classes}">{c.get("id", "")}</{tag}>')

