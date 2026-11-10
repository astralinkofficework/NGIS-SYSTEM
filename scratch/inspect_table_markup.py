with open('pages/principal/principal-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

m = re.search(r'<div class="bg-white border border-slate-200/90 rounded-xl.*?</table>.*?</div>\s*<!-- Table Pagination', text, re.DOTALL)
if m:
    print("--- Table Container ---")
    print(m.group(0)[:800])

m_pag = re.search(r'<!-- Table Pagination.*?</div>\s*</div>\s*</div>', text, re.DOTALL)
if m_pag:
    print("--- Pagination Container ---")
    print(m_pag.group(0)[:800])

