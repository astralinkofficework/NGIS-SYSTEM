from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1024, 'height': 768})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    heavy_fonts = page.evaluate('''() => {
        const els = document.querySelectorAll('*');
        const heavy = [];
        for (const el of els) {
            const fw = window.getComputedStyle(el).fontWeight;
            if (fw === '700' || fw === '800' || fw === '900' || fw === 'bold') {
                heavy.push({
                    tag: el.tagName,
                    cls: el.className,
                    text: el.innerText ? el.innerText.substring(0, 30) : '',
                    weight: fw
                });
            }
        }
        return heavy;
    }''')
    print(f'Heavy font elements found: {len(heavy_fonts)}')
    for h in heavy_fonts[:10]:
        print(h)
        
    browser.close()

