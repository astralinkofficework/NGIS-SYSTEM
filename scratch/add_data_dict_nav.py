with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

dict_svg = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="9" cy="5" rx="6" ry="2.5"/><path d="M3 5v4c0 1.38 2.69 2.5 6 2.5 1.15 0 2.22-.14 3.12-.38"/><path d="M3 9v4c0 1.38 2.69 2.5 6 2.5 .88 0 1.72-.08 2.47-.23"/><path d="M3 13v4c0 1.38 2.69 2.5 6 2.5 .6 0 1.18-.04 1.72-.11"/><circle cx="16" cy="15" r="4"/><line x1="19" y1="18" x2="22" y2="21"/></svg>'

admin_dict_block = f"""        {{ id:"data-dict-grp", label:"DATA DICTIONARY", icon:"database", links:[
          {{
            id: "data-dictionary-drop",
            label: "Data Dictionary",
            icon: `{dict_svg}`,
            collapsible: true,
            children: [
              {{ id: "dict-school", label: "School Data", hasChevron: true, href: "pages/admin/admin-dictionary-school.html" }},
              {{ id: "dict-students", label: "Student's Data", hasChevron: true, href: "pages/admin/admin-dictionary-students.html" }},
              {{ id: "dict-teachers", label: "Teacher's Data", hasChevron: true, href: "pages/admin/admin-dictionary-teachers.html" }},
              {{ id: "dict-additional", label: "Additional Data", hasChevron: true, href: "pages/admin/admin-dictionary-additional.html" }},
              {{ id: "dict-timetable", label: "Timetable's Data", hasChevron: true, href: "pages/admin/admin-dictionary-timetable.html" }},
            ]
          }}
        ]}},
"""

prl_dict_block = f"""        {{ id: "data-dict-grp", label: "DATA DICTIONARY", icon: "database", links: [
          {{
            id: "data-dictionary-drop",
            label: "Data Dictionary",
            icon: `{dict_svg}`,
            collapsible: true,
            children: [
              {{ id: "dict-school", label: "School Data", hasChevron: true, href: "pages/principal/principal-dictionary-school.html" }},
              {{ id: "dict-students", label: "Student's Data", hasChevron: true, href: "pages/principal/principal-dictionary-students.html" }},
              {{ id: "dict-teachers", label: "Teacher's Data", hasChevron: true, href: "pages/principal/principal-dictionary-teachers.html" }},
              {{ id: "dict-additional", label: "Additional Data", hasChevron: true, href: "pages/principal/principal-dictionary-additional.html" }},
              {{ id: "dict-timetable", label: "Timetable's Data", hasChevron: true, href: "pages/principal/principal-dictionary-timetable.html" }},
            ]
          }}
        ]}},
"""

# In Admin, insert right after student-mgmt-drop inside USER MANAGEMENT or right after USER MANAGEMENT
target_admin = '        { id:"academic", label:"ACADEMIC STRUCTURE"'
assert target_admin in text, "target_admin not found"
text = text.replace(target_admin, admin_dict_block + '\n' + target_admin, 1)

# In Principal, insert right after student-mgmt-drop group
target_prl = '        { id: "decisions", label: "DECISIONS & NOTICES"'
assert target_prl in text, "target_prl not found"
text = text.replace(target_prl, prl_dict_block + '\n' + target_prl, 1)

with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(text)

with open('layout.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated layout.js and assets/js/layout.js successfully!")
