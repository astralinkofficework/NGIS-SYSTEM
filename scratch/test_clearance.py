import urllib.request
import urllib.error
import json

try:
    req = urllib.request.Request('http://127.0.0.1:3000/api/academic/gradebook/clearance-status?classId=cls-10a')
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode('utf-8')[:500])
