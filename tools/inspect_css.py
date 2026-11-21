import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html')
        info = await page.evaluate('''() => {
            const bodyEl = document.querySelector('#cardAttendance .hub-card-body');
            const rules = [];
            for (let i = 0; i < document.styleSheets.length; i++) {
                const sheet = document.styleSheets[i];
                try {
                    const cssRules = sheet.cssRules || sheet.rules;
                    for (let j = 0; j < cssRules.length; j++) {
                        const rule = cssRules[j];
                        if (rule.selectorText && bodyEl.matches(rule.selectorText)) {
                            rules.push({
                                href: sheet.href || 'inline',
                                selector: rule.selectorText,
                                bg: rule.style.backgroundColor || rule.style.background
                            });
                        }
                    }
                } catch(e) {}
            }
            return {
                computedBg: window.getComputedStyle(bodyEl).backgroundColor,
                rules: rules
            };
        }''')
        print('Computed BG:', info['computedBg'])
        print('Matched Rules:')
        for r in info['rules']:
            if r['bg']:
                print(f"[{r['href']}] {r['selector']} --> {r['bg']}")
        await browser.close()

asyncio.run(check())
