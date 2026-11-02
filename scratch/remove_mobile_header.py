import os

path = r'pages/teacher/teacher-classes.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = '<!-- BEGIN: MobileAppHeader -->'
end_marker = '<!-- END: Top Utility & Brand Bar -->'

idx1 = text.find(start_marker)
idx2 = text.find(end_marker)

if idx1 != -1 and idx2 != -1:
    # Also check if comment precedes start_marker
    comment_marker = '<!-- ═══════════════════════════════════════════════════════════════════\n\n     MANDATORY MOBILE HAMBURGER APP BAR'
    c_idx = text.rfind('<!-- ═══', 0, idx1)
    if c_idx != -1 and c_idx > idx1 - 300:
        cut_start = c_idx
    else:
        cut_start = idx1
    cut_end = idx2 + len(end_marker)
    
    # Remove block
    new_text = text[:cut_start].rstrip() + '\n\n' + text[cut_end:].lstrip()
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(new_text)
    print("Successfully removed mobile header block from pages/teacher/teacher-classes.html")
else:
    print("Markers not found!")

