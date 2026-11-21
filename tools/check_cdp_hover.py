import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.evaluate("() => document.documentElement.setAttribute('data-theme', 'dark')")
        card = page.locator('#cardAttendance')
        await card.hover()
        await page.wait_for_timeout(200)
        
        # Check computed background
        bg = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        print("Computed Background on Hover:", bg)
        
        # Inspect matched rules via CDP
        client = await page.context.new_cdp_session(page)
        await client.send('DOM.enable')
        await client.send('CSS.enable')
        doc = await client.send('DOM.getDocument')
        node = await client.send('DOM.querySelector', {
            'nodeId': doc['root']['nodeId'],
            'selector': '#cardAttendance'
        })
        # Force pseudo-class :hover on the node in CDP!
        await client.send('CSS.forcePseudoState', {
            'nodeId': node['nodeId'],
            'forcedPseudoClasses': ['hover']
        })
        styles = await client.send('CSS.getMatchedStylesForNode', {'nodeId': node['nodeId']})
        
        print("\n=== MATCHED RULES FOR #cardAttendance WITH :hover FORCED ===")
        for rule_match in styles.get('matchedCSSRules', []):
            rule = rule_match['rule']
            selector = rule['selectorList']['text']
            css_props = rule['style']['cssProperties']
            for bp in css_props:
                if 'background' in bp['name'] and not bp.get('disabled') and bp.get('important'):
                    print(f"[{rule.get('origin', 'user-sheet')}] {selector[:60]}... -> {bp['name']}: {bp['value']} !important")
        
        await browser.close()

asyncio.run(test())
