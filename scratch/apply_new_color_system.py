import glob, os, re

# Color replacements dictionary
REPLACEMENTS = [
    # Accent & Brand Colors
    ('#1e4d38', '#2455D6'),
    ('#1E4D38', '#2455D6'),
    ('#163b2a', '#193DAA'),
    ('#163B2A', '#193DAA'),
    ('#0f281d', '#132F85'),
    ('#0F281D', '#132F85'),
    ('#13829b', '#2455D6'),
    ('#13829B', '#2455D6'),
    ('#0e6d82', '#193DAA'),
    ('#179bb8', '#2455D6'),
    ('#1baec7', '#3B82F6'),
    ('#2f4550', '#2455D6'),
    ('#2F4550', '#2455D6'),
    ('#24363f', '#193DAA'),
    ('#24363F', '#193DAA'),
    
    # Soft & Supporting Colors
    ('#b8dbd9', '#EAF2FF'),
    ('#B8DBD9', '#EAF2FF'),
    ('#586f7c', '#64748B'),
    ('#586F7C', '#64748B'),
    ('#f8fafc', '#F2F6FC'),
    ('#F8FAFC', '#F2F6FC'),
    ('#e2e8f0', '#E5EAF2'),
    ('#E2E8F0', '#E5EAF2'),
    ('#0f172a', '#243247'),
    ('#0F172A', '#243247'),
    
    # Soft translucent greens to soft translucent blues
    ('rgba(30, 77, 56,', 'rgba(36, 85, 214,'),
    ('rgba(19, 130, 155,', 'rgba(36, 85, 214,'),
    ('rgba(16, 185, 129,', 'rgba(36, 85, 214,'),
    ('rgba(47, 69, 80,', 'rgba(36, 50, 71,'),
    ('rgba(184, 219, 217,', 'rgba(234, 242, 255,'),
]

def migrate_file(fpath):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig = content
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            
    # Also clean up any hover scaling / hover transforms if present in styles
    content = re.sub(r'transform:\s*(?:translateY\(-[1-9]px\)|scale\([1-9]\.[0-9]+\));?', 'transform: none !important;', content)
    
    if content != orig:
        with open(fpath, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(content)
        return True
    return False

if __name__ == '__main__':
    targets = sorted(
        glob.glob('pages/**/*.html', recursive=True) +
        glob.glob('assets/css/*.css') +
        ['index.html', 'pages-directory.html']
    )
    changed = 0
    for p in targets:
        if migrate_file(p):
            changed += 1
            print(f"Migrated colors in: {p}")
    print(f"Complete. Migrated {changed} of {len(targets)} files.")

