import json, urllib.request, os, re

with open('scratch/phase0_inventory.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

print(f"Total pages in inventory: {len(pages)}")

status_results = []
asset_errors = []

for page in pages:
    rel_path = page['path'].replace('\\', '/')
    url = f"http://localhost:3000/{rel_path}"
    
    # Try fetching page
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NGISTestBot'})
        with urllib.request.urlopen(req) as resp:
            code = resp.status
            html = resp.read().decode('utf-8', errors='ignore')
            status_results.append((rel_path, code, len(html)))
            
            # Check referenced assets (css, js, img)
            links = re.findall(r'(?:href|src)=["\']([^"\']+)["\']', html)
            for link in links:
                if link.startswith(('http://', 'https://', '//', 'data:', 'javascript:', '#', 'mailto:', 'tel:')):
                    continue
                page_dir = os.path.dirname(rel_path)
                clean_link = link.split('?')[0].split('#')[0]
                target_path = os.path.normpath(os.path.join(page_dir, clean_link)).replace('\\', '/')
                if not os.path.exists(target_path):
                    if not '${' in link and not '{' in link:
                        asset_errors.append((rel_path, link, target_path))
    except urllib.error.HTTPError as e:
        status_results.append((rel_path, e.code, 0))
    except Exception as e:
        status_results.append((rel_path, str(e), 0))

print("\n--- Summary of Page Requests ---")
failed_pages = [r for r in status_results if r[1] != 200]
print(f"Total 200 OK: {len(status_results) - len(failed_pages)} / {len(status_results)}")
if failed_pages:
    print(f"Failed pages: {failed_pages}")
else:
    print("ALL 74 pages returned 200 OK!")

print(f"\n--- Asset Check ---")
print(f"Missing local assets: {len(asset_errors)}")
for page, link, target in asset_errors[:15]:
    print(f"  In {page}: missing '{link}' (checked {target})")
