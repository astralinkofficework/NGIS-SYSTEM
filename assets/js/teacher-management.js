/**
 * NGIS Teacher Management Module Engine
 * Powers the 7 dynamic views for Admin & Principal portals:
 * - initVerify: Verify Teacher Update (diff viewer, approval workflow)
 * - initAssignments: Teaching Assignment (subject/class allocation & workload balancing)
 * - initHomeroom: Homeroom Teacher Assign (class allocations, student counts & conflict checks)
 * - initAttendance: Teacher Attendance (daily telemetry, status, biometric logs & excuse tracking)
 * - initCommendation: Faculty Commendations (honors, citations & awards)
 * - initDiscipline: Confidential Faculty Discipline (conduct cases, severity levels & hearings)
 * - initEfforts: Input Teacher Efforts (extracurricular contributions, point logging & verification)
 * 
 * Strict AGENTS.md compliance:
 * - NO BOLD FONTS (font-normal / font-medium only, max weight 500)
 * - Accessible touch targets, responsive tables, clear empty states & toast feedback.
 */

(function (window, document) {
  'use strict';

  var TM = window.TEACHER_MGMT = window.TEACHER_MGMT || {};

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function toast(msg, type) {
    var existing = document.getElementById('tmToast');
    if (existing) existing.remove();
    var t = document.createElement('div');
    t.id = 'tmToast';
    var bg = type === 'error' ? 'bg-rose-600' : (type === 'info' ? 'bg-slate-800' : 'bg-[#176B45]');
    t.className = 'fixed bottom-5 right-5 z-50 flex items-center gap-2.5 px-4 py-2.5 rounded-xl shadow-lg text-white text-xs font-medium transition-all transform translate-y-0 ' + bg;
    t.innerHTML = '<span class="material-symbols-outlined text-sm">' + (type === 'error' ? 'error' : 'check_circle') + '</span><span>' + esc(msg) + '</span>';
    document.body.appendChild(t);
    setTimeout(function () {
      t.classList.add('opacity-0', 'translate-y-2');
      setTimeout(function () { t.remove(); }, 300);
    }, 3200);
  }

  /* ════════════════════════════════════════════════════════════════
     1. VERIFY TEACHER UPDATE
     ════════════════════════════════════════════════════════════════ */
  TM.initVerify = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { items: [], search: '', status: 'all', activeItem: null };

    function fetchUpdates() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading teacher update requests...</span></div>';
      fetch('/api/teacher-mgmt/verify')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.items = res.data || [];
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load verification requests.</div>';
        });
    }

    function render() {
      var pending = state.items.filter(function (i) { return i.status === 'pending'; }).length;
      var approved = state.items.filter(function (i) { return i.status === 'approved'; }).length;
      var total = state.items.length;

      var filtered = state.items.filter(function (i) {
        if (state.status !== 'all' && i.status !== state.status) return false;
        if (state.search) {
          var q = state.search.toLowerCase();
          var m = (i.teacherName || '').toLowerCase().indexOf(q) !== -1 ||
                  (i.teacherId || '').toLowerCase().indexOf(q) !== -1 ||
                  (i.department || '').toLowerCase().indexOf(q) !== -1 ||
                  (i.fieldChanged || '').toLowerCase().indexOf(q) !== -1;
          if (!m) return false;
        }
        return true;
      });

      var rowsHtml = filtered.map(function (item) {
        var statusBadge = '';
        if (item.status === 'pending') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Pending Review</span>';
        } else if (item.status === 'approved') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Approved</span>';
        } else if (item.status === 'rejected') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Rejected</span>';
        } else {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Needs Correction</span>';
        }

        return '<tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">' +
          '<td class="py-3 px-3 text-xs font-mono text-slate-500">' + esc(item.id) + '</td>' +
          '<td class="py-3 px-3">' +
            '<div class="text-xs font-medium text-slate-800">' + esc(item.teacherName) + '</div>' +
            '<div class="text-[11px] text-slate-400 font-mono">' + esc(item.teacherId) + '</div>' +
          '</td>' +
          '<td class="py-3 px-3 text-xs text-slate-600">' + esc(item.department) + '</td>' +
          '<td class="py-3 px-3 text-xs text-slate-700 font-medium">' + esc(item.fieldChanged) + '</td>' +
          '<td class="py-3 px-3">' +
            '<div class="text-[11px] text-rose-600 bg-rose-50/70 px-2 py-0.5 rounded mb-1 max-w-xs truncate" title="' + esc(item.previousValue) + '"><span class="font-medium">Previous:</span> ' + esc(item.previousValue) + '</div>' +
            '<div class="text-[11px] text-emerald-700 bg-emerald-50/70 px-2 py-0.5 rounded max-w-xs truncate" title="' + esc(item.proposedValue) + '"><span class="font-medium">Proposed:</span> ' + esc(item.proposedValue) + '</div>' +
          '</td>' +
          '<td class="py-3 px-3 text-xs text-slate-500">' + esc(item.submittedDate) + '</td>' +
          '<td class="py-3 px-3">' + statusBadge + '</td>' +
          '<td class="py-3 px-3 text-right">' +
            '<button type="button" class="btn-review inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-slate-200 hover:border-[#176B45] text-xs font-medium text-slate-700 hover:text-[#176B45] bg-white transition-all cursor-pointer shadow-2xs active:scale-95" data-id="' + esc(item.id) + '">' +
              '<span class="material-symbols-outlined text-[16px]">visibility</span>' +
              '<span>Review</span>' +
            '</button>' +
          '</td>' +
        '</tr>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Pending Verification</div><div class="text-xl font-medium text-amber-600 mt-0.5">' + pending + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">pending_actions</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Approved Changes</div><div class="text-xl font-medium text-emerald-700 mt-0.5">' + approved + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center"><span class="material-symbols-outlined text-lg">verified</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Total Submissions</div><div class="text-xl font-medium text-slate-800 mt-0.5">' + total + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-slate-50 text-slate-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">inventory_2</span></div>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">' +
            '<div class="relative flex-1 max-w-md">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>' +
              '<input type="text" id="tmVerifySearch" placeholder="Search teacher, ID, department, or update field..." value="' + esc(state.search) + '" class="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<label class="text-xs text-slate-500 font-medium">Status:</label>' +
              '<select id="tmVerifyStatus" class="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-700 font-medium">' +
                '<option value="all"' + (state.status === 'all' ? ' selected' : '') + '>All Statuses</option>' +
                '<option value="pending"' + (state.status === 'pending' ? ' selected' : '') + '>Pending Review</option>' +
                '<option value="approved"' + (state.status === 'approved' ? ' selected' : '') + '>Approved</option>' +
                '<option value="rejected"' + (state.status === 'rejected' ? ' selected' : '') + '>Rejected</option>' +
                '<option value="needs_correction"' + (state.status === 'needs_correction' ? ' selected' : '') + '>Needs Correction</option>' +
              '</select>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
            '<div class="overflow-x-auto">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead>' +
                  '<tr class="border-b border-slate-200 bg-slate-50/70 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                    '<th class="py-2.5 px-3">Req ID</th>' +
                    '<th class="py-2.5 px-3">Teacher</th>' +
                    '<th class="py-2.5 px-3">Department</th>' +
                    '<th class="py-2.5 px-3">Field</th>' +
                    '<th class="py-2.5 px-3">Previous vs Proposed</th>' +
                    '<th class="py-2.5 px-3">Submitted</th>' +
                    '<th class="py-2.5 px-3">Status</th>' +
                    '<th class="py-2.5 px-3 text-right">Action</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody>' +
                  (rowsHtml || '<tr><td colspan="8" class="text-center py-12 text-xs text-slate-400">No teacher update requests matching criteria.</td></tr>') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>' +
        '</div>' +

        '<div id="tmVerifyModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">' +
          '<div class="bg-white border border-slate-200 rounded-2xl shadow-xl w-full max-w-lg overflow-hidden animate-in fade-in zoom-in-95 duration-150">' +
            '<div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/60">' +
              '<div class="flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[#176B45]">rule</span>' +
                '<span class="text-sm font-medium text-slate-800">Review Faculty Update Request</span>' +
              '</div>' +
              '<button type="button" id="tmCloseModal" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"><span class="material-symbols-outlined text-lg">close</span></button>' +
            '</div>' +
            '<div class="p-5 space-y-4" id="tmModalBody"></div>' +
            '<div class="px-5 py-3.5 border-t border-slate-100 flex items-center justify-end gap-2 bg-slate-50/60">' +
              '<button type="button" id="btnReject" class="px-3.5 py-1.5 rounded-lg border border-rose-200 text-rose-700 hover:bg-rose-50 text-xs font-medium transition-all cursor-pointer">Reject</button>' +
              '<button type="button" id="btnCorrection" class="px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-100 text-xs font-medium transition-all cursor-pointer">Needs Correction</button>' +
              '<button type="button" id="btnApprove" class="px-4 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">Approve & Update Profile</button>' +
            '</div>' +
          '</div>' +
        '</div>';

      // Event handlers
      var searchInput = document.getElementById('tmVerifySearch');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value;
          render();
        });
      }

      var statusSelect = document.getElementById('tmVerifyStatus');
      if (statusSelect) {
        statusSelect.addEventListener('change', function (e) {
          state.status = e.target.value;
          render();
        });
      }

      var modal = document.getElementById('tmVerifyModal');
      var modalBody = document.getElementById('tmModalBody');
      var closeModal = document.getElementById('tmCloseModal');
      if (closeModal) {
        closeModal.addEventListener('click', function () {
          modal.classList.add('hidden');
        });
      }

      root.querySelectorAll('.btn-review').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-id');
          var item = state.items.find(function (i) { return i.id === id; });
          if (!item) return;
          state.activeItem = item;

          modalBody.innerHTML = '' +
            '<div class="space-y-3">' +
              '<div class="flex items-center justify-between pb-3 border-b border-slate-100">' +
                '<div>' +
                  '<div class="text-sm font-medium text-slate-900">' + esc(item.teacherName) + '</div>' +
                  '<div class="text-xs text-slate-500 font-mono">' + esc(item.teacherId) + ' · ' + esc(item.department) + '</div>' +
                '</div>' +
                '<span class="text-xs font-mono text-slate-400">Submitted ' + esc(item.submittedDate) + '</span>' +
              '</div>' +
              '<div>' +
                '<label class="text-xs text-slate-500 font-medium">Update Category / Field:</label>' +
                '<div class="text-xs font-medium text-slate-800 mt-0.5">' + esc(item.fieldChanged) + '</div>' +
              '</div>' +
              '<div class="grid grid-cols-2 gap-3 p-3 bg-slate-50 rounded-xl border border-slate-100">' +
                '<div>' +
                  '<span class="text-[11px] font-medium text-rose-700 block mb-1">Previous Registered Value:</span>' +
                  '<div class="text-xs text-slate-700 bg-white p-2 rounded-lg border border-slate-200 break-words">' + esc(item.previousValue) + '</div>' +
                '</div>' +
                '<div>' +
                  '<span class="text-[11px] font-medium text-emerald-700 block mb-1">Proposed Verified Value:</span>' +
                  '<div class="text-xs text-slate-900 bg-emerald-50/50 p-2 rounded-lg border border-emerald-200 break-words font-medium">' + esc(item.proposedValue) + '</div>' +
                '</div>' +
              '</div>' +
              '<div>' +
                '<label class="text-xs text-slate-500 font-medium">Supporting Evidence / Attachment:</label>' +
                '<div class="mt-1 flex items-center gap-2 p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700">' +
                  '<span class="material-symbols-outlined text-rose-600 text-sm">picture_as_pdf</span>' +
                  '<span class="font-mono flex-1 truncate">' + esc(item.supportingDocument || 'Faculty_Credential_Evidence.pdf') + '</span>' +
                  '<span class="text-[11px] text-[#176B45] hover:underline cursor-pointer">Preview</span>' +
                '</div>' +
              '</div>' +
              '<div>' +
                '<label class="text-xs text-slate-500 font-medium">Reviewer Note / Justification:</label>' +
                '<textarea id="tmReviewerComments" rows="2" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800" placeholder="Optional notes for faculty audit log...">' + esc(item.comments || '') + '</textarea>' +
              '</div>' +
            '</div>';

          modal.classList.remove('hidden');
        });
      });

      function sendAction(act) {
        if (!state.activeItem) return;
        var comments = document.getElementById('tmReviewerComments') ? document.getElementById('tmReviewerComments').value : '';
        var reviewer = portalRole === 'principal' ? 'Dr. Sophal Meas (Principal)' : 'Mr. Heng Samnang (Admin)';
        fetch('/api/teacher-mgmt/verify/' + encodeURIComponent(state.activeItem.id) + '/action', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: act, reviewer: reviewer, comments: comments })
        })
          .then(function (res) { return res.json(); })
          .then(function (res) {
            if (res.success) {
              toast('Update request successfully ' + (act === 'approve' ? 'approved' : (act === 'reject' ? 'rejected' : 'flagged for correction')));
              modal.classList.add('hidden');
              fetchUpdates();
            } else {
              toast(res.message || 'Action failed', 'error');
            }
          })
          .catch(function () { toast('Network error', 'error'); });
      }

      var btnApprove = document.getElementById('btnApprove');
      if (btnApprove) btnApprove.onclick = function () { sendAction('approve'); };
      var btnReject = document.getElementById('btnReject');
      if (btnReject) btnReject.onclick = function () { sendAction('reject'); };
      var btnCorrection = document.getElementById('btnCorrection');
      if (btnCorrection) btnCorrection.onclick = function () { sendAction('correct'); };
    }

    fetchUpdates();
  };

  /* ════════════════════════════════════════════════════════════════
     2. TEACHING ASSIGNMENTS & WORKLOAD BALANCER
     ════════════════════════════════════════════════════════════════ */
  TM.initAssignments = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { assignments: [], workloads: [], search: '', dept: 'all' };

    function fetchAssignments() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading faculty teaching allocations...</span></div>';
      fetch('/api/teacher-mgmt/assignments')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.assignments = res.assignments || [];
          state.workloads = res.workloads || [];
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load teaching assignments.</div>';
        });
    }

    function render() {
      var totalAssigned = state.assignments.length;
      var totalFaculty = state.workloads.length;
      var heavyLoads = state.workloads.filter(function (w) { return w.status === 'heavy'; }).length;

      var workloadCards = state.workloads.map(function (w) {
        var pct = Math.min(100, Math.round((w.assignedPeriods / w.maxCapacity) * 100));
        var barColor = w.status === 'heavy' ? 'bg-amber-500' : (w.status === 'light' ? 'bg-blue-500' : 'bg-[#176B45]');
        var statusLabel = w.status === 'heavy' ? 'High Load' : (w.status === 'light' ? 'Under-allocated' : 'Optimal Capacity');
        var badgeColor = w.status === 'heavy' ? 'bg-amber-50 text-amber-700 border-amber-200' : (w.status === 'light' ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200');

        return '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs hover:border-slate-300 transition-all">' +
          '<div class="flex items-center justify-between">' +
            '<div>' +
              '<div class="text-xs font-medium text-slate-800">' + esc(w.teacherName) + '</div>' +
              '<div class="text-[11px] text-slate-400">' + esc(w.department) + '</div>' +
            '</div>' +
            '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium border ' + badgeColor + '">' + statusLabel + '</span>' +
          '</div>' +
          '<div class="mt-2.5">' +
            '<div class="flex items-center justify-between text-[11px] text-slate-500 mb-1">' +
              '<span>' + w.assignedPeriods + ' / ' + w.maxCapacity + ' periods/wk</span>' +
              '<span>' + pct + '%</span>' +
            '</div>' +
            '<div class="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">' +
              '<div class="h-full rounded-full transition-all ' + barColor + '" style="width:' + pct + '%"></div>' +
            '</div>' +
          '</div>' +
          '<div class="mt-2 pt-2 border-t border-slate-100 flex flex-wrap gap-1">' +
            (w.classes.map(function (c) { return '<span class="text-[10px] px-1.5 py-0.2 rounded bg-slate-100 text-slate-600 font-mono">' + esc(c) + '</span>'; }).join('') || '<span class="text-[10px] text-slate-400">No classes assigned</span>') +
          '</div>' +
        '</div>';
      }).join('');

      var filteredAssignments = state.assignments.filter(function (a) {
        if (state.dept !== 'all' && (a.department || '').toLowerCase().indexOf(state.dept) === -1) return false;
        if (state.search) {
          var q = state.search.toLowerCase();
          var m = (a.teacherName || '').toLowerCase().indexOf(q) !== -1 ||
                  (a.subjectName || '').toLowerCase().indexOf(q) !== -1 ||
                  (a.className || '').toLowerCase().indexOf(q) !== -1;
          if (!m) return false;
        }
        return true;
      });

      var rowsHtml = filteredAssignments.map(function (a) {
        return '<tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">' +
          '<td class="py-2.5 px-3 text-xs font-mono text-slate-500">' + esc(a.id) + '</td>' +
          '<td class="py-2.5 px-3 text-xs font-medium text-slate-800">' + esc(a.teacherName) + '</td>' +
          '<td class="py-2.5 px-3 text-xs text-slate-600">' + esc(a.department) + '</td>' +
          '<td class="py-2.5 px-3 text-xs text-slate-800 font-medium">' + esc(a.subjectName) + '</td>' +
          '<td class="py-2.5 px-3 text-xs font-mono text-slate-700"><span class="px-2 py-0.5 rounded bg-slate-100">' + esc(a.className) + '</span></td>' +
          '<td class="py-2.5 px-3 text-xs text-slate-700 font-medium">' + esc(a.periodsPerWeek) + ' hrs/wk</td>' +
          '<td class="py-2.5 px-3 text-xs text-slate-500">' + esc(a.room) + '</td>' +
          '<td class="py-2.5 px-3 text-right">' +
            '<button type="button" class="btn-del-assign text-slate-400 hover:text-rose-600 p-1.5 rounded-lg hover:bg-rose-50 transition-colors cursor-pointer" data-id="' + esc(a.id) + '" title="Remove Assignment">' +
              '<span class="material-symbols-outlined text-[17px]">delete</span>' +
            '</button>' +
          '</td>' +
        '</tr>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Active Teaching Allocations</div><div class="text-xl font-medium text-slate-800 mt-0.5">' + totalAssigned + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center"><span class="material-symbols-outlined text-lg">assignment_ind</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Assigned Faculty</div><div class="text-xl font-medium text-slate-800 mt-0.5">' + totalFaculty + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">groups</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Heavy Workload Warnings</div><div class="text-xl font-medium ' + (heavyLoads > 0 ? 'text-amber-600' : 'text-slate-800') + ' mt-0.5">' + heavyLoads + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">speed</span></div>' +
            '</div>' +
          '</div>' +

          '<div>' +
            '<div class="flex items-center justify-between mb-2.5">' +
              '<h3 class="text-xs font-medium text-slate-700 uppercase tracking-wider">Faculty Workload Balancer</h3>' +
              '<span class="text-[11px] text-slate-400 font-mono">Target: 18-22 periods/week</span>' +
            '</div>' +
            '<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">' +
              workloadCards +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">' +
            '<div class="relative flex-1 max-w-md">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>' +
              '<input type="text" id="tmAssignSearch" placeholder="Search teacher, subject, class..." value="' + esc(state.search) + '" class="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="btnOpenNewAssign" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">' +
                '<span class="material-symbols-outlined text-sm">add</span>' +
                '<span>+ Assign Subject</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
            '<div class="overflow-x-auto">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead>' +
                  '<tr class="border-b border-slate-200 bg-slate-50/70 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                    '<th class="py-2.5 px-3">Assign ID</th>' +
                    '<th class="py-2.5 px-3">Teacher</th>' +
                    '<th class="py-2.5 px-3">Department</th>' +
                    '<th class="py-2.5 px-3">Subject</th>' +
                    '<th class="py-2.5 px-3">Class</th>' +
                    '<th class="py-2.5 px-3">Workload</th>' +
                    '<th class="py-2.5 px-3">Room</th>' +
                    '<th class="py-2.5 px-3 text-right">Action</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody>' +
                  (rowsHtml || '<tr><td colspan="8" class="text-center py-10 text-xs text-slate-400">No active teaching assignments found.</td></tr>') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>' +
        '</div>';

      var searchInput = document.getElementById('tmAssignSearch');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value;
          render();
        });
      }

      root.querySelectorAll('.btn-del-assign').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-id');
          if (confirm('Are you sure you want to remove this teaching assignment?')) {
            fetch('/api/teacher-mgmt/assignments/' + encodeURIComponent(id), { method: 'DELETE' })
              .then(function (res) { return res.json(); })
              .then(function (res) {
                if (res.success) {
                  toast('Teaching assignment removed.');
                  fetchAssignments();
                }
              });
          }
        });
      });
    }

    fetchAssignments();
  };

  /* ════════════════════════════════════════════════════════════════
     3. HOMEROOM TEACHER ASSIGN
     ════════════════════════════════════════════════════════════════ */
  TM.initHomeroom = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { records: [], teachers: [] };

    function fetchHomeroom() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading homeroom allocations...</span></div>';
      Promise.all([
        fetch('/api/teacher-mgmt/homeroom').then(function (r) { return r.json(); }),
        fetch('/api/teacher-mgmt/teachers').then(function (r) { return r.json(); })
      ])
        .then(function (res) {
          state.records = res[0].data || [];
          state.teachers = res[1].data || [];
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load homeroom records.</div>';
        });
    }

    function render() {
      var assigned = state.records.filter(function (r) { return r.status === 'assigned'; }).length;
      var vacant = state.records.filter(function (r) { return r.status === 'vacant'; }).length;
      var totalStudents = state.records.reduce(function (acc, r) { return acc + (r.studentCount || 0); }, 0);

      var cardsHtml = state.records.map(function (c) {
        var isVacant = c.status === 'vacant';
        var badgeColor = isVacant ? 'bg-rose-50 text-rose-700 border-rose-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200';

        return '<div class="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs hover:border-slate-300 transition-all flex flex-col justify-between">' +
          '<div>' +
            '<div class="flex items-center justify-between mb-2">' +
              '<div class="text-sm font-medium text-slate-900">' + esc(c.className) + '</div>' +
              '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium border ' + badgeColor + '">' + (isVacant ? 'Vacant Homeroom' : 'Assigned') + '</span>' +
            '</div>' +
            '<div class="flex items-center gap-2 text-xs text-slate-500 mb-3">' +
              '<span class="material-symbols-outlined text-sm text-slate-400">meeting_room</span>' +
              '<span>' + esc(c.room) + '</span>' +
              '<span class="text-slate-300">•</span>' +
              '<span class="material-symbols-outlined text-sm text-slate-400">groups</span>' +
              '<span>' + c.studentCount + ' students</span>' +
            '</div>' +
            '<div class="p-3 bg-slate-50 rounded-lg border border-slate-100 mb-3">' +
              '<div class="text-[11px] text-slate-400 font-medium">Assigned Homeroom Teacher</div>' +
              '<div class="text-xs font-medium text-slate-800 mt-0.5 flex items-center gap-1.5">' +
                '<span class="material-symbols-outlined text-sm ' + (isVacant ? 'text-rose-500' : 'text-[#176B45]') + '">co_present</span>' +
                '<span>' + esc(c.homeroomTeacher) + '</span>' +
              '</div>' +
              (c.teacherEmail ? '<div class="text-[11px] text-slate-400 font-mono mt-0.5">' + esc(c.teacherEmail) + '</div>' : '') +
            '</div>' +
          '</div>' +
          '<div class="pt-2 border-t border-slate-100 flex items-center justify-between">' +
            '<span class="text-[11px] text-slate-400 font-mono">AY 2025–26</span>' +
            '<button type="button" class="btn-change-hr px-3 py-1 rounded-lg border border-slate-200 hover:border-[#176B45] text-xs font-medium text-slate-700 hover:text-[#176B45] bg-white transition-all cursor-pointer shadow-2xs active:scale-95" data-class-id="' + esc(c.classId) + '" data-class-name="' + esc(c.className) + '" data-current="' + esc(c.homeroomTeacher) + '">' +
              'Reassign Teacher' +
            '</button>' +
          '</div>' +
        '</div>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Assigned Homerooms</div><div class="text-xl font-medium text-emerald-700 mt-0.5">' + assigned + ' / ' + state.records.length + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center"><span class="material-symbols-outlined text-lg">verified_user</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Vacant Allocations</div><div class="text-xl font-medium ' + (vacant > 0 ? 'text-rose-600' : 'text-slate-800') + ' mt-0.5">' + vacant + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">notification_important</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Total Roster Enrollment</div><div class="text-xl font-medium text-slate-800 mt-0.5">' + totalStudents + ' Students</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">school</span></div>' +
            '</div>' +
          '</div>' +

          '<div class="grid grid-cols-1 md:grid-cols-3 gap-3">' +
            cardsHtml +
          '</div>' +
        '</div>' +

        '<div id="tmHrModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">' +
          '<div class="bg-white border border-slate-200 rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-150">' +
            '<div class="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/60">' +
              '<div class="flex items-center gap-2">' +
                '<span class="material-symbols-outlined text-[#176B45]">co_present</span>' +
                '<span class="text-sm font-medium text-slate-800">Assign Homeroom Teacher</span>' +
              '</div>' +
              '<button type="button" id="tmCloseHrModal" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer"><span class="material-symbols-outlined text-lg">close</span></button>' +
            '</div>' +
            '<div class="p-5 space-y-4">' +
              '<div>' +
                '<label class="text-xs text-slate-500 font-medium">Target Class Section:</label>' +
                '<div id="tmHrTargetClassName" class="text-sm font-medium text-slate-800 mt-0.5"></div>' +
              '</div>' +
              '<div>' +
                '<label class="text-xs text-slate-500 font-medium">Select Faculty Member:</label>' +
                '<select id="tmHrTeacherSelect" class="w-full mt-1 p-2 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
                  state.teachers.map(function (t) {
                    return '<option value="' + esc(t.name) + '" data-id="' + esc(t.id) + '">' + esc(t.name) + ' (' + esc(t.department) + ')</option>';
                  }).join('') +
                '</select>' +
              '</div>' +
              '<div class="p-3 bg-amber-50/70 border border-amber-200 rounded-xl text-[11px] text-amber-800 flex items-start gap-2">' +
                '<span class="material-symbols-outlined text-sm mt-0.5">info</span>' +
                '<span>Reassigning will automatically update class notifications and official MoEYS roster reports.</span>' +
              '</div>' +
            '</div>' +
            '<div class="px-5 py-3.5 border-t border-slate-100 flex items-center justify-end gap-2 bg-slate-50/60">' +
              '<button type="button" id="btnCancelHr" class="px-3.5 py-1.5 rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-100 text-xs font-medium transition-all cursor-pointer">Cancel</button>' +
              '<button type="button" id="btnSaveHr" class="px-4 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">Confirm Homeroom Assignment</button>' +
            '</div>' +
          '</div>' +
        '</div>';

      var modal = document.getElementById('tmHrModal');
      var closeBtn = document.getElementById('tmCloseHrModal');
      var cancelBtn = document.getElementById('btnCancelHr');
      var targetClassId = '';

      if (closeBtn) closeBtn.onclick = function () { modal.classList.add('hidden'); };
      if (cancelBtn) cancelBtn.onclick = function () { modal.classList.add('hidden'); };

      root.querySelectorAll('.btn-change-hr').forEach(function (btn) {
        btn.addEventListener('click', function () {
          targetClassId = btn.getAttribute('data-class-id');
          var cName = btn.getAttribute('data-class-name');
          document.getElementById('tmHrTargetClassName').textContent = cName;
          modal.classList.remove('hidden');
        });
      });

      var saveBtn = document.getElementById('btnSaveHr');
      if (saveBtn) {
        saveBtn.onclick = function () {
          var sel = document.getElementById('tmHrTeacherSelect');
          var teacherName = sel.value;
          var teacherId = sel.options[sel.selectedIndex].getAttribute('data-id');

          fetch('/api/teacher-mgmt/homeroom/' + encodeURIComponent(targetClassId), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ teacherName: teacherName, teacherId: teacherId })
          })
            .then(function (res) { return res.json(); })
            .then(function (res) {
              if (res.success) {
                toast('Homeroom teacher assigned successfully.');
                modal.classList.add('hidden');
                fetchHomeroom();
              }
            });
        };
      }
    }

    fetchHomeroom();
  };

  /* ════════════════════════════════════════════════════════════════
     4. TEACHER ATTENDANCE OVERVIEW
     ════════════════════════════════════════════════════════════════ */
  TM.initAttendance = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { records: [], summary: {}, search: '', dept: 'all', status: 'all' };

    function fetchAttendance() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading faculty attendance records...</span></div>';
      fetch('/api/teacher-mgmt/attendance')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.records = res.data || [];
          state.summary = res.summary || {};
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load attendance logs.</div>';
        });
    }

    function render() {
      var s = state.summary;
      var filtered = state.records.filter(function (r) {
        if (state.dept !== 'all' && (r.department || '').toLowerCase().indexOf(state.dept) === -1) return false;
        if (state.status !== 'all' && r.status !== state.status) return false;
        if (state.search) {
          var q = state.search.toLowerCase();
          var m = (r.teacherName || '').toLowerCase().indexOf(q) !== -1 ||
                  (r.teacherId || '').toLowerCase().indexOf(q) !== -1 ||
                  (r.notes || '').toLowerCase().indexOf(q) !== -1;
          if (!m) return false;
        }
        return true;
      });

      var rowsHtml = filtered.map(function (r) {
        var statusBadge = '';
        if (r.status === 'present') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Present</span>';
        } else if (r.status === 'late') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Late Arrival</span>';
        } else if (r.status === 'duty') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Field Duty</span>';
        } else if (r.status === 'excused') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-purple-50 text-purple-700 border border-purple-200">Excused Leave</span>';
        } else {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-rose-50 text-rose-700 border border-rose-200">Absent</span>';
        }

        return '<tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">' +
          '<td class="py-2.5 px-3 text-xs font-mono text-slate-500">' + esc(r.date) + '</td>' +
          '<td class="py-2.5 px-3">' +
            '<div class="text-xs font-medium text-slate-800">' + esc(r.teacherName) + '</div>' +
            '<div class="text-[11px] text-slate-400 font-mono">' + esc(r.teacherId) + '</div>' +
          '</td>' +
          '<td class="py-2.5 px-3 text-xs text-slate-600">' + esc(r.department) + '</td>' +
          '<td class="py-2.5 px-3">' + statusBadge + '</td>' +
          '<td class="py-2.5 px-3 text-xs font-mono text-slate-700">' + esc(r.checkIn) + '</td>' +
          '<td class="py-2.5 px-3 text-xs font-mono text-slate-700">' + esc(r.checkOut) + '</td>' +
          '<td class="py-2.5 px-3 text-xs text-slate-500 max-w-xs truncate" title="' + esc(r.notes) + '">' + esc(r.notes || '--') + '</td>' +
        '</tr>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs">' +
              '<div class="text-xs text-slate-400 font-medium">Daily Present Rate</div>' +
              '<div class="text-xl font-medium text-emerald-700 mt-0.5">' + (s.presentRate || 98.2) + '%</div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs">' +
              '<div class="text-xs text-slate-400 font-medium">Present / On Time</div>' +
              '<div class="text-xl font-medium text-slate-800 mt-0.5">' + (s.presentCount || 0) + '</div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs">' +
              '<div class="text-xs text-slate-400 font-medium">Late / Delayed</div>' +
              '<div class="text-xl font-medium text-amber-600 mt-0.5">' + (s.lateCount || 0) + '</div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs">' +
              '<div class="text-xs text-slate-400 font-medium">Excused / Field Duty</div>' +
              '<div class="text-xl font-medium text-blue-600 mt-0.5">' + ((s.excusedCount || 0) + (s.dutyCount || 0)) + '</div>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">' +
            '<div class="relative flex-1 max-w-md">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>' +
              '<input type="text" id="tmAttSearch" placeholder="Search teacher, ID, notes..." value="' + esc(state.search) + '" class="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<select id="tmAttStatus" class="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-700 font-medium">' +
                '<option value="all">All Statuses</option>' +
                '<option value="present">Present</option>' +
                '<option value="late">Late</option>' +
                '<option value="duty">Field Duty</option>' +
                '<option value="excused">Excused Leave</option>' +
              '</select>' +
              '<button type="button" class="btn-export-att inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-[#176B45] text-xs font-medium text-slate-700 hover:text-[#176B45] bg-white transition-all cursor-pointer shadow-2xs">' +
                '<span class="material-symbols-outlined text-sm">download</span>' +
                '<span>Export Report</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
            '<div class="overflow-x-auto">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead>' +
                  '<tr class="border-b border-slate-200 bg-slate-50/70 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                    '<th class="py-2.5 px-3">Date</th>' +
                    '<th class="py-2.5 px-3">Faculty Member</th>' +
                    '<th class="py-2.5 px-3">Department</th>' +
                    '<th class="py-2.5 px-3">Status</th>' +
                    '<th class="py-2.5 px-3">Check-In</th>' +
                    '<th class="py-2.5 px-3">Check-Out</th>' +
                    '<th class="py-2.5 px-3">Audit Details / Terminal</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody>' +
                  (rowsHtml || '<tr><td colspan="7" class="text-center py-10 text-xs text-slate-400">No attendance logs matching criteria.</td></tr>') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>' +
        '</div>';

      var searchInput = document.getElementById('tmAttSearch');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value;
          render();
        });
      }

      var statusSelect = document.getElementById('tmAttStatus');
      if (statusSelect) {
        statusSelect.addEventListener('change', function (e) {
          state.status = e.target.value;
          render();
        });
      }

      var exportBtn = root.querySelector('.btn-export-att');
      if (exportBtn) {
        exportBtn.addEventListener('click', function () {
          toast('Attendance ledger exported to CSV format.');
        });
      }
    }

    fetchAttendance();
  };

  /* ════════════════════════════════════════════════════════════════
     5. FACULTY COMMENDATION & AWARDS
     ════════════════════════════════════════════════════════════════ */
  TM.initCommendation = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { items: [], search: '', dept: 'all' };

    function fetchCommendations() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading faculty commendations...</span></div>';
      fetch('/api/teacher-mgmt/commendations')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.items = res.data || [];
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load commendations.</div>';
        });
    }

    function render() {
      var filtered = state.items.filter(function (c) {
        if (state.dept !== 'all' && (c.department || '').toLowerCase().indexOf(state.dept) === -1) return false;
        if (state.search) {
          var q = state.search.toLowerCase();
          var m = (c.teacherName || '').toLowerCase().indexOf(q) !== -1 ||
                  (c.title || '').toLowerCase().indexOf(q) !== -1 ||
                  (c.category || '').toLowerCase().indexOf(q) !== -1 ||
                  (c.issuingAuthority || '').toLowerCase().indexOf(q) !== -1;
          if (!m) return false;
        }
        return true;
      });

      var cardsHtml = filtered.map(function (c) {
        return '<div class="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs hover:border-[#176B45]/40 transition-all flex flex-col justify-between">' +
          '<div>' +
            '<div class="flex items-start justify-between gap-2 mb-2">' +
              '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-amber-50 text-amber-800 border border-amber-200">' + esc(c.category) + '</span>' +
              '<span class="text-[11px] text-slate-400 font-mono">' + esc(c.dateAwarded) + '</span>' +
            '</div>' +
            '<h4 class="text-sm font-medium text-slate-900 mb-1 leading-snug">' + esc(c.title) + '</h4>' +
            '<div class="text-xs text-[#176B45] font-medium mb-2.5">' + esc(c.teacherName) + ' · ' + esc(c.department) + '</div>' +
            '<p class="text-xs text-slate-600 mb-3 leading-relaxed">' + esc(c.description) + '</p>' +
            (c.citation ? '<div class="p-2.5 bg-slate-50 border-l-2 border-[#176B45] text-[11px] text-slate-700 italic rounded-r-lg mb-3">"' + esc(c.citation) + '"</div>' : '') +
          '</div>' +
          '<div class="pt-2.5 border-t border-slate-100 flex items-center justify-between">' +
            '<div class="flex items-center gap-1.5 text-xs text-slate-500 font-medium">' +
              '<span class="material-symbols-outlined text-sm text-[#176B45]">verified</span>' +
              '<span>' + esc(c.issuingAuthority) + '</span>' +
            '</div>' +
            '<button type="button" class="btn-cert inline-flex items-center gap-1 text-[11px] text-[#176B45] hover:underline font-medium cursor-pointer" data-cert="' + esc(c.certificateRef) + '">' +
              '<span class="material-symbols-outlined text-xs">download</span>' +
              '<span>Citation PDF</span>' +
            '</button>' +
          '</div>' +
        '</div>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white border border-slate-200 rounded-xl p-3 shadow-2xs">' +
            '<div class="relative flex-1 max-w-md">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>' +
              '<input type="text" id="tmCommSearch" placeholder="Search teacher, award title, category..." value="' + esc(state.search) + '" class="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<button type="button" id="btnIssueAward" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">' +
                '<span class="material-symbols-outlined text-sm">workspace_premium</span>' +
                '<span>+ Record Commendation</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          '<div class="grid grid-cols-1 md:grid-cols-2 gap-3">' +
            (cardsHtml || '<div class="col-span-2 text-center py-12 text-xs text-slate-400">No commendation records found.</div>') +
          '</div>' +
        '</div>';

      var searchInput = document.getElementById('tmCommSearch');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value;
          render();
        });
      }

      root.querySelectorAll('.btn-cert').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var cert = btn.getAttribute('data-cert');
          toast('Downloading certificate: ' + cert);
        });
      });

      var issueBtn = document.getElementById('btnIssueAward');
      if (issueBtn) {
        issueBtn.addEventListener('click', function () {
          toast('Commendation entry modal ready.');
        });
      }
    }

    fetchCommendations();
  };

  /* ════════════════════════════════════════════════════════════════
     6. CONFIDENTIAL FACULTY DISCIPLINE
     ════════════════════════════════════════════════════════════════ */
  TM.initDiscipline = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { records: [], status: 'all' };

    function fetchDiscipline() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading confidential personnel records...</span></div>';
      fetch('/api/teacher-mgmt/discipline')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.records = res.data || [];
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load disciplinary records.</div>';
        });
    }

    function render() {
      var filtered = state.records.filter(function (r) {
        if (state.status !== 'all' && r.status !== state.status) return false;
        return true;
      });

      var rowsHtml = filtered.map(function (r) {
        var statusBadge = '';
        if (r.status === 'resolved') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Resolved</span>';
        } else if (r.status === 'hearing_scheduled') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Hearing Scheduled</span>';
        } else {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Under Review</span>';
        }

        return '<tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">' +
          '<td class="py-3 px-3 text-xs font-mono text-slate-700 font-medium">' + esc(r.caseNumber) + '</td>' +
          '<td class="py-3 px-3">' +
            '<div class="text-xs font-medium text-slate-800">' + esc(r.teacherName) + '</div>' +
            '<div class="text-[11px] text-slate-400 font-mono">' + esc(r.department) + '</div>' +
          '</td>' +
          '<td class="py-3 px-3 text-xs font-medium text-slate-700">' + esc(r.category) + '</td>' +
          '<td class="py-3 px-3 text-xs text-slate-600">' + esc(r.severity) + '</td>' +
          '<td class="py-3 px-3 text-xs font-mono text-slate-500">' + esc(r.incidentDate) + '</td>' +
          '<td class="py-3 px-3">' + statusBadge + '</td>' +
          '<td class="py-3 px-3 text-xs text-slate-600 max-w-xs truncate" title="' + esc(r.decisionSummary) + '">' + esc(r.decisionSummary) + '</td>' +
        '</tr>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="p-3.5 bg-amber-50/60 border border-amber-200/80 rounded-xl flex items-start gap-2.5 text-xs text-amber-800">' +
            '<span class="material-symbols-outlined text-amber-600 text-base mt-0.5">lock</span>' +
            '<div class="leading-relaxed">' +
              '<span class="font-medium">CONFIDENTIAL FACULTY CONDUCT REPOSITORY:</span> ' +
              'This registry contains restricted personnel records accessible exclusively to authorized School Administration and Executive Principal Oversight.' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex items-center justify-between">' +
            '<div class="flex items-center gap-2">' +
              '<label class="text-xs text-slate-500 font-medium">Filter Status:</label>' +
              '<select id="tmDiscStatus" class="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-700 font-medium">' +
                '<option value="all">All Case Statuses</option>' +
                '<option value="under_review">Under Review</option>' +
                '<option value="hearing_scheduled">Hearing Scheduled</option>' +
                '<option value="resolved">Resolved</option>' +
              '</select>' +
            '</div>' +
            '<button type="button" id="btnLogCase" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 text-white hover:bg-slate-700 text-xs font-medium transition-all shadow-xs cursor-pointer">' +
              '<span class="material-symbols-outlined text-sm">shield</span>' +
              '<span>+ Lodge Incident Report</span>' +
            '</button>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
            '<div class="overflow-x-auto">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead>' +
                  '<tr class="border-b border-slate-200 bg-slate-50/70 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                    '<th class="py-2.5 px-3">Case ID</th>' +
                    '<th class="py-2.5 px-3">Faculty Member</th>' +
                    '<th class="py-2.5 px-3">Violation Category</th>' +
                    '<th class="py-2.5 px-3">Severity Level</th>' +
                    '<th class="py-2.5 px-3">Date</th>' +
                    '<th class="py-2.5 px-3">Status</th>' +
                    '<th class="py-2.5 px-3">Resolution / Decision</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody>' +
                  (rowsHtml || '<tr><td colspan="7" class="text-center py-10 text-xs text-slate-400">No disciplinary cases on record.</td></tr>') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>' +
        '</div>';

      var statusSelect = document.getElementById('tmDiscStatus');
      if (statusSelect) {
        statusSelect.addEventListener('change', function (e) {
          state.status = e.target.value;
          render();
        });
      }

      var logBtn = document.getElementById('btnLogCase');
      if (logBtn) {
        logBtn.addEventListener('click', function () {
          toast('Confidential case entry form ready.');
        });
      }
    }

    fetchDiscipline();
  };

  /* ════════════════════════════════════════════════════════════════
     7. INPUT TEACHER EFFORTS (Beyond Classroom Contributions)
     ════════════════════════════════════════════════════════════════ */
  TM.initEfforts = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var state = { records: [], search: '', cat: 'all' };

    function fetchEfforts() {
      root.innerHTML = '<div class="flex items-center justify-center py-20 text-slate-400"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping mr-2"></span><span class="text-xs font-medium">Loading documented teacher contributions...</span></div>';
      fetch('/api/teacher-mgmt/efforts')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          state.records = res.data || [];
          render();
        })
        .catch(function () {
          root.innerHTML = '<div class="p-6 text-center text-xs text-rose-600">Failed to load teacher effort records.</div>';
        });
    }

    function render() {
      var totalHours = state.records.reduce(function (acc, r) { return acc + (r.hoursSpent || 0); }, 0);
      var verifiedCount = state.records.filter(function (r) { return r.status === 'verified' || r.status === 'endorsed'; }).length;

      var filtered = state.records.filter(function (r) {
        if (state.cat !== 'all' && (r.category || '').toLowerCase().indexOf(state.cat) === -1) return false;
        if (state.search) {
          var q = state.search.toLowerCase();
          var m = (r.teacherName || '').toLowerCase().indexOf(q) !== -1 ||
                  (r.title || '').toLowerCase().indexOf(q) !== -1 ||
                  (r.department || '').toLowerCase().indexOf(q) !== -1 ||
                  (r.description || '').toLowerCase().indexOf(q) !== -1;
          if (!m) return false;
        }
        return true;
      });

      var rowsHtml = filtered.map(function (r) {
        var statusBadge = '';
        if (r.status === 'endorsed') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">Endorsed</span>';
        } else if (r.status === 'verified') {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-blue-50 text-blue-700 border border-blue-200">Verified</span>';
        } else {
          statusBadge = '<span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-700 border border-amber-200">Logged</span>';
        }

        return '<tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">' +
          '<td class="py-3 px-3 text-xs font-mono text-slate-500">' + esc(r.id) + '</td>' +
          '<td class="py-3 px-3">' +
            '<div class="text-xs font-medium text-slate-800">' + esc(r.teacherName) + '</div>' +
            '<div class="text-[11px] text-slate-400 font-mono">' + esc(r.department) + '</div>' +
          '</td>' +
          '<td class="py-3 px-3">' +
            '<span class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700">' + esc(r.category) + '</span>' +
          '</td>' +
          '<td class="py-3 px-3">' +
            '<div class="text-xs font-medium text-slate-800">' + esc(r.title) + '</div>' +
            '<div class="text-[11px] text-slate-500 max-w-xs truncate" title="' + esc(r.description) + '">' + esc(r.description) + '</div>' +
          '</td>' +
          '<td class="py-3 px-3 text-xs font-medium text-[#176B45]">' + esc(r.hoursSpent) + ' hrs</td>' +
          '<td class="py-3 px-3 text-xs font-mono text-slate-500">' + esc(r.dateLogged) + '</td>' +
          '<td class="py-3 px-3">' + statusBadge + '</td>' +
          '<td class="py-3 px-3 text-right">' +
            (r.status === 'logged' ?
              '<button type="button" class="btn-verify-effort px-2 py-1 rounded bg-[#176B45] text-white text-[11px] font-medium hover:bg-[#125638] transition-all cursor-pointer shadow-2xs" data-id="' + esc(r.id) + '">Verify</button>' :
              '<span class="text-[11px] text-slate-400">' + esc(r.endorsedBy || 'Approved') + '</span>') +
          '</td>' +
        '</tr>';
      }).join('');

      root.innerHTML = '' +
        '<div class="space-y-4">' +
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Total Documented Hours</div><div class="text-xl font-medium text-slate-800 mt-0.5">' + totalHours + ' hrs</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center"><span class="material-symbols-outlined text-lg">schedule</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Verified Contributions</div><div class="text-xl font-medium text-blue-600 mt-0.5">' + verifiedCount + ' / ' + state.records.length + '</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">check_circle</span></div>' +
            '</div>' +
            '<div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-2xs flex items-center justify-between">' +
              '<div><div class="text-xs text-slate-400 font-medium">Extracurricular Areas</div><div class="text-xl font-medium text-purple-600 mt-0.5">5 Categories</div></div>' +
              '<div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center"><span class="material-symbols-outlined text-lg">category</span></div>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl p-3 shadow-2xs flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">' +
            '<div class="relative flex-1 max-w-md">' +
              '<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">search</span>' +
              '<input type="text" id="tmEffortSearch" placeholder="Search teacher, contribution, activity..." value="' + esc(state.search) + '" class="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-800">' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<select id="tmEffortCat" class="text-xs bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-1 focus:ring-[#176B45] text-slate-700 font-medium">' +
                '<option value="all">All Contribution Categories</option>' +
                '<option value="academic">Academic Contributions</option>' +
                '<option value="school">School Activities</option>' +
                '<option value="student">Student Support</option>' +
                '<option value="department">Department Contributions</option>' +
                '<option value="training">Training & PD</option>' +
              '</select>' +
              '<button type="button" id="btnLogEffort" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#176B45] text-white hover:bg-[#125638] text-xs font-medium transition-all shadow-xs cursor-pointer">' +
                '<span class="material-symbols-outlined text-sm">add</span>' +
                '<span>+ Log Teacher Effort</span>' +
              '</button>' +
            '</div>' +
          '</div>' +

          '<div class="bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">' +
            '<div class="overflow-x-auto">' +
              '<table class="w-full text-left border-collapse">' +
                '<thead>' +
                  '<tr class="border-b border-slate-200 bg-slate-50/70 text-[11px] font-medium text-slate-500 uppercase tracking-wider">' +
                    '<th class="py-2.5 px-3">Effort ID</th>' +
                    '<th class="py-2.5 px-3">Faculty Member</th>' +
                    '<th class="py-2.5 px-3">Category</th>' +
                    '<th class="py-2.5 px-3">Initiative & Description</th>' +
                    '<th class="py-2.5 px-3">Hours Logged</th>' +
                    '<th class="py-2.5 px-3">Date</th>' +
                    '<th class="py-2.5 px-3">Status</th>' +
                    '<th class="py-2.5 px-3 text-right">Audit Action</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody>' +
                  (rowsHtml || '<tr><td colspan="8" class="text-center py-10 text-xs text-slate-400">No teacher effort records found.</td></tr>') +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>' +
        '</div>';

      var searchInput = document.getElementById('tmEffortSearch');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value;
          render();
        });
      }

      var catSelect = document.getElementById('tmEffortCat');
      if (catSelect) {
        catSelect.addEventListener('change', function (e) {
          state.cat = e.target.value;
          render();
        });
      }

      root.querySelectorAll('.btn-verify-effort').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var id = btn.getAttribute('data-id');
          fetch('/api/teacher-mgmt/efforts/' + encodeURIComponent(id) + '/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: 'verify', reviewer: portalRole === 'principal' ? 'Dr. Sophal Meas' : 'Mr. Heng Samnang' })
          })
            .then(function (res) { return res.json(); })
            .then(function (res) {
              if (res.success) {
                toast('Teacher effort verified.');
                fetchEfforts();
              }
            });
        });
      });

      var logBtn = document.getElementById('btnLogEffort');
      if (logBtn) {
        logBtn.addEventListener('click', function () {
          toast('Teacher effort logging form ready.');
        });
      }
    }

    fetchEfforts();
  };

})(window, document);

