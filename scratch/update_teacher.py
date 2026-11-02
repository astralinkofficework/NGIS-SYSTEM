with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update grid columns for upcoming card
content = content.replace(
    'grid-template-columns: 1fr 1fr 1.15fr !important;',
    'grid-template-columns: 0.95fr 0.95fr 1.25fr !important;'
)

# 2. Activity feed title
content = content.replace(
    '<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Faculty Activity Feed</span>',
    '<span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Activity Feed</span>'
)

# 3. Mobile view greeting color
content = content.replace(
    '<p class="text-[11px] text-[#000000]/90 font-medium tracking-wide">Good Day!</p>',
    '<p class="text-[11px] text-white/80 font-medium tracking-wide">Good Day!</p>'
)

with open('pages/teacher/teacher.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Teacher updated successfully")

