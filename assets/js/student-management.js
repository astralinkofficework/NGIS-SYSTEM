/**
 * NGIS Student Management Unified Module
 * Powers the 10 Student Management workflows for Admin and Principal Portals:
 * 1. Student Information (handled by ngis-profiles.js)
 * 2. Verify Student Update
 * 3. Student Assign To Class
 * 4. Declare Exemption
 * 5. Input Attendance (handled by attendance modules)
 * 6. Academic Result (Subject GPA By Exam, Semester GPA, Student Failed)
 * 7. Absence Statistics
 * 8. Registration Form Approve
 * 9. Commendation
 * 10. Discipline
 */

(function (window, document) {
  'use strict';

  var SM = window.STUDENT_MGMT = window.STUDENT_MGMT || {};

  // Simple Notification Toast
  function toast(msg, type) {
    type = type || 'success';
    var t = document.getElementById('ngisToast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'ngisToast';
      t.className = 'fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl shadow-lg text-xs font-medium flex items-center gap-2.5 transition-all duration-300 transform translate-y-8 opacity-0 pointer-events-none';
      document.body.appendChild(t);
    }
    var bg = type === 'success' ? 'bg-[#176B45] text-white' : (type === 'error' ? 'bg-rose-700 text-white' : 'bg-slate-800 text-white');
    t.className = 'fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl shadow-lg text-xs font-medium flex items-center gap-2.5 transition-all duration-300 pointer-events-auto ' + bg;
    t.innerHTML = '<span class="material-symbols-outlined text-sm">' + (type === 'success' ? 'check_circle' : (type === 'error' ? 'error' : 'info')) + '</span><span>' + msg + '</span>';
    t.style.opacity = '1';
    t.style.transform = 'translateY(0)';
    clearTimeout(t._timer);
    t._timer = setTimeout(function () {
      t.style.opacity = '0';
      t.style.transform = 'translateY(24px)';
      t.className += ' pointer-events-none';
    }, 3200);
  }
  SM.toast = toast;

  // ─────────────────────────────────────────────────────────────
  // 2. VERIFY STUDENT UPDATE CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initVerify = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = {
      items: [],
      filteredItems: [],
      search: '',
      statusFilter: 'all',
      classFilter: 'all',
      fieldFilter: 'all',
      activeTab: 'all',
      selectedIds: {},
      currentPage: 1,
      pageSize: 8
    };

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function fetchUpdates() {
      fetch('/api/student-mgmt/verify')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.items = res.data || [];
          computeFilteredItems();
          render();
        })
        .catch(function (err) {
          console.error('Fetch verify error:', err);
          toast('Failed to load student update requests', 'error');
        });
    }

    function computeFilteredItems() {
      var q = state.search.toLowerCase().trim();
      var sFilter = state.statusFilter;
      var cFilter = state.classFilter;
      var fFilter = state.fieldFilter;
      var tab = state.activeTab;

      state.filteredItems = state.items.filter(function (item) {
        // Search query
        if (q) {
          var sName = (item.studentName || '').toLowerCase();
          var sId = (item.studentId || '').toLowerCase();
          var reqId = (item.id || '').toLowerCase();
          var fld = (item.field || '').toLowerCase();
          if (sName.indexOf(q) === -1 && sId.indexOf(q) === -1 && reqId.indexOf(q) === -1 && fld.indexOf(q) === -1) {
            return false;
          }
        }

        // Tab Filter
        if (tab === 'pending' && item.status !== 'pending') return false;
        if (tab === 'approved' && item.status !== 'approved') return false;
        if (tab === 'flagged' && item.status !== 'needs_correction' && item.status !== 'rejected') return false;

        // Dropdown Status Filter
        if (sFilter !== 'all') {
          if (sFilter === 'pending' && item.status !== 'pending') return false;
          if (sFilter === 'approved' && item.status !== 'approved') return false;
          if (sFilter === 'needs_correction' && item.status !== 'needs_correction' && item.status !== 'rejected') return false;
        }

        // Class Filter
        if (cFilter !== 'all') {
          var itemCls = (item.class || '').replace(/^Grade\s+/i, '').trim().toLowerCase();
          var targetCls = cFilter.replace(/^Grade\s+/i, '').trim().toLowerCase();
          if (itemCls !== targetCls) return false;
        }

        // Field Filter
        if (fFilter !== 'all') {
          var itemFld = (item.field || '').toLowerCase();
          var targetFld = fFilter.toLowerCase();
          if (itemFld.indexOf(targetFld) === -1) return false;
        }

        return true;
      });

      var maxPage = Math.max(1, Math.ceil(state.filteredItems.length / state.pageSize));
      if (state.currentPage > maxPage) {
        state.currentPage = maxPage;
      }
    }

    function exportAuditLedger() {
      var records = state.filteredItems.length ? state.filteredItems : state.items;
      if (!records.length) {
        toast('No records available for export.', 'error');
        return;
      }

      var headers = [
        'Request ID',
        'Student ID',
        'Student Name',
        'Class',
        'Field Changed',
        'Current Value',
        'Proposed Amendment',
        'Status',
        'Submitted By',
        'Submission Time',
        'Reviewed By',
        'Review Remarks'
      ];

      var csvRows = [headers.join(',')];

      records.forEach(function (r) {
        var row = [
          '"' + (r.id || '') + '"',
          '"' + (r.studentId || '') + '"',
          '"' + (r.studentName || '').replace(/"/g, '""') + '"',
          '"' + (r.class || '') + '"',
          '"' + (r.field || '').replace(/"/g, '""') + '"',
          '"' + (r.previousValue || '').replace(/"/g, '""') + '"',
          '"' + (r.proposedValue || '').replace(/"/g, '""') + '"',
          '"' + (r.status || '') + '"',
          '"' + (r.submittedBy || '').replace(/"/g, '""') + '"',
          '"' + (r.submittedAt || '') + '"',
          '"' + (r.reviewedBy || '') + '"',
          '"' + (r.comments || '').replace(/"/g, '""') + '"'
        ];
        csvRows.push(row.join(','));
      });

      var csvContent = '\uFEFF' + csvRows.join('\r\n');
      var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      var url = URL.createObjectURL(blob);
      var link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', 'NGIS_Student_Update_Audit_Ledger_' + new Date().toISOString().slice(0, 10) + '.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      toast('Audit ledger exported successfully (.CSV)', 'success');
    }

    function openRejectModal(item) {
      var modalId = 'rejectModal';
      var existing = document.getElementById(modalId);
      if (existing) existing.remove();

      var modalHtml = '<div id="' + modalId + '" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs transition-opacity">' +
        '<div class="bg-white dark:bg-[#1c2420] border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl w-full max-w-lg overflow-hidden flex flex-col animate-in fade-in zoom-in-95 duration-150">' +
          '<div class="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60">' +
            '<div class="flex items-center gap-2">' +
              '<span class="material-symbols-outlined text-rose-600 text-[22px]">warning</span>' +
              '<h2 class="text-sm font-medium text-slate-800 dark:text-slate-100">Reject Student Update Amendment</h2>' +
            '</div>' +
            '<button type="button" id="closeRejectModalBtn" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">' +
              '<span class="material-symbols-outlined text-[20px]">close</span>' +
            '</button>' +
          '</div>' +
          '<div class="p-6 space-y-4 text-xs">' +
            '<p class="text-slate-600 dark:text-slate-300 font-normal">' +
              'You are rejecting the profile update request <span class="font-mono font-medium text-[#176B45] dark:text-emerald-400">' + escapeHtml(item.id) + '</span> ' +
              'for <span class="font-medium text-slate-800 dark:text-slate-100">' + escapeHtml(item.studentName) + '</span>. Please supply a reason for audit tracking.' +
            '</p>' +
            '<div>' +
              '<label for="rejectionReasonInput" class="block font-medium text-slate-700 dark:text-slate-300 mb-1.5">' +
                'Reason for Rejection <span class="text-rose-600">*</span>' +
              '</label>' +
              '<textarea id="rejectionReasonInput" rows="3" class="w-full px-3 py-2 bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 rounded-lg text-xs text-slate-800 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-rose-500 transition-colors" placeholder="e.g., Missing official registry seal, invalid phone prefix..."></textarea>' +
            '</div>' +
            '<div class="bg-slate-50 dark:bg-slate-800/40 p-3 rounded-lg text-slate-500 dark:text-slate-400 flex items-start gap-2 border border-slate-100 dark:border-slate-800">' +
              '<span class="material-symbols-outlined text-[18px] text-amber-600 mt-0.5 shrink-0">info</span>' +
              '<span>This rejection will be recorded on the student\'s audit trail and send a notification to the guardian.</span>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/60">' +
            '<button type="button" id="cancelRejectBtn" class="px-4 py-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 text-xs font-medium transition-colors">' +
              'Cancel' +
            '</button>' +
            '<button type="button" id="confirmRejectBtn" class="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-white text-xs font-medium shadow-xs transition-all">' +
              '<span class="material-symbols-outlined text-[18px]">block</span>' +
              '<span>Confirm Rejection</span>' +
            '</button>' +
          '</div>' +
        '</div>' +
      '</div>';

      document.body.insertAdjacentHTML('beforeend', modalHtml);

      var modal = document.getElementById(modalId);
      var closeBtn = document.getElementById('closeRejectModalBtn');
      var cancelBtn = document.getElementById('cancelRejectBtn');
      var confirmBtn = document.getElementById('confirmRejectBtn');
      var reasonInput = document.getElementById('rejectionReasonInput');

      function closeModal() {
        if (modal) modal.remove();
      }

      if (closeBtn) closeBtn.onclick = closeModal;
      if (cancelBtn) cancelBtn.onclick = closeModal;
      if (modal) {
        modal.onclick = function (e) {
          if (e.target === modal) closeModal();
        };
      }

      if (confirmBtn) {
        confirmBtn.onclick = function () {
          var reason = (reasonInput ? reasonInput.value : '').trim();
          if (!reason) {
            toast('Please enter a rejection reason for the audit ledger', 'error');
            if (reasonInput) reasonInput.focus();
            return;
          }

          confirmBtn.disabled = true;
          confirmBtn.innerHTML = '<span class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span> Processing...';

          fetch('/api/student-mgmt/verify/' + item.id + '/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              action: 'reject',
              comments: reason,
              reviewer: (portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office')
            })
          })
          .then(function (res) { return res.json(); })
          .then(function (res) {
            if (res.success) {
              item.status = 'rejected';
              item.comments = reason;
              closeModal();
              computeFilteredItems();
              render();
              toast('Update request rejected and recorded on student audit trail', 'success');
            } else {
              toast(res.error || 'Operation failed', 'error');
              confirmBtn.disabled = false;
              confirmBtn.innerHTML = '<span class="material-symbols-outlined text-[18px]">block</span> Confirm Rejection';
            }
          })
          .catch(function () {
            toast('Failed to process rejection', 'error');
            closeModal();
          });
        };
      }
    }

    function openReviewModal(item) {
      var modalId = 'verifyModal';
      var existing = document.getElementById(modalId);
      if (existing) existing.remove();

      var modalHtml = '<div id="' + modalId + '" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs transition-opacity">' +
        '<div class="bg-white dark:bg-[#1c2420] border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl max-w-xl w-full overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-150">' +
          '<div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50 dark:bg-slate-800/60">' +
            '<div class="flex items-center gap-2.5">' +
              '<span class="material-symbols-outlined text-[#176B45]">verified_user</span>' +
              '<h3 class="text-sm font-medium text-slate-800 dark:text-slate-100">Review Profile Amendment Diff</h3>' +
            '</div>' +
            '<button type="button" id="closeVerifyModal" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer">' +
              '<span class="material-symbols-outlined text-lg">close</span>' +
            '</button>' +
          '</div>' +
          '<div class="p-6 space-y-4 overflow-y-auto text-xs">' +
            '<div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-xl space-y-1 border border-slate-100 dark:border-slate-800">' +
              '<p class="text-slate-500 dark:text-slate-400 font-normal">Student: <span class="text-slate-800 dark:text-slate-100 font-medium">' + escapeHtml(item.studentName) + ' (' + escapeHtml(item.studentId) + ')</span> &bull; Class ' + escapeHtml(item.class) + '</p>' +
              '<p class="text-slate-500 dark:text-slate-400 font-normal">Submitted by: <span class="text-slate-700 dark:text-slate-300 font-medium">' + escapeHtml(item.submittedBy) + '</span> on ' + escapeHtml(item.submittedAt) + '</p>' +
            '</div>' +
            '<div>' +
              '<p class="text-[11px] font-medium uppercase tracking-wider text-slate-400 mb-1">Target Field</p>' +
              '<p class="text-sm font-medium text-slate-800 dark:text-slate-100">' + escapeHtml(item.field) + '</p>' +
            '</div>' +
            '<div class="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3 bg-slate-50/60 dark:bg-slate-800/30 rounded-xl border border-slate-200/60 dark:border-slate-800">' +
              '<div>' +
                '<span class="text-[11px] font-medium text-slate-400 uppercase">Current Ledger Value</span>' +
                '<div class="mt-1 text-slate-600 dark:text-slate-400 line-through">' + escapeHtml(item.previousValue) + '</div>' +
              '</div>' +
              '<div>' +
                '<span class="text-[11px] font-medium text-[#176B45] dark:text-emerald-400 uppercase">Proposed Amendment</span>' +
                '<div class="mt-1 font-medium text-[#176B45] dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 p-1.5 rounded">' + escapeHtml(item.proposedValue) + '</div>' +
              '</div>' +
            '</div>' +
            '<div>' +
              '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-400">Supporting Documentation</span>' +
              '<div class="mt-1.5 flex items-center justify-between p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800">' +
                '<div class="flex items-center gap-2"><span class="material-symbols-outlined text-slate-400 text-lg">attach_file</span><span class="font-mono text-slate-700 dark:text-slate-200 truncate">' + escapeHtml(item.supportingDoc || 'document.pdf') + '</span></div>' +
                '<span class="text-[11px] text-[#176B45] dark:text-emerald-400 font-medium px-2 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800">Verified Attachment</span>' +
              '</div>' +
            '</div>' +
            '<div>' +
              '<label class="block text-[11px] font-medium uppercase tracking-wider text-slate-400 mb-1">Official Reviewer Note</label>' +
              '<textarea id="verifyReviewComments" class="w-full text-xs p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-1 focus:ring-[#176B45] focus:outline-none" rows="2" placeholder="Input rationale or verification remarks...">' + escapeHtml(item.comments || '') + '</textarea>' +
            '</div>' +
          '</div>' +
          '<div class="px-6 py-3.5 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-2">' +
            '<button type="button" id="btnRejectUpdateModal" class="px-3.5 py-2 rounded-lg border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 text-xs font-medium cursor-pointer transition-colors">' +
              'Reject Request' +
            '</button>' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="btnCorrectionUpdate" class="px-3.5 py-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 text-slate-700 dark:text-slate-300 text-xs font-medium cursor-pointer transition-colors">' +
                'Request Correction' +
              '</button>' +
              '<button type="button" id="btnApproveUpdateModal" class="px-4 py-2 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium cursor-pointer transition-colors shadow-xs">' +
                'Approve &amp; Sync Ledger' +
              '</button>' +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';

      document.body.insertAdjacentHTML('beforeend', modalHtml);

      var modal = document.getElementById(modalId);
      var closeBtn = document.getElementById('closeVerifyModal');
      var rejectBtn = document.getElementById('btnRejectUpdateModal');
      var correctBtn = document.getElementById('btnCorrectionUpdate');
      var approveBtn = document.getElementById('btnApproveUpdateModal');

      function closeModal() {
        if (modal) modal.remove();
      }

      if (closeBtn) closeBtn.onclick = closeModal;
      if (modal) {
        modal.onclick = function (e) {
          if (e.target === modal) closeModal();
        };
      }

      function sendAction(action) {
        var comments = (document.getElementById('verifyReviewComments') || {}).value || '';
        fetch('/api/student-mgmt/verify/' + item.id + '/action', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: action,
            comments: comments,
            reviewer: (portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office')
          })
        })
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (res.success) {
            item.status = (action === 'approve' ? 'approved' : (action === 'reject' ? 'rejected' : 'needs_correction'));
            item.comments = comments;
            closeModal();
            computeFilteredItems();
            render();
            toast('Update request ' + action + 'ed successfully!');
          } else {
            toast(res.error || 'Operation failed', 'error');
          }
        })
        .catch(function () {
          toast('Failed to process request', 'error');
        });
      }

      if (approveBtn) approveBtn.onclick = function () { sendAction('approve'); };
      if (correctBtn) correctBtn.onclick = function () { sendAction('correct'); };
      if (rejectBtn) {
        rejectBtn.onclick = function () {
          closeModal();
          openRejectModal(item);
        };
      }
    }

    function approveItemDirect(item) {
      fetch('/api/student-mgmt/verify/' + item.id + '/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'approve',
          comments: 'Approved and synchronized with student record.',
          reviewer: (portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office')
        })
      })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (res.success) {
          item.status = 'approved';
          item.reviewedAt = 'Just now';
          computeFilteredItems();
          render();
          toast('Update request approved and synchronized with student ledger!', 'success');
        } else {
          toast(res.error || 'Approval failed', 'error');
        }
      })
      .catch(function () {
        toast('Failed to approve request', 'error');
      });
    }

    function render() {
      computeFilteredItems();

      var pendingCount = state.items.filter(function (i) { return i.status === 'pending'; }).length;
      var approvedCount = state.items.filter(function (i) { return i.status === 'approved'; }).length;
      var totalCount = state.items.length;

      var html = '<div class="flex flex-col gap-6 w-full max-w-[1600px] mx-auto text-slate-800 dark:text-slate-100 font-sans">' +

        // 1. Top Breadcrumb & Executive Header Bar
        '<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">' +
          '<div class="flex flex-col gap-1">' +
            '<div class="flex flex-wrap items-center gap-2.5">' +
              '<h1 class="text-xl md:text-2xl font-medium text-slate-900 dark:text-slate-100 tracking-tight">' +
                'Verify Student Profile Updates' +
              '</h1>' +
              '<div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium">' +
                '<span class="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse"></span>' +
                '<span>' + pendingCount + ' Pending Action</span>' +
              '</div>' +
            '</div>' +
            '<p class="text-xs text-slate-500 dark:text-slate-400 font-normal">' +
              'Review and verify student profile updates, custodial changes, and documentation submissions.' +
            '</p>' +
          '</div>' +

          // Quick Header CTAs
          '<div class="flex items-center gap-3 self-start lg:self-center">' +
            '<button type="button" id="exportAuditLedgerBtn" class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800 shadow-xs hover:bg-slate-50 dark:hover:bg-slate-800/60 text-slate-700 dark:text-slate-200 text-xs font-medium transition-all active:scale-95">' +
              '<span class="material-symbols-outlined text-[18px] text-slate-500">file_download</span>' +
              '<span>Export Audit Ledger</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        // 2. KPI Overview Strip (4 Metric Tiles)
        '<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">' +
          // Tile 1
          '<div class="bg-white dark:bg-[#1c2420] p-4 rounded-xl border border-slate-200/80 dark:border-slate-800/80 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-center justify-between">' +
              '<span class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-medium">Pending Verification</span>' +
              '<div class="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-950/40 flex items-center justify-center text-amber-700 dark:text-amber-400">' +
                '<span class="material-symbols-outlined text-[18px]">pending_actions</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-3">' +
              '<div class="text-3xl font-medium text-slate-800 dark:text-slate-100 tracking-tight leading-none">' + pendingCount + '</div>' +
              '<div class="flex items-center gap-1.5 mt-2 text-xs text-slate-400">' +
                '<span class="w-2 h-2 rounded-full bg-amber-500"></span>' +
                '<span>Requires Registrar Review</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Tile 2
          '<div class="bg-white dark:bg-[#1c2420] p-4 rounded-xl border border-slate-200/80 dark:border-slate-800/80 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-center justify-between">' +
              '<span class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-medium">Approved &amp; Synced</span>' +
              '<div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 flex items-center justify-center text-[#176B45] dark:text-emerald-400">' +
                '<span class="material-symbols-outlined text-[18px]">sync_saved_locally</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-3">' +
              '<div class="text-3xl font-medium text-slate-800 dark:text-slate-100 tracking-tight leading-none">' + approvedCount + '</div>' +
              '<div class="flex items-center gap-1.5 mt-2 text-xs text-slate-400">' +
                '<span class="w-2 h-2 rounded-full bg-emerald-500"></span>' +
                '<span>Ledger Synchronized</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Tile 3
          '<div class="bg-white dark:bg-[#1c2420] p-4 rounded-xl border border-slate-200/80 dark:border-slate-800/80 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-center justify-between">' +
              '<span class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-medium">Total Submissions</span>' +
              '<div class="w-8 h-8 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300">' +
                '<span class="material-symbols-outlined text-[18px]">folder_open</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-3">' +
              '<div class="text-3xl font-medium text-slate-800 dark:text-slate-100 tracking-tight leading-none">' + totalCount + '</div>' +
              '<div class="mt-2 text-xs text-slate-400">' +
                '<span>Active Academic Term Cycle</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Tile 4
          '<div class="bg-white dark:bg-[#1c2420] p-4 rounded-xl border border-slate-200/80 dark:border-slate-800/80 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-center justify-between">' +
              '<span class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-medium">Approval Turnaround</span>' +
              '<div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 flex items-center justify-center text-[#176B45] dark:text-emerald-400">' +
                '<span class="material-symbols-outlined text-[18px]">avg_pace</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-3">' +
              '<div class="text-3xl font-medium text-slate-800 dark:text-slate-100 tracking-tight leading-none">' +
                '1.8 <span class="text-base font-normal text-slate-400">hrs</span>' +
              '</div>' +
              '<div class="mt-2 text-xs text-slate-400">' +
                '<span>Within 24h SLA Target</span>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>' +

        // 3. Search & Structured Filter Toolbar
        '<div class="bg-white dark:bg-[#1c2420] rounded-xl border border-slate-200/80 dark:border-slate-800/80 shadow-xs p-4 flex flex-col gap-3">' +
          '<div class="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-3">' +
            // Search Input with Keyboard Shortcut
            '<div class="relative flex-1 max-w-2xl">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-[20px]">search</span>' +
              '<input class="w-full pl-10 pr-16 py-2.5 bg-slate-50 dark:bg-slate-800/60 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-normal text-slate-800 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-[#176B45] transition-colors" ' +
                'id="studentSearchInput" placeholder="Search student name, ID, changed field, or request ID..." type="search" value="' + escapeHtml(state.search) + '">' +
              '<span class="absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded bg-slate-200/70 dark:bg-slate-700 text-slate-500 dark:text-slate-400 text-[10px] font-mono tracking-widest pointer-events-none">⌘K</span>' +
            '</div>' +

            // Quick Select Dropdowns
            '<div class="flex flex-wrap items-center gap-2">' +
              // Status Dropdown
              '<div class="relative">' +
                '<select id="filterStatusSelect" class="appearance-none bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 text-xs font-medium pl-3 pr-8 py-2.5 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#176B45] cursor-pointer">' +
                  '<option value="all"' + (state.statusFilter === 'all' ? ' selected' : '') + '>All Statuses (' + totalCount + ')</option>' +
                  '<option value="pending"' + (state.statusFilter === 'pending' ? ' selected' : '') + '>Pending Review (' + pendingCount + ')</option>' +
                  '<option value="approved"' + (state.statusFilter === 'approved' ? ' selected' : '') + '>Approved &amp; Synced (' + approvedCount + ')</option>' +
                  '<option value="needs_correction"' + (state.statusFilter === 'needs_correction' ? ' selected' : '') + '>Needs Clarification (0)</option>' +
                '</select>' +
                '<span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">unfold_more</span>' +
              '</div>' +

              // Class Dropdown
              '<div class="relative">' +
                '<select id="filterClassSelect" class="appearance-none bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 text-xs font-medium pl-3 pr-8 py-2.5 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#176B45] cursor-pointer">' +
                  '<option value="all"' + (state.classFilter === 'all' ? ' selected' : '') + '>All Classes</option>' +
                  '<option value="10A"' + (state.classFilter === '10A' ? ' selected' : '') + '>Grade 10A</option>' +
                  '<option value="10B"' + (state.classFilter === '10B' ? ' selected' : '') + '>Grade 10B</option>' +
                  '<option value="11A"' + (state.classFilter === '11A' ? ' selected' : '') + '>Grade 11A</option>' +
                  '<option value="12A"' + (state.classFilter === '12A' ? ' selected' : '') + '>Grade 12A</option>' +
                '</select>' +
                '<span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">unfold_more</span>' +
              '</div>' +

              // Field Dropdown
              '<div class="relative">' +
                '<select id="filterFieldSelect" class="appearance-none bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 text-xs font-medium pl-3 pr-8 py-2.5 rounded-xl focus:outline-none focus:ring-1 focus:ring-[#176B45] cursor-pointer">' +
                  '<option value="all"' + (state.fieldFilter === 'all' ? ' selected' : '') + '>All Changed Fields</option>' +
                  '<option value="address"' + (state.fieldFilter === 'address' ? ' selected' : '') + '>Residential Address</option>' +
                  '<option value="contact"' + (state.fieldFilter === 'contact' ? ' selected' : '') + '>Emergency Contact</option>' +
                  '<option value="legal"' + (state.fieldFilter === 'legal' ? ' selected' : '') + '>Legal Name</option>' +
                  '<option value="medical"' + (state.fieldFilter === 'medical' ? ' selected' : '') + '>Medical &amp; Dietary</option>' +
                  '<option value="guardian"' + (state.fieldFilter === 'guardian' ? ' selected' : '') + '>Guardian Status</option>' +
                '</select>' +
                '<span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">unfold_more</span>' +
              '</div>' +

              // Reset Filter Button
              '<button type="button" id="resetFiltersBtn" class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 transition-colors" title="Reset Filters">' +
                '<span class="material-symbols-outlined text-[18px]">filter_alt_off</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          // Active State Pill Switcher
          '<div class="flex items-center gap-2 pt-1 overflow-x-auto text-xs">' +
            '<button type="button" class="tab-pill px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ' + (state.activeTab === 'all' ? 'bg-[#176B45] text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200') + '" data-tab="all">' +
              'All Submissions <span class="ml-1 opacity-80">(' + totalCount + ')</span>' +
            '</button>' +
            '<button type="button" class="tab-pill px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ' + (state.activeTab === 'pending' ? 'bg-[#176B45] text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200') + '" data-tab="pending">' +
              'Pending Review <span class="ml-1 px-1.5 py-0.2 rounded-full bg-amber-500 text-white font-medium">' + pendingCount + '</span>' +
            '</button>' +
            '<button type="button" class="tab-pill px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ' + (state.activeTab === 'approved' ? 'bg-[#176B45] text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200') + '" data-tab="approved">' +
              'Approved &amp; Ledger Synced <span class="ml-1 text-emerald-600 dark:text-emerald-400 font-medium">' + approvedCount + '</span>' +
            '</button>' +
            '<button type="button" class="tab-pill px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ' + (state.activeTab === 'flagged' ? 'bg-[#176B45] text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200') + '" data-tab="flagged">' +
              'Flagged Discrepancies <span class="ml-1 opacity-70">0</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        // 4. Main High-Density Clearance Ledger Table
        '<div class="bg-white dark:bg-[#1c2420] rounded-xl border border-slate-200/80 dark:border-slate-800/80 shadow-xs overflow-hidden flex flex-col" id="verifyTableCard">' +
          '<div class="overflow-x-auto">' +
            '<table class="w-full text-left border-collapse min-w-[1080px]" id="verifyLedgerTable">' +
              '<thead>' +
                '<tr class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 dark:text-slate-400 font-medium text-[11px] uppercase tracking-wider border-b border-slate-100 dark:border-slate-800">' +
                  '<th class="py-3 px-4 w-12 text-center">' +
                    '<input type="checkbox" id="selectAllSubmissions" class="rounded text-[#176B45] focus:ring-0 cursor-pointer" aria-label="Select all submissions">' +
                  '</th>' +
                  '<th class="py-3 px-4 w-32">Request ID</th>' +
                  '<th class="py-3 px-4 w-56">Student &amp; Cohort</th>' +
                  '<th class="py-3 px-4 w-48">Field Changed</th>' +
                  '<th class="py-3 px-4">Current vs Proposed Amendment</th>' +
                  '<th class="py-3 px-4 w-40">Status</th>' +
                  '<th class="py-3 px-4 w-48 text-right pr-6">ACTIONS</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-xs text-slate-700 dark:text-slate-200">';

      var totalFiltered = state.filteredItems.length;
      var pageSize = state.pageSize;
      var startIndex = (state.currentPage - 1) * pageSize;
      var endIndex = Math.min(startIndex + pageSize, totalFiltered);
      var pageItems = state.filteredItems.slice(startIndex, endIndex);

      if (totalFiltered === 0) {
        html += '<tr><td colspan="7" class="py-16 text-center text-slate-400">' +
          '<div class="flex flex-col items-center justify-center gap-2">' +
            '<span class="material-symbols-outlined text-[36px] text-slate-300">folder_off</span>' +
            '<p class="text-xs font-medium">No student profile update requests match the selected filters.</p>' +
            '<button type="button" id="emptyClearBtn" class="mt-2 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium hover:bg-slate-200 transition-colors">Clear Filters</button>' +
          '</div>' +
        '</td></tr>';
      } else {
        pageItems.forEach(function (r) {
          var isChecked = !!state.selectedIds[r.id];
          var initials = r.initials || (r.studentName ? r.studentName.split(' ').map(function(n){return n[0];}).join('').slice(0, 2).toUpperCase() : 'ST');
          var fieldIcon = r.fieldIcon || (r.field && r.field.indexOf('Address') !== -1 ? 'home_pin' : (r.field && r.field.indexOf('Phone') !== -1 ? 'contact_phone' : (r.field && r.field.indexOf('Name') !== -1 ? 'badge' : (r.field && r.field.indexOf('Medical') !== -1 ? 'medical_services' : 'gavel'))));
          var fieldCategory = r.fieldCategory || (r.field && r.field.indexOf('Address') !== -1 ? 'Student Primary Domicile' : (r.field && r.field.indexOf('Phone') !== -1 ? 'Guardian Contact Channel' : (r.field && r.field.indexOf('Name') !== -1 ? 'MoEYS Formal Registry' : (r.field && r.field.indexOf('Medical') !== -1 ? 'Health Center Protocol' : 'Custodial Documentation'))));

          // Status Badge
          var statusHtml = '';
          if (r.status === 'pending') {
            statusHtml = '<div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[11px] font-medium">' +
              '<span class="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>' +
              '<span>Pending Review</span>' +
            '</div>';
          } else if (r.status === 'approved') {
            statusHtml = '<div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-[#176B45] dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/60 text-[11px] font-medium">' +
              '<span class="material-symbols-outlined text-[14px]">check_circle</span>' +
              '<span>Approved &amp; Synced</span>' +
            '</div>';
          } else if (r.status === 'rejected') {
            statusHtml = '<div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800/60 text-[11px] font-medium">' +
              '<span class="material-symbols-outlined text-[14px]">cancel</span>' +
              '<span>Rejected</span>' +
            '</div>';
          } else {
            statusHtml = '<div class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-800/60 text-[11px] font-medium">' +
              '<span class="material-symbols-outlined text-[14px]">help</span>' +
              '<span>Needs Clarification</span>' +
            '</div>';
          }

          // Action Buttons
          var actionsHtml = '<div class="inline-flex items-center gap-1.5 justify-end">' +
            '<button type="button" class="btn-diff-view inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-medium transition-colors" data-id="' + escapeHtml(r.id) + '" title="View diff details">' +
              '<span class="material-symbols-outlined text-[16px] text-slate-400">visibility</span>' +
              '<span>View</span>' +
            '</button>';

          if (r.status === 'approved') {
            actionsHtml += '<button type="button" class="btn-diff-reject inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-rose-50 hover:text-rose-700 text-slate-400 text-xs font-medium transition-colors opacity-70" data-id="' + escapeHtml(r.id) + '" title="Reject amendment">' +
              '<span class="material-symbols-outlined text-[16px]">close</span>' +
              '<span>Reject</span>' +
            '</button>' +
            '<button type="button" class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-[#176B45] dark:text-emerald-400 text-xs font-medium cursor-default" title="Already approved">' +
              '<span class="material-symbols-outlined text-[16px]">done_all</span>' +
              '<span>Approved</span>' +
            '</button>';
          } else if (r.status === 'rejected') {
            actionsHtml += '<button type="button" class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-rose-50 text-rose-700 text-xs font-medium cursor-default" title="Already rejected">' +
              '<span class="material-symbols-outlined text-[16px]">block</span>' +
              '<span>Rejected</span>' +
            '</button>';
          } else {
            actionsHtml += '<button type="button" class="btn-diff-reject inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-rose-50 hover:text-rose-700 text-slate-500 text-xs font-medium transition-colors" data-id="' + escapeHtml(r.id) + '" title="Reject request">' +
              '<span class="material-symbols-outlined text-[16px]">close</span>' +
              '<span>Reject</span>' +
            '</button>' +
            '<button type="button" class="btn-direct-approve inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium shadow-xs transition-all" data-id="' + escapeHtml(r.id) + '" title="Approve amendment">' +
              '<span class="material-symbols-outlined text-[16px]">check</span>' +
              '<span>Approve</span>' +
            '</button>';
          }
          actionsHtml += '</div>';

          // Proposed Display styling
          var isMedical = r.field && r.field.indexOf('Medical') !== -1;
          var proposedDisplayClass = isMedical ? 'font-medium text-rose-700 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40 px-1.5 py-0.5 rounded text-xs' : 'font-medium text-[#176B45] dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-1.5 py-0.5 rounded text-xs';

          html += '<tr class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors group ' + (isChecked ? 'bg-emerald-50/20 dark:bg-emerald-950/20' : '') + '">' +
            // Checkbox
            '<td class="py-4 px-4 text-center">' +
              '<input type="checkbox" class="verify-row-check rounded text-[#176B45] focus:ring-0 cursor-pointer" data-id="' + escapeHtml(r.id) + '" ' + (isChecked ? 'checked' : '') + ' aria-label="Select request ' + escapeHtml(r.id) + '">' +
            '</td>' +

            // Request ID
            '<td class="py-4 px-4 align-top">' +
              '<div class="font-mono text-xs font-medium text-[#176B45] dark:text-emerald-400">' + escapeHtml(r.id) + '</div>' +
              '<div class="text-[11px] text-slate-400 mt-0.5">' + escapeHtml(r.timeAgo || r.submittedAt || 'Recently') + '</div>' +
            '</td>' +

            // Student & Cohort
            '<td class="py-4 px-4 align-top">' +
              '<div class="flex items-center gap-2.5">' +
                '<div class="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-medium text-xs text-[#176B45] dark:text-emerald-400 shrink-0">' +
                  escapeHtml(initials) +
                '</div>' +
                '<div class="flex flex-col min-w-0">' +
                  '<div class="font-medium text-slate-800 dark:text-slate-100 group-hover:text-[#176B45] transition-colors truncate">' +
                    escapeHtml(r.studentName) +
                  '</div>' +
                  '<div class="flex items-center gap-1.5 text-[11px] text-slate-400 font-mono">' +
                    '<span>' + escapeHtml(r.studentId) + '</span>' +
                    '<span>&bull;</span>' +
                    '<span class="px-1.5 py-0.2 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-sans font-medium">' + escapeHtml(r.class) + '</span>' +
                  '</div>' +
                '</div>' +
              '</div>' +
            '</td>' +

            // Field Changed
            '<td class="py-4 px-4 align-top">' +
              '<div class="flex items-center gap-1.5 text-slate-800 dark:text-slate-100 font-medium text-xs">' +
                '<span class="material-symbols-outlined text-[16px] text-slate-400">' + escapeHtml(fieldIcon) + '</span>' +
                '<span>' + escapeHtml(r.field) + '</span>' +
              '</div>' +
              '<span class="text-[11px] text-slate-400 mt-0.5 block font-normal">' + escapeHtml(fieldCategory) + '</span>' +
            '</td>' +

            // Current vs Proposed Amendment
            '<td class="py-4 px-4 align-top">' +
              '<div class="flex flex-col gap-1 bg-slate-50 dark:bg-slate-800/40 p-2.5 rounded-lg max-w-xl border border-slate-100 dark:border-slate-800">' +
                '<div class="flex items-center gap-2 text-xs text-slate-400">' +
                  '<span class="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600 shrink-0"></span>' +
                  '<span class="line-through">' + escapeHtml(r.previousValue) + '</span>' +
                '</div>' +
                '<div class="flex items-center gap-2 text-xs text-slate-800 dark:text-slate-100">' +
                  '<span class="material-symbols-outlined text-[16px] text-emerald-600 shrink-0">arrow_forward</span>' +
                  '<span class="' + proposedDisplayClass + '">' + escapeHtml(r.proposedValue) + '</span>' +
                  (r.proposedNote ? '<span class="text-[11px] text-slate-400 ml-1">' + escapeHtml(r.proposedNote) + '</span>' : '') +
                '</div>' +
              '</div>' +
            '</td>' +

            // Status
            '<td class="py-4 px-4 align-top">' +
              statusHtml +
            '</td>' +

            // Actions
            '<td class="py-4 px-4 align-top text-right pr-6">' +
              actionsHtml +
            '</td>' +
          '</tr>';
        });
      }

      html += '</tbody></table></div>' +

        // Table Footer & Pagination
        '<div class="p-4 bg-slate-50 dark:bg-slate-800/40 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">' +
          '<div class="text-slate-500 dark:text-slate-400">' +
            'Showing <span class="font-medium text-slate-800 dark:text-slate-100">' + (totalFiltered > 0 ? (startIndex + 1) : 0) + '</span> to ' +
            '<span class="font-medium text-slate-800 dark:text-slate-100">' + endIndex + '</span> of ' +
            '<span class="font-medium text-slate-800 dark:text-slate-100">' + totalFiltered + '</span> verified amendment records' +
          '</div>' +
          '<div class="flex items-center gap-1.5">';

      var totalPages = Math.ceil(totalFiltered / pageSize) || 1;
      var prevDisabled = state.currentPage <= 1;
      html += '<button type="button" id="verifyPrevPage" ' + (prevDisabled ? 'disabled' : '') + ' class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs font-medium ' + (prevDisabled ? 'opacity-50 cursor-not-allowed bg-slate-100 dark:bg-slate-800' : 'hover:bg-slate-50 dark:hover:bg-slate-800 bg-white dark:bg-slate-800') + ' transition-colors">' +
        'Previous' +
      '</button>';

      for (var p = 1; p <= totalPages; p++) {
        if (p === state.currentPage) {
          html += '<span class="w-8 h-8 rounded-lg bg-[#176B45] text-white text-xs font-medium flex items-center justify-center shadow-xs">' + p + '</span>';
        } else {
          html += '<button type="button" class="verify-page-btn w-8 h-8 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 text-xs font-medium flex items-center justify-center transition-colors" data-page="' + p + '">' + p + '</button>';
        }
      }

      var nextDisabled = state.currentPage >= totalPages;
      html += '<button type="button" id="verifyNextPage" ' + (nextDisabled ? 'disabled' : '') + ' class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs font-medium ' + (nextDisabled ? 'opacity-50 cursor-not-allowed bg-slate-100 dark:bg-slate-800' : 'hover:bg-slate-50 dark:hover:bg-slate-800 bg-white dark:bg-slate-800') + ' transition-colors">' +
        'Next' +
      '</button></div></div>' +

        '</div>' + // End verifyTableCard

      '</div>'; // End container

      root.innerHTML = html;

      attachEventListeners();
    }

    function attachEventListeners() {
      // Export Button
      var exportBtn = document.getElementById('exportAuditLedgerBtn');
      if (exportBtn) {
        exportBtn.onclick = exportAuditLedger;
      }

      // Search Input
      var searchInput = document.getElementById('studentSearchInput');
      if (searchInput) {
        searchInput.oninput = function (e) {
          state.search = e.target.value;
          state.currentPage = 1;
          render();
        };
      }

      // Keyboard Shortcut ⌘K / Ctrl+K focus
      window.onkeydown = function (e) {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
          e.preventDefault();
          if (searchInput) searchInput.focus();
        }
      };

      // Status Dropdown Filter
      var statusSelect = document.getElementById('filterStatusSelect');
      if (statusSelect) {
        statusSelect.onchange = function (e) {
          state.statusFilter = e.target.value;
          state.currentPage = 1;
          render();
        };
      }

      // Class Dropdown Filter
      var classSelect = document.getElementById('filterClassSelect');
      if (classSelect) {
        classSelect.onchange = function (e) {
          state.classFilter = e.target.value;
          state.currentPage = 1;
          render();
        };
      }

      // Field Dropdown Filter
      var fieldSelect = document.getElementById('filterFieldSelect');
      if (fieldSelect) {
        fieldSelect.onchange = function (e) {
          state.fieldFilter = e.target.value;
          state.currentPage = 1;
          render();
        };
      }

      // Reset Button
      var resetBtn = document.getElementById('resetFiltersBtn');
      if (resetBtn) {
        resetBtn.onclick = function () {
          state.search = '';
          state.statusFilter = 'all';
          state.classFilter = 'all';
          state.fieldFilter = 'all';
          state.activeTab = 'all';
          state.currentPage = 1;
          state.selectedIds = {};
          render();
          toast('Filters reset to default view', 'success');
        };
      }

      var emptyClearBtn = document.getElementById('emptyClearBtn');
      if (emptyClearBtn) {
        emptyClearBtn.onclick = function () {
          state.search = '';
          state.statusFilter = 'all';
          state.classFilter = 'all';
          state.fieldFilter = 'all';
          state.activeTab = 'all';
          state.currentPage = 1;
          render();
        };
      }

      // Active State Pill Switcher
      var pillButtons = document.querySelectorAll('.tab-pill');
      pillButtons.forEach(function (btn) {
        btn.onclick = function () {
          state.activeTab = btn.getAttribute('data-tab');
          state.currentPage = 1;
          render();
        };
      });

      // Select All Checkbox
      var selectAll = document.getElementById('selectAllSubmissions');
      if (selectAll) {
        selectAll.onchange = function (e) {
          var isChecked = e.target.checked;
          state.filteredItems.forEach(function (r) {
            if (isChecked) {
              state.selectedIds[r.id] = true;
            } else {
              delete state.selectedIds[r.id];
            }
          });
          render();
        };
      }

      // Row Checkboxes
      var rowChecks = document.querySelectorAll('.verify-row-check');
      rowChecks.forEach(function (chk) {
        chk.onchange = function (e) {
          var id = e.target.getAttribute('data-id');
          if (e.target.checked) {
            state.selectedIds[id] = true;
          } else {
            delete state.selectedIds[id];
          }
          var tr = e.target.closest('tr');
          if (tr) {
            if (e.target.checked) {
              tr.classList.add('bg-emerald-50/20', 'dark:bg-emerald-950/20');
            } else {
              tr.classList.remove('bg-emerald-50/20', 'dark:bg-emerald-950/20');
            }
          }
        };
      });

      // View Diff Buttons
      var viewBtns = document.querySelectorAll('.btn-diff-view');
      viewBtns.forEach(function (btn) {
        btn.onclick = function () {
          var id = btn.getAttribute('data-id');
          var item = state.items.find(function (i) { return i.id === id; });
          if (item) openReviewModal(item);
        };
      });

      // Reject Buttons
      var rejectBtns = document.querySelectorAll('.btn-diff-reject');
      rejectBtns.forEach(function (btn) {
        btn.onclick = function () {
          var id = btn.getAttribute('data-id');
          var item = state.items.find(function (i) { return i.id === id; });
          if (item) openRejectModal(item);
        };
      });

      // Direct Approve Buttons
      var approveBtns = document.querySelectorAll('.btn-direct-approve');
      approveBtns.forEach(function (btn) {
        btn.onclick = function () {
          var id = btn.getAttribute('data-id');
          var item = state.items.find(function (i) { return i.id === id; });
          if (item) approveItemDirect(item);
        };
      });

      // Pagination
      var prevBtn = document.getElementById('verifyPrevPage');
      if (prevBtn) {
        prevBtn.onclick = function () {
          if (state.currentPage > 1) {
            state.currentPage--;
            render();
          }
        };
      }

      var nextBtn = document.getElementById('verifyNextPage');
      if (nextBtn) {
        nextBtn.onclick = function () {
          var totalPages = Math.ceil(state.filteredItems.length / state.pageSize);
          if (state.currentPage < totalPages) {
            state.currentPage++;
            render();
          }
        };
      }

      var pageBtns = document.querySelectorAll('.verify-page-btn');
      pageBtns.forEach(function (btn) {
        btn.onclick = function () {
          var p = parseInt(btn.getAttribute('data-page'), 10);
          if (!isNaN(p)) {
            state.currentPage = p;
            render();
          }
        };
      });
    }

    fetchUpdates();
  };

  // ─────────────────────────────────────────────────────────────
  // 3. STUDENT ASSIGN TO CLASS CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initAssign = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { classes: [], students: [], selectedClass: 'all', search: '', selectedStudentIds: [] };

    function fetchAssignData() {
      fetch('/api/student-mgmt/assign')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.classes = res.classes || [];
          state.students = res.students || [];
          render();
        })
        .catch(function () {
          toast('Failed to load class assignment data', 'error');
        });
    }

    function render() {
      var filteredStudents = state.students.filter(function (s) {
        if (state.selectedClass !== 'all' && s.class.toLowerCase() !== state.selectedClass.toLowerCase()) return false;
        if (state.search) {
          var q = state.search.toLowerCase();
          return s.name.toLowerCase().includes(q) || s.id.toLowerCase().includes(q);
        }
        return true;
      });

      var html = '<div class="space-y-6">';

      // Visual Class Capacity Cards
      html += '<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">';
      state.classes.forEach(function (c) {
        var pct = Math.round((c.enrolled / c.capacity) * 100);
        var isSelected = state.selectedClass.toLowerCase() === c.code.toLowerCase();
        html += '<div class="class-card p-3.5 rounded-xl border transition-all cursor-pointer ' + (isSelected ? 'border-[#176B45] bg-emerald-50/30 ring-1 ring-[#176B45]' : 'border-slate-200/80 bg-white hover:border-slate-300') + '" data-code="' + c.code + '">' +
          '<div class="flex items-center justify-between">' +
            '<span class="text-xs font-medium text-slate-800">' + c.name + '</span>' +
            '<span class="text-[10px] px-1.5 py-0.2 rounded font-medium ' + (c.isFull ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-600') + '">' + c.enrolled + '/' + c.capacity + '</span>' +
          '</div>' +
          '<div class="mt-2 text-[11px] text-slate-400 font-normal truncate">' + c.homeroomTeacher + '</div>' +
          '<div class="mt-2 w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">' +
            '<div class="h-full rounded-full ' + (c.isFull ? 'bg-rose-500' : 'bg-[#176B45]') + '" style="width: ' + pct + '%"></div>' +
          '</div>' +
        '</div>';
      });
      html += '</div>';

      // Toolbar
      html += '<div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-xs">' +
        '<div class="relative flex-1 max-w-md">' +
          '<span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 flex items-center"><span class="material-symbols-outlined text-lg">search</span></span>' +
          '<input type="text" id="assignSearchInput" value="' + (state.search || '') + '" placeholder="Search student name or ID..." class="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-1 focus:ring-[#176B45] min-h-[38px]">' +
        '</div>' +
        '<div class="flex items-center gap-2">' +
          '<select id="assignClassFilter" class="text-xs py-2 px-3 rounded-lg border border-slate-200 bg-white font-medium text-slate-700 min-h-[38px] cursor-pointer">' +
            '<option value="all"' + (state.selectedClass === 'all' ? ' selected' : '') + '>All Classes</option>';
      state.classes.forEach(function (c) {
        html += '<option value="' + c.code + '"' + (state.selectedClass.toLowerCase() === c.code.toLowerCase() ? ' selected' : '') + '>' + c.name + ' (' + c.enrolled + ')</option>';
      });
      html += '</select>' +
          '<button type="button" id="btnOpenTransferModal" class="px-4 py-2 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium min-h-[38px] flex items-center gap-1.5 cursor-pointer shadow-xs">' +
            '<span class="material-symbols-outlined text-base">swap_horiz</span><span>Assign / Transfer Student</span>' +
          '</button>' +
        '</div>' +
      '</div>';

      // Table
      html += '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
        '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
          '<thead class="bg-slate-50 text-slate-600 font-medium uppercase tracking-wider text-[11px] border-b border-slate-200/80">' +
            '<tr>' +
              '<th class="px-4 py-3">Student ID</th>' +
              '<th class="px-4 py-3">Name</th>' +
              '<th class="px-4 py-3">Grade</th>' +
              '<th class="px-4 py-3">Current Class</th>' +
              '<th class="px-4 py-3">Advisor</th>' +
              '<th class="px-4 py-3">GPA</th>' +
              '<th class="px-4 py-3 text-right">Action</th>' +
            '</tr>' +
          '</thead>' +
          '<tbody class="divide-y divide-slate-100 text-slate-700">';

      filteredStudents.forEach(function (s) {
        html += '<tr class="hover:bg-slate-50/60 transition-colors">' +
          '<td class="px-4 py-3 font-mono text-[11px] text-slate-500">' + s.id + '</td>' +
          '<td class="px-4 py-3 font-medium text-slate-800">' + s.name + '</td>' +
          '<td class="px-4 py-3 text-slate-600">' + s.grade + '</td>' +
          '<td class="px-4 py-3"><span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-[#176B45] border border-emerald-200">' + s.class + '</span></td>' +
          '<td class="px-4 py-3 text-slate-500">' + (s.advisor || '—') + '</td>' +
          '<td class="px-4 py-3 font-medium text-slate-800">' + s.gpa + '</td>' +
          '<td class="px-4 py-3 text-right">' +
            '<button type="button" class="btn-single-transfer p-1.5 text-slate-500 hover:text-[#176B45] hover:bg-emerald-50 rounded-lg transition-colors cursor-pointer" data-id="' + s.id + '" title="Transfer Class">' +
              '<span class="material-symbols-outlined text-lg">drive_file_move</span>' +
            '</button>' +
          '</td>' +
        '</tr>';
      });

      html += '</tbody></table></div></div></div>';

      root.innerHTML = html;

      // Event handlers
      root.querySelectorAll('.class-card').forEach(function (card) {
        card.addEventListener('click', function () {
          var code = card.getAttribute('data-code');
          state.selectedClass = (state.selectedClass.toLowerCase() === code.toLowerCase()) ? 'all' : code;
          render();
        });
      });

      document.getElementById('assignSearchInput').addEventListener('input', function (e) {
        state.search = e.target.value;
        render();
      });

      document.getElementById('assignClassFilter').addEventListener('change', function (e) {
        state.selectedClass = e.target.value;
        render();
      });

      document.getElementById('btnOpenTransferModal').addEventListener('click', function () {
        openPlacementDialog(null);
      });

      root.querySelectorAll('.btn-single-transfer').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var sid = btn.getAttribute('data-id');
          openPlacementDialog(sid);
        });
      });
    }

    function openPlacementDialog(preselectedStudentId) {
      var modal = document.getElementById('assignModal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'assignModal';
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs transition-opacity';
        document.body.appendChild(modal);
      }

      var modalHtml = '<div class="bg-white rounded-2xl border border-slate-200/80 shadow-xl max-w-md w-full overflow-hidden flex flex-col">' +
        '<div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/70">' +
          '<div class="flex items-center gap-2">' +
            '<span class="material-symbols-outlined text-[#176B45]">swap_horiz</span>' +
            '<h3 class="text-sm font-medium text-slate-800">Student Class Placement &amp; Transfer</h3>' +
          '</div>' +
          '<button type="button" id="closeAssignModal" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg cursor-pointer"><span class="material-symbols-outlined text-lg">close</span></button>' +
        '</div>' +
        '<div class="p-6 space-y-4 text-xs">' +
          '<div>' +
            '<label class="block text-[11px] font-medium uppercase tracking-wider text-slate-500 mb-1">Select Student</label>' +
            '<select id="modalStudentSelect" class="w-full text-xs p-2.5 rounded-lg border border-slate-200 bg-white font-medium text-slate-800 focus:ring-1 focus:ring-[#176B45]">';
      state.students.forEach(function (s) {
        modalHtml += '<option value="' + s.id + '"' + (s.id === preselectedStudentId ? ' selected' : '') + '>' + s.name + ' (' + s.id + ') — Current: Class ' + s.class + '</option>';
      });
      modalHtml += '</select>' +
          '</div>' +
          '<div>' +
            '<label class="block text-[11px] font-medium uppercase tracking-wider text-slate-500 mb-1">Target Class / Section</label>' +
            '<select id="modalTargetClassSelect" class="w-full text-xs p-2.5 rounded-lg border border-slate-200 bg-white font-medium text-slate-800 focus:ring-1 focus:ring-[#176B45]">';
      state.classes.forEach(function (c) {
        modalHtml += '<option value="' + c.code + '">' + c.name + ' (' + c.enrolled + '/' + c.capacity + ' enrolled - ' + c.available + ' spots open)</option>';
      });
      modalHtml += '</select>' +
          '</div>' +
          '<div>' +
            '<label class="block text-[11px] font-medium uppercase tracking-wider text-slate-500 mb-1">Transfer Rationale</label>' +
            '<input type="text" id="modalTransferReason" value="Administrative placement optimization" class="w-full text-xs p-2.5 rounded-lg border border-slate-200 focus:ring-1 focus:ring-[#176B45]">' +
          '</div>' +
          '<div class="p-3 bg-amber-50/70 border border-amber-200/60 rounded-xl text-[11px] text-amber-800 flex items-start gap-2">' +
            '<span class="material-symbols-outlined text-amber-600 text-sm mt-0.5">info</span>' +
            '<span>Class assignment automatically syncs student gradebook, exam schedule, and attendance ledger.</span>' +
          '</div>' +
        '</div>' +
        '<div class="px-6 py-3.5 bg-slate-50 border-t border-slate-100 flex items-center justify-end gap-2">' +
          '<button type="button" id="btnCancelAssign" class="px-3.5 py-2 rounded-lg border border-slate-200 bg-white text-slate-700 text-xs font-medium cursor-pointer">Cancel</button>' +
          '<button type="button" id="btnConfirmAssign" class="px-4 py-2 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium cursor-pointer">Confirm Placement</button>' +
        '</div>' +
      '</div>';

      modal.innerHTML = modalHtml;
      modal.classList.remove('hidden');

      function closeModal() {
        modal.classList.add('hidden');
      }

      document.getElementById('closeAssignModal').addEventListener('click', closeModal);
      document.getElementById('btnCancelAssign').addEventListener('click', closeModal);

      document.getElementById('btnConfirmAssign').addEventListener('click', function () {
        var studentId = document.getElementById('modalStudentSelect').value;
        var targetClass = document.getElementById('modalTargetClassSelect').value;
        var reason = document.getElementById('modalTransferReason').value;

        fetch('/api/student-mgmt/assign', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ studentId: studentId, targetClass: targetClass, reason: reason })
        })
          .then(function (res) { return res.json(); })
          .then(function (res) {
            if (res.success) {
              toast(res.message);
              closeModal();
              fetchAssignData();
            } else {
              toast(res.error || 'Transfer failed', 'error');
            }
          })
          .catch(function () {
            toast('Failed to process transfer', 'error');
          });
      });
    }

    fetchAssignData();
  };

  // ─────────────────────────────────────────────────────────────
  // 4. DECLARE EXEMPTION CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initExemption = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { items: [], status: 'all', search: '' };

    function fetchExemptions() {
      fetch('/api/student-mgmt/exemptions?status=' + state.status + '&search=' + encodeURIComponent(state.search))
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.items = res.data || [];
          render();
        })
        .catch(function () {
          toast('Failed to load exemption records', 'error');
        });
    }

    function render() {
      var html = '<div class="space-y-6">' +
        '<div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-xs">' +
          '<div class="relative flex-1 max-w-md">' +
            '<span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 flex items-center"><span class="material-symbols-outlined text-lg">search</span></span>' +
            '<input type="text" id="exmSearch" value="' + state.search + '" placeholder="Search student name, ID, or subject..." class="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-200 focus:outline-none focus:ring-1 focus:ring-[#176B45] min-h-[38px]">' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            '<select id="exmStatus" class="text-xs py-2 px-3 rounded-lg border border-slate-200 bg-white font-medium text-slate-700 min-h-[38px] cursor-pointer">' +
              '<option value="all">All Exemptions</option>' +
              '<option value="active">Active Only</option>' +
              '<option value="under_review">Under Review</option>' +
            '</select>' +
            '<button type="button" id="btnNewExemption" class="px-4 py-2 rounded-lg bg-[#176B45] hover:bg-[#125638] text-white text-xs font-medium min-h-[38px] flex items-center gap-1.5 cursor-pointer shadow-xs">' +
              '<span class="material-symbols-outlined text-base">add</span><span>+ Declare Exemption</span>' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
          '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
            '<thead class="bg-slate-50 text-slate-600 font-medium uppercase tracking-wider text-[11px] border-b border-slate-200/80">' +
              '<tr>' +
                '<th class="px-4 py-3">Exemption ID</th>' +
                '<th class="px-4 py-3">Student</th>' +
                '<th class="px-4 py-3">Subject / Activity</th>' +
                '<th class="px-4 py-3">Category</th>' +
                '<th class="px-4 py-3">Duration</th>' +
                '<th class="px-4 py-3">Authorized Authority</th>' +
                '<th class="px-4 py-3">Status</th>' +
              '</tr>' +
            '</thead>' +
            '<tbody class="divide-y divide-slate-100 text-slate-700">';

      state.items.forEach(function (e) {
        var statusBadge = e.status === 'active' ?
          '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-[#176B45] border border-emerald-200">Active Exemption</span>' :
          '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Under Review</span>';

        html += '<tr class="hover:bg-slate-50/60 transition-colors">' +
          '<td class="px-4 py-3 font-mono text-[11px] text-slate-500">' + e.id + '</td>' +
          '<td class="px-4 py-3"><div class="font-medium text-slate-800">' + e.studentName + '</div><div class="text-[11px] text-slate-400 font-mono">' + e.studentId + '</div></td>' +
          '<td class="px-4 py-3 font-medium text-slate-800">' + e.subject + '</td>' +
          '<td class="px-4 py-3 text-slate-600">' + e.category + '</td>' +
          '<td class="px-4 py-3 text-slate-500">' + e.duration + '</td>' +
          '<td class="px-4 py-3 text-slate-700">' + e.authorizedBy + '</td>' +
          '<td class="px-4 py-3">' + statusBadge + '</td>' +
        '</tr>';
      });

      html += '</tbody></table></div></div></div>';
      root.innerHTML = html;

      document.getElementById('exmSearch').addEventListener('input', function (e) {
        state.search = e.target.value;
        fetchExemptions();
      });
      document.getElementById('exmStatus').addEventListener('change', function (e) {
        state.status = e.target.value;
        fetchExemptions();
      });
      document.getElementById('btnNewExemption').addEventListener('click', openDeclareModal);
    }

    function openDeclareModal() {
      var modal = document.getElementById('exmModal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'exmModal';
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs';
        document.body.appendChild(modal);
      }

      modal.innerHTML = '<div class="bg-white rounded-2xl border border-slate-200/80 shadow-xl max-w-md w-full p-6 space-y-4 text-xs">' +
        '<div class="flex items-center justify-between border-b pb-3">' +
          '<h3 class="font-medium text-sm text-slate-800">Declare Authorized Exemption</h3>' +
          '<button type="button" id="closeExmModal" class="text-slate-400 hover:text-slate-600 cursor-pointer"><span class="material-symbols-outlined text-lg">close</span></button>' +
        '</div>' +
        '<div><label class="block text-slate-500 mb-1">Student ID / Name</label><input type="text" id="modalExmStudent" value="2026-STD-0142 (Nrinphouneta Hok)" class="w-full p-2.5 border rounded-lg"></div>' +
        '<div><label class="block text-slate-500 mb-1">Exempted Subject</label><select id="modalExmSubject" class="w-full p-2.5 border rounded-lg bg-white"><option>Physical Education</option><option>Khmer Literature & History</option><option>Introductory ICT</option><option>Swimming</option></select></div>' +
        '<div><label class="block text-slate-500 mb-1">Exemption Category</label><input type="text" id="modalExmCategory" value="Medical / Physician Order" class="w-full p-2.5 border rounded-lg"></div>' +
        '<div><label class="block text-slate-500 mb-1">Justification Reason</label><textarea id="modalExmReason" class="w-full p-2.5 border rounded-lg" rows="2" placeholder="Official medical or ministerial documentation rationale..."></textarea></div>' +
        '<div class="flex justify-end gap-2 pt-2 border-t">' +
          '<button type="button" id="btnCancelExm" class="px-3.5 py-2 border rounded-lg">Cancel</button>' +
          '<button type="button" id="btnSaveExm" class="px-4 py-2 bg-[#176B45] text-white rounded-lg">Declare Exemption</button>' +
        '</div>' +
      '</div>';
      modal.classList.remove('hidden');

      document.getElementById('closeExmModal').onclick = function () { modal.classList.add('hidden'); };
      document.getElementById('btnCancelExm').onclick = function () { modal.classList.add('hidden'); };
      document.getElementById('btnSaveExm').onclick = function () {
        var sub = document.getElementById('modalExmSubject').value;
        var cat = document.getElementById('modalExmCategory').value;
        var rea = document.getElementById('modalExmReason').value || 'Medical clearance certificate attached.';
        fetch('/api/student-mgmt/exemptions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            studentId: '2026-STD-0142',
            studentName: 'Nrinphouneta Hok',
            class: '10A',
            subject: sub,
            category: cat,
            reason: rea,
            authorizedBy: (portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Officer')
          })
        }).then(function () {
          toast('Exemption officially recorded in registry!');
          modal.classList.add('hidden');
          fetchExemptions();
        });
      };
    }

    fetchExemptions();
  };

  // ─────────────────────────────────────────────────────────────
  // 6A. SUBJECT GPA BY EXAM CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initSubjectGpa = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { exam: 'Final Exam', subject: 'Advanced Mathematics', classFilter: 'all', data: [], summary: {} };

    function fetchData() {
      fetch('/api/student-mgmt/academic-results/by-exam?exam=' + encodeURIComponent(state.exam) + '&subject=' + encodeURIComponent(state.subject) + '&class=' + state.classFilter)
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.data = res.data || [];
          state.summary = res.summary || {};
          render();
        })
        .catch(function () {
          toast('Failed to load subject exam GPA results', 'error');
        });
    }

    function render() {
      var html = '<div class="space-y-6">' +
        '<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">' +
          '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">' +
            '<p class="text-xs text-slate-500">Class Average Score</p>' +
            '<p class="text-2xl font-medium text-slate-800 mt-1">' + (state.summary.averageScore || '—') + '%</p>' +
          '</div>' +
          '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">' +
            '<p class="text-xs text-slate-500">Highest Score</p>' +
            '<p class="text-2xl font-medium text-emerald-700 mt-1">' + (state.summary.highestScore || '—') + '%</p>' +
          '</div>' +
          '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">' +
            '<p class="text-xs text-slate-500">Lowest Score</p>' +
            '<p class="text-2xl font-medium text-slate-700 mt-1">' + (state.summary.lowestScore || '—') + '%</p>' +
          '</div>' +
          '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs">' +
            '<p class="text-xs text-slate-500">Passing Rate</p>' +
            '<p class="text-2xl font-medium text-[#176B45] mt-1">' + (state.summary.passingRate || '—') + '%</p>' +
          '</div>' +
        '</div>' +
        '<div class="flex flex-wrap items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-xs">' +
          '<div class="flex items-center gap-2">' +
            '<select id="gpaExamSelect" class="text-xs py-2 px-3 border rounded-lg bg-white font-medium text-slate-700 cursor-pointer">' +
              '<option value="Final Exam"' + (state.exam === 'Final Exam' ? ' selected' : '') + '>Final Exam (Semester 1)</option>' +
              '<option value="Mid-Term Exam"' + (state.exam === 'Mid-Term Exam' ? ' selected' : '') + '>Mid-Term Exam</option>' +
              '<option value="Quiz 1"' + (state.exam === 'Quiz 1' ? ' selected' : '') + '>Quiz 1</option>' +
            '</select>' +
            '<select id="gpaSubjectSelect" class="text-xs py-2 px-3 border rounded-lg bg-white font-medium text-slate-700 cursor-pointer">' +
              '<option value="Advanced Mathematics"' + (state.subject === 'Advanced Mathematics' ? ' selected' : '') + '>Advanced Mathematics</option>' +
              '<option value="Chemistry"' + (state.subject === 'Chemistry' ? ' selected' : '') + '>Chemistry</option>' +
              '<option value="English Literature"' + (state.subject === 'English Literature' ? ' selected' : '') + '>English Literature</option>' +
              '<option value="Physics"' + (state.subject === 'Physics' ? ' selected' : '') + '>Physics</option>' +
            '</select>' +
            '<select id="gpaClassSelect" class="text-xs py-2 px-3 border rounded-lg bg-white font-medium text-slate-700 cursor-pointer">' +
              '<option value="all">All Classes</option>' +
              '<option value="10A">Grade 10A</option>' +
              '<option value="10B">Grade 10B</option>' +
              '<option value="11A">Grade 11A</option>' +
            '</select>' +
          '</div>' +
          '<span class="text-xs text-slate-400 font-mono">Standard 4.0 Scale Formula Active</span>' +
        '</div>' +
        '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
          '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
            '<thead class="bg-slate-50 text-slate-600 font-medium uppercase text-[11px] border-b">' +
              '<tr>' +
                '<th class="px-4 py-3">Rank</th>' +
                '<th class="px-4 py-3">Student Name</th>' +
                '<th class="px-4 py-3">Student ID</th>' +
                '<th class="px-4 py-3">Class</th>' +
                '<th class="px-4 py-3">Raw Score</th>' +
                '<th class="px-4 py-3">Letter Grade</th>' +
                '<th class="px-4 py-3">GPA Points (4.0)</th>' +
                '<th class="px-4 py-3">Status</th>' +
              '</tr>' +
            '</thead>' +
            '<tbody class="divide-y divide-slate-100">';

      state.data.forEach(function (r) {
        html += '<tr class="hover:bg-slate-50/60">' +
          '<td class="px-4 py-3 font-medium text-slate-800">#' + r.classRank + '</td>' +
          '<td class="px-4 py-3 font-medium text-slate-800">' + r.studentName + '</td>' +
          '<td class="px-4 py-3 font-mono text-[11px] text-slate-400">' + r.studentId + '</td>' +
          '<td class="px-4 py-3">' + r.class + '</td>' +
          '<td class="px-4 py-3 font-medium text-slate-800">' + r.rawScore + '%</td>' +
          '<td class="px-4 py-3"><span class="px-2 py-0.5 rounded font-medium ' + (r.letterGrade === 'A' ? 'bg-emerald-50 text-[#176B45]' : (r.letterGrade === 'F' ? 'bg-rose-50 text-rose-700' : 'bg-slate-100 text-slate-700')) + '">' + r.letterGrade + '</span></td>' +
          '<td class="px-4 py-3 font-medium text-slate-800">' + r.gradePoints.toFixed(1) + '</td>' +
          '<td class="px-4 py-3">' + (r.isPassed ? '<span class="text-[#176B45] font-medium">Passed</span>' : '<span class="text-rose-600 font-medium">Failed</span>') + '</td>' +
        '</tr>';
      });

      html += '</tbody></table></div></div></div>';
      root.innerHTML = html;

      document.getElementById('gpaExamSelect').onchange = function (e) { state.exam = e.target.value; fetchData(); };
      document.getElementById('gpaSubjectSelect').onchange = function (e) { state.subject = e.target.value; fetchData(); };
      document.getElementById('gpaClassSelect').onchange = function (e) { state.classFilter = e.target.value; fetchData(); };
    }

    fetchData();
  };

  // ─────────────────────────────────────────────────────────────
  // 6B. SEMESTER GPA CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initSemesterGpa = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;

    fetch('/api/student-mgmt/academic-results/semester-gpa')
      .then(function (res) { return res.json(); })
      .then(function (res) {
        var records = res.data || [];
        var summary = res.summary || {};

        var html = '<div class="space-y-6">' +
          '<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">' +
            '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs"><p class="text-xs text-slate-500">Enrolled Students</p><p class="text-2xl font-medium text-slate-800 mt-1">' + summary.totalStudents + '</p></div>' +
            '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs"><p class="text-xs text-slate-500">Average Semester GPA</p><p class="text-2xl font-medium text-[#176B45] mt-1">' + summary.averageGpa + '</p></div>' +
            '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs"><p class="text-xs text-slate-500">Highest GPA</p><p class="text-2xl font-medium text-emerald-700 mt-1">' + summary.highestGpa + '</p></div>' +
            '<div class="bg-white p-4 rounded-xl border border-slate-200/80 shadow-xs"><p class="text-xs text-slate-500">Academic Standing</p><p class="text-sm font-medium text-slate-700 mt-2">100% Good / Honors</p></div>' +
          '</div>' +
          '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
            '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
              '<thead class="bg-slate-50 text-slate-600 font-medium uppercase text-[11px] border-b">' +
                '<tr>' +
                  '<th class="px-4 py-3">Rank</th>' +
                  '<th class="px-4 py-3">Student Name</th>' +
                  '<th class="px-4 py-3">Class</th>' +
                  '<th class="px-4 py-3">Credits (Earned/Att.)</th>' +
                  '<th class="px-4 py-3">Unweighted GPA</th>' +
                  '<th class="px-4 py-3">Weighted GPA (Honors)</th>' +
                  '<th class="px-4 py-3">Academic Standing</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody class="divide-y divide-slate-100">';

        records.forEach(function (r) {
          html += '<tr class="hover:bg-slate-50/60">' +
            '<td class="px-4 py-3 font-medium text-slate-800">#' + r.rank + '</td>' +
            '<td class="px-4 py-3 font-medium text-slate-800">' + r.studentName + '</td>' +
            '<td class="px-4 py-3">' + r.class + '</td>' +
            '<td class="px-4 py-3">' + r.creditsEarned + ' / ' + r.creditsAttempted + '</td>' +
            '<td class="px-4 py-3 font-medium text-slate-900">' + r.unweightedGpa.toFixed(2) + '</td>' +
            '<td class="px-4 py-3 font-medium text-emerald-800">' + r.weightedGpa.toFixed(2) + '</td>' +
            '<td class="px-4 py-3"><span class="px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-[#176B45] border border-emerald-200">' + r.standing + '</span></td>' +
          '</tr>';
        });

        html += '</tbody></table></div></div></div>';
        root.innerHTML = html;
      });
  };

  // ─────────────────────────────────────────────────────────────
  // 6C. STUDENT FAILED CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initFailed = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;

    fetch('/api/student-mgmt/academic-results/failed')
      .then(function (res) { return res.json(); })
      .then(function (res) {
        var failedList = res.data || [];
        var summary = res.summary || {};

        var html = '<div class="space-y-6">' +
          '<div class="p-4 bg-amber-50/70 border border-amber-200/80 rounded-xl flex items-start gap-3">' +
            '<span class="material-symbols-outlined text-amber-600">gavel</span>' +
            '<div class="text-xs text-amber-900">' +
              '<p class="font-medium">Official Failing Criteria: ' + summary.failingThreshold + '</p>' +
              '<p class="text-[11px] text-amber-700 mt-0.5">Students listed below have an active academic failure in at least one subject or cumulative semester GPA below the graduation threshold.</p>' +
            '</div>' +
          '</div>' +
          '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
            '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
              '<thead class="bg-slate-50 text-slate-600 font-medium uppercase text-[11px] border-b">' +
                '<tr>' +
                  '<th class="px-4 py-3">Student</th>' +
                  '<th class="px-4 py-3">Class</th>' +
                  '<th class="px-4 py-3">GPA</th>' +
                  '<th class="px-4 py-3">Failed Subject(s) &amp; Scores</th>' +
                  '<th class="px-4 py-3">Remedial Status</th>' +
                  '<th class="px-4 py-3">Intervention Action</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody class="divide-y divide-slate-100">';

        failedList.forEach(function (f) {
          var subjectsHtml = f.failedSubjects.map(function (s) {
            return '<div class="text-[11px] text-rose-700 font-medium">' + s.subject + ': ' + s.score + '% (' + s.grade + ')</div>';
          }).join('');

          html += '<tr class="hover:bg-slate-50/60">' +
            '<td class="px-4 py-3"><div class="font-medium text-slate-800">' + f.studentName + '</div><div class="text-[11px] text-slate-400 font-mono">' + f.studentId + '</div></td>' +
            '<td class="px-4 py-3">' + f.class + '</td>' +
            '<td class="px-4 py-3 font-medium text-rose-700">' + f.gpa + '</td>' +
            '<td class="px-4 py-3">' + subjectsHtml + '</td>' +
            '<td class="px-4 py-3"><span class="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">' + f.remedialStatus + '</span></td>' +
            '<td class="px-4 py-3 text-slate-600">' + f.interventionAction + '</td>' +
          '</tr>';
        });

        html += '</tbody></table></div></div></div>';
        root.innerHTML = html;
      });
  };

  // ─────────────────────────────────────────────────────────────
  // 7. ABSENCE STATISTICS CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initAbsenceStats = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    // Internal state
    var state = {
      kpis: { overallRate: 95.1, totalAbsences: 115, unexcusedTotal: 40, chronicAbsentees: 8 },
      students: [],
      filteredStudents: [],
      classComparison: [],
      cohortDistribution: [],
      absenceCategories: [],
      selectedIds: {},
      searchQuery: '',
      cohortFilter: 'all',
      riskFilter: 'all',
      noticeFilter: 'all',
      selectedTerm: 'term1',
      currentPage: 1,
      pageSize: 8
    };

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function computeFilteredStudents() {
      var q = state.searchQuery.toLowerCase().trim();
      var cFilter = state.cohortFilter;
      var rFilter = state.riskFilter;
      var nFilter = state.noticeFilter;

      state.filteredStudents = state.students.filter(function (s) {
        // Search query
        if (q) {
          var sName = (s.studentName || '').toLowerCase();
          var sId = (s.studentId || '').toLowerCase();
          var sCls = (s.class || '').toLowerCase();
          if (sName.indexOf(q) === -1 && sId.indexOf(q) === -1 && sCls.indexOf(q) === -1) {
            return false;
          }
        }

        // Cohort filter
        if (cFilter !== 'all') {
          var studentClassNorm = (s.class || '').replace(/^Grade\s+/i, '').trim().toLowerCase();
          var targetClassNorm = cFilter.replace(/^Grade\s+/i, '').trim().toLowerCase();
          if (studentClassNorm !== targetClassNorm) {
            return false;
          }
        }

        // Risk filter
        if (rFilter !== 'all') {
          var rLevel = (s.riskLevel || '').toLowerCase();
          if (rFilter === 'critical' && rLevel.indexOf('critical') === -1) return false;
          if (rFilter === 'moderate' && rLevel.indexOf('moderate') === -1) return false;
          if (rFilter === 'normal' && rLevel.indexOf('normal') === -1 && rLevel.indexOf('low') === -1) return false;
        }

        // Notice filter
        if (nFilter !== 'all') {
          var nStatus = (s.noticeStatus || (s.parentNotified ? 'Dispatched' : 'Pending Dispatch')).toLowerCase();
          if (nFilter === 'dispatched' && nStatus.indexOf('dispatched') === -1) return false;
          if (nFilter === 'delivered' && nStatus.indexOf('delivered') === -1) return false;
          if (nFilter === 'pending' && nStatus.indexOf('pending') === -1) return false;
        }

        return true;
      });

      // Clamp current page
      var maxPage = Math.max(1, Math.ceil(state.filteredStudents.length / state.pageSize));
      if (state.currentPage > maxPage) {
        state.currentPage = maxPage;
      }
    }

    function exportToCSV() {
      var records = state.filteredStudents.length ? state.filteredStudents : state.students;
      if (!records.length) {
        toast('No student records available for export.', 'error');
        return;
      }

      var headers = [
        'Student ID',
        'Student Name',
        'Class',
        'Grade',
        'Attendance Rate (%)',
        'Attended Days',
        'Total Absent Days',
        'Excused Absences',
        'Unexcused Absences',
        'Risk Assessment',
        'Parent Notice Status',
        'Notice Timestamp',
        'Guardian Contact'
      ];

      var csvRows = [headers.join(',')];

      records.forEach(function (s) {
        var row = [
          '"' + (s.studentId || '') + '"',
          '"' + (s.studentName || '').replace(/"/g, '""') + '"',
          '"' + (s.class || '') + '"',
          '"' + (s.grade || '') + '"',
          s.attendancePct || 0,
          s.attendedDays || 0,
          s.totalAbsentDays || 0,
          s.excusedAbsences || 0,
          s.unexcusedAbsences || 0,
          '"' + (s.riskLevel || 'Normal') + '"',
          '"' + (s.noticeStatus || (s.parentNotified ? 'Dispatched' : 'Pending Dispatch')) + '"',
          '"' + (s.noticeDate || 'AY 2025-26') + '"',
          '"' + ((s.guardian && s.guardian.phone) ? s.guardian.phone : '+855 12 000 000') + '"'
        ];
        csvRows.push(row.join(','));
      });

      var csvContent = '\uFEFF' + csvRows.join('\r\n');
      var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      var url = URL.createObjectURL(blob);
      var link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', 'NGIS_Absence_Risk_Register_' + new Date().toISOString().slice(0, 10) + '.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      toast('Risk audit exported successfully (.CSV)', 'success');
    }

    function openStudentLogModal(student) {
      var modalId = 'absenceLogModal';
      var existing = document.getElementById(modalId);
      if (existing) existing.remove();

      var logs = student.absenceLog || [
        { date: 'Nov 07, 2026', session: 'Full Day', category: 'Unexcused Truancy', verification: 'Unverified', action: 'Notice Sent' },
        { date: 'Nov 05, 2026', session: 'Morning', category: 'Medical Leave', verification: 'Doctor Note Verified', action: 'Excused' },
        { date: 'Nov 02, 2026', session: 'Afternoon', category: 'Family Emergency', verification: 'Parent Call Verified', action: 'Excused' }
      ];

      var modalHtml = '<div id="' + modalId + '" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs transition-opacity">' +
        '<div class="bg-white dark:bg-[#1c2420] border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-150">' +
          // Header
          '<div class="px-6 py-4 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">' +
            '<div class="flex items-center gap-3">' +
              '<div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-[#176B45] dark:text-emerald-400 flex items-center justify-center font-medium text-sm">' +
                escapeHtml(student.initials || 'ST') +
              '</div>' +
              '<div class="flex flex-col">' +
                '<h3 class="text-sm font-medium text-slate-800 dark:text-slate-100">' + escapeHtml(student.studentName) + '</h3>' +
                '<div class="flex items-center gap-2 text-xs text-slate-400 font-mono">' +
                  '<span>' + escapeHtml(student.studentId) + '</span>' +
                  '<span>&bull;</span>' +
                  '<span class="text-slate-600 dark:text-slate-300 font-sans">Class ' + escapeHtml(student.class) + ' (' + escapeHtml(student.grade || 'Grade 10') + ')</span>' +
                '</div>' +
              '</div>' +
            '</div>' +
            '<button type="button" id="closeAbsenceLogModal" class="w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">' +
              '<span class="material-symbols-outlined text-[20px]">close</span>' +
            '</button>' +
          '</div>' +

          // Metrics Tiles
          '<div class="p-6 overflow-y-auto space-y-6">' +
            '<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">' +
              '<div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-100 dark:border-slate-800 text-center">' +
                '<span class="text-[10px] text-slate-400 uppercase tracking-wider font-medium">Attendance Rate</span>' +
                '<p class="text-lg font-medium text-[#176B45] dark:text-emerald-400 mt-0.5">' + student.attendancePct + '%</p>' +
              '</div>' +
              '<div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-100 dark:border-slate-800 text-center">' +
                '<span class="text-[10px] text-slate-400 uppercase tracking-wider font-medium">Attended Days</span>' +
                '<p class="text-lg font-medium text-slate-800 dark:text-slate-100 mt-0.5">' + student.attendedDays + ' / 80</p>' +
              '</div>' +
              '<div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-100 dark:border-slate-800 text-center">' +
                '<span class="text-[10px] text-slate-400 uppercase tracking-wider font-medium">Excused Leaves</span>' +
                '<p class="text-lg font-medium text-emerald-700 dark:text-emerald-400 mt-0.5">' + student.excusedAbsences + ' days</p>' +
              '</div>' +
              '<div class="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-100 dark:border-slate-800 text-center">' +
                '<span class="text-[10px] text-slate-400 uppercase tracking-wider font-medium">Unexcused</span>' +
                '<p class="text-lg font-medium text-rose-700 dark:text-rose-400 mt-0.5">' + student.unexcusedAbsences + ' days</p>' +
              '</div>' +
            '</div>' +

            // Log Table
            '<div class="space-y-2.5">' +
              '<div class="flex items-center justify-between">' +
                '<h4 class="text-xs font-medium text-slate-700 dark:text-slate-300 uppercase tracking-wider">Attendance Incidents &amp; Evidence Log</h4>' +
                '<span class="text-[11px] text-slate-400">Term 1 (AY 2025–2026)</span>' +
              '</div>' +
              '<div class="border border-slate-200/80 dark:border-slate-800 rounded-lg overflow-hidden">' +
                '<table class="w-full text-left text-xs">' +
                  '<thead class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-medium border-b border-slate-200/80 dark:border-slate-800">' +
                    '<tr>' +
                      '<th class="px-3.5 py-2.5">Date</th>' +
                      '<th class="px-3.5 py-2.5">Session</th>' +
                      '<th class="px-3.5 py-2.5">Category</th>' +
                      '<th class="px-3.5 py-2.5">Verification</th>' +
                      '<th class="px-3.5 py-2.5 text-right">Action</th>' +
                    '</tr>' +
                  '</thead>' +
                  '<tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-200">';

      logs.forEach(function (log) {
        var isUnexcused = log.category.indexOf('Truancy') !== -1 || log.category.indexOf('Unexcused') !== -1;
        modalHtml += '<tr class="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">' +
          '<td class="px-3.5 py-2.5 font-medium">' + escapeHtml(log.date) + '</td>' +
          '<td class="px-3.5 py-2.5 text-slate-500">' + escapeHtml(log.session) + '</td>' +
          '<td class="px-3.5 py-2.5">' +
            (isUnexcused ?
              '<span class="inline-flex items-center gap-1 text-rose-700 dark:text-rose-400 font-medium"><span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span>' + escapeHtml(log.category) + '</span>' :
              '<span class="inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-400 font-medium"><span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>' + escapeHtml(log.category) + '</span>') +
          '</td>' +
          '<td class="px-3.5 py-2.5 text-slate-500 dark:text-slate-400">' + escapeHtml(log.verification) + '</td>' +
          '<td class="px-3.5 py-2.5 text-right text-slate-600 dark:text-slate-300 font-medium">' + escapeHtml(log.action) + '</td>' +
        '</tr>';
      });

      modalHtml += '</tbody></table></div></div></div>' +

          // Footer
          '<div class="px-6 py-3.5 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">' +
            '<button type="button" id="modalContactGuardianBtn" class="px-3 py-1.5 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-[#176B45] dark:text-emerald-400 hover:bg-emerald-100 dark:hover:bg-emerald-900/50 text-xs font-medium flex items-center gap-1.5 transition-colors">' +
              '<span class="material-symbols-outlined text-[16px]">outgoing_mail</span>' +
              '<span>Dispatch Notice</span>' +
            '</button>' +
            '<button type="button" id="modalCloseActionBtn" class="px-4 py-1.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700/60 text-xs font-medium transition-colors">' +
              'Close' +
            '</button>' +
          '</div>' +
        '</div>' +
      '</div>';

      document.body.insertAdjacentHTML('beforeend', modalHtml);

      var modalEl = document.getElementById(modalId);
      var closeBtn = document.getElementById('closeAbsenceLogModal');
      var closeActionBtn = document.getElementById('modalCloseActionBtn');
      var contactBtn = document.getElementById('modalContactGuardianBtn');

      function closeModal() {
        if (modalEl) modalEl.remove();
      }

      if (closeBtn) closeBtn.onclick = closeModal;
      if (closeActionBtn) closeActionBtn.onclick = closeModal;
      if (modalEl) {
        modalEl.onclick = function (e) {
          if (e.target === modalEl) closeModal();
        };
      }

      if (contactBtn) {
        contactBtn.onclick = function () {
          closeModal();
          openContactGuardianModal(student);
        };
      }
    }

    function openContactGuardianModal(student) {
      var modalId = 'contactGuardianModal';
      var existing = document.getElementById(modalId);
      if (existing) existing.remove();

      var g = student.guardian || {
        name: 'Guardian of ' + student.studentName,
        phone: '+855 12 889 912',
        email: 'parent@ngis.edu.kh'
      };

      var modalHtml = '<div id="' + modalId + '" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs transition-opacity">' +
        '<div class="bg-white dark:bg-[#1c2420] border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl w-full max-w-md overflow-hidden flex flex-col animate-in fade-in zoom-in-95 duration-150">' +
          '<div class="px-5 py-4 bg-slate-50 dark:bg-slate-800/60 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">' +
            '<div class="flex items-center gap-2">' +
              '<span class="material-symbols-outlined text-[20px] text-[#176B45]">contact_phone</span>' +
              '<h3 class="text-sm font-medium text-slate-800 dark:text-slate-100">Guardian Contact &amp; Intervention</h3>' +
            '</div>' +
            '<button type="button" id="closeGuardianModal" class="w-7 h-7 rounded-lg flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">' +
              '<span class="material-symbols-outlined text-[18px]">close</span>' +
            '</button>' +
          '</div>' +

          '<div class="p-5 space-y-4">' +
            '<div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-100 dark:border-slate-800 space-y-2">' +
              '<div class="flex items-center justify-between text-xs">' +
                '<span class="text-slate-400">Student:</span>' +
                '<span class="font-medium text-slate-800 dark:text-slate-100">' + escapeHtml(student.studentName) + ' (' + escapeHtml(student.studentId) + ')</span>' +
              '</div>' +
              '<div class="flex items-center justify-between text-xs">' +
                '<span class="text-slate-400">Guardian Name:</span>' +
                '<span class="font-medium text-slate-700 dark:text-slate-300">' + escapeHtml(g.name) + '</span>' +
              '</div>' +
              '<div class="flex items-center justify-between text-xs">' +
                '<span class="text-slate-400">Phone Number:</span>' +
                '<span class="font-mono font-medium text-[#176B45] dark:text-emerald-400">' + escapeHtml(g.phone) + '</span>' +
              '</div>' +
              '<div class="flex items-center justify-between text-xs">' +
                '<span class="text-slate-400">Email Address:</span>' +
                '<span class="text-slate-600 dark:text-slate-300 font-mono text-[11px]">' + escapeHtml(g.email) + '</span>' +
              '</div>' +
            '</div>' +

            '<div class="space-y-2">' +
              '<label class="text-xs font-medium text-slate-700 dark:text-slate-300">Intervention Message Template</label>' +
              '<textarea id="guardianMessageInput" class="w-full text-xs p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-1 focus:ring-[#176B45]" rows="3">' +
                'NGIS Notice: ' + escapeHtml(student.studentName) + ' has accumulated ' + student.unexcusedAbsences + ' unexcused absences (Attendance: ' + student.attendancePct + '%). Please contact administration.' +
              '</textarea>' +
            '</div>' +

            '<div class="flex items-center gap-2">' +
              '<label class="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-300 cursor-pointer">' +
                '<input type="checkbox" id="sendSmsCheck" checked class="rounded text-[#176B45] focus:ring-0">' +
                '<span>SMS Alert</span>' +
              '</label>' +
              '<label class="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-300 cursor-pointer ml-3">' +
                '<input type="checkbox" id="sendTelegramCheck" checked class="rounded text-[#176B45] focus:ring-0">' +
                '<span>Telegram Bot</span>' +
              '</label>' +
            '</div>' +
          '</div>' +

          '<div class="px-5 py-3.5 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end gap-2">' +
            '<button type="button" id="cancelGuardianModal" class="px-3.5 py-1.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-50 text-xs font-medium transition-colors">' +
              'Cancel' +
            '</button>' +
            '<button type="button" id="confirmDispatchNotice" class="px-4 py-1.5 rounded-lg bg-[#176B45] hover:bg-[#14532D] text-white text-xs font-medium shadow-xs transition-colors flex items-center gap-1.5">' +
              '<span class="material-symbols-outlined text-[16px]">send</span>' +
              '<span>Dispatch Notice</span>' +
            '</button>' +
          '</div>' +
        '</div>' +
      '</div>';

      document.body.insertAdjacentHTML('beforeend', modalHtml);

      var modalEl = document.getElementById(modalId);
      var closeBtn = document.getElementById('closeGuardianModal');
      var cancelBtn = document.getElementById('cancelGuardianModal');
      var confirmBtn = document.getElementById('confirmDispatchNotice');

      function closeModal() {
        if (modalEl) modalEl.remove();
      }

      if (closeBtn) closeBtn.onclick = closeModal;
      if (cancelBtn) cancelBtn.onclick = closeModal;
      if (modalEl) {
        modalEl.onclick = function (e) {
          if (e.target === modalEl) closeModal();
        };
      }

      if (confirmBtn) {
        confirmBtn.onclick = function () {
          confirmBtn.disabled = true;
          confirmBtn.innerHTML = '<span class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span> Dispatching...';

          fetch('/api/student-mgmt/absence-stats/notify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              studentIds: [student.studentId],
              channel: 'sms_telegram'
            })
          })
          .then(function (res) { return res.json(); })
          .then(function () {
            student.parentNotified = true;
            student.noticeStatus = 'Dispatched';
            student.noticeDate = 'Today, ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            closeModal();
            renderTableSection();
            toast('Notice successfully dispatched to ' + g.name + ' (' + g.phone + ')', 'success');
          })
          .catch(function () {
            closeModal();
            toast('Notice logged and dispatched.', 'success');
          });
        };
      }
    }

    function renderDashboard() {
      computeFilteredStudents();
      var k = state.kpis;

      var html = '<div class="flex flex-col gap-6 w-full max-w-[1600px] mx-auto text-slate-800 dark:text-slate-100 font-sans">' +

        // 1. Top Executive Control Bar
        '<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">' +
          '<div class="flex flex-col gap-1">' +
            '<h1 class="text-xl md:text-2xl font-medium text-slate-900 dark:text-slate-100 tracking-tight">' +
              'Absence Statistics &amp; Attendance Risk Register' +
            '</h1>' +
            '<p class="text-xs text-slate-500 dark:text-slate-400 font-normal">' +
              'Institutional attendance telemetry, chronic absenteeism tracking, and parent intervention register.' +
            '</p>' +
          '</div>' +

          '<div class="flex flex-wrap items-center gap-3">' +
            // Academic Term Dropdown
            '<div class="relative bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800 shadow-xs rounded-xl flex items-center px-3.5 py-2">' +
              '<span class="material-symbols-outlined text-[18px] text-slate-400 mr-2.5">event_note</span>' +
              '<div class="flex flex-col">' +
                '<span class="text-[10px] text-slate-400 uppercase tracking-wider font-medium">Academic Term</span>' +
                '<select id="termSelector" class="bg-transparent text-xs font-medium text-slate-800 dark:text-slate-100 focus:outline-none cursor-pointer pr-4">' +
                  '<option value="term1" ' + (state.selectedTerm === 'term1' ? 'selected' : '') + '>Term 1 (AY 2025–2026)</option>' +
                  '<option value="term2" ' + (state.selectedTerm === 'term2' ? 'selected' : '') + '>Term 2 (AY 2025–2026)</option>' +
                  '<option value="year" ' + (state.selectedTerm === 'year' ? 'selected' : '') + '>Full Academic Year 2025–2026</option>' +
                '</select>' +
              '</div>' +
            '</div>' +

            // Export CSV Button
            '<button type="button" id="exportRiskCsvBtn" class="h-10 px-4 rounded-xl bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800 text-slate-700 dark:text-slate-200 shadow-xs hover:bg-slate-50 dark:hover:bg-slate-800/60 active:scale-95 transition-all flex items-center gap-2 text-xs font-medium">' +
              '<span class="material-symbols-outlined text-[18px] text-slate-500">download</span>' +
              '<span>Export Risk Audit (.CSV)</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        // 2. Executive KPI & Telemetry Cards (4-column grid)
        '<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">' +
          // Card 1: Attendance Rate
          '<div class="bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl p-5 shadow-xs flex flex-col justify-between relative overflow-hidden">' +
            '<div class="flex items-start justify-between">' +
              '<div class="flex flex-col">' +
                '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">Overall Attendance Rate</span>' +
                '<div class="flex items-baseline gap-2 mt-1">' +
                  '<span class="text-3xl font-medium text-[#176B45] dark:text-emerald-400 tracking-tight">' + k.overallRate + '%</span>' +
                  '<span class="inline-flex items-center text-xs font-medium text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-1.5 py-0.5 rounded">' +
                    '<span class="material-symbols-outlined text-[14px]">arrow_upward</span>+0.4%' +
                  '</span>' +
                '</div>' +
              '</div>' +
              '<div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-[#176B45] dark:text-emerald-400 flex items-center justify-center">' +
                '<span class="material-symbols-outlined text-[22px]">verified_user</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-4 pt-3 flex flex-col gap-1.5 border-t border-slate-100 dark:border-slate-800/60">' +
              '<div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">' +
                '<div class="bg-[#176B45] h-full rounded-full transition-all duration-700" style="width: ' + k.overallRate + '%"></div>' +
              '</div>' +
              '<div class="flex justify-between items-center text-slate-400 text-[11px] pt-1">' +
                '<span>Benchmark Target: 95.0%</span>' +
                '<span class="text-emerald-700 dark:text-emerald-400 font-medium">On Target</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Card 2: Total Absences
          '<div class="bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl p-5 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-start justify-between">' +
              '<div class="flex flex-col">' +
                '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">Total Absences (Term)</span>' +
                '<div class="flex items-baseline gap-2 mt-1">' +
                  '<span class="text-3xl font-medium text-slate-800 dark:text-slate-100 tracking-tight">' + k.totalAbsences + '</span>' +
                  '<span class="text-xs text-slate-500 dark:text-slate-400 font-medium">days logged</span>' +
                '</div>' +
              '</div>' +
              '<div class="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center">' +
                '<span class="material-symbols-outlined text-[22px]">event_busy</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-4 pt-3 flex flex-col gap-1.5 border-t border-slate-100 dark:border-slate-800/60">' +
              '<div class="flex h-2 w-full rounded-full overflow-hidden bg-slate-100 dark:bg-slate-800">' +
                '<div class="bg-emerald-600 h-full" style="width: 65.2%" title="Excused: 65.2%"></div>' +
                '<div class="bg-amber-500 h-full" style="width: 34.8%" title="Unexcused: 34.8%"></div>' +
              '</div>' +
              '<div class="flex justify-between items-center text-slate-400 text-[11px] pt-1">' +
                '<span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-600"></span>65% Excused</span>' +
                '<span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500"></span>35% Unexcused</span>' +
              '</div>' +
            '</div>' +
          '</div>' +

          // Card 3: Unexcused Absences
          '<div class="bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl p-5 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-start justify-between">' +
              '<div class="flex flex-col">' +
                '<span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 dark:text-slate-400">Unexcused Absences</span>' +
                '<div class="flex items-baseline gap-2 mt-1">' +
                  '<span class="text-3xl font-medium text-amber-700 dark:text-amber-400 tracking-tight">' + k.unexcusedTotal + '</span>' +
                  '<span class="text-xs text-slate-500 dark:text-slate-400 font-medium">days</span>' +
                '</div>' +
              '</div>' +
              '<div class="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 flex items-center justify-center">' +
                '<span class="material-symbols-outlined text-[22px]">warning</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-4 pt-3 flex items-center justify-between text-[11px] border-t border-slate-100 dark:border-slate-800/60">' +
              '<span class="text-slate-500 dark:text-slate-400">Policy Threshold: &gt;3 Days</span>' +
              '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-800/60">Action Required</span>' +
            '</div>' +
          '</div>' +

          // Card 4: Chronic Absenteeism Flag
          '<div class="bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl p-5 shadow-xs flex flex-col justify-between">' +
            '<div class="flex items-start justify-between">' +
              '<div class="flex flex-col">' +
                '<span class="text-[11px] font-medium uppercase tracking-wider text-rose-700 dark:text-rose-400">Chronic Absenteeism Flag</span>' +
                '<div class="flex items-baseline gap-2 mt-1">' +
                  '<span class="text-3xl font-medium text-rose-700 dark:text-rose-400 tracking-tight">' + k.chronicAbsentees + '</span>' +
                  '<span class="text-xs text-rose-600 dark:text-rose-400 font-medium">students flagged</span>' +
                '</div>' +
              '</div>' +
              '<div class="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 flex items-center justify-center">' +
                '<span class="material-symbols-outlined text-[22px]">emergency_home</span>' +
              '</div>' +
            '</div>' +
            '<div class="mt-4 pt-3 flex items-center justify-between text-[11px] border-t border-slate-100 dark:border-slate-800/60">' +
              '<span class="text-slate-500 dark:text-slate-400">&ge; 10% School Term Days</span>' +
              '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800/60">Protocol Active</span>' +
            '</div>' +
          '</div>' +
        '</div>' +

        // 3. Visual Analytics & Category Breakdown (Split Bento View)
        '<div class="grid grid-cols-1 lg:grid-cols-12 gap-5">' +
          // Left: Cohort Distribution (7 cols)
          '<div class="lg:col-span-7 bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl p-6 shadow-xs flex flex-col justify-between gap-5">' +
            '<div class="flex items-center justify-between">' +
              '<div class="flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[20px] text-[#176B45]">bar_chart</span>' +
                '<h2 class="text-sm font-medium text-slate-800 dark:text-slate-100">Attendance Distribution by Cohort</h2>' +
              '</div>' +
              '<span class="px-2.5 py-1 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 text-[11px] font-medium">' +
                'Target: 95.0%' +
              '</span>' +
            '</div>' +

            '<div class="flex flex-col gap-3.5">';

      var cohorts = (state.cohortDistribution && state.cohortDistribution.length) ? state.cohortDistribution : [
        { cohort: 'Grade 12A', enrolled: 178, absences: 1, attendancePct: 97.0 },
        { cohort: 'Grade 10B', enrolled: 182, absences: 7, attendancePct: 96.1 },
        { cohort: 'Grade 10A', enrolled: 180, absences: 21, attendancePct: 95.4 },
        { cohort: 'Grade 11A', enrolled: 174, absences: 18, attendancePct: 94.8 },
        { cohort: 'Grade 11B', enrolled: 172, absences: 32, attendancePct: 93.2 }
      ];

      cohorts.forEach(function (c) {
        var barColor = c.attendancePct >= 96 ? 'bg-[#176B45]' : (c.attendancePct >= 95 ? 'bg-emerald-600' : (c.attendancePct >= 94 ? 'bg-[#176B45]/80' : 'bg-amber-500'));
        var textColor = c.attendancePct >= 95 ? 'text-[#176B45] dark:text-emerald-400' : (c.attendancePct >= 94 ? 'text-slate-800 dark:text-slate-200' : 'text-amber-700 dark:text-amber-400');

        html += '<div class="flex flex-col gap-1">' +
          '<div class="flex justify-between items-center text-xs">' +
            '<div class="flex items-center gap-2">' +
              '<span class="font-medium text-slate-800 dark:text-slate-100 w-20">' + escapeHtml(c.cohort) + '</span>' +
              '<span class="text-slate-400 text-[11px]">' + c.enrolled + ' students</span>' +
            '</div>' +
            '<div class="flex items-center gap-3">' +
              '<span class="text-slate-400 text-[11px]">' + c.absences + ' ' + (c.absences === 1 ? 'absence' : 'absences') + '</span>' +
              '<span class="font-medium ' + textColor + '">' + c.attendancePct.toFixed(1) + '%</span>' +
            '</div>' +
          '</div>' +
          '<div class="w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">' +
            '<div class="' + barColor + ' h-full rounded-full transition-all duration-500" style="width: ' + c.attendancePct + '%"></div>' +
          '</div>' +
        '</div>';
      });

      html += '</div>' +
            '<div class="flex items-center justify-between pt-2 text-slate-400 text-[11px] border-t border-slate-100 dark:border-slate-800">' +
              '<span>Live synchronisation across 5 academic cohorts</span>' +
              '<span class="text-[#176B45] dark:text-emerald-400 font-medium">Telemetry Healthy</span>' +
            '</div>' +
          '</div>' +

          // Right: Absence Category (5 cols)
          '<div class="lg:col-span-5 bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl p-6 shadow-xs flex flex-col justify-between gap-5">' +
            '<div class="flex items-center justify-between">' +
              '<div class="flex flex-col">' +
                '<div class="flex items-center gap-2">' +
                  '<span class="material-symbols-outlined text-[20px] text-emerald-600">pie_chart</span>' +
                  '<h2 class="text-sm font-medium text-slate-800 dark:text-slate-100">Absence Classification</h2>' +
                '</div>' +
                '<span class="text-xs text-slate-400 mt-0.5">Verification status &amp; root causes breakdown</span>' +
              '</div>' +
              '<span class="material-symbols-outlined text-slate-400 cursor-pointer hover:text-slate-600 text-[18px]" title="Detailed breakdown of documented leaves versus unexcused incidents">info</span>' +
            '</div>' +

            '<div class="flex flex-col gap-3">' +
              // Medical
              '<div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-lg flex items-center justify-between border border-slate-100 dark:border-slate-800">' +
                '<div class="flex items-center gap-3">' +
                  '<div class="w-3 h-3 rounded-full bg-emerald-600 shrink-0"></div>' +
                  '<div class="flex flex-col">' +
                    '<span class="text-xs font-medium text-slate-800 dark:text-slate-100">Medical &amp; Authorized Leaves</span>' +
                    '<span class="text-[11px] text-slate-400">Clinic notes &amp; guardian approvals</span>' +
                  '</div>' +
                '</div>' +
                '<div class="text-right">' +
                  '<div class="text-xs font-medium text-slate-800 dark:text-slate-100">75 days</div>' +
                  '<span class="text-[11px] font-medium text-emerald-700 dark:text-emerald-400">65.2%</span>' +
                '</div>' +
              '</div>' +

              // Unexcused Truancy
              '<div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-lg flex items-center justify-between border border-slate-100 dark:border-slate-800">' +
                '<div class="flex items-center gap-3">' +
                  '<div class="w-3 h-3 rounded-full bg-rose-600 shrink-0"></div>' +
                  '<div class="flex flex-col">' +
                    '<span class="text-xs font-medium text-slate-800 dark:text-slate-100">Unexcused Truancy</span>' +
                    '<span class="text-[11px] text-slate-400">Absent without prior notice</span>' +
                  '</div>' +
                '</div>' +
                '<div class="text-right">' +
                  '<div class="text-xs font-medium text-rose-700 dark:text-rose-400">25 days</div>' +
                  '<span class="text-[11px] font-medium text-rose-600 dark:text-rose-400">21.7%</span>' +
                '</div>' +
              '</div>' +

              // Unverified
              '<div class="p-3.5 bg-slate-50 dark:bg-slate-800/40 rounded-lg flex items-center justify-between border border-slate-100 dark:border-slate-800">' +
                '<div class="flex items-center gap-3">' +
                  '<div class="w-3 h-3 rounded-full bg-amber-500 shrink-0"></div>' +
                  '<div class="flex flex-col">' +
                    '<span class="text-xs font-medium text-slate-800 dark:text-slate-100">Unverified / Late Submission</span>' +
                    '<span class="text-[11px] text-slate-400">Pending administrative review</span>' +
                  '</div>' +
                '</div>' +
                '<div class="text-right">' +
                  '<div class="text-xs font-medium text-amber-700 dark:text-amber-400">15 days</div>' +
                  '<span class="text-[11px] font-medium text-amber-600 dark:text-amber-400">13.1%</span>' +
                '</div>' +
              '</div>' +
            '</div>' +

            '<div class="flex items-center justify-between pt-2 text-slate-400 text-[11px] border-t border-slate-100 dark:border-slate-800">' +
              '<span>Total 115 absence incidents recorded</span>' +
              '<span class="text-emerald-700 dark:text-emerald-400 font-medium">Verified: 65.2%</span>' +
            '</div>' +
          '</div>' +
        '</div>' +

        // 4. High-Density Risk Register Table Container
        '<div class="bg-white dark:bg-[#1c2420] border border-slate-200/80 dark:border-slate-800/80 rounded-xl shadow-xs overflow-hidden flex flex-col" id="riskRegisterCard">' +
          // Filter Toolbar
          '<div class="p-4 md:p-5 flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4 bg-slate-50/50 dark:bg-slate-800/30 border-b border-slate-100 dark:border-slate-800">' +
            // Search Box
            '<div class="relative flex-1 max-w-lg">' +
              '<span class="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px]">search</span>' +
              '<input type="text" id="studentSearchInput" value="' + escapeHtml(state.searchQuery) + '" ' +
                'placeholder="Search student name, ID (e.g. 2026-STD-0174), or class..." ' +
                'class="w-full h-10 pl-10 pr-4 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 placeholder:text-slate-400 text-xs rounded-xl border border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45] transition-all">' +
            '</div>' +

            // Action Filters
            '<div class="flex flex-wrap items-center gap-2.5">' +
              // Cohort Filter
              '<div class="relative">' +
                '<select id="cohortFilter" class="h-10 pl-3 pr-8 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 appearance-none cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#176B45]">' +
                  '<option value="all" ' + (state.cohortFilter === 'all' ? 'selected' : '') + '>All Classes / Cohorts</option>' +
                  '<option value="10A" ' + (state.cohortFilter === '10A' ? 'selected' : '') + '>Grade 10A</option>' +
                  '<option value="10B" ' + (state.cohortFilter === '10B' ? 'selected' : '') + '>Grade 10B</option>' +
                  '<option value="11A" ' + (state.cohortFilter === '11A' ? 'selected' : '') + '>Grade 11A</option>' +
                  '<option value="11B" ' + (state.cohortFilter === '11B' ? 'selected' : '') + '>Grade 11B</option>' +
                  '<option value="11C" ' + (state.cohortFilter === '11C' ? 'selected' : '') + '>Grade 11C</option>' +
                  '<option value="12A" ' + (state.cohortFilter === '12A' ? 'selected' : '') + '>Grade 12A</option>' +
                '</select>' +
                '<span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">arrow_drop_down</span>' +
              '</div>' +

              // Risk Filter
              '<div class="relative">' +
                '<select id="riskFilter" class="h-10 pl-3 pr-8 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 appearance-none cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#176B45]">' +
                  '<option value="all" ' + (state.riskFilter === 'all' ? 'selected' : '') + '>All Risk Levels</option>' +
                  '<option value="critical" ' + (state.riskFilter === 'critical' ? 'selected' : '') + '>Critical (&gt;5 Days)</option>' +
                  '<option value="moderate" ' + (state.riskFilter === 'moderate' ? 'selected' : '') + '>Moderate (2–4 Days)</option>' +
                  '<option value="normal" ' + (state.riskFilter === 'normal' ? 'selected' : '') + '>Low Risk / Normal</option>' +
                '</select>' +
                '<span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">arrow_drop_down</span>' +
              '</div>' +

              // Parent Notice Filter
              '<div class="relative">' +
                '<select id="noticeFilter" class="h-10 pl-3 pr-8 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-xs font-medium rounded-xl border border-slate-200 dark:border-slate-700 appearance-none cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#176B45]">' +
                  '<option value="all" ' + (state.noticeFilter === 'all' ? 'selected' : '') + '>All Notice Statuses</option>' +
                  '<option value="dispatched" ' + (state.noticeFilter === 'dispatched' ? 'selected' : '') + '>Dispatched</option>' +
                  '<option value="delivered" ' + (state.noticeFilter === 'delivered' ? 'selected' : '') + '>Delivered</option>' +
                  '<option value="pending" ' + (state.noticeFilter === 'pending' ? 'selected' : '') + '>Pending Dispatch</option>' +
                '</select>' +
                '<span class="material-symbols-outlined absolute right-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-[18px] pointer-events-none">arrow_drop_down</span>' +
              '</div>' +

              // Reset Filter Button
              '<button type="button" id="resetFiltersBtn" class="w-10 h-10 flex items-center justify-center rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors" title="Reset all filters">' +
                '<span class="material-symbols-outlined text-[18px]">restart_alt</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          // Subheader Telemetry & Batch Action Bar
          '<div id="tableTelemetrySubheader" class="px-5 py-2.5 bg-slate-50/80 dark:bg-slate-800/40 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs">' +
            '<div class="flex items-center gap-2">' +
              '<span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>' +
              '<span class="text-slate-600 dark:text-slate-300 font-medium" id="tableFilterCountText">' +
                'Showing ' + state.filteredStudents.length + ' student records requiring institutional oversight' +
              '</span>' +
            '</div>' +
            '<div id="selectionBatchActions" class="hidden flex items-center gap-2">' +
              '<span class="text-xs text-slate-500 font-medium" id="selectedCountBadge">0 selected</span>' +
              '<button type="button" id="batchNotifyBtn" class="px-3 py-1 rounded-lg bg-[#176B45] text-white text-xs font-medium hover:bg-[#14532D] transition-colors flex items-center gap-1">' +
                '<span class="material-symbols-outlined text-[15px]">outgoing_mail</span>' +
                '<span>Dispatch Notices</span>' +
              '</button>' +
              '<button type="button" id="clearSelectionBtn" class="px-2 py-1 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-medium hover:bg-slate-200 transition-colors">' +
                'Deselect' +
              '</button>' +
            '</div>' +
            '<div class="hidden sm:flex items-center gap-1 text-slate-400 text-[11px] font-mono">' +
              '<span>Sorted by Unexcused Absences</span>' +
            '</div>' +
          '</div>' +

          // Dynamic Table Body Container
          '<div id="riskTableContentArea" class="overflow-x-auto w-full">' +
            // Populated by renderTableSection()
          '</div>' +

          // Table Footer & Pagination
          '<div id="riskTableFooter" class="p-4 bg-white dark:bg-[#1c2420] border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">' +
            // Populated by renderTableSection()
          '</div>' +
        '</div>' +

      '</div>';

      root.innerHTML = html;

      // Attach global listeners
      attachDashboardListeners();
      renderTableSection();
    }

    function renderTableSection() {
      computeFilteredStudents();

      var tableContainer = document.getElementById('riskTableContentArea');
      var footerContainer = document.getElementById('riskTableFooter');
      var countText = document.getElementById('tableFilterCountText');
      var batchContainer = document.getElementById('selectionBatchActions');
      var selectedBadge = document.getElementById('selectedCountBadge');

      if (!tableContainer || !footerContainer) return;

      var total = state.filteredStudents.length;
      var pageSize = state.pageSize;
      var startIndex = (state.currentPage - 1) * pageSize;
      var endIndex = Math.min(startIndex + pageSize, total);
      var pageItems = state.filteredStudents.slice(startIndex, endIndex);

      // Update count text
      if (countText) {
        countText.innerHTML = 'Showing <span class="font-medium text-slate-800 dark:text-slate-100">' + total + '</span> student records requiring institutional oversight';
      }

      // Check selected count
      var selectedCount = Object.keys(state.selectedIds).length;
      if (batchContainer) {
        if (selectedCount > 0) {
          batchContainer.classList.remove('hidden');
          if (selectedBadge) selectedBadge.textContent = selectedCount + ' selected';
        } else {
          batchContainer.classList.add('hidden');
        }
      }

      if (total === 0) {
        tableContainer.innerHTML = '<div class="py-16 text-center text-slate-400 flex flex-col items-center justify-center gap-2">' +
          '<span class="material-symbols-outlined text-[36px] text-slate-300">manage_search</span>' +
          '<p class="text-xs font-medium">No student attendance records match the selected criteria.</p>' +
          '<button type="button" id="emptyStateResetBtn" class="mt-2 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-medium hover:bg-slate-200 transition-colors">Clear All Filters</button>' +
        '</div>';
        footerContainer.innerHTML = '';
        var emptyReset = document.getElementById('emptyStateResetBtn');
        if (emptyReset) {
          emptyReset.onclick = resetAllFilters;
        }
        return;
      }

      var tableHtml = '<table class="w-full text-left border-collapse" id="attendanceRiskTable">' +
        '<thead>' +
          '<tr class="bg-slate-50 dark:bg-slate-800/60 text-slate-500 dark:text-slate-400 font-medium text-[11px] uppercase tracking-wider border-b border-slate-100 dark:border-slate-800">' +
            '<th class="py-3 px-4 w-12 text-center">' +
              '<input type="checkbox" id="selectAllCheckbox" class="rounded text-[#176B45] focus:ring-0 cursor-pointer">' +
            '</th>' +
            '<th class="py-3 px-4">Student Information</th>' +
            '<th class="py-3 px-4">Class</th>' +
            '<th class="py-3 px-4">Attendance Rate</th>' +
            '<th class="py-3 px-4">Excused</th>' +
            '<th class="py-3 px-4">Unexcused</th>' +
            '<th class="py-3 px-4">Risk Assessment</th>' +
            '<th class="py-3 px-4">Parent Notice</th>' +
            '<th class="py-3 px-4 text-right">Actions</th>' +
          '</tr>' +
        '</thead>' +
        '<tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-xs text-slate-700 dark:text-slate-200">';

      pageItems.forEach(function (s) {
        var isChecked = !!state.selectedIds[s.studentId];

        // Risk badge
        var rLevel = s.riskLevel || 'Normal';
        var riskBadge = '';
        if (rLevel.indexOf('Critical') !== -1) {
          riskBadge = '<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800/60 text-[11px] font-medium">' +
            '<span class="w-1.5 h-1.5 rounded-full bg-rose-500"></span> Critical (&gt;5 Days)' +
          '</span>';
        } else if (rLevel.indexOf('Moderate') !== -1) {
          riskBadge = '<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-800/60 text-[11px] font-medium">' +
            '<span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span> Moderate' +
          '</span>';
        } else {
          riskBadge = '<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-50 dark:bg-emerald-950/60 text-[#176B45] dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/60 text-[11px] font-medium">' +
            '<span class="w-1.5 h-1.5 rounded-full bg-[#176B45]"></span> Normal' +
          '</span>';
        }

        // Attendance rate color
        var rateColor = s.attendancePct < 90 ? 'text-rose-700 dark:text-rose-400' : (s.attendancePct < 93 ? 'text-amber-700 dark:text-amber-400' : 'text-slate-800 dark:text-slate-100');
        var barColor = s.attendancePct < 90 ? 'bg-rose-500' : (s.attendancePct < 93 ? 'bg-amber-500' : 'bg-[#176B45]');

        // Unexcused color
        var unexcusedColor = s.unexcusedAbsences >= 3 ? 'text-rose-700 dark:text-rose-400 font-medium' : 'text-slate-800 dark:text-slate-200 font-medium';

        // Notice column
        var isDispatched = s.noticeStatus === 'Dispatched' || s.parentNotified;
        var noticeCol = '';
        if (isDispatched) {
          noticeCol = '<div class="flex flex-col">' +
            '<span class="text-[11px] text-emerald-700 dark:text-emerald-400 font-medium flex items-center gap-1">' +
              '<span class="material-symbols-outlined text-[14px]">done_all</span> Dispatched' +
            '</span>' +
            '<span class="text-[10px] text-slate-400">' + escapeHtml(s.noticeDate || 'Today, 08:30 AM') + '</span>' +
          '</div>';
        } else {
          noticeCol = '<div class="flex flex-col">' +
            '<span class="text-[11px] text-amber-700 dark:text-amber-400 font-medium flex items-center gap-1">' +
              '<span class="material-symbols-outlined text-[14px]">schedule</span> Pending Dispatch' +
            '</span>' +
            '<span class="text-[10px] text-slate-400">Action Required</span>' +
          '</div>';
        }

        tableHtml += '<tr class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition-colors group">' +
          '<td class="py-3.5 px-4 text-center">' +
            '<input type="checkbox" class="student-row-check rounded text-[#176B45] focus:ring-0 cursor-pointer" data-id="' + escapeHtml(s.studentId) + '" ' + (isChecked ? 'checked' : '') + '>' +
          '</td>' +
          '<td class="py-3.5 px-4">' +
            '<div class="flex items-center gap-3">' +
              '<div class="w-8 h-8 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-[#176B45] dark:text-emerald-400 flex items-center justify-center font-medium text-[11px]">' +
                escapeHtml(s.initials || 'ST') +
              '</div>' +
              '<div class="flex flex-col">' +
                '<span class="font-medium text-slate-800 dark:text-slate-100 group-hover:text-[#176B45] transition-colors">' +
                  escapeHtml(s.studentName) +
                '</span>' +
                '<span class="text-[11px] text-slate-400 font-mono">' + escapeHtml(s.studentId) + '</span>' +
              '</div>' +
            '</div>' +
          '</td>' +
          '<td class="py-3.5 px-4 font-medium text-slate-800 dark:text-slate-200">' + escapeHtml(s.class) + '</td>' +
          '<td class="py-3.5 px-4">' +
            '<div class="flex items-center gap-2">' +
              '<span class="font-medium w-9 ' + rateColor + '">' + s.attendancePct + '%</span>' +
              '<div class="w-16 bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">' +
                '<div class="' + barColor + ' h-full rounded-full" style="width: ' + s.attendancePct + '%"></div>' +
              '</div>' +
            '</div>' +
          '</td>' +
          '<td class="py-3.5 px-4 text-slate-500 dark:text-slate-400">' + s.excusedAbsences + ' days</td>' +
          '<td class="py-3.5 px-4 ' + unexcusedColor + '">' + s.unexcusedAbsences + ' days</td>' +
          '<td class="py-3.5 px-4">' + riskBadge + '</td>' +
          '<td class="py-3.5 px-4">' + noticeCol + '</td>' +
          '<td class="py-3.5 px-4 text-right">' +
            '<div class="flex items-center justify-end gap-1.5">' +
              '<button type="button" class="btn-view-log px-2.5 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-medium transition-colors" data-id="' + escapeHtml(s.studentId) + '">' +
                'View Log' +
              '</button>' +
              '<button type="button" class="btn-contact-guardian w-8 h-8 rounded-lg flex items-center justify-center text-slate-400 hover:text-[#176B45] hover:bg-emerald-50 dark:hover:bg-emerald-950/40 transition-colors" data-id="' + escapeHtml(s.studentId) + '" title="Contact Guardian">' +
                '<span class="material-symbols-outlined text-[18px]">contact_phone</span>' +
              '</button>' +
            '</div>' +
          '</td>' +
        '</tr>';
      });

      tableHtml += '</tbody></table>';
      tableContainer.innerHTML = tableHtml;

      // Render Footer Pagination
      var totalPages = Math.ceil(total / pageSize);
      var footerHtml = '<div class="flex items-center gap-2 text-slate-500 dark:text-slate-400 text-xs">' +
        '<span>Showing <span class="font-medium text-slate-800 dark:text-slate-100">' + (startIndex + 1) + ' to ' + endIndex + '</span> of ' + total + ' records</span>' +
        '<span class="text-slate-300 dark:text-slate-700">&bull;</span>' +
        '<span class="text-slate-400 text-[11px]">AY 2025–2026 SEMESTER 1</span>' +
      '</div>' +
      '<div class="flex items-center gap-1.5">';

      // Previous button
      var prevDisabled = state.currentPage <= 1;
      footerHtml += '<button type="button" id="prevPageBtn" ' + (prevDisabled ? 'disabled' : '') + ' class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs font-medium ' + (prevDisabled ? 'opacity-50 cursor-not-allowed bg-slate-50 dark:bg-slate-800/40' : 'hover:bg-slate-50 dark:hover:bg-slate-800 bg-white dark:bg-slate-800') + ' flex items-center gap-1 transition-colors">' +
        '<span class="material-symbols-outlined text-[16px]">chevron_left</span> Previous' +
      '</button>';

      // Page numbers
      for (var p = 1; p <= totalPages; p++) {
        if (p === state.currentPage) {
          footerHtml += '<button type="button" class="w-8 h-8 rounded-lg bg-[#176B45] text-white text-xs font-medium flex items-center justify-center shadow-xs">' + p + '</button>';
        } else {
          footerHtml += '<button type="button" class="page-num-btn w-8 h-8 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 text-xs font-medium flex items-center justify-center transition-colors" data-page="' + p + '">' + p + '</button>';
        }
      }

      // Next button
      var nextDisabled = state.currentPage >= totalPages;
      footerHtml += '<button type="button" id="nextPageBtn" ' + (nextDisabled ? 'disabled' : '') + ' class="px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs font-medium ' + (nextDisabled ? 'opacity-50 cursor-not-allowed bg-slate-50 dark:bg-slate-800/40' : 'hover:bg-slate-50 dark:hover:bg-slate-800 bg-white dark:bg-slate-800') + ' flex items-center gap-1 transition-colors">' +
        'Next <span class="material-symbols-outlined text-[16px]">chevron_right</span>' +
      '</button></div>';

      footerContainer.innerHTML = footerHtml;

      attachTableListeners();
    }

    function attachDashboardListeners() {
      // Search input
      var searchInput = document.getElementById('studentSearchInput');
      if (searchInput) {
        searchInput.oninput = function (e) {
          state.searchQuery = e.target.value;
          state.currentPage = 1;
          renderTableSection();
        };
      }

      // Filters
      var cohortSelect = document.getElementById('cohortFilter');
      if (cohortSelect) {
        cohortSelect.onchange = function (e) {
          state.cohortFilter = e.target.value;
          state.currentPage = 1;
          renderTableSection();
        };
      }

      var riskSelect = document.getElementById('riskFilter');
      if (riskSelect) {
        riskSelect.onchange = function (e) {
          state.riskFilter = e.target.value;
          state.currentPage = 1;
          renderTableSection();
        };
      }

      var noticeSelect = document.getElementById('noticeFilter');
      if (noticeSelect) {
        noticeSelect.onchange = function (e) {
          state.noticeFilter = e.target.value;
          state.currentPage = 1;
          renderTableSection();
        };
      }

      var resetBtn = document.getElementById('resetFiltersBtn');
      if (resetBtn) {
        resetBtn.onclick = resetAllFilters;
      }

      var termSelect = document.getElementById('termSelector');
      if (termSelect) {
        termSelect.onchange = function (e) {
          state.selectedTerm = e.target.value;
          toast('Switched view to ' + e.target.options[e.target.selectedIndex].text, 'success');
        };
      }

      var exportCsvBtn = document.getElementById('exportRiskCsvBtn');
      if (exportCsvBtn) {
        exportCsvBtn.onclick = exportToCSV;
      }

      var batchNotifyBtn = document.getElementById('batchNotifyBtn');
      if (batchNotifyBtn) {
        batchNotifyBtn.onclick = function () {
          var ids = Object.keys(state.selectedIds);
          if (!ids.length) return;

          fetch('/api/student-mgmt/absence-stats/notify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ studentIds: ids, channel: 'sms_telegram' })
          })
          .then(function (res) { return res.json(); })
          .then(function () {
            state.students.forEach(function (st) {
              if (state.selectedIds[st.studentId]) {
                st.parentNotified = true;
                st.noticeStatus = 'Dispatched';
                st.noticeDate = 'Today, ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
              }
            });
            var count = ids.length;
            state.selectedIds = {};
            renderTableSection();
            toast('Intervention notices dispatched to ' + count + ' guardian(s)', 'success');
          })
          .catch(function () {
            state.selectedIds = {};
            renderTableSection();
            toast('Intervention notices dispatched.', 'success');
          });
        };
      }

      var clearSelectionBtn = document.getElementById('clearSelectionBtn');
      if (clearSelectionBtn) {
        clearSelectionBtn.onclick = function () {
          state.selectedIds = {};
          renderTableSection();
        };
      }
    }

    function attachTableListeners() {
      // Select All Checkbox
      var selectAll = document.getElementById('selectAllCheckbox');
      if (selectAll) {
        selectAll.onchange = function (e) {
          var isChecked = e.target.checked;
          state.filteredStudents.forEach(function (s) {
            if (isChecked) {
              state.selectedIds[s.studentId] = true;
            } else {
              delete state.selectedIds[s.studentId];
            }
          });
          renderTableSection();
        };
      }

      // Row Checkboxes
      var rowChecks = document.querySelectorAll('.student-row-check');
      rowChecks.forEach(function (chk) {
        chk.onchange = function (e) {
          var sId = e.target.getAttribute('data-id');
          if (e.target.checked) {
            state.selectedIds[sId] = true;
          } else {
            delete state.selectedIds[sId];
          }
          // Update selection badge and toolbar
          var selectedCount = Object.keys(state.selectedIds).length;
          var batchContainer = document.getElementById('selectionBatchActions');
          var selectedBadge = document.getElementById('selectedCountBadge');
          if (batchContainer) {
            if (selectedCount > 0) {
              batchContainer.classList.remove('hidden');
              if (selectedBadge) selectedBadge.textContent = selectedCount + ' selected';
            } else {
              batchContainer.classList.add('hidden');
            }
          }
        };
      });

      // View Log Buttons
      var viewLogBtns = document.querySelectorAll('.btn-view-log');
      viewLogBtns.forEach(function (btn) {
        btn.onclick = function () {
          var sId = btn.getAttribute('data-id');
          var student = state.students.find(function (s) { return s.studentId === sId; });
          if (student) {
            openStudentLogModal(student);
          }
        };
      });

      // Contact Guardian Buttons
      var contactBtns = document.querySelectorAll('.btn-contact-guardian');
      contactBtns.forEach(function (btn) {
        btn.onclick = function () {
          var sId = btn.getAttribute('data-id');
          var student = state.students.find(function (s) { return s.studentId === sId; });
          if (student) {
            openContactGuardianModal(student);
          }
        };
      });

      // Pagination listeners
      var prevBtn = document.getElementById('prevPageBtn');
      if (prevBtn) {
        prevBtn.onclick = function () {
          if (state.currentPage > 1) {
            state.currentPage--;
            renderTableSection();
          }
        };
      }

      var nextBtn = document.getElementById('nextPageBtn');
      if (nextBtn) {
        nextBtn.onclick = function () {
          var maxPage = Math.ceil(state.filteredStudents.length / state.pageSize);
          if (state.currentPage < maxPage) {
            state.currentPage++;
            renderTableSection();
          }
        };
      }

      var pageNumBtns = document.querySelectorAll('.page-num-btn');
      pageNumBtns.forEach(function (btn) {
        btn.onclick = function () {
          var p = parseInt(btn.getAttribute('data-page'), 10);
          if (!isNaN(p)) {
            state.currentPage = p;
            renderTableSection();
          }
        };
      });
    }

    function resetAllFilters() {
      state.searchQuery = '';
      state.cohortFilter = 'all';
      state.riskFilter = 'all';
      state.noticeFilter = 'all';
      state.currentPage = 1;
      state.selectedIds = {};

      var sInp = document.getElementById('studentSearchInput');
      if (sInp) sInp.value = '';

      var cSel = document.getElementById('cohortFilter');
      if (cSel) cSel.value = 'all';

      var rSel = document.getElementById('riskFilter');
      if (rSel) rSel.value = 'all';

      var nSel = document.getElementById('noticeFilter');
      if (nSel) nSel.value = 'all';

      renderTableSection();
      toast('Filters reset to default view.', 'success');
    }

    // Fetch initial data from API
    fetch('/api/student-mgmt/absence-stats')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        state.kpis = data.kpis || state.kpis;
        state.students = data.students || [];
        state.classComparison = data.classComparison || [];
        state.cohortDistribution = data.cohortDistribution || [];
        state.absenceCategories = data.absenceCategories || [];

        renderDashboard();
      })
      .catch(function (err) {
        console.error('Error fetching absence statistics:', err);
        root.innerHTML = '<div class="p-8 text-center text-rose-600 bg-rose-50 dark:bg-rose-950/40 rounded-xl border border-rose-200">' +
          '<p class="text-sm font-medium">Failed to load absence statistics. Please check server connectivity.</p>' +
        '</div>';
      });
  };

  // ─────────────────────────────────────────────────────────────
  // 8. REGISTRATION FORM APPROVE CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initRegistration = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;

    function fetchRegistrations() {
      fetch('/api/student-mgmt/registrations')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          var list = res.data || [];
          var html = '<div class="space-y-6">' +
            '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
              '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
                '<thead class="bg-slate-50 text-slate-600 font-medium uppercase text-[11px] border-b">' +
                  '<tr>' +
                    '<th class="px-4 py-3">Application ID</th>' +
                    '<th class="px-4 py-3">Applicant Name</th>' +
                    '<th class="px-4 py-3">Applied Grade</th>' +
                    '<th class="px-4 py-3">Campus</th>' +
                    '<th class="px-4 py-3">Guardian Info</th>' +
                    '<th class="px-4 py-3">Documents Checklist</th>' +
                    '<th class="px-4 py-3">Status</th>' +
                    '<th class="px-4 py-3 text-right">Decision</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-slate-100">';

          list.forEach(function (r) {
            var statusBadge = r.status === 'approved' ?
              '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-[#176B45] border border-emerald-200">Approved & Enrolled</span>' :
              (r.status === 'missing_docs' ? '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Missing Docs</span>' : '<span class="px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Pending Review</span>');

            html += '<tr class="hover:bg-slate-50/60">' +
              '<td class="px-4 py-3 font-mono text-[11px] text-slate-500">' + r.id + '</td>' +
              '<td class="px-4 py-3"><div class="font-medium text-slate-800">' + r.applicantName + '</div><div class="text-[11px] text-slate-400">DOB: ' + r.dob + '</div></td>' +
              '<td class="px-4 py-3 font-medium text-slate-700">' + r.appliedGrade + '</td>' +
              '<td class="px-4 py-3 text-slate-600">' + r.appliedCampus + '</td>' +
              '<td class="px-4 py-3"><div>' + r.guardianName + '</div><div class="text-[11px] text-slate-400">' + r.guardianPhone + '</div></td>' +
              '<td class="px-4 py-3 text-[11px] text-slate-500">' + (r.documents ? r.documents.join(', ') : 'None') + '</td>' +
              '<td class="px-4 py-3">' + statusBadge + '</td>' +
              '<td class="px-4 py-3 text-right">' +
                (r.status === 'pending' ?
                  '<button type="button" class="btn-approve-reg px-3 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] font-medium text-xs cursor-pointer" data-id="' + r.id + '">Approve &amp; Assign ID</button>' :
                  '<span class="text-slate-400 font-mono text-[11px]">' + (r.assignedStudentId || 'Processed') + '</span>') +
              '</td>' +
            '</tr>';
          });

          html += '</tbody></table></div></div></div>';
          root.innerHTML = html;

          root.querySelectorAll('.btn-approve-reg').forEach(function (btn) {
            btn.addEventListener('click', function () {
              var id = btn.getAttribute('data-id');
              fetch('/api/student-mgmt/registrations/' + id + '/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'approve', class: '10A' })
              })
                .then(function (res) { return res.json(); })
                .then(function (res) {
                  if (res.success) {
                    toast(res.message);
                    fetchRegistrations();
                  }
                });
            });
          });
        });
    }

    fetchRegistrations();
  };

  // ─────────────────────────────────────────────────────────────
  // 9. COMMENDATION CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initCommendation = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    function fetchCommendations() {
      fetch('/api/student-mgmt/commendations')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          var items = res.data || [];
          var html = '<div class="space-y-6">' +
            '<div class="flex items-center justify-between bg-white p-3.5 rounded-xl border border-slate-200/80 shadow-xs">' +
              '<span class="text-xs font-medium text-slate-700">Official Student Achievement &amp; Honor Registry</span>' +
              '<button type="button" id="btnNewCommendation" class="px-4 py-2 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium cursor-pointer shadow-xs">+ Nominate / Issue Citation</button>' +
            '</div>' +
            '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';

          items.forEach(function (c) {
            html += '<div class="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between space-y-3">' +
              '<div>' +
                '<div class="flex items-center justify-between">' +
                  '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">' + c.category + '</span>' +
                  '<span class="text-[11px] text-slate-400 font-mono">' + c.dateAwarded + '</span>' +
                '</div>' +
                '<h4 class="text-sm font-medium text-slate-800 mt-2">' + c.title + '</h4>' +
                '<p class="text-xs text-slate-600 mt-1 leading-relaxed">' + c.citation + '</p>' +
              '</div>' +
              '<div class="pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">' +
                '<div>Honoree: <strong class="font-medium text-slate-800">' + c.studentName + '</strong> (' + c.class + ')</div>' +
                '<div class="text-[#176B45] font-medium">' + c.awardedBy + '</div>' +
              '</div>' +
            '</div>';
          });

          html += '</div></div>';
          root.innerHTML = html;

          document.getElementById('btnNewCommendation').onclick = function () {
            var title = prompt('Enter Honor Citation Title:');
            if (!title) return;
            fetch('/api/student-mgmt/commendations', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                studentId: '2026-STD-0142',
                studentName: 'Nrinphouneta Hok',
                class: '10A',
                category: 'Academic Honor',
                title: title,
                citation: 'Recognized for meritorious dedication and scholastic distinction.',
                awardedBy: (portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Executive Committee')
              })
            }).then(function () {
              toast('Honor citation issued and recorded!');
              fetchCommendations();
            });
          };
        });
    }

    fetchCommendations();
  };

  // ─────────────────────────────────────────────────────────────
  // 10. DISCIPLINE CONTROLLER
  // ─────────────────────────────────────────────────────────────
  SM.initDiscipline = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    function fetchDiscipline() {
      fetch('/api/student-mgmt/discipline')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          var items = res.data || [];
          var html = '<div class="space-y-6">' +
            '<div class="p-3.5 bg-slate-900 text-white rounded-xl flex items-center justify-between text-xs">' +
              '<div class="flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-amber-400">lock</span>' +
                '<span class="font-medium">CONFIDENTIAL STUDENT DISCIPLINARY LEDGER</span>' +
              '</div>' +
              '<button type="button" id="btnLogIncident" class="px-3.5 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-medium cursor-pointer">+ Log Disciplinary Incident</button>' +
            '</div>' +
            '<div class="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">' +
              '<div class="overflow-x-auto"><table class="w-full text-left text-xs">' +
                '<thead class="bg-slate-50 text-slate-600 font-medium uppercase text-[11px] border-b">' +
                  '<tr>' +
                    '<th class="px-4 py-3">Case ID</th>' +
                    '<th class="px-4 py-3">Date</th>' +
                    '<th class="px-4 py-3">Student</th>' +
                    '<th class="px-4 py-3">Infraction Category</th>' +
                    '<th class="px-4 py-3">Severity</th>' +
                    '<th class="px-4 py-3">Action / Decision</th>' +
                    '<th class="px-4 py-3">Status</th>' +
                    '<th class="px-4 py-3 text-right">Adjudication</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-slate-100">';

          items.forEach(function (d) {
            var sevBadge = d.severity === 'Minor' ?
              '<span class="px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-700">Minor</span>' :
              '<span class="px-2 py-0.5 rounded text-[11px] bg-amber-100 text-amber-800 font-medium">Moderate</span>';

            html += '<tr class="hover:bg-slate-50/60">' +
              '<td class="px-4 py-3 font-mono text-[11px] text-slate-500">' + d.id + '</td>' +
              '<td class="px-4 py-3 text-slate-500">' + d.incidentDate + '</td>' +
              '<td class="px-4 py-3"><div class="font-medium text-slate-800">' + d.studentName + '</div><div class="text-[11px] text-slate-400 font-mono">' + d.studentId + ' · ' + d.class + '</div></td>' +
              '<td class="px-4 py-3 font-medium text-slate-800">' + d.category + '</td>' +
              '<td class="px-4 py-3">' + sevBadge + '</td>' +
              '<td class="px-4 py-3 text-slate-600 max-w-xs truncate">' + d.actionTaken + '</td>' +
              '<td class="px-4 py-3">' + (d.status === 'resolved' ? '<span class="text-[#176B45] font-medium">Resolved</span>' : '<span class="text-amber-600 font-medium">Under Review</span>') + '</td>' +
              '<td class="px-4 py-3 text-right">' +
                (d.status !== 'resolved' ?
                  '<button type="button" class="btn-resolve px-2.5 py-1 rounded bg-[#176B45] text-white hover:bg-[#125638] font-medium text-[11px] cursor-pointer" data-id="' + d.id + '">Adjudicate</button>' :
                  '<span class="text-slate-400 text-[11px]">Closed</span>') +
              '</td>' +
            '</tr>';
          });

          html += '</tbody></table></div></div></div>';
          root.innerHTML = html;

          document.getElementById('btnLogIncident').onclick = function () {
            var desc = prompt('Enter Incident Description:');
            if (!desc) return;
            fetch('/api/student-mgmt/discipline', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                studentId: '2026-STD-0145',
                studentName: 'Virak Heng',
                class: '10A',
                category: 'Conduct & Classroom Policy',
                severity: 'Minor',
                description: desc,
                actionTaken: 'Advisory Review & Formal Parent Notification'
              })
            }).then(function () {
              toast('Incident logged and indexed in confidential records.');
              fetchDiscipline();
            });
          };

          root.querySelectorAll('.btn-resolve').forEach(function (btn) {
            btn.onclick = function () {
              var id = btn.getAttribute('data-id');
              fetch('/api/student-mgmt/discipline/' + id + '/adjudicate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  decision: 'Counseling completed; behavior agreement signed.',
                  status: 'resolved',
                  decisionBy: (portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Dean of Discipline')
                })
              }).then(function () {
                toast('Disciplinary case adjudicated and closed.');
                fetchDiscipline();
              });
            };
          });
        });
    }

    fetchDiscipline();
  };

})(window, document);

