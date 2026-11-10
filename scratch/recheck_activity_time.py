from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.chromium.launch(); ctx = b.new_context(viewport={'width':1440,'height':900})
    s = ctx.new_page(); s.goto('http://localhost:3000/pages/principal/principal.html', wait_until='domcontentloaded')
    s.evaluate("()=>localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'X',token:'mock-jwt-token-principal'}))")
    s.close(); p = ctx.new_page()
    p.goto('http://localhost:3000/pages/principal/principal-activity.html', wait_until='networkidle'); p.wait_for_timeout(2300)
    print('WHEN cell:', repr(p.evaluate("()=>document.querySelector('#logBody td')?.innerText")))
    p.screenshot(path='scratch/prl_final/principal-activity_desktop.png'); b.close()
