"""Probe computed layout of lost-found + activity toolbars at 1440."""
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})

    page = ctx.new_page()
    page.goto('http://localhost:3000/pages/principal/principal-lost-found.html', wait_until='networkidle')
    page.wait_for_timeout(1500)
    d = page.evaluate("""() => {
      const tf = document.getElementById('typeFilter');
      const sf = document.getElementById('statusFilter');
      const cf = document.getElementById('campusFilter');
      const box = tf.closest('div');
      const r = el => { const b = el.getBoundingClientRect(); return {x:Math.round(b.x),y:Math.round(b.y),w:Math.round(b.width),h:Math.round(b.height)}; };
      return { containerClass: box.className, containerDisplay: getComputedStyle(box).display,
               containerFlexDir: getComputedStyle(box).flexDirection,
               type: r(tf), status: r(sf), campus: r(cf) };
    }""")
    print('LOST-FOUND toolbar:', d)
    page.screenshot(path='scratch/prl_audit/lf_now.png')
    page.close()

    page = ctx.new_page()
    page.goto('http://localhost:3000/pages/principal/principal-activity.html', wait_until='networkidle')
    page.wait_for_timeout(1500)
    d = page.evaluate("""() => {
      const s = document.querySelector('#searchInput, input[type=search], input[type=text]');
      const selects = [...document.querySelectorAll('select')].slice(0,2);
      const btn = [...document.querySelectorAll('button')].find(b=>/query|search/i.test(b.textContent));
      const r = el => el ? {x:Math.round(el.getBoundingClientRect().x),y:Math.round(el.getBoundingClientRect().y),w:Math.round(el.getBoundingClientRect().width)} : null;
      const box = s ? s.closest('div') : null;
      return { search: r(s), sel0: r(selects[0]), sel1: r(selects[1]), btn: r(btn),
               boxClass: box ? box.className : '?', boxDisplay: box ? getComputedStyle(box).display : '?' };
    }""")
    print('ACTIVITY toolbar:', d)
    page.screenshot(path='scratch/prl_audit/act_now.png')
    page.close()
    b.close()
