from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import json, os, re
root = Path(__file__).resolve().parent.parent
out = Path(__file__).parent
base = os.environ.get('NGIS_AUDIT_URL', 'http://127.0.0.1:3000')
groups = {r: sorted('/' + f.relative_to(root).as_posix() for f in (root/'pages'/r).glob('*.html')) for r in ['student','teacher','principal','admin','shared']}
groups['public'] = ['/','/index.html','/404.html','/pages-directory.html','/sitemap.html','/admin','/teacher','/student','/principal','/staff','/access-denied','/parent','/superadmin','/audit-missing.html']
groups['superadmin'] = ['/pages/admin/admin.html?portal=superadmin','/pages/shared/announcements.html?portal=superadmin']
for role in ('student','teacher','principal','admin','superadmin'):
    groups[role] += [f'/pages/shared/{name}.html?portal={role}' for name in ('announcements','departments','lessons','exams')]
groups['shared'] += ['/pages/shared/department.html?id=dept-mat','/pages/shared/lesson-details.html?id=1']
groups['timetable'] = ['/', '/schedule']
measure = """() => {
 const vis=e=>!!(e.getClientRects().length && getComputedStyle(e).visibility==='visible');
 const take=s=>[...document.querySelectorAll(s)].filter(vis);
 const hb=take('[data-action="toggle-sidebar"],.hamburger-btn,.mobile-hamburger-btn,.htb-hamburger');
 const side=document.querySelector('[data-portal-role]');
 const headers=take('header,[role=banner]').map(e=>e.id||e.className).slice(0,10);
 return {title:document.title, h1:take('h1').map(e=>e.innerText.trim()).slice(0,8), headers,
   portal:side?.dataset.portalRole||document.body.dataset.portal||null,
   sidebar:!!side, nav:side? [...side.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).slice(0,90):[],
   hamburgers:hb.map(e=>({label:e.getAttribute('aria-label'),expanded:e.getAttribute('aria-expanded'),width:Math.round(e.getBoundingClientRect().width),height:Math.round(e.getBoundingClientRect().height)})),
   overflow:Math.max(0,document.documentElement.scrollWidth-innerWidth),
   fields:take('input,select,textarea').length,
   unnamed:take('button').filter(e=>!(e.innerText.trim()|| e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')||e.title)).map(e=>e.id||String(e.className)).slice(0,12),
   heavy:take('h1,h2,h3,button').filter(e=>+getComputedStyle(e).fontWeight>500).map(e=>[e.innerText.trim().slice(0,36),getComputedStyle(e).fontWeight]).slice(0,8),
   excerpt:document.body.innerText.trim().slice(0,105)
 };
}"""
def run(task):
 role, width, paths = task
 result = []
 with sync_playwright() as pw:
    browser = pw.chromium.launch()
    c = browser.new_context(viewport={'width':width,'height':860}, is_mobile=width==375, has_touch=width==375, service_workers='block')
    page = c.new_page()
    host = 'http://127.0.0.1:3001' if role == 'timetable' else base
    if role in {'admin','principal','teacher','student'}:
        if width==375: page.set_viewport_size({'width':1440,'height':860})
        page.goto(base+'/',wait_until='domcontentloaded')
        page.locator(f'a[data-portal="{role}"]:visible').first.click(timeout=6000)
        page.wait_for_load_state('domcontentloaded')
        if width==375: page.set_viewport_size({'width':375,'height':860})
    errors, bad = [], []
    page.on('pageerror',lambda err: errors.append(str(err)[:400]))
    page.on('response',lambda res: bad.append([res.status,res.url.replace(host,'')]) if res.status>=400 and res.url.startswith(host) else None)
    for url in dict.fromkeys(paths):
      row={'role':role,'width':width,'path':url}
      try:
        errors.clear()
        bad.clear()
        response=page.goto(host+url,wait_until='domcontentloaded',timeout=28000)
        page.wait_for_timeout(550)
        row.update(status=response.status, final=page.url.replace(host,''), **page.evaluate(measure))
        primary = url.split('?')[0] in [f'/pages/{role}/{role}.html','/pages/admin/admin.html','/pages/principal/principal-requests.html']
        if primary:
          page.reload(wait_until='domcontentloaded',timeout=9000)
          page.wait_for_timeout(550)
          row['refreshPortal']=page.evaluate(measure)['portal']
        if width==375 and row['hamburgers'] and row['sidebar']:
          button=page.locator('[data-action="toggle-sidebar"]:visible,.hamburger-btn:visible,.mobile-hamburger-btn:visible,.htb-hamburger:visible').first
          try:
            button.click(timeout=1600)
            page.wait_for_timeout(220)
            row['drawer']=button.get_attribute('aria-expanded')=='true' or page.locator('#sidebar').evaluate("e=>['open','is-open','active'].some(c=>e.classList.contains(c)) || e.getBoundingClientRect().right > 15")
          except Exception:
            row['drawer']=False
        if primary and width==1440 and row['sidebar']:
          link=page.locator('#sidebar a.nav-link:visible').first
          if link.count():
            style="e=>[getComputedStyle(e).backgroundColor,getComputedStyle(e).color,getComputedStyle(e).boxShadow]"
            before=link.evaluate(style)
            link.hover(timeout=2000)
            page.wait_for_timeout(250)
            row['navHover']=[before,link.evaluate(style)]
        row.update(errors=list(set(errors)),bad=bad[:22])
        if (row.get('overflow',0)>4 or (width==375 and row['sidebar'] and (not row['hamburgers'] or row.get('drawer') is False)) or (url in ('/parent','/superadmin') or 'principal-requests' in url or row.get('navHover', [None,None])[0]!=row.get('navHover',[None,None])[1])):
          name=f'{role}-{width}-'+re.sub('[^a-zA-Z0-9-]+','-',url).strip('-')
          page.screenshot(path=out/(name+'.png'),timeout=2800,animations='disabled')
          row['screenshot']=name+'.png'
      except Exception as err:
        row['error']=str(err).splitlines()[0][:250]
      result.append(row)
    browser.close()
 return result
tasks=[(role,width,paths) for role,paths in groups.items() for width in (1440,375)]
if os.getenv('NGIS_AUDIT_RETRY'):
 tasks=[t for t in tasks if t[0]=='timetable' or (t[1]==375 and t[0] in ('admin','principal','teacher','student'))]
with ThreadPoolExecutor(max_workers=5) as pool:
 result=[r for r in json.loads((out/'page-results.json').read_text(encoding='utf8')) if (r['role'],r['width']) not in {(t[0],t[1]) for t in tasks}] if os.getenv('NGIS_AUDIT_RETRY') else []
 for task in as_completed([pool.submit(run,task) for task in tasks]):
    try: rows=task.result()
    except Exception as err:
      print(str(err)[:500],flush=True)
      continue
    result.extend(rows)
    (out/'page-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(rows[0]['role'],rows[0]['width'],len(rows),flush=True)


