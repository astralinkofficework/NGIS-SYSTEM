"""Non-destructive approvals workflow test: intercept POST, verify contract + backend-only load + View modal."""
from playwright.sync_api import sync_playwright
import json
BASE = 'http://localhost:3000/pages/principal/principal-approvals.html'
SEED_IDS = ['REQ-2026-091', 'APV-2026-042', 'CLR-2026-104', 'DOC-2026-055']

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    s = ctx.new_page(); s.goto('http://localhost:3000/pages/principal/principal.html', wait_until='domcontentloaded')
    s.evaluate("()=>{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'Dr. Ly Bunheng',token:'mock-jwt-token-principal'}));}")
    s.close()

    captured = []
    p = ctx.new_page()
    errs = []
    p.on('pageerror', lambda e: errs.append(str(e)[:100]))

    def route_action(route):
        req = route.request
        captured.append({'method': req.method, 'url': req.url, 'body': req.post_data})
        route.fulfill(status=200, content_type='application/json',
                      body=json.dumps({'status': 'success', 'message': 'intercepted'}))

    p.route('**/api/principal/approvals/**/action', route_action)
    p.goto(BASE, wait_until='networkidle'); p.wait_for_timeout(2200)

    rows = p.evaluate("()=>[...document.querySelectorAll('#approvalsTableBody tr')].length")
    present_ids = p.evaluate("""()=>[...document.querySelectorAll('.row-checkbox')].map(c=>c.value)""")
    leaked_seed = [i for i in SEED_IDS if any(i in str(x) for x in present_ids)]
    print('backend rows=%d  leaked_seed_ids=%s' % (rows, leaked_seed or 'NONE'))
    print('sample ids:', present_ids[:4])

    # Click first Authorize button (pending item) -> should POST /action approve (intercepted)
    auth = p.query_selector("#approvalsTableBody button:has-text('Authorize')")
    if auth:
        auth.click(); p.wait_for_timeout(1500)
        print('authorize POST captured:', captured[-1] if captured else 'NONE')
    else:
        print('no Authorize button present (may be all decided)')

    # Click first View button -> detail modal
    view = p.query_selector("#approvalsTableBody button:has-text('View')")
    if view:
        view.click(); p.wait_for_timeout(500)
        vis = p.evaluate("()=>{const m=document.getElementById('recordDetailModal');return m&&m.classList.contains('open')&&m.offsetParent!==null;}")
        title = p.evaluate("()=>document.getElementById('recordDetailTitle')?.textContent")
        bodylen = p.evaluate("()=>document.getElementById('recordDetailBody')?.innerText.length")
        print('view modal open=%s title=%r bodyChars=%s' % (vis, title, bodylen))
        p.keyboard.press('Escape')
    else:
        print('no View button present')

    print('page errors:', errs[:5] if errs else 'NONE')
    b.close()
