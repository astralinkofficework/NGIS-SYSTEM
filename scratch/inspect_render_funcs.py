import re

for fname in ['pages/principal/principal-services.html', 'pages/principal/principal-departments.html', 'pages/admin/admin-users.html']:
    print(f"\n==================== {fname} ====================")
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find functions that render tables (e.g. renderRequests, renderTable, renderUsers)
    for m in re.finditer(r'function\s+(render\w+|buildRow\w*)\s*\(', content):
        func_name = m.group(1)
        print(f"Found function: {func_name}")
        start = m.start()
        # Grab 1500 chars
        snippet = content[start:start+2500]
        # find table-actions or action-group
        if 'action' in snippet:
            print("Snippet with action:")
            for line in snippet.split('\n'):
                if any(w in line for w in ['action', 'button', '<td', 'btn-']):
                    print("  ", line.strip())

