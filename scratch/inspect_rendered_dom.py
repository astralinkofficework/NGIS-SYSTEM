from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    
    # Check elements inside main
    main_html = page.evaluate("() => document.querySelector('main').outerHTML")
    print('MAIN length:', len(main_html))
    
    # Check if heroBanner rendered
    hero_html = page.evaluate("() => document.getElementById('heroBanner')?.innerHTML")
    print('HeroBanner rendered:', bool(hero_html and hero_html.strip()))
    
    # Check if there is an h1
    h1 = page.evaluate("() => document.querySelector('h1')?.innerText")
    print('H1:', h1)
    
    # Check top text/structure of ks-root
    ks_root_children = page.evaluate("() => Array.from(document.getElementById('ks-root')?.children || []).map(c => ({ tag: c.tagName, cls: c.className }))")
    print('ks-root children:', ks_root_children)
    
    browser.close()

