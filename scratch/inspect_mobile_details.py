from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    
    # check mobile visibility and overflow
    mobile_info = page.evaluate("""() => {
        const docWidth = document.documentElement.scrollWidth;
        const winWidth = window.innerWidth;
        const hasHorizontalScroll = docWidth > winWidth;
        
        const hamburger = document.querySelector('[data-action="toggle-sidebar"]');
        const hamburgerVisible = hamburger ? (hamburger.offsetWidth > 0 && hamburger.offsetHeight > 0) : false;
        
        const h1 = document.querySelector('h1');
        
        // Find visible elements at the top
        const elements = [];
        document.querySelectorAll('body *').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top >= 0 && rect.top < 150 && rect.height > 0 && el.innerText && el.children.length === 0) {
                elements.push({ text: el.innerText.trim(), tag: el.tagName, top: Math.round(rect.top) });
            }
        });
        
        return {
            hasHorizontalScroll,
            docWidth,
            winWidth,
            hamburgerExists: !!hamburger,
            hamburgerVisible,
            hasH1: !!h1,
            topTextSnippets: elements.slice(0, 10)
        };
    }""")
    print('Mobile info (390x844):')
    print(mobile_info)
    browser.close()

