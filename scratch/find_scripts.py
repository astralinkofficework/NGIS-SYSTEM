with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script[^>]*src="([^"]+)"', text)
print("Scripts loaded:", scripts)

