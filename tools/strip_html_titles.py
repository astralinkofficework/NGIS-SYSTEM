import os
import re

TAG_REGEX = re.compile(r'<([a-zA-Z0-9\-]+)(\s+[^>]*)>', re.DOTALL)
TITLE_ATTR_REGEX = re.compile(r'\btitle\s*=\s*(["\'])(.*?)\1', re.DOTALL | re.IGNORECASE)
DATA_TOOLTIP_REGEX = re.compile(r'\bdata-tooltip\s*=\s*(["\'])(.*?)\1', re.DOTALL | re.IGNORECASE)
DATA_TITLE_REGEX = re.compile(r'\bdata-title\s*=\s*(["\'])(.*?)\1', re.DOTALL | re.IGNORECASE)
ARIA_LABEL_REGEX = re.compile(r'\b(aria-label|aria-labelledby)\s*=', re.IGNORECASE)

INTERACTIVE_TAGS = {'button', 'a', 'input', 'select', 'textarea', 'svg'}

def process_file(path, dry_run=False):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        orig = f.read()

    # Split by script and style tags to avoid modifying JavaScript or CSS
    parts = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)', orig, flags=re.DOTALL | re.IGNORECASE)

    mod_count = 0
    aria_added = 0
    new_parts = []

    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            new_parts.append(part)
            continue

        def replace_tag(match):
            nonlocal mod_count, aria_added
            tag_name = match.group(1).lower()
            if tag_name in ['title', 'head', 'html']:
                return match.group(0)

            attrs = match.group(2)
            title_m = TITLE_ATTR_REGEX.search(attrs)
            dt_m = DATA_TOOLTIP_REGEX.search(attrs)
            dtitle_m = DATA_TITLE_REGEX.search(attrs)

            if not (title_m or dt_m or dtitle_m):
                return match.group(0)

            # Determine best label text for aria-label if missing
            fallback_text = ""
            if title_m:
                fallback_text = title_m.group(2).strip()
            elif dt_m:
                fallback_text = dt_m.group(2).strip()
            elif dtitle_m:
                fallback_text = dtitle_m.group(2).strip()

            has_aria = bool(ARIA_LABEL_REGEX.search(attrs))

            new_attrs = attrs
            # Remove title attribute
            if title_m:
                new_attrs = re.sub(r'\s+\btitle\s*=\s*(["\']).*?\1', '', new_attrs, count=1, flags=re.DOTALL | re.IGNORECASE)
                mod_count += 1

            # Remove data-tooltip attribute
            if dt_m:
                new_attrs = re.sub(r'\s+\bdata-tooltip\s*=\s*(["\']).*?\1', '', new_attrs, count=1, flags=re.DOTALL | re.IGNORECASE)
                mod_count += 1

            # Remove data-title attribute
            if dtitle_m:
                new_attrs = re.sub(r'\s+\bdata-title\s*=\s*(["\']).*?\1', '', new_attrs, count=1, flags=re.DOTALL | re.IGNORECASE)
                mod_count += 1

            # Ensure accessibility if missing
            if not has_aria and fallback_text and tag_name in INTERACTIVE_TAGS:
                clean_label = fallback_text.replace('"', '&quot;')
                new_attrs += f' aria-label="{clean_label}"'
                aria_added += 1

            return f"<{match.group(1)}{new_attrs}>"

        new_part = TAG_REGEX.sub(replace_tag, part)
        new_parts.append(new_part)

    new_content = "".join(new_parts)
    if mod_count > 0 and not dry_run:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return mod_count, aria_added

def run():
    html_files = []
    for root, dirs, files in os.walk('.'):
        if any(skip in root for skip in ['node_modules', '.git', '.gemini', '.system_generated']):
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    print(f"Scanning {len(html_files)} HTML files for tooltip cleanup...")

    total_mods = 0
    total_aria = 0
    files_changed = 0

    for p in html_files:
        mods, arias = process_file(p, dry_run=False)
        if mods > 0:
            files_changed += 1
            total_mods += mods
            total_aria += arias

    print(f"COMPLETE: Updated {files_changed} files.")
    print(f"Stripped {total_mods} tooltip attributes (title, data-tooltip, data-title).")
    print(f"Added {total_aria} aria-labels to preserve WCAG accessibility.")

if __name__ == '__main__':
    run()
