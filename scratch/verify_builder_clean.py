from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.goto('http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html', wait_until='networkidle')
    page.wait_for_timeout(1000)

    has_btn_auto = page.locator('#btnAutoGenerate').count()
    has_conflicts = page.locator('.flex.items-center.gap-2 [data-act="conflicts"]').count()

    print('btnAutoGenerate count in DOM:', has_btn_auto)
    print('toolbar conflicts button count:', has_conflicts)
    print('Console errors:', len(errors))
    for err in errors[:5]:
        print(' -', err)

    page.screenshot(path='scratch/verify_builder_clean.png')
    print('Screenshot saved to scratch/verify_builder_clean.png')
    browser.close()
