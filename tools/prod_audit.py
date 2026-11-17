import os
import glob
import re
import json

def normalize_path(p):
    return p.replace(os.sep, '/')

def run_discovery():
    html_files = [normalize_path(f) for f in glob.glob('**/*.html', recursive=True) if 'node_modules' not in f and not f.startswith(('.', 'tests'))]
    js_files = [normalize_path(f) for f in glob.glob('**/*.js', recursive=True) if 'node_modules' not in f and not f.startswith(('.', 'tests', 'timetable/node_modules'))]
    css_files = [normalize_path(f) for f in glob.glob('**/*.css', recursive=True) if 'node_modules' not in f and not f.startswith(('.', 'tests'))]

    print(f"=== INVENTORY SUMMARY ===")
    print(f"HTML Pages: {len(html_files)}")
    print(f"App JS:     {len(js_files)}")
    print(f"App CSS:    {len(css_files)}")

    # 1. Check broken local asset references (<link>, <script>, <img>)
    print("\n=== CHECKING ASSET REFERENCE INTEGRITY ===")
    broken_assets = []
    duplicate_tags = []
    hardcoded_urls = []
    xss_risks = []
    exposed_secrets = []

    for page in html_files:
        try:
            with open(page, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                page_dir = os.path.dirname(page)

                # Script tags
                scripts = re.findall(r'<script[^>]*src=[\"\']([^\"\']+)[\"\']', content)
                seen_scripts = set()
                for s in scripts:
                    clean_s = s.split('?')[0].split('#')[0]
                    if s in seen_scripts and not s.startswith(('http://', 'https://')):
                        duplicate_tags.append((page, 'script', s))
                    seen_scripts.add(s)

                    if not s.startswith(('http://', 'https://', '//', 'data:')):
                        # Resolve path
                        target = os.path.normpath(os.path.join(page_dir, clean_s))
                        if not os.path.exists(target):
                            broken_assets.append((page, 'script', s, normalize_path(target)))

                # Link tags (css)
                links = re.findall(r'<link[^>]*rel=[\"\']stylesheet[\"\'][^>]*href=[\"\']([^\"\']+)[\"\']', content)
                links += re.findall(r'<link[^>]*href=[\"\']([^\"\']+)[\"\'][^>]*rel=[\"\']stylesheet[\"\']', content)
                seen_links = set()
                for l in links:
                    clean_l = l.split('?')[0].split('#')[0]
                    if l in seen_links and not l.startswith(('http://', 'https://')):
                        duplicate_tags.append((page, 'link', l))
                    seen_links.add(l)

                    if not l.startswith(('http://', 'https://', '//', 'data:')):
                        target = os.path.normpath(os.path.join(page_dir, clean_l))
                        if not os.path.exists(target):
                            broken_assets.append((page, 'stylesheet', l, normalize_path(target)))

                # Img tags
                imgs = re.findall(r'<img[^>]*src=[\"\']([^\"\']+)[\"\']', content)
                for img in imgs:
                    clean_img = img.split('?')[0].split('#')[0]
                    if not img.startswith(('http://', 'https://', '//', 'data:')):
                        target = os.path.normpath(os.path.join(page_dir, clean_img))
                        if not os.path.exists(target):
                            broken_assets.append((page, 'image', img, normalize_path(target)))

                # Check hardcoded URLs
                matches_url = re.findall(r'(https?://(?:localhost|127\.0\.0\.1)(?::\d+)?/[^\s\"\'\<\>]*)', content)
                for u in matches_url:
                    hardcoded_urls.append((page, u))

        except Exception as e:
            print(f"Error reading {page}: {e}")

    # Check JS files for hardcoded localhost URLs, dangerous innerHTML, and exposed secrets
    print("\n=== CHECKING JS CODE QUALITY & SECURITY ===")
    for js in js_files:
        try:
            with open(js, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Hardcoded URLs
                matches_url = re.findall(r'(https?://(?:localhost|127\.0\.0\.1)(?::\d+)?/[^\s\"\'\<\>]*)', content)
                for u in matches_url:
                    hardcoded_urls.append((js, u))

                # Potential secrets (tokens, api keys, private keys)
                secrets = re.findall(r'(?:api[_-]?key|secret|password|bearer|auth[_-]?token)\s*[:=]\s*[\"\']([A-Za-z0-9_\-\.]{16,})[\"\']', content, re.IGNORECASE)
                for s in secrets:
                    if 'example' not in s.lower() and 'dummy' not in s.lower() and 'placeholder' not in s.lower() and 'fake-jwt' not in s:
                        exposed_secrets.append((js, s[:6] + '...'))

                # DOM XSS via unescaped search params
                if 'location.search' in content and 'innerHTML' in content:
                    xss_risks.append(js)

        except Exception as e:
            print(f"Error reading {js}: {e}")

    print(f"Broken asset references found: {len(broken_assets)}")
    for page, kind, ref, target in broken_assets[:20]:
        print(f"  [404] {page} -> {kind}: '{ref}' (resolved to: {target})")
    if len(broken_assets) > 20:
        print(f"  ... and {len(broken_assets) - 20} more broken assets")

    print(f"\nDuplicate script/link tags: {len(duplicate_tags)}")
    for page, kind, ref in duplicate_tags[:10]:
        print(f"  [DUP] {page} has duplicate {kind}: '{ref}'")

    print(f"\nHardcoded localhost URLs: {len(hardcoded_urls)}")
    for file, url in hardcoded_urls[:15]:
        print(f"  [URL] {file}: {url}")

    print(f"\nExposed potential secrets: {len(exposed_secrets)}")
    for file, secret in exposed_secrets:
        print(f"  [SECRET] {file}: {secret}")

    print(f"\nXSS Risk files (location.search + innerHTML): {len(xss_risks)}")
    for f in xss_risks:
        print(f"  [XSS] {f}")

    # Output full details to JSON
    results = {
        "html_count": len(html_files),
        "js_count": len(js_files),
        "css_count": len(css_files),
        "broken_assets": broken_assets,
        "duplicate_tags": duplicate_tags,
        "hardcoded_urls": hardcoded_urls,
        "exposed_secrets": exposed_secrets,
        "xss_risks": xss_risks
    }
    with open('tools/discovery_audit_results.json', 'w', encoding='utf-8') as out:
        json.dump(results, out, indent=2)

if __name__ == '__main__':
    run_discovery()
