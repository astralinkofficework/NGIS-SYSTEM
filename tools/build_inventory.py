import os
import json

def generate_inventory():
    pages = []
    
    # 1. Root
    for f in os.listdir('.'):
        if f.endswith('.html'):
            pages.append({
                'file': f,
                'path': f,
                'portal': 'Root / Auth / Portal Hub',
                'role': 'Public / Shared'
            })
            
    # 2. Portals
    portal_map = {
        'admin': ('Admin / Super Admin', 'admin'),
        'principal': ('Principal / Leadership', 'principal'),
        'teacher': ('Teacher Portal', 'teacher'),
        'student': ('Student Portal', 'student'),
        'shared': ('Shared Portal', 'shared')
    }
    
    pages_dir = 'pages'
    if os.path.exists(pages_dir):
        for sub in sorted(os.listdir(pages_dir)):
            subpath = os.path.join(pages_dir, sub)
            if os.path.isdir(subpath):
                portal_info = portal_map.get(sub, (f'{sub.capitalize()} Portal', sub))
                for f in sorted(os.listdir(subpath)):
                    if f.endswith('.html'):
                        rel = os.path.join(pages_dir, sub, f).replace('\\', '/')
                        pages.append({
                            'file': f,
                            'path': rel,
                            'portal': portal_info[0],
                            'role': portal_info[1]
                        })
                        
    print(f"Discovered {len(pages)} total routes.")
    with open('tools/page_inventory.json', 'w', encoding='utf-8') as f:
        json.dump(pages, f, indent=2)
    return pages

if __name__ == '__main__':
    generate_inventory()
