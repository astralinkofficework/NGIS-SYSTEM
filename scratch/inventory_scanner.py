import glob, os, re

def build_inventory():
    pages = []
    
    # Root pages
    for f in sorted(glob.glob('*.html')):
        pages.append({
            'file': f,
            'portal': 'Root',
            'route': '/' + f,
            'name': f.replace('.html', '').replace('-', ' ').title()
        })
        
    # Portal pages
    for f in sorted(glob.glob('pages/**/*.html', recursive=True)):
        rel = f.replace('\\', '/')
        parts = rel.split('/')
        portal = parts[1].capitalize() if len(parts) > 2 else 'Shared'
        pages.append({
            'file': rel,
            'portal': portal,
            'route': '/' + rel,
            'name': os.path.basename(f).replace('.html', '').replace('-', ' ').title()
        })
        
    print(f"Total HTML pages found: {len(pages)}")
    
    # Now scan each page for modals, drawers, empty states, loading states
    detailed_inventory = []
    for p in pages:
        with open(p['file'], 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modals = re.findall(r'id=["\']([^"\']*(?:modal|dialog)[^"\']*)["\']', content, re.IGNORECASE)
        drawers = re.findall(r'id=["\']([^"\']*(?:drawer|offcanvas|sidebar-drawer)[^"\']*)["\']', content, re.IGNORECASE)
        empty_states = re.findall(r'class=["\'][^"\']*(?:empty|empty-state|no-data)[^"\']*["\']', content, re.IGNORECASE)
        has_table = '<table' in content.lower()
        has_tabs = 'role="tablist"' in content or 'segmented' in content.lower() or 'cat-pill' in content.lower()
        
        detailed_inventory.append({
            'page': p,
            'modals': list(set(modals)),
            'drawers': list(set(drawers)),
            'has_empty_state': len(empty_states) > 0,
            'has_table': has_table,
            'has_tabs': has_tabs
        })
        
    return detailed_inventory

if __name__ == '__main__':
    inv = build_inventory()
    print("Inventory sample:")
    for item in inv[:5]:
        print(item['page']['route'], "Modals:", item['modals'], "Drawers:", item['drawers'])

