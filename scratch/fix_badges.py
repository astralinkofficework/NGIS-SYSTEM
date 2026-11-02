with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200/80 dark:border-slate-700" id="wsHomeroomBadge">

              <span class="material-symbols-outlined text-[15px] text-slate-500 dark:text-slate-400">home</span>

              <span id="wsHomeroomBadgeText">Homeroom · Room 302</span>

            </span>

            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-[#F3F3F5] dark:bg-[#202F63]/60 text-[#000000] dark:text-[#000000] border border-[#E5E5E8]/80 dark:border-[#E5E5E8]/80">

              <span class="w-1.5 h-1.5 rounded-full bg-[#202F63] animate-pulse"></span>

              Active Term

            </span>'''

replacement = '''            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-white text-slate-700 border border-[#E5E5E8]" id="wsHomeroomBadge">

              <span class="material-symbols-outlined text-[15px] text-[#202F63]">home</span>

              <span id="wsHomeroomBadgeText">Homeroom · Room 302</span>

            </span>

            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-white text-[#202F63] border border-[#E5E5E8]">

              <span class="w-1.5 h-1.5 rounded-full bg-[#202F63] animate-pulse"></span>

              Active Term

            </span>'''

text_norm = text.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')

if target_norm in text_norm:
    text_norm = text_norm.replace(target_norm, replacement.replace('\r\n', '\n'), 1)
    with open('pages/teacher/teacher-classes.html', 'w', encoding='utf-8') as f:
        f.write(text_norm)
    print("SUCCESS: Updated badge styling in teacher-classes.html")
else:
    print("Target badges not found, checking alternatives...")

