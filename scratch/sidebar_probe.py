from playwright.sync_api import sync_playwright

init = """
try {
  localStorage.setItem('ngis_token', 'mock-jwt-token-admin');
  localStorage.setItem('ngis_user', JSON.stringify({role:'admin', portal:'admin'}));
  localStorage.setItem('ngis_active_portal', 'admin');
} catch (e) {}
"""

JS = """() => {
  const el = document.getElementById('sidebarExpandBtn');
  if (!el) return {missing:true};
  const out = {inlineDisplay: el.style.display, inlineOpacity: el.style.opacity,
               inlineCssText: el.getAttribute('style'), matched: []};
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch(e){ continue; }
    const href = (sheet.href||'').split('/').pop();
    const walk = (list, mq) => {
      for (const r of list) {
        if (r.type === 4 || r.type === 12) { walk(r.cssRules, r.conditionText || r.media?.mediaText || mq); continue; }
        if (r.type !== 1 || !r.selectorText) continue;
        let ok = false;
        const parts = r.selectorText.split(',');
        for (const sel of parts) {
          try { if (el.matches(sel.trim())) { ok = true; break; } } catch(e){}
        }
        if (ok) out.matched.push({href, mq: mq||null, sel: r.selectorText, css: r.style.cssText});
      }
    };
    walk(rules, null);
  }
  return out;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.add_init_script(init)
    p = ctx.new_page()
    p.goto('http://localhost:3000/pages/admin/admin.html', wait_until='domcontentloaded')
    p.wait_for_timeout(2000)
    for m in p.evaluate(JS)['matched']:
        print(m['href'], '|', m['mq'], '|', m['sel'], '|', m['css'])
    b.close()
