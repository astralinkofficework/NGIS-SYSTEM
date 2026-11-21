# -*- coding: utf-8 -*-
"""
NGIS-SYSTEM Full UX Writing, Dialogs & Interaction Audit
"""
import os
import re
import json

def run_audit():
    root_dir = '.'
    ignore_dirs = {'node_modules', '.git', '.gemini', '.agents', '.venv'}
    
    findings = {
        'confirm_usages': [],
        'buzzword_headings': [],
        'tooltips_and_titles': [],
        'generic_buttons': [],
        'notifications': [],
        'error_messages': []
    }
    
    buzzwords = [
        "Institutional Faculty",
        "Performance Intelligence",
        "Balancing Matrix",
        "Comprehensive Learning",
        "Perimeter Monitoring",
        "Intelligence Center",
        "Credentialing Management",
        "Student Placement Balancing",
        "Enterprise Security and Perimeter",
        "Executive Principal Workspace",
        "Academic Performance Intelligence"
    ]
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for f in files:
            if not (f.endswith('.html') or f.endswith('.js')):
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
            except Exception as e:
                continue
                
            # 1. Native confirm() calls
            for match in re.finditer(r'confirm\s*\(\s*([^\)]+)\)', content):
                val = match.group(1).strip()[:100]
                if not val.startswith('options') and not val.startswith('this'):
                    findings['confirm_usages'].append({
                        'file': path,
                        'snippet': val
                    })
                    
            # 2. Buzzwords in titles/headings
            for b in buzzwords:
                if b.lower() in content.lower():
                    findings['buzzword_headings'].append({
                        'file': path,
                        'buzzword': b
                    })
                    
            # 3. Bad/Generic tooltips or titles
            # E.g. title="Down arrow", title="Three dots", title="Cross icon", title="Eye icon", title="Close"
            bad_titles = ['down arrow', 'three dots', 'cross icon', 'eye icon', 'pencil', 'trash', 'dots']
            for bt in bad_titles:
                if f'title="{bt}"' in content.lower() or f'title=\'{bt}\'' in content.lower():
                    findings['tooltips_and_titles'].append({
                        'file': path,
                        'bad_title': bt
                    })
                    
            # 4. Generic buttons like >Submit<, >Confirm<, >Add<, >Done<, >OK<
            # Look for <button ...>Submit</button>
            for m in re.finditer(r'<button[^>]*>\s*(Submit|Confirm|Done|OK)\s*</button>', content, re.IGNORECASE):
                findings['generic_buttons'].append({
                    'file': path,
                    'button_text': m.group(1)
                })

    print("=== AUDIT SUMMARY ===")
    print(f"Total confirm() usages found: {len(findings['confirm_usages'])}")
    for c in findings['confirm_usages'][:10]:
        print(f"  [{c['file']}] {c['snippet']}")
        
    print(f"\nTotal buzzword headings found: {len(findings['buzzword_headings'])}")
    for b in findings['buzzword_headings'][:10]:
        print(f"  [{b['file']}] {b['buzzword']}")
        
    print(f"\nTotal bad tooltips found: {len(findings['tooltips_and_titles'])}")
    for t in findings['tooltips_and_titles'][:10]:
        print(f"  [{t['file']}] {t['bad_title']}")
        
    print(f"\nTotal bare generic buttons (Submit/Confirm/Done/OK): {len(findings['generic_buttons'])}")
    for gb in findings['generic_buttons'][:10]:
        print(f"  [{gb['file']}] {gb['button_text']}")

if __name__ == '__main__':
    run_audit()
