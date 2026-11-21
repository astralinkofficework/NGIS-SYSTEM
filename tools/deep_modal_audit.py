import os
import re
import json

with open('tools/component_scan_raw.json', 'r', encoding='utf-8') as f:
    scan_data = json.load(f)

modal_pages = list(scan_data['modals'].keys())
print(f"Auditing modals across {len(modal_pages)} pages...")

results = []

for page_path in modal_pages:
    try:
        with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find all modal blocks
        # Looking for div with id containing modal or class containing modal
        pattern = r'(<(?:div|dialog|section)[^>]*id=["\']([^"\']*(?:modal|dialog)[^"\']*)["\'][^>]*>)'
        matches = re.findall(pattern, content, re.I)
        
        for full_tag, modal_id in matches:
            # Extract classes
            cls_match = re.search(r'class=["\']([^"\']*)["\']', full_tag)
            classes = cls_match.group(1) if cls_match else ''
            
            # Find the inner dialog box width/classes if nested
            # Find snippet following the modal opening
            pos = content.find(full_tag)
            snippet = content[pos:pos+1500]
            inner_box_match = re.search(r'<div[^>]*class=["\']([^"\']*(?:max-w|w-|rounded|bg-white)[^"\']*)["\']', snippet)
            inner_classes = inner_box_match.group(1) if inner_box_match else ''
            
            # Check tabs inside modal
            has_tabs = bool(re.search(r'(?:tab-button|role=["\']tab|class=["\'][^"\']*tab[^"\']*)', snippet, re.I))
            
            results.append({
                'page': page_path,
                'modal_id': modal_id,
                'outer_classes': classes,
                'inner_classes': inner_classes,
                'has_tabs': has_tabs
            })
    except Exception as e:
        print(f"Error auditing {page_path}: {e}")

print(f"Total modal instances found: {len(results)}")

with open('tools/deep_modal_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("Saved detailed modal analysis to tools/deep_modal_results.json")
