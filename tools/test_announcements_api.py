import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:3000/api/announcements?portal=student')
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print('HTTP Status:', resp.status)
        print('Data keys:', list(data.keys()))
        items = data.get('data', []) or data.get('announcements', [])
        print('Announcements count:', len(items))
        for item in items[:5]:
            print(' ', item.get('id'), item.get('title'), item.get('target_audience'), item.get('status'))
except Exception as e:
    print('Error:', e)
