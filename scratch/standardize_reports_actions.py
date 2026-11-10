with open('pages/principal/principal-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Standardize authorize rows:
pattern_auth = r'<td class="py-2\.5 pr-4 pl-3 align-middle text-right whitespace-nowrap"><div class="inline-flex items-center gap-1\.5"><button type="button" class="btn-authorize[^"]*"[^>]*>Authorize</button><button type="button" class="p-1[^"]*" title="Inspect Full Gradebook"[^>]*><span data-ngis-icon="list" class="text-\[16px\]"></span></button></div></td>'

repl_auth = '''<td class="py-2.5 pr-4 pl-3 align-middle text-right whitespace-nowrap table-actions">
                  <div class="action-group">
                    <button type="button" class="btn-authorize action-btn-pill primary" title="Authorize Gradebook">
                      <span data-ngis-icon="check"></span>
                      <span>Authorize</span>
                    </button>
                    <button type="button" class="action-icon-btn" title="Inspect Full Gradebook" aria-label="Inspect Full Gradebook">
                      <span data-ngis-icon="list"></span>
                    </button>
                  </div>
                </td>'''

text, n_auth = re.subn(pattern_auth, repl_auth, text)
print(f"Replaced {n_auth} authorize actions in principal-reports.html")

# Standardize review rows:
pattern_rev = r'<td class="py-2\.5 pr-4 pl-3 align-middle text-right whitespace-nowrap"><div class="inline-flex items-center gap-1\.5"><button type="button" class="btn-review[^"]*"[^>]*>Review</button><button type="button" class="p-1[^"]*" title="Request Modification"[^>]*><span data-ngis-icon="edit" class="text-\[16px\]"></span></button></div></td>'

repl_rev = '''<td class="py-2.5 pr-4 pl-3 align-middle text-right whitespace-nowrap table-actions">
                  <div class="action-group">
                    <button type="button" class="btn-review action-btn-pill" title="Review Gradebook">
                      <span data-ngis-icon="view"></span>
                      <span>Review</span>
                    </button>
                    <button type="button" class="action-icon-btn" title="Request Modification" aria-label="Request Modification">
                      <span data-ngis-icon="edit"></span>
                    </button>
                  </div>
                </td>'''

text, n_rev = re.subn(pattern_rev, repl_rev, text)
print(f"Replaced {n_rev} review actions in principal-reports.html")

with open('pages/principal/principal-reports.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved principal-reports.html")

