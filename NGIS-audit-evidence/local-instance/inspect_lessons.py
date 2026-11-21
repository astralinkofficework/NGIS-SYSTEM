from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    errors = []
    page.on('console', lambda msg: errors.append(f'{msg.type}: {msg.text}') if msg.type in ['error', 'warning'] else None)
    page.on('pageerror', lambda err: errors.append(f'pageerror: {err}'))
    
    url = 'http://127.0.0.1:3000/pages/shared/lessons.html?dept=english&portal=student'
    page.goto(url)
    page.wait_for_timeout(1500)
    
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/6db479c3-37eb-42ef-ad87-bb4ce393a277/lessons_desktop_before.png', full_page=True)
    
    page.set_viewport_size({'width': 768, 'height': 1024})
    page.wait_for_timeout(400)
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/6db479c3-37eb-42ef-ad87-bb4ce393a277/lessons_tablet_before.png')
    
    page.set_viewport_size({'width': 375, 'height': 812})
    page.wait_for_timeout(400)
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/6db479c3-37eb-42ef-ad87-bb4ce393a277/lessons_mobile_before.png')
    
    info = page.evaluate('''() => {
        const modals = Array.from(document.querySelectorAll('.oak-preview-modal-overlay, .oak-modal-overlay, [class*="modal" i]')).map(m => {
            const cs = window.getComputedStyle(m);
            return { id: m.id, className: m.className, display: cs.display, visibility: cs.visibility, opacity: cs.opacity };
        });
        const hb = document.querySelector('[data-action="toggle-sidebar"], .hamburger-btn, .mobile-hamburger-btn');
        const heroTitle = document.querySelector('#heroBanner h1, .dash-hero-title, .hero-title, .portal-title');
        const subjName = document.querySelector('#curSubjName');
        const cardCount = document.querySelectorAll('.oak-card, .oak-grid > *').length;
        return {
            title: document.title,
            heroTitle: heroTitle ? heroTitle.innerText : 'None',
            subjName: subjName ? subjName.innerText : 'None',
            cardCount: cardCount,
            hasHamburger: !!hb,
            visibleModals: modals.filter(m => m.display !== 'none' && m.visibility !== 'hidden')
        };
    }''')
    print('Page Info:', info)
    print('Console Errors:', errors[:10])
    browser.close()
