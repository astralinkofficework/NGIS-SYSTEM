with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('border border-[#202F63] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#92243D]" type="button">\n          <svg class="w-3.5 h-3.5 text-[#000000]"',
              'border border-[#92243D] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#92243D]" type="button">\n          <svg class="w-3.5 h-3.5 text-white"')

c = c.replace('border border-[#202F63] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#92243D]" type="button">\r\n          <svg class="w-3.5 h-3.5 text-[#000000]"',
              'border border-[#92243D] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#92243D]" type="button">\r\n          <svg class="w-3.5 h-3.5 text-white"')

with open('pages/teacher/teacher-submissions.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated btnUploadAssignmentOrWork!')

