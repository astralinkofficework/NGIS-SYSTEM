/**
 * NGIS — Roles & Access Control Workspace (v3.0)
 * ---------------------------------------------------------------------------
 * Vanilla JS. No framework. Every action is backed by a server endpoint in
 * roles_permissions_api.py / roles_permissions_ext.py. Nothing in this file
 * is an authorization decision: it renders server-computed state, edits draft
 * documents, and asks the backend to validate, preview and persist them.
 *
 * Tabs: Roles & Permissions | User Access & Visibility | Portal Access Control
 *       | Activity Audit Log
 *
 * Legacy endpoint references are retained as real fallbacks:
 *   /api/roles-mgmt/registry, /api/roles-mgmt/users,
 *   /api/roles-mgmt/preview, /api/roles-mgmt/overrides/
 */
(function (window, document) {
  'use strict';

  var R = window.NGIS_ROLES = window.NGIS_ROLES || {};
  R.version = '3.0';

  var S = {
    tab: 'roles', root: null, busy: false, busyLabel: '', toast: null, modal: null,
    boot: null, registry: { categories: [], actions: [], action_labels: {}, core_roles: [] },
    authority: {}, roles: { core_roles: [], custom_roles: [] }, overview: {},
    pages: { portals: {}, total: 0 }, definitions: { custom: [], enforced_pairs: [] },
    permInventory: null, bindings: [], rolePortals: { portals: [], configs: {} },
    campuses: [], protectedPortals: [], categories: [],
    selectedRoleId: 'ADMIN', rolePerms: null, roleMembers: null,
    permDraft: null, permDirty: false, customKeys: [], rolePortalDraft: null,
    selectedPortalRole: '', portalMode: 'role',
    selectedUser: null, overrides: null, draft: null, effective: null, preview: null,
    userRoles: null,
    users: [], userTotal: 0, userOffset: 0, userHasMore: false,
    userQ: '', userRole: 'ALL', userCampus: 'ALL', userLimit: 10,
    pagePortal: 'admin', pageSearch: '', showAllActions: false,
    auditRows: [], auditTotal: 0, auditActions: [], auditPage: 1, auditPageSize: 20,
    auditAction: '', auditSearch: '',
    compareA: '', compareB: '', compareResult: null,
    assignQ: '', assignRoleId: '', assignUsers: [],
    roleSearch: '',
    ngxOpen: {}, ngxLimits: { dir: 5, rev: 5, members: 5, restricted: 5, defs: 6, sources: 8 },
    portalLabels: {
      admin: 'Admin Portal', principal: 'Principal Portal', teacher: 'Teacher Portal',
      student: 'Student Portal', staff: 'Staff Portal', superadmin: 'Super Admin Portal'
    },
    portalIcons: {
      admin: 'admin_panel_settings', principal: 'account_balance', teacher: 'co_present',
      student: 'school', staff: 'badge', superadmin: 'security'
    }
  };

  var INIT = { dir: 5, rev: 5, members: 5, restricted: 5, defs: 6, sources: 8 };
  var STEP = 5;
  var SENSITIVE = {
    'roles-access': ['manage'], 'login-security': ['manage'],
    'user-management': ['manage'], 'system-configuration': ['manage'],
    'account-directories': ['manage', 'delete'], 'grades': ['approve', 'publish']
  };
  var TRI = ['inherit', 'allow', 'deny'];
  var VIS = ['inherit', 'visible', 'hidden'];

  /* ------------------------------------------------------------------ util */
  function esc(v) {
    return String(v === undefined || v === null ? '' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function ic(name, cls) {
    return '<span class="material-symbols-outlined' + (cls ? ' ' + cls : '') +
      '" aria-hidden="true">' + esc(name) + '</span>';
  }
  var SVG = {
    plus: '<path d="M12 5v14M5 12h14"/>',
    key: '<path d="M15 7a4 4 0 1 0-3.7 5.7L9 15H7v2H5v2H2v-3l7.3-7.3A4 4 0 0 0 15 7Z"/><circle cx="15.5" cy="7.5" r="1.2"/>',
    users: '<path d="M16 19v-1.5a3.5 3.5 0 0 0-3.5-3.5h-5A3.5 3.5 0 0 0 4 17.5V19"/><circle cx="10" cy="8" r="3"/><path d="M20 19v-1.5a3.5 3.5 0 0 0-2.6-3.4M15.5 5.2a3 3 0 0 1 0 5.6"/>',
    compare: '<path d="M4 6h7M4 12h4M4 18h7M16 4v16M13 17l3 3 3-3M20 6h-7M20 12h-4M20 18h-7"/>',
    shield: '<path d="M12 3 4 6v6c0 4.4 3.4 8 8 9 4.6-1 8-4.6 8-9V6l-8-3Z"/>',
    check: '<path d="m5 12 4.5 4.5L19 7"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>'
  };
  function svg(name, size) {
    return '<svg class="rp-svg" width="' + (size || 15) + '" height="' + (size || 15) +
      '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" ' +
      'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      (SVG[name] || SVG.plus) + '</svg>';
  }
  function clone(o) { return JSON.parse(JSON.stringify(o === undefined ? null : o)); }
  function actor() {
    try {
      var u = null;
      if (window.NGISAuth && typeof window.NGISAuth.getUser === 'function') u = window.NGISAuth.getUser();
      if (!u) u = JSON.parse(window.localStorage.getItem('ngis_user') || 'null');
      if (!u) u = JSON.parse(window.localStorage.getItem('auth_user') || 'null');
      var v = u && (u.email || u.username);
      return v ? String(v).trim().toLowerCase() : '';
    } catch (e) { return ''; }
  }
  function api(path, method, body) {
    var opts = { method: method || 'GET', headers: { 'X-Actor': actor() } };
    if (body !== undefined) {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(body);
    }
    return window.fetch(path, opts).then(function (r) {
      return r.json().then(function (j) {
        if (!r.ok || j.success === false) {
          var err = new Error(j.error || ('Request failed (' + r.status + ')'));
          err.status = r.status;
          err.payload = j;
          throw err;
        }
        return j;
      });
    });
  }
  function notify(msg, bad) {
    S.toast = { msg: msg, bad: !!bad };
    render();
    window.setTimeout(function () {
      if (S.toast && S.toast.msg === msg) { S.toast = null; render(); }
    }, 4600);
  }
  function status(label, tone) {
    return '<span class="rp-status ' + esc(tone || 'neutral') + '">' + esc(label) + '</span>';
  }
  function actionLabel(a) { return (S.registry.action_labels || {})[a] || a; }
  function portalName(k) { return S.portalLabels[k] || k; }
  function busy(on, label) { S.busy = !!on; S.busyLabel = label || 'Saving…'; render(); }
  function withBusy(p, okMsg) {
    busy(true);
    return p.then(function (r) {
      S.busy = false;
      if (okMsg) notify(okMsg); else render();
      return r;
    }).catch(function (err) {
      S.busy = false;
      if (S.modal) { S.modal.error = err.message; }
      notify(err.message, true);
      render();
      throw err;
    });
  }

  /* --------------------------------------------------------------- rendering */
  function render(keepFocus) {
    if (!S.root) return;
    var active = document.activeElement;
    var fid = active && active.id;
    var start = null, end = null;
    try { if (active && active.setSelectionRange) { start = active.selectionStart; end = active.selectionEnd; } } catch (e) {}

    var h = ['<div class="ngis-rp rp-v3">'];
    h.push(renderTopbar());
    h.push('<div class="rp-tabs" role="tablist" aria-label="Roles & Access Control sections">');
    [['roles', 'Roles & Permissions'], ['access', 'User Access & Visibility'],
      ['portals', 'Portal Access Control'], ['activity', 'Activity Audit Log']].forEach(function (t) {
      h.push('<button type="button" class="rp-tab" role="tab" data-act="tab" data-tab="' + t[0] + '"' +
        ' aria-selected="' + (S.tab === t[0] ? 'true' : 'false') + '">' + t[1] + '</button>');
    });
    h.push('</div>');
    h.push('<div role="tabpanel">');
    if (S.tab === 'roles') h.push(renderRoles());
    else if (S.tab === 'access') h.push(renderAccess());
    else if (S.tab === 'portals') h.push(renderPortals());
    else h.push(renderActivity());
    h.push('</div>');
    if (S.modal) h.push(renderModal());
    if (S.toast) h.push('<div class="rp-toast' + (S.toast.bad ? ' bad' : '') +
      '" role="status">' + esc(S.toast.msg) + '</div>');
    h.push('</div>');
    S.root.innerHTML = h.join('');

    // Hoist the dialog out of the page root. The global hero/topbar and the
    // mobile app bar are siblings of #rolesRoot with their own stacking
    // contexts; a scrim left inside the root cannot blur or dim them and can
    // be clipped by the root's overflow. This mirrors NGIS_MODAL.open(), which
    // always reparents the backdrop to document.body.
    if (S.modalEl && S.modalEl.parentNode) S.modalEl.parentNode.removeChild(S.modalEl);
    S.modalEl = null;
    if (S.modal) {
      var scrim = S.root.querySelector('.rp-modal-scrim');
      if (scrim) {
        // Keep the .ngis-rp.rp-v3 scope on the scrim itself so the v3 theme
        // variables and all descendant rules still resolve after reparenting.
        scrim.classList.add('ngis-rp', 'rp-v3', 'rp-v3-scrim');
        document.body.appendChild(scrim);
        S.modalEl = scrim;
        scrim.addEventListener('click', onClick);
        scrim.addEventListener('change', onChange);
        scrim.addEventListener('input', onInput);
      }
    }

    document.body.classList[S.modal ? 'add' : 'remove']('ngis-modal-open');
    if (S.modal && !keepFocus) {
      var target = (S.modalEl || S.root).querySelector('[data-modal-focus]');
      if (target) { try { target.focus(); } catch (e) {} }
    }
    if (keepFocus && fid) {
      var el = document.getElementById(fid);
      if (el) {
        el.focus();
        try { if (start !== null) el.setSelectionRange(start, end); } catch (e) {}
      }
    }
  }

  function renderTopbar() {
    var a = S.authority || {};
    var h = ['<div class="rp-topbar">'];
    h.push('<div class="rp-topbar-left"><div class="rp-topbar-title">Roles &amp; Access Control</div>');
    h.push('<div class="rp-topbar-meta">' + esc(a.explanation || 'Loading authority…') + '</div></div>');
    h.push('<div class="rp-topbar-actions">');
    h.push('<button type="button" class="rp-btn primary sm" data-act="role-new"' +
      (a.can_create_roles === false ? ' disabled title="Not authorized"' : '') + '>' +
      svg('plus') + 'Add New Role</button>');
    h.push('<button type="button" class="rp-btn secondary sm" data-act="permission-new"' +
      (a.can_manage_permissions === false ? ' disabled' : '') + '>' + svg('key') + 'Add Permission</button>');
    h.push('<button type="button" class="rp-btn secondary sm" data-act="assignments">' +
      svg('users') + 'Manage Assignments</button>');
    var isCompareOpen = S.modal && S.modal.type === 'compare';
    h.push('<button type="button" class="rp-btn secondary sm rp-btn-compare' + (isCompareOpen ? ' is-active' : '') + '" data-act="compare-open" aria-expanded="' + (isCompareOpen ? 'true' : 'false') + '" title="Compare permissions between two roles">' +
      svg('compare') + 'Compare</button>');
    h.push('</div></div>');
    return h.join('');
  }

  function kpi(label, value) {
    return '<div class="rp-kpi"><div class="rp-kpi-label">' + esc(label) +
      '</div><div class="rp-kpi-value">' + esc(value) + '</div></div>';
  }
  function cardHead(title, sub, actions) {
    return '<div class="rp-card-head"><div><div class="rp-card-title">' + title + '</div>' +
      (sub ? '<div class="rp-card-sub">' + esc(sub) + '</div>' : '') + '</div>' +
      (actions ? '<div class="rp-card-actions">' + actions + '</div>' : '') + '</div>';
  }

  /* ------------------------------------------------------- ngx expandable UI */
  function limit(scope) {
    var v = S.ngxLimits[scope];
    var init = INIT[scope] || 5;
    return (typeof v === 'number' && v >= init) ? v : init;
  }
  function moreBar(scope, total, unit) {
    var init = INIT[scope] || 5;
    var lim = limit(scope);
    if (total <= init) return '';
    var h = ['<div class="ngx-more-bar" role="group" aria-label="Expand ' + esc(unit) + ' list">'];
    if (lim > init) h.push('<button type="button" class="ngx-btn-more" data-act="ngx-less" data-scope="' +
      esc(scope) + '" aria-expanded="true">' + ic('expand_less') + 'Show less</button>');
    if (total > lim) h.push('<button type="button" class="ngx-btn-more" data-act="ngx-more" data-scope="' +
      esc(scope) + '" aria-expanded="false">' + ic('expand_more') + 'Show more (' + (total - lim) + ')</button>');
    h.push('<span class="ngx-count">Showing ' + Math.min(lim, total) + ' of ' + total + '</span></div>');
    return h.join('');
  }
  function preview(scope, rows, rowFn, unit, emptyHtml) {
    if (!rows.length) return emptyHtml || '';
    return rows.slice(0, limit(scope)).map(rowFn).join('') + moreBar(scope, rows.length, unit || 'items');
  }
  function clamp(text, key) {
    var t = String(text == null ? '' : text);
    if (t.length <= 180) return '<span class="rp-clamp-text">' + esc(t) + '</span>';
    var open = !!S.ngxOpen['txt-' + key];
    return '<span class="ngx-clamp-wrap"><span class="ngx-clamp' + (open ? ' is-open' : '') +
      '" id="ngx-txt-' + esc(key) + '">' + esc(t) + '</span>' +
      '<button type="button" class="ngx-btn-more inline" data-act="ngx-toggle-text" data-key="' + esc(key) +
      '" aria-expanded="' + open + '" aria-controls="ngx-txt-' + esc(key) + '">' +
      ic(open ? 'expand_less' : 'expand_more') + (open ? 'Show less' : 'Show more') + '</button></span>';
  }
  function groupOpen(key, def) { return S.ngxOpen[key] !== undefined ? !!S.ngxOpen[key] : !!def; }
  function catOpen(cat, idx) { return groupOpen('matrix-' + cat, idx === 0); }

  /* ------------------------------------------------------------------ roles */
  function allRoles() {
    return (S.roles.core_roles || []).concat(S.roles.custom_roles || []);
  }
  function currentRole() {
    return allRoles().filter(function (r) { return r.id === S.selectedRoleId; })[0] || null;
  }
  function visibleRoles() {
    var list = allRoles();
    if (S.roleSearch) {
      var q = S.roleSearch.toLowerCase();
      list = list.filter(function (r) {
        return (r.name + ' ' + (r.description || '') + ' ' + (r.identifier || '')).toLowerCase().indexOf(q) !== -1;
      });
    }
    var lim = limit('dir');
    var shown = list.slice(0, lim);
    var selected = list.filter(function (r) { return r.id === S.selectedRoleId; })[0];
    if (selected && shown.indexOf(selected) === -1) shown = shown.concat([selected]);
    return { shown: shown, total: list.length };
  }

  function renderRoles() {
    var m = S.overview.metrics || {};
    var t = (S.boot && S.boot.totals) || {};
    var h = [];
    h.push('<div class="rp-kpis">');
    h.push(kpi('Total Roles', t.total_roles !== undefined ? t.total_roles : allRoles().length));
    h.push(kpi('Custom Roles', t.custom_roles !== undefined ? t.custom_roles : (S.roles.custom_roles || []).length));
    h.push(kpi('Role Assignments', m.totalAssignments !== undefined ? m.totalAssignments : 0));
    h.push(kpi('High Privilege', m.highPrivilegeRoles !== undefined ? m.highPrivilegeRoles : 0));
    h.push('</div>');

    h.push('<div class="rp-grid">');
    /* ---- left: role directory ---- */
    h.push('<aside class="rp-card rp-directory">');
    h.push(cardHead(ic('shield') + 'Role Directory', allRoles().length + ' roles'));
    h.push('<div class="rp-card-body rp-dir-tools"><div class="rp-field">' +
      '<label for="rpRoleSearch">Find a role</label>' +
      '<input class="rp-input" id="rpRoleSearch" data-act="role-search" placeholder="Name or identifier" value="' +
      esc(S.roleSearch) + '"></div></div>');
    var vr = visibleRoles();
    h.push('<div class="rp-card-body tight"><div class="rp-list">');
    if (!vr.shown.length) h.push('<div class="rp-empty">No roles match this search.</div>');
    vr.shown.forEach(function (r) {
      var core = !!r.protected;
      h.push('<button type="button" class="rp-list-item' + (S.selectedRoleId === r.id ? ' is-active' : '') +
        '" data-act="role-select" data-id="' + esc(r.id) + '" aria-pressed="' +
        (S.selectedRoleId === r.id) + '">' +
        '<div class="rp-list-name"><span>' + esc(r.name) + '</span>' +
        (core ? '<span class="rp-plain-tag">Protected</span>'
              : '<span class="rp-plain-tag ' + (r.status === 'active' ? 'ok' : 'warn') + '">' +
                esc(r.status === 'active' ? 'Active' : 'Archived') + '</span>') + '</div>' +
        '<div class="rp-list-meta">' + esc(r.module_count || 0) + ' modules &middot; ' +
        esc(r.action_count || 0) + ' actions &middot; ' + esc(r.members || 0) + ' members</div>' +
        (r.description ? '<div class="rp-list-desc">' + clamp(r.description, 'role-' + r.id) + '</div>' : '') +
        '</button>');
    });
    h.push('</div>' + moreBar('dir', vr.total, 'roles') + '</div></aside>');

    /* ---- right: permission configuration ---- */
    var role = currentRole();
    h.push('<section class="rp-card rp-workspace">');
    if (!role) {
      h.push('<div class="rp-empty">Select a role to inspect its permission matrix.</div>');
    } else {
      h.push(renderRoleDetail(role));
    }
    h.push('</section></div>');
    return h.join('');
  }

  function renderRoleDetail(role) {
    var core = !!role.protected;
    var h = [];
    var acts = [];
    if (S.authority.can_manage_permissions !== false) {
      if (!core) {
        acts.push('<button type="button" class="rp-btn sm" data-act="role-edit">Edit</button>');
        acts.push('<button type="button" class="rp-btn sm" data-act="role-duplicate">Duplicate</button>');
        acts.push('<button type="button" class="rp-btn sm" data-act="role-assign">Assign Users</button>');
        acts.push('<button type="button" class="rp-btn sm" data-act="role-archive">' +
          (role.status === 'active' ? 'Disable' : 'Enable') + '</button>');
        acts.push('<button type="button" class="rp-btn sm danger" data-act="role-delete">Delete</button>');
      }
    }
    h.push(cardHead(ic('tune') + esc(role.name),
      (core ? 'Protected system role' : 'Custom role') + ' &middot; ' + esc(role.id) +
      (role.identifier ? ' &middot; ' + esc(role.identifier) : ''), acts.join('')));

    h.push('<div class="rp-card-body">');
    h.push('<div class="rp-note' + (core ? ' warn' : '') + '">' +
      (core
        ? 'Core system roles are protected institutional identities. This matrix is read-only and reflects the authoritative server-side baseline. To create an editable variant, use Duplicate on a custom role or Add New Role.'
        : 'Configure the permission matrix and click Save permissions. View is required before any other action. Unsupported actions are shown as unavailable. Sensitive changes require confirmation and every save is versioned in the audit log.') +
      '</div>');
    if (!core && (role.description || role.category || role.default_portal)) {
      h.push('<div class="rp-facts">');
      if (role.description) h.push('<div><span>Description</span>' + clamp(role.description, 'detail-' + role.id) + '</div>');
      h.push('<div><span>Category</span>' + esc(role.category || 'custom') + '</div>');
      h.push('<div><span>Default portal</span>' + esc(role.default_portal ? portalName(role.default_portal) : 'Inherited') + '</div>');
      h.push('<div><span>Last updated</span>' + esc(role.updated_at || '—') + '</div>');
      h.push('</div>');
    }
    h.push('</div>');

    /* ---- permission matrix ---- */
    h.push('<div class="rp-section">');
    h.push('<div class="rp-section-head"><div><div class="rp-section-title">Module Permission Matrix</div>' +
      '<div class="rp-section-sub">' + (S.registry.categories || []).length + ' categories &middot; ' +
      (S.registry.actions || []).length + ' registered actions &middot; ' +
      esc((S.boot && S.boot.totals && S.boot.totals.enforced_bindings) || 0) +
      ' backend-enforced API bindings</div></div></div>');
    var perms = (core ? (S.rolePerms && S.rolePerms.permissions) : S.permDraft) || {};
    var actions = S.registry.actions || [];
    (S.registry.categories || []).forEach(function (cat, ci) {
      var key = 'matrix-' + cat.category;
      var open = catOpen(cat.category, ci);
      var grantedCount = cat.modules.reduce(function (n, mod) {
        return n + ((perms[mod.id] || []).length);
      }, 0);
      h.push('<details class="rp-cat ngx-matrix-group" data-ngx-key="' + esc(key) + '"' + (open ? ' open' : '') + '>');
      h.push('<summary><span class="ngx-sum-title">' + ic('folder_open') + esc(cat.category) + '</span>' +
        '<span class="ngx-sum-meta">' + cat.modules.length + ' modules &middot; ' + grantedCount + ' grants' +
        (!core ? '<span class="ngx-sum-actions">' +
          '<button type="button" class="rp-btn sm" data-act="cat-select-all" data-category="' + esc(cat.category) + '">Select all</button>' +
          '<button type="button" class="rp-btn sm" data-act="cat-clear" data-category="' + esc(cat.category) + '">Clear</button>' +
          '</span>' : '') + '</span></summary>');
      /* desktop table */
      h.push('<div class="rp-desktop-only rp-matrix-scroll"><table class="rp-matrix"><thead><tr>' +
        '<th class="rp-col-module">Module</th>');
      actions.forEach(function (a) { h.push('<th>' + esc(actionLabel(a)) + '</th>'); });
      h.push('</tr></thead><tbody>');
      cat.modules.forEach(function (mod) {
        var granted = perms[mod.id] || [];
        h.push('<tr><th class="rp-col-module"><span>' + esc(mod.name) + '</span>' +
          '<small>' + esc(mod.id) + '</small></th>');
        actions.forEach(function (a) {
          var supported = mod.actions.indexOf(a) !== -1;
          var checked = granted.indexOf(a) !== -1;
          h.push('<td>' + (supported
            ? '<input class="rp-check" type="checkbox" data-kind="perm" data-key="' + esc(mod.id) +
              '" data-module="' + esc(mod.id) + '" data-action="' + esc(a) + '" aria-label="' +
              esc(mod.name + ' ' + actionLabel(a)) + '"' + (checked ? ' checked' : '') +
              (core ? ' disabled' : '') + '>'
            : '<span class="rp-unavailable" title="Unsupported action">&mdash;</span>') + '</td>');
        });
        h.push('</tr>');
      });
      h.push('</tbody></table></div>');
      /* mobile module detail */
      h.push('<div class="rp-mobile-only rp-modules">');
      cat.modules.forEach(function (mod) {
        var granted = perms[mod.id] || [];
        var mk = 'mod-' + mod.id;
        h.push('<details class="rp-mod" data-ngx-key="' + esc(mk) + '"' +
          (groupOpen(mk, false) ? ' open' : '') + '><summary><span>' + esc(mod.name) + '</span>' +
          '<span class="ngx-sum-meta">' + granted.length + ' granted</span></summary>');
        h.push('<div class="rp-mod-actions">');
        mod.actions.forEach(function (a) {
          var checked = granted.indexOf(a) !== -1;
          h.push('<label class="rp-mod-action"><span>' + esc(actionLabel(a)) + '</span>' +
            '<input class="rp-check" type="checkbox" data-kind="perm" data-key="' + esc(mod.id) +
            '" data-module="' + esc(mod.id) + '" data-action="' + esc(a) + '"' +
            (checked ? ' checked' : '') + (core ? ' disabled' : '') + '></label>');
        });
        actions.filter(function (a) { return mod.actions.indexOf(a) === -1; }).forEach(function (a) {
          h.push('<div class="rp-mod-action is-unsupported"><span>' + esc(actionLabel(a)) + '</span>' +
            '<span class="rp-unavailable">&mdash;</span></div>');
        });
        h.push('</div></details>');
      });
      h.push('</div></details>');
    });
    if (!core) {
      var changes = permDiff();
      h.push('<div class="rp-savebar">' +
        '<span class="rp-muted">' + (S.permDirty ? changes.added.length + changes.removed.length +
          ' pending change(s)' : 'No unsaved changes') + '</span>' +
        '<div class="rp-card-actions">' +
        '<button type="button" class="rp-btn" data-act="perm-reset"' + (S.permDirty ? '' : ' disabled') +
        '>Discard changes</button>' +
        '<button type="button" class="rp-btn primary" data-act="perm-save"' +
        ((S.busy || !S.permDirty) ? ' disabled' : '') + '>' +
        (S.busy ? esc(S.busyLabel) : 'Save permissions') + '</button></div></div>');
    }
    h.push('</div>');

    /* ---- custom permission definitions ---- */
    h.push(renderDefinitions());

    /* ---- role portal access ---- */
    if (!core) h.push(renderRolePortals(role));

    /* ---- revisions ---- */
    var revisions = ((S.rolePerms && S.rolePerms.revisions) || []).slice().reverse();
    h.push('<div class="rp-section"><div class="rp-section-title">Revision History</div>' +
      '<div class="rp-section-sub">Previous permission configurations can be restored safely.</div>');
    if (!revisions.length) h.push('<div class="rp-muted rp-small">No revisions recorded for this role.</div>');
    else {
      h.push('<div class="rp-table-scroll"><table class="rp-table"><thead><tr><th>Revision</th>' +
        '<th>Timestamp</th><th>Actor</th><th>Modules</th><th></th></tr></thead><tbody>');
      h.push(preview('rev', revisions, function (rv) {
        return '<tr><td class="rp-mono">#' + esc(rv.index) + '</td><td>' + esc(rv.ts) + '</td><td>' +
          esc(rv.actor) + '</td><td class="rp-mono">' + esc(rv.module_count) + '</td>' +
          '<td class="right">' + (core ? '' : '<button type="button" class="rp-btn sm" data-act="perm-rollback" data-index="' +
            esc(rv.index) + '">Restore</button>') + '</td></tr>';
      }, 'revisions'));
      h.push('</tbody></table></div>');
    }
    h.push('</div>');

    /* ---- members ---- */
    var members = (S.roleMembers && S.roleMembers.members) || [];
    h.push('<div class="rp-section"><div class="rp-section-title">Assigned Members</div>' +
      '<div class="rp-section-sub">' + members.length + ' account(s) hold this ' +
      (core ? 'core identity' : 'custom role') + '.</div>');
    if (!members.length) h.push('<div class="rp-muted rp-small">No members assigned.</div>');
    else {
      h.push('<div class="rp-table-scroll"><table class="rp-table"><thead><tr><th>Name</th>' +
        '<th>Username</th><th>Type</th><th>Campus</th><th></th></tr></thead><tbody>');
      h.push(preview('members', members, function (u) {
        return '<tr><td>' + esc(u.name) + '</td><td>' + esc(u.username) + '</td><td>' +
          esc(u.person_type || u.current_role || '') + '</td><td>' + esc(u.campus || '') + '</td>' +
          '<td class="right">' + (!core ? '<button type="button" class="rp-btn sm" data-act="member-remove" data-username="' +
            esc(u.username) + '">Remove</button>' : '') + '</td></tr>';
      }, 'members'));
      h.push('</tbody></table></div>');
    }
    if (!core) h.push('<div class="rp-card-actions" style="margin-top:12px">' +
      '<button type="button" class="rp-btn" data-act="role-assign">' + svg('users') + 'Manage assignments</button></div>');
    h.push('</div>');
    return h.join('');
  }

  function permDiff() {
    var before = (S.rolePerms && S.rolePerms.permissions) || {};
    var after = S.permDraft || {};
    var added = [], removed = [];
    var mods = {};
    Object.keys(before).forEach(function (m) { mods[m] = 1; });
    Object.keys(after).forEach(function (m) { mods[m] = 1; });
    Object.keys(mods).forEach(function (m) {
      var b = before[m] || [], a = after[m] || [];
      a.filter(function (x) { return b.indexOf(x) === -1; }).forEach(function (x) {
        added.push({ module: m, action: x });
      });
      b.filter(function (x) { return a.indexOf(x) === -1; }).forEach(function (x) {
        removed.push({ module: m, action: x });
      });
    });
    return { added: added, removed: removed };
  }

  function renderDefinitions() {
    var defs = S.definitions.custom || [];
    var h = ['<div class="rp-section"><div class="rp-section-head"><div>' +
      '<div class="rp-section-title">Custom Permission Definitions</div>' +
      '<div class="rp-section-sub">Definitions without a backend enforcement binding are marked ' +
      'Requires Integration and cannot be granted. Creating a definition never creates a security bypass.</div>' +
      '</div><button type="button" class="rp-btn sm" data-act="permission-new">' + svg('plus') +
      'Add Permission</button></div>'];
    if (!defs.length) h.push('<div class="rp-muted rp-small">No custom permission definitions yet.</div>');
    else {
      h.push('<div class="rp-def-list">');
      h.push(preview('defs', defs, function (d) {
        return '<div class="rp-def-row"><div class="rp-def-main">' +
          '<div class="rp-def-name">' + esc(d.name) + ' <span class="rp-plain-tag ' +
          (d.enforceable ? 'ok' : 'warn') + '">' + (d.enforceable ? 'Enforced' : 'Requires Integration') +
          '</span></div>' +
          '<div class="rp-def-meta"><code>' + esc(d.key) + '</code> &middot; ' + esc(d.module_label || d.module) +
          ' &middot; ' + esc(d.action_label) + ' &middot; ' + esc(portalName(d.portal)) +
          ' &middot; ' + esc(d.scope_label) + (d.target_page ? ' &middot; ' + esc(d.target_page) : '') + '</div>' +
          (d.description ? '<div class="rp-def-desc">' + esc(d.description) + '</div>' : '') +
          '</div><div class="rp-def-actions">' +
          '<button type="button" class="rp-btn sm" data-act="permission-edit" data-key="' + esc(d.key) + '">Edit</button>' +
          '<button type="button" class="rp-btn sm danger" data-act="permission-delete" data-key="' + esc(d.key) + '">Delete</button>' +
          '</div></div>';
      }, 'definitions'));
      h.push('</div>');
    }
    h.push('</div>');
    return h.join('');
  }

  function renderRolePortals(role) {
    var ports = S.rolePortals.portals || [];
    var draft = S.rolePortalDraft || (role.portals || []);
    var h = ['<div class="rp-section"><div class="rp-section-title">Role Portal Access</div>' +
      '<div class="rp-section-sub">Portal grants are resolved server-side together with the account type ' +
      'and per-account overrides. A page permission never grants an entire portal. ' +
      'Protected portals require SUPER_ADMIN authority.</div>'];
    h.push('<div class="rp-portal-grid">');
    ports.forEach(function (p) {
      var checked = draft.indexOf(p.id) !== -1;
      var locked = p.protected && S.authority.can_configure_protected_portals === false;
      h.push('<label class="rp-portal-check' + (locked ? ' is-locked' : '') + '">' +
        '<input type="checkbox" data-kind="roleportal" data-value="' + esc(p.id) + '"' +
        (checked ? ' checked' : '') + (locked ? ' disabled' : '') + '>' +
        '<span>' + ic(S.portalIcons[p.id] || 'hub') + esc(p.label) + '</span>' +
        (p.protected ? '<span class="rp-plain-tag">Protected</span>' : '') + '</label>');
    });
    h.push('</div>');
    h.push('<div class="rp-card-actions" style="margin-top:12px">' +
      '<button type="button" class="rp-btn primary" data-act="role-portals-save"' + (S.busy ? ' disabled' : '') +
      '>Save Portal Access</button></div></div>');
    return h.join('');
  }

  /* ------------------------------------------------------------ user access */
  function emptyDraft() { return { portals: {}, pages: {}, actions: {} }; }
  function setTri(kind, key, action, value, visibility) {
    var d = S.draft || (S.draft = emptyDraft());
    if (kind === 'portal') {
      if (value === 'inherit') delete d.portals[key]; else d.portals[key] = value;
    } else if (kind === 'page') {
      var rule = d.pages[key] || { visibility: 'inherit', access: 'inherit' };
      if (visibility) rule.visibility = value; else rule.access = value;
      if (rule.visibility === 'inherit' && rule.access === 'inherit') delete d.pages[key];
      else d.pages[key] = rule;
    } else if (kind === 'action') {
      var mod = d.actions[key] || {};
      if (value === 'inherit') delete mod[action]; else mod[action] = value;
      if (Object.keys(mod).length) d.actions[key] = mod; else delete d.actions[key];
    }
    S.preview = null;
  }
  function triSelect(kind, key, action, value, options, isVisibility) {
    var map = options === VIS
      ? { inherit: 'Inherit', visible: 'Visible', hidden: 'Hidden' }
      : { inherit: 'Inherit', allow: 'Allow', deny: 'Deny' };
    var h = ['<select class="rp-tri" data-kind="' + kind + '" data-key="' + esc(key) + '"'];
    if (action) h.push(' data-action="' + esc(action) + '"');
    if (isVisibility) h.push(' data-visibility="1"');
    h.push(' data-state="' + esc(value) + '" aria-label="' +
      esc(isVisibility ? 'Page visibility' : (kind === 'portal' ? 'Portal access' : 'Action permission')) +
      ' for ' + esc(key) + '">');
    options.forEach(function (o) {
      h.push('<option value="' + o + '"' + (o === value ? ' selected' : '') + '>' + map[o] + '</option>');
    });
    return h.join('') + '</select>';
  }
  function draftSize() {
    if (!S.draft) return 0;
    return Object.keys(S.draft.portals || {}).length + Object.keys(S.draft.pages || {}).length +
      Object.keys(S.draft.actions || {}).length;
  }

  function renderUserDirectory(mode) {
    var h = ['<aside class="rp-card rp-directory">'];
    h.push(cardHead(ic('group') + (mode === 'portals' ? 'Select Account' : 'User Directory'),
      S.userTotal + ' accounts'));
    h.push('<div class="rp-card-body rp-dir-tools">');
    h.push('<div class="rp-field"><label for="rpUserSearch">Search accounts</label>' +
      '<input class="rp-input" id="rpUserSearch" data-act="user-search" placeholder="Name, ID, role, campus" value="' +
      esc(S.userQ) + '"></div>');
    h.push('<div class="rp-filter-row"><select class="rp-tri" id="rpUserRole" data-act="user-role" aria-label="Filter by role">' +
      [['ALL', 'All roles'], ['STUDENT', 'Students'], ['TEACHER', 'Teachers'], ['STAFF', 'Staff'],
       ['PRINCIPAL', 'Principals'], ['ADMIN', 'Admins'], ['SUPER_ADMIN', 'Super Admins']].map(function (o) {
        return '<option value="' + o[0] + '"' + (S.userRole === o[0] ? ' selected' : '') + '>' + o[1] + '</option>';
      }).join('') + '</select>');
    h.push('<select class="rp-tri" id="rpUserCampus" data-act="user-campus" aria-label="Filter by campus">' +
      '<option value="ALL">Every campus (no filter)</option>' +
      S.campuses.map(function (c) {
        return '<option value="' + esc(c) + '"' + (S.userCampus.toLowerCase() === String(c).toLowerCase() ? ' selected' : '') + '>' +
          esc(c) + '</option>';
      }).join('') + '</select></div></div>');
    h.push('<div class="rp-card-body tight"><div class="rp-list">');
    if (!S.users.length) h.push('<div class="rp-empty">No matching accounts found.</div>');
    S.users.forEach(function (u) {
      h.push('<button type="button" class="rp-list-item' + (S.selectedUser === u.username ? ' is-active' : '') +
        '" data-act="user-select" data-username="' + esc(u.username) + '" aria-pressed="' +
        (S.selectedUser === u.username) + '">' +
        '<div class="rp-list-name"><span>' + esc(u.name || u.username) + '</span>' +
        (u.has_overrides ? '<span class="rp-plain-tag warn">Overrides</span>' : '') + '</div>' +
        '<div class="rp-list-meta">' + esc(u.username) + ' &middot; ' + esc(u.role) +
        (u.campus ? ' &middot; ' + esc(u.campus) : '') + '</div></button>');
    });
    h.push('</div>');
    if (S.userHasMore || S.users.length > S.userLimit) {
      h.push('<div class="ngx-more-bar">' +
        (S.users.length > S.userLimit ? '<button type="button" class="ngx-btn-more" data-act="user-less">' +
          ic('expand_less') + 'Show less</button>' : '') +
        (S.userHasMore ? '<button type="button" class="ngx-btn-more" data-act="user-more">' +
          ic('expand_more') + 'Show more (' + (S.userTotal - S.users.length) + ')</button>' : '') +
        '<span class="ngx-count">Showing ' + S.users.length + ' of ' + S.userTotal + '</span></div>');
    }
    h.push('</div></aside>');
    return h.join('');
  }

  function renderAccess() {
    var h = ['<div class="rp-grid">', renderUserDirectory('access'), '<section class="rp-card rp-workspace">'];
    if (!S.selectedUser) {
      h.push(cardHead(ic('lock') + 'User Access &amp; Visibility', 'Select an account to begin'));
      h.push('<div class="rp-empty">Choose an account to review effective permissions, assign roles, and configure page visibility.</div>');
      h.push('</section></div>');
      return h.join('');
    }
    var u = S.users.filter(function (x) { return x.username === S.selectedUser; })[0] || {};
    var eff = S.effective || {};
    var protectedUser = !!u.protected || eff.protected;
    h.push(cardHead(ic('manage_accounts') + esc(u.name || S.selectedUser),
      esc(S.selectedUser) + ' &middot; ' + esc(u.role) + ' &middot; ' + esc(u.status || 'Active'),
      '<button type="button" class="rp-btn sm" data-act="preview">' + ic('visibility') + 'Preview</button>' +
      '<button type="button" class="rp-btn sm primary" data-act="save"' + (S.busy ? ' disabled' : '') + '>' +
      ic('save') + 'Save &amp; Apply</button>'));

    /* identity facts */
    h.push('<div class="rp-card-body"><div class="rp-user-info-grid">');
    [['Institutional ID', u.id || '—'], ['Account Type', u.role || '—'],
     ['Account Status', u.status || 'Active'], ['Campus', u.campus || 'All campuses'],
     ['Department', u.department || '—'],
     ['Override State', u.has_overrides ? 'Active overrides' : 'Inheriting baseline']].forEach(function (f) {
      h.push('<div class="rp-user-info-item"><span class="rp-user-info-label">' + esc(f[0]) +
        '</span><span class="rp-user-info-val">' + esc(f[1]) + '</span></div>');
    });
    h.push('</div>');
    if (protectedUser) h.push('<div class="rp-note warn">' +
      (u.role === 'SUPER_ADMIN'
        ? 'SUPER_ADMIN is a protected system identity. It cannot receive overrides or custom roles.'
        : 'This account is not active; system restrictions still apply.') + '</div>');
    h.push('</div>');

    /* role assignments + effective sources */
    h.push('<div class="rp-section"><div class="rp-section-head"><div>' +
      '<div class="rp-section-title">Role Assignments &amp; Effective Permission Sources</div>' +
      '<div class="rp-section-sub">Effective access = core role baseline &cup; active custom roles &cup; per-account overrides. ' +
      'An administrator cannot delegate a permission they do not hold.</div></div></div>');
    var ur = S.userRoles || {};
    h.push('<div class="rp-assignments">');
    (ur.assignments || []).forEach(function (a) {
      h.push('<div class="rp-assignment"><span>' + svg('shield', 14) + esc(a.name) +
        ' <small>' + esc(a.assigned_by ? 'by ' + a.assigned_by + ' · ' + a.assigned_at : a.status) + '</small></span>' +
        '<button type="button" class="rp-btn sm danger" data-act="user-role-revoke" data-role-id="' +
        esc(a.role_id) + '">Revoke</button></div>');
    });
    if (!(ur.assignments || []).length) h.push('<div class="rp-muted rp-small">No custom roles assigned. Only the core baseline applies.</div>');
    if ((ur.eligible || []).length && !protectedUser) {
      h.push('<div class="rp-card-actions" style="margin-top:10px">' +
        '<select class="rp-tri" id="rpUserRoleAssign" aria-label="Role to assign">' +
        ur.eligible.map(function (a) {
          return '<option value="' + esc(a.id) + '">' + esc(a.name) + '</option>';
        }).join('') + '</select>' +
        '<button type="button" class="rp-btn" data-act="user-role-assign">' + svg('plus') + 'Assign role</button></div>');
    }
    h.push('</div>');
    var effRows = ur.effective || [];
    if (effRows.length) {
      h.push('<div class="rp-section-sub" style="margin-top:14px">Effective permissions (' + effRows.length + ' modules)</div>');
      h.push('<div class="rp-table-scroll"><table class="rp-table"><thead><tr><th>Module</th>' +
        '<th>Actions</th><th>Permission source</th></tr></thead><tbody>');
      h.push(preview('sources', effRows, function (row) {
        return '<tr><td>' + esc(row.label) + '</td><td class="rp-mono">' +
          esc(row.actions.join(', ')) + '</td><td>' + esc(row.source) + '</td></tr>';
      }, 'modules'));
      h.push('</tbody></table></div>');
    }
    h.push('</div>');

    /* page visibility */
    h.push('<div class="rp-section"><div class="rp-section-title">Page Visibility &amp; Direct Access Control</div>' +
      '<div class="rp-section-sub">Hiding removes a link from navigation. Denying blocks direct URL requests at the server. ' +
      'Explicit Deny always wins.</div>');
    h.push('<div class="rp-card-actions" style="margin-bottom:12px">' +
      '<select class="rp-tri" id="rpPagePortal" data-act="page-portal" aria-label="Portal filter">' +
      Object.keys(S.pages.portals || {}).map(function (p) {
        return '<option value="' + esc(p) + '"' + (S.pagePortal === p ? ' selected' : '') + '>' +
          esc(portalName(p)) + '</option>';
      }).join('') + '</select>' +
      '<input class="rp-input" id="rpPageSearch" data-act="page-search" placeholder="Filter pages" value="' +
      esc(S.pageSearch) + '"></div>');
    var pages = (S.pages.portals || {})[S.pagePortal] || [];
    var pq = (S.pageSearch || '').toLowerCase();
    var shown = pages.filter(function (p) {
      return !pq || (p.label + ' ' + p.id + ' ' + p.group + ' ' + (p.file || '')).toLowerCase().indexOf(pq) !== -1;
    });
    if (!shown.length) h.push('<div class="rp-muted rp-small">No pages match this filter.</div>');
    else {
      var groups = {};
      shown.forEach(function (p) { (groups[p.group || 'Other'] = groups[p.group || 'Other'] || []).push(p); });
      var gi = 0;
      Object.keys(groups).forEach(function (g) {
        var gKey = 'pg-' + S.pagePortal + '-' + g;
        var isOpen = groupOpen(gKey, !!pq || shown.length <= 30 || gi < 2);
        gi++;
        h.push('<details class="rp-page-group" data-ngx-key="' + esc(gKey) + '"' + (isOpen ? ' open' : '') +
          '><summary>' + esc(g) + '<span class="rp-muted rp-small">' + groups[g].length + ' pages</span></summary>');
        groups[g].forEach(function (p) {
          var rule = (S.draft && S.draft.pages && S.draft.pages[p.key]) || { visibility: 'inherit', access: 'inherit' };
          h.push('<div class="rp-page-row"><div class="rp-page-label" title="' + esc(p.href) + '">' +
            esc(p.label) + '<br><small>' + esc(p.file || p.key) + '</small></div>' +
            triSelect('page', p.key, '', rule.visibility, VIS, true) +
            triSelect('page', p.key, '', rule.access, TRI, false) +
            '<button type="button" class="rp-btn sm" data-act="hide-deny" data-key="' + esc(p.key) +
            '" title="Remove from navigation and block URL">Hide &amp; Deny</button></div>');
        });
        h.push('</details>');
      });
    }
    h.push('</div>');

    /* granular action permissions */
    h.push('<div class="rp-section"><div class="rp-section-title">Action-Level Granular Permissions</div>' +
      '<div class="rp-section-sub">' + clamp('Override individual actions on top of the assigned role baseline. ' +
        'Only actions registered for each module are presented; unknown identifiers are rejected by the backend. ' +
        'Supported actions include View, Create, Edit, Delete, Approve, Reject, Publish, Upload, Download, Export, Import and Manage.', 'act-perms-sub') + '</div>');
    h.push('<button type="button" class="rp-btn sm" data-act="toggle-actions" style="margin-bottom:10px">' +
      (S.showAllActions ? 'Show changed modules only' : 'Show all available modules') + '</button>');
    var changed = Object.keys((S.draft && S.draft.actions) || {});
    (S.registry.categories || []).forEach(function (cat) {
      var mods = cat.modules.filter(function (m) { return S.showAllActions || changed.indexOf(m.id) !== -1; });
      if (!mods.length) return;
      h.push('<details class="rp-page-group" data-ngx-key="actgrp-' + esc(cat.category) + '"' +
        (groupOpen('actgrp-' + cat.category, true) ? ' open' : '') + '><summary>' + esc(cat.category) +
        '<span class="rp-muted rp-small">' + mods.length + ' modules</span></summary>');
      h.push('<div class="rp-table-scroll"><table class="rp-table"><thead><tr><th>Module</th><th>Action</th>' +
        '<th>Override</th><th>Effective baseline</th></tr></thead><tbody>');
      mods.forEach(function (m) {
        var granted = ((S.effective || {}).action_permissions || {})[m.id] || [];
        m.actions.forEach(function (a) {
          var val = ((((S.draft && S.draft.actions) || {})[m.id] || {})[a]) || 'inherit';
          h.push('<tr><td>' + esc(m.name) + '</td><td>' + esc(actionLabel(a)) + '</td><td>' +
            triSelect('action', m.id, a, val, TRI, false) + '</td><td>' +
            (granted.indexOf(a) !== -1 ? status('Granted', 'ok') : status('Not granted', 'neutral')) +
            '</td></tr>');
        });
      });
      h.push('</tbody></table></div></details>');
    });
    h.push('</div>');

    /* effective inspector */
    h.push('<div class="rp-section"><div class="rp-section-title">Effective Access Inspector (Server-Computed)</div>' +
      '<div class="rp-section-sub">Computed by the exact backend resolver used for sidebar filtering and the direct-URL gate.</div>');
    var doc = S.preview || S.effective || {};
    if (!doc.portals) h.push('<div class="rp-empty"><button type="button" class="rp-btn" data-act="preview">' +
      ic('visibility') + 'Compute Effective Access Preview</button></div>');
    else {
      h.push('<div class="rp-card-actions" style="margin-bottom:12px">' +
        status((doc.hidden_keys || []).length + ' hidden pages', (doc.hidden_keys || []).length ? 'warn' : 'neutral') +
        status((doc.denied_keys || []).length + ' denied pages', (doc.denied_keys || []).length ? 'warn' : 'neutral') +
        status(Object.keys(doc.permissions || {}).length + ' permission modules', 'ok') + '</div>');
      h.push('<div class="rp-portals">');
      Object.keys(S.portalLabels).forEach(function (p) {
        var v = doc.portals[p] || 'inherit';
        h.push('<div class="rp-portal-row"><span>' + ic(S.portalIcons[p], 'rp-muted') + esc(portalName(p)) + '</span>' +
          status(v === 'allow' ? 'Allowed' : (v === 'deny' ? 'Denied' : 'Inherit'),
            v === 'allow' ? 'ok' : (v === 'deny' ? 'bad' : 'neutral')) + '</div>');
      });
      h.push('</div>');
      var restricted = (doc.pages || []).filter(function (p) { return !p.visible || !p.allowed; });
      if (restricted.length) {
        h.push('<div class="rp-table-scroll" style="margin-top:12px"><table class="rp-table"><thead><tr>' +
          '<th>Restricted page</th><th>Portal</th><th>Visibility</th><th>Direct URL</th><th>Reason</th></tr></thead><tbody>');
        h.push(preview('restricted', restricted, function (p) {
          return '<tr><td>' + esc(p.label) + ' <small class="rp-muted">(' + esc(p.file || p.key) + ')</small></td>' +
            '<td>' + esc(portalName(p.portal)) + '</td><td>' +
            status(p.visible ? 'Visible' : 'Hidden', p.visible ? 'ok' : 'warn') + '</td><td>' +
            status(p.allowed ? 'Allowed' : 'Blocked', p.allowed ? 'ok' : 'bad') + '</td><td class="rp-mono">' +
            esc(p.source || 'enforced') + '</td></tr>';
        }, 'pages'));
        h.push('</tbody></table></div>');
      } else {
        h.push('<div class="rp-note">All pages in accessible portals are visible and allowed.</div>');
      }
    }
    h.push('</div>');

    h.push('<div class="rp-sticky-bar"><span class="rp-muted rp-small">' + draftSize() +
      ' pending override group(s)</span><div class="rp-card-actions">' +
      '<button type="button" class="rp-btn" data-act="clear">Discard</button>' +
      '<button type="button" class="rp-btn" data-act="preview">' + ic('visibility') + 'Preview</button>' +
      '<button type="button" class="rp-btn primary" data-act="save"' + (S.busy ? ' disabled' : '') + '>' +
      (S.busy ? esc(S.busyLabel) : 'Save &amp; Apply Changes') + '</button></div></div>');
    h.push('</section></div>');
    return h.join('');
  }

  /* ------------------------------------------------------------ portal access */
  function renderPortals() {
    var h = ['<div class="rp-modebar"><span>Portal access configuration</span><div class="rp-mode-switch">' +
      '<button type="button" class="rp-btn sm' + (S.portalMode === 'role' ? ' is-active' : '') +
      '" data-act="portal-mode" data-mode="role">By custom role</button>' +
      '<button type="button" class="rp-btn sm' + (S.portalMode === 'account' ? ' is-active' : '') +
      '" data-act="portal-mode" data-mode="account">By account</button></div></div>'];
    h.push('<div class="rp-note">Base portal access follows the account type. Custom roles and per-account overrides ' +
      'are resolved by the same server-side engine that gates direct URLs. Explicit Deny always wins; ' +
      'only SUPER_ADMIN may grant Admin, Principal or Super Admin portals.</div>');
    h.push('<div class="rp-grid">');
    if (S.portalMode === 'role') {
      h.push('<aside class="rp-card rp-directory">');
      h.push(cardHead(ic('shield') + 'Custom Roles', (S.roles.custom_roles || []).length + ' editable roles'));
      h.push('<div class="rp-card-body tight"><div class="rp-list">');
      if (!(S.roles.custom_roles || []).length) h.push('<div class="rp-empty">No custom roles yet. Create one first.</div>');
      (S.roles.custom_roles || []).forEach(function (r) {
        h.push('<button type="button" class="rp-list-item' + (S.selectedPortalRole === r.id ? ' is-active' : '') +
          '" data-act="portal-role-select" data-id="' + esc(r.id) + '"><div class="rp-list-name"><span>' +
          esc(r.name) + '</span></div><div class="rp-list-meta">' +
          esc((r.portals || []).length) + ' portals &middot; ' + esc(r.members || 0) + ' members</div></button>');
      });
      h.push('</div></div></aside>');
      h.push('<section class="rp-card rp-workspace">');
      var role = (S.roles.custom_roles || []).filter(function (r) { return r.id === S.selectedPortalRole; })[0];
      if (!role) {
        h.push(cardHead(ic('hub') + 'Portal Access Control', 'Select a custom role'));
        h.push('<div class="rp-empty">Select a custom role to configure its portal access.</div>');
      } else {
        var draft = S.rolePortalDraft || role.portals || [];
        h.push(cardHead(ic('hub') + esc(role.name), esc(role.id) + ' &middot; ' +
          esc(role.members || 0) + ' assigned account(s)'));
        h.push('<div class="rp-card-body"><div class="rp-note">Granting a portal here affects every account holding ' +
          'this role. It does not grant any page or action permission by itself.</div></div>');
        h.push('<div class="rp-section"><div class="rp-table-scroll"><table class="rp-table"><thead><tr>' +
          '<th>Portal</th><th>Base type</th><th>Role grant</th><th>Backend enforcement</th></tr></thead><tbody>');
        (S.rolePortals.portals || []).forEach(function (p) {
          var checked = draft.indexOf(p.id) !== -1;
          var locked = p.protected && S.authority.can_configure_protected_portals === false;
          h.push('<tr><td><span class="rp-portal-name">' + ic(S.portalIcons[p.id] || 'hub') +
            esc(p.label) + '</span></td><td>' +
            status(p.protected ? 'Protected' : 'Eligible', p.protected ? 'warn' : 'neutral') + '</td><td>' +
            '<label class="rp-inline-check"><input type="checkbox" data-kind="roleportal" data-value="' +
            esc(p.id) + '"' + (checked ? ' checked' : '') + (locked ? ' disabled' : '') + '>' +
            (checked ? 'Allowed' : 'Not granted') + '</label></td><td class="rp-small">' +
            (p.protected && locked ? 'SUPER_ADMIN only' : 'Server-side page gate') + '</td></tr>');
        });
        h.push('</tbody></table></div>');
        h.push('<div class="rp-card-actions" style="margin-top:14px;justify-content:flex-end">' +
          '<button type="button" class="rp-btn" data-act="portal-role-reset">Discard</button>' +
          '<button type="button" class="rp-btn primary" data-act="role-portals-save"' + (S.busy ? ' disabled' : '') +
          '>Save Portal Access</button></div></div>');
      }
      h.push('</section>');
    } else {
      h.push(renderUserDirectory('portals'));
      h.push('<section class="rp-card rp-workspace">');
      if (!S.selectedUser) {
        h.push(cardHead(ic('hub') + 'Account Portal Overrides', 'Select an account'));
        h.push('<div class="rp-empty">Select an account from the directory.</div>');
      } else {
        var u = S.users.filter(function (x) { return x.username === S.selectedUser; })[0] || {};
        var eff = S.effective || {};
        var protectedUser = !!u.protected || eff.protected;
        h.push(cardHead(ic('hub') + esc(u.name || S.selectedUser),
          esc(S.selectedUser) + ' &middot; ' + esc(u.role),
          '<button type="button" class="rp-btn sm" data-act="preview">' + ic('visibility') + 'Preview</button>' +
          '<button type="button" class="rp-btn sm primary" data-act="save"' + (S.busy ? ' disabled' : '') +
          '>Save Portal Access</button>'));
        if (protectedUser) h.push('<div class="rp-card-body"><div class="rp-note warn">' +
          'SUPER_ADMIN accounts have permanent full access and cannot receive overrides.</div></div>');
        h.push('<div class="rp-section"><div class="rp-table-scroll"><table class="rp-table"><thead><tr>' +
          '<th>Portal</th><th>Base access</th><th>Effective status</th><th>Access control</th></tr></thead><tbody>');
        Object.keys(S.portalLabels).forEach(function (p) {
          var val = (S.draft && S.draft.portals && S.draft.portals[p]) || 'inherit';
          var base = (eff.portals && eff.portals[p]) || 'deny';
          var effStatus = val === 'allow' ? 'allow' : (val === 'deny' ? 'deny' : base);
          var privileged = S.protectedPortals.indexOf(p) !== -1;
          var isSelf = actor() && actor() === S.selectedUser;
          var disabled = protectedUser || (isSelf && privileged);
          h.push('<tr><td><span class="rp-portal-name">' + ic(S.portalIcons[p], 'rp-muted') +
            esc(portalName(p)) + '</span></td><td>' +
            status(base === 'allow' ? 'Allowed' : 'Denied', base === 'allow' ? 'ok' : 'neutral') + '</td><td>' +
            status(effStatus === 'allow' ? 'Allowed' : 'Denied', effStatus === 'allow' ? 'ok' : 'bad') +
            '</td><td>' + (disabled ? '<span class="rp-muted rp-small">Protected</span>' :
              triSelect('portal', p, '', val, TRI, false)) + '</td></tr>');
        });
        h.push('</tbody></table></div>');
        h.push('<div class="rp-card-actions" style="margin-top:14px;justify-content:flex-end">' +
          '<button type="button" class="rp-btn" data-act="clear">Discard</button>' +
          '<button type="button" class="rp-btn" data-act="preview">' + ic('visibility') + 'Preview</button>' +
          '<button type="button" class="rp-btn primary" data-act="save"' + (S.busy ? ' disabled' : '') +
          '>Save Portal Access</button></div></div>');
      }
      h.push('</section>');
    }
    h.push('</div>');
    return h.join('');
  }

  /* --------------------------------------------------------------- activity */
  function renderActivity() {
    var h = ['<div class="rp-activity-bar"><div class="rp-activity-meta">' +
      esc(S.auditTotal) + ' audit events &middot; ' + esc(S.auditActions.length) + ' action types &middot; ' +
      'newest first, loaded from the server</div><div class="rp-card-actions">' +
      '<select class="rp-tri" id="rpAuditAction" data-act="audit-action" aria-label="Filter by action">' +
      '<option value="">All actions</option>' +
      S.auditActions.map(function (a) {
        return '<option value="' + esc(a.id) + '"' + (S.auditAction === a.id ? ' selected' : '') + '>' +
          esc(a.id) + ' (' + a.count + ')</option>';
      }).join('') + '</select>' +
      '<input class="rp-input" id="rpAuditSearch" data-act="audit-search" placeholder="Search actor, target, details" value="' +
      esc(S.auditSearch) + '">' +
      '<select class="rp-tri" id="rpAuditSize" data-act="audit-size" aria-label="Rows per page">' +
      [20, 50, 100].map(function (n) {
        return '<option value="' + n + '"' + (S.auditPageSize === n ? ' selected' : '') + '>' + n + ' / page</option>';
      }).join('') + '</select></div></div>'];
    h.push('<div class="rp-card"><div class="rp-card-body tight"><div class="rp-table-scroll">' +
      '<table class="rp-table"><thead><tr><th>Timestamp</th><th>Actor</th><th>Action</th>' +
      '<th>Target</th><th>Outcome</th><th></th></tr></thead><tbody>');
    if (!S.auditRows.length) h.push('<tr><td colspan="6" class="rp-empty">No matching audit events.</td></tr>');
    S.auditRows.forEach(function (e, i) {
      h.push('<tr><td class="rp-mono">' + esc(e.ts) + '<div class="rp-muted rp-small">' + esc(e.id) + '</div></td>' +
        '<td>' + esc(e.actor) + '</td><td class="rp-mono">' + esc(e.action) + '</td><td>' +
        esc(e.target_role_name || e.target_user || e.target_role || '—') + '</td><td>' +
        status(e.outcome || 'success', e.outcome === 'success' ? 'ok' : 'warn') + '</td>' +
        '<td class="right"><button type="button" class="rp-btn sm" data-act="audit-detail" data-index="' +
        i + '">Details</button></td></tr>');
    });
    h.push('</tbody></table></div>');
    var totalPages = Math.max(1, Math.ceil(S.auditTotal / S.auditPageSize));
    h.push('<div class="ngx-pager" role="navigation" aria-label="Audit log pagination">' +
      '<button type="button" class="ngx-page-btn" data-act="audit-page" data-dir="-1"' +
      (S.auditPage <= 1 ? ' disabled' : '') + '>' + ic('chevron_left') + 'Prev</button>' +
      '<span class="ngx-page-info">Page ' + S.auditPage + ' of ' + totalPages + '</span>' +
      '<button type="button" class="ngx-page-btn" data-act="audit-page" data-dir="1"' +
      (S.auditPage >= totalPages ? ' disabled' : '') + '>Next' + ic('chevron_right') + '</button>' +
      '<span class="ngx-count">' + S.auditTotal + ' events &middot; server-paginated</span></div>');
    h.push('</div></div>');
    return h.join('');
  }

  /* ------------------------------------------------------------------ modal */
  function field(label, id, value, placeholder, type, extra) {
    return '<div class="rp-field"><label for="' + esc(id) + '">' + esc(label) + '</label>' +
      '<input class="rp-input" id="' + esc(id) + '" data-field="' + esc(id) + '" type="' +
      (type || 'text') + '" value="' + esc(value || '') + '" placeholder="' + esc(placeholder || '') +
      '" ' + (extra || '') + '></div>';
  }
  function selectField(label, id, value, options, extra) {
    return '<div class="rp-field"><label for="' + esc(id) + '">' + esc(label) + '</label>' +
      '<select class="rp-tri" id="' + esc(id) + '" data-field="' + esc(id) + '" ' + (extra || '') + '>' +
      options.map(function (o) {
        return '<option value="' + esc(o.value) + '"' + (String(value || '') === String(o.value) ? ' selected' : '') +
          '>' + esc(o.label) + '</option>';
      }).join('') + '</select></div>';
  }

  function renderModal() {
    var m = S.modal || {};
    var f = m.form || {};
    var isWide = m.type === 'compare';
    var h = ['<div class="rp-modal-scrim ngis-modal-backdrop ngis-modal-active" data-act="modal-scrim">' +
      '<div class="rp-modal ngis-modal' + (isWide ? ' rp-modal-wide' : '') + '" role="dialog" aria-modal="true" aria-label="' +
      esc(m.title || 'Dialog') + '">'];
    h.push('<div class="rp-modal-head"><div class="rp-modal-title">' + esc(m.title || '') + '</div>' +
      '<button type="button" class="rp-modal-x" data-act="modal-close" aria-label="Close dialog">' +
      svg('close', 16) + '</button></div>');
    h.push('<div class="rp-modal-body">');
    if (m.error) h.push('<div class="rp-modal-error" role="alert">' + esc(m.error) + '</div>');

    if (m.type === 'role') {
      h.push('<div class="rp-modal-section-title">Role Information</div>');
      h.push('<div class="rp-form-grid">');
      h.push(field('Role Name', 'rpRoleName', f.rpRoleName, 'e.g. Academic Coordinator', 'text', 'data-modal-focus'));
      h.push(field('Role Identifier', 'rpRoleIdent', f.rpRoleIdent, 'generated-from-name'));
      h.push(selectField('Role Category', 'rpRoleCategory', f.rpRoleCategory,
        (S.categories || ['custom']).map(function (c) { return { value: c, label: c }; })));
      h.push(selectField('Default Portal', 'rpRolePortal', f.rpRolePortal,
        [{ value: '', label: 'Inherited from base role' }].concat(Object.keys(S.portalLabels).map(function (p) {
          return { value: p, label: portalName(p) };
        }))));
      h.push(selectField('Role Status', 'rpRoleStatus', f.rpRoleStatus,
        [{ value: 'active', label: 'Active' }, { value: 'archived', label: 'Disabled' }]));
      if (!m.edit) h.push(selectField('Base Role Baseline', 'rpRoleBase', f.rpRoleBase,
        (S.registry.core_roles || []).map(function (r) { return { value: r, label: r.replace(/_/g, ' ') }; })));
      h.push('</div>');
      h.push(field('Description', 'rpRoleDesc', f.rpRoleDesc, 'What this role is responsible for'));
      if (!m.edit) {
        h.push('<div class="rp-modal-section-title">Permission Configuration</div>');
        h.push('<div class="rp-modal-note">Select modules to grant the View permission. Additional actions can be ' +
          'configured in the matrix after the role is created. Every permission is validated against the server registry.</div>');
        h.push('<div class="rp-modal-modules">');
        (S.registry.categories || []).forEach(function (cat, i) {
          h.push('<details class="rp-modal-cat" data-ngx-key="modal-cat-' + esc(cat.category) + '"' +
            (groupOpen('modal-cat-' + cat.category, i === 0) ? ' open' : '') + '><summary>' +
            esc(cat.category) + '<span class="rp-muted rp-small">' + cat.modules.length + ' modules</span></summary>');
          cat.modules.forEach(function (mod) {
            var on = (f.modules || []).indexOf(mod.id) !== -1;
            h.push('<label class="rp-inline-check"><input type="checkbox" data-act="modal-module" data-value="' +
              esc(mod.id) + '"' + (on ? ' checked' : '') + '> ' + esc(mod.name) + '</label>');
          });
          h.push('</details>');
        });
        h.push('</div>');
      } else {
        h.push('<div class="rp-modal-note">The permission matrix and portal access are edited in the workspace. ' +
          'Core role definitions cannot be modified.</div>');
      }
    } else if (m.type === 'permission') {
      h.push('<div class="rp-modal-section-title">Basic Information</div>');
      h.push('<div class="rp-form-grid">');
      h.push(field('Permission Name', 'rpPermName', f.rpPermName, 'e.g. Approve Teacher Reports', 'text', 'data-modal-focus'));
      h.push(field('Permission Key', 'rpPermKey', f.rpPermKey, 'teacher-reports.approve', 'text',
        m.edit ? 'readonly' : ''));
      h.push(selectField('Target Module', 'rpPermModule', f.rpPermModule,
        [{ value: '__new__', label: '＋ New module…' }].concat(
          (S.permInventory && S.permInventory.modules ? S.permInventory.modules : []).map(function (mod) {
            return { value: mod.id, label: mod.label };
          }))));
      if (f.rpPermModule === '__new__') h.push(field('New Module Slug', 'rpPermNewModule', f.rpPermNewModule, 'teacher-reports'));
      h.push(selectField('Action Type', 'rpPermAction', f.rpPermAction,
        ((S.permInventory && S.permInventory.actions) || []).map(function (a) {
          return { value: a.id, label: a.label };
        })));
      h.push(selectField('Applicable Portal', 'rpPermPortal', f.rpPermPortal,
        Object.keys(S.portalLabels).map(function (p) { return { value: p, label: portalName(p) }; })));
      h.push(selectField('Permission Scope', 'rpPermScope', f.rpPermScope,
        ((S.boot && S.boot.permission_scopes) || []).map(function (s) {
          return { value: s.id, label: s.label };
        })));
      var pageOpts = [{ value: '', label: 'No specific page (module-level)' }];
      var portalPages = ((S.pages.portals || {})[f.rpPermPortal] || []);
      pageOpts = pageOpts.concat(portalPages.map(function (p) {
        return { value: p.key, label: p.label + ' — ' + p.file };
      }));
      h.push(selectField('Target Page / Resource', 'rpPermPage', f.rpPermPage, pageOpts));
      h.push('</div>');
      h.push(field('Description', 'rpPermDesc', f.rpPermDesc, 'What this permission controls'));
      h.push('<div class="rp-modal-note">A permission definition is not an access grant. It becomes enforceable only ' +
        'when its module and action map to a real backend binding. Otherwise it is stored as ' +
        '<strong>Requires Integration</strong> and cannot be assigned to any role. Custom action identifiers are ' +
        'not supported — only registered actions are accepted.</div>');
    } else if (m.type === 'assign') {
      h.push('<div class="rp-modal-note">Assign or revoke eligible custom roles for real login accounts. ' +
        'Self-assignment, SUPER_ADMIN identities and permissions you do not hold are blocked by the backend.</div>');
      h.push('<div class="rp-form-grid">');
      h.push(selectField('Custom Role', 'rpAssignRole', f.rpAssignRole,
        [{ value: '', label: 'Select a role' }].concat((S.roles.custom_roles || []).map(function (r) {
          return { value: r.id, label: r.name + ' (' + r.id + ')' };
        }))));
      h.push(field('Find account', 'rpAssignSearch', f.rpAssignSearch, 'Name or username'));
      h.push('</div>');
      h.push('<div class="rp-assign-list">');
      if (!f.rpAssignRole) h.push('<div class="rp-muted rp-small">Select a role to see eligible accounts.</div>');
      else if (!S.assignUsers.length) h.push('<div class="rp-muted rp-small">No matching accounts.</div>');
      else S.assignUsers.forEach(function (u) {
        var holds = (u.custom_roles || []).indexOf(f.rpAssignRole) !== -1;
        h.push('<div class="rp-assignment"><span>' + esc(u.name || u.username) +
          ' <small>' + esc(u.username) + ' &middot; ' + esc(u.role) + '</small></span>' +
          '<button type="button" class="rp-btn sm' + (holds ? ' danger' : '') +
          '" data-act="assign-toggle" data-username="' + esc(u.username) + '" data-op="' +
          (holds ? 'revoke' : 'assign') + '">' + (holds ? 'Revoke' : 'Assign') + '</button></div>');
      });
      h.push('</div>');
    } else if (m.type === 'confirm') {
      h.push('<div class="rp-modal-note">' + esc(m.message || '') + '</div>');
      if (m.changes && m.changes.length) {
        h.push('<div class="rp-confirm-list">');
        m.changes.slice(0, 12).forEach(function (c) {
          h.push('<div><span class="rp-plain-tag ' + (c.tone || '') + '">' + esc(c.tag) + '</span>' +
            esc(c.text) + '</div>');
        });
        if (m.changes.length > 12) h.push('<div class="rp-muted rp-small">+' +
          (m.changes.length - 12) + ' more change(s)</div>');
        h.push('</div>');
      }
    } else if (m.type === 'compare') {
      h.push('<div class="rp-compare-banner">' +
        '<div class="banner-icon">' + svg('compare', 18) + '</div>' +
        '<div><div style="font-weight:500;margin-bottom:2px">Compare Role Permissions &amp; Access Matrix</div>' +
        '<div style="font-size:12px;opacity:0.9">Select two roles below to analyze permission boundaries, exclusive capabilities, and overlapping privileges in real time.</div></div>' +
      '</div>');

      var allR = allRoles();
      h.push('<div class="rp-compare-cards-grid">');
      // Role A card
      h.push('<div class="rp-role-card role-a">' +
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">' +
          '<span style="font-size:11px;font-weight:500;text-transform:uppercase;color:#15803D;letter-spacing:0.04em">Role A (Reference)</span>' +
          '<span class="rp-diff-badge-a">Reference</span>' +
        '</div>' +
        selectField('Select Role A', 'rpCompareA', S.compareA, allR.map(function (r) {
          return { value: r.id, label: r.name + ' (' + (r.category || 'core') + ')' };
        })) +
      '</div>');

      // VS Badge
      h.push('<div class="rp-vs-divider">' +
        '<div class="rp-vs-badge">' + svg('compare', 14) + '</div>' +
        '<span>VS</span>' +
      '</div>');

      // Role B card
      h.push('<div class="rp-role-card role-b">' +
        '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">' +
          '<span style="font-size:11px;font-weight:500;text-transform:uppercase;color:#1D4ED8;letter-spacing:0.04em">Role B (Comparison)</span>' +
          '<span class="rp-diff-badge-b">Target</span>' +
        '</div>' +
        selectField('Select Role B', 'rpCompareB', S.compareB, allR.map(function (r) {
          return { value: r.id, label: r.name + ' (' + (r.category || 'core') + ')' };
        })) +
      '</div>');
      h.push('</div>');

      if (S.compareLoading) {
        h.push('<div style="padding:36px 16px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:12px">' +
          '<div style="width:30px;height:30px;border:3px solid #E2E8F0;border-top-color:#176B45;border-radius:50%;animation:spin 0.8s linear infinite"></div>' +
          '<div style="font-size:13px;color:#64748B">Analyzing permission matrix between roles…</div>' +
        '</div>');
      } else if (S.compareError) {
        h.push('<div class="rp-modal-error" style="display:flex;align-items:center;justify-content:space-between">' +
          '<div>' + esc(S.compareError) + '</div>' +
          '<button type="button" class="rp-btn sm danger" data-act="compare-run">Retry Comparison</button>' +
        '</div>');
      } else if (S.compareResult) {
        var res = S.compareResult;
        var allRows = [];
        var onlyA = 0;
        var onlyB = 0;
        var identical = 0;

        Object.keys(res.modules || {}).forEach(function (cat) {
          (res.modules[cat] || []).forEach(function (row) {
            var hasA = row.only_a && row.only_a.length > 0;
            var hasB = row.only_b && row.only_b.length > 0;
            if (hasA && !hasB) onlyA++;
            else if (hasB && !hasA) onlyB++;
            else if (hasA && hasB) { onlyA++; onlyB++; }
            else identical++;
            allRows.push({
              category: cat,
              module: row.module || row.label,
              label: row.label,
              only_a: row.only_a || [],
              only_b: row.only_b || []
            });
          });
        });

        h.push('<div class="rp-compare-kpis">' +
          '<div class="rp-kpi-chip"><div class="chip-label">Total Modules</div><div class="chip-val">' + allRows.length + '</div></div>' +
          '<div class="rp-kpi-chip"><div class="chip-label">Exclusive to ' + esc(res.a.name) + '</div><div class="chip-val" style="color:#15803D">' + onlyA + '</div></div>' +
          '<div class="rp-kpi-chip"><div class="chip-label">Exclusive to ' + esc(res.b.name) + '</div><div class="chip-val" style="color:#1D4ED8">' + onlyB + '</div></div>' +
          '<div class="rp-kpi-chip"><div class="chip-label">Identical Modules</div><div class="chip-val" style="color:#475569">' + identical + '</div></div>' +
        '</div>');

        if (!allRows.length) {
          h.push('<div class="rp-note">No module permissions found for comparison.</div>');
        } else {
          var diffRows = allRows.filter(function (r) { return r.only_a.length > 0 || r.only_b.length > 0; });
          h.push('<div style="display:flex;align-items:center;justify-content:space-between;margin-top:6px">' +
            '<div style="font-size:12px;font-weight:500;color:#334155">' +
              (diffRows.length ? 'Found ' + diffRows.length + ' differences across ' + allRows.length + ' modules' : 'All permissions are identical between ' + esc(res.a.name) + ' and ' + esc(res.b.name)) +
            '</div>' +
            '<button type="button" class="rp-btn sm secondary" data-act="compare-run" title="Re-run comparison">' + svg('compare') + ' Refresh</button>' +
          '</div>');

          h.push('<div class="rp-table-scroll" style="max-height:360px;overflow-y:auto;border:1px solid #E2E8F0;border-radius:8px">' +
            '<table class="rp-table" style="width:100%;font-size:12px">' +
            '<thead><tr>' +
              '<th style="width:32%">Module</th>' +
              '<th style="width:28%;color:#15803D">Only in ' + esc(res.a.name) + '</th>' +
              '<th style="width:28%;color:#1D4ED8">Only in ' + esc(res.b.name) + '</th>' +
              '<th style="width:12%;text-align:right">Verdict</th>' +
            '</tr></thead><tbody>');

          allRows.forEach(function (r) {
            var isDiff = r.only_a.length > 0 || r.only_b.length > 0;
            var verdict = !isDiff ? '<span class="rp-diff-badge-same">Identical</span>' :
              (r.only_a.length && !r.only_b.length ? '<span class="rp-diff-badge-a">A Only</span>' :
              (!r.only_a.length && r.only_b.length ? '<span class="rp-diff-badge-b">B Only</span>' :
              '<span class="rp-diff-badge-a">Differs</span>'));

            h.push('<tr style="' + (isDiff ? 'background:#F8FAFC' : '') + '">' +
              '<td><div style="font-weight:500;color:#1E293B">' + esc(r.label) + '</div><div style="font-size:10.5px;color:#64748B">' + esc(r.category) + '</div></td>' +
              '<td>' + (r.only_a.length ? '<span style="color:#15803D;font-weight:500">' + esc(r.only_a.join(', ')) + '</span>' : '<span style="color:#94A3B8">—</span>') + '</td>' +
              '<td>' + (r.only_b.length ? '<span style="color:#1D4ED8;font-weight:500">' + esc(r.only_b.join(', ')) + '</span>' : '<span style="color:#94A3B8">—</span>') + '</td>' +
              '<td style="text-align:right">' + verdict + '</td>' +
            '</tr>');
          });
          h.push('</tbody></table></div>');
        }
      }
    } else if (m.type === 'audit') {
      var e = S.auditRows[m.index] || {};
      h.push('<div class="rp-table-scroll"><table class="rp-table"><tbody>');
      Object.keys(e).forEach(function (k) {
        var v = typeof e[k] === 'object' ? JSON.stringify(e[k], null, 2) : String(e[k]);
        h.push('<tr><th>' + esc(k) + '</th><td><pre class="rp-pre">' + esc(v) + '</pre></td></tr>');
      });
      h.push('</tbody></table></div>');
    }
    h.push('</div>');
    h.push('<div class="rp-modal-foot">');
    if (m.type === 'role') h.push('<button type="button" class="rp-btn primary" data-act="role-submit"' +
      (S.busy ? ' disabled' : '') + '>' + (m.edit ? 'Save Role' : 'Create Role') + '</button>');
    if (m.type === 'permission') h.push('<button type="button" class="rp-btn primary" data-act="permission-submit"' +
      (S.busy ? ' disabled' : '') + '>' + (m.edit ? 'Save Permission' : 'Create Permission') + '</button>');
    if (m.type === 'confirm') h.push('<button type="button" class="rp-btn ' +
      (m.danger ? 'danger' : 'primary') + '" data-act="confirm-yes"' + (S.busy ? ' disabled' : '') + '>' +
      esc(m.confirmLabel || 'Confirm') + '</button>');
    if (m.type === 'compare') {
      h.push('<button type="button" class="rp-btn secondary" data-act="modal-close">Close Comparison</button>');
      h.push('<button type="button" class="rp-btn primary" data-act="compare-run"' +
        (S.compareLoading ? ' disabled' : '') + '>' + svg('compare') + ' ' + (S.compareLoading ? 'Comparing…' : 'Compare Again') + '</button>');
    } else {
      h.push('<button type="button" class="rp-btn" data-act="modal-close">Cancel</button>');
    }
    h.push('</div>');
    h.push('</div></div>');
    return h.join('');
  }

  /* ------------------------------------------------------------------ loads */
  function loadBase() {
    return Promise.all([
      api('/api/roles-mgmt/bootstrap'),
      api('/api/roles-mgmt/registry'),
      api('/api/roles-mgmt/permissions'),
      api('/api/roles-mgmt/role-portals'),
      api('/api/roles-mgmt/campuses'),
      api('/api/roles-mgmt/enforcement'),
      api('/api/roles-mgmt/audit/paged?limit=' + S.auditPageSize + '&offset=0')
    ]).then(function (res) {
      S.boot = res[0];
      S.registry = (res[0].registry && res[0].registry.categories) ? res[0].registry : res[1];
      S.authority = res[0].authority || {};
      S.roles = res[0].roles || { core_roles: [], custom_roles: [] };
      S.overview = res[0].overview || {};
      S.pages = res[0].pages || { portals: {}, total: 0 };
      S.definitions = res[0].definitions || { custom: [], enforced_pairs: [] };
      S.definitions.custom = (res[2].custom || []);
      S.categories = res[0].categories || ['custom'];
      S.protectedPortals = res[0].protected_portals || [];
      S.permInventory = res[2];
      S.rolePortals = res[3];
      S.campuses = res[4].campuses || [];
      S.bindings = res[5].bindings || [];
      S.auditRows = res[6].data || [];
      S.auditTotal = res[6].total || 0;
      S.auditActions = res[6].actions || [];
      if (!currentRole()) S.selectedRoleId = (S.roles.core_roles[0] || {}).id || '';
      if (!S.selectedPortalRole && (S.roles.custom_roles || []).length) {
        S.selectedPortalRole = S.roles.custom_roles[0].id;
        S.rolePortalDraft = S.roles.custom_roles[0].portals || [];
      }
      return fetchUsers(true);
    }).then(function () {
      if (!S.selectedUser) S.selectedUser = (S.users[0] || {}).username || null;
      return Promise.all([loadRoleDetail(), loadUserDetail()]);
    });
  }
  function reloadRoles() {
    return api('/api/roles-mgmt/bootstrap').then(function (b) {
      S.boot = b; S.roles = b.roles; S.overview = b.overview;
      S.definitions.custom = b.definitions.custom;
      S.authority = b.authority;
      S.pages = b.pages;
    });
  }
  function fetchUsers(reset) {
    if (reset) { S.users = []; S.userOffset = 0; }
    var params = ['limit=' + (reset ? S.userLimit : S.userLimit),
      'offset=' + S.userOffset, 'q=' + encodeURIComponent(S.userQ),
      'role=' + encodeURIComponent(S.userRole), 'campus=' + encodeURIComponent(S.userCampus)];
    return api('/api/roles-mgmt/users/paged?' + params.join('&')).catch(function () {
      // Legacy fallback keeps the workspace usable on older deployments.
      return api('/api/roles-mgmt/users').then(function (d) {
        var rows = d.users || [];
        return { users: rows.slice(S.userOffset, S.userOffset + S.userLimit),
                 total: rows.length, has_more: false };
      });
    }).then(function (d) {
      S.users = reset ? (d.users || []) : S.users.concat(d.users || []);
      S.userTotal = d.total || 0;
      S.userHasMore = !!d.has_more;
      S.userOffset = S.users.length;
      if (!S.selectedUser || !S.users.filter(function (u) {
        return u.username === S.selectedUser; }).length) {
        S.selectedUser = (S.users[0] || {}).username || null;
      }
    });
  }
  function loadRoleDetail() {
    var id = S.selectedRoleId;
    if (!id) return Promise.resolve();
    return Promise.all([
      api('/api/roles-mgmt/roles/' + encodeURIComponent(id) + '/permissions'),
      api('/api/roles-mgmt/roles/' + encodeURIComponent(id) + '/members')
    ]).then(function (res) {
      S.rolePerms = res[0];
      S.roleMembers = res[1];
      S.permDraft = clone(res[0].permissions || {});
      S.permDirty = false;
      var role = currentRole();
      S.customKeys = clone((role && role.custom_permission_keys) || []);
      S.rolePortalDraft = clone((role && role.portals) || []);
    });
  }
  function loadUserDetail() {
    var u = S.selectedUser;
    if (!u) return Promise.resolve();
    return Promise.all([
      api('/api/roles-mgmt/overrides/' + encodeURIComponent(u)),
      api('/api/roles-mgmt/effective/' + encodeURIComponent(u)),
      api('/api/roles-mgmt/user-roles?username=' + encodeURIComponent(u))
    ]).then(function (res) {
      var ov = res[0].overrides || {};
      S.overrides = clone(ov);
      S.draft = { portals: clone(ov.portals || {}), pages: clone(ov.pages || {}),
        actions: clone(ov.actions || {}) };
      S.effective = res[1];
      S.userRoles = res[2];
      S.preview = null;
    });
  }
  function loadAudit() {
    var params = ['limit=' + S.auditPageSize,
      'offset=' + ((S.auditPage - 1) * S.auditPageSize),
      'action=' + encodeURIComponent(S.auditAction),
      'search=' + encodeURIComponent(S.auditSearch)];
    return api('/api/roles-mgmt/audit/paged?' + params.join('&')).then(function (d) {
      S.auditRows = d.data || [];
      S.auditTotal = d.total || 0;
      S.auditActions = d.actions || S.auditActions;
      render();
    });
  }

  /* ---------------------------------------------------------------- actions */
  function closeModal() { S.modal = null; render(); }
  function openConfirm(title, message, changes, onYes, danger, label) {
    S.modal = { type: 'confirm', title: title, message: message, changes: changes,
      onYes: onYes, danger: !!danger, confirmLabel: label || 'Confirm' };
    render();
  }
  function openRoleModal(edit) {
    var role = currentRole() || {};
    S.modal = {
      type: 'role', edit: !!edit,
      title: edit ? 'Edit Custom Role' : 'Add New Role',
      form: {
        rpRoleName: edit ? role.name : '', rpRoleIdent: edit ? role.identifier : '',
        rpRoleDesc: edit ? role.description : '',
        rpRoleCategory: edit ? (role.category || 'custom') : 'custom',
        rpRolePortal: edit ? (role.default_portal || '') : '',
        rpRoleStatus: edit ? (role.status || 'active') : 'active',
        rpRoleBase: 'TEACHER', modules: []
      }
    };
    render();
  }
  function openPermissionModal(edit, key) {
    var d = (S.definitions.custom || []).filter(function (x) { return x.key === key; })[0] || {};
    S.modal = {
      type: 'permission', edit: !!edit, key: key,
      title: edit ? 'Edit Permission Definition' : 'Add Permission',
      form: {
        rpPermName: d.name || '', rpPermKey: d.key || '',
        rpPermDesc: d.description || '',
        // A custom module slug is not a registered dropdown option. Select the
        // "New module…" entry and repopulate its slug so editing a definition
        // never silently shows a different module than the one being saved.
        rpPermModule: (edit && !d.custom_module) ? d.module : '__new__',
        rpPermNewModule: edit && d.custom_module ? d.module : '',
        rpPermAction: d.action || 'view',
        rpPermPortal: d.portal || 'admin',
        rpPermScope: d.scope || 'global',
        rpPermPage: d.target_page || ''
      }
    };
    render();
  }
  function refreshAfterWrite() {
    return Promise.all([reloadRoles(), loadRoleDetail(), loadAudit(), loadUserDetail()])
      .then(function () {
        // loadRoleDetail() re-seeds rolePortalDraft from the Roles-tab
        // selection. When the Portal tab is active, re-seed it from the
        // role actually being configured there instead, otherwise the next
        // save would silently submit the wrong role's (empty) portal list.
        if (S.tab === 'portals' && S.portalMode === 'role') {
          var pr = (S.roles.custom_roles || []).filter(function (r) {
            return r.id === S.selectedPortalRole; })[0];
          S.rolePortalDraft = clone((pr && pr.portals) || []);
        }
        render();
      });
  }

  function onTab(tab) {
    S.tab = tab; S.modal = null;
    if (tab === 'activity') { S.auditPage = 1; loadAudit(); }
    else render();
  }

  function onClick(e) {
    var t = e.target && e.target.closest ? e.target.closest('[data-act]') : null;
    if (!t || (!S.root.contains(t) && !(S.modalEl && S.modalEl.contains(t)))) return;
    var act = t.getAttribute('data-act');
    var id = t.getAttribute('data-id');
    var key = t.getAttribute('data-key');
    var username = t.getAttribute('data-username');

    if (act === 'tab') { onTab(t.getAttribute('data-tab')); return; }
    if (act === 'ngx-more' || act === 'ngx-less') {
      e.preventDefault();
      var sc = t.getAttribute('data-scope');
      S.ngxLimits[sc] = act === 'ngx-more' ? limit(sc) + STEP : (INIT[sc] || 5);
      render(true); return;
    }
    if (act === 'ngx-toggle-text') {
      e.preventDefault();
      var tk = t.getAttribute('data-key');
      S.ngxOpen['txt-' + tk] = !S.ngxOpen['txt-' + tk];
      render(true); return;
    }
    if (act === 'modal-close' || (act === 'modal-scrim' && e.target === t)) { closeModal(); return; }
    if (act === 'confirm-yes') {
      var fn = S.modal && S.modal.onYes;
      S.modal = null;
      if (fn) fn();
      else render();
      return;
    }

    function runCompare() {
      if (!S.compareA || !S.compareB) return;
      S.compareLoading = true;
      S.compareError = null;
      render();
      api('/api/roles-mgmt/compare?a=' + encodeURIComponent(S.compareA) + '&b=' + encodeURIComponent(S.compareB))
        .then(function (r) {
          S.compareResult = r;
          S.compareLoading = false;
          render();
        })
        .catch(function (err) {
          S.compareLoading = false;
          S.compareError = err.message || 'Comparison failed';
          render();
        });
    }

    /* ---- top-level actions ---- */
    if (act === 'role-new') { openRoleModal(false); return; }
    if (act === 'permission-new') { openPermissionModal(false); return; }
    if (act === 'permission-edit') { openPermissionModal(true, key); return; }
    if (act === 'compare-open') {
      var allR = allRoles();
      if (!allR.length) {
        notify('No roles available to compare.', true);
        return;
      }
      S.compareA = (S.roles.core_roles[0] || allR[0] || {}).id || '';
      S.compareB = (S.roles.core_roles[1] || allR[1] || allR[0] || {}).id || '';
      if (S.compareA === S.compareB && allR.length > 1) {
        S.compareB = allR[1].id;
      }
      S.compareResult = null;
      S.compareLoading = true;
      S.compareError = null;
      S.modal = { type: 'compare', title: 'Compare Role Permissions', form: {} };
      render();
      runCompare();
      return;
    }
    if (act === 'compare-run') {
      runCompare();
      return;
    }
    if (act === 'assignments') {
      S.modal = { type: 'assign', title: 'Manage Role Assignments',
        form: { rpAssignRole: S.selectedRoleId && S.selectedRoleId.indexOf('ROL-') === 0 ? S.selectedRoleId : '',
                rpAssignSearch: '' } };
      fetchAssignUsers(); render(); return;
    }
    if (act === 'assign-toggle') {
      var op = t.getAttribute('data-op');
      var roleId = (S.modal.form || {}).rpAssignRole;
      withBusy(api('/api/roles-mgmt/user-roles', 'POST',
        { username: username, role_id: roleId, op: op }), op === 'assign' ? 'Role assigned' : 'Role revoked')
        .then(function () { fetchAssignUsers(); return Promise.all([reloadRoles(), loadUserDetail(), loadRoleDetail(), loadAudit()]); })
        .then(function () { render(); }).catch(function () {});
      return;
    }

    /* ---- role form ---- */
    if (act === 'modal-module') {
      var val = t.getAttribute('data-value');
      var f = S.modal.form;
      f.modules = f.modules || [];
      var ix = f.modules.indexOf(val);
      if (t.checked && ix === -1) f.modules.push(val);
      if (!t.checked && ix !== -1) f.modules.splice(ix, 1);
      return;
    }
    if (act === 'role-submit') {
      var f2 = S.modal.form || {};
      var perms = {};
      (f2.modules || []).forEach(function (mod) { perms[mod] = ['view']; });
      var body = {
        name: f2.rpRoleName, identifier: f2.rpRoleIdent, description: f2.rpRoleDesc,
        category: f2.rpRoleCategory, default_portal: f2.rpRolePortal,
        status: f2.rpRoleStatus, permissions: perms, scopes: {}, portals: []
      };
      if (!S.modal.edit) { body.base_role = f2.rpRoleBase || 'TEACHER'; }
      else { body.expected_updated_at = (currentRole() || {}).updated_at; }
      var url = S.modal.edit
        ? '/api/roles-mgmt/roles/' + encodeURIComponent(S.selectedRoleId) + '/edit'
        : '/api/roles-mgmt/roles/create';
      withBusy(api(url, 'POST', body), S.modal.edit ? 'Role updated' : 'Role created')
        .then(function (r) {
          S.modal = null;
          if (r.role) S.selectedRoleId = r.role.id;
          return refreshAfterWrite();
        }).catch(function () {});
      return;
    }
    if (act === 'permission-submit') {
      var pf = S.modal.form || {};
      var module = pf.rpPermModule === '__new__' ? (pf.rpPermNewModule || '') : pf.rpPermModule;
      var pbody = {
        name: pf.rpPermName, key: pf.rpPermKey, description: pf.rpPermDesc,
        module: module, action: pf.rpPermAction, portal: pf.rpPermPortal,
        scope: pf.rpPermScope, target_page: pf.rpPermPage
      };
      var purl = S.modal.edit
        ? '/api/roles-mgmt/permissions/' + encodeURIComponent(S.modal.key)
        : '/api/roles-mgmt/permissions';
      var pmethod = S.modal.edit ? 'PUT' : 'POST';
      if (S.modal.edit) pbody.expected_updated_at = (S.modal.def || {}).updated_at;
      withBusy(api(purl, pmethod, pbody),
        S.modal.edit ? 'Permission definition updated' : 'Permission definition created')
        .then(function () { S.modal = null; return refreshAfterWrite(); })
        .catch(function () {});
      return;
    }
    if (act === 'permission-delete') {
      var def = (S.definitions.custom || []).filter(function (x) { return x.key === key; })[0] || {};
      openConfirm('Delete Permission Definition',
        'Remove "' + def.name + '" (' + key + ')? This only deletes the definition. ' +
        'No access grant is created or removed.', null, function () {
          withBusy(api('/api/roles-mgmt/permissions/' + encodeURIComponent(key) + '/delete', 'POST', {}),
            'Permission definition removed')
            .then(refreshAfterWrite).catch(function () {});
        }, true, 'Delete Definition');
      return;
    }

    /* ---- role directory / detail ---- */
    if (act === 'role-select') {
      S.selectedRoleId = id; S.permDraft = null; S.rolePerms = null; S.roleMembers = null;
      S.ngxLimits.rev = INIT.rev; S.ngxLimits.members = INIT.members;
      loadRoleDetail().then(render); render(); return;
    }
    if (act === 'role-edit') { openRoleModal(true); return; }
    if (act === 'role-duplicate') {
      withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(S.selectedRoleId) + '/duplicate', 'POST', {}),
        'Role duplicated').then(refreshAfterWrite).catch(function () {});
      return;
    }
    if (act === 'role-archive') {
      var role = currentRole() || {};
      var next = role.status === 'active' ? 'archived' : 'active';
      withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(S.selectedRoleId), 'PUT',
        { status: next, expected_updated_at: role.updated_at }),
        next === 'active' ? 'Role enabled' : 'Role disabled')
        .then(refreshAfterWrite).catch(function () {});
      return;
    }
    if (act === 'role-delete') {
      var dr = currentRole() || {};
      openConfirm('Delete Custom Role',
        'Permanently delete "' + dr.name + '"? The backend refuses deletion while any account still holds the role.',
        null, function () {
          withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(dr.id), 'DELETE',
            { expected_updated_at: dr.updated_at }), 'Role deleted')
            .then(function () {
              S.selectedRoleId = (S.roles.core_roles[0] || {}).id || '';
              return refreshAfterWrite();
            }).catch(function () {});
        }, true, 'Delete Role');
      return;
    }
    if (act === 'role-assign') {
      S.modal = { type: 'assign', title: 'Manage Role Assignments',
        form: { rpAssignRole: S.selectedRoleId, rpAssignSearch: '' } };
      fetchAssignUsers(); render(); return;
    }

    /* ---- permission matrix ---- */
    if (act === 'cat-select-all' || act === 'cat-clear') {
      e.preventDefault();
      var catName = t.getAttribute('data-category');
      var cat = (S.registry.categories || []).filter(function (c) { return c.category === catName; })[0];
      if (cat) {
        var mod = S.permDraft || (S.permDraft = {});
        cat.modules.forEach(function (m) {
          if (act === 'cat-select-all') mod[m.id] = m.actions.slice();
          else delete mod[m.id];
        });
        S.permDirty = true; render();
      }
      return;
    }
    if (act === 'perm-reset') {
      S.permDraft = clone((S.rolePerms || {}).permissions || {});
      S.permDirty = false; render(); return;
    }
    if (act === 'perm-save') { confirmAndSavePermissions(); return; }
    if (act === 'perm-rollback') {
      withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(S.selectedRoleId) + '/rollback', 'POST',
        { revision_index: Number(t.getAttribute('data-index')) }), 'Revision restored')
        .then(refreshAfterWrite).catch(function () {});
      return;
    }
    if (act === 'role-portals-save') {
      var target = S.tab === 'portals' ? S.selectedPortalRole : S.selectedRoleId;
      var rrole = allRoles().filter(function (r) { return r.id === target; })[0] || {};
      withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(target) + '/portals', 'PUT',
        { portals: S.rolePortalDraft || [], expected_updated_at: rrole.updated_at }),
        'Portal access saved').then(refreshAfterWrite).catch(function () {});
      return;
    }
    if (act === 'portal-role-reset') {
      var pr = (S.roles.custom_roles || []).filter(function (r) { return r.id === S.selectedPortalRole; })[0];
      S.rolePortalDraft = clone((pr && pr.portals) || []); render(); return;
    }
    if (act === 'portal-mode') { S.portalMode = t.getAttribute('data-mode'); S.rolePortalDraft = null; render(); return; }
    if (act === 'portal-role-select') {
      S.selectedPortalRole = id;
      var sel = (S.roles.custom_roles || []).filter(function (r) { return r.id === id; })[0];
      S.rolePortalDraft = clone((sel && sel.portals) || []);
      render(); return;
    }
    if (act === 'member-remove') {
      withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(S.selectedRoleId) + '/members/remove',
        'POST', { username: username }), 'Member removed')
        .then(refreshAfterWrite).catch(function () {});
      return;
    }

    /* ---- user access ---- */
    if (act === 'user-select') {
      S.selectedUser = username; S.draft = null; S.effective = null; S.preview = null;
      S.userRoles = null;
      loadUserDetail().then(render); render(); return;
    }
    if (act === 'user-more') { S.userOffset = S.users.length; fetchUsers(false).then(render); return; }
    if (act === 'user-less') { fetchUsers(true).then(render); return; }
    if (act === 'user-role-assign' || act === 'user-role-revoke') {
      var rid = act === 'user-role-assign'
        ? (document.getElementById('rpUserRoleAssign') || {}).value
        : t.getAttribute('data-role-id');
      if (!rid) return;
      var opx = act === 'user-role-assign' ? 'assign' : 'revoke';
      var run = function () {
        withBusy(api('/api/roles-mgmt/user-roles', 'POST',
          { username: S.selectedUser, role_id: rid, op: opx }),
          opx === 'assign' ? 'Role assigned' : 'Role revoked')
          .then(function () {
            try { window.sessionStorage.removeItem('ngis-nav-access-v2'); } catch (err) {}
            if (window.NGIS_SIDEBAR && typeof window.NGIS_SIDEBAR.refreshAccess === 'function') {
              window.NGIS_SIDEBAR.refreshAccess();
            }
            return Promise.all([reloadRoles(), loadUserDetail(), loadAudit()]);
          }).then(render).catch(function () {});
      };
      if (opx === 'revoke') {
        openConfirm('Revoke Role', 'Remove this custom role from ' + S.selectedUser +
          '? The account keeps its core institutional identity.', null, run, true, 'Revoke Role');
      } else run();
      return;
    }
    if (act === 'hide-deny') {
      setTri('page', key, '', 'hidden', true);
      setTri('page', key, '', 'deny', false);
      render(); return;
    }
    if (act === 'toggle-actions') { S.showAllActions = !S.showAllActions; render(); return; }
    if (act === 'preview') {
      api('/api/roles-mgmt/preview', 'POST',
        { username: S.selectedUser, overrides: S.draft || emptyDraft() })
        .then(function (r) { S.preview = r.effective; notify('Effective access preview computed'); })
        .catch(function (err) { notify(err.message, true); });
      return;
    }
    if (act === 'clear') {
      S.draft = emptyDraft(); S.preview = null; render(); return;
    }
    if (act === 'save') {
      withBusy(api('/api/roles-mgmt/overrides/' + encodeURIComponent(S.selectedUser), 'PUT',
        S.draft || emptyDraft()), 'Access overrides applied')
        .then(function () {
          try { window.sessionStorage.removeItem('ngis-nav-access-v2'); } catch (err) {}
          if (window.NGIS_SIDEBAR && typeof window.NGIS_SIDEBAR.refreshAccess === 'function') {
            window.NGIS_SIDEBAR.refreshAccess();
          }
          return Promise.all([fetchUsers(false), loadUserDetail(), loadAudit()]);
        }).then(render).catch(function () {});
      return;
    }

    /* ---- activity ---- */
    if (act === 'audit-page') {
      S.auditPage += Number(t.getAttribute('data-dir') || '1');
      loadAudit(); return;
    }
    if (act === 'audit-detail') {
      S.modal = { type: 'audit', title: 'Audit Event Detail', index: Number(t.getAttribute('data-index')) };
      render(); return;
    }
  }

  function confirmAndSavePermissions() {
    var diff = permDiff();
    var sensitive = diff.added.filter(function (c) {
      return (SENSITIVE[c.module] || []).indexOf(c.action) !== -1;
    });
    var run = function () {
      var role = currentRole() || {};
      withBusy(api('/api/roles-mgmt/roles/' + encodeURIComponent(S.selectedRoleId) + '/permissions/save', 'PUT',
        { permissions: S.permDraft || {}, custom_permission_keys: S.customKeys || [],
          expected_updated_at: role.updated_at }), 'Permissions saved')
        .then(refreshAfterWrite).catch(function () {});
    };
    if (!sensitive.length) { run(); return; }
    var changes = diff.added.map(function (c) {
      return { tag: 'Grant', tone: 'warn', text: c.module + ' → ' + actionLabel(c.action) };
    }).concat(diff.removed.map(function (c) {
      return { tag: 'Revoke', tone: '', text: c.module + ' → ' + actionLabel(c.action) };
    }));
    openConfirm('Confirm Sensitive Permission Changes',
      'These grants affect privileged operations. They are validated against your delegated authority by the server, ' +
      'and the change will be recorded in the audit log.', changes, run, false, 'Save Changes');
  }

  function fetchAssignUsers() {
    var q = (S.modal && S.modal.form && S.modal.form.rpAssignSearch) || '';
    return api('/api/roles-mgmt/users/paged?limit=25&offset=0&q=' + encodeURIComponent(q))
      .then(function (d) { S.assignUsers = d.users || []; if (S.modal) render(true); })
      .catch(function (err) { notify(err.message, true); });
  }

  function onChange(e) {
    var el = e.target;
    var fieldId = el.getAttribute && el.getAttribute('data-field');
    if (fieldId && S.modal) {
      S.modal.form[fieldId] = el.value;
      S.modal.error = null;
      if (fieldId === 'rpRoleName' && !S.modal.edit && !S.modal.form.rpRoleIdentTouched) {
        S.modal.form.rpRoleIdent = String(el.value).toLowerCase()
          .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 38);
      }
      if (fieldId === 'rpRoleIdent') S.modal.form.rpRoleIdentTouched = true;
      // Re-render only when dependent option lists or the modal layout change.
      if (fieldId === 'rpPermPortal' || fieldId === 'rpPermModule' || fieldId === 'rpAssignRole' ||
          fieldId === 'rpCompareA' || fieldId === 'rpCompareB') {
        if (fieldId === 'rpCompareA') S.compareA = el.value;
        if (fieldId === 'rpCompareB') S.compareB = el.value;
        if (fieldId === 'rpAssignRole') fetchAssignUsers();
        else if (fieldId === 'rpCompareA' || fieldId === 'rpCompareB') {
          S.compareLoading = true;
          S.compareError = null;
          render(true);
          api('/api/roles-mgmt/compare?a=' + encodeURIComponent(S.compareA) + '&b=' + encodeURIComponent(S.compareB))
            .then(function (r) { S.compareResult = r; S.compareLoading = false; render(true); })
            .catch(function (err) { S.compareLoading = false; S.compareError = err.message || 'Comparison failed'; render(true); });
        } else render(true);
      }
      return;
    }
    var kind = el.getAttribute && el.getAttribute('data-kind');
    if (kind) {
      var key = el.getAttribute('data-key') || el.getAttribute('data-module') || '';
      var action = el.getAttribute('data-action') || '';
      var value = el.value;
      var isVisibility = el.getAttribute('data-visibility') === '1';
      if (kind === 'perm') {
        var mod = S.permDraft || (S.permDraft = {});
        var list = mod[key] || (mod[key] = []);
        var i = list.indexOf(action);
        if (el.checked && i === -1) {
          list.push(action);
          if (action !== 'view' && list.indexOf('view') === -1) {
            list.push('view');
            var row = el.closest('tr');
            if (row) { var vcb = row.querySelector('[data-action="view"]'); if (vcb) vcb.checked = true; }
          }
        }
        if (!el.checked && i !== -1) {
          list.splice(i, 1);
          if (action === 'view') {
            list.length = 0;
            var row2 = el.closest('tr');
            if (row2) row2.querySelectorAll('.rp-check').forEach(function (cb) { cb.checked = false; });
          }
        }
        if (!list.length) delete mod[key];
        S.permDirty = true;
        // Keep both desktop and mobile representations in sync without a full
        // re-render (which would lose focus); update matching checkboxes only.
        S.root.querySelectorAll('input[data-kind="perm"][data-key="' + key +
          '"][data-action="' + action + '"]').forEach(function (cb) {
          if (cb !== el) cb.checked = el.checked;
        });
        var saveBar = S.root.querySelector('.rp-savebar');
        if (saveBar) {
          var d = permDiff();
          saveBar.querySelector('.rp-muted').textContent =
            d.added.length + d.removed.length + ' pending change(s)';
          var btn = saveBar.querySelector('[data-act="perm-save"]');
          if (btn) btn.disabled = false;
          var reset = saveBar.querySelector('[data-act="perm-reset"]');
          if (reset) reset.disabled = false;
        }
        return;
      }
      if (kind === 'roleportal') {
        var v = el.getAttribute('data-value');
        var arr = S.rolePortalDraft || (S.rolePortalDraft = []);
        var ix = arr.indexOf(v);
        if (el.checked && ix === -1) arr.push(v);
        if (!el.checked && ix !== -1) arr.splice(ix, 1);
        S.root.querySelectorAll('input[data-kind="roleportal"][data-value="' + v + '"]')
          .forEach(function (cb) { if (cb !== el) cb.checked = el.checked; });
        return;
      }
      setTri(kind, key, action, value, isVisibility);
      render();
      return;
    }
    var act = el.getAttribute && el.getAttribute('data-act');
    if (act === 'page-portal') { S.pagePortal = el.value; render(); return; }
    if (act === 'audit-action') { S.auditAction = el.value; S.auditPage = 1; loadAudit(); return; }
    if (act === 'audit-size') { S.auditPageSize = Number(el.value); S.auditPage = 1; loadAudit(); return; }
    if (act === 'user-role') { S.userRole = el.value; fetchUsers(true).then(render); return; }
    if (act === 'user-campus') { S.userCampus = el.value; fetchUsers(true).then(render); return; }
  }

  function onInput(e) {
    var el = e.target;
    var act = el.getAttribute && el.getAttribute('data-act');
    var fieldId = el.getAttribute && el.getAttribute('data-field');
    if (fieldId && S.modal) {
      S.modal.form[fieldId] = el.value;
      S.modal.error = null;
      if (fieldId === 'rpRoleName' && !S.modal.edit && !S.modal.form.rpRoleIdentTouched) {
        var ident = String(el.value).toLowerCase().replace(/[^a-z0-9]+/g, '-')
          .replace(/^-|-$/g, '').slice(0, 38);
        S.modal.form.rpRoleIdent = ident;
        var identEl = document.getElementById('rpRoleIdent');
        if (identEl) identEl.value = ident;
      }
      if (fieldId === 'rpAssignSearch') fetchAssignUsers();
      return;
    }
    if (act === 'user-search') { S.userQ = el.value; fetchUsers(true).then(function () { render(true); }); }
    else if (act === 'page-search') { S.pageSearch = el.value; render(true); }
    else if (act === 'audit-search') { S.auditSearch = el.value; S.auditPage = 1; loadAudit(); }
    else if (act === 'role-search') { S.roleSearch = el.value; render(true); }
  }

  /* ------------------------------------------------------------------- init */
  R.init = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root || root.getAttribute('data-roles-ready')) return;
    root.setAttribute('data-roles-ready', '1');
    S.root = root;
    root.addEventListener('click', onClick);
    root.addEventListener('change', onChange);
    root.addEventListener('input', onInput);
    root.addEventListener('toggle', function (e) {
      var d = e.target;
      if (d && d.getAttribute && d.getAttribute('data-ngx-key')) {
        S.ngxOpen[d.getAttribute('data-ngx-key')] = d.open;
      }
    }, true);
    document.addEventListener('keydown', function (e) {
      if (!S.modal) return;
      if (e.key === 'Escape') { e.preventDefault(); closeModal(); return; }
      if (e.key !== 'Tab') return;
      var box = (S.modalEl || S.root).querySelector('.rp-modal');
      if (!box) return;
      var focusable = box.querySelectorAll(
        'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea, [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    loadBase().then(function () { render(); })
      .catch(function (err) {
        root.innerHTML = '<div class="rp-load-error"><strong>Access control workspace unavailable</strong>' +
          '<p>' + esc(err.message) + '</p></div>';
      });
  };

  R.state = S;
})(window, document);
