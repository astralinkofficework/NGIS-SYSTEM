file_path = 'pages/admin/admin-classes.html'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """          <div class="flex items-center justify-end gap-1.5">
            <button class="p-1 rounded-lg hover:bg-slate-100 text-slate-500 hover:text-[#0F5132] btn-edit-class transition-colors" data-code="${esc(c.code)}" aria-label="Edit class ${esc(c.code)}" title="Edit Section" type="button">
              <span class="material-symbols-outlined text-lg">edit</span>
            </button>
            <button class="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-700 btn-more-class transition-colors" data-code="${esc(c.code)}" aria-label="More options for ${esc(c.code)}" title="More options" type="button">
              <span class="material-symbols-outlined text-lg">more_vert</span>
            </button>
          </div>"""

replacement = """          <div class="flex items-center justify-end gap-1.5 relative">
            <button class="p-1 rounded-lg hover:bg-slate-100 text-slate-500 hover:text-[#0F5132] btn-edit-class transition-colors cursor-pointer" data-code="${esc(c.code)}" aria-label="Edit class ${esc(c.code)}" title="Edit Section" type="button">
              <span class="material-symbols-outlined text-lg">edit</span>
            </button>
            <div class="relative inline-block text-left class-menu-wrapper">
              <button class="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-700 btn-more-class transition-colors cursor-pointer" data-code="${esc(c.code)}" aria-label="More options for ${esc(c.code)}" title="More options" type="button">
                <span class="material-symbols-outlined text-lg">more_vert</span>
              </button>
              <div class="class-action-menu hidden absolute right-0 mt-1 w-44 bg-white rounded-xl shadow-lg border border-slate-200/90 py-1 z-30 text-left text-xs font-normal text-slate-700">
                <a href="admin-timetables.html?class=${encodeURIComponent(c.code)}" class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 transition-colors">
                  <span class="material-symbols-outlined text-[15px] text-slate-500">calendar_view_week</span>
                  <span>View Timetable</span>
                </a>
                <a href="admin-users-students.html?class=${encodeURIComponent(c.code)}" class="flex items-center gap-2 px-3 py-2 hover:bg-slate-50 transition-colors">
                  <span class="material-symbols-outlined text-[15px] text-slate-500">group</span>
                  <span>Student Roster</span>
                </a>
                <button type="button" class="btn-menu-edit w-full flex items-center gap-2 px-3 py-2 hover:bg-slate-50 transition-colors text-left cursor-pointer" data-code="${esc(c.code)}">
                  <span class="material-symbols-outlined text-[15px] text-slate-500">edit</span>
                  <span>Edit Section</span>
                </button>
                <div class="my-1 border-t border-slate-100"></div>
                <button type="button" class="btn-menu-delete w-full flex items-center gap-2 px-3 py-2 hover:bg-rose-50 text-rose-600 transition-colors text-left cursor-pointer" data-code="${esc(c.code)}">
                  <span class="material-symbols-outlined text-[15px] text-rose-500">delete</span>
                  <span>Delete Section</span>
                </button>
              </div>
            </div>
          </div>"""

if target in code:
    code = code.replace(target, replacement, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully replaced row action buttons!")
else:
    print("Target not found.")
