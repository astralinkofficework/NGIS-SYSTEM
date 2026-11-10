import json
from playwright.sync_api import sync_playwright

URLS = [
    "http://127.0.0.1:3000/pages/principal/principal-reports.html",
    "http://127.0.0.1:3000/pages/principal/principal-dashboard.html",
    "http://127.0.0.1:3000/pages/principal/principal-teachers.html",
    "http://127.0.0.1:3000/pages/student/student-dashboard.html",
]

DIAG = """() => {
  const cs = el => { const s = getComputedStyle(el); return {ox: s.overflowX, oy: s.overflowY, h: s.height, maxH: s.maxHeight, pos: s.position}; };
  const html = document.documentElement, b = document.body;
  // try programmatic scroll
  window.scrollTo(0, 600);
  const afterScroll = window.scrollY;
  window.scrollTo(0, 0);
  // what element sits under the cursor mid-screen and walk up for scroll containers
  const cx = Math.floor(innerWidth/2), cy = Math.floor(innerHeight/2);
  const under = document.elementFromPoint(cx, cy);
  const chain = [];
  let e = under;
  while (e && e !== html) {
    const s = getComputedStyle(e);
    chain.push({
      tag: e.tagName.toLowerCase(),
      id: e.id || '',
      cls: (e.className && typeof e.className === 'string') ? e.className.slice(0,60) : '',
      pos: s.position, oy: s.overflowY, pe: s.pointerEvents, z: s.zIndex,
    });
    e = e.parentElement;
  }
  // find all fixed/absolute full-screen-ish elements on top
  const blockers = [];
  document.querySelectorAll('body *').forEach(el => {
    const s = getComputedStyle(el);
    if (s.position === 'fixed' && s.display !== 'none' && s.visibility !== 'hidden') {
      const r = el.getBoundingClientRect();
      if (r.width >= innerWidth * 0.9 && r.height >= innerHeight * 0.6 && s.pointerEvents !== 'none' && parseFloat(s.opacity) > 0.01) {
        blockers.push({tag: el.tagName.toLowerCase(), id: el.id, cls: String(el.className).slice(0,60), z: s.zIndex, w: Math.round(r.width), h: Math.round(r.height), pe: s.pointerEvents});
      }
    }
  });
  return {
    scrollH: html.scrollHeight, clientH: html.clientHeight, innerH: innerHeight,
    canScroll: html.scrollHeight > innerHeight + 5,
    afterScroll,
    html: cs(html), body: cs(b),
    bodyOverscroll: getComputedStyle(b).overscrollBehavior,
    blockers, chain,
  };
}"""

out = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    page = br.new_page(viewport={"width": 1440, "height": 900})
    for u in URLS:
        page.goto(u, wait_until="networkidle")
        page.wait_for_timeout(1200)
        out[u.split('/')[-1]] = page.evaluate(DIAG)
    br.close()
print(json.dumps(out, indent=1))
