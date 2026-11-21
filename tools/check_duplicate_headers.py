import glob, re

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
duplicate_pages = []

for path in html_files:
    content = open(path, encoding='utf-8', errors='ignore').read()
    headers = re.findall(r'<header[^>]*>', content)
    # Filter out sr-only headers or modal headers
    page_headers = [h for h in headers if 'modal' not in h.lower() and 'sr-only' not in h.lower() and 'dialog' not in h.lower()]
    if len(page_headers) > 1:
        duplicate_pages.append((path, page_headers))

print(f"Pages with multiple headers: {len(duplicate_pages)}")
for p, hdrs in duplicate_pages[:20]:
    print(f"\n{p} ({len(hdrs)} headers):")
    for h in hdrs:
        print("  -", h[:80])
