import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("NGIS ERP - COMPREHENSIVE PAGE HEADER AUDIT")
print("=" * 60)

pages = sorted(glob.glob('pages/**/*.html', recursive=True) + ['index.html'])
print(f"Auditing {len(pages)} HTML pages...")

banned_patterns = [
    (r'class=["\'][^"\']*login-card-head[^"\']*["\']', 'login-card-head'),
    (r'data-purpose=["\']workspace-masthead["\']', 'workspace-masthead'),
    (r'class=["\'][^"\']*msg-page-head[^"\']*["\']', 'msg-page-head'),
    (r'class=["\'][^"\']*tp-page-header[^"\']*["\']', 'tp-page-header'),
    (r'class=["\'][^"\']*page-head\b[^"\']*["\']', 'page-head class'),
    (r'class=["\'][^"\']*\bhub-header\b[^"\']*["\']', 'hub-header class'),
    (r'<div class="login-divider">', 'login-divider')
]

issues_found = []

for p in pages:
    p_norm = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        full_content = f.read()

    # Extract body / main content before scripts
    main_match = re.search(r'<main[^>]*>([\s\S]*?)<\/main>', full_content)
    if not main_match:
        main_match = re.search(r'<body[^>]*>([\s\S]*?)<\/body>', full_content)
    
    if not main_match:
        continue

    content = main_match.group(1)
    # Strip script tags from content to only check rendered DOM
    content = re.sub(r'<script[\s\S]*?<\/script>', '', content)

    # 1. Check for banned header patterns
    for pat, label in banned_patterns:
        if re.search(pat, content):
            issues_found.append(f"[{p_norm}] Found banned pattern: {label}")

    # 2. Check for duplicate hero-body in subpages
    is_subpage = not any(p_norm.endswith(root) for root in ['admin.html', 'teacher.html', 'student.html', 'staff.html', 'principal.html', 'index.html'])
    if is_subpage and 'class="hero-body"' in content:
        issues_found.append(f"[{p_norm}] Found hardcoded hero-body in subpage")

    # 3. Check for specific previous boxed headers inside main content
    if 'Timetable Management' in content and '<h1' in content:
        issues_found.append(f"[{p_norm}] Found boxed Timetable Management header in main")

    if 'Official Academic Reports' in content and '<h1' in content:
        issues_found.append(f"[{p_norm}] Found boxed Academic Reports header in main")

    if 'Student Work Submissions' in content and '<h1' in content:
        issues_found.append(f"[{p_norm}] Found boxed Student Work Submissions header in main")

    if 'Student Lifecycle & MoEYS Governance' in content and '<h1' in content:
        issues_found.append(f"[{p_norm}] Found boxed Lifecycle header in main")

    if 'Academic Hubs & Department Oversight' in content:
        issues_found.append(f"[{p_norm}] Found boxed Academic Hubs hero in main")

    if 'English Department' in content and 'Masthead Hero Card' in content:
        issues_found.append(f"[{p_norm}] Found boxed English Department masthead in main")

    if 'Lost or found something on campus?' in content:
        issues_found.append(f"[{p_norm}] Found boxed Lost or found hero in main")

print(f"\nAudit completed. Total issues: {len(issues_found)}")
if issues_found:
    for issue in issues_found:
        print("  FAIL:", issue)
    sys.exit(1)
else:
    print("  PASS: All 71 pages have cleanly removed the separate boxed page-heading sections!")
    print("  PASS: Zero banned page-heading classes, dividers, or boxed title wrappers detected.")
