with open('pages/admin/admin-classes.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
for i, l in enumerate(lines):
    if '<!-- Card: Administrator Notice banner -->' in l:
        start_idx = i
        break

end_idx = None
for j in range(start_idx, len(lines)):
    if '</div>' in lines[j] and '</div>' in lines[j+1] and '</div>' in lines[j+2]:
        end_idx = j + 3
        break

print(f"Replacing lines {start_idx} to {end_idx}")

new_lines = [
    '          <!-- Card: Administrator Notice banner (Rules V2, V3, V4 Compliant) -->\n',
    '          <div class="p-5 rounded-2xl bg-white border border-[#E5E5E8] relative">\n',
    '            <div>\n',
    '              <div class="flex items-center gap-2 text-xs font-medium text-[#202F63] uppercase tracking-wider mb-2">\n',
    '                <span class="material-symbols-outlined text-sm">schedule</span>\n',
    '                <span>Term Schedule Notice</span>\n',
    '              </div>\n',
    '              <h4 class="font-medium text-sm text-[#000000]">Course Quota Finalization</h4>\n',
    '              <p class="text-xs text-[#555555] mt-1 leading-relaxed">\n',
    '                Add-drop period concludes in 5 business days. Please review senior cohort allocations before the registry deadline.\n',
    '              </p>\n',
    '              <div class="mt-4 flex items-center gap-2">\n',
    '                <a href="admin-timetables.html" class="inline-flex items-center gap-1 text-xs font-medium text-[#202F63] hover:underline transition-colors">\n',
    '                  <span>View Timetable Master</span>\n',
    '                  <span class="material-symbols-outlined text-sm">arrow_forward</span>\n',
    '                </a>\n',
    '              </div>\n',
    '            </div>\n',
    '          </div>\n'
]

lines[start_idx:end_idx] = new_lines

with open('pages/admin/admin-classes.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated admin-classes.html")
