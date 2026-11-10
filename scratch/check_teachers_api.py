import urllib.request
import json

req = urllib.request.Request("http://127.0.0.1:3000/api/principal/roster/teachers")
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("Total teachers:", len(data.get("data", [])))
    if data.get("data"):
        print("Sample teacher keys:", list(data["data"][0].keys()))
        print("Sample teacher:", json.dumps(data["data"][0], indent=2))

