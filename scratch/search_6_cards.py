import os
import re

for root, dirs, files in os.walk('pages'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fl:
                content = fl.read()
                if 'Lessons & Materials' in content or 'Tasks & Submissions' in content or 'Report Cards & Grades' in content:
                    print(f"Matched in {p}")

