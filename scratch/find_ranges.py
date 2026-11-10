with open('assets/js/ngis-profiles.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_range(start_pat, end_pat):
    s = None
    for i, line in enumerate(lines):
        if s is None and start_pat in line:
            s = i
        elif s is not None and end_pat in line:
            return s, i
    return s, len(lines)

print("renderShell:", find_range("function renderShell()", "function resetAllFilters()"))
print("wireShell:", find_range("function wireShell()", "function renderFilterOptions()"))
print("renderTable:", find_range("function renderTable()", "function renderPager()"))
print("mountModals:", find_range("function mountModals()", "function boot()"))

