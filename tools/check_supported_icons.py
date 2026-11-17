import re

with open('assets/js/action-icons.js', 'r', encoding='utf-8') as f:
    c = f.read()

icons_to_check = [
    'dashboard', 'group', 'school', 'badge', 'support_agent', 'account_balance',
    'admin_panel_settings', 'co_present', 'assignment_ind', 'verified_user',
    'person', 'verified', 'group_add', 'fact_check', 'bar_chart', 'menu_book',
    'apartment', 'location_city', 'calendar_view_week', 'assignment', 'inventory_2',
    'assessment', 'dashboard_customize', 'campaign', 'newspaper', 'settings',
    'domain', 'calendar_month', 'tune', 'date_range', 'view_week', 'view_quilt',
    'history', 'security', 'home', 'how_to_reg', 'grading', 'description',
    'local_activity', 'grid_view', 'business_center'
]

print("Checking icon support in action-icons.js:")
supported = []
missing = []
for ic in icons_to_check:
    # check if ic is in PATHS or ALIASES
    if f'"{ic}":' in c or f"'{ic}':" in c or f'{ic}:' in c:
        supported.append(ic)
    else:
        missing.append(ic)

print(f"Supported ({len(supported)}):", supported)
print(f"Missing ({len(missing)}):", missing)
