with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_str = 'w-10 h-10 rounded-full bg-white group-hover:bg-[#F3F3F5] border border-slate-200 group-hover:border-[#E5E5E8] flex items-center justify-center text-[#202F63] transition-colors shadow-sm'
new_str = 'w-10 h-10 rounded-full bg-[#F3F3F5] border border-slate-200 flex items-center justify-center text-[#202F63] shadow-sm'

if old_str in c:
    c = c.replace(old_str, new_str)
    print('Replaced in teacher-reports.html')

with open('pages/teacher/teacher-reports.html', 'w', encoding='utf-8') as f:
    f.write(c)

