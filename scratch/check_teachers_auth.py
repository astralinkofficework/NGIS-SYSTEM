import sys
sys.path.insert(0, '.')
import server
client = server.app.test_client()

login_res = client.post('/api/auth/login', json={'username': 'principal', 'password': 'password123'})
print("Login status:", login_res.status_code)
token = ""
if login_res.status_code == 200:
    token = login_res.json.get('token', '')
    print("Token found")

headers = {'Authorization': f'Bearer {token}'} if token else {}
res = client.get('/api/principal/roster/teachers', headers=headers)
print("Teachers endpoint status:", res.status_code)
if res.status_code == 200:
    data = res.json.get('data', [])
    print("Teachers count:", len(data))
    if data:
        print("First teacher:")
        for k, v in data[0].items():
            print(f"  {k}: {v}")
