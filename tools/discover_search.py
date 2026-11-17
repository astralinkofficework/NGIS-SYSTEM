import os
import re
import json

def discover_search_inputs():
    search_inputs = []
    html_files = []
    
    ignore_dirs = {'node_modules', '.agents', '.claude', '.git', '.workbuddy-ai', '.ux', '.testshots'}

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    print(f"Total HTML files to inspect: {len(html_files)}")

    input_pattern = re.compile(r'<input\b[^>]*>', re.IGNORECASE)

    for fpath in html_files:
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            continue

        for m in input_pattern.finditer(content):
            tag = m.group(0)
            is_search = False
            if re.search(r'type\s*=\s*["\']search["\']', tag, re.I):
                is_search = True
            elif re.search(r'placeholder\s*=\s*["\'][^"\']*search[^"\']*["\']', tag, re.I):
                is_search = True
            elif re.search(r'id\s*=\s*["\'][^"\']*search[^"\']*["\']', tag, re.I):
                is_search = True
            elif re.search(r'class\s*=\s*["\'][^"\']*search[^"\']*["\']', tag, re.I):
                is_search = True
            elif re.search(r'name\s*=\s*["\'][^"\']*search[^"\']*["\']', tag, re.I):
                is_search = True

            if is_search:
                line_no = content[:m.start()].count('\n') + 1
                # Find the surrounding container if possible
                start_ctx = max(0, m.start() - 250)
                end_ctx = min(len(content), m.end() + 250)
                context = content[start_ctx:end_ctx]

                search_inputs.append({
                    'file': fpath.replace('\\', '/'),
                    'line': line_no,
                    'tag': tag.strip(),
                    'context': context
                })

    print(f"Discovered {len(search_inputs)} search input occurrences across HTML files.")

    # Also discover in JS files (dynamic templates, document.createElement, etc.)
    js_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if f.endswith('.js'):
                js_files.append(os.path.join(root, f))

    print(f"Total JS files to inspect: {len(js_files)}")
    js_search_inputs = []
    for fpath in js_files:
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue

        # Look for search input strings or creation
        matches = list(re.finditer(r'(<input\b[^>]*search[^>]*>|type\s*[:=]\s*["\']search["\'])', content, re.I))
        for m in matches:
            line_no = content[:m.start()].count('\n') + 1
            start_ctx = max(0, m.start() - 150)
            end_ctx = min(len(content), m.end() + 150)
            js_search_inputs.append({
                'file': fpath.replace('\\', '/'),
                'line': line_no,
                'match': m.group(0),
                'context': content[start_ctx:end_ctx]
            })

    print(f"Discovered {len(js_search_inputs)} search references in JS files.")

    with open('tools/search_inventory.json', 'w', encoding='utf-8') as out:
        json.dump({'html_inputs': search_inputs, 'js_inputs': js_search_inputs}, out, indent=2)

    print("Inventory saved to tools/search_inventory.json")

if __name__ == '__main__':
    discover_search_inputs()
