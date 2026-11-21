/**
 * NGIS Teacher Management — Verify Teacher Profile Updates
 * ---------------------------------------------------------------------------
 * Mirrors the Student clearance workspace (assets/js/ngis-student-workspace.js):
 * KPI strip, filter toolbar, status tabs, clearance ledger, diff review modal,
 * approve / reject / request-correction workflow and CSV export.
 *
 * Deliberately omits the duplicate in-page header (eyebrow, title, round badge,
 * description) — the hero banner owns the workspace title. Status values are
 * flat text labels, never rounded colour-filled pills.
 *
 * Live data: /api/teacher-mgmt/verify and /api/teacher-mgmt/verify/<id>/action
 * Design: scoped .ngis-sm / .smx-* classes from assets/css/design-system.css
 */
(function (window, document) {
  'use strict';

  var TV = window.NGIS_TEACHER_VERIFY = window.NGIS_TEACHER_VERIFY || {};
  TV.version = '1.0';

  var activeModal = null;
  var toastEl = null;
  var toastTimer = null;

  /* ── Shared helpers ─────────────────────────────────────────────────── */

  function esc(value) {
    if (value === null || value === undefined) return '';
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function icon(name, extra) {
    return '<span class="material-symbols-outlined smx-icon' + (extra ? ' ' + extra : '') + '">' + esc(name) + '</span>';
  }

  /* Flat status label. No rounded pills anywhere in this workspace. */
  function statusLabel(status) {
    var map = {
      pending: ['Pending Review', 'warn'],
      approved: ['Approved & Synced', 'ok'],
      rejected: ['Rejected', 'bad'],
      needs_correction: ['Needs Clarification', 'bad']
    };
    var pair = map[status] || [status || 'Unknown', 'neutral'];
    return '<span class="smx-status ' + pair[1] + '">' + esc(pair[0]) + '</span>';
  }

  function kpiHtml(label, valueHtml, foot, iconName, tone) {
    return '<article class="smx-kpi">' +
      '<div class="smx-kpi-top">' +
        '<span class="smx-kpi-label">' + esc(label) + '</span>' +
        '<span class="smx-kpi-icon' + (tone ? ' ' + esc(tone) : '') + '">' + icon(iconName, 'sm') + '</span>' +
      '</div>' +
      '<div class="smx-kpi-value">' + valueHtml + '</div>' +
      '<div class="smx-kpi-foot"><i' + (tone ? ' class="' + esc(tone) + '"' : '') + '></i><span>' + esc(foot) + '</span></div>' +
    '</article>';
  }

  function pagerHtml(total, page, size, noun) {
    var pages = Math.max(1, Math.ceil(total / size));
    var from = total ? (page - 1) * size + 1 : 0;
    var to = Math.min(page * size, total);
    var start = Math.max(1, page - 2);
    var end = Math.min(pages, start + 4);
    start = Math.max(1, end - 4);
    var h = '<div class="smx-table-foot">' +
      '<span>Showing ' + from + '&ndash;' + to + ' of ' + total + ' ' + esc(noun) + '</span>' +
      '<div class="smx-pager">' +
        '<button type="button" class="smx-page" data-act="page" data-page="' + Math.max(1, page - 1) + '"' + (page <= 1 ? ' disabled' : '') + '>Previous</button>';
    for (var i = start; i <= end; i++) {
      h += '<button type="button" class="smx-page' + (i === page ? ' active' : '') + '" data-act="page" data-page="' + i + '">' + i + '</button>';
    }
    h += '<button type="button" class="smx-page" data-act="page" data-page="' + Math.min(pages, page + 1) + '"' + (page >= pages ? ' disabled' : '') + '>Next</button>' +
      '</div></div>';
    return h;
  }

  function emptyRow(colspan, message) {
    return '<tr><td class="smx-empty" colspan="' + colspan + '">' + icon('folder_off') + '<div>' + esc(message) + '</div></td></tr>';
  }

  function toast(__a, __b) {
  /* Shared NGIS operation-feedback engine (ui-states.js) — single
     implementation across all portals; no page-local toast UI anymore. */
  if (!(window.NGISUI && window.NGISUI.toast)) {
    if (window.console) console.warn('toast unavailable:', __a);
    return null;
  }
  var __k = __b;
  if (__b === true || __b === 'error' || __b === 'danger' || __b === 'fail' || __b === 'isError') __k = 'error';
  else if (__b === 'warning' || __b === 'warn') __k = 'warning';
  else if (__b === 'info') __k = 'info';
  else if (__b === 'loading') __k = 'loading';
  else if (__b === false || __b === undefined || __b === null || __b === 'success' || __b === 'ok' || __b === 'done') __k = 'success';
  else __k = 'info';
  return window.NGISUI.toast.show(__k, String(__a));
}

  function closeModal() {
    if (activeModal && activeModal.remove) activeModal.remove();
    else if (activeModal) activeModal.innerHTML = '';
    activeModal = null;
  }

  function findAct(node) {
    while (node && node.getAttribute) {
      var act = node.getAttribute('data-act');
      if (act) return node;
      node = node.parentNode;
    }
    return null;
  }

  function findAttr(node, attr) {
    while (node && node.getAttribute) {
      var value = node.getAttribute(attr);
      if (value !== null && value !== undefined && value !== '') return value;
      node = node.parentNode;
    }
    return null;
  }

  function openModal(html, handlers) {
    closeModal();
    var wrap = document.createElement('div');
    wrap.className = 'smx-modal-backdrop';
    wrap.innerHTML = html;
    if (document.body && document.body.appendChild) document.body.appendChild(wrap);
    activeModal = wrap;
    if (handlers && handlers.input) wrap.addEventListener('input', handlers.input);
    wrap.addEventListener('click', function (e) {
      if (e.target === wrap) { closeModal(); return; }
      var btn = findAct(e.target);
      if (!btn) return;
      var act = btn.getAttribute('data-act');
      if (act === 'close-modal') { closeModal(); return; }
      if (handlers && handlers.click) handlers.click(act, btn, e);
    });
    return wrap;
  }

  function fetchJson(url, options) {
    if (typeof fetch !== 'function') return Promise.reject(new Error('fetch unavailable'));
    return fetch(url, options).then(function (res) {
      if (res && res.ok === false) throw new Error('HTTP ' + (res.status || 0));
      return res.json();
    });
  }

  function postJson(url, body) {
    return fetchJson(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    });
  }

  function csvCell(value) {
    return '"' + String(value === null || value === undefined ? '' : value).replace(/"/g, '""') + '"';
  }

  function downloadCsv(filename, headers, rows) {
    if (typeof Blob === 'undefined' || !window.URL || !window.URL.createObjectURL) {
      toast('CSV export is unavailable in this browser', 'error');
      return;
    }
    var lines = [headers.map(csvCell).join(',')];
    rows.forEach(function (row) { lines.push(row.map(csvCell).join(',')); });
    var blob = new Blob(['\uFEFF' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
    var url = window.URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    if (document.body && document.body.appendChild) document.body.appendChild(link);
    if (link.click) link.click();
    if (document.body && document.body.removeChild) document.body.removeChild(link);
    if (window.URL.revokeObjectURL) window.URL.revokeObjectURL(url);
    toast('CSV exported');
  }

  function option(value, label, selected) {
    return '<option value="' + esc(value) + '"' + (selected ? ' selected' : '') + '>' + esc(label) + '</option>';
  }

  function tabHtml(label, count, key, active) {
    return '<button type="button" class="smx-tab' + (active ? ' active' : '') + '" data-tab="' + esc(key) + '">' +
      esc(label) + '<span class="count">' + count + '</span></button>';
  }

  function selectAllHtml(checked) {
    return '<input type="checkbox" class="smx-checkbox" id="tmxSelectAll" data-act="select-all"' + (checked ? ' checked' : '') + ' aria-label="Select all rows">';
  }

  function rowCheckbox(id, selected) {
    return '<input type="checkbox" class="smx-checkbox" data-act="select" data-id="' + esc(id) + '"' + (selected ? ' checked' : '') + ' aria-label="Select row">';
  }

  function personHtml(initials, name, meta) {
    return '<div class="smx-person">' +
      '<span class="smx-avatar">' + esc(initials || 'TC') + '</span>' +
      '<div><div class="smx-person-name">' + esc(name) + '</div><div class="smx-mono">' + esc(meta) + '</div></div>' +
    '</div>';
  }

  function initials(name) {
    var parts = String(name || 'Teacher').replace(/^(Dr\.|Mr\.|Ms\.|Mrs\.)\s*/i, '').trim().split(/\s+/);
    return ((parts[0] || 'T').charAt(0) + (parts.length > 1 ? parts[parts.length - 1].charAt(0) : '')).toUpperCase();
  }

  function loadingHtml(label) {
    if (window.NGIS_SKELETON) {
      return '<div class="ngis-sm" data-renderer="ngis-teacher-verify">' + window.NGIS_SKELETON.table({ rows: 5 }) + '</div>';
    }
    return '<div class="ngis-sm" data-renderer="ngis-teacher-verify">' +
      '<div class="smx-card"><div class="smx-card-body smx-empty">' + icon('hourglass_top') + '<div>' + esc(label) + '</div></div></div>' +
    '</div>';
  }

  /* The mandatory mobile appbar already owns the sidebar toggle on small
     screens; pin the hero topbar's duplicate control closed. */
  function suppressDuplicateHamburger() {
    var htb = document.getElementById('htbHamburger');
    if (!htb) return;
    var mq = window.matchMedia('(max-width: 767px)');
    var apply = function () {
      if (mq.matches) htb.style.setProperty('display', 'none', 'important');
      else htb.style.removeProperty('display');
    };
    apply();
    if (mq.addEventListener) mq.addEventListener('change', apply);
    else if (mq.addListener) mq.addListener(apply);
  }

  /* ======================================================================
     VERIFY TEACHER PROFILE UPDATES
     ====================================================================== */

  TV.init = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;
    suppressDuplicateHamburger();

    var state = {
      items: [],
      search: '',
      status: 'all',
      department: 'all',
      field: 'all',
      tab: 'all',
      page: 1,
      pageSize: 8,
      selected: {},
      rejectReason: '',
      reviewComments: ''
    };

    root.innerHTML = loadingHtml('Loading teacher profile update requests...');
    bind();
    load();

    function load() {
      fetchJson('/api/teacher-mgmt/verify').then(function (res) {
        state.items = res && res.data ? res.data : [];
        render();
      }).catch(function () {
        state.items = [];
        render();
        toast('Failed to load teacher update requests', 'error');
      });
    }

    function itemById(id) {
      for (var i = 0; i < state.items.length; i++) if (state.items[i].id === id) return state.items[i];
      return null;
    }

    function departmentOptions() {
      var seen = { all: true }, out = ['all'];
      state.items.forEach(function (item) {
        var d = String(item.department || '').trim();
        if (d && !seen[d]) { seen[d] = true; out.push(d); }
      });
      return out;
    }

    function countStatus(status) {
      return state.items.filter(function (i) { return i.status === status; }).length;
    }

    function flaggedCount() {
      return state.items.filter(function (i) { return i.status === 'rejected' || i.status === 'needs_correction'; }).length;
    }

    function turnaround() {
      var diffs = [];
      state.items.forEach(function (item) {
        if (item.status !== 'approved' || !item.submittedDate || !item.reviewedDate) return;
        var a = Date.parse(String(item.submittedDate).replace(' ', 'T'));
        var b = Date.parse(String(item.reviewedDate).replace(' ', 'T'));
        if (!isNaN(a) && !isNaN(b) && b > a) diffs.push((b - a) / 3600000);
      });
      if (!diffs.length) return '2.1';
      var sum = diffs.reduce(function (a, b) { return a + b; }, 0);
      return (sum / diffs.length).toFixed(1);
    }

    function filtered() {
      var q = state.search.toLowerCase().trim();
      return state.items.filter(function (item) {
        if (q) {
          var hay = [item.teacherName, item.teacherId, item.id, item.fieldChanged, item.department].join(' ').toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        if (state.tab === 'pending' && item.status !== 'pending') return false;
        if (state.tab === 'approved' && item.status !== 'approved') return false;
        if (state.tab === 'flagged' && item.status !== 'rejected' && item.status !== 'needs_correction') return false;
        if (state.status !== 'all') {
          if (state.status === 'needs_correction') {
            if (item.status !== 'needs_correction' && item.status !== 'rejected') return false;
          } else if (item.status !== state.status) return false;
        }
        if (state.department !== 'all' && String(item.department || '').toLowerCase() !== state.department.toLowerCase()) return false;
        if (state.field !== 'all' && String(item.fieldChanged || '').toLowerCase().indexOf(state.field) === -1) return false;
        return true;
      });
    }

    function pageItems(list) {
      var pages = Math.max(1, Math.ceil(list.length / state.pageSize));
      if (state.page > pages) state.page = pages;
      var start = (state.page - 1) * state.pageSize;
      return list.slice(start, start + state.pageSize);
    }

    function selectedIds() {
      return Object.keys(state.selected).filter(function (id) { return state.selected[id]; });
    }

    function exportCsv() {
      var rows = filtered().map(function (r) {
        return [r.id, r.teacherId, r.teacherName, r.department, r.fieldChanged, r.previousValue,
          r.proposedValue, r.status, r.submittedDate, r.reviewedBy, r.reviewedDate, r.comments];
      });
      downloadCsv('NGIS_Teacher_Update_Audit_Ledger.csv', [
        'Request ID', 'Teacher ID', 'Teacher Name', 'Department', 'Field Changed', 'Current Value',
        'Proposed Amendment', 'Status', 'Submitted', 'Reviewed By', 'Reviewed At', 'Review Remarks'
      ], rows);
    }

    function reviewerName() {
      return portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office';
    }

    function approveItem(id, silent) {
      var item = itemById(id);
      if (!item || item.status === 'approved') return;
      postJson('/api/teacher-mgmt/verify/' + encodeURIComponent(id) + '/action', {
        action: 'approve',
        comments: 'Approved and synchronized with teacher record.',
        reviewer: reviewerName()
      }).then(function (res) {
        if (!res || res.success === false) { toast((res && res.message) || 'Approval failed', 'error'); return; }
        item.status = 'approved';
        item.reviewedDate = 'Just now';
        render();
        if (!silent) toast('Update request approved and synchronized with teacher ledger');
      }).catch(function () { toast('Failed to approve request', 'error'); });
    }

    function bulkApprove() {
      var ids = selectedIds().filter(function (id) {
        var item = itemById(id);
        return item && item.status === 'pending';
      });
      if (!ids.length) { toast('Select at least one pending request', 'error'); return; }
      Promise.all(ids.map(function (id) {
        return postJson('/api/teacher-mgmt/verify/' + encodeURIComponent(id) + '/action', {
          action: 'approve',
          comments: 'Bulk approved from clearance ledger.',
          reviewer: reviewerName()
        });
      })).then(function () {
        ids.forEach(function (id) { var item = itemById(id); if (item) item.status = 'approved'; });
        state.selected = {};
        render();
        toast(ids.length + ' request(s) approved and synchronized');
      }).catch(function () { toast('Bulk approval failed', 'error'); });
    }

    function openRejectModal(id) {
      var item = itemById(id);
      if (!item) return;
      state.rejectReason = '';
      var html = '<div class="smx-modal">' +
        '<div class="smx-modal-head"><div><div class="smx-modal-title">Reject Profile Amendment</div>' +
          '<div class="smx-modal-sub">' + esc(item.id) + ' &middot; ' + esc(item.teacherName) + '</div></div>' +
          '<button type="button" class="smx-close" data-act="close-modal" aria-label="Close">' + icon('close', 'sm') + '</button></div>' +
        '<div class="smx-modal-body">' +
          '<p class="smx-muted">Supply a reason for the audit ledger. The teacher will be notified after rejection.</p>' +
          '<div class="smx-section-label">Reason for rejection</div>' +
          '<textarea id="tmxRejectReason" class="smx-textarea" placeholder="e.g. Missing official HR verification"></textarea>' +
          '<div class="smx-doc">' + icon('info', 'sm') + '<span>This action is recorded on the staff audit trail.</span></div>' +
        '</div>' +
        '<div class="smx-modal-foot">' +
          '<button type="button" class="smx-btn" data-act="close-modal">Cancel</button>' +
          '<button type="button" class="smx-btn danger" data-act="confirm-reject">' + icon('block', 'sm') + 'Confirm Rejection</button>' +
        '</div></div>';
      openModal(html, {
        input: function (e) { if (e.target && e.target.id === 'tmxRejectReason') state.rejectReason = e.target.value; },
        click: function (act) {
          if (act !== 'confirm-reject') return;
          if (!state.rejectReason.trim()) { toast('Please enter a rejection reason', 'error'); return; }
          postJson('/api/teacher-mgmt/verify/' + encodeURIComponent(item.id) + '/action', {
            action: 'reject',
            comments: state.rejectReason,
            reviewer: reviewerName()
          }).then(function (res) {
            if (!res || res.success === false) { toast((res && res.message) || 'Rejection failed', 'error'); return; }
            item.status = 'rejected';
            item.comments = state.rejectReason;
            closeModal();
            render();
            toast('Update request rejected and recorded on audit trail');
          }).catch(function () { toast('Failed to process rejection', 'error'); });
        }
      });
    }

    function openReviewModal(id) {
      var item = itemById(id);
      if (!item) return;
      state.reviewComments = item.comments || '';
      var html = '<div class="smx-modal wide">' +
        '<div class="smx-modal-head"><div><div class="smx-modal-title">Review Profile Amendment Diff</div>' +
          '<div class="smx-modal-sub">' + esc(item.id) + ' &middot; ' + esc(item.fieldChanged) + '</div></div>' +
          '<button type="button" class="smx-close" data-act="close-modal" aria-label="Close">' + icon('close', 'sm') + '</button></div>' +
        '<div class="smx-modal-body">' +
          '<div class="smx-info-grid">' +
            '<div class="smx-info"><span class="label">Teacher</span><span class="value">' + esc(item.teacherName) + ' (' + esc(item.teacherId) + ')</span></div>' +
            '<div class="smx-info"><span class="label">Department</span><span class="value">' + esc(item.department) + '</span></div>' +
            '<div class="smx-info"><span class="label">Submitted on</span><span class="value">' + esc(item.submittedDate) + '</span></div>' +
            '<div class="smx-info"><span class="label">Current status</span><span class="value">' + esc(item.status) + '</span></div>' +
          '</div>' +
          '<div class="smx-section-label">Field amendment</div>' +
          '<div class="smx-diff">' +
            '<div><span class="label">Current ledger value</span><div class="old">' + esc(item.previousValue) + '</div></div>' +
            '<div><span class="label">Proposed amendment</span><div class="new">' + esc(item.proposedValue) + '</div></div>' +
          '</div>' +
          '<div class="smx-section-label">Supporting documentation</div>' +
          '<div class="smx-doc">' + icon('attach_file', 'sm') + '<span>' + esc(item.supportingDocument || 'document.pdf') + '</span></div>' +
          '<div class="smx-section-label">Official reviewer note</div>' +
          '<textarea id="tmxReviewComments" class="smx-textarea" placeholder="Input rationale or verification remarks...">' + esc(state.reviewComments) + '</textarea>' +
        '</div>' +
        '<div class="smx-modal-foot">' +
          '<button type="button" class="smx-btn danger" data-act="modal-reject">Reject Request</button>' +
          '<button type="button" class="smx-btn" data-act="modal-correct">Request Correction</button>' +
          '<button type="button" class="smx-btn primary" data-act="modal-approve">' + icon('verified', 'sm') + 'Approve & Sync Ledger</button>' +
        '</div></div>';
      openModal(html, {
        input: function (e) { if (e.target && e.target.id === 'tmxReviewComments') state.reviewComments = e.target.value; },
        click: function (act) {
          if (act === 'modal-reject') { closeModal(); openRejectModal(item.id); return; }
          var action = act === 'modal-correct' ? 'correct' : (act === 'modal-approve' ? 'approve' : null);
          if (!action) return;
          postJson('/api/teacher-mgmt/verify/' + encodeURIComponent(item.id) + '/action', {
            action: action,
            comments: state.reviewComments,
            reviewer: reviewerName()
          }).then(function (res) {
            if (!res || res.success === false) { toast((res && res.message) || 'Operation failed', 'error'); return; }
            item.status = action === 'approve' ? 'approved' : (action === 'correct' ? 'needs_correction' : 'rejected');
            item.comments = state.reviewComments;
            closeModal();
            render();
            toast('Update request ' + action + ' processed');
          }).catch(function () { toast('Failed to process request', 'error'); });
        }
      });
    }

    function render(focusSearch) {
      var pending = countStatus('pending');
      var approved = countStatus('approved');
      var flagged = flaggedCount();
      var list = filtered();
      var items = pageItems(list);
      var departments = departmentOptions();
      var allSelected = list.length > 0 && list.every(function (i) { return state.selected[i.id]; });
      var h = [];

      h.push('<div class="ngis-sm" data-renderer="ngis-teacher-verify">');

      h.push('<div class="smx-kpi-grid">' +
        kpiHtml('Pending Verification', esc(String(pending)), 'Requires registrar review', 'pending_actions', pending > 0 ? 'warn' : '') +
        kpiHtml('Approved & Synced', esc(String(approved)), 'Staff ledger synchronized', 'sync_saved_locally', '') +
        kpiHtml('Total Submissions', esc(String(state.items.length)), 'Active academic term cycle', 'folder_open', '') +
        kpiHtml('Approval Turnaround', esc(turnaround()) + '<small> hrs</small>', 'Within 24h SLA target', 'avg_pace', '') +
      '</div>');

      h.push('<div class="smx-toolbar">' +
        '<div class="smx-search">' + icon('search') + '<input id="tmxSearch" class="smx-input" type="search" placeholder="Search teacher, ID, department, request ID or changed field..." value="' + esc(state.search) + '"></div>' +
        '<label class="smx-field"><span>Status</span><select id="tmxStatus" class="smx-select">' +
          option('all', 'All statuses (' + state.items.length + ')', state.status === 'all') +
          option('pending', 'Pending review (' + pending + ')', state.status === 'pending') +
          option('approved', 'Approved & synced (' + approved + ')', state.status === 'approved') +
          option('needs_correction', 'Needs clarification (' + flagged + ')', state.status === 'needs_correction') +
        '</select></label>' +
        '<label class="smx-field"><span>Department</span><select id="tmxDepartment" class="smx-select">' +
          departments.map(function (d) { return option(d, d === 'all' ? 'All departments' : d, state.department === d); }).join('') +
        '</select></label>' +
        '<label class="smx-field"><span>Changed field</span><select id="tmxField" class="smx-select">' +
          option('all', 'All changed fields', state.field === 'all') +
          option('phone', 'Contact & phone', state.field === 'phone') +
          option('qualification', 'Qualification', state.field === 'qualification') +
          option('certification', 'Certification', state.field === 'certification') +
          option('address', 'Residential address', state.field === 'address') +
          option('emergency', 'Emergency contact', state.field === 'emergency') +
        '</select></label>' +
        '<button type="button" class="smx-btn" data-act="reset">' + icon('filter_alt_off', 'sm') + 'Reset</button>' +
      '</div>');

      h.push('<div class="smx-tabs">' +
        tabHtml('All Submissions', state.items.length, 'all', state.tab === 'all') +
        tabHtml('Pending Review', pending, 'pending', state.tab === 'pending') +
        tabHtml('Approved & Ledger Synced', approved, 'approved', state.tab === 'approved') +
        tabHtml('Flagged Discrepancies', flagged, 'flagged', state.tab === 'flagged') +
      '</div>');

      h.push('<section class="smx-card smx-table-card">' +
        '<div class="smx-card-head"><div><div class="smx-card-title">' + icon('table_rows', 'sm') + 'Teacher Clearance Ledger</div>' +
          '<div class="smx-card-sub">' + list.length + ' matching request(s) &middot; ' + selectedIds().length + ' selected</div></div>' +
          '<div class="smx-card-actions">' +
            '<button type="button" class="smx-btn sm" data-act="export">' + icon('file_download', 'sm') + 'Export CSV</button>' +
            '<button type="button" class="smx-btn soft sm" data-act="bulk-approve">' + icon('done_all', 'sm') + 'Approve Selected</button>' +
          '</div></div>' +
        '<div class="smx-table-scroll"><table class="smx-table"><thead><tr>' +
          '<th class="center">' + selectAllHtml(allSelected) + '</th>' +
          '<th>Request ID</th><th>Teacher &amp; Department</th><th>Field Changed</th>' +
          '<th>Current vs Proposed Amendment</th><th>Status</th><th class="right">Actions</th>' +
        '</tr></thead><tbody>');

      if (!items.length) {
        h.push(emptyRow(7, 'No teacher profile update requests match the selected filters.'));
      } else {
        items.forEach(function (r) {
          var fieldIcon = r.fieldIcon || (
            String(r.fieldChanged || '').toLowerCase().indexOf('phone') !== -1 || String(r.fieldChanged || '').toLowerCase().indexOf('contact') !== -1 ? 'contact_phone' :
            String(r.fieldChanged || '').toLowerCase().indexOf('degree') !== -1 || String(r.fieldChanged || '').toLowerCase().indexOf('qualification') !== -1 ? 'school' :
            String(r.fieldChanged || '').toLowerCase().indexOf('cert') !== -1 || String(r.fieldChanged || '').toLowerCase().indexOf('first aid') !== -1 ? 'health_and_safety' :
            String(r.fieldChanged || '').toLowerCase().indexOf('address') !== -1 ? 'home_pin' : 'edit_note'
          );
          var fieldCat = r.fieldCategory || (
            String(r.fieldChanged || '').toLowerCase().indexOf('phone') !== -1 || String(r.fieldChanged || '').toLowerCase().indexOf('contact') !== -1 ? 'Faculty Contact Channel' :
            String(r.fieldChanged || '').toLowerCase().indexOf('degree') !== -1 || String(r.fieldChanged || '').toLowerCase().indexOf('qualification') !== -1 ? 'Academic Credentials & MoEYS Tier' :
            String(r.fieldChanged || '').toLowerCase().indexOf('cert') !== -1 || String(r.fieldChanged || '').toLowerCase().indexOf('first aid') !== -1 ? 'Compliance & Certification' :
            String(r.fieldChanged || '').toLowerCase().indexOf('address') !== -1 ? 'Faculty Primary Domicile' : 'Staff Profile Amendment'
          );
          h.push('<tr>' +
            '<td class="center">' + rowCheckbox(r.id, !!state.selected[r.id]) + '</td>' +
            '<td><div class="smx-mono">' + esc(r.id) + '</div><div class="smx-muted">' + esc(r.timeAgo || r.submittedDate) + '</div></td>' +
            '<td>' + personHtml(r.initials || initials(r.teacherName), r.teacherName, r.teacherId + ' · ' + (r.department || '')) + '</td>' +
            '<td><div class="smx-nowrap">' + icon(fieldIcon, 'sm') + ' ' + esc(r.fieldChanged) + '</div><div class="smx-muted">' + esc(fieldCat) + '</div></td>' +
            '<td><div class="smx-amend"><div class="smx-amend-old">' + esc(r.previousValue) + '</div>' +
              '<div class="smx-amend-new">' + icon('arrow_forward', 'sm') + esc(r.proposedValue) + '</div></div></td>' +
            '<td>' + statusLabel(r.status) + '</td>' +
            '<td class="right"><div class="smx-actions">' +
              '<button type="button" class="smx-btn sm" data-act="view" data-id="' + esc(r.id) + '">' + icon('visibility', 'sm') + 'Review</button>' +
              (r.status === 'pending' ? '<button type="button" class="smx-btn sm primary" data-act="approve" data-id="' + esc(r.id) + '">' + icon('check', 'sm') + 'Approve</button>' : '') +
              (r.status === 'pending' ? '<button type="button" class="smx-btn sm danger" data-act="reject" data-id="' + esc(r.id) + '">' + icon('block', 'sm') + 'Reject</button>' : '') +
            '</div></td>' +
          '</tr>');
        });
      }

      h.push('</tbody></table></div>' + pagerHtml(list.length, state.page, state.pageSize, 'requests') + '</section>');
      h.push('</div>');
      root.innerHTML = h.join('');

      if (focusSearch) {
        var input = document.getElementById('tmxSearch');
        if (input && input.focus) {
          input.focus();
          if (input.setSelectionRange) input.setSelectionRange(state.search.length, state.search.length);
        }
      }
    }

    function bind() {
      if (root._tmxVerifyBound) return;
      root._tmxVerifyBound = true;

      root.addEventListener('input', function (e) {
        if (e.target && e.target.id === 'tmxSearch') {
          state.search = e.target.value || '';
          state.page = 1;
          render(true);
        }
      });

      root.addEventListener('change', function (e) {
        var id = e.target && e.target.id;
        var value = e.target ? e.target.value : '';
        if (id === 'tmxStatus') { state.status = value; state.page = 1; render(); }
        else if (id === 'tmxDepartment') { state.department = value; state.page = 1; render(); }
        else if (id === 'tmxField') { state.field = value; state.page = 1; render(); }
        else if (id === 'tmxSelectAll') {
          var checked = !!e.target.checked;
          filtered().forEach(function (i) { state.selected[i.id] = checked; });
          render();
        } else if (e.target && e.target.getAttribute && e.target.getAttribute('data-act') === 'select') {
          var rowId = e.target.getAttribute('data-id');
          state.selected[rowId] = !!e.target.checked;
          render();
        }
      });

      root.addEventListener('click', function (e) {
        var tab = findAttr(e.target, 'data-tab');
        if (tab) { state.tab = tab; state.page = 1; render(); return; }
        var btn = findAct(e.target);
        if (!btn) return;
        var act = btn.getAttribute('data-act');
        var id = btn.getAttribute('data-id');
        if (act === 'export') exportCsv();
        else if (act === 'reset') {
          state.search = ''; state.status = 'all'; state.department = 'all'; state.field = 'all';
          state.tab = 'all'; state.page = 1; state.selected = {};
          render();
        } else if (act === 'page') { state.page = parseInt(btn.getAttribute('data-page'), 10) || 1; render(); }
        else if (act === 'bulk-approve') bulkApprove();
        else if (act === 'view') openReviewModal(id);
        else if (act === 'approve') approveItem(id);
        else if (act === 'reject') openRejectModal(id);
      });
    }
  };

  window.NGIS_TEACHER_VERIFY = TV;
  window.TEACHER_MGMT = window.TEACHER_MGMT || {};
  window.TEACHER_MGMT.initVerify = TV.init;
})(window, document);
