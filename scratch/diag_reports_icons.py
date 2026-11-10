"""Diagnose why Material ligatures render as words on principal-reports."""
from playwright.sync_api import sync_playwright

JS = """() => {
  const spans = [...document.querySelectorAll('#sidebar span.material-symbols-outlined, aside span.material-symbols-outlined')].slice(0,3);
  const out = spans.map(s => ({
    text: s.textContent.trim(),
    cls: s.className,
    ff: getComputedStyle(s).fontFamily,
    fs: getComputedStyle(s).fontSize,
  }));
  // which stylesheet rules target material-symbols-outlined?
  let rules = [];
  for (const sheet of document.styleSheets) {
    let r; try { r = sheet.cssRules; } catch(e) { continue; }
    for (const rule of r) {
      if (rule.selectorText && /material-symbols/i.test(rule.selectorText)) {
        rules.push((sheet.href || 'INLINE') + ' :: ' + rule.cssText.slice(0,200));
      }
    }
  }
  const fonts = [...document.fonts].filter(f => /Material/i.test(f.family)).map(f => f.family + ' ' + f.status);
  return { out, rules: rules.slice(0,12), fonts,
           sidebarFound: !!document.querySelector('#sidebar'), sidebarTag: (document.querySelector('#sidebar')||{}).tagName };
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for page in ['principal-reports.html', 'principal-classes.html']:
        pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
        pg.goto('http://localhost:3000/pages/principal/' + page, wait_until='networkidle')
        pg.wait_for_timeout(2000)
        d = pg.evaluate(JS)
        print('===', page)
        for s in d['out']:
            print('  span:', s)
        print('  fonts:', d['fonts'])
        print('  sidebar:', d['sidebarFound'], d['sidebarTag'])
        for r in d['rules']:
            print('  rule:', r)
        pg.context.close()
    b.close()
