from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    errors = []
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    page.goto('http://127.0.0.1:3000/pages/admin/admin-school-information.html', wait_until='networkidle')
    page.wait_for_timeout(1000)

    has_persona = page.locator('text="Persona:"').count()
    has_subtitle = page.locator('.si-subtitle').count()
    has_h1 = page.locator('h1.si-title').count()

    print('Persona count in DOM:', has_persona)
    print('si-subtitle count in DOM:', has_subtitle)
    print('h1.si-title count in DOM:', has_h1)
    print('Console errors:', len(errors))
    for err in errors[:5]:
        print(' -', err)

    page.screenshot(path='scratch/verify_school_info_clean.png')
    print('Screenshot saved to scratch/verify_school_info_clean.png')
    browser.close()

