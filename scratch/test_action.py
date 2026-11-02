import urllib.request
import json

url = 'http://127.0.0.1:3000/api/principal/approvals/appr-amd-001/action'
payload = json.dumps({'action': 'approve', 'note': 'Verified during departmental moderation'}).encode('utf-8')
req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')

resp = urllib.request.urlopen(req)
res_data = json.loads(resp.read().decode('utf-8'))
print('Action response status:', res_data.get('status'))
print('Updated item status:', res_data.get('item', {}).get('status'))
print('New counts:', res_data.get('counts'))

