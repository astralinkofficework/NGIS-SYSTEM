import re

with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add getSubjectColor after initials()
target_initials = """  function initials(name) {
    var parts = String(name || '').trim().split(/\\s+/);
    return ((parts[0] || 'N')[0] + (parts.length > 1 ? parts[parts.length - 1][0] : '')).toUpperCase();
  }"""

replacement_initials = """  function initials(name) {
    var parts = String(name || '').trim().split(/\\s+/);
    return ((parts[0] || 'N')[0] + (parts.length > 1 ? parts[parts.length - 1][0] : '')).toUpperCase();
  }
  function getSubjectColor(subj) {
    var s = String(subj || '').toLowerCase();
    if (s.indexOf('khmer') !== -1) return '#d97706';
    if (s.indexOf('math') !== -1) return '#2563eb';
    if (s.indexOf('phys') !== -1) return '#7c3aed';
    if (s.indexOf('chem') !== -1) return '#db2777';
    if (s.indexOf('bio') !== -1) return '#059669';
    if (s.indexOf('hist') !== -1 || s.indexOf('geo') !== -1) return '#b45309';
    if (s.indexOf('eng') !== -1) return '#0284c7';
    if (s.indexOf('sport') !== -1 || s.indexOf('pe') !== -1) return '#dc2626';
    return '#176B45';
  }"""

if target_initials in text:
    text = text.replace(target_initials, replacement_initials, 1)
    print("1. Injected getSubjectColor")
else:
    print("WARNING: target_initials not found")

# 2. Update applyFilters to search more teacher fields and support target sorting
target_apply = """      var hay = IS_TEACHER
        ? [r.name, r.id, r.email, r.subject, r.department, r.role]
        : [r.name, r.id, r.grade, r.class, r.parentName, r.parentEmail, r.advisor];"""

replacement_apply = """      var hay = IS_TEACHER
        ? [r.name, r.id, r.email, r.subject, r.department, r.role, r.code, r.employee_id, r.specialization, r.notes]
        : [r.name, r.id, r.grade, r.class, r.parentName, r.parentEmail, r.advisor];"""

if target_apply in text:
    text = text.replace(target_apply, replacement_apply, 1)
    print("2. Injected applyFilters search fields")
else:
    print("WARNING: target_apply not found")

target_sort = """    rows.sort(function (a, b) {
      if (key === 'name') return String(a.name || '').localeCompare(String(b.name || '')) * (desc ? -1 : 1);
      var av = Number(a[key] || 0), bv = Number(b[key] || 0);
      return (bv - av) * (desc ? -1 : 1);
    });"""

replacement_sort = """    rows.sort(function (a, b) {
      if (key === 'name') return String(a.name || '').localeCompare(String(b.name || '')) * (desc ? -1 : 1);
      if (key === 'target') {
        var at = Number(a.target || (a.classesAssigned ? a.classesAssigned * 3 : 17));
        var bt = Number(b.target || (b.classesAssigned ? b.classesAssigned * 3 : 17));
        return (bt - at) * (desc ? -1 : 1);
      }
      var av = Number(a[key] || 0), bv = Number(b[key] || 0);
      return (bv - av) * (desc ? -1 : 1);
    });"""

if target_sort in text:
    text = text.replace(target_sort, replacement_sort, 1)
    print("3. Injected applyFilters sort logic")
else:
    print("WARNING: target_sort not found")

with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated initial sections")
