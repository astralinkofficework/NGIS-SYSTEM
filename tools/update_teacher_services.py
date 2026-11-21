with open('pages/teacher/teacher-services.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update openNewRequestModal and closeNewRequestModal
old_modals = '''    function openNewRequestModal() {
      const modal = document.getElementById('newRequestModal');
      if (modal) {
        modal.classList.add('show');
        handleCategoryChange(document.getElementById('reqCategory').value);
      }
    }

    function closeNewRequestModal() {
      const modal = document.getElementById('newRequestModal');
      if (modal) modal.classList.remove('show');
    }'''

new_modals = '''    function isNewRequestFormDirty() {
      const title = document.getElementById('reqTitle');
      const desc = document.getElementById('reqDesc');
      return (title && title.value.trim() !== '') || (desc && desc.value.trim() !== '');
    }

    function openNewRequestModal() {
      const modal = document.getElementById('newRequestModal');
      if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        document.body.classList.add('modal-open');
        handleCategoryChange(document.getElementById('reqCategory').value);
      }
    }

    function closeNewRequestModal(force) {
      if (!force && isNewRequestFormDirty()) {
        if (!confirm('You have unsaved changes. Discard faculty request?')) return;
      }
      const modal = document.getElementById('newRequestModal');
      if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
        document.body.classList.remove('modal-open');
      }
    }'''

code = code.replace(old_modals, new_modals)

# Update closeDetailsModal to restore scroll
old_close_details = '''    function closeDetailsModal() {
      const modal = document.getElementById('detailsModal');
      if (modal) modal.classList.remove('show');
    }'''

new_close_details = '''    function closeDetailsModal() {
      const modal = document.getElementById('detailsModal');
      if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
        document.body.classList.remove('modal-open');
      }
    }'''

code = code.replace(old_close_details, new_close_details)

# Update openDetailsModal to lock scroll
old_open_details = '''    function openDetailsModal(id) {
      const req = allRequests.find(r => r.id === id);
      if (!req) return;
      currentRequest = req;
      renderDetails(req);
      const modal = document.getElementById('detailsModal');
      if (modal) modal.classList.add('show');
    }'''

new_open_details = '''    function openDetailsModal(id) {
      const req = allRequests.find(r => r.id === id);
      if (!req) return;
      currentRequest = req;
      renderDetails(req);
      const modal = document.getElementById('detailsModal');
      if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        document.body.classList.add('modal-open');
      }
    }'''

code = code.replace(old_open_details, new_open_details)

# Add NGIS_showOperationSuccess on submit
old_submit_end = '''      closeNewRequestModal();
      document.getElementById('newRequestForm').reset();
      renderDashboard();
      if (window.toast) {
        window.toast(`Service request ${newId} submitted!`, 'success');
      }'''

new_submit_end = '''      closeNewRequestModal(true);
      document.getElementById('newRequestForm').reset();
      renderDashboard();
      if (window.NGIS_showOperationSuccess) {
        window.NGIS_showOperationSuccess({
          title: 'Faculty Request Submitted',
          message: `Requisition ticket ${newId} has been successfully logged with Operations & Facilities.`
        });
      } else if (window.toast) {
        window.toast(`Service request ${newId} submitted!`, 'success');
      }'''

code = code.replace(old_submit_end, new_submit_end)

with open('pages/teacher/teacher-services.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated teacher-services.html successfully.")
