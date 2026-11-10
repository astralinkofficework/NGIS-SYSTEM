import glob, re

for f in sorted(glob.glob('pages/**/*.html', recursive=True)):
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # look for search input inside flex-col md:flex-row or similar
    pattern = r'<div[^>]*class="[^"]*flex flex-col [^"]*flex-row[^"]*"[^>]*>[\s\S]{1,500}?<input[^>]*type="(?:text|search)"'
    matches = list(re.finditer(pattern, c))
    if matches:
        print(f"=== {f} ({len(matches)} matches) ===")
        for m in matches:
            line_no = c[:m.start()].count('\n') + 1
            first_line = m.group(0).split('\n')[0]
            print(f"  Line {line_no}: {first_line}")

