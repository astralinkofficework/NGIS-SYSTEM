"""Pinpoint undefined/NaN/[object Object] text leaks per principal page."""
from playwright.sync_api import sync_playwright

PAGES = ['principal-teacher-profiles.html', 'principal-student-profiles.html',
         'principal-approvals.html', 'principal-activity.html',
         'principal-reports.html', 'principal-classes.html',
         'principal-departments.html', 'principal-attendance.html',
         'principal-timetables.html', 'principal-services.html',
         'principal-lost-found.html', 'principal-profile.html', 'principal.html']

PROBE = r"""() => {
  const hits = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = (n.textContent || '').trim();
    if (/undefined|NaN|\[object Object\]|null/.test(t) && t.length < 60) {
      let el = n.parentElement, path = [];
      while (el && path.length < 3) { path.push(el.className || el.tagName); el = el.parentElement; }
      hits.push(t.slice(0,50) + '  @ ' + path.join(' < ').slice(0,80));
    }
  }
  return hits.slice(0, 10);
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    warm = ctx.new_page(); warm.goto('http://localhost:3000/pages/principal/principal-classes.html', wait_until='networkidle'); warm.close()
    for name in PAGES:
        page = ctx.new_page()
        page.goto('http://localhost:3000/pages/principal/' + name, wait_until='networkidle')
        page.wait_for_timeout(2200)
        hits = page.evaluate(PROBE)
        print('=== %-34s leaks=%d' % (name, len(hits)))
        for h in hits:
            print('    ', h)
        page.close()
    b.close()
