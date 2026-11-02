import re

principal_files = [
    'pages/principal/principal.html',
    'pages/principal/principal-approvals.html',
    'pages/principal/principal-reports.html',
    'pages/principal/principal-profile.html'
]

# Rogue color patterns to flag
rogue_patterns = [
    r'#(?!202[fF]63|92243[dD]|(?:[fF]{6}|[fF]3[fF]3[fF]5|[eE]5[eE]5[eE]8|000000|[fF]{3}|000))[0-9a-fA-F]{3,8}\b',
    r'\b(?:bg|text|border)-(?:blue|indigo|emerald|purple|amber|yellow|orange|cyan|pink|violet)-\d{2,3}\b',
    r'\b(?:green|blue|amber|purple|teal)\b'
]

for p in principal_files:
    print(f"\n--- Checking {p} ---")
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues = []
    for idx, line in enumerate(lines, 1):
        # Ignore comments or external URLs
        if 'http://' in line or 'https://' in line or '<!--' in line:
            continue
        # Check rogue tailwind classes
        tw = re.findall(r'\b(?:bg|text|border)-(?:blue|indigo|emerald|purple|amber|yellow|orange|cyan|pink|violet)-\d{2,3}\b', line)
        if tw:
            issues.append((idx, f"Tailwind color: {tw}", line.strip()[:90]))
        # Check hex codes not in palette
        hexes = re.findall(r'#[0-9a-fA-F]{3,8}\b', line)
        for h in hexes:
            h_norm = h.upper()
            if h_norm not in ('#202F63', '#92243D', '#FFFFFF', '#000000', '#F3F3F5', '#E5E5E8', '#FFF', '#000', '#666', '#777', '#888', '#999', '#333', '#111', '#222', '#444', '#555', '#7A1D32', '#7E1E34'):
                # Flag if looks like green, blue, yellow, etc.
                if any(k in h_norm for k in ['10B981', '2563EB', '3B82F6', 'D97706', '9333EA', 'F59E0B', 'EF4444', '16A34A']):
                    issues.append((idx, f"Rogue hex: {h}", line.strip()[:90]))

    if issues:
        for lnum, desc, snippet in issues:
            print(f"  Line {lnum}: {desc} -> {snippet}")
    else:
        print("  Clean! No rogue colors found.")

