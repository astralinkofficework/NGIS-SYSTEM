import urllib.request
import json

AUTH_HEADER = {'Authorization': 'Bearer mock-jwt-token-principal', 'Content-Type': 'application/json'}

def post_json(url, data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=AUTH_HEADER)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get_json(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer mock-jwt-token-principal'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("1. Submitting clearance from teacher...")
r1 = post_json('http://127.0.0.1:3000/api/academic/gradebook/submit-clearance', {'classId': 'cls-10a', 'periodId': 'gp-q1'})
print("Submit result:", r1)

print("\n2. Checking status as teacher...")
r2 = get_json('http://127.0.0.1:3000/api/academic/gradebook/clearance-status?classId=cls-10a&periodId=gp-q1')
print("Clearance status:", r2)

print("\n3. Checking Principal Approvals Queue...")
r3 = get_json('http://127.0.0.1:3000/api/principal/approvals?status=pending')
grade_items = [it for it in r3.get('data', []) if it.get('type') == 'grade_submission']
print("Pending grade submissions in queue:", len(grade_items))
if grade_items:
    target_item = grade_items[0]
    item_id = target_item['id']
    print(f"Target grade item id: {item_id}")

    print("\n4. Principal authorizes item...")
    r4 = post_json(f'http://127.0.0.1:3000/api/principal/approvals/{item_id}/action', {'action': 'approve', 'note': 'Approved by Dr. Ly Bunheng'})
    print("Action result:", r4)

    print("\n5. Checking status as teacher again...")
    r5 = get_json('http://127.0.0.1:3000/api/academic/gradebook/clearance-status?classId=cls-10a&periodId=gp-q1')
    print("Final Clearance status:", r5)
