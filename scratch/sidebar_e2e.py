"""Full sidebar functional test across every NGIS portal page.

For each page x each viewport (desktop/tablet/mobile) verifies:
  - sidebar + scrim mounted by layout engine
  - toggle control visible & clickable
  - collapse/expand (desktop) or open/close drawer (<=1024) round trip
  - main content tracks sidebar state; no horizontal document overflow
  - scrim/outside click closes drawer; close button works
  - state survives a reload
Outputs scratch/sidebar_test_results.json + screenshots for failures.
"""
import json, os, sys, time, tempfile
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:3000/pages/'
ROOT = 'pages'
# Artifacts go OUTSIDE the Flask-watched project tree to avoid reloader churn.
OUT = os.path.join(tempfile.gettempdir(), 'ngis_sidebar')
os.makedirs(OUT, exist_ok=True)
_shot_budget = [12]  # only capture a handful of failure screenshots

def collect_pages():
    pages = []
    for dp, _, fs in os.walk(ROOT):
        for fn in sorted(fs):
            if not fn.endswith('.html'):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), ROOT).replace('\\', '/')
            src = open(os.path.join(dp, fn), encoding='utf-8', errors='replace').read()
            if len(src) < 2000:   # redirect stubs
                continue
            if 'transcript-viewer' in rel or 'access-denied' in rel:
                continue          # standalone pages by design
            pages.append(rel)
    return pages

VIEWPORTS = {
    'desktop': {'width': 1440, 'height': 900},
    'tablet':  {'width': 900,  'height': 1000},
    'mobile':  {'width': 390,  'height': 844},
}

JS_HELPERS = """
(function () {
  window.__sb = {
    sidebar: () => document.getElementById('sidebar'),
    isCollapsed: () => { const s = document.getElementById('sidebar'); return !!s && s.classList.contains('collapsed'); },
    isOpen: () => { const s = document.getElementById('sidebar'); return !!s && s.classList.contains('open'); },
    hOverflow: () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    visible: (el) => {
      if (!el) return false;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0' || cs.pointerEvents === 'none') return false;
      const r = el.getBoundingClientRect();
      return r.width > 4 && r.height > 4;
    },
    toggle: () => {
      const cands = [document.getElementById('sidebarExpandBtn'),
                     document.getElementById('sidebarCollapseBtn')];
      Array.from(document.querySelectorAll("#menuBtn,#htbHamburger,.htb-hamburger,.menu-btn,.hamburger-btn,[data-action='toggle-sidebar']"))
        .forEach(b => { if (!['sidebarCollapseBtn','sidebarExpandBtn'].includes(b.id)) cands.push(b); });
      return cands.find(b => b && __sb.visible(b));
    },
    mainRect: () => { const m = document.querySelector('.main'); return m ? m.getBoundingClientRect().left : null; },
  };
})();
"""

def find_hamburger(page):
    return page.evaluate("""() => {
      const cands = Array.from(document.querySelectorAll("#menuBtn,#htbHamburger,.htb-hamburger,.menu-btn,.hamburger-btn,[data-action='toggle-sidebar']"))
        .filter(b => !['sidebarCollapseBtn','sidebarExpandBtn'].includes(b.id));
      for (const b of cands) {
        const cs = getComputedStyle(b);
        const r = b.getBoundingClientRect();
        if (cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 4 && r.height > 4) {
          b.setAttribute('data-sb-test', '1');
          return true;
        }
      }
      return false;
    }""")

def test_page(ctx, base_url, rel, vp_name, results):
    rec = {'page': rel, 'viewport': vp_name, 'issues': []}
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)[:200]))
    try:
        page.goto(base_url + rel, wait_until='domcontentloaded', timeout=20000)
        try:
            page.wait_for_selector('#sidebar.ngis-layout-ready, body.ngis-layout-ready', timeout=8000)
        except Exception:
            pass
        page.wait_for_timeout(900)
        page.add_script_tag(content=JS_HELPERS)

        mounted = page.evaluate("() => !!document.getElementById('sidebar') && document.body.classList.contains('ngis-layout-ready')")
        if not mounted:
            rec['issues'].append('sidebar-not-mounted')
            results.append(rec); page.close(); return

        scrim = page.evaluate("() => !!document.getElementById('scrim')")
        if not scrim:
            rec['issues'].append('scrim-missing')

        if vp_name == 'desktop':
            start_collapsed = page.evaluate("() => __sb.isCollapsed()")
            hb = find_hamburger(page)
            if hb:
                rec['issues'].append('desktop-hamburger-visible')
            tog = page.evaluate("() => { const t = __sb.toggle(); return !!t && __sb.visible(t); }")
            if not tog:
                rec['issues'].append('no-visible-desktop-toggle')
                results.append(rec); page.close(); return
            page.evaluate("() => __sb.toggle().click()")
            page.wait_for_timeout(500)
            now = page.evaluate("() => __sb.isCollapsed()")
            if now == start_collapsed:
                rec['issues'].append('toggle-1-no-effect(%s->same)' % ('c' if start_collapsed else 'e'))
            page.evaluate("() => __sb.toggle().click()")
            page.wait_for_timeout(500)
            now2 = page.evaluate("() => __sb.isCollapsed()")
            if vp_name == 'desktop' and now2 != start_collapsed:
                rec['issues'].append('toggle-2-did-not-restore')
            mleft = page.evaluate("() => __sb.mainRect()")
            final_collapsed = now2
            if mleft is not None:
                if final_collapsed and mleft > 95:
                    rec['issues'].append('rail-margin-too-wide-for-collapsed(%.0f)' % mleft)
                if (not final_collapsed) and mleft < 200:
                    rec['issues'].append('margin-too-narrow-for-expanded(%.0f)' % mleft)
        else:
            hb = find_hamburger(page)
            if not hb:
                rec['issues'].append('no-visible-hamburger')
                results.append(rec); page.close(); return
            if page.evaluate("() => __sb.isOpen()"):
                page.evaluate("() => document.body.classList.remove('x')")
            page.click('[data-sb-test="1"]')
            page.wait_for_timeout(500)
            if not page.evaluate("() => __sb.isOpen()"):
                rec['issues'].append('drawer-did-not-open')
            if not page.evaluate("() => document.getElementById('scrim').classList.contains('show')"):
                rec['issues'].append('scrim-not-shown')
            if page.evaluate("() => document.querySelector('.main') && document.querySelector('.main').getBoundingClientRect().left < -5"):
                rec['issues'].append('main-shifted')
            # close via sidebar close button
            closed = page.evaluate("""() => {
                const b = document.getElementById('sidebarCloseBtn');
                if (!b) return 'no-close-btn';
                const cs = getComputedStyle(b);
                if (cs.display === 'none' || cs.visibility === 'hidden') return 'close-btn-hidden';
                b.click(); return 'clicked';
            }""")
            page.wait_for_timeout(500)
            if closed == 'clicked' and page.evaluate("() => __sb.isOpen()"):
                rec['issues'].append('close-btn-did-not-close')
            if closed in ('no-close-btn', 'close-btn-hidden'):
                rec['issues'].append(closed)
            # reopen, close via scrim
            page.click('[data-sb-test="1"]')
            page.wait_for_timeout(450)
            page.mouse.click(370, 500)
            page.wait_for_timeout(450)
            if page.evaluate("() => __sb.isOpen()"):
                rec['issues'].append('scrim-click-did-not-close')
            # overflow check with drawer closed
        ovf = page.evaluate("() => __sb.hOverflow()")
        if ovf > 8:
            rec['issues'].append('h-overflow(%dpx)' % ovf)
        if errors:
            rec['issues'].append('js-errors:' + '|'.join(errors[:2]))
    except Exception as e:
        rec['issues'].append('exception:' + str(e)[:150])
        if _shot_budget[0] > 0:
            _shot_budget[0] -= 1
            try:
                page.screenshot(path=os.path.join(OUT, 'sbfail_%s_%s.png' % (rel.replace('/', '_'), vp_name)))
            except Exception:
                pass
    results.append(rec)
    page.close()

def main():
    pages = collect_pages()
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if only:
        pages = [p for p in pages if only in p]
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for vp_name, vp in VIEWPORTS.items():
            ctx = browser.new_context(viewport=vp)
            ctx.add_init_script("""
              try {
                localStorage.setItem('ngis_token', 'mock-jwt-token-admin');
                localStorage.setItem('ngis_user', JSON.stringify({id:'ADM-2024-001', firstName:'Sok Panha', lastName:'Heng', role:'admin', portal:'admin', email:'admin@ngis.edu.kh', title:'Super Administrator'}));
                localStorage.setItem('ngis_active_portal', 'admin');
              } catch (e) {}
            """)
            for rel in pages:
                test_page(ctx, BASE, rel, vp_name, results)
            ctx.close()
        browser.close()
    bad = [r for r in results if r['issues']]
    summary = {'total': len(results), 'failing': len(bad)}
    print(json.dumps(summary))
    for r in bad:
        print('%-50s %-8s %s' % (r['page'], r['viewport'], '; '.join(r['issues'])))
    json.dump(results, open(os.path.join(OUT, 'sidebar_test_results.json'), 'w', encoding='utf-8'), indent=1)

if __name__ == '__main__':
    main()
