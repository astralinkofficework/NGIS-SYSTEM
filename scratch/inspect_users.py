import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

print("Searching DB users in server.py...")
users_block = re.search(r"'users':\s*\[(.*?)\]\s*,", text, re.DOTALL)
if users_block:
    print("Found users list:")
    print(users_block.group(1)[:1000])
else:
    print("No direct 'users' list, checking roles:")
    for m in re.finditer(r"'(user_id|userId|id)':\s*'([^']+)'.*?'role':\s*'([^']+)'", text):
        print(m.groups())

