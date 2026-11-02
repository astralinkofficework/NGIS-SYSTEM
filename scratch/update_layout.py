with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = """        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[
          { id:"announcements", label:"Class Announcements",      icon:"campaign",      href:"pages/teacher/teacher-announcements.html" },
        ]},"""

replacement = """        { id:"communication", label:"COMMUNICATION", icon:"campaign", links:[
          { id:"announcements", label:"Class Announcements",      icon:"campaign",      href:"pages/teacher/teacher-announcements.html" },
        ]},
        { id:"campus-services", label:"CAMPUS & SERVICES", icon:"local_activity", links:[
          { id:"services",       label:"Faculty Services Hub",      icon:"grid_view",     href:"pages/teacher/teacher-services.html" },
          { id:"lost-found",     label:"Lost & Found",              icon:"inventory_2",   href:"pages/teacher/teacher-lost-found.html" },
        ]},"""

content_norm = content.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')

if target_norm in content_norm:
    content_norm = content_norm.replace(target_norm, replacement.replace('\r\n', '\n'), 1)
    # Also update side-foot-help for teacher:
    old_help = "role === 'teacher' ? 'pages/teacher/teacher-profile.html?tab=help'"
    new_help = "role === 'teacher' ? 'pages/teacher/teacher-services.html'"
    content_norm = content_norm.replace(old_help, new_help)

    with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
        f.write(content_norm.replace('\n', '\r\n'))
    print("SUCCESS: Updated assets/js/layout.js with teacher campus services!")
else:
    print("ERROR: Target not found in layout.js")

