with open('pages/principal/principal-timetables.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Standardize cohort rows action cell:
pattern = r'<td class="py-3\.5 px-6 text-right font-sans">\s*<div class="inline-flex items-center gap-1\.5">\s*<button onclick="openUploadModal\(([^)]+)\)"[^>]*>[\s\S]*?Upload[\s\S]*?</button>\s*<button onclick="toggleScheduleRow\(([^)]+)\)"[^>]*>[\s\S]*?View Timetable[\s\S]*?</button>\s*</div>\s*</td>'

def repl(m):
    c1 = m.group(1)
    c2 = m.group(2)
    return f'''<td class="py-3.5 px-6 text-right font-sans table-actions">
                <div class="action-group">
                  <button type="button" onclick="openUploadModal({c1})" class="action-btn-pill" title="Upload Timetable">
                    <span data-ngis-icon="upload"></span>
                    <span>Upload</span>
                  </button>
                  <button type="button" onclick="toggleScheduleRow({c2})" class="action-btn-pill primary" title="View Schedule">
                    <span data-ngis-icon="view"></span>
                    <span>View Schedule</span>
                  </button>
                </div>
              </td>'''

new_text, n = re.subn(pattern, repl, text)
print(f"Replaced {n} occurrences in principal-timetables.html")
if n > 0:
    with open('pages/principal/principal-timetables.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Saved principal-timetables.html")

