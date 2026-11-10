with open('pages/admin/admin-departments.html', 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

# Replace alert in editDepartment & deleteDepartment
old_handlers = '''  // Global helper functions
  window.editDepartment = function(deptId) {
    if (window.toast) {
      window.toast(`Opening editor for ${deptId.toUpperCase()} Department...`, 'info');
    } else {
      alert(`Edit Department: ${deptId}`);
    }
  };

  window.deleteDepartment = function(deptId) {
    if (window.toast) {
      window.toast(`Cannot archive ${deptId} — active curriculum and students exist`, 'error');
    } else {
      alert(`Cannot archive ${deptId}: Department currently has active faculty and enrolled students.`);
    }
  };'''

new_handlers = '''  // Global helper functions (Rules 2 & 5 Compliant)
  window.editDepartment = function(deptId) {
    if (window.toast) {
      window.toast(`Opening editor for ${deptId.toUpperCase()} Department...`, 'info');
    }
  };

  window.deleteDepartment = function(deptId) {
    if (window.NGISCancelDialog) {
      window.NGISCancelDialog.open({
        title: `Archive Department: ${deptId.toUpperCase()}`,
        description: `Verify that all semester syllabi and student grades have been concluded before archiving.`,
        consequence: `Curriculum records and faculty assignments will be safely preserved in institutional compliance archives.`,
        confirmLabel: "Archive Division",
        cancelLabel: "Keep Active",
        isDestructive: true,
        onConfirm: () => {
          if (window.toast) {
            window.toast(`Cannot archive ${deptId} — active faculty and students currently assigned`, 'warning');
          }
        }
      });
    } else if (window.toast) {
      window.toast(`Cannot archive ${deptId} — active curriculum and students exist`, 'warning');
    }
  };'''

if old_handlers in c:
    c = c.replace(old_handlers, new_handlers)
    print("edit/deleteDepartment patched")
else:
    print("old_handlers NOT found")

# Remove hover:shadow-md and hover:shadow-xl
c = c.replace('hover:shadow-md', 'hover:border-slate-300')
c = c.replace('hover:shadow-xl', 'hover:border-slate-300')
c = c.replace('shadow-md shadow-brand-700/25', '')

with open('pages/admin/admin-departments.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("Finished updating admin-departments.html")

