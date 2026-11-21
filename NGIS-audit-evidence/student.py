from pathlib import Path
from playwright.sync_api import sync_playwright
import json, base64
out=Path(__file__).parent
base='http://127.0.0.1:3017'
res={}
pdf={'name':'audit-sample.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4\nNGIS test fixture\n%%EOF'}
def open_page(p,path): return p.goto(base+path,wait_until='domcontentloaded',timeout=14000).status
def shot(p,n):
 try: p.screenshot(path=out/(n+'.png'),timeout=3500,animations='disabled')
 except Exception: pass
def run(name,fn):
 c=b.new_context(viewport={'width':1440,'height':850},service_workers='block')
 p=c.new_page()
 p.on('dialog',lambda d:d.accept())
 p.set_default_timeout(5000)
 row={}
 try:
  open_page(p,'/')
  p.locator('a[data-portal=student]:visible').first.click()
  fn(p,row)
 except Exception as err: row['error']=str(err).splitlines()[0]
 res[name]=row
 (out/'student-workflows.json').write_text(json.dumps(res,indent=2),encoding='utf8')
 c.close()
def assignment(p,r):
 r['status']=open_page(p,'/pages/student/student-assignments.html')
 p.locator('button[onclick^=openUpload]:visible').first.click()
 r['initialDisabled']=p.locator('#umSubmitBtn').is_disabled()
 p.locator('#umFileInput').set_input_files(pdf)
 r['fileSelected']=p.locator('#umFName').inner_text()
 r['disabledBeforeDeclaration']=p.locator('#umSubmitBtn').is_disabled()
 p.locator('#umIntegrity').check()
 r['enabledAfterDeclaration']=p.locator('#umSubmitBtn').is_enabled()
 req=[]
 p.on('request',lambda q:req.append([q.method,q.url.replace(base,'')]) if q.method in ('POST','PUT','PATCH') else None)
 p.locator('#umSubmitBtn').click()
 r['uploadProgress']=p.locator('#umLoader.show').is_visible()
 p.locator('#umSuccessPhase.show').wait_for()
 r['reportedSuccess']=True
 r['writeRequests']=req
 shot(p,'assignment-upload-simulated')
 p.reload(wait_until='domcontentloaded')
 r['submitRemainsAvailable']=p.locator('button[onclick^=openUpload]:visible').first.is_visible()
def service(p,r):
 r['status']=open_page(p,'/pages/student/student-services.html')
 p.locator('#openNewRequestHeroBtn').click()
 p.locator('#serviceStep1').wait_for()
 r['wizardOpened']=True
 for step in (2,3,4):
  if step==4:
   p.locator('#srvFileInput').set_input_files(pdf)
   r['filePreview']=p.locator('#srvFileName').inner_text()
  p.locator('#srvNextBtn').click()
  p.locator('#serviceStep'+str(step)).wait_for()
 r['reviewReached']=True
 r['disabledBeforeConfirmation']=p.locator('#srvSubmitBtn').is_disabled()
 p.locator('#srvConfirmCheck').check()
 req=[]
 p.on('request',lambda q:req.append([q.method,q.url.replace(base,'')]) if q.method in ('POST','PUT','PATCH') else None)
 p.locator('#srvSubmitBtn').click()
 p.wait_for_timeout(350)
 r['writeRequests']=req
 r['successText']=p.get_by_text('Service request submitted successfully',exact=False).count()
 shot(p,'service-request-result')
def lost(p,r):
 r['status']=open_page(p,'/pages/student/student-lost-found.html')
 p.locator('#openReportHeroBtn').click()
 p.locator('#formTitle').fill('Audit sample pencil case')
 p.locator('#formLocation').fill('Audit sample room')
 p.locator('#formDate').fill('2026-11-20')
 p.locator('#formDescription').fill('An audit-only record for a sample pencil case.')
 for loc in ('#formCategory','#formCampus'):
  el=p.locator(loc)
  values=el.locator('option').evaluate_all("es=>es.filter(e=>e.value&&!e.disabled).map(e=>e.value)")
  if values and not el.input_value(): el.select_option(values[0])
 with p.expect_response(lambda q:q.request.method=='POST' and q.url.endswith('/api/lost-found'),timeout=8000) as response:
  p.locator('#btnSubmitReport').click()
 r['submitHttpStatus']=response.value.status
 r['hasServerData']=bool(response.value.json().get('data'))
with sync_playwright() as pw:
 b=pw.chromium.launch()
 for k,f in [('assignment',assignment),('service',service),('lostFound',lost)]: run(k,f)
 b.close()
