import os
from playwright.sync_api import sync_playwright

student_pages = [
    'student.html',
    'student-grades.html',
    'student-attendance.html',
    'student-assignments.html',
    'student-exams.html',
    'student-timetable.html',
    'student-calendar.html',
    'student-announcements.html',
    'student-services.html',
    'student-notifications.html',
    'student-profile.html',
    'student-lost-found.html'
]

out_dir = r'C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536\student_qa'
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    # Desktop 1366
    page = browser.new_page(viewport={'width': 1366, 'height': 768})
    for sp in student_pages:
        try:
            url = f'http://127.0.0.1:3000/pages/student/{sp}'
            page.goto(url, wait_until='load', timeout=10000)
            page.wait_for_timeout(400)
            base = sp.replace('.html', '')
            page.screenshot(path=os.path.join(out_dir, f'desktop_{base}.png'))
            print(f'Captured desktop {base}')
        except Exception as e:
            print(f'Error desktop {sp}: {e}')

    # Mobile 375
    page_m = browser.new_page(viewport={'width': 375, 'height': 812})
    for sp in student_pages:
        try:
            url = f'http://127.0.0.1:3000/pages/student/{sp}'
            page_m.goto(url, wait_until='load', timeout=10000)
            page_m.wait_for_timeout(400)
            base = sp.replace('.html', '')
            page_m.screenshot(path=os.path.join(out_dir, f'mobile_{base}.png'))
            print(f'Captured mobile {base}')
        except Exception as e:
            print(f'Error mobile {sp}: {e}')

    browser.close()

print('Finished capturing all student QA screenshots!')
