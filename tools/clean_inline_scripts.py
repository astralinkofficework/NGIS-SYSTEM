import os
import re

TAG_IN_JS_REGEX = re.compile(r'(<[a-zA-Z0-9\-]+[^>]*?\b)title\s*=\s*(["\']|\\+["\'])(.*?)\2([^>]*?>)', re.IGNORECASE)

def clean_script_templates(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Find script blocks
    parts = re.split(r'(<script\b[^>]*>.*?</script>)', content, flags=re.DOTALL | re.IGNORECASE)
    mod_count = 0

    new_parts = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            # Inside script
            def replace_tag_in_code(m):
                nonlocal mod_count
                prefix = m.group(1)
                quote = m.group(2)
                title_val = m.group(3)
                suffix = m.group(4)

                # Skip document.title or variable assignments
                if prefix.endswith('.'):
                    return m.group(0)

                mod_count += 1
                # Check if prefix or suffix already has aria-label
                has_aria = 'aria-label' in prefix or 'aria-label' in suffix
                aria_insert = ''
                if not has_aria and title_val and not title_val.startswith('$'):
                    # if quote is escaped e.g. \"
                    if quote.startswith('\\'):
                        aria_insert = f' aria-label=\\"{title_val}\\"'
                    else:
                        aria_insert = f' aria-label="{title_val}"'

                return f"{prefix}{aria_insert}{suffix}"

            # Replace HTML title attributes inside string templates
            # We look for pattern: <button ... title="..." or <a ... title="..."
            cleaned_script = re.sub(
                r'(<(?:button|a|input|select|span|div)\b[^>]*?)\s+title\s*=\s*(\\?["\'])(.*?)\2([^>]*?>)',
                replace_tag_in_code,
                part,
                flags=re.IGNORECASE
            )
            new_parts.append(cleaned_script)
        else:
            new_parts.append(part)

    if mod_count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("".join(new_parts))

    return mod_count

total_script_mods = 0
for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            c = clean_script_templates(p)
            if c > 0:
                total_script_mods += c
                print(f"Cleaned {c} template titles in {p}")

print(f"Total template titles cleaned: {total_script_mods}")
