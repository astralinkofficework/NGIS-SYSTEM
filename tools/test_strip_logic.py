import os
import re

TAG_REGEX = re.compile(r'<([a-zA-Z0-9\-]+)(\s+[^>]*)>', re.DOTALL)
TITLE_ATTR_REGEX = re.compile(r'\btitle\s*=\s*(["\'])(.*?)\1', re.DOTALL | re.IGNORECASE)
ARIA_LABEL_REGEX = re.compile(r'\baria-label\s*=', re.IGNORECASE)

def clean_tag(match):
    tag_name = match.group(1).lower()
    # Skip head <title> (though that has no attributes usually)
    if tag_name in ['title', 'head', 'html']:
        return match.group(0)

    attrs = match.group(2)
    title_match = TITLE_ATTR_REGEX.search(attrs)
    if not title_match:
        return match.group(0)

    title_val = title_match.group(2).strip()
    quote = title_match.group(1)

    has_aria = bool(ARIA_LABEL_REGEX.search(attrs))

    # Remove the title attribute
    # Handle leading whitespace
    new_attrs = re.sub(r'\s+\btitle\s*=\s*(["\']).*?\1', '', attrs, count=1, flags=re.DOTALL | re.IGNORECASE)

    # If it didn't have aria-label and has a meaningful title, add aria-label
    if not has_aria and title_val and tag_name in ['button', 'a', 'input', 'select', 'textarea']:
        # Escape quotes if necessary
        safe_val = title_val.replace('"', '&quot;')
        new_attrs += f' aria-label="{safe_val}"'

    return f"<{match.group(1)}{new_attrs}>"

# Test on 3 files
test_files = [
    os.path.join('pages', 'principal', 'principal-dashboard.html'),
    os.path.join('pages', 'teacher', 'attendance-management.html'),
    os.path.join('pages', 'student', 'student-exams.html')
]

for p in test_files:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        orig = f.read()
    new_content = TAG_REGEX.sub(clean_tag, orig)
    print(f"File: {p}")
    print(f"  Orig size: {len(orig)}, New size: {len(new_content)}")
    orig_titles = len(TITLE_ATTR_REGEX.findall(re.sub(r'<title[^>]*>.*?</title>', '', orig, flags=re.IGNORECASE | re.DOTALL)))
    new_titles = len(TITLE_ATTR_REGEX.findall(re.sub(r'<title[^>]*>.*?</title>', '', new_content, flags=re.IGNORECASE | re.DOTALL)))
    print(f"  Titles before: {orig_titles}, Titles after: {new_titles}")
