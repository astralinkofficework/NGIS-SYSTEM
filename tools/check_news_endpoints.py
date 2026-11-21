import urllib.request
import json

for ep in ['/api/news', '/api/announcements', '/api/announcements/student']:
    try:
        req = urllib.request.Request('http://127.0.0.1:3000' + ep)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(ep, 'STATUS:', resp.status, 'COUNT:', len(data.get('data', [])))
    except Exception as e:
        print(ep, 'ERROR:', e)
