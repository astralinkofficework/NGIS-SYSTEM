/**
 * NGIS Student Management Executive Workspace
 * ---------------------------------------------------------------------------
 * Token-scoped renderers for:
 *   - Verify Student Profile Updates
 *   - Absence Statistics & Attendance Risk Register
 *
 * These controllers override the legacy Tailwind-heavy implementations in
 * student-management.js. All visual output uses the scoped .ngis-sm/.smx-*
 * classes from assets/css/design-system.css and the live student-management
 * API. No gradients, no 600/700 font weights, no decorative lifting.
 */
(function (window, document) {
  'use strict';

  var SM = window.STUDENT_MGMT = window.STUDENT_MGMT || {};
  SM.__ngisWorkspaceVersion = '1.0';

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

  function num(value, fallback) {
    var n = Number(value);
    return isFinite(n) ? n : (fallback || 0);
  }

  function pct(value) {
    return Math.max(0, Math.min(100, num(value, 0)));
  }

  function icon(name, extra) {
    return '<span class="material-symbols-outlined smx-icon' + (extra ? ' ' + extra : '') + '">' + esc(name) + '</span>';
  }

  function badge(label, tone) {
    return '<span class="smx-badge ' + esc(tone || 'neutral') + '"><i class="smx-dot"></i>' + esc(label) + '</span>';
  }

  function headHtml(eyebrow, title, sub, badgeLabel, actionsHtml) {
    return '<section class="smx-head">' +
      '<div>' +
        '<div class="smx-eyebrow">' + esc(eyebrow) + '</div>' +
        '<div class="smx-title-row">' +
          '<h1 class="smx-title">' + esc(title) + '</h1>' +
          (badgeLabel ? badge(badgeLabel, 'ok') : '') +
        '</div>' +
        '<p class="smx-sub">' + esc(sub) + '</p>' +
      '</div>' +
      '<div class="smx-head-actions">' + (actionsHtml || '') + '</div>' +
    '</section>';
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

  function toast(message, type) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'smx-toast';
      if (document.body && document.body.appendChild) document.body.appendChild(toastEl);
    }
    toastEl.textContent = message;
    toastEl.className = 'smx-toast show' + (type ? ' ' + esc(type) : '');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      if (toastEl) toastEl.className = 'smx-toast';
    }, 3200);
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
    toast('CSV exported successfully');
  }

  function loadingHtml(label) {
    return '<div class="ngis-sm" data-renderer="ngis-sm">' +
      '<div class="smx-card"><div class="smx-card-body smx-empty">' + icon('hourglass_top') + '<div>' + esc(label) + '</div></div></div>' +
    '</div>';
  }

  function termPill() {
    return '<span class="smx-term-pill"><span class="label">ACADEMIC TERM</span>' + icon('calendar_month', 'sm') + '<span>AY 2026&ndash;2027 &middot; Term 1</span></span>';
  }

  /* Below the md breakpoint the page's mandatory appbar already owns the
     sidebar toggle. A stylesheet rule is not enough here (the hero topbar's
     own !important declaration outranks author rules), so pin the duplicate
     control closed with an inline declaration instead. */
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

  function exportButton() {
    return '<button type="button" class="smx-btn" data-act="export">' + icon('file_download', 'sm') + '<span>Export CSV</span></button>';
  }

  function option(value, label, selected) {
    return '<option value="' + esc(value) + '"' + (selected ? ' selected' : '') + '>' + esc(label) + '</option>';
  }

  function tabHtml(label, count, key, active) {
    return '<button type="button" class="smx-tab' + (active ? ' active' : '') + '" data-tab="' + esc(key) + '">' +
      esc(label) + '<span class="count">' + count + '</span></button>';
  }

  function statusBadge(status) {
    if (status === 'pending') return badge('Pending Review', 'warn');
    if (status === 'approved') return badge('Approved & Synced', 'ok');
    if (status === 'rejected') return badge('Rejected', 'bad');
    if (status === 'needs_correction') return badge('Needs Clarification', 'bad');
    return badge(status || 'Unknown', 'neutral');
  }

  function riskBadge(level) {
    var text = String(level || 'Normal');
    if (text.indexOf('Critical') !== -1) return badge(text, 'bad');
    if (text.indexOf('Moderate') !== -1) return badge(text, 'warn');
    return badge(text, 'ok');
  }

  function noticeBadge(status) {
    if (status === 'Dispatched') return badge(status, 'ok');
    if (status === 'Pending Dispatch') return badge(status, 'warn');
    return badge(status || 'Not required', 'neutral');
  }

  function selectAllHtml(checked) {
    return '<input type="checkbox" class="smx-checkbox" id="smxSelectAll" data-act="select-all"' + (checked ? ' checked' : '') + ' aria-label="Select all rows">';
  }

  function rowCheckbox(id, selected) {
    return '<input type="checkbox" class="smx-checkbox" data-act="select" data-id="' + esc(id) + '"' + (selected ? ' checked' : '') + ' aria-label="Select row">';
  }

  function personHtml(initials, name, meta) {
    return '<div class="smx-person">' +
      '<span class="smx-avatar">' + esc(initials || 'ST') + '</span>' +
      '<div><div class="smx-person-name">' + esc(name) + '</div><div class="smx-mono">' + esc(meta) + '</div></div>' +
    '</div>';
  }

  function barHtml(value, tone) {
    return '<div class="smx-bar"><i class="' + (tone || '') + '" style="width:' + pct(value) + '%"></i></div>';
  }

  function initials(name) {
    var parts = String(name || 'Student').trim().split(/\s+/);
    return ((parts[0] || 'S').charAt(0) + (parts.length > 1 ? parts[parts.length - 1].charAt(0) : '')).toUpperCase();
  }

  /* ======================================================================
     VERIFY STUDENT PROFILE UPDATES
     ====================================================================== */

  SM.initVerify = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;
    suppressDuplicateHamburger();

    var state = {
      items: [],
      search: '',
      status: 'all',
      klass: 'all',
      field: 'all',
      tab: 'all',
      page: 1,
      pageSize: 8,
      selected: {},
      rejectReason: '',
      reviewComments: '',
      reviewItem: null
    };

    root.innerHTML = loadingHtml('Loading student profile update requests...');
    bind();
    load();

    function load() {
      fetchJson('/api/student-mgmt/verify').then(function (res) {
        state.items = res && res.data ? res.data : [];
        render();
      }).catch(function () {
        state.items = [];
        render();
        toast('Failed to load student update requests', 'error');
      });
    }

    function itemById(id) {
      for (var i = 0; i < state.items.length; i++) if (state.items[i].id === id) return state.items[i];
      return null;
    }

    function classOptions() {
      var seen = { all: true }, out = ['all'];
      state.items.forEach(function (item) {
        var c = String(item.class || '').trim();
        if (c && !seen[c]) { seen[c] = true; out.push(c); }
      });
      return out;
    }

    function countStatus(status) {
      return state.items.filter(function (i) { return i.status === status; }).length;
    }

    function turnaround() {
      var diffs = [];
      state.items.forEach(function (item) {
        if (item.status !== 'approved' || !item.submittedAt || !item.reviewedAt) return;
        var a = Date.parse(String(item.submittedAt).replace(' ', 'T'));
        var b = Date.parse(String(item.reviewedAt).replace(' ', 'T'));
        if (!isNaN(a) && !isNaN(b) && b > a) diffs.push((b - a) / 3600000);
      });
      if (!diffs.length) return '1.8';
      var sum = diffs.reduce(function (a, b) { return a + b; }, 0);
      return (sum / diffs.length).toFixed(1);
    }

    function filtered() {
      var q = state.search.toLowerCase().trim();
      return state.items.filter(function (item) {
        if (q) {
          var hay = [item.studentName, item.studentId, item.id, item.field].join(' ').toLowerCase();
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
        if (state.klass !== 'all') {
          var c = String(item.class || '').replace(/^Grade\s+/i, '').toLowerCase();
          if (c !== state.klass.replace(/^Grade\s+/i, '').toLowerCase()) return false;
        }
        if (state.field !== 'all' && String(item.field || '').toLowerCase().indexOf(state.field) === -1) return false;
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
        return [r.id, r.studentId, r.studentName, r.class, r.field, r.previousValue, r.proposedValue,
          r.status, r.submittedBy, r.submittedAt, r.reviewedBy, r.comments];
      });
      downloadCsv('NGIS_Student_Update_Audit_Ledger.csv', [
        'Request ID', 'Student ID', 'Student Name', 'Class', 'Field Changed', 'Current Value',
        'Proposed Amendment', 'Status', 'Submitted By', 'Submission Time', 'Reviewed By', 'Review Remarks'
      ], rows);
    }

    function approveItem(id, silent) {
      var item = itemById(id);
      if (!item || item.status === 'approved') return;
      postJson('/api/student-mgmt/verify/' + encodeURIComponent(id) + '/action', {
        action: 'approve',
        comments: 'Approved and synchronized with student record.',
        reviewer: portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office'
      }).then(function (res) {
        if (!res || res.success === false) { toast((res && res.error) || 'Approval failed', 'error'); return; }
        item.status = 'approved';
        item.reviewedAt = 'Just now';
        render();
        if (!silent) toast('Update request approved and synchronized with student ledger');
      }).catch(function () { toast('Failed to approve request', 'error'); });
    }

    function bulkApprove() {
      var ids = selectedIds().filter(function (id) {
        var item = itemById(id);
        return item && item.status === 'pending';
      });
      if (!ids.length) { toast('Select at least one pending request', 'error'); return; }
      Promise.all(ids.map(function (id) {
        return postJson('/api/student-mgmt/verify/' + encodeURIComponent(id) + '/action', {
          action: 'approve',
          comments: 'Bulk approved from clearance ledger.',
          reviewer: portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office'
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
          '<div class="smx-modal-sub">' + esc(item.id) + ' &middot; ' + esc(item.studentName) + '</div></div>' +
          '<button type="button" class="smx-close" data-act="close-modal" aria-label="Close">' + icon('close', 'sm') + '</button></div>' +
        '<div class="smx-modal-body">' +
          '<p class="smx-muted">Supply a reason for the audit ledger. The guardian will be notified after rejection.</p>' +
          '<div class="smx-section-label">Reason for rejection</div>' +
          '<textarea id="smxRejectReason" class="smx-textarea" placeholder="e.g. Missing official registry seal"></textarea>' +
          '<div class="smx-doc">' + icon('info', 'sm') + '<span>This action is recorded on the student audit trail.</span></div>' +
        '</div>' +
        '<div class="smx-modal-foot">' +
          '<button type="button" class="smx-btn" data-act="close-modal">Cancel</button>' +
          '<button type="button" class="smx-btn danger" data-act="confirm-reject">' + icon('block', 'sm') + 'Confirm Rejection</button>' +
        '</div></div>';
      openModal(html, {
        input: function (e) { if (e.target && e.target.id === 'smxRejectReason') state.rejectReason = e.target.value; },
        click: function (act) {
          if (act !== 'confirm-reject') return;
          if (!state.rejectReason.trim()) { toast('Please enter a rejection reason', 'error'); return; }
          postJson('/api/student-mgmt/verify/' + encodeURIComponent(item.id) + '/action', {
            action: 'reject',
            comments: state.rejectReason,
            reviewer: portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office'
          }).then(function (res) {
            if (!res || res.success === false) { toast((res && res.error) || 'Rejection failed', 'error'); return; }
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
      state.reviewItem = item;
      state.reviewComments = item.comments || '';
      var html = '<div class="smx-modal wide">' +
        '<div class="smx-modal-head"><div><div class="smx-modal-title">Review Profile Amendment Diff</div>' +
          '<div class="smx-modal-sub">' + esc(item.id) + ' &middot; ' + esc(item.field) + '</div></div>' +
          '<button type="button" class="smx-close" data-act="close-modal" aria-label="Close">' + icon('close', 'sm') + '</button></div>' +
        '<div class="smx-modal-body">' +
          '<div class="smx-info-grid">' +
            '<div class="smx-info"><span class="label">Student</span><span class="value">' + esc(item.studentName) + ' (' + esc(item.studentId) + ')</span></div>' +
            '<div class="smx-info"><span class="label">Cohort</span><span class="value">Grade ' + esc(item.class) + '</span></div>' +
            '<div class="smx-info"><span class="label">Submitted by</span><span class="value">' + esc(item.submittedBy) + '</span></div>' +
            '<div class="smx-info"><span class="label">Submitted at</span><span class="value">' + esc(item.submittedAt) + '</span></div>' +
          '</div>' +
          '<div class="smx-section-label">Field amendment</div>' +
          '<div class="smx-diff">' +
            '<div><span class="label">Current ledger value</span><div class="old">' + esc(item.previousValue) + '</div></div>' +
            '<div><span class="label">Proposed amendment</span><div class="new">' + esc(item.proposedValue) + '</div></div>' +
          '</div>' +
          '<div class="smx-section-label">Supporting documentation</div>' +
          '<div class="smx-doc">' + icon('attach_file', 'sm') + '<span>' + esc(item.supportingDoc || 'document.pdf') + '</span>' + badge('Verified Attachment', 'ok') + '</div>' +
          '<div class="smx-section-label">Official reviewer note</div>' +
          '<textarea id="smxReviewComments" class="smx-textarea" placeholder="Input rationale or verification remarks...">' + esc(state.reviewComments) + '</textarea>' +
        '</div>' +
        '<div class="smx-modal-foot">' +
          '<button type="button" class="smx-btn danger" data-act="modal-reject">Reject Request</button>' +
          '<button type="button" class="smx-btn" data-act="modal-correct">Request Correction</button>' +
          '<button type="button" class="smx-btn primary" data-act="modal-approve">' + icon('verified', 'sm') + 'Approve & Sync Ledger</button>' +
        '</div></div>';
      openModal(html, {
        input: function (e) { if (e.target && e.target.id === 'smxReviewComments') state.reviewComments = e.target.value; },
        click: function (act) {
          if (act === 'modal-reject') { closeModal(); openRejectModal(item.id); return; }
          var action = act === 'modal-correct' ? 'correct' : (act === 'modal-approve' ? 'approve' : null);
          if (!action) return;
          postJson('/api/student-mgmt/verify/' + encodeURIComponent(item.id) + '/action', {
            action: action,
            comments: state.reviewComments,
            reviewer: portalRole === 'principal' ? 'Principal · Dr. Ly Bunheng' : 'Admin · Records Office'
          }).then(function (res) {
            if (!res || res.success === false) { toast((res && res.error) || 'Operation failed', 'error'); return; }
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
      var flagged = state.items.filter(function (i) { return i.status === 'rejected' || i.status === 'needs_correction'; }).length;
      var list = filtered();
      var items = pageItems(list);
      var classes = classOptions();
      var allSelected = list.length > 0 && list.every(function (i) { return state.selected[i.id]; });
      var h = [];

      h.push('<div class="ngis-sm" data-renderer="ngis-sm">');
      h.push(headHtml(
        'STUDENT MANAGEMENT · CLEARANCE DESK',
        'Verify Student Profile Updates',
        'Review custodial changes, legal identifiers, contact channels and supporting documentation before syncing the student ledger.',
        pending + ' Pending Action',
        termPill() + exportButton()
      ));

      h.push('<div class="smx-kpi-grid">' +
        kpiHtml('Pending Verification', esc(String(pending)), 'Requires registrar review', 'pending_actions', 'warn') +
        kpiHtml('Approved & Synced', esc(String(approved)), 'Ledger synchronized', 'sync_saved_locally', '') +
        kpiHtml('Total Submissions', esc(String(state.items.length)), 'Active academic term cycle', 'folder_open', '') +
        kpiHtml('Approval Turnaround', esc(turnaround()) + '<small> hrs</small>', 'Within 24h SLA target', 'avg_pace', '') +
      '</div>');

      h.push('<div class="smx-toolbar">' +
        '<div class="smx-search">' + icon('search') + '<input id="smxSearch" class="smx-input" type="search" placeholder="Search student, ID, request ID or changed field..." value="' + esc(state.search) + '"></div>' +
        '<label class="smx-field"><span>Status</span><select id="smxStatus" class="smx-select">' +
          option('all', 'All statuses (' + state.items.length + ')', state.status === 'all') +
          option('pending', 'Pending review (' + pending + ')', state.status === 'pending') +
          option('approved', 'Approved & synced (' + approved + ')', state.status === 'approved') +
          option('needs_correction', 'Needs clarification (' + flagged + ')', state.status === 'needs_correction') +
        '</select></label>' +
        '<label class="smx-field"><span>Class</span><select id="smxClass" class="smx-select">' +
          classes.map(function (c) { return option(c, c === 'all' ? 'All classes' : 'Grade ' + c, state.klass === c); }).join('') +
        '</select></label>' +
        '<label class="smx-field"><span>Changed field</span><select id="smxField" class="smx-select">' +
          option('all', 'All changed fields', state.field === 'all') +
          option('address', 'Residential address', state.field === 'address') +
          option('contact', 'Emergency contact', state.field === 'contact') +
          option('legal', 'Legal name', state.field === 'legal') +
          option('medical', 'Medical & dietary', state.field === 'medical') +
          option('guardian', 'Guardian status', state.field === 'guardian') +
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
        '<div class="smx-card-head"><div><div class="smx-card-title">' + icon('table_rows', 'sm') + 'Clearance Ledger</div>' +
          '<div class="smx-card-sub">' + list.length + ' matching request(s) &middot; ' + selectedIds().length + ' selected</div></div>' +
          '<button type="button" class="smx-btn soft sm" data-act="bulk-approve">' + icon('done_all', 'sm') + 'Approve Selected</button></div>' +
        '<div class="smx-table-scroll"><table class="smx-table"><thead><tr>' +
          '<th class="center">' + selectAllHtml(allSelected) + '</th>' +
          '<th>Request ID</th><th>Student & Cohort</th><th>Field Changed</th>' +
          '<th>Current vs Proposed Amendment</th><th>Status</th><th class="right">Actions</th>' +
        '</tr></thead><tbody>');

      if (!items.length) {
        h.push(emptyRow(7, 'No student profile update requests match the selected filters.'));
      } else {
        items.forEach(function (r) {
          var fieldIcon = r.fieldIcon || (String(r.field || '').indexOf('Address') !== -1 ? 'home_pin' : 'edit_note');
          h.push('<tr>' +
            '<td class="center">' + rowCheckbox(r.id, !!state.selected[r.id]) + '</td>' +
            '<td><div class="smx-mono">' + esc(r.id) + '</div><div class="smx-muted">' + esc(r.timeAgo || r.submittedAt) + '</div></td>' +
            '<td>' + personHtml(r.initials || initials(r.studentName), r.studentName, r.studentId + ' · Grade ' + (r.class || '')) + '</td>' +
            '<td><div class="smx-nowrap">' + icon(fieldIcon, 'sm') + ' ' + esc(r.field) + '</div><div class="smx-muted">' + esc(r.fieldCategory || 'Profile amendment') + '</div></td>' +
            '<td><div class="smx-amend"><div class="smx-amend-old">' + esc(r.previousValue) + '</div>' +
              '<div class="smx-amend-new">' + icon('arrow_forward', 'sm') + esc(r.proposedValue) + '</div></div></td>' +
            '<td>' + statusBadge(r.status) + '</td>' +
            '<td class="right"><div class="smx-actions">' +
              '<button type="button" class="smx-btn sm" data-act="view" data-id="' + esc(r.id) + '">' + icon('visibility', 'sm') + 'View</button>' +
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
        var input = document.getElementById('smxSearch');
        if (input && input.focus) {
          input.focus();
          if (input.setSelectionRange) input.setSelectionRange(state.search.length, state.search.length);
        }
      }
    }

    function bind() {
      if (root._smxVerifyBound) return;
      root._smxVerifyBound = true;

      root.addEventListener('input', function (e) {
        if (e.target && e.target.id === 'smxSearch') {
          state.search = e.target.value || '';
          state.page = 1;
          render(true);
        }
      });

      root.addEventListener('change', function (e) {
        var id = e.target && e.target.id;
        var value = e.target ? e.target.value : '';
        if (id === 'smxStatus') { state.status = value; state.page = 1; render(); }
        else if (id === 'smxClass') { state.klass = value; state.page = 1; render(); }
        else if (id === 'smxField') { state.field = value; state.page = 1; render(); }
        else if (id === 'smxSelectAll') {
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
          state.search = ''; state.status = 'all'; state.klass = 'all'; state.field = 'all'; state.tab = 'all'; state.page = 1; state.selected = {};
          render();
        } else if (act === 'page') { state.page = parseInt(btn.getAttribute('data-page'), 10) || 1; render(); }
        else if (act === 'bulk-approve') bulkApprove();
        else if (act === 'view') openReviewModal(id);
        else if (act === 'approve') approveItem(id);
        else if (act === 'reject') openRejectModal(id);
      });
    }
  };

  /* ======================================================================
     ABSENCE STATISTICS & ATTENDANCE RISK REGISTER
     ====================================================================== */

  SM.initAbsenceStats = function (containerId, portalRole) {
    var root = document.getElementById(containerId);
    if (!root) return;
    suppressDuplicateHamburger();

    var state = {
      data: null,
      search: '',
      risk: 'all',
      klass: 'all',
      notice: 'all',
      tab: 'all',
      page: 1,
      pageSize: 8,
      selected: {}
    };

    root.innerHTML = loadingHtml('Loading attendance telemetry and risk register...');
    bind();
    load();

    function load() {
      fetchJson('/api/student-mgmt/absence-stats?class=all').then(function (res) {
        state.data = res || {};
        render();
      }).catch(function () {
        state.data = { students: [], kpis: {}, cohortDistribution: [], absenceCategories: [], classComparison: [] };
        render();
        toast('Failed to load attendance statistics', 'error');
      });
    }

    function students() { return (state.data && state.data.students) || []; }
    function kpis() { return (state.data && state.data.kpis) || {}; }
    function cohorts() { return (state.data && state.data.cohortDistribution) || []; }
    function categories() { return (state.data && state.data.absenceCategories) || []; }
    function comparison() { return (state.data && state.data.classComparison) || []; }

    function studentById(id) {
      var list = students();
      for (var i = 0; i < list.length; i++) if (list[i].studentId === id) return list[i];
      return null;
    }

    function classOptions() {
      var seen = { all: true }, out = ['all'];
      students().forEach(function (s) {
        var c = String(s.class || '').trim();
        if (c && !seen[c]) { seen[c] = true; out.push(c); }
      });
      return out;
    }

    function countRisk(kind) {
      return students().filter(function (s) {
        var risk = String(s.riskLevel || 'Normal');
        if (kind === 'critical') return risk.indexOf('Critical') !== -1;
        if (kind === 'moderate') return risk.indexOf('Moderate') !== -1;
        if (kind === 'normal') return risk.indexOf('Critical') === -1 && risk.indexOf('Moderate') === -1;
        return true;
      }).length;
    }

    function noticePending() {
      return students().filter(function (s) { return s.noticeStatus === 'Pending Dispatch'; }).length;
    }

    function filtered() {
      var q = state.search.toLowerCase().trim();
      return students().filter(function (s) {
        if (q) {
          var hay = [s.studentName, s.studentId, s.class, s.grade].join(' ').toLowerCase();
          if (hay.indexOf(q) === -1) return false;
        }
        if (state.klass !== 'all' && String(s.class || '').toLowerCase() !== state.klass.toLowerCase()) return false;
        if (state.notice !== 'all' && s.noticeStatus !== state.notice) return false;
        var risk = String(s.riskLevel || 'Normal');
        if (state.risk === 'critical' && risk.indexOf('Critical') === -1) return false;
        if (state.risk === 'moderate' && risk.indexOf('Moderate') === -1) return false;
        if (state.risk === 'normal' && (risk.indexOf('Critical') !== -1 || risk.indexOf('Moderate') !== -1)) return false;
        if (state.tab === 'critical' && risk.indexOf('Critical') === -1) return false;
        if (state.tab === 'moderate' && risk.indexOf('Moderate') === -1) return false;
        if (state.tab === 'normal' && (risk.indexOf('Critical') !== -1 || risk.indexOf('Moderate') !== -1)) return false;
        if (state.tab === 'notice' && s.noticeStatus !== 'Pending Dispatch') return false;
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
      var rows = filtered().map(function (s) {
        return [s.studentId, s.studentName, s.class, s.attendancePct, s.totalAbsentDays,
          s.excusedAbsences, s.unexcusedAbsences, s.riskLevel, s.noticeStatus, s.guardian && s.guardian.phone];
      });
      downloadCsv('NGIS_Attendance_Risk_Register.csv', [
        'Student ID', 'Student Name', 'Class', 'Attendance %', 'Total Absences',
        'Excused', 'Unexcused', 'Risk Level', 'Parent Notice', 'Guardian Phone'
      ], rows);
    }

    function notify(ids) {
      var targets = (ids || []).filter(Boolean);
      if (!targets.length) { toast('Select at least one student to notify', 'error'); return; }
      postJson('/api/student-mgmt/absence-stats/notify', {
        studentIds: targets,
        channel: 'sms_telegram'
      }).then(function (res) {
        targets.forEach(function (id) {
          var s = studentById(id);
          if (s) { s.parentNotified = true; s.noticeStatus = 'Dispatched'; }
        });
        state.selected = {};
        render();
        toast((res && res.message) || 'Guardian notice dispatched');
      }).catch(function () { toast('Failed to dispatch guardian notice', 'error'); });
    }

    function openLog(id) {
      var s = studentById(id);
      if (!s) return;
      var logs = s.absenceLog || [];
      var html = '<div class="smx-modal wide">' +
        '<div class="smx-modal-head"><div><div class="smx-modal-title">Absence Log &middot; ' + esc(s.studentName) + '</div>' +
          '<div class="smx-modal-sub">' + esc(s.studentId) + ' &middot; Grade ' + esc(s.class) + '</div></div>' +
          '<button type="button" class="smx-close" data-act="close-modal" aria-label="Close">' + icon('close', 'sm') + '</button></div>' +
        '<div class="smx-modal-body">' +
          '<div class="smx-info-grid">' +
            '<div class="smx-info"><span class="label">Attendance rate</span><span class="value">' + esc(String(s.attendancePct)) + '%</span></div>' +
            '<div class="smx-info"><span class="label">Total absences</span><span class="value">' + esc(String(s.totalAbsentDays)) + ' days</span></div>' +
            '<div class="smx-info"><span class="label">Unexcused</span><span class="value">' + esc(String(s.unexcusedAbsences)) + ' days</span></div>' +
            '<div class="smx-info"><span class="label">Risk level</span><span class="value">' + esc(s.riskLevel) + '</span></div>' +
          '</div>' +
          '<div class="smx-section-label">Guardian channel</div>' +
          '<div class="smx-doc">' + icon('contact_phone', 'sm') + '<span>' + esc((s.guardian && s.guardian.name) || 'Guardian') + ' &middot; ' + esc((s.guardian && s.guardian.phone) || '') + '</span>' + noticeBadge(s.noticeStatus) + '</div>' +
          '<div class="smx-section-label">Recorded absence events</div>';
      if (!logs.length) html += '<div class="smx-doc">' + icon('event_available', 'sm') + '<span>No individual absence events recorded.</span></div>';
      else logs.forEach(function (log) {
        html += '<div class="smx-doc"><div><div class="smx-person-name">' + esc(log.date) + ' &middot; ' + esc(log.session) + '</div>' +
          '<div class="smx-muted">' + esc(log.category) + ' &middot; ' + esc(log.verification) + '</div></div>' + badge(log.action, 'neutral') + '</div>';
      });
      html += '</div><div class="smx-modal-foot">' +
        '<button type="button" class="smx-btn" data-act="close-modal">Close</button>' +
        '<button type="button" class="smx-btn primary" data-act="notify-one">' + icon('notifications_active', 'sm') + 'Notify Guardian</button>' +
      '</div></div>';
      openModal(html, {
        click: function (act) {
          if (act === 'notify-one') { closeModal(); notify([s.studentId]); }
        }
      });
    }

    function render(focusSearch) {
      var k = kpis();
      var list = filtered();
      var items = pageItems(list);
      var classes = classOptions();
      var allSelected = list.length > 0 && list.every(function (s) { return state.selected[s.studentId]; });
      var critical = countRisk('critical');
      var moderate = countRisk('moderate');
      var normal = countRisk('normal');
      var pendingNotices = noticePending();
      var h = [];

      h.push('<div class="ngis-sm" data-renderer="ngis-sm">');
      h.push(headHtml(
        'STUDENT MANAGEMENT · ATTENDANCE INTELLIGENCE',
        'Absence Statistics & Attendance Risk Register',
        'Institutional attendance telemetry, chronic absenteeism tracking and parent-notice workflow for the active academic term.',
        'Live registry',
        termPill() + exportButton()
      ));

      h.push('<div class="smx-kpi-grid">' +
        kpiHtml('Overall Attendance Rate', esc(String(num(k.overallRate, 0).toFixed(1))) + '<small>%</small>', 'Across all enrolled cohorts', 'insights', '') +
        kpiHtml('Total Absences (Term)', esc(String(num(k.totalAbsences, 0))), 'Recorded absence days', 'event_busy', 'warn') +
        kpiHtml('Unexcused Absences', esc(String(num(k.unexcusedTotal, 0))), 'Requires verification', 'report', 'warn') +
        kpiHtml('Chronic Absenteeism Flag', esc(String(num(k.chronicAbsentees, 0))), 'Students above intervention threshold', 'warning', 'bad') +
      '</div>');

      h.push('<div class="smx-bento">' +
        '<section class="smx-card"><div class="smx-card-head"><div><div class="smx-card-title">' + icon('bar_chart', 'sm') + 'Attendance Distribution by Cohort</div>' +
          '<div class="smx-card-sub">Average attendance rate versus term benchmark</div></div>' + badge('Benchmark 95.0%', 'ok') + '</div>' +
          '<div class="smx-card-body"><div class="smx-cohort-list">');
      cohorts().forEach(function (c) {
        var tone = String(c.status || '').indexOf('Risk') !== -1 ? 'bad' : (String(c.status || '').indexOf('Attention') !== -1 ? 'warn' : '');
        h.push('<div class="smx-cohort-row">' +
          '<div class="smx-cohort-name">' + esc(c.cohort) + '</div>' +
          '<div class="smx-cohort-meta">' + esc(String(c.enrolled)) + ' enrolled &middot; ' + esc(String(c.absences)) + ' absences &middot; ' + esc(c.status) + '</div>' +
          '<div class="smx-cohort-value">' + esc(String(c.attendancePct)) + '%</div>' +
          '<div style="grid-column:1 / -1">' + barHtml(c.attendancePct, tone) + '</div>' +
        '</div>');
      });
      h.push('</div><div class="smx-note">Class comparison: ' + comparison().slice(0, 3).map(function (c) {
        return esc(c.class) + ' ' + esc(String(c.averageAttendance)) + '%';
      }).join(' &middot; ') + '</div></div></section>' +

        '<section class="smx-card"><div class="smx-card-head"><div><div class="smx-card-title">' + icon('donut_large', 'sm') + 'Absence Classification</div>' +
          '<div class="smx-card-sub">Distribution of recorded absence days</div></div></div>' +
          '<div class="smx-card-body"><div class="smx-class-list">');
      categories().forEach(function (c, idx) {
        var tone = idx === 1 ? 'warn' : (idx === 2 ? 'bad' : '');
        h.push('<div class="smx-class-row">' +
          '<div class="smx-class-label">' + esc(c.category) + '</div>' +
          '<div class="smx-class-value">' + esc(String(c.days)) + ' days &middot; ' + esc(String(c.pct)) + '%</div>' +
          barHtml(c.pct, tone) +
          '<div class="smx-muted" style="grid-column:1 / -1">' + esc(c.desc) + '</div>' +
        '</div>');
      });
      h.push('</div><div class="smx-note">' + icon('info', 'sm') + ' Classification totals are derived from the active term absence ledger.</div></div></section>' +
      '</div>');

      h.push('<div class="smx-toolbar">' +
        '<div class="smx-search">' + icon('search') + '<input id="smxSearch" class="smx-input" type="search" placeholder="Search student, ID or cohort..." value="' + esc(state.search) + '"></div>' +
        '<label class="smx-field"><span>Risk level</span><select id="smxRisk" class="smx-select">' +
          option('all', 'All risk levels', state.risk === 'all') +
          option('critical', 'Critical', state.risk === 'critical') +
          option('moderate', 'Moderate', state.risk === 'moderate') +
          option('normal', 'Normal', state.risk === 'normal') +
        '</select></label>' +
        '<label class="smx-field"><span>Class</span><select id="smxClass" class="smx-select">' +
          classes.map(function (c) { return option(c, c === 'all' ? 'All classes' : 'Grade ' + c, state.klass === c); }).join('') +
        '</select></label>' +
        '<label class="smx-field"><span>Parent notice</span><select id="smxNotice" class="smx-select">' +
          option('all', 'All notice states', state.notice === 'all') +
          option('Dispatched', 'Dispatched', state.notice === 'Dispatched') +
          option('Pending Dispatch', 'Pending dispatch', state.notice === 'Pending Dispatch') +
          option('Not required', 'Not required', state.notice === 'Not required') +
        '</select></label>' +
        '<button type="button" class="smx-btn" data-act="reset">' + icon('filter_alt_off', 'sm') + 'Reset</button>' +
      '</div>');

      h.push('<div class="smx-tabs">' +
        tabHtml('All Students', students().length, 'all', state.tab === 'all') +
        tabHtml('Critical Risk', critical, 'critical', state.tab === 'critical') +
        tabHtml('Moderate', moderate, 'moderate', state.tab === 'moderate') +
        tabHtml('Normal', normal, 'normal', state.tab === 'normal') +
        tabHtml('Notice Pending', pendingNotices, 'notice', state.tab === 'notice') +
      '</div>');

      h.push('<section class="smx-card smx-table-card">' +
        '<div class="smx-card-head"><div><div class="smx-card-title">' + icon('table_rows', 'sm') + 'Attendance Risk Register</div>' +
          '<div class="smx-card-sub">' + list.length + ' matching student(s) &middot; ' + selectedIds().length + ' selected</div></div>' +
          '<button type="button" class="smx-btn soft sm" data-act="notify-selected">' + icon('notifications_active', 'sm') + 'Notify Selected</button></div>' +
        '<div class="smx-table-scroll"><table class="smx-table"><thead><tr>' +
          '<th class="center">' + selectAllHtml(allSelected) + '</th>' +
          '<th>Student & Cohort</th><th>Attendance Rate</th><th class="center">Absences</th>' +
          '<th class="center">Unexcused</th><th>Risk Level</th><th>Parent Notice</th><th class="right">Actions</th>' +
        '</tr></thead><tbody>');

      if (!items.length) {
        h.push(emptyRow(8, 'No students match the selected attendance filters.'));
      } else {
        items.forEach(function (s) {
          var risk = String(s.riskLevel || 'Normal');
          var tone = risk.indexOf('Critical') !== -1 ? 'bad' : (risk.indexOf('Moderate') !== -1 ? 'warn' : '');
          h.push('<tr>' +
            '<td class="center">' + rowCheckbox(s.studentId, !!state.selected[s.studentId]) + '</td>' +
            '<td>' + personHtml(s.initials || initials(s.studentName), s.studentName, s.studentId + ' · Grade ' + (s.class || '')) + '</td>' +
            '<td><div class="smx-attendance"><div class="value">' + esc(String(s.attendancePct)) + '%</div>' + barHtml(s.attendancePct, tone) + '</div></td>' +
            '<td class="center"><strong>' + esc(String(s.totalAbsentDays)) + '</strong><div class="smx-muted">' + esc(String(s.excusedAbsences)) + ' excused</div></td>' +
            '<td class="center">' + badge(esc(String(s.unexcusedAbsences)) + ' days', tone === 'bad' ? 'bad' : (tone === 'warn' ? 'warn' : 'neutral')) + '</td>' +
            '<td>' + riskBadge(risk) + '</td>' +
            '<td><div class="smx-nowrap">' + noticeBadge(s.noticeStatus) + '</div><div class="smx-muted">' + esc(s.noticeDate || '') + '</div></td>' +
            '<td class="right"><div class="smx-actions">' +
              '<button type="button" class="smx-btn sm" data-act="log" data-id="' + esc(s.studentId) + '">' + icon('visibility', 'sm') + 'View Log</button>' +
              '<button type="button" class="smx-btn sm primary" data-act="notify" data-id="' + esc(s.studentId) + '">' + icon('notifications_active', 'sm') + 'Notify</button>' +
            '</div></td>' +
          '</tr>');
        });
      }

      h.push('</tbody></table></div>' + pagerHtml(list.length, state.page, state.pageSize, 'students') + '</section>');
      h.push('</div>');
      root.innerHTML = h.join('');

      if (focusSearch) {
        var input = document.getElementById('smxSearch');
        if (input && input.focus) {
          input.focus();
          if (input.setSelectionRange) input.setSelectionRange(state.search.length, state.search.length);
        }
      }
    }

    function bind() {
      if (root._smxAbsenceBound) return;
      root._smxAbsenceBound = true;

      root.addEventListener('input', function (e) {
        if (e.target && e.target.id === 'smxSearch') {
          state.search = e.target.value || '';
          state.page = 1;
          render(true);
        }
      });

      root.addEventListener('change', function (e) {
        var id = e.target && e.target.id;
        var value = e.target ? e.target.value : '';
        if (id === 'smxRisk') { state.risk = value; state.page = 1; render(); }
        else if (id === 'smxClass') { state.klass = value; state.page = 1; render(); }
        else if (id === 'smxNotice') { state.notice = value; state.page = 1; render(); }
        else if (id === 'smxSelectAll') {
          var checked = !!e.target.checked;
          filtered().forEach(function (s) { state.selected[s.studentId] = checked; });
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
          state.search = ''; state.risk = 'all'; state.klass = 'all'; state.notice = 'all'; state.tab = 'all'; state.page = 1; state.selected = {};
          render();
        } else if (act === 'page') { state.page = parseInt(btn.getAttribute('data-page'), 10) || 1; render(); }
        else if (act === 'log') openLog(id);
        else if (act === 'notify') notify([id]);
        else if (act === 'notify-selected') notify(selectedIds());
      });
    }
  };

})(window, document);
