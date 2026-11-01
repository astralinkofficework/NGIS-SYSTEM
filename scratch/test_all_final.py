from playwright.sync_api import sync_playwright
import os

pages_to_test = [
    'student.html',
    'student-attendance.html',
    'student-grades.html',
    'student-assignments.html',
    'student-exams.html',
    'student-timetable.html',
    'student-calendar.html',
    'student-services.html',
    'student-id.html',
    'student-clubs.html',
    'student-lost-found.html',
    'student-notifications.html',
    'student-profile.html',
    'student-announcements.html'
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for pg in pages_to_test:
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(f'http://127.0.0.1:3000/pages/student/{pg}')
        page.wait_for_timeout(800)
        out_name = f'scratch/final_{pg.replace(".html", "")}.png'
        page.screenshot(path=out_name, full_page=False)
        print(f"Captured {pg} -> {out_name}")
    
    # Test drawer open on student-timetable.html
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/student/student-timetable.html')
    page.wait_for_timeout(500)
    page.click('#htbHamburger')
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/final_drawer_open.png', full_page=False)
    print("Captured drawer open on student-timetable.html -> scratch/final_drawer_open.png")

    # Test mobile view (390px) on student.html and student-grades.html
    page_mobile = browser.new_page(viewport={'width': 390, 'height': 844})
    page_mobile.goto('http://127.0.0.1:3000/pages/student/student.html')
    page_mobile.wait_for_timeout(500)
    page_mobile.screenshot(path='scratch/final_mobile_student.png', full_page=False)
    print("Captured mobile student.html -> scratch/final_mobile_student.png")

    browser.close()
print("All screenshots captured successfully!")

