import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:3000/api/exams/student?portal=student')
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print('HTTP Status:', resp.status)
        print('Data keys:', list(data.keys()))
        print('Exams count:', len(data.get('exams', [])))
        print('Exams:', data.get('exams'))
except Exception as e:
    print('Error:', e)
