from pathlib import Path
from playwright.sync_api import sync_playwright
import json, base64, time, re, os
out=Path(__file__).parent
base='http://127.0.0.1:3017'
results=json.loads((out/'workflow-results.json').read_text(encoding='utf8')) if os.getenv('NGIS_AUDIT_RETRY') else {}
def save(): (out/'workflow-results.json').write_text(json.dumps(results,indent=2),encoding='utf8')
def visit(page,path): return page.goto(base+path,wait_until='domcontentloaded').status
def demo(page,role):
    visit(page,'/')
    page.locator(f'a[data-portal="{role}"]:visible').first.click()
    page.wait_for_load_state('domcontentloaded')
def opt(page, selector):
    el=page.locator(selector)
    if not el.count(): return
    vals=el.locator('option').evaluate_all("es=>es.filter(e=>e.value&&!e.disabled).map(e=>e.value)")
    if vals and not el.input_value(): el.select_option(vals[0])
def shot(page,name): page.screenshot(path=out/(name+'.png'),timeout=5000)
def check(name,fn):
    row={}
    results[name]=row
    try: fn(row)
    except Exception as err: row['error']=str(err).splitlines()[0]
    save()
def register(role, file, row):
    c=b.new_context(viewport={'width':1440,'height':900},service_workers='block')
    p=c.new_page()
    p.set_default_timeout(5000)
    try:
      demo(p,'admin')
      row['status']=visit(p,'/pages/admin/admin-users-'+file+'.html')
      p.locator('[data-action=add-account]').click()
      p.locator('#nrg-first').wait_for()
      row['wizardOpened']=True
      p.wait_for_timeout(1100)
      row['initialAdvanceDisabled']=p.locator('[data-nrg-primary]').is_disabled()
      suffix=str(int(time.time()))[-6:]
      p.locator('#nrg-first').fill('Audit'+suffix)
      p.locator('#nrg-last').fill(role.capitalize()+'Sample')
      p.locator('#nrg-email').fill(f'audit-{role}-{suffix}@example.test')
      if role=='staff':
        p.locator('#nrg-photo-file').set_input_files({'name':'audit.png','mimeType':'image/png','buffer':base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jhZsAAAAASUVORK5CYII=')})
        p.locator('#nrg-photo-preview img').wait_for()
        row['identityClearedOnSelect']=not p.locator('#nrg-first').input_value()
        row['imagePreview']=True
        p.locator('#nrg-photo-clear').click()
        row['imageRemoved']=p.locator('#nrg-photo-preview img').count()==0
        row['identityClearedByPhoto']=not p.locator('#nrg-first').input_value()
        p.locator('#nrg-first').fill('Audit'+suffix)
        p.locator('#nrg-last').fill(role.capitalize()+'Sample')
        p.locator('#nrg-email').fill(f'audit-{role}-{suffix}@example.test')
      for sel in ('campus','dept','position','enr-dept-0','enr-grade-0','enr-class-0','asgn-dept-0','asgn-grade-0','asgn-class-0','asgn-subj-0'):
        opt(p,'#nrg-'+sel)
      p.locator('[data-nrg-primary]').click()
      p.locator('#nrg-username').wait_for()
      username=p.locator('#nrg-username').input_value()
      password=p.locator('#nrg-password').input_value()
      row['credentialsStep']=bool(username and password)
      p.wait_for_timeout(850)
      p.locator('[data-nrg-primary]').click()
      row['reviewStep']=p.locator('[data-nrg-pane="3"]').count()>0
      with p.expect_response(lambda r:'/api/user-mgmt/create-person' in r.url,timeout=9000) as resp:
        p.locator('[data-nrg-primary]').click()
      response=resp.value
      row['createStatus']=response.status
      data=response.json()
      if not response.ok: row['message']=str(data.get('error',''))[:200]
      else:
        p.locator('[data-nrg-close]').wait_for()
        row['successScreen']=True
        login=c.request.post(base+'/api/auth/login',data={'email':username,'password':password})
        row['loginStatus']=login.status
        if login.ok: row['loginRole']=login.json().get('data',{}).get('user',{}).get('role')
        p.locator('[data-nrg-close]').click()
        row['returnedToDirectory']=p.locator('[data-action=add-account]').is_visible()
    except Exception:
      pane=p.locator('[data-nrg-pane]:visible')
      if pane.count():
        row['pane']=pane.first.get_attribute('data-nrg-pane')
        errs=p.locator('.nrg-error:visible,[role=alert]:visible')
        if errs.count(): row['visibleError']=errs.first.inner_text()[:250]
      if row.get('pane') in ('1',None):
        try: shot(p,'add-'+role+'-blocked')
        except Exception: pass
      raise
    finally: c.close()
def principal(row):
    c=b.new_context(viewport={'width':1440,'height':900})
    p=c.new_page()
    p.set_default_timeout(5500)
    demo(p,'principal')
    path='/pages/principal/principal-requests.html'
    row['status']=visit(p,path)
    p.locator('.btn-inspect').first.wait_for()
    row['initialRows']=p.locator('.btn-inspect').count()
    search=p.locator('#searchRequests')
    search.fill('zz-audit-no-matches')
    row['emptyFeedback']=p.get_by_text('No adjustment requests matching the filter.').is_visible()
    search.fill('')
    p.locator('.btn-inspect').first.click()
    p.locator('#btnAdminClarify').wait_for()
    shot(p,'principal-inspect-actions')
    row['principalActions']=[p.locator(i).inner_text() for i in ('#btnAdminAccept','#btnAdminPublish','#btnAdminClarify','#btnAdminDecline')]
    selector=c.new_page()
    demo(selector,'admin')
    for name, button, dialog in (('clarify','#btnAdminClarify',True),('accept','#btnAdminAccept',False),('publish','#btnAdminPublish',False),('decline','#btnAdminDecline',True)):
      if name!='clarify':
        demo(p,'principal')
        visit(p,path)
        p.locator('.btn-inspect').first.click()
      if dialog: p.once('dialog',lambda d:d.accept('Audit sample rationale'))
      p.locator(button).click()
      p.wait_for_timeout(450)
      row[name]=p.evaluate("""() => {const a=JSON.parse(localStorage.getItem('ngis_academic_adjustment_requests'));return {status:a[0].status,entry:a[0].timeline.at(-1),entries:a[0].timeline.length}}""")
    demo(p,'principal')
    visit(p,path)
    p.locator('.btn-inspect').first.wait_for()
    row['historyAfterReload']=p.locator('#requestsTableBody tr').first.inner_text().splitlines()[-3:]
    separate=b.new_context().new_page()
    demo(separate,'principal')
    visit(separate,path)
    separate.locator('.btn-inspect').first.wait_for()
    row['freshContextStatus']=separate.evaluate("() => JSON.parse(localStorage.getItem('ngis_academic_adjustment_requests'))[0].status")
    shot(p,'principal-local-status')
    shot(separate,'principal-fresh-status')
    separate.context.close()
    c.close()
def parent(row):
    c=b.new_context()
    p=c.new_page()
    row['status']=visit(p,'/parent')
    row['title']=p.title()
    row['landingPortalCards']=p.locator('a[data-portal]').evaluate_all("es=>[...new Set(es.map(e=>e.dataset.portal))]")
    row['parentPageStatus']=visit(p,'/pages/parent/parent.html')
    shot(p,'parent-page-missing')
    c.close()
def permission(row):
    p=b.new_page()
    demo(p,'student')
    row['ownPage']=visit(p,'/pages/student/student.html')
    row['otherRolePage']=visit(p,'/pages/admin/admin.html')
    row['otherRoleTitle']=p.title()
    p.close()
with sync_playwright() as pw:
 b=pw.chromium.launch()
 for role,file in [('student','students'),('teacher','teachers'),('staff','staff'),('principal','principals'),('admin','admins')]:
  if (os.getenv('NGIS_AUDIT_RETRY')=='staff' and role=='staff') or (os.getenv('NGIS_AUDIT_RETRY')!='staff' and (not os.getenv('NGIS_AUDIT_RETRY') or role in ('student','staff'))):
   check('Add '+role,lambda row,role=role,file=file:register(role,file,row))
 if os.getenv('NGIS_AUDIT_RETRY')!='staff':
  check('Principal adjustment review',principal)
  check('Parent routing',parent)
  check('Portal navigation with a Student demo session',permission)
 b.close()


