from playwright.sync_api import sync_playwright
import os

pages_to_test = [
    'student.html',
    'student-attendance.html',
    'student-grades.html',
    'student-assignments.html',
    'student-exams.html',
    'student-timetable.html'
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for pg in pages_to_test:
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'http://127.0.0.1:3000/pages/student/{pg}')
        page.wait_for_timeout(800)
        out_name = f'scratch/{pg.replace(".html", "")}.png'
        page.screenshot(path=out_name, full_page=False)
        print(f"Captured {pg} -> {out_name}")
    browser.close()

