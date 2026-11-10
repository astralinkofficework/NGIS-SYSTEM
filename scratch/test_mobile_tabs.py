from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:3000/pages/admin/admin-school-information.html', wait_until='networkidle')
    page.wait_for_timeout(1000)

    # List of tabs
    tabs = [
        'profile', 'academic-years', 'campuses', 'school-days',
        'bell-schedule', 'academic-calendar', 'departments-grades',
        'timetable-rules', 'academic-policies', 'permissions-access', 'change-history'
    ]

    for tab_id in tabs[:4]:
        page.evaluate(f"window.SCHOOL_INFO.switchSection('{tab_id}')")
        page.wait_for_timeout(500)
        page.screenshot(path=f'scratch/mobile_tab_{tab_id}.png')
        print(f'Captured mobile tab {tab_id}')

    browser.close()

