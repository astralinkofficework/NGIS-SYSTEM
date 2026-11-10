from playwright.sync_api import sync_playwright

portals = [
    ('Principal', 'http://127.0.0.1:3000/pages/principal/principal.html'),
    ('Admin', 'http://127.0.0.1:3000/pages/admin/admin.html'),
    ('Teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
    ('Student', 'http://127.0.0.1:3000/pages/student/student.html'),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, url in portals:
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.goto(url)
        page.wait_for_selector('#sidebar')
        
        chevrons = page.evaluate("""() => {
            const els = Array.from(document.querySelectorAll('#sidebar *'));
            return els.filter(e => {
                const txt = (e.innerText || '').trim();
                const cls = typeof e.className === 'string' ? e.className : (e.className.baseVal || '');
                const isArrow = txt === 'expand_more' || txt === 'chevron_right' || txt === 'keyboard_arrow_down' || 
                                txt === 'arrow_forward' || txt === 'arrow_right' || cls.includes('chevron') || cls.includes('arrow');
                if (!isArrow) return false;
                // Check if element is visible
                const style = window.getComputedStyle(e);
                return style && style.display !== 'none' && style.visibility !== 'hidden';
            }).map(e => ({
                tag: e.tagName,
                cls: typeof e.className === 'string' ? e.className : (e.className.baseVal || ''),
                text: (e.innerText || '').trim(),
                parentCls: e.parentElement ? (typeof e.parentElement.className === 'string' ? e.parentElement.className : '') : ''
            }));
        }""")
        print(f"{name} sidebar visible arrows/chevrons count: {len(chevrons)}")
        for c in chevrons:
            print("  ->", c)
            
        page.screenshot(path=f"scratch/sidebar_{name.lower()}_clean.png")
        page.close()
        
    browser.close()
