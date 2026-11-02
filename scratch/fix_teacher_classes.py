import re

with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Neutralize .ws-card:hover style
old_css = """.ws-card:hover {

  transform: none !important;

  box-shadow: 0 10px 22px -6px rgba(1, 54, 35, 0.12), 0 2px 4px rgba(0, 0, 0, 0.04);

}"""

new_css = """.ws-card:hover,
.ws-card:active,
.ws-card:focus {
  transform: none !important;
  box-shadow: none !important;
  border-color: #E5E5E8 !important;
  background-color: inherit !important;
}"""

c = c.replace(old_css, new_css)

# 2. In .ws-card elements, remove hover:shadow-elevated hover:border-brand-600/30 dark:hover:border-brand-400/30
c = c.replace('hover:shadow-elevated hover:border-brand-600/30 dark:hover:border-brand-400/30', '')

# 3. In the icon container inside .ws-card, replace group-hover:bg-brand-600 group-hover:text-white
old_icon_cls = 'w-9 h-9 rounded-xl bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 group-hover:bg-brand-600 group-hover:text-white transition-colors flex items-center justify-center'
new_icon_cls = 'w-9 h-9 rounded-xl bg-[#F3F3F5] text-[#202F63] flex items-center justify-center'

count_icon = c.count(old_icon_cls)
c = c.replace(old_icon_cls, new_icon_cls)
print(f'Replaced {count_icon} icon badges in teacher-classes.html')

with open('pages/teacher/teacher-classes.html', 'w', encoding='utf-8') as f:
    f.write(c)

