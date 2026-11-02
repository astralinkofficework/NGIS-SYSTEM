from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-submissions.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='scratch/teacher_submissions_title_updated.png')
    browser.close()
    print('Screenshot taken successfully!')

