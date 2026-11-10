import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

routes = re.findall(r"@(?:app|[a-zA-Z_]+)\.route\(['\"]([^'\"]+)['\"]", text)
print(f"Total direct routes in server.py: {len(routes)}")
for r in routes:
    if any(k in r for k in ['banner', 'hero', 'announc', 'news', 'content', 'upload', 'media', 'config', 'dashboard']):
        print('Route:', r)

# check blueprints
blueprints = re.findall(r"app\.register_blueprint\(([^,\)]+)(?:,\s*url_prefix=['\"]([^'\"]+)['\"])?", text)
print("\nRegistered blueprints:")
for bp in blueprints:
    print(bp)

