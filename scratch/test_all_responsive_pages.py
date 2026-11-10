from playwright.sync_api import sync_playwright

pages_to_test = [
    'http://127.0.0.1:3000/pages/principal/principal-departments.html',
    'http://127.0.0.1:3000/pages/principal/principal-classes.html',
    'http://127.0.0.1:3000/pages/admin/admin-departments.html',
    'http://127.0.0.1:3000/pages/admin/admin-department-detail.html',
    'http://127.0.0.1:3000/pages/teacher/teacher-reports.html'
]

viewports = [
    (360, 740),
    (375, 667),
    (390, 844),
    (768, 1024),
    (820, 1180),
    (1024, 768),
    (1280, 800)
]

all_passed = True

with sync_playwright() as p:
    browser = p.chromium.launch()
    for page_url in pages_to_test:
        page_name = page_url.split('/')[-1]
        print(f"\nTesting {page_name}...")
        for w, h in viewports:
            page = browser.new_page(viewport={'width': w, 'height': h})
            page.goto(page_url)
            page.wait_for_timeout(400)
            
            scroll_w = page.evaluate('document.documentElement.scrollWidth')
            client_w = page.evaluate('document.documentElement.clientWidth')
            overflow = scroll_w > client_w
            
            if overflow:
                all_passed = False
                print(f"  FAILED @ {w}px: scrollW={scroll_w} > clientW={client_w}")
            else:
                print(f"  OK @ {w}px (scrollW={scroll_w})")
            page.close()
    browser.close()

if all_passed:
    print("\nALL RESPONSIVE AUDITS PASSED WITH ZERO HORIZONTAL OVERFLOW!")
else:
    print("\nSOME AUDITS FAILED.")

