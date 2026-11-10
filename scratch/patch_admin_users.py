with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    content = f.read().replace('\r\n', '\n')

# 1. Fix pre-ticked consent checkboxes
content = content.replace(
    '<input type="checkbox" checked style="margin-top:3px">\n                <div>\n                  <div style="font-weight: 400">Access Student Directory</div>',
    '<input type="checkbox" style="margin-top:3px">\n                <div>\n                  <div style="font-weight: 400">Access Student Directory</div>'
)

content = content.replace(
    '<input type="checkbox" checked style="margin-top:3px">\n                <div>\n                  <div style="font-weight: 400">Access Academic Configuration</div>',
    '<input type="checkbox" style="margin-top:3px">\n                <div>\n                  <div style="font-weight: 400">Access Academic Configuration</div>'
)

# 2. Fix triggerDeleteUser confirm() with honest NGISCancelDialog
old_delete = '''      const confirmDelete = confirm(`Are you sure you want to permanently delete the account of ${user.name} (${user.id})? This action is irreversible.`);
      if (confirmDelete) {
        state.users = state.users.filter(u => u.id !== uid);
        state.selectedIds.delete(uid);
        window.toast(`Account successfully deleted for ${user.name}`, "error");
        
        // If in profile view of this user, return to list
        if (state.profileUserId === uid) {
          navigateTo("students");
        } else {
          filterAndRenderUsers();
          renderStats();
        }
      }'''

new_delete = '''      const doDelete = () => {
        state.users = state.users.filter(u => u.id !== uid);
        state.selectedIds.delete(uid);
        window.toast(`Account successfully deleted for ${user.name}`, "error");
        if (state.profileUserId === uid) {
          navigateTo("students");
        } else {
          filterAndRenderUsers();
          renderStats();
        }
      };

      if (window.NGISCancelDialog) {
        window.NGISCancelDialog.open({
          title: `Delete Account: ${user.name}`,
          description: `You are about to remove user ${user.name} (${user.id}).`,
          consequence: "Account credentials and portal access will be revoked immediately. Historical grade rosters and attendance records remain safely archived in institutional storage.",
          confirmLabel: "Delete Account",
          cancelLabel: "Keep Account",
          isDestructive: true,
          onConfirm: doDelete
        });
      } else if (confirm(`Delete account for ${user.name} (${user.id})?`)) {
        doDelete();
      }'''

if old_delete in content:
    content = content.replace(old_delete, new_delete)
    print("triggerDeleteUser patched")
else:
    print("old_delete NOT found")

# 3. Fix bulk delete confirm()
old_bulk = '''        const confirmDelete = confirm(`Are you sure you want to permanently delete ${state.selectedIds.size} selected accounts? This is a bulk administrative operation.`);
        if (confirmDelete) {
          const selectedArr = Array.from(state.selectedIds);
          state.users = state.users.filter(u => !selectedArr.includes(u.id));
          window.toast(`Bulk deleted ${selectedArr.length} user records`, "error");
          clearBulkSelection();
          filterAndRenderUsers();
          renderStats();
        }'''

new_bulk = '''        const doBulkDelete = () => {
          const selectedArr = Array.from(state.selectedIds);
          state.users = state.users.filter(u => !selectedArr.includes(u.id));
          window.toast(`Bulk deleted ${selectedArr.length} user records`, "error");
          clearBulkSelection();
          filterAndRenderUsers();
          renderStats();
        };

        if (window.NGISCancelDialog) {
          window.NGISCancelDialog.open({
            title: `Delete ${state.selectedIds.size} Selected Accounts`,
            description: `You have selected ${state.selectedIds.size} user accounts for permanent removal.`,
            consequence: "Selected users will be deregistered. Historical records remain preserved in administrative compliance archives.",
            confirmLabel: `Delete ${state.selectedIds.size} Accounts`,
            cancelLabel: "Cancel",
            isDestructive: true,
            onConfirm: doBulkDelete
          });
        } else if (confirm(`Delete ${state.selectedIds.size} accounts?`)) {
          doBulkDelete();
        }'''

if old_bulk in content:
    content = content.replace(old_bulk, new_bulk)
    print("bulkDelete patched")
else:
    print("old_bulk NOT found")

with open('pages/admin/admin-users.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Finished updating admin-users.html")

