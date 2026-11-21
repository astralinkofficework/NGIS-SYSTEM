from playwright.sync_api import sync_playwright

test_urls = [
    'http://127.0.0.1:3000/pages/admin/admin-departments.html',
    'http://127.0.0.1:3000/pages/principal/principal-classes.html',
    'http://127.0.0.1:3000/pages/teacher/teacher-reports.html',
    'http://127.0.0.1:3000/pages/student/student.html',
    'http://127.0.0.1:3000/pages/student/student-grades.html'
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1366, 'height': 768})
    for u in test_urls:
        page.goto(u, wait_until='networkidle')
        page_name = u.split('/')[-1]
        h1s = page.locator('h1').all()
        for i, h1 in enumerate(h1s):
            box = h1.bounding_box()
            txt = h1.inner_text().strip().replace('\n', ' ')
            if box and box['width'] > 0 and box['height'] > 0:
                print(f'{page_name} [h1-{i}]: x={box["x"]:.1f}, y={box["y"]:.1f}, w={box["width"]:.1f} | "{txt}"')
    browser.close()
