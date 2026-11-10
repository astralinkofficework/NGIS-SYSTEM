from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    pages_to_check = [
        'http://127.0.0.1:3000/pages/principal/principal-school-information.html',
        'http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html',
        'http://127.0.0.1:3000/pages/principal/principal-classes.html',
        'http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html'
    ]
    
    for url in pages_to_check:
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.goto(url)
        page.wait_for_load_state('networkidle')
        name = url.split('/')[-1]
        
        info = page.evaluate("""() => {
            const h1 = document.querySelector('h1')?.innerText;
            const titleEl = document.querySelector('.page-header, .page-title, h1, .ks-head, .ks-top-bar, .hero-title-area, .si-header');
            const pageDiv = document.querySelector('.page');
            const main = document.querySelector('main');
            
            // first 3 non-empty text blocks below header.hero
            const hero = document.querySelector('header.hero');
            let sibling = hero ? hero.nextElementSibling : main?.firstElementChild;
            const topBlocks = [];
            while (sibling && topBlocks.length < 3) {
                if (sibling.innerText && sibling.innerText.trim()) {
                    topBlocks.push({
                        tag: sibling.tagName,
                        cls: sibling.className,
                        text: sibling.innerText.trim().slice(0, 150).replace(/\\n/g, ' ')
                    });
                }
                sibling = sibling.nextElementSibling;
            }
            
            return {
                h1: h1 || null,
                hasPageDiv: !!pageDiv,
                pageDivCls: pageDiv ? pageDiv.className : null,
                pageDivStyle: pageDiv ? pageDiv.getAttribute('style') : null,
                topBlocks: topBlocks
            };
        }""")
        print('=== ' + name + ' ===')
        print(info)
        page.close()
        
    browser.close()

