import re

content = open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8').read()
# Find viewerHtml section
start = content.find('function viewerHtml()')
end = content.find('function attachViewerInteractions()')
viewer_code = content[start:end]

bold_patterns = [
    r'\bfont-bold\b',
    r'\bfont-semibold\b',
    r'\bfont-extrabold\b',
    r'\bfont-black\b',
    r'font-weight\s*:\s*[6-9]\d\d'
]

for pat in bold_patterns:
    matches = re.findall(pat, viewer_code)
    if matches:
        print(f"Match found for {pat}: {len(matches)}")
print("viewerHtml bold scan finished.")

