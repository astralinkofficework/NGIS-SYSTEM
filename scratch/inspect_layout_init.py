with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = re.findall(r'heroBanner', c)
print('heroBanner in layout.js:', len(matches))
init_fn = re.findall(r'function initLayout[\s\S]*?(?:function|\Z)', c)
if init_fn:
    print('initLayout:', init_fn[0][:800])

