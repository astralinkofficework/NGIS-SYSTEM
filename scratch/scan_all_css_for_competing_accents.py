import glob
import re

css_files = glob.glob('assets/css/*.css')

# check for purple, indigo, pink, cyan in all css files
re_comp = re.compile(r'\b(#[0-9a-fA-F]{6}|rgba?\([^)]+\))\b')

findings = []

for cf in css_files:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        # look for purple/pink/cyan hexes
        if any(k in l.lower() for k in ['#a855f7', '#7c3aed', '#9333ea', '#8b5cf6', '#c084fc', '#ec4899', '#db2777', '#f43f5e', '#06b6d4', '#0891b2', '#0ea5e9', '#3b82f6', '#6366f1', '#4f46e5']):
            # ignore semantic info if it's #2563eb or #1d4ed8
            findings.append((cf, i+1, l.strip()))

print(f"Found {len(findings)} competing color lines in CSS:")
for cf, line_no, text in findings[:30]:
    print(f"  {cf}:{line_no} -> {text[:80]}")
