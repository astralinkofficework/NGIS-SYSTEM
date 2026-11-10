import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

CANONICAL_LINK = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'

def update_html_fonts(content):
    # Pattern for text Google Font links (not Material Symbols / Icons)
    font_link_pattern = re.compile(
        r'<link[^>]*fonts\.googleapis\.com/css2\?family=(?!Material)[^>]*>\s*',
        re.IGNORECASE
    )

    matches = list(font_link_pattern.finditer(content))
    if not matches:
        return content, False

    # Replace the first match with CANONICAL_LINK, and remove any subsequent matches (deduplication)
    new_content = ""
    last_end = 0
    for idx, m in enumerate(matches):
        new_content += content[last_end:m.start()]
        if idx == 0:
            new_content += CANONICAL_LINK + "\n"
        last_end = m.end()
    new_content += content[last_end:]

    # Remove any stray JetBrains Mono or Inter font links if present as separate tags
    new_content = re.sub(
        r'<link[^>]*fonts\.googleapis\.com/css2\?[^>]*JetBrains[^>]*>\s*',
        '',
        new_content,
        flags=re.IGNORECASE
    )

    # Clean Tailwind fontFamily declarations: replace 'Inter' with 'Plus Jakarta Sans'
    # and replace JetBrains Mono with monospace or Plus Jakarta Sans
    new_content = new_content.replace("'Inter'", "'Plus Jakarta Sans'")
    new_content = new_content.replace('"Inter"', '"Plus Jakarta Sans"')
    new_content = new_content.replace("'JetBrains Mono'", "'Plus Jakarta Sans'")
    new_content = new_content.replace('"JetBrains Mono"', '"Plus Jakarta Sans"')

    # Clean inline font-family overrides for Inter
    new_content = re.sub(r'font-family:\s*[\'"]?Inter[\'"]?[^;"]*;?', "font-family: 'Plus Jakarta Sans', sans-serif;", new_content)

    return new_content, True

updated_files = []
for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            orig = f.read()
        
        updated, changed = update_html_fonts(orig)
        if changed and updated != orig:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(updated)
            updated_files.append(path)
    except Exception as e:
        print(f'Error processing {path}: {e}')

print(f'Updated typography in {len(updated_files)} HTML files.')

