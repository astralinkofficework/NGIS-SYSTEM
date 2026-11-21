from pathlib import Path
from playwright.sync_api import sync_playwright
import json, re, base64, os
out=Path(__file__).parent
base='http://127.0.0.1:3017'
rows=json.loads((out/'targeted-results.json').read_text(encoding='utf8')) if os.getenv('NGIS_AUDIT_SCOPE_ONLY') else {}
def check(name,fn):
 c=b.new_context(viewport={'width':1440,'height':900})
 p=c.new_page()
 p.set_default_timeout(6000)
 row={}
 try: fn(c,p,row)
 except Exception as err: row['error']=str(err).splitlines()[0]
 rows[name]=row
 c.close()
 (out/'targeted-results.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
def visit(p,path,host=base):
 return p.goto(host+path,wait_until='domcontentloaded',timeout=20000).status
def shot(p,name): p.screenshot(path=out/(name+'.png'),timeout=4500)
def demo(p,role):
 visit(p,'/')
 p.locator(f'a[data-portal="{role}"]:visible').first.click()
 p.wait_for_load_state('domcontentloaded')
def mobile(c,p,r):
 p.set_viewport_size({'width':375,'height':800})
 visit(p,'/')
 p.wait_for_timeout(650)
 el=p.locator('a.portal-card[data-portal=student]').first
 el.scroll_into_view_if_needed()
 r['cardHitTest']=el.evaluate("""e=>{const b=e.getBoundingClientRect();const t=document.elementFromPoint(b.x+b.width/2,b.y+b.height/2);return {hitsCard:e.contains(t),hit:t?.closest('aside')?.id||t?.tagName}}""")
 shot(p,'landing-mobile')
 close=p.locator('#sidebarCloseBtn:visible')
 r['closeVisible']=close.count()>0
 if close.count():
  close.click()
  p.wait_for_timeout(300)
  r['cardAfterClose']=el.evaluate("""e=>{const b=e.getBoundingClientRect();return e.contains(document.elementFromPoint(b.x+b.width/2,b.y+b.height/2))}""")
def css(c,p,r):
 demo(p,'principal')
 visit(p,'/pages/principal/principal-requests.html')
 e=p.locator('.btn-inspect').first
 e.wait_for()
 style="""e=>{const z=getComputedStyle(e);return {surface:z.backgroundColor,color:z.color,outline:z.outlineStyle,outlineWidth:z.outlineWidth,shadow:z.boxShadow,keyboard:e.matches(':focus-visible')}}"""
 r['base']=e.evaluate(style)
 e.hover()
 p.wait_for_timeout(350)
 r['hover']=e.evaluate(style)
 shot(p,'principal-inspect-hover')
 box=e.bounding_box()
 p.mouse.move(box['x']+8,box['y']+8)
 p.mouse.down()
 p.wait_for_timeout(250)
 r['pressed']=e.evaluate(style)
 p.mouse.move(0,0)
 p.mouse.up()
 e.focus()
 p.keyboard.press('Tab')
 p.keyboard.press('Shift+Tab')
 r['keyboard']=e.evaluate(style)
 shot(p,'principal-inspect-keyboard')
def nextapp(c,p,r):
 host='http://127.0.0.1:3001'
 r['home']=visit(p,'/',host)
 r['navLinks']=p.locator('a[href]').evaluate_all("es=>[...new Set(es.map(x=>x.getAttribute('href')))]")
 r['schedule']=visit(p,'/schedule',host)
 r['body']=p.locator('body').inner_text()[:240]
 shot(p,'standalone-timetable-error')
def strict_sessions(c,p,r):
 visit(p,'/')
 for role in ('parent','superadmin'):
  p.evaluate('() => window.NGISAuth.clearSession()')
  rr={}
  r[role]=rr
  try:
   data=p.evaluate("""async role=>{try{const x=await window.NGISAuth.login(role+'@ngis.edu.kh','password123');return {role:x.user.role}}catch(e){return {error:e.message}}}""",role)
   rr.update(data)
   if 'error' in data: continue
   path='/pages/admin/admin.html?portal=superadmin' if role=='superadmin' else '/parent'
   rr['landingStatus']=visit(p,path)
   rr['title']=p.title()
   rr['portal']=p.locator('body').get_attribute('data-portal')
   p.reload(wait_until='domcontentloaded')
   rr['refreshPortal']=p.locator('body').get_attribute('data-portal')
  except Exception as err: rr['exception']=str(err).splitlines()[0]
  visit(p,'/')
def public_shortcuts(c,p,r):
 demo(p,'student')
 for path in ('/pages/admin/admin.html','/admin','/teacher','/principal','/student'):
  status=visit(p,path)
  p.wait_for_timeout(280)
  r[path]={'status':status,'title':p.title(),'portal':p.locator('body').get_attribute('data-portal'),'final':p.url.replace(base,'')}
def scope(c,p,r):
 demo(p,'admin')
 token=p.evaluate('() => window.NGISAuth.getToken()')
 options=c.request.get(base+'/api/user-mgmt/form-options?type=admin',headers={'Authorization':'Bearer '+token})
 r['optionsStatus']=options.status
 if not options.ok: return
 data=options.json()
 campuses=data.get('campuses') or data.get('data',{}).get('campuses',[])
 values=[x if isinstance(x,str) else x.get('name') for x in campuses]
 values=[v for v in values if v and 'all campus' not in v.lower()]
 if len(values)<2: r['campusOptionsCount']=len(values); return
 import uuid
 ident='auditscope'+uuid.uuid4().hex[:10]
 pwd='Test-only-password79!'
 add=c.request.post(base+'/api/user-mgmt/create-person',headers={'Authorization':'Bearer '+token},data={'person_type':'admin','first_name':'Scope'+ident[-5:],'last_name':'AuditSample','campus':values[0],'username':ident,'activation':'password','temporary_password':pwd})
 r['createStatus']=add.status
 if not add.ok: r['createError']=str(add.json().get('error',''))[:160]; return
 try:
  p.evaluate("""async ([u,v])=>{await window.NGISAuth.login(u,v)}""",[ident,pwd])
 except Exception as err:
  r['loginError']=str(err).splitlines()[0]
  return
 r['assignmentCampus']=values[0]
 r['availableCampuses']=len(values)
 for api in ('/api/admin/operations/campuses','/api/admin/operations/departments','/api/admin/campuses','/api/admin/departments','/api/user-mgmt/directory?type=student'):
  result=p.evaluate("""async u=>{const a=window.NGISAuth.getUser(); const headers={Authorization:'Bearer '+window.NGISAuth.getToken(),'X-Actor':a.email}; const r=await fetch(u,{headers}),j=await r.json();const x=Array.isArray(j.data)?j.data:(j.rows||j.data?.rows||[]);return {status:r.status,count:x.length,campuses:[...new Set(x.map(a=>a.campus||a.campus_name))].filter(Boolean),nameCount:x.filter(a=>a.name).length,names:u.endsWith("/campuses")?x.map(a=>a.name):undefined}}""",api)
  r[api]=result
 r['assignmentCampus']=values[0]
 r['availableCampuses']=len(values)
with sync_playwright() as pw:
 b=pw.chromium.launch()
 for name,func in [('Mobile landing hit test',mobile),('Control color and keyboard focus',css),('Signed-in Parent and Super Admin',strict_sessions),('Direct route aliases',public_shortcuts),('Scoped Admin data reads',scope),('Standalone timetable',nextapp)]:
  if not os.getenv('NGIS_AUDIT_SCOPE_ONLY') or name=='Scoped Admin data reads': check(name,func)
 b.close()



