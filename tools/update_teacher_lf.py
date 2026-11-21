with open('pages/teacher/teacher-lost-found.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update openReportModal and closeReportModal
old_modals = '''    function openReportModal(mode = 'found') {
      setReportMode(mode);
      const modal = document.getElementById('reportModal');
      if (modal) modal.classList.add('show');
    }

    function closeReportModal() {
      const modal = document.getElementById('reportModal');
      if (modal) modal.classList.remove('show');
    }'''

new_modals = '''    function isReportFormDirty() {
      const title = document.getElementById('formTitle');
      const desc = document.getElementById('formDesc');
      return (title && title.value.trim() !== '') || (desc && desc.value.trim() !== '');
    }

    function openReportModal(mode = 'found') {
      setReportMode(mode);
      const modal = document.getElementById('reportModal');
      if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        document.body.classList.add('modal-open');
      }
    }

    function closeReportModal(force) {
      if (!force && isReportFormDirty()) {
        if (!confirm('You have unsaved changes. Discard item report?')) return;
      }
      const modal = document.getElementById('reportModal');
      if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
        document.body.classList.remove('modal-open');
      }
    }'''

code = code.replace(old_modals, new_modals)

# Update closeDetailModal to restore scroll
old_close_detail = '''    function closeDetailModal() {
      const modal = document.getElementById('detailModal');
      if (modal) modal.classList.remove('show');
    }'''

new_close_detail = '''    function closeDetailModal() {
      const modal = document.getElementById('detailModal');
      if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
        document.body.classList.remove('modal-open');
      }
    }'''

code = code.replace(old_close_detail, new_close_detail)

# Update openDetailModal to lock scroll
old_open_detail = '''    function openDetailModal(id) {
      const item = allItems.find(i => i.id === id);
      if (!item) return;
      currentItem = item;
      renderDetail(item);
      const modal = document.getElementById('detailModal');
      if (modal) modal.classList.add('show');
    }'''

new_open_detail = '''    function openDetailModal(id) {
      const item = allItems.find(i => i.id === id);
      if (!item) return;
      currentItem = item;
      renderDetail(item);
      const modal = document.getElementById('detailModal');
      if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        document.body.classList.add('modal-open');
      }
    }'''

code = code.replace(old_open_detail, new_open_detail)

# Add NGIS_showOperationSuccess on submit
old_lf_submit_end = '''      closeReportModal();
      document.getElementById('reportForm').reset();
      renderDashboard();
      if (window.toast) {
        window.toast(`${currentModalMode === 'found' ? 'Found' : 'Lost'} item report lodged!`, 'success');
      }'''

new_lf_submit_end = '''      closeReportModal(true);
      document.getElementById('reportForm').reset();
      renderDashboard();
      if (window.NGIS_showOperationSuccess) {
        window.NGIS_showOperationSuccess({
          title: currentModalMode === 'found' ? 'Found Item Registered' : 'Missing Item Reported',
          message: `Item record ${refId} (${title}) has been registered with Campus Operations.`
        });
      } else if (window.toast) {
        window.toast(`${currentModalMode === 'found' ? 'Found' : 'Lost'} item report lodged!`, 'success');
      }'''

code = code.replace(old_lf_submit_end, new_lf_submit_end)

with open('pages/teacher/teacher-lost-found.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated teacher-lost-found.html successfully.")
