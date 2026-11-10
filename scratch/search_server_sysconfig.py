with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

terms = ['system_configuration', 'school_info', 'school_years', 'campuses', 'editor', 'role', 'auth', 'protect']
for t in terms:
    print(f"'{t}': {text.count(t)} occurrences")

lines = text.splitlines()
for idx, l in enumerate(lines):
    if any(k in l for k in ['/api/school', '/api/system-config', 'system_configuration', 'school_info']):
        print(f"L{idx+1}: {l.strip()[:100]}")

