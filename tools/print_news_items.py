import urllib.request
import json

req = urllib.request.Request('http://127.0.0.1:3000/api/news')
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for item in data.get('data', [])[:5]:
        print(item.get('id'), item.get('title'), item.get('category'))
