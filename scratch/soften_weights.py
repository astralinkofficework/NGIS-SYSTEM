with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student.html', 'r', encoding='utf-8') as f:
    c = f.read()

# In student-mobile-view, replace font-bold and font-extrabold
start_marker = '<div class="student-mobile-view" id="studentMobileView">'
end_marker = '</div><!-- /.main -->'

start_idx = c.find(start_marker)
end_idx = c.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    mobile_part = c[start_idx:end_idx]
    # Replace extrabold and bold with normal or medium
    mobile_part = mobile_part.replace('font-extrabold', 'font-normal')
    mobile_part = mobile_part.replace('font-bold', 'font-normal')
    mobile_part = mobile_part.replace('font-semibold', 'font-normal')
    
    # Selectively keep font-medium for headings or primary names so they are not ultra-faint
    mobile_part = mobile_part.replace('<h2 class="text-base font-normal text-white', '<h2 class="text-base font-medium text-white')
    mobile_part = mobile_part.replace('<h4 class="text-xs font-normal text-slate-800', '<h4 class="text-xs font-medium text-slate-800')
    mobile_part = mobile_part.replace('<p class="text-xs font-normal text-slate-800 leading-tight">Classes Attended', '<p class="text-xs font-medium text-slate-800 leading-tight">Classes Attended')
    mobile_part = mobile_part.replace('<p class="text-xs font-normal text-slate-800 leading-tight">Next Class: Physics Lab', '<p class="text-xs font-medium text-slate-800 leading-tight">Next Class: Physics Lab')
    mobile_part = mobile_part.replace('text-white font-normal text-xs flex items-center justify-center gap-2 backdrop-blur-md', 'text-white font-medium text-xs flex items-center justify-center gap-2 backdrop-blur-md')
    
    c = c[:start_idx] + mobile_part + c[end_idx:]
    with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\pages\student\student.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Softened font weights in mobile view (NO BOLD)!")
else:
    print("Markers not found!")
