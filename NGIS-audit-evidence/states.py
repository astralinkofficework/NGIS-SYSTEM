from pathlib import Path
from playwright.sync_api import sync_playwright
import json, time
out=Path(__file__).parent
base='http://127.0.0.1:3017'
rows={}
def note(k,val): 
 rows[k]=val
 (out/'states-results.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
def go(p,path,host=base):
 return p.goto(host+path,wait_until='domcontentloaded',timeout=16000).status
def demo(p,role):
 go(p,'/')
 p.locator(f'a[data-portal="{role}"]:visible').first.click(timeout=7000)
with sync_playwright() as pw:
 b=pw.chromium.launch()
 c=b.new_context(viewport={'width':1440,'height':850},service_workers='block')
 p=c.new_page()
 p.set_default_timeout(7000)
 st={}
 try:
  demo(p,'student')
  p.route('**/api/timetable/state',lambda route:(time.sleep(0.8),route.fulfill(status=503,content_type='application/json',body='{}')))
  st['status']=p.goto(base+'/pages/student/student-timetable.html',wait_until='commit',timeout=10000).status
  st['loading']=p.get_by_text('Loading timetable',exact=False).first.is_visible()
  p.locator('.wktt-state-title').wait_for(timeout=12000)
  st['errorTitle']=p.locator('.wktt-state-title').first.inner_text()
  st['retryVisible']=p.locator('#wkttRetry').is_visible()
  p.screenshot(path=out/'student-timetable-network.png',timeout=5000,animations='disabled')
 except Exception as err: st['error']=str(err).splitlines()[0]
 note('studentTimetable',st)
 c.close()
 c=b.new_context(viewport={'width':1440,'height':850})
 p=c.new_page()
 req={}
 try:
  demo(p,'principal')
  go(p,'/pages/principal/principal-requests.html')
  p.locator('.btn-inspect').first.wait_for()
  p.locator('#searchRequests').fill('zz-audit-no-matches')
  p.get_by_text('No adjustment requests matching the filter.',exact=True).wait_for(timeout=2500)
  req['emptyVisible']=True
 except Exception as err: req['error']=str(err).splitlines()[0]
 note('principalRequestsSearch',req)
 hh={}
 for route in ['/assign','/teachers','/classes','/subjects','/overtime','/now','/print']:
  try: hh[route]={'status':go(p,route,'http://127.0.0.1:3001')}
  except Exception as err: hh[route]={'error':str(err).splitlines()[0]}
 note('timetableDeclared',hh)
 c.close()
 b.close()
