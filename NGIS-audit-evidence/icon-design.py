"""Browser regression check for ordinary icon slots and semantic controls."""
import json
import mimetypes
from urllib.parse import urlsplit
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = 'http://ngis-audit.local'
OUT = Path(__file__).resolve().parent
PHASE = sys.argv[1]
ROOT = OUT.parent
FILES = {str(f.relative_to(ROOT).as_posix()):f.read_bytes() for d in ('assets','pages') for f in (ROOT/d).rglob('*') if f.is_file() and f.suffix in {'.css','.js','.html','.svg'}}
CSS = ['design-tokens', 'app', 'shared-components', 'design-system', 'khmer-suite', 'mobile-header']
PAGES = {
    'admin': '/pages/admin/admin.html',
    'principal': '/pages/principal/principal.html',
    'teacher': '/pages/teacher/teacher-attendance.html',
    'student': '/pages/student/student-grades.html',
    'shared': '/pages/shared/departments.html',
}
CHECK = """el => {
  const style = getComputedStyle(el);
  return {background: style.backgroundColor, color: style.color,
    image: style.backgroundImage, box: style.boxShadow, outline: style.outlineStyle,
    width: el.getBoundingClientRect().width};
}"""
ICONS = ['.smx-kpi-icon', '.ks-kpi-icon', '.ngis-notif-icon-wrap', '.mob-bn-icon-wrap']
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    context = browser.new_context(viewport={'width': 1024, 'height': 768})
    page = context.new_page()
    def serve(route):
        parts = urlsplit(route.request.url)
        path = parts.path.lstrip('/')
        if parts.hostname != 'ngis-audit.local':
            return route.abort()
        if path in FILES:
            return route.fulfill(body=FILES[path], content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream')
        if path.startswith('api/'):
            return route.fulfill(json={'data': [], 'success': True})
        return route.fulfill(status=404, body='')
    page.route('**/*', serve)
    page.route('**/icon-audit-fixture', lambda route: route.fulfill(content_type='text/html', body=
        '<!doctype html><html><head><meta name="viewport" content="width=device-width">' +
        ''.join(f'<link rel="stylesheet" href="/assets/css/{name}.css">' for name in CSS) +
        '</head><body style="padding:40px"><main>' +
        '<div class="smx-kpi"><span class="smx-kpi-icon">A</span><span class="smx-kpi-icon warn">!</span></div>' +
        '<div class="ks-kpi"><span class="ks-kpi-icon">B</span><span class="ks-kpi-icon bad">!</span></div>' +
        '<div class="ngis-notif-icon-wrap">C</div>' +
        '<a href="#current" class="mob-bn-item is-active" aria-current="page"><span class="mob-bn-icon-wrap">D</span><span>Current</span></a>' +
        '<button type="button" class="btn-primary">Primary</button><button type="button" class="btn-accent">Legacy accent</button>' +
        '</main></body></html>'))
    page.goto(BASE + '/icon-audit-fixture', wait_until='load')
    fixture = {selector: [el.evaluate(CHECK) for el in page.locator(selector).all()]
               for selector in [*ICONS, '.btn-primary', '.btn-accent']}
    page.screenshot(path=OUT / f'icon-components-{PHASE}.png', timeout=5000)
    page.locator('.btn-accent').hover()
    fixture['accentHover'] = page.locator('.btn-accent').evaluate(CHECK)
    page.keyboard.press('Tab')
    page.keyboard.press('Tab')
    fixture['primaryFocus'] = page.locator('.btn-primary').evaluate(CHECK)
    page.evaluate("document.documentElement.dataset.theme = 'dark'")
    fixture['dark'] = {selector: [el.evaluate(CHECK) for el in page.locator(selector).all()] for selector in ICONS}
    rows = []
    for width in (1440, 768, 375):
        page.set_viewport_size({'width':width,'height':850})
        for role, path in PAGES.items():
            try:
                response = page.goto(BASE + path, wait_until='domcontentloaded', timeout=10000)
                page.wait_for_timeout(450)
                rows.append({'role':role,'path':path,'width':width,'status':response.status,'title':page.title(),
                    'icons':{sel:[el.evaluate(CHECK) for el in page.locator(sel).all()[:3]] for sel in ICONS}})
                if width == 375 or role == 'admin':
                    try:
                        page.screenshot(path=OUT / f'icons-{role}-{width}-{PHASE}.png', timeout=4500)
                    except Exception as e:
                        rows[-1]['screenshotError'] = str(e).splitlines()[0]
            except Exception as e:
                rows.append({'role':role,'width':width,'error':str(e).splitlines()[0]})
    (OUT / f'icon-design-{PHASE}.json').write_text(json.dumps({'fixture':fixture,'pages':rows},indent=2),encoding='utf-8')
    if PHASE == 'after':
        for result in [fixture, fixture['dark']]:
            for selector in ICONS:
                for style in result[selector]:
                    assert style['background'] == 'rgba(0, 0, 0, 0)' and style['image'] == 'none', (selector, style)
        assert fixture['.btn-primary'][0]['background'] == fixture['.btn-accent'][0]['background']
        assert fixture['primaryFocus']['outline'] != 'none'

