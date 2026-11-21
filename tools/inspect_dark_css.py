import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        
        await page.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.documentElement.classList.add('dark');
        }""")
        await page.wait_for_timeout(300)
        
        info = await page.evaluate('''() => {
            const cardEl = document.querySelector('#cardAttendance');
            const rules = [];
            for (let i = 0; i < document.styleSheets.length; i++) {
                const sheet = document.styleSheets[i];
                try {
                    const cssRules = sheet.cssRules || sheet.rules;
                    for (let j = 0; j < cssRules.length; j++) {
                        const rule = cssRules[j];
                        if (rule.selectorText && cardEl.matches(rule.selectorText)) {
                            rules.push({
                                href: sheet.href ? sheet.href.split('/').pop() : 'inline',
                                selector: rule.selectorText,
                                bg: rule.style.backgroundColor || rule.style.background
                            });
                        }
                    }
                } catch(e) {}
            }
            return {
                computedBg: window.getComputedStyle(cardEl).backgroundColor,
                rules: rules
            };
        }''')
        print('Card Computed BG in Dark Mode:', info['computedBg'])
        print('Matched Rules:')
        for r in info['rules']:
            if r['bg']:
                print(f"[{r['href']}] {r['selector']} --> {r['bg']}")
        await browser.close()

asyncio.run(check())
