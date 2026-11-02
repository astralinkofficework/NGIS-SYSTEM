with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Desktop Quick Actions
target_desktop = """        <a class="ql-item" href="teacher-profile.html">
          <div class="ql-icon-wrap" style="background:#F3F3F5"><span class="mi" style="color:#202F63">account_circle</span></div>
          <span class="ql-label">My Profile</span>
        </a>"""

replacement_desktop = """        <a class="ql-item" href="teacher-services.html">
          <div class="ql-icon-wrap" style="background:#F3F3F5"><span class="mi" style="color:#202F63">room_service</span></div>
          <span class="ql-label">Services Hub</span>
        </a>
        <a class="ql-item" href="teacher-lost-found.html">
          <div class="ql-icon-wrap" style="background:#F3F3F5"><span class="mi" style="color:#202F63">inventory_2</span></div>
          <span class="ql-label">Lost &amp; Found</span>
        </a>
        <a class="ql-item" href="teacher-profile.html">
          <div class="ql-icon-wrap" style="background:#F3F3F5"><span class="mi" style="color:#202F63">account_circle</span></div>
          <span class="ql-label">My Profile</span>
        </a>"""

# 2. Mobile Quick Actions
target_mobile = """          <!-- Classes -->
          <div onclick="window.location.href='teacher-classes.html'" class="flex flex-col items-center justify-center p-3 rounded-2xl bg-[#F3F3F5] hover:bg-[#E5E5E8] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-white/90 text-[#333333] flex items-center justify-center mb-1.5 shadow-xs">
              <i class="ph-bold ph-chalkboard-teacher text-lg"></i>
            </div>
            <span class="text-[11px] font-normal text-[#333333] text-center leading-tight">Classes</span>
          </div>
        </div>
      </section>"""

replacement_mobile = """          <!-- Classes -->
          <div onclick="window.location.href='teacher-classes.html'" class="flex flex-col items-center justify-center p-3 rounded-2xl bg-[#F3F3F5] hover:bg-[#E5E5E8] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-white/90 text-[#333333] flex items-center justify-center mb-1.5 shadow-xs">
              <i class="ph-bold ph-chalkboard-teacher text-lg"></i>
            </div>
            <span class="text-[11px] font-normal text-[#333333] text-center leading-tight">Classes</span>
          </div>
        </div>
      </section>

      <!-- Campus & Faculty Services -->
      <section data-purpose="faculty-services" class="mt-3">
        <h3 class="text-xs font-normal uppercase tracking-wider text-slate-600 mb-2 px-0.5">Faculty Services &amp; Campus</h3>
        <div class="grid grid-cols-2 gap-2.5">
          <div onclick="window.location.href='teacher-services.html'" class="flex items-center gap-2.5 p-3 rounded-2xl bg-white border border-slate-200/90 hover:bg-[#F3F3F5] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-[#F3F3F5] text-[#202F63] flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">room_service</span>
            </div>
            <div class="min-w-0">
              <p class="text-xs font-medium text-[#000000] leading-tight truncate">Services Hub</p>
              <p class="text-[10px] text-[#555555] truncate">IT, AV &amp; repairs</p>
            </div>
          </div>
          <div onclick="window.location.href='teacher-lost-found.html'" class="flex items-center gap-2.5 p-3 rounded-2xl bg-white border border-slate-200/90 hover:bg-[#F3F3F5] active:scale-95 transition-all cursor-pointer">
            <div class="w-9 h-9 rounded-xl bg-[#F3F3F5] text-[#202F63] flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[20px]">inventory_2</span>
            </div>
            <div class="min-w-0">
              <p class="text-xs font-medium text-[#000000] leading-tight truncate">Lost &amp; Found</p>
              <p class="text-[10px] text-[#555555] truncate">Classroom items</p>
            </div>
          </div>
        </div>
      </section>"""

text_norm = text.replace('\r\n', '\n')
target_desktop_norm = target_desktop.replace('\r\n', '\n')
target_mobile_norm = target_mobile.replace('\r\n', '\n')

updated = False
if target_desktop_norm in text_norm:
    text_norm = text_norm.replace(target_desktop_norm, replacement_desktop.replace('\r\n', '\n'), 1)
    updated = True
    print("Desktop quick actions updated!")
else:
    print("Target desktop not found!")

if target_mobile_norm in text_norm:
    text_norm = text_norm.replace(target_mobile_norm, replacement_mobile.replace('\r\n', '\n'), 1)
    updated = True
    print("Mobile quick actions updated!")
else:
    print("Target mobile not found!")

if updated:
    with open('pages/teacher/teacher.html', 'w', encoding='utf-8') as f:
        f.write(text_norm.replace('\n', '\r\n'))
    print("SUCCESS: Updated teacher.html!")
