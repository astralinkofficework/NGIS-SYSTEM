from pathlib import Path
import json, subprocess, sys, os, inspect
evidence=Path(__file__).resolve().parent
copy=evidence/'local-instance'
sys.path.insert(0,str(copy))
os.chdir(copy)
from server import app
routes=[]
for rule in sorted(app.url_map.iter_rules(), key=lambda x:x.rule):
 fn=app.view_functions[rule.endpoint]
 try:
  source=Path(inspect.getsourcefile(fn)).relative_to(copy).as_posix()
  line=inspect.getsourcelines(fn)[1]
 except Exception: source,line=None,None
 routes.append({'route':rule.rule,'methods':sorted(set(rule.methods)-{'HEAD','OPTIONS'}),'endpoint':rule.endpoint,'source':source,'line':line})
(evidence/'server-routes.json').write_text(json.dumps(routes,indent=2),encoding='utf-8')
scripts=['test_roles_permissions.py','test_timetable_replacement.py','test_timetable_monitoring.py','test_simplified_exams.py','test_sidebar_manager.py','test_dashboard_cms.py','test_khmer_suite.py','test_ui_states_mvp.py']
results=[r for r in json.loads((evidence/'suite-results.json').read_text(encoding='utf-8')) if r['suite'] not in scripts and not r['suite'].endswith('.test.py')]
for script in scripts:
 try:
  x=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-p',script],capture_output=True,cwd=copy,timeout=42,encoding='utf-8',errors='replace',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
  import re
  tx=x.stdout+'\n'+x.stderr
  keylines=[line[:350] for line in tx.splitlines() if re.match(r'^(FAIL:|ERROR:|Ran \d|OK|FAILED|AssertionError:|ImportError:|ModuleNotFoundError:|FileNotFoundError:)',line)]
  (evidence/(script+'-output.txt')).write_text(tx,encoding='utf-8')
  results.append({'suite':script,'exit':x.returncode,'summary':keylines})
 except subprocess.TimeoutExpired:
  results.append({'suite':script,'error':'42 second timeout'})
 (evidence/'suite-results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
 print(script,results[-1].get('exit'),flush=True)

