/* ============================================================================
 * NGIS User Management — role-scoped identity administration & provisioning.
 * Drives the five Account Directories via NGIS_USERS.init(containerId, module):
 *   students | teachers | staff | principals | admins
 *
 * Design: token-scoped .ngis-sm / .smx-* classes (see assets/css/design-system.css).
 *         Zero font-weight >= 600, zero CSS gradients, inline SVGs with viewBox.
 * Data:   live /api/user-mgmt/* endpoints with race-safe search, server pagination,
 *         live username checks, role-specific Add Account modal, and contextual
 *         row actions with confirmation dialogs.
 * ==========================================================================*/
(function (window, document) {
  'use strict';

  var UM = window.NGIS_USERS = {};
  UM.version = '1.0';

  var ROLES_BY_TYPE = {
    student: 'STUDENT',
    teacher: 'TEACHER',
    staff: 'STAFF',
    principal: 'PRINCIPAL',
    admin: 'ADMIN'
  };

  var ADMIN_SCOPES = [
    'All Departments & Operations',
    'Identity & User Access',
    'Academic Operations',
    'Campus & Facility Admin',
    'Finance & Registrar'
  ];

  var MODULES = {
    students: {
      module: 'students',
      type: 'student',
      eyebrow: 'ACCOUNT DIRECTORIES · STUDENT ACCOUNTS',
      title: 'Student Accounts',
      sub: 'Manage student login credentials linked to enrolled academic profiles.',
      addLabel: 'Add Student Account',
      portalNote: 'Grants read access to Student Portal, timetable, homework, and grades.',
      recordNoun: 'student',
      recordPlural: 'students',
      hasBulk: true,
      hasImport: true,
      showLastLogin: true,
      extraFilter: 'class',
      extraFilterLabel: 'Class',
      fallbackUrl: 'admin-student-profiles.html',
      fallbackLabel: 'Open Student Profiles',
      searchPlaceholder: 'Search student name, ID, or username...',
      columns: ['Student', 'Username', 'Campus', 'Class', 'Account Status', 'Last Login', 'Actions']
    },
    teachers: {
      module: 'teachers',
      type: 'teacher',
      eyebrow: 'ACCOUNT DIRECTORIES · TEACHER ACCOUNTS',
      title: 'Teacher Accounts',
      sub: 'Provision and govern faculty portal logins linked to teaching assignments.',
      addLabel: 'Add Teacher Account',
      portalNote: 'Grants access to Teacher Portal, class rosters, attendance, and gradebook.',
      recordNoun: 'teacher',
      recordPlural: 'teachers',
      hasBulk: true,
      hasImport: true,
      showLastLogin: true,
      extraFilter: 'department',
      extraFilterLabel: 'Department',
      fallbackUrl: 'admin-teacher-profiles.html',
      fallbackLabel: 'Open Teacher Profiles',
      searchPlaceholder: 'Search teacher name, ID, or department...',
      columns: ['Teacher', 'Username', 'Campus', 'Department', 'Account Status', 'Last Login', 'Actions']
    },
    staff: {
      module: 'staff',
      type: 'staff',
      eyebrow: 'ACCOUNT DIRECTORIES · STAFF ACCOUNTS',
      title: 'Staff Accounts',
      sub: 'Manage operational non-teaching staff logins scoped to their department.',
      addLabel: 'Add Staff Account',
      portalNote: 'Grants scoped operational access without academic classroom editing privileges.',
      recordNoun: 'staff member',
      recordPlural: 'staff records',
      hasBulk: false,
      hasImport: true,
      showLastLogin: false,
      extraFilter: 'department',
      extraFilterLabel: 'Department',
      fallbackUrl: '',
      fallbackLabel: '',
      searchPlaceholder: 'Search staff name, ID, or position...',
      columns: ['Staff Member', 'Username', 'Department', 'Position', 'Account Status', 'Actions']
    },
    principals: {
      module: 'principals',
      type: 'principal',
      eyebrow: 'ACCOUNT DIRECTORIES · PRINCIPAL ACCOUNTS',
      title: 'Principal Accounts',
      sub: 'Manage campus leadership accounts with academic oversight across assigned campuses.',
      addLabel: 'Add Principal Account',
      portalNote: 'Grants access to Principal Portal for campus academics and timetable oversight.',
      recordNoun: 'principal',
      recordPlural: 'principal records',
      hasBulk: false,
      hasImport: false,
      showLastLogin: true,
      extraFilter: null,
      extraFilterLabel: '',
      fallbackUrl: '',
      fallbackLabel: '',
      searchPlaceholder: 'Search principal name, ID, or campus...',
      columns: ['Principal', 'Username', 'Assigned Campus', 'Account Status', 'Last Login', 'Actions']
    },
    admins: {
      module: 'admins',
      type: 'admin',
      eyebrow: 'ACCOUNT DIRECTORIES · ADMIN ACCOUNTS',
      title: 'Admin Accounts',
      sub: 'Govern privileged administrator accounts under Super Admin authorization.',
      addLabel: 'Add Admin Account',
      portalNote: 'Grants Administrative Portal privileges. Super Admin roles cannot be assigned here.',
      recordNoun: 'administrator',
      recordPlural: 'administrators',
      hasBulk: false,
      hasImport: false,
      showLastLogin: false,
      extraFilter: null,
      extraFilterLabel: '',
      fallbackUrl: '',
      fallbackLabel: '',
      searchPlaceholder: 'Search administrator name, username, or scope...',
      columns: ['Administrator', 'Username', 'Campus', 'Access Scope', 'Account Status', 'Actions']
    }
  };

  var STATUS_LABEL = {
    pending_activation: 'Pending Activation',
    active: 'Active',
    suspended: 'Suspended',
    disabled: 'Disabled',
    locked: 'Locked',
    none: 'No Account'
  };

  var ICONS = {
    plus:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
    upload:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>',
    download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>',
    filter:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><path d="M3 5h18M6 12h12M10 19h4"/></svg>',
    search:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
    reset:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
    more:     '<svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16" aria-hidden="true"><circle cx="5" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="19" cy="12" r="1.6"/></svg>',
    copy:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="14" height="14" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
    sliders:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/></svg>',
    check:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>',
    shield:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="15" height="15" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    external: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="13" height="13" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14L21 3"/></svg>'
  };

  function esc(v) {
    return String(v === null || v === undefined ? '' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function q(root, sel) { return root ? root.querySelector(sel) : null; }
  function qa(root, sel) { return root ? Array.prototype.slice.call(root.querySelectorAll(sel)) : []; }

  function currentUser() {
    if (window.NGIS_CURRENT_USER && (window.NGIS_CURRENT_USER.email || window.NGIS_CURRENT_USER.username)) {
      return window.NGIS_CURRENT_USER;
    }
    if (window.NGISAuth && typeof window.NGISAuth.getUser === 'function') {
      var u = window.NGISAuth.getUser();
      if (u && (u.email || u.username)) return u;
    }
    try {
      var raw = window.localStorage.getItem('auth_user');
      if (raw) {
        var parsed = JSON.parse(raw);
        if (parsed && (parsed.email || parsed.username)) return parsed;
      }
    } catch (_) {}
    return null;
  }

  function actor() {
    var u = currentUser();
    if (u && u.email) return String(u.email).trim().toLowerCase();
    if (u && u.username) return String(u.username).trim().toLowerCase();
    return (window.PAGE && window.PAGE.userEmail) || 'admin@ngis.edu.kh';
  }

  function fetchJson(url) {
    return fetch(url, { headers: { 'X-Actor': actor() } }).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok) {
          var err = new Error((j && j.error) || ('HTTP ' + r.status));
          err.status = r.status;
          err.payload = j;
          throw err;
        }
        return j;
      });
    });
  }

  function postJson(url, body, method) {
    return fetch(url, {
      method: method || 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Actor': actor() },
      body: JSON.stringify(body || {})
    }).then(function (r) {
      return r.json().then(function (j) { j.__status = r.status; return j; });
    });
  }

  function toast(__root, __a, __b) {
  /* Shared NGIS operation-feedback engine (ui-states.js) — this module's
     legacy signature is toast(root, message, tone); root is ignored. */
  if (!(window.NGISUI && window.NGISUI.toast)) {
    if (window.console) console.warn('toast unavailable:', __a);
    return null;
  }
  var __k;
  if (__b === 'bad' || __b === true || __b === 'error' || __b === 'danger' || __b === 'fail') __k = 'error';
  else if (__b === 'warning' || __b === 'warn') __k = 'warning';
  else if (__b === 'info') __k = 'info';
  else __k = 'success';
  return window.NGISUI.toast.show(__k, String(__a));
}

  function initials(name) {
    var clean = String(name || '?')
      .replace(/^(?:h\.e\.|dr|mr|mrs|ms|prof|coach)\.?\s+/i, '')
      .trim();
    var parts = clean ? clean.split(/\s+/) : ['?'];
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function avatarTone(name) {
    var s = String(name || '');
    var hash = 0;
    for (var i = 0; i < s.length; i += 1) hash = (hash + s.charCodeAt(i)) % 6;
    return 'tone-' + hash;
  }

  function avatarSrc(photo) {
    var url = String(photo || '').trim();
    if (!url) return '';
    if (url.indexOf('images.pexels.com/') !== -1) {
      var base = url.split('?')[0];
      return base + '?auto=compress&cs=tinysrgb&w=240&h=240&fit=crop&crop=faces,top';
    }
    if (url.indexOf('images.unsplash.com/') !== -1 && url.indexOf('fit=crop') !== -1) {
      return url.replace(/w=\d+/g, 'w=240').replace(/h=\d+/g, 'h=240');
    }
    return url;
  }

  function avatarHtml(name, photo, opts) {
    var o = opts || {};
    var sizeCls = o.size === 'lg' ? ' smx-avatar-lg' : (o.size === 'sm' ? ' smx-avatar-sm' : '');
    var src = avatarSrc(photo);
    var inner =
      '<span class="smx-avatar-wrap' + sizeCls + '">' +
        '<span class="smx-avatar smx-avatar-fallback ' + avatarTone(name) + '" aria-hidden="true">' + esc(initials(name)) + '</span>' +
        (src ? '<img class="smx-avatar smx-avatar-img" src="' + esc(src) + '" alt="' + (o.interactive ? '' : esc(name)) + '" loading="lazy" decoding="async" onerror="this.remove()">' : '') +
      '</span>';
    if (o.interactive) {
      return '<button type="button" class="smx-avatar-btn" data-action="view" aria-label="View ' + esc(name) + ' details" title="View details">' + inner + '</button>';
    }
    return inner;
  }

  function statusIndicatorHtml(status) {
    var s = status || 'none';
    var label = STATUS_LABEL[s] || s;
    return '<span class="smx-status-inline' + (s === 'none' ? ' is-none' : '') + '">' +
      '<i class="smx-status-dot ' + esc(s) + '" aria-hidden="true"></i>' + esc(label) + '</span>';
  }

  function formatDateTime(ts) {
    if (!ts) return 'Never';
    return String(ts).replace('T', ' ').slice(0, 16);
  }

  function suggestUsername(name, personType) {
    var clean = String(name || '')
      .replace(/^(?:h\.e\.|dr|mr|mrs|ms|prof|coach)\.?\s+/i, '')
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, ' ')
      .trim()
      .split(/\s+/)
      .filter(Boolean);
    var base = clean.length >= 2 ? (clean[0] + '.' + clean[clean.length - 1]) : (clean[0] || personType || 'user');
    base = base.slice(0, 26);
    if (personType === 'admin' && base.indexOf('@') === -1) return base + '@ngis.edu.kh';
    return base;
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
        resolve();
      } catch (err) { reject(err); }
    });
  }

  function pageWindow(current, totalPages) {
    if (totalPages <= 7) {
      var arr = [];
      for (var i = 1; i <= totalPages; i += 1) arr.push(i);
      return arr;
    }
    var out = [1];
    var left = Math.max(2, current - 1);
    var right = Math.min(totalPages - 1, current + 1);
    if (left > 2) out.push('…');
    for (var p = left; p <= right; p += 1) out.push(p);
    if (right < totalPages - 1) out.push('…');
    out.push(totalPages);
    return out;
  }

  function pagerHtml(st) {
    if (!st.total) return '';
    var start = (st.page - 1) * st.pageSize + 1;
    var end = Math.min(st.total, st.page * st.pageSize);
    var parts = ['<div class="smx-table-foot">'];
    parts.push('<span>Showing <span class="smx-record-count">' + start + '</span> to <span class="smx-record-count">' +
      end + '</span> of <span class="smx-record-count">' + st.total + '</span> records</span>');
    if (st.pages > 1) {
      parts.push('<div class="smx-pager" role="navigation" aria-label="Directory pagination">');
      parts.push('<button type="button" class="smx-btn sm ghost" data-page="prev"' +
        (st.page <= 1 ? ' disabled' : '') + '>Previous</button>');
      pageWindow(st.page, st.pages).forEach(function (item) {
        if (item === '…') {
          parts.push('<span class="smx-pager-ellip" aria-hidden="true">…</span>');
        } else {
          var isCur = item === st.page;
          parts.push('<button type="button" class="smx-page-btn' + (isCur ? ' active' : '') + '" data-page-num="' + item + '"' +
            (isCur ? ' aria-current="page"' : '') + '>' + item + '</button>');
        }
      });
      parts.push('<button type="button" class="smx-btn sm ghost" data-page="next"' +
        (st.page >= st.pages ? ' disabled' : '') + '>Next</button>');
      parts.push('</div>');
    }
    parts.push('</div>');
    return parts.join('');
  }

  function closeFloatingMenus() {
    qa(document, '.smx-row-menu').forEach(function (el) { el.remove(); });
    qa(document, '.smx-more-pop').forEach(function (el) { el.classList.add('hidden'); });
    qa(document, '[aria-expanded="true"][data-action="more"]').forEach(function (b) {
      b.setAttribute('aria-expanded', 'false');
    });
  }

  function openModal(root, title, subtitle, bodyHtml, footHtml, wide, options) {
    closeFloatingMenus();
    closeModal(root, true);
    var wrap = document.createElement('div');
    wrap.className = 'smx-modal-backdrop ngis-modal-backdrop';
    wrap.setAttribute('role', 'dialog');
    wrap.setAttribute('aria-modal', 'true');
    wrap.setAttribute('aria-label', title || 'Modal Dialog');
    wrap.innerHTML =
      '<div class="smx-modal ngis-modal' + (wide ? ' wide ngis-modal-lg' : '') + '" role="document">' +
        '<div class="smx-modal-head ngis-modal-head"><div>' +
          '<h2 class="smx-modal-title ngis-modal-title">' + esc(title) + '</h2>' +
          (subtitle ? '<p class="smx-modal-sub ngis-modal-sub">' + esc(subtitle) + '</p>' : '') +
        '</div><button type="button" class="smx-close ngis-modal-close" data-modal-close aria-label="Close modal">&times;</button></div>' +
        '<div class="smx-modal-body ngis-modal-body">' + bodyHtml + '</div>' +
        (footHtml ? '<div class="smx-modal-foot ngis-modal-foot">' + footHtml + '</div>' : '') +
      '</div>';

    // Append to document.body to ensure full viewport isolation from transformed ancestors
    document.body.appendChild(wrap);

    if (window.NGIS_MODAL && typeof window.NGIS_MODAL.open === 'function') {
      window.NGIS_MODAL.open(wrap, options || { confirmUnsaved: true });
    } else {
      document.body.classList.add('ngis-modal-open');
      wrap.classList.add('ngis-modal-active');
    }

    wrap.addEventListener('click', function (e) {
      if (e.target === wrap) {
        closeModal(root, false);
      } else if (e.target.closest('[data-modal-close]')) {
        closeModal(root, false);
      }
    });
    return wrap;
  }

  function closeModal(root, force) {
    var old = document.querySelector('.smx-modal-backdrop') || (root && q(root, '.smx-modal-backdrop'));
    if (!old) return;
    if (window.NGIS_MODAL && typeof window.NGIS_MODAL.close === 'function') {
      window.NGIS_MODAL.close(old, !!force);
    } else {
      old.remove();
      document.body.classList.remove('ngis-modal-open');
    }
  }

  function closeFilterSheet(root, force) {
    var sheet = document.querySelector('.smx-sheet-backdrop') || (root && q(root, '.smx-sheet-backdrop'));
    if (!sheet) return;
    if (window.NGIS_MODAL && typeof window.NGIS_MODAL.close === 'function') {
      window.NGIS_MODAL.close(sheet, !!force);
    } else {
      sheet.remove();
      document.body.classList.remove('ngis-modal-open');
    }
  }

  function renderDirectory(root, cfg) {
    var state = {
      search: '',
      status: '',
      campus: '',
      department: '',
      classFilter: '',
      sort: 'name',
      order: 'asc',
      page: 1,
      pageSize: 25,
      pages: 1,
      total: 0,
      summary: { total: 0, active: 0, pending: 0, locked: 0, suspended: 0, disabled: 0, withoutAccount: 0, withAccount: 0, campusesCount: 1 },
      facets: { campuses: [], campus_options: ['Tuol Kork Main Campus', 'Chamkarmon High School Branch', 'STEM & Robotics Innovation Hub', 'Sensok', 'All campuses'], departments: [], classes: [] },
      rows: [],
      allTypeRows: [],
      selected: {},
      selectedRows: {},
      tokenNotice: null,
      loading: true,
      requestSeq: 0
    };

    var docEscBound = false;

    function isSuperAdminActor() {
      var u = currentUser();
      var em = actor();
      var role = String((u && (u.accountRole || u.role)) || '').toUpperCase().replace(/\s+/g, '_');
      var poolList = (state.allTypeRows && state.allTypeRows.length) ? state.allTypeRows : state.rows;
      var superMatch = (poolList || []).find(function (r) {
        return r.account && r.account.role === 'SUPER_ADMIN' && r.account.status === 'active' &&
          (r.account.username === em || r.account.email === em);
      });
      if (superMatch) return true;
      return role === 'SUPER_ADMIN' || em === 'admin@ngis.edu.kh';
    }

    function activeFilterCount() {
      var n = 0;
      if (state.status) n += 1;
      if (state.campus) n += 1;
      if (state.department) n += 1;
      if (state.classFilter) n += 1;
      return n;
    }

    function queryUrl(exportCsv) {
      var p = new URLSearchParams({
        type: cfg.type,
        search: state.search,
        status: state.status || 'all',
        campus: state.campus || 'all',
        department: state.department || 'all',
        'class': state.classFilter || 'all',
        sort: state.sort,
        order: state.order,
        page: String(state.page),
        page_size: String(state.pageSize)
      });
      return (exportCsv ? '/api/user-mgmt/export?' : '/api/user-mgmt/directory?') + p.toString();
    }

    function load(opts) {
      var keepShell = opts && opts.keepToolbar;
      state.requestSeq += 1;
      var seq = state.requestSeq;
      if (!keepShell && !state.rows.length) {
        root.innerHTML = window.NGIS_SKELETON
          ? '<div class="ngis-sm">' + window.NGIS_SKELETON.table({ rows: 6 }) + '</div>'
          : '<div class="ngis-sm"><div class="smx-empty">Loading ' + esc(cfg.title.toLowerCase()) + '...</div></div>';
      }
      fetchJson(queryUrl(false)).then(function (j) {
        if (seq !== state.requestSeq) return;
        state.loading = false;
        state.rows = j.data || [];
        state.total = j.total || 0;
        state.pages = j.pages || 1;
        state.summary = j.summary || state.summary;
        state.facets = j.facets || state.facets;
        state.rows.forEach(function (r) {
          if (state.selected[r.person_id]) state.selectedRows[r.person_id] = r;
        });
        paint();
      }).catch(function (err) {
        if (seq !== state.requestSeq) return;
        root.innerHTML = '<div class="ngis-sm"><div class="smx-empty">Unable to load directory (' + esc(err.message) + ').</div></div>';
      });
    }

    function metricsHtml() {
      var s = state.summary || {};
      var total = s.totalRecords || 0;
      var linked = s.linkedCount || 0;
      var active = s.activeCount || 0;
      var pending = s.pendingCount || 0;
      var unlinked = s.unlinkedCount || 0;
      var suspended = s.suspendedCount || 0;
      var attention = pending + suspended;
      var notReady = pending + unlinked;
      var activePct = total ? Math.round((active * 100) / total) : 0;

      var sub3 = [];
      if (pending) sub3.push(pending + ' pending activation');
      if (unlinked) sub3.push(unlinked + ' without login');
      if (suspended) sub3.push(suspended + ' restricted');
      if (!sub3.length) sub3.push('All accounts verified');

      return '<section class="smx-stat-strip" aria-label="Directory summary">' +
        '<div class="smx-stat-card">' +
          '<span class="smx-stat-label">Total Accounts</span>' +
          '<div class="smx-stat-value">' + total + '</div>' +
          '<span class="smx-stat-sub">' + linked + ' provisioned · ' + (s.campusesCount || 1) + (s.campusesCount === 1 ? ' campus' : ' campuses') + '</span>' +
        '</div>' +
        '<div class="smx-stat-card">' +
          '<span class="smx-stat-label">Active Accounts</span>' +
          '<div class="smx-stat-value ok">' + active + '</div>' +
          '<span class="smx-stat-sub">' + activePct + '% enabled for portal sign-in</span>' +
        '</div>' +
        '<div class="smx-stat-card' + (attention > 0 ? ' warn' : '') + '">' +
          '<span class="smx-stat-label">Pending / No Login</span>' +
          '<div class="smx-stat-value' + (attention > 0 ? ' warn' : '') + '">' + notReady + '</div>' +
          '<span class="smx-stat-sub">' + esc(sub3.join(' · ')) + '</span>' +
        '</div>' +
      '</section>';
    }

    function headSectionHtml() {
      var isAdminDir = cfg.type === 'admin';
      var allowAdd = true;
      var secondaryDesktop =
        (cfg.hasImport ? '<button type="button" class="smx-btn smx-head-secondary-desktop" data-action="import">' + ICONS.upload + 'Import</button>' : '') +
        '<a class="smx-btn smx-head-secondary-desktop" href="' + esc(queryUrl(true)) + '" download>' + ICONS.download + 'Export CSV</a>';
      var addBtn =
        '<button type="button" class="smx-btn primary smx-btn-primary-add" data-action="add-account"' +
        (allowAdd ? '' : ' disabled title="Super Admin authorization required to create administrator logins"') + '>' +
        ICONS.plus + esc(cfg.addLabel) + '</button>';
      var overflowBtn =
        '<button type="button" class="smx-btn smx-head-overflow-btn" data-action="head-overflow" aria-label="More directory actions" title="Import or Export">' +
        ICONS.more + '</button>';

      return '<section class="smx-head">' +
        '<div>' +
          '<div class="smx-eyebrow">' + esc(cfg.eyebrow) + '</div>' +
          '<div class="smx-title-row"><h1 class="smx-title">' + esc(cfg.title) + '</h1></div>' +
        '</div>' +
        '<div class="smx-head-actions">' + addBtn + secondaryDesktop + overflowBtn + '</div>' +
      '</section>';
    }

    function statusOptionsHtml(selected) {
      var opts = [
        ['', 'All statuses'],
        ['active', 'Active'],
        ['pending_activation', 'Pending Activation'],
        ['none', 'No Account'],
        ['suspended', 'Suspended'],
        ['disabled', 'Disabled'],
        ['locked', 'Locked']
      ];
      return opts.map(function (o) {
        return '<option value="' + esc(o[0]) + '"' + (selected === o[0] ? ' selected' : '') + '>' + esc(o[1]) + '</option>';
      }).join('');
    }

    function campusFilterOptionsHtml(selected) {
      var list = state.facets.campuses || [];
      return '<option value="">All campuses</option>' + list.map(function (c) {
        return '<option value="' + esc(c) + '"' + (selected === c ? ' selected' : '') + '>' + esc(c) + '</option>';
      }).join('');
    }

    function extraFilterSelectHtml(idPrefix) {
      if (cfg.extraFilter === 'class') {
        var classes = state.facets.classes || [];
        return '<select id="' + esc(idPrefix) + 'class" class="smx-select" aria-label="Filter by class">' +
          '<option value="">All classes</option>' +
          classes.map(function (c) {
            return '<option value="' + esc(c) + '"' + (state.classFilter === c ? ' selected' : '') + '>' + esc(c) + '</option>';
          }).join('') + '</select>';
      }
      if (cfg.extraFilter === 'department') {
        var deps = state.facets.departments || [];
        return '<select id="' + esc(idPrefix) + 'dept" class="smx-select" aria-label="Filter by department">' +
          '<option value="">All departments</option>' +
          deps.map(function (d) {
            return '<option value="' + esc(d) + '"' + (state.department === d ? ' selected' : '') + '>' + esc(d) + '</option>';
          }).join('') + '</select>';
      }
      return '';
    }

    function toolbarHtml() {
      var fCount = activeFilterCount();
      var hasAny = fCount > 0 || !!state.search || state.sort !== 'name';
      return '<section class="smx-filter-card" aria-label="Directory search and filters">' +
        '<div class="smx-filter-top">' +
          '<div class="smx-search">' +
            '<span class="smx-search-icon">' + ICONS.search + '</span>' +
            '<input id="smx-search" class="smx-input" type="search" value="' + esc(state.search) + '" placeholder="' + esc(cfg.searchPlaceholder) + '" aria-label="' + esc(cfg.searchPlaceholder) + '">' +
          '</div>' +
          '<button type="button" class="smx-btn smx-filters-toggle" data-action="open-filter-sheet">' +
            ICONS.filter + 'Filters' + (fCount ? ' (' + fCount + ')' : '') +
          '</button>' +
          '<div class="smx-filter-group">' +
            '<select id="smx-status" class="smx-select" aria-label="Filter by account status">' + statusOptionsHtml(state.status) + '</select>' +
            '<select id="smx-campus" class="smx-select" aria-label="Filter by campus">' + campusFilterOptionsHtml(state.campus) + '</select>' +
            extraFilterSelectHtml('smx-') +
            '<div class="smx-more-wrap">' +
              '<button type="button" class="smx-btn" data-action="toggle-more-pop" aria-haspopup="true" aria-expanded="false">' + ICONS.sliders + 'More</button>' +
              '<div class="smx-more-pop hidden" id="smx-more-pop" role="dialog" aria-label="Sort and display options">' +
                '<div><label class="smx-more-pop-label" for="smx-sort">Sort order</label>' +
                  '<select id="smx-sort" class="smx-select">' +
                    '<option value="name"' + (state.sort === 'name' ? ' selected' : '') + '>Name (A to Z)</option>' +
                    '<option value="status"' + (state.sort === 'status' ? ' selected' : '') + '>Account Status</option>' +
                    '<option value="last_login"' + (state.sort === 'last_login' ? ' selected' : '') + '>Last Login</option>' +
                  '</select></div>' +
                '<div><label class="smx-more-pop-label" for="smx-pagesize">Rows per page</label>' +
                  '<select id="smx-pagesize" class="smx-select">' +
                    '<option value="25"' + (state.pageSize === 25 ? ' selected' : '') + '>25 per page</option>' +
                    '<option value="50"' + (state.pageSize === 50 ? ' selected' : '') + '>50 per page</option>' +
                    '<option value="100"' + (state.pageSize === 100 ? ' selected' : '') + '>100 per page</option>' +
                  '</select></div>' +
              '</div>' +
            '</div>' +
            (hasAny ? '<button type="button" class="smx-btn ghost smx-reset-btn" data-action="clear-filters">' + ICONS.reset + 'Clear</button>' : '') +
          '</div>' +
        '</div>' +
        '<div class="smx-filter-sub">' +
          '<div class="smx-filter-sub-left">' +
            '<span>Showing <span class="smx-record-count">' + state.total + '</span> ' + esc(state.total === 1 ? cfg.recordNoun : cfg.recordPlural) + '</span>' +
            (fCount ? '<span class="smx-vdiv" aria-hidden="true"></span><span>' + fCount + (fCount === 1 ? ' filter active' : ' filters active') + '</span>' : '') +
          '</div>' +
          '<div class="smx-filter-sub-left">' +
            (cfg.type === 'admin' && !isSuperAdminActor() ? '<span class="smx-cell-muted">Read-only view (Super Admin required to create or edit admins)</span>' : '') +
          '</div>' +
        '</div>' +
      '</section>';
    }

    function tokenBarHtml() {
      var t = state.tokenNotice;
      if (!t) return '';
      return '<div class="smx-token-bar" role="status">' +
        '<div class="smx-token-main">' +
          '<span><strong>' + esc(t.title) + ':</strong> ' + esc(t.username) + ' · One-time token' + (t.expires ? ' (expires ' + esc(formatDateTime(t.expires)) + ')' : '') + ':</span>' +
          '<code class="smx-token-code">' + esc(t.token) + '</code>' +
        '</div>' +
        '<div class="smx-token-actions">' +
          '<button type="button" class="smx-btn sm" data-action="copy-token">' + ICONS.copy + 'Copy Token</button>' +
          '<button type="button" class="smx-btn sm ghost" data-action="dismiss-token">Dismiss</button>' +
        '</div>' +
      '</div>';
    }

    function bulkBarHtml() {
      if (!cfg.hasBulk) return '';
      var count = Object.keys(state.selected).length;
      if (!count) return '';
      return '<div class="smx-bulk-bar" role="region" aria-label="Bulk selection actions">' +
        '<div class="smx-bulk-info">' +
          '<span class="smx-bulk-badge">' + count + ' selected</span>' +
          '<span>Apply action to selected records in this directory</span>' +
        '</div>' +
        '<div class="smx-bulk-actions">' +
          '<button type="button" class="smx-btn sm primary" data-action="bulk-provision">Provision Unlinked</button>' +
          '<button type="button" class="smx-btn sm" data-action="bulk-activate">Activate</button>' +
          '<button type="button" class="smx-btn sm danger" data-action="bulk-suspend">Suspend</button>' +
          '<button type="button" class="smx-btn sm ghost" data-action="clear-selection">Clear</button>' +
        '</div>' +
      '</div>';
    }

    function profileLinkHtml(r) {
      if (!cfg.fallbackUrl || !r.person_id) return '';
      return '<button type="button" class="smx-action-link primary-link" data-action="open-profile" ' +
        'title="Open the full ' + esc(cfg.recordNoun) + ' profile">' + ICONS.external + 'Profile</button>';
    }

    function rowActionsHtml(r) {
      if (!r.account) {
        return '<div class="smx-row-actions">' +
          '<button type="button" class="smx-action-link" data-action="view">View</button>' +
          profileLinkHtml(r) +
        '</div>';
      }
      return '<div class="smx-row-actions">' +
        '<button type="button" class="smx-action-link" data-action="view">View</button>' +
        profileLinkHtml(r) +
        '<button type="button" class="smx-action-link" data-action="edit">Edit</button>' +
        '<button type="button" class="smx-icon-btn smx-more-trigger" data-action="more" aria-label="More options for ' + esc(r.name) + '" aria-expanded="false" aria-haspopup="menu" title="More options">' + ICONS.more + '</button>' +
      '</div>';
    }

    function rowCellsHtml(r) {
      var a = r.account;
      var uname = a && a.username
        ? '<span class="smx-username">' + esc(a.username) + '</span>'
        : '<span class="smx-cell-muted">Not provisioned</span>';
      var personCol = cfg.columns[0];
      var personCell =
        '<td class="smx-cell-person" data-label="' + esc(personCol) + '">' +
          '<div class="smx-person">' +
            avatarHtml(r.name, r.photo, { interactive: true }) +
            '<div><div class="smx-person-name">' + esc(r.name) + '</div>' +
            '<div class="smx-person-id smx-mono">' + esc(r.person_id) + '</div></div>' +
          '</div>' +
        '</td>';

      var checkCell = cfg.hasBulk
        ? '<td class="center" data-label="Select"><input type="checkbox" class="smx-checkbox" data-row-check' +
          (state.selected[r.person_id] ? ' checked' : '') + ' aria-label="Select ' + esc(r.name) + '"></td>'
        : '';

      var middle = '';
      var rowStatus = a ? a.status : 'none';
      if (cfg.type === 'student') {
        middle =
          '<td data-label="Username">' + uname + '</td>' +
          '<td data-label="Campus"><span class="smx-cell-plain">' + esc(r.campus || '—') + '</span></td>' +
          '<td data-label="Class"><span class="smx-cell-plain">' + esc(r.assignment || '—') + '</span></td>' +
          '<td data-label="Account Status">' + statusIndicatorHtml(rowStatus) + '</td>' +
          '<td data-label="Last Login"><span class="smx-cell-muted smx-nowrap">' + esc(formatDateTime(a && a.last_login)) + '</span></td>';
      } else if (cfg.type === 'teacher') {
        middle =
          '<td data-label="Username">' + uname + '</td>' +
          '<td data-label="Campus"><span class="smx-cell-plain">' + esc(r.campus || '—') + '</span></td>' +
          '<td data-label="Department"><span class="smx-cell-plain">' + esc(r.department || '—') + '</span></td>' +
          '<td data-label="Account Status">' + statusIndicatorHtml(rowStatus) + '</td>' +
          '<td data-label="Last Login"><span class="smx-cell-muted smx-nowrap">' + esc(formatDateTime(a && a.last_login)) + '</span></td>';
      } else if (cfg.type === 'staff') {
        middle =
          '<td data-label="Username">' + uname + '</td>' +
          '<td data-label="Department"><span class="smx-cell-plain">' + esc(r.department || '—') + '</span></td>' +
          '<td data-label="Position"><span class="smx-cell-plain">' + esc(r.assignment || r.display_role || '—') + '</span></td>' +
          '<td data-label="Account Status">' + statusIndicatorHtml(rowStatus) + '</td>';
      } else if (cfg.type === 'principal') {
        middle =
          '<td data-label="Username">' + uname + '</td>' +
          '<td data-label="Assigned Campus"><span class="smx-cell-plain">' + esc(r.campus || '—') + '</span></td>' +
          '<td data-label="Account Status">' + statusIndicatorHtml(rowStatus) + '</td>' +
          '<td data-label="Last Login"><span class="smx-cell-muted smx-nowrap">' + esc(formatDateTime(a && a.last_login)) + '</span></td>';
      } else {
        var scopeText = (a && a.access_scope) || (a && a.role === 'SUPER_ADMIN' ? 'Full System Access' : 'Standard Admin Scope');
        middle =
          '<td data-label="Username">' + uname + '</td>' +
          '<td data-label="Campus"><span class="smx-cell-plain">' + esc(r.campus || 'All campuses') + '</span></td>' +
          '<td data-label="Access Scope"><span class="smx-cell-plain">' + esc(scopeText) + '</span></td>' +
          '<td data-label="Account Status">' + statusIndicatorHtml(rowStatus) + '</td>';
      }

      return checkCell + personCell + middle + '<td class="right" data-label="Actions">' + rowActionsHtml(r) + '</td>';
    }

    function tableHtml() {
      var allPageSelected = cfg.hasBulk && state.rows.length > 0 && state.rows.every(function (r) {
        return !!state.selected[r.person_id];
      });
      var ths = [];
      if (cfg.hasBulk) {
        ths.push('<th class="center smx-th-check"><input type="checkbox" class="smx-checkbox" id="smx-check-all"' +
          (allPageSelected ? ' checked' : '') + ' aria-label="Select all on page"></th>');
      }
      cfg.columns.forEach(function (col) {
        ths.push('<th' + (col === 'Actions' ? ' class="right"' : '') + '>' + esc(col) + '</th>');
      });

      var colSpan = cfg.columns.length + (cfg.hasBulk ? 1 : 0);
      var rowsHtml = state.rows.length
        ? state.rows.map(function (r) {
            return '<tr class="' + (state.selected[r.person_id] ? 'is-selected' : '') + '" data-pid="' + esc(r.person_id) + '">' +
              rowCellsHtml(r) + '</tr>';
          }).join('')
        : '<tr><td colspan="' + colSpan + '" class="smx-empty">No matching records in ' + esc(cfg.title) + '.</td></tr>';

      return '<section class="smx-table-card" aria-label="' + esc(cfg.title) + ' table">' +
        '<div class="smx-table-scroll"><table class="smx-table">' +
          '<thead><tr>' + ths.join('') + '</tr></thead>' +
          '<tbody>' + rowsHtml + '</tbody>' +
        '</table></div>' + pagerHtml(state) + '</section>';
    }

    function paint() {
      var activeEl = document.activeElement;
      var restoreSearchFocus = activeEl && activeEl.id === 'smx-search';
      var selStart = restoreSearchFocus ? activeEl.selectionStart : null;
      var selEnd = restoreSearchFocus ? activeEl.selectionEnd : null;

      root.innerHTML = '<div class="ngis-sm">' +
        headSectionHtml() +
        metricsHtml() +
        toolbarHtml() +
        tokenBarHtml() +
        bulkBarHtml() +
        tableHtml() +
      '</div>';

      bindHandlers();

      if (restoreSearchFocus) {
        var inp = q(root, '#smx-search');
        if (inp) {
          inp.focus();
          if (selStart !== null) {
            try { inp.setSelectionRange(selStart, selEnd); } catch (_) {}
          }
        }
      }
    }

    var searchTimer = null;
    function bindHandlers() {
      var searchInput = q(root, '#smx-search');
      if (searchInput) {
        searchInput.addEventListener('input', function (e) {
          state.search = e.target.value.trim();
          state.page = 1;
          if (searchTimer) clearTimeout(searchTimer);
          searchTimer = setTimeout(function () { load({ keepToolbar: true }); }, 160);
        });
      }

      var statusSel = q(root, '#smx-status');
      if (statusSel) {
        statusSel.addEventListener('change', function (e) {
          state.status = e.target.value; state.page = 1; load({ keepToolbar: true });
        });
      }
      var campusSel = q(root, '#smx-campus');
      if (campusSel) {
        campusSel.addEventListener('change', function (e) {
          state.campus = e.target.value; state.page = 1; load({ keepToolbar: true });
        });
      }
      var classSel = q(root, '#smx-class');
      if (classSel) {
        classSel.addEventListener('change', function (e) {
          state.classFilter = e.target.value; state.page = 1; load({ keepToolbar: true });
        });
      }
      var deptSel = q(root, '#smx-dept');
      if (deptSel) {
        deptSel.addEventListener('change', function (e) {
          state.department = e.target.value; state.page = 1; load({ keepToolbar: true });
        });
      }
      var sortSel = q(root, '#smx-sort');
      if (sortSel) {
        sortSel.addEventListener('change', function (e) {
          state.sort = e.target.value;
          state.order = state.sort === 'last_login' ? 'desc' : 'asc';
          state.page = 1;
          load({ keepToolbar: true });
        });
      }
      var sizeSel = q(root, '#smx-pagesize');
      if (sizeSel) {
        sizeSel.addEventListener('change', function (e) {
          state.pageSize = parseInt(e.target.value, 10) || 25;
          state.page = 1;
          load({ keepToolbar: true });
        });
      }

      var moreBtn = q(root, '[data-action="toggle-more-pop"]');
      var morePop = q(root, '#smx-more-pop');
      if (moreBtn && morePop) {
        moreBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          var wasHidden = morePop.classList.contains('hidden');
          closeFloatingMenus();
          if (wasHidden) {
            morePop.classList.remove('hidden');
            moreBtn.setAttribute('aria-expanded', 'true');
          }
        });
        morePop.addEventListener('click', function (e) { e.stopPropagation(); });
      }

      var sheetBtn = q(root, '[data-action="open-filter-sheet"]');
      if (sheetBtn) sheetBtn.addEventListener('click', openFilterSheet);

      var clearBtn = q(root, '[data-action="clear-filters"]');
      if (clearBtn) {
        clearBtn.addEventListener('click', function () {
          state.search = ''; state.status = ''; state.campus = '';
          state.department = ''; state.classFilter = '';
          state.sort = 'name'; state.order = 'asc'; state.page = 1;
          load();
        });
      }

      var addBtn = q(root, '[data-action="add-account"]');
      if (addBtn) addBtn.addEventListener('click', function () {
        // Add User is link-first: search and link an existing registry record
        // of THIS directory's type (Sections A-D). When the person does not
        // exist yet, Section A offers the sanctioned create-new-record path.
        // The backend independently validates the account type and the
        // actor's authority regardless of the page context.
        openAddAccountModal(null);
      });

      var impBtn = q(root, '[data-action="import"]');
      if (impBtn) impBtn.addEventListener('click', openImportModal);

      var overflowBtn = q(root, '[data-action="head-overflow"]');
      if (overflowBtn) {
        overflowBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          openHeaderOverflowMenu(overflowBtn);
        });
      }

      var copyBtn = q(root, '[data-action="copy-token"]');
      if (copyBtn && state.tokenNotice) {
        copyBtn.addEventListener('click', function () {
          copyToClipboard(state.tokenNotice.token).then(function () {
            toast(root, 'One-time token copied to clipboard.');
          });
        });
      }
      var dismissBtn = q(root, '[data-action="dismiss-token"]');
      if (dismissBtn) {
        dismissBtn.addEventListener('click', function () { state.tokenNotice = null; paint(); });
      }

      var bulkProv = q(root, '[data-action="bulk-provision"]');
      if (bulkProv) bulkProv.addEventListener('click', openBulkModal);
      var bulkAct = q(root, '[data-action="bulk-activate"]');
      if (bulkAct) bulkAct.addEventListener('click', function () { confirmBulkStatus('activate'); });
      var bulkSusp = q(root, '[data-action="bulk-suspend"]');
      if (bulkSusp) bulkSusp.addEventListener('click', function () { confirmBulkStatus('suspend'); });
      var bulkClr = q(root, '[data-action="clear-selection"]');
      if (bulkClr) bulkClr.addEventListener('click', function () {
        state.selected = {}; state.selectedRows = {}; paint();
      });

      var checkAll = q(root, '#smx-check-all');
      if (checkAll) {
        checkAll.addEventListener('change', function (e) {
          state.rows.forEach(function (r) {
            if (e.target.checked) { state.selected[r.person_id] = true; state.selectedRows[r.person_id] = r; }
            else { delete state.selected[r.person_id]; delete state.selectedRows[r.person_id]; }
          });
          paint();
        });
      }

      qa(root, '[data-row-check]').forEach(function (cb) {
        cb.addEventListener('change', function (e) {
          var pid = cb.closest('tr').getAttribute('data-pid');
          var r = state.rows.find(function (x) { return x.person_id === pid; });
          if (e.target.checked) { state.selected[pid] = true; if (r) state.selectedRows[pid] = r; }
          else { delete state.selected[pid]; delete state.selectedRows[pid]; }
          paint();
        });
      });

      qa(root, 'tbody tr[data-pid]').forEach(function (tr) {
        var pid = tr.getAttribute('data-pid');
        var row = state.rows.find(function (r) { return r.person_id === pid; });
        if (!row) return;
        qa(tr, '[data-action]').forEach(function (btn) {
          btn.addEventListener('click', function (e) {
            e.stopPropagation();
            var act = btn.getAttribute('data-action');
            if (act === 'view') openViewModal(row);
            else if (act === 'open-profile') openExternalProfile(row);
            else if (act === 'edit') openEditModal(row);
            else if (act === 'create-for-row') openAddAccountModal(row);
            else if (act === 'more') openRowMenu(row, btn);
          });
        });
      });

      qa(root, '[data-page]').forEach(function (b) {
        b.addEventListener('click', function () {
          state.page += (b.getAttribute('data-page') === 'next' ? 1 : -1);
          load({ keepToolbar: true });
        });
      });
      qa(root, '[data-page-num]').forEach(function (b) {
        b.addEventListener('click', function () {
          state.page = parseInt(b.getAttribute('data-page-num'), 10) || 1;
          load({ keepToolbar: true });
        });
      });

      if (!docEscBound) {
        docEscBound = true;
        document.addEventListener('click', function () { closeFloatingMenus(); });
        document.addEventListener('keydown', function (e) {
          if (e.key === 'Escape') {
            closeFloatingMenus();
            closeFilterSheet(root);
            closeModal(root);
          }
        });
      }
    }

    function openHeaderOverflowMenu(triggerBtn) {
      closeFloatingMenus();
      var rect = triggerBtn.getBoundingClientRect();
      var menu = document.createElement('div');
      menu.className = 'smx-row-menu';
      menu.setAttribute('role', 'menu');
      menu.innerHTML =
        (cfg.hasImport ? '<button type="button" class="smx-menu-item" role="menuitem" data-hdr="import">Import Provisioning CSV</button>' : '') +
        '<a class="smx-menu-item" role="menuitem" href="' + esc(queryUrl(true)) + '" download>Export Directory CSV</a>';
      menu.style.top = (rect.bottom + 6) + 'px';
      menu.style.right = Math.max(12, window.innerWidth - rect.right) + 'px';
      document.body.appendChild(menu);
      menu.addEventListener('click', function (e) { e.stopPropagation(); });
      var imp = q(menu, '[data-hdr="import"]');
      if (imp) imp.addEventListener('click', function () { closeFloatingMenus(); openImportModal(); });
    }

    function openFilterSheet() {
      closeFilterSheet(root);
      var host = q(root, '.ngis-sm') || root;
      var sheet = document.createElement('div');
      sheet.className = 'smx-sheet-backdrop';
      sheet.innerHTML =
        '<div class="smx-sheet" role="dialog" aria-modal="true" aria-label="Filter ' + esc(cfg.title) + '">' +
          '<div class="smx-sheet-head">' +
            '<h2 class="smx-modal-title">Filter &amp; Sort</h2>' +
            '<button type="button" class="smx-close" data-sheet-close aria-label="Close filters">&times;</button>' +
          '</div>' +
          '<label class="smx-field"><span>Account Status</span><select id="sh-status" class="smx-select">' + statusOptionsHtml(state.status) + '</select></label>' +
          '<label class="smx-field"><span>Campus</span><select id="sh-campus" class="smx-select">' + campusFilterOptionsHtml(state.campus) + '</select></label>' +
          (cfg.extraFilter ? '<label class="smx-field"><span>' + esc(cfg.extraFilterLabel) + '</span>' + extraFilterSelectHtml('sh-') + '</label>' : '') +
          '<label class="smx-field"><span>Sort by</span><select id="sh-sort" class="smx-select">' +
            '<option value="name"' + (state.sort === 'name' ? ' selected' : '') + '>Name (A to Z)</option>' +
            '<option value="status"' + (state.sort === 'status' ? ' selected' : '') + '>Account Status</option>' +
            '<option value="last_login"' + (state.sort === 'last_login' ? ' selected' : '') + '>Last Login</option>' +
          '</select></label>' +
          '<div class="smx-sheet-actions">' +
            '<button type="button" class="smx-btn" data-sheet-reset>Clear All</button>' +
            '<button type="button" class="smx-btn primary" data-sheet-apply>Apply Filters</button>' +
          '</div>' +
        '</div>';
      host.appendChild(sheet);
      sheet.addEventListener('click', function (e) {
        if (e.target === sheet || e.target.closest('[data-sheet-close]')) closeFilterSheet(root);
      });
      q(sheet, '[data-sheet-reset]').addEventListener('click', function () {
        state.status = ''; state.campus = ''; state.department = ''; state.classFilter = '';
        state.sort = 'name'; state.order = 'asc'; state.page = 1;
        closeFilterSheet(root);
        load();
      });
      q(sheet, '[data-sheet-apply]').addEventListener('click', function () {
        state.status = q(sheet, '#sh-status').value;
        state.campus = q(sheet, '#sh-campus').value;
        var shClass = q(sheet, '#sh-class');
        var shDept = q(sheet, '#sh-dept');
        if (shClass) state.classFilter = shClass.value;
        if (shDept) state.department = shDept.value;
        state.sort = q(sheet, '#sh-sort').value;
        state.order = state.sort === 'last_login' ? 'desc' : 'asc';
        state.page = 1;
        closeFilterSheet(root);
        load();
      });
    }

    function openRowMenu(row, triggerBtn) {
      var wasOpen = triggerBtn.getAttribute('aria-expanded') === 'true';
      closeFloatingMenus();
      if (wasOpen) return;

      var acc = row.account;
      if (!acc) return;
      var st = acc.status || 'pending_activation';
      var isSuper = acc.role === 'SUPER_ADMIN';
      var canModifyAdmin = cfg.type !== 'admin' || isSuperAdminActor();
      var items = [];

      if (st !== 'disabled' && canModifyAdmin) {
        items.push({ key: 'reset', label: 'Reset Password' });
      }
      if (canModifyAdmin) {
        if (st === 'pending_activation') items.push({ key: 'activate', label: 'Activate Account' });
        else if (st === 'locked') items.push({ key: 'unlock', label: 'Unlock Account' });
        else if (st === 'suspended' || st === 'disabled') items.push({ key: 'activate', label: 'Reactivate Account' });

        if ((st === 'active' || st === 'pending_activation') && !isSuper) {
          items.push({ key: 'suspend', label: 'Suspend Account', danger: true });
        }
        if (st !== 'disabled' && !isSuper) {
          items.push({ key: 'disable', label: 'Disable Account', danger: true });
        }
        if (st === 'active' || st === 'pending_activation') {
          items.push({ key: 'revoke', label: 'Revoke Active Sessions', danger: true });
        }
      }
      items.push({ sep: true });
      items.push({ key: 'activity', label: 'View Activity History' });

      var menu = document.createElement('div');
      menu.className = 'smx-row-menu';
      menu.setAttribute('role', 'menu');
      menu.innerHTML = items.map(function (it) {
        if (it.sep) return '<div class="smx-menu-sep" role="separator"></div>';
        return '<button type="button" class="smx-menu-item' + (it.danger ? ' danger' : '') + '" role="menuitem" data-menu="' + esc(it.key) + '">' + esc(it.label) + '</button>';
      }).join('');

      document.body.appendChild(menu);
      var rect = triggerBtn.getBoundingClientRect();
      var mw = menu.offsetWidth || 200;
      var mh = menu.offsetHeight || 180;
      var left = Math.min(window.innerWidth - mw - 12, Math.max(12, rect.right - mw));
      var top = (rect.bottom + mh + 10 > window.innerHeight) ? Math.max(12, rect.top - mh - 6) : (rect.bottom + 6);
      menu.style.left = left + 'px';
      menu.style.top = top + 'px';
      triggerBtn.setAttribute('aria-expanded', 'true');

      menu.addEventListener('click', function (e) { e.stopPropagation(); });
      qa(menu, '[data-menu]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var key = btn.getAttribute('data-menu');
          closeFloatingMenus();
          if (key === 'activity') openActivityModal(row);
          else confirmRowSecurityAction(row, key);
        });
      });
    }

    function confirmRowSecurityAction(row, actionKey) {
      var acc = row.account;
      var titles = {
        reset: 'Reset Password',
        activate: 'Activate Login Account',
        unlock: 'Unlock Login Account',
        suspend: 'Suspend Login Account',
        disable: 'Disable Login Account',
        revoke: 'Revoke Active Sessions'
      };
      var descriptions = {
        reset: 'Generates a single-use password reset token and invalidates prior reset tokens for ' + row.name + '.',
        activate: 'Allows ' + row.name + ' (' + acc.username + ') to sign in to the assigned portal immediately.',
        unlock: 'Clears the lockout flag on ' + acc.username + ' so the user can authenticate again.',
        suspend: 'Temporarily blocks sign-in for ' + acc.username + '. Institutional student/teacher/staff records remain intact.',
        disable: 'Disables portal login access for ' + acc.username + '. Academic and employment profile records are preserved and never deleted.',
        revoke: 'Signs ' + acc.username + ' out of all active browser sessions immediately.'
      };
      var isDanger = (actionKey === 'suspend' || actionKey === 'disable' || actionKey === 'revoke');
      var modal = openModal(
        root,
        titles[actionKey] || 'Confirm Action',
        row.name + ' · ' + acc.username,
        '<div class="smx-note-box' + (isDanger ? ' warn' : '') + '">' + esc(descriptions[actionKey]) + '</div>',
        '<button type="button" class="smx-btn" data-modal-close>Cancel</button>' +
        '<button type="button" class="smx-btn ' + (isDanger ? 'danger' : 'primary') + '" data-confirm-sec>Confirm</button>'
      );
      q(modal, '[data-confirm-sec]').addEventListener('click', function (e) {
        var btn = e.currentTarget;
        btn.disabled = true;
        var req;
        if (actionKey === 'reset') req = postJson('/api/user-mgmt/account/' + encodeURIComponent(acc.id) + '/reset-password', {});
        else if (actionKey === 'revoke') req = postJson('/api/user-mgmt/account/' + encodeURIComponent(acc.id) + '/revoke-sessions', {});
        else req = postJson('/api/user-mgmt/account/' + encodeURIComponent(acc.id) + '/status', { action: actionKey });

        req.then(function (j) {
          closeModal(root);
          if (!j.success) {
            toast(root, j.error || 'Action rejected', 'bad');
            return;
          }
          if (j.reset_token) {
            state.tokenNotice = {
              title: 'Password reset token ready',
              username: acc.username,
              token: j.reset_token,
              expires: j.expires_at
            };
          }
          toast(root, titles[actionKey] + ' completed.');
          load({ keepToolbar: true });
        });
      });
    }

    function openExternalProfile(row) {
      if (!cfg.fallbackUrl || !row.person_id) return;
      window.location.href = cfg.fallbackUrl + '?open-profile=' + encodeURIComponent(row.person_id);
    }

    function openViewModal(row) {
      fetchJson('/api/user-mgmt/user/' + encodeURIComponent(row.person_type) + '/' + encodeURIComponent(row.person_id))
        .then(function (d) {
          var p = d.person || row;
          var a = d.account;
          var scopeOrAssign = cfg.type === 'admin'
            ? ((a && a.access_scope) || (a && a.role === 'SUPER_ADMIN' ? 'Full System Access' : 'Standard Admin Scope'))
            : (p.assignment || p.department || p.display_role || '—');
          var assignLabel = cfg.type === 'student' ? 'Enrolled Class'
            : (cfg.type === 'teacher' ? 'Teaching Assignment'
            : (cfg.type === 'staff' ? 'Department / Position'
            : (cfg.type === 'admin' ? 'Access Scope' : 'Academic Oversight')));

          var infoGrid =
            '<div class="smx-profile-banner">' +
              avatarHtml(p.name, p.photo, { size: 'lg' }) +
              '<div class="smx-profile-banner-meta">' +
                '<div class="smx-profile-banner-name">' + esc(p.name) + '</div>' +
                '<div class="smx-profile-banner-sub"><span class="smx-mono">' + esc(p.person_id) + '</span><span>·</span>' +
                  statusIndicatorHtml(a && a.id ? a.status : 'none') + '</div>' +
              '</div>' +
            '</div>' +
            '<div class="smx-info-grid">' +
              '<div class="smx-info"><span class="smx-info-label">Account Type</span><span>' + esc(ROLES_BY_TYPE[cfg.type]) + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">Username</span><span class="smx-mono">' + esc((a && a.username) || 'Not provisioned') + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">Campus</span><span>' + esc((a && a.campus) || p.campus || '—') + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">' + esc(assignLabel) + '</span><span>' + esc(scopeOrAssign) + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">Email</span><span>' + esc((a && a.email) || 'Not set') + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">Last Login</span><span>' + esc(formatDateTime(a && a.last_login)) + '</span></div>' +
            '</div>' +
            '<p class="smx-note">Identity records remain preserved in the institutional directory even when portal login access is disabled.</p>';

          var foot = '<button type="button" class="smx-btn" data-modal-close>Close</button>' +
            (cfg.fallbackUrl && row.person_id
              ? '<button type="button" class="smx-btn" data-view-act="profile">' + ICONS.external + 'View Profile</button>'
              : '') +
            (a && a.id
              ? '<button type="button" class="smx-btn" data-view-act="activity">Activity</button><button type="button" class="smx-btn primary" data-view-act="edit">Edit Account</button>'
              : '<button type="button" class="smx-btn primary" data-view-act="create">' + ICONS.plus + 'Create Account</button>');
          var modal = openModal(root, p.name, cfg.title + ' · Account Details', infoGrid, foot, true);
          qa(modal, '[data-view-act]').forEach(function (btn) {
            btn.addEventListener('click', function () {
              var k = btn.getAttribute('data-view-act');
              closeModal(root);
              if (k === 'edit') openEditModal(row);
              else if (k === 'activity') openActivityModal(row);
              else if (k === 'create') openAddAccountModal(row);
              else if (k === 'profile') openExternalProfile(row);
            });
          });
        });
    }

    function openEditModal(row) {
      var a = row.account;
      if (!a) { openAddAccountModal(row); return; }
      var campusOpts = (state.facets.campus_options || state.facets.campuses || ['Sensok', 'All campuses']);
      var canChangeCampus = cfg.type === 'principal' || cfg.type === 'admin' || cfg.type === 'staff';
      var campusField = canChangeCampus
        ? '<label class="smx-field"><span>Assigned Campus</span><select id="ed-campus" class="smx-select">' +
            campusOpts.map(function (c) {
              return '<option value="' + esc(c) + '"' + ((a.campus || row.campus) === c ? ' selected' : '') + '>' + esc(c) + '</option>';
            }).join('') + '</select></label>'
        : '<div class="smx-field"><span>Linked Campus</span><div class="smx-note-box">' + esc(row.campus || 'Sensok') + ' (synced from ' + esc(cfg.recordNoun) + ' profile)</div></div>';

      var scopeField = cfg.type === 'admin'
        ? '<label class="smx-field smx-span-2"><span>Access Scope</span><select id="ed-scope" class="smx-select">' +
            ADMIN_SCOPES.map(function (s) {
              return '<option value="' + esc(s) + '"' + ((a.access_scope || '') === s ? ' selected' : '') + '>' + esc(s) + '</option>';
            }).join('') + '</select></label>'
        : (cfg.type === 'staff'
          ? '<label class="smx-field"><span>Department</span><input id="ed-dept" class="smx-input" value="' + esc(a.department || row.department || '') + '"></label>' +
            '<label class="smx-field"><span>Position</span><input id="ed-assign" class="smx-input" value="' + esc(a.assignment || row.assignment || '') + '"></label>'
          : '<div class="smx-field smx-span-2"><span>' + esc(cfg.type === 'student' ? 'Class Assignment' : 'Teaching Department') + '</span>' +
              '<div class="smx-note-box">' + esc(cfg.type === 'student' ? (row.assignment || '—') : (row.department || '—')) +
              ' · Managed from the institutional profile registry to prevent duplicate records.</div></div>');

      var body =
        '<div id="ed-err"></div>' +
        '<div class="smx-form-grid">' +
          '<label class="smx-field"><span>Username</span><input id="ed-username" class="smx-input" value="' + esc(a.username) + '"><div id="ed-un-avail" class="smx-avail"></div></label>' +
          '<label class="smx-field"><span>Email Address</span><input id="ed-email" class="smx-input" type="email" value="' + esc(a.email || '') + '"></label>' +
          campusField +
          '<div class="smx-field"><span>Account Role</span><div class="smx-readonly-chip">' + esc(a.role) + ' (Locked to directory)</div></div>' +
          scopeField +
        '</div>';

      var modal = openModal(
        root,
        'Edit ' + cfg.recordNoun.charAt(0).toUpperCase() + cfg.recordNoun.slice(1) + ' Account',
        row.name + ' · ' + row.person_id,
        body,
        '<button type="button" class="smx-btn" data-modal-close>Cancel</button>' +
        '<button type="button" class="smx-btn primary" data-edit-save>Save Changes</button>',
        true
      );

      var unInp = q(modal, '#ed-username');
      var unAvail = q(modal, '#ed-un-avail');
      var unTimer = null;
      unInp.addEventListener('input', function () {
        var v = unInp.value.trim().toLowerCase();
        if (unTimer) clearTimeout(unTimer);
        if (!v) { unAvail.className = 'smx-avail bad'; unAvail.textContent = 'Username cannot be empty.'; return; }
        unAvail.className = 'smx-avail checking'; unAvail.textContent = 'Checking availability...';
        unTimer = setTimeout(function () {
          fetchJson('/api/user-mgmt/check-username?username=' + encodeURIComponent(v) + '&exclude_id=' + encodeURIComponent(a.id))
            .then(function (res) {
              unAvail.className = 'smx-avail ' + (res.available ? 'ok' : 'bad');
              unAvail.textContent = res.message || (res.available ? 'Available' : 'Already taken');
            });
        }, 180);
      });

      q(modal, '[data-edit-save]').addEventListener('click', function (e) {
        var btn = e.currentTarget;
        var errBox = q(modal, '#ed-err');
        errBox.innerHTML = '';
        var username = unInp.value.trim().toLowerCase();
        var email = q(modal, '#ed-email').value.trim();
        if (!username) { errBox.innerHTML = '<div class="smx-note-box warn" role="alert">Username is required.</div>'; return; }
        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
          errBox.innerHTML = '<div class="smx-note-box warn" role="alert">Enter a valid email address.</div>';
          return;
        }
        var payload = { username: username, email: email };
        var edCampus = q(modal, '#ed-campus');
        var edScope = q(modal, '#ed-scope');
        var edDept = q(modal, '#ed-dept');
        var edAssign = q(modal, '#ed-assign');
        if (edCampus) payload.campus = edCampus.value;
        if (edScope) payload.access_scope = edScope.value;
        if (edDept) payload.department = edDept.value;
        if (edAssign) payload.assignment = edAssign.value;

        btn.disabled = true;
        postJson('/api/user-mgmt/account/' + encodeURIComponent(a.id), payload, 'PUT').then(function (j) {
          btn.disabled = false;
          if (!j.success) {
            errBox.innerHTML = '<div class="smx-note-box warn" role="alert">' + esc(j.error || 'Could not update account') + '</div>';
            return;
          }
          closeModal(root);
          toast(root, 'Account updated for ' + row.name + '.');
          load({ keepToolbar: true });
        });
      });
    }

    function openActivityModal(row) {
      fetchJson('/api/user-mgmt/user/' + encodeURIComponent(row.person_type) + '/' + encodeURIComponent(row.person_id))
        .then(function (d) {
          var logins = (d.login_history || []).slice().reverse();
          var audits = (d.audit || []).slice().reverse();
          var lh = logins.length
            ? logins.map(function (l) {
                return '<div class="smx-activity-row"><span class="smx-mono">' + esc(formatDateTime(l.ts || l.at)) + '</span>' +
                  '<span class="smx-activity-action">' + esc(l.event || 'sign-in') + '</span>' +
                  '<span class="smx-cell-muted smx-mono">' + esc(l.ip || l.by || '') + '</span></div>';
              }).join('')
            : '<div class="smx-cell-muted">No login events recorded yet.</div>';
          var ah = audits.length
            ? audits.map(function (e) {
                return '<div class="smx-activity-row"><span class="smx-mono">' + esc(formatDateTime(e.ts || e.at)) + '</span>' +
                  '<span class="smx-activity-action">' + esc(e.action) + '</span>' +
                  '<span class="smx-cell-muted">' + esc(e.actor || '') + '</span></div>';
              }).join('')
            : '<div class="smx-cell-muted">No security audit events yet.</div>';

          openModal(
            root,
            'Activity & Audit History',
            row.name + ' · ' + ((row.account && row.account.username) || row.person_id),
            '<h3 class="smx-section-label">Recent Authentication Events</h3><div class="smx-activity">' + lh + '</div>' +
            '<h3 class="smx-section-label">Account Security Log</h3><div class="smx-activity">' + ah + '</div>',
            '<button type="button" class="smx-btn primary" data-modal-close>Done</button>',
            true
          );
        });
    }

    // ── Shared 3-step registration wizard ────────────────────────────────
    // The modal design lives in assets/js/ngis-register.js so all five admin
    // account directories render an identical, role-aware flow. This adapter
    // only supplies the directory context (role, API helpers, modal shell).
    function openThreeStepWizard(prefill) {
      if (!window.NGIS_REGISTER || typeof window.NGIS_REGISTER.open !== 'function') {
        toast(root, 'Registration component is unavailable. Please refresh the page.', 'bad');
        return;
      }
      var roleTitles = {
        student: 'Student', teacher: 'Teacher', staff: 'Staff Member',
        principal: 'Principal', admin: 'Administrator'
      };
      window.NGIS_REGISTER.open({
        cfg: cfg,
        roleTitle: roleTitles[cfg.type] || 'User',
        accountType: ROLES_BY_TYPE[cfg.type] || 'ADMIN',
        root: root,
        state: state,
        esc: esc,
        q: q,
        qa: qa,
        fetchJson: fetchJson,
        postJson: postJson,
        fetchDirectory: function () { load(); },
        openModal: function (title, subtitle, body, footer, wide, options) {
          return openModal(root, title, subtitle, body, footer, wide, options);
        },
        closeModal: function (force) { closeModal(root, force); },
        toast: function (message, tone) { toast(root, message, tone); }
      }, prefill || null);
    }

    var openAddAccountModal = openThreeStepWizard;

    function confirmBulkStatus(actionKey) {
      var ids = Object.keys(state.selected);
      var rows = ids.map(function (id) {
        return state.selectedRows[id] || state.rows.find(function (r) { return r.person_id === id; });
      }).filter(function (r) { return r && r.account; });
      if (!rows.length) {
        toast(root, 'Selected rows do not have provisioned login accounts yet.', 'bad');
        return;
      }
      var label = actionKey === 'activate' ? 'Activate Selected Accounts' : 'Suspend Selected Accounts';
      var isDanger = actionKey === 'suspend';
      var modal = openModal(
        root,
        label,
        rows.length + ' provisioned accounts selected',
        '<div class="smx-note-box' + (isDanger ? ' warn' : '') + '">' +
          (isDanger
            ? 'Selected accounts will be prevented from signing in. Institutional profile records are never removed.'
            : 'Selected accounts will become Active and allowed to sign in.') +
        '</div>',
        '<button type="button" class="smx-btn" data-modal-close>Cancel</button>' +
        '<button type="button" class="smx-btn ' + (isDanger ? 'danger' : 'primary') + '" data-bulk-st-go>' + esc(label) + '</button>'
      );
      q(modal, '[data-bulk-st-go]').addEventListener('click', function (e) {
        e.currentTarget.disabled = true;
        postJson('/api/user-mgmt/bulk-status', {
          person_type: cfg.type, person_ids: rows.map(function (r) { return r.person_id; }), action: actionKey
        }).then(function (j) {
          closeModal(root);
          var ok = (j.results || []).filter(function (r) { return r.ok; }).length;
          toast(root, label + ': ' + ok + ' updated.', ok ? undefined : 'bad');
          state.selected = {};
          state.selectedRows = {};
          load({ keepToolbar: true });
        });
      });
    }

    function openBulkModal() {
      var ids = Object.keys(state.selected);
      if (!ids.length) { toast(root, 'Select rows first to bulk provision.', 'bad'); return; }
      var rows = ids.map(function (id) {
        return state.selectedRows[id] || state.rows.find(function (r) { return r.person_id === id; });
      }).filter(Boolean);
      var ready = rows.filter(function (r) { return !r.account; });
      var already = rows.filter(function (r) { return r.account; });
      var modal = openModal(
        root,
        'Bulk Account Provisioning',
        cfg.title,
        '<p class="smx-note-box">' + ready.length + ' unlinked records will receive Pending Activation login accounts. ' +
          (already.length ? already.length + ' already provisioned will be skipped automatically.' : '') + '</p>' +
        '<div class="smx-activity smx-mt-sm">' + rows.map(function (r) {
          return '<div class="smx-activity-row">' +
            '<span class="smx-person" style="min-width:0;flex:1 1 auto">' +
              avatarHtml(r.name, r.photo, { size: 'sm' }) +
              '<span class="smx-person-meta"><span class="smx-person-name">' + esc(r.name) + '</span>' +
              '<span class="smx-person-id smx-mono">' + esc(r.person_id) + '</span></span>' +
            '</span>' +
            '<span class="smx-cell-muted">' + (r.account ? 'Already linked' : 'Ready') + '</span>' +
          '</div>';
        }).join('') + '</div>',
        '<button type="button" class="smx-btn" data-modal-close>Cancel</button>' +
        '<button type="button" class="smx-btn primary" data-bulk-confirm' + (ready.length ? '' : ' disabled') + '>Provision ' + ready.length + ' Accounts</button>'
      );
      q(modal, '[data-bulk-confirm]').addEventListener('click', function () {
        postJson('/api/user-mgmt/bulk-provision', {
          person_type: cfg.type, person_ids: ids, activation: 'token'
        }).then(function (j) {
          closeModal(root);
          var ok = (j.results || []).filter(function (r) { return r.ok; }).length;
          var fail = (j.results || []).length - ok;
          toast(root, 'Bulk provisioning: ' + ok + ' created' + (fail ? ', ' + fail + ' skipped.' : '.'));
          state.selected = {};
          state.selectedRows = {};
          load();
        });
      });
    }

    function openImportModal() {
      var body =
        '<p class="smx-note-box">Upload a CSV file containing an <span class="smx-mono">ID</span> column matching existing ' +
        esc(cfg.recordPlural) + '. Duplicate accounts and unknown IDs are rejected without altering existing records.</p>' +
        '<input type="file" id="smx-import-file" class="smx-input smx-mt-sm" accept=".csv,text/csv">' +
        '<div id="smx-import-preview" class="smx-mt-sm"></div>';
      var modal = openModal(
        root,
        'Import Provisioning List',
        cfg.title,
        body,
        '<button type="button" class="smx-btn" data-modal-close>Cancel</button>' +
        '<button type="button" class="smx-btn primary" data-import-confirm disabled>Provision Valid Records</button>'
      );
      var fileInput = q(modal, '#smx-import-file');
      var preview = q(modal, '#smx-import-preview');
      var confirmBtn = q(modal, '[data-import-confirm]');

      fileInput.addEventListener('change', function () {
        var file = fileInput.files && fileInput.files[0];
        if (!file) return;
        var reader = new FileReader();
        reader.onload = function () {
          var lines = String(reader.result).split(/\r?\n/).filter(Boolean);
          var header = (lines[0] || '').toLowerCase();
          var idIdx = header.split(',').findIndex(function (c) { return c.trim() === 'id'; });
          if (idIdx === -1) {
            preview.innerHTML = '<div class="smx-note-box warn">CSV must include an "ID" header column.</div>';
            confirmBtn.disabled = true;
            return;
          }
          var parsedIds = lines.slice(1).map(function (l) { return (l.split(',')[idIdx] || '').trim(); }).filter(Boolean);
          fetchJson('/api/user-mgmt/directory?type=' + encodeURIComponent(cfg.type) + '&page_size=200').then(function (j) {
            var all = j.data || [];
            var valid = parsedIds.filter(function (id) {
              var r = all.find(function (x) { return x.person_id === id; });
              return r && !r.account;
            });
            var dup = parsedIds.filter(function (id) {
              var r = all.find(function (x) { return x.person_id === id; });
              return r && r.account;
            });
            var unknown = parsedIds.filter(function (id) {
              return !all.find(function (x) { return x.person_id === id; });
            });
            preview.innerHTML = '<div class="smx-info-grid">' +
              '<div class="smx-info"><span class="smx-info-label">Ready</span><span>' + valid.length + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">Already Linked</span><span>' + dup.length + '</span></div>' +
              '<div class="smx-info"><span class="smx-info-label">Unknown IDs</span><span>' + unknown.length + '</span></div>' +
            '</div>';
            confirmBtn.disabled = !valid.length;
            confirmBtn.setAttribute('data-valid-ids', JSON.stringify(valid));
          });
        };
        reader.readAsText(file);
      });

      confirmBtn.addEventListener('click', function () {
        var valid = JSON.parse(confirmBtn.getAttribute('data-valid-ids') || '[]');
        if (!valid.length) return;
        postJson('/api/user-mgmt/bulk-provision', {
          person_type: cfg.type, person_ids: valid, activation: 'token'
        }).then(function (j) {
          closeModal(root);
          var ok = (j.results || []).filter(function (r) { return r.ok; }).length;
          toast(root, 'Import processed: ' + ok + '/' + valid.length + ' accounts created.', ok ? undefined : 'bad');
          load();
        });
      });
    }

    load();
  }

  function suppressDuplicateHamburger() {
    var heroBtn = document.getElementById('htbHamburger');
    var mq = window.matchMedia('(max-width: 767px)');
    function apply() {
      if (!heroBtn) return;
      if (mq.matches) heroBtn.style.setProperty('display', 'none', 'important');
      else heroBtn.style.removeProperty('display');
    }
    if (mq.addEventListener) mq.addEventListener('change', apply);
    else mq.addListener(apply);
    apply();
  }

  UM.init = function (containerId, module) {
    var root = document.getElementById(containerId);
    if (!root) return;
    var cfg = MODULES[module];
    if (!cfg) return;
    suppressDuplicateHamburger();
    renderDirectory(root, cfg);
    // The Admin Dashboard "Add User" button deep-links here with ?open=add.
    // Open the shared registration wizard through the exact same code path as
    // the toolbar Add Account action. A short retry loop makes this immune to
    // boot-order races (layout mount, auth bootstrap, async directory paint):
    // the first attempt usually succeeds; later attempts only fire if the
    // modal is still not present in the DOM.
    try {
      if (new URLSearchParams(window.location.search).get('open') === 'add') {
        var openAttempts = 0;
        (function tryOpenAdd() {
          openAttempts += 1;
          if (document.querySelector('.nrg-backdrop')) return; // wizard is open
          if (openAttempts > 20) return; // give up after ~6s; toolbar still works
          try {
            if (typeof openAddAccountModal === 'function') {
              openAddAccountModal(null);
            } else {
              var btn = root.querySelector('[data-action="add-account"]');
              if (btn && !btn.disabled) btn.click();
            }
          } catch (openErr) {
            if (window.console && console.warn) console.warn('[ngis-users] open=add attempt failed:', openErr);
          }
          if (!document.querySelector('.nrg-backdrop')) window.setTimeout(tryOpenAdd, 300);
        })();
      }
    } catch (e) { /* URLSearchParams unsupported: normal toolbar still works */ }
  };
})(window, document);
