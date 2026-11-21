from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    cdp = page.context.new_cdp_session(page)
    cdp.send('DOM.enable')
    cdp.send('CSS.enable')
    doc = cdp.send('DOM.getDocument')
    node = cdp.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': '#ngisGlobalNavbar'})
    styles = cdp.send('CSS.getMatchedStylesForNode', {'nodeId': node['nodeId']})
    
    print('Matched rules count:', len(styles.get('matchedCSSRules', [])))
    for r in styles.get('matchedCSSRules', []):
        rule = r['rule']
        selector = rule['selectorList']['text']
        props = []
        for p in rule['style']['cssProperties']:
            if 'background' in p['name'] or 'border' in p['name']:
                imp = ' !important' if p.get('important') else ''
                props.append(f"{p['name']}: {p['value']}{imp}")
        if props:
            origin = rule.get('origin', 'regular')
            print(f'Selector: {selector} (origin: {origin})')
            for pr in props:
                print('   ', pr)
    browser.close()
