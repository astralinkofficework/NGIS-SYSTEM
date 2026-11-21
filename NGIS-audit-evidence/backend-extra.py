from pathlib import Path
import json, subprocess, sys, os, re
evidence=Path(__file__).resolve().parent
copy=evidence/'local-instance'
scripts=['tests/academic-mvp.test.py','tests/academic-architecture.test.py','tests/teacher-my-class.test.py','test_principal_e2e.py','test_school_information_e2e.py']
results=[]
for script in scripts:
 try:
  p=subprocess.run([sys.executable,'-B',script],cwd=copy,timeout=45,capture_output=True,encoding='utf-8',errors='replace',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
  out=p.stdout+'\n'+p.stderr
  (evidence/(Path(script).stem+'-output.txt')).write_text(out,encoding='utf8')
  results.append({'suite':script,'exit':p.returncode,'summary':[line.strip() for line in out.splitlines() if re.search(r'^(\s*(FAIL|PASS):|Ran \d|OK|FAILED|AssertionError:|ImportError:|ModuleNotFoundError:)',line)][:100]})
 except subprocess.TimeoutExpired:
  results.append({'suite':script,'error':'45 second timeout'})
 (evidence/'extra-suite-results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
 print(results[-1]['suite'],results[-1].get('exit'),flush=True)
