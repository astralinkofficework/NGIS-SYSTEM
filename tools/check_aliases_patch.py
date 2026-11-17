import re

with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    text = f.read()

aliases_to_add = {
    'co_present': 'teachers',
    'assignment_ind': 'user',
    'verified_user': 'shield',
    'verified': 'checkCircle',
    'group_add': 'users',
    'support_agent': 'user',
    'account_balance': 'bank',
    'fact_check': 'attendance',
    'bar_chart': 'report',
    'menu_book': 'book',
    'location_city': 'building',
    'apartment': 'building',
    'calendar_view_week': 'calendarWeek',
    'calendar_month': 'calendar',
    'date_range': 'calendar',
    'view_week': 'calendarWeek',
    'inventory_2': 'inventory',
    'dashboard_customize': 'dashboardCustom',
    'view_quilt': 'grid',
    'grid_view': 'grid',
    'local_activity': 'activity',
    'business_center': 'building',
    'how_to_reg': 'attendance',
    'tune': 'settings',
    'domain': 'building',
    'circle': 'record'
}

pos = text.find('var ALIASES = {')
print("ALIASES start:", pos)
# Let's see what's right after var ALIASES = {\n
insert_pos = text.find('\n', pos) + 1
print("Insert after:", text[pos:pos+60])

# Prepare lines to add
new_entries = []
for k, v in aliases_to_add.items():
    if f"'{k}':" not in text and f'"{k}":' not in text and f'{k}:' not in text:
        new_entries.append(f"    '{k}': '{v}',")

print(f"New alias entries to add ({len(new_entries)}):")
for e in new_entries:
    print(e)
