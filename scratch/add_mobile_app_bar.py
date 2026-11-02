# Update teacher-lost-found.html
with open('pages/teacher/teacher-lost-found.html', 'r', encoding='utf-8') as f:
    text_lf = f.read()

target_lf = '<main class="main w-full min-h-screen pb-16">'
mobile_bar_lf = '''<main class="main w-full min-h-screen pb-16">
    <!-- Mobile App Bar with Mandatory Hamburger Button (AGENTS.md) -->
    <header class="lg:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-[#E5E5E8] sticky top-0 z-30">
      <div class="flex items-center gap-3">
        <button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn w-10 h-10 rounded-xl bg-[#F3F3F5] border border-[#E5E5E8] text-[#202F63] flex items-center justify-center hover:bg-[#E5E5E8] active:scale-95 transition-all" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">
          <i class="ph ph-list text-xl"></i>
        </button>
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-[#202F63] text-xl">inventory_2</span>
          <span class="text-sm font-medium text-[#000000]">Lost &amp; Found Desk</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <a href="teacher.html" class="p-2 text-[#555555] hover:text-[#202F63] rounded-lg" title="Back to Home">
          <span class="material-symbols-outlined text-[20px]">home</span>
        </a>
      </div>
    </header>'''

if target_lf in text_lf:
    text_lf = text_lf.replace(target_lf, mobile_bar_lf, 1)
    with open('pages/teacher/teacher-lost-found.html', 'w', encoding='utf-8') as f:
        f.write(text_lf)
    print("SUCCESS: Added mobile header with hamburger to teacher-lost-found.html")

# Update teacher-services.html
with open('pages/teacher/teacher-services.html', 'r', encoding='utf-8') as f:
    text_srv = f.read()

target_srv = '<main class="main w-full min-h-screen pb-16">'
mobile_bar_srv = '''<main class="main w-full min-h-screen pb-16">
    <!-- Mobile App Bar with Mandatory Hamburger Button (AGENTS.md) -->
    <header class="lg:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-[#E5E5E8] sticky top-0 z-30">
      <div class="flex items-center gap-3">
        <button type="button" class="htb-hamburger hamburger-btn mobile-hamburger-btn w-10 h-10 rounded-xl bg-[#F3F3F5] border border-[#E5E5E8] text-[#202F63] flex items-center justify-center hover:bg-[#E5E5E8] active:scale-95 transition-all" data-action="toggle-sidebar" aria-label="Open menu" aria-expanded="false" title="Open navigation">
          <i class="ph ph-list text-xl"></i>
        </button>
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-[#202F63] text-xl">room_service</span>
          <span class="text-sm font-medium text-[#000000]">Faculty Services</span>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <a href="teacher.html" class="p-2 text-[#555555] hover:text-[#202F63] rounded-lg" title="Back to Home">
          <span class="material-symbols-outlined text-[20px]">home</span>
        </a>
      </div>
    </header>'''

if target_srv in text_srv:
    text_srv = text_srv.replace(target_srv, mobile_bar_srv, 1)
    with open('pages/teacher/teacher-services.html', 'w', encoding='utf-8') as f:
        f.write(text_srv)
    print("SUCCESS: Added mobile header with hamburger to teacher-services.html")

