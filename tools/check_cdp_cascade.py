import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        await page.wait_for_timeout(200)
        
        client = await page.context.new_cdp_session(page)
        await client.send('DOM.enable')
        await client.send('CSS.enable')
        doc = await client.send('DOM.getDocument')
        node = await client.send('DOM.querySelector', {
            'nodeId': doc['root']['nodeId'],
            'selector': '#cardAttendance'
        })
        styles = await client.send('CSS.getMatchedStylesForNode', {'nodeId': node['nodeId']})
        
        print("=== MATCHED CSS RULES (in cascade order) ===")
        for rule_match in styles.get('matchedCSSRules', []):
            rule = rule_match['rule']
            selector = rule['selectorList']['text']
            css_props = rule['style']['cssProperties']
            bg_props = [p for p in css_props if 'background' in p['name']]
            if bg_props:
                for bp in bg_props:
                    print(f"Selector: {selector[:60]}... | {bp['name']}: {bp['value']} (disabled={bp.get('disabled')})")
        
        await browser.close()

asyncio.run(test())
