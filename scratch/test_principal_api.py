import urllib.request
import json
import time

time.sleep(1) # wait for server to bind

for endpoint in ['/api/principal/stats', '/api/principal/approvals', '/api/principal/audit']:
    url = f'http://127.0.0.1:3000{endpoint}'
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        print(f'{endpoint} -> 200 OK:')
        if 'counts' in data:
            print('  Counts:', data['counts'])
        if 'data' in data:
            if isinstance(data['data'], list):
                print('  Items count:', len(data['data']))
            elif isinstance(data['data'], dict):
                print('  Stats keys:', list(data['data'].keys()))
    except Exception as exc:
        print(f'{endpoint} -> ERROR: {exc}')

