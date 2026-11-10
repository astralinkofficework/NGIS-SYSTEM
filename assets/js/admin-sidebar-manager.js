/**
 * NGIS Global Sidebar Manager
 *
 * Centralized navigation configuration workspace for every NGIS portal sidebar.
 * Backed by the navigation configuration store (/api/nav/*) so published
 * navigation reaches every portal without editing each portal's HTML.
 *
 * Workflow: Edit → Preview → Validate → Publish (with version history + rollback).
 *
 * Vanilla JavaScript only. Consumes the shared CMS shell (window.CMS) for
 * modals and toasts, and the shared layout engine reads /api/nav/published.
 */

(function () {
  'use strict';

  var PORTAL_ROLE_SCOPE = {
    admin: 'Admin, Super Admin',
    principal: 'Principal',
    teacher: 'Teacher',
    student: 'Student'
  };

  var COMMON_ICONS = [
    'dashboard', 'space_dashboard', 'menu_open', 'splitscreen', 'group', 'manage_accounts',
    'co_present', 'school', 'apartment', 'calendar_month', 'badge', 'local_activity',
    'grid_view', 'inventory_2', 'campaign', 'notifications', 'person', 'logout',
    'settings', 'history', 'monitor_heart', 'assignment', 'quiz', 'menu_book',
    'event_note', 'insights', 'verified_user', 'business', 'admin_panel_settings'
  ];

  function clone(o) { return JSON.parse(JSON.stringify(o == null ? null : o)); }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function uid(prefix) {
    return prefix + '-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 6);
  }

  function iconHtml(icon) {
    if (!icon) return '';
    var t = String(icon).trim();
    if (t.indexOf('<svg') === 0) return '<span class="sv-svg">' + t + '</span>';
    if (t.indexOf('ph ') === 0 || t.indexOf('ph-') === 0) return '<i class="' + esc(t) + '" aria-hidden="true"></i>';
    return '<span class="material-symbols-outlined" aria-hidden="true">' + esc(t) + '</span>';
  }

  var NavMgr = {
    ready: false,
    booted: false,

    portal: 'admin',
    portals: [],
    state: null,
    working: null,          // { brand, meta, groups: [...] }
    selectedId: null,
    collapsed: {},          // node/group id -> true (collapsed)
    undoStack: [],
    dirty: false,
    routes: [],
    viewport: 'desktop',
    previewCollapsed: false,
    search: '',
    drag: null,
    dropPlan: null,
    editSessionOpen: false,

    // ── DOM ──
    dom: {},

    // ────────────────────────────────────────────────────────────
    // Lifecycle
    // ────────────────────────────────────────────────────────────

    ensureLoaded: function () {
      var self = this;
      if (!this.ready) this.init();
      if (this.booted) return;
      this.booted = true;
      this.loadPortals().then(function () { return self.selectPortal(self.portal); });
    },

    init: function () {
      if (this.ready) return;
      this.ready = true;

      this.dom = {
        portalSelect: document.getElementById('sgmPortalSelect'),
        statusChip: document.getElementById('sgmStatusChip'),
        search: document.getElementById('sgmSearch'),
        btnUndo: document.getElementById('sgmBtnUndo'),
        btnHealth: document.getElementById('sgmBtnHealth'),
        btnValidate: document.getElementById('sgmBtnValidate'),
        btnVersions: document.getElementById('sgmBtnVersions'),
        btnDefaults: document.getElementById('sgmBtnDefaults'),
        btnSave: document.getElementById('sgmBtnSave'),
        btnPublish: document.getElementById('sgmBtnPublish'),
        btnAddGroup: document.getElementById('sgmBtnAddGroup'),
        btnAddItem: document.getElementById('sgmBtnAddItem'),
        btnAddFromSettings: document.getElementById('sgmBtnAddFromSettings'),
        tree: document.getElementById('sgmTree'),
        preview: document.getElementById('sgmPreview'),
        settings: document.getElementById('sgmSettings'),
        health: document.getElementById('sgmHealth'),
        viewportBtns: document.querySelectorAll('[data-sgm-viewport]'),
        previewCollapseBtn: document.getElementById('sgmPreviewCollapse')
      };

      this.bindEvents();
      this.loadRoutes();
    },

    bindEvents: function () {
      var self = this;
      var d = this.dom;

      if (d.portalSelect) {
        d.portalSelect.addEventListener('change', function () { self.selectPortal(this.value); });
      }
      if (d.search) {
        d.search.addEventListener('input', function () {
          self.search = this.value.trim().toLowerCase();
          self.renderTree();
        });
      }
      if (d.btnUndo) d.btnUndo.addEventListener('click', function () { self.undo(); });
      if (d.btnHealth) d.btnHealth.addEventListener('click', function () { self.loadHealth(); });
      if (d.btnValidate) d.btnValidate.addEventListener('click', function () { self.validateDraft(); });
      if (d.btnVersions) d.btnVersions.addEventListener('click', function () { self.openVersions(); });
      if (d.btnDefaults) d.btnDefaults.addEventListener('click', function () { self.restoreDefaults(); });
      if (d.btnSave) d.btnSave.addEventListener('click', function () { self.saveDraft(false); });
      if (d.btnPublish) d.btnPublish.addEventListener('click', function () { self.publish(); });
      if (d.btnAddGroup) d.btnAddGroup.addEventListener('click', function () { self.addGroup(); });
      if (d.btnAddItem) d.btnAddItem.addEventListener('click', function () { self.addItem(); });
      if (d.btnAddFromSettings) d.btnAddFromSettings.addEventListener('click', function () { self.addItem(); });

      // Viewport switch for the live preview
      Array.prototype.forEach.call(d.viewportBtns, function (btn) {
        btn.addEventListener('click', function () {
          Array.prototype.forEach.call(d.viewportBtns, function (b) { b.classList.remove('active'); });
          btn.classList.add('active');
          self.viewport = btn.dataset.sgmViewport;
          if (d.preview) d.preview.className = 'sgm-preview mode-' + self.viewport + (self.previewCollapsed ? ' is-collapsed' : '');
        });
      });

      // Collapsed-sidebar preview toggle
      if (d.previewCollapseBtn) {
        d.previewCollapseBtn.addEventListener('click', function () {
          self.previewCollapsed = !self.previewCollapsed;
          this.setAttribute('aria-pressed', self.previewCollapsed ? 'true' : 'false');
          this.classList.toggle('active', self.previewCollapsed);
          if (d.preview) d.preview.className = 'sgm-preview mode-' + self.viewport + (self.previewCollapsed ? ' is-collapsed' : '');
        });
      }

      // Delegated tree interactions (selection, toggles, actions)
      if (d.tree) {
        d.tree.addEventListener('click', function (e) { self.onTreeClick(e); });
        d.tree.addEventListener('keydown', function (e) { self.onTreeKeydown(e); });

        // Drag and drop
        d.tree.addEventListener('dragstart', function (e) { self.onDragStart(e); });
        d.tree.addEventListener('dragover', function (e) { self.onDragOver(e); });
        d.tree.addEventListener('dragleave', function (e) { self.onDragLeave(e); });
        d.tree.addEventListener('drop', function (e) { self.onDrop(e); });
        d.tree.addEventListener('dragend', function () { self.clearDrag(); });
      }

      // Settings form (delegated)
      if (d.settings) {
        d.settings.addEventListener('input', function (e) { self.onSettingsInput(e); });
        d.settings.addEventListener('change', function (e) { self.onSettingsChange(e); });
        d.settings.addEventListener('click', function (e) { self.onSettingsClick(e); });

        // Snapshot once per text-editing session so field edits are undoable.
        d.settings.addEventListener('focusin', function (e) {
          var el = e.target;
          if (!el || !el.tagName) return;
          var isText = (el.tagName === 'TEXTAREA') ||
            (el.tagName === 'INPUT' && el.type !== 'checkbox' && el.type !== 'radio');
          if (!isText || self.editSessionOpen) return;
          self.editSessionOpen = true;
          self.pushUndo();
        });
        d.settings.addEventListener('focusout', function () { self.editSessionOpen = false; });
      }
    },

    // ────────────────────────────────────────────────────────────
    // Data loading
    // ────────────────────────────────────────────────────────────

    loadRoutes: function () {
      var self = this;
      fetch('/api/nav/routes')
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res && res.success) self.routes = res.data || [];
        })
        .catch(function () { self.routes = []; });
    },

    loadPortals: function () {
      var self = this;
      return fetch('/api/nav/portals')
        .then(function (r) { return r.json(); })
        .then(function (res) {
          self.portals = (res && res.success && res.data) ? res.data : [];
          if (self.dom.portalSelect) {
            self.dom.portalSelect.innerHTML = self.portals.map(function (p) {
              return '<option value="' + esc(p.portal) + '">' + esc(p.label) + '</option>';
            }).join('');
            if (self.portals.length && !self.portals.some(function (p) { return p.portal === self.portal; })) {
              self.portal = self.portals[0].portal;
            }
            self.dom.portalSelect.value = self.portal;
          }
        })
        .catch(function () {
          if (self.dom.tree) {
            self.dom.tree.innerHTML = '<div class="cms-error">Unable to load the portal list. Verify the /api/nav/portals endpoint.</div>';
          }
        });
    },

    selectPortal: function (portal) {
      var self = this;
      if (!portal) return Promise.resolve();
      this.portal = portal;
      this.selectedId = null;
      this.undoStack = [];
      this.dirty = false;
      if (this.dom.portalSelect) this.dom.portalSelect.value = portal;
      if (this.dom.tree) {
        this.dom.tree.innerHTML = '<div class="cms-loading"><span class="cms-spinner" aria-hidden="true"></span><span>Loading navigation…</span></div>';
      }

      return fetch('/api/nav/config?portal=' + encodeURIComponent(portal))
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (!res || !res.success) {
            if (self.dom.tree) {
              self.dom.tree.innerHTML = '<div class="cms-error">' + esc((res && res.error) || 'Unable to load navigation configuration.') + '</div>';
            }
            return;
          }
          self.state = res.data;
          var source = res.data.draft || res.data.published || {};
          self.working = {
            brand: source.brand != null ? source.brand : res.data.brand,
            meta: source.meta != null ? source.meta : res.data.meta,
            groups: clone(source.groups || [])
          };
          self.updateStatusChip(res.data.status);
          self.updateUndoBtn();
          self.renderTree();
          self.renderPreview();
          self.renderSettings();
          self.hideHealth();
        })
        .catch(function () {
          if (self.dom.tree) {
            self.dom.tree.innerHTML = '<div class="cms-error">Network error loading navigation configuration.</div>';
          }
        });
    },

    reloadState: function () {
      var self = this;
      return fetch('/api/nav/config?portal=' + encodeURIComponent(this.portal))
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res && res.success) {
            self.state = res.data;
            self.updateStatusChip(res.data.status);
          }
        });
    },

    // ────────────────────────────────────────────────────────────
    // Data helpers
    // ────────────────────────────────────────────────────────────

    walk: function (cb) {
      var groups = (this.working && this.working.groups) || [];
      for (var gi = 0; gi < groups.length; gi++) {
        var links = groups[gi].links || [];
        for (var i = 0; i < links.length; i++) {
          this._walkItem(links[i], {
            group: groups[gi], groupIndex: gi, parent: null,
            siblings: links, index: i, depth: 1
          }, cb);
        }
      }
    },

    _walkItem: function (item, meta, cb) {
      cb(item, meta);
      var children = item.children || [];
      for (var j = 0; j < children.length; j++) {
        this._walkItem(children[j], {
          group: meta.group, groupIndex: meta.groupIndex, parent: item,
          siblings: children, index: j, depth: meta.depth + 1
        }, cb);
      }
    },

    findNode: function (id) {
      var found = null;
      this.walk(function (item, meta) {
        if (item.id === id) found = { item: item, meta: meta };
      });
      return found;
    },

    findGroup: function (gid) {
      var groups = (this.working && this.working.groups) || [];
      for (var i = 0; i < groups.length; i++) {
        if (groups[i].id === gid) return { group: groups[i], index: i };
      }
      return null;
    },

    itemCount: function (group) {
      var n = 0;
      (function rec(items) {
        (items || []).forEach(function (it) {
          n += 1;
          if (it.children) rec(it.children);
        });
      })(group.links || []);
      return n;
    },

    isDescendant: function (ancestorId, maybeChildId) {
      var loc = this.findNode(ancestorId);
      if (!loc) return false;
      var found = false;
      (function rec(item) {
        (item.children || []).forEach(function (c) {
          if (c.id === maybeChildId) found = true;
          rec(c);
        });
      })(loc.item);
      return found;
    },

    extractItem: function (id) {
      var loc = this.findNode(id);
      if (!loc) return null;
      loc.meta.siblings.splice(loc.meta.index, 1);
      return loc.item;
    },

    allIds: function () {
      var ids = {};
      this.walk(function (item) { ids[item.id] = true; });
      return ids;
    },

    // ────────────────────────────────────────────────────────────
    // History (uncommitted changes)
    // ────────────────────────────────────────────────────────────

    pushUndo: function () {
      this.undoStack.push(clone((this.working && this.working.groups) || []));
      if (this.undoStack.length > 60) this.undoStack.shift();
      this.updateUndoBtn();
    },

    undo: function () {
      if (!this.undoStack.length) return;
      this.working.groups = this.undoStack.pop();
      this.dirty = true;
      var ids = this.allIds();
      if (this.selectedId && !ids[this.selectedId]) this.selectedId = null;
      this.updateUndoBtn();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
      this.markDirty();
    },

    updateUndoBtn: function () {
      if (this.dom.btnUndo) this.dom.btnUndo.disabled = this.undoStack.length === 0;
    },

    markDirty: function () {
      this.dirty = true;
      this.updateStatusChip('draft');
    },

    updateStatusChip: function (status) {
      var el = this.dom.statusChip;
      if (!el) return;
      if (status === 'draft') {
        el.className = 'cms-pill cms-pill-lock';
        el.textContent = 'Draft (unpublished)';
      } else {
        el.className = 'cms-pill cms-pill-on';
        el.textContent = 'Published';
      }
    },

    // ────────────────────────────────────────────────────────────
    // Tree rendering
    // ────────────────────────────────────────────────────────────

    renderTree: function () {
      var el = this.dom.tree;
      if (!el || !this.working) return;
      var groups = this.working.groups || [];

      if (!groups.length) {
        el.innerHTML = '<div class="cms-empty">No navigation groups yet. Use “Group” to create one, then add items.</div>';
        return;
      }

      var html = '';
      for (var gi = 0; gi < groups.length; gi++) {
        html += this.renderGroup(groups[gi], gi, groups.length);
      }
      el.innerHTML = html;
    },

    matchesSearch: function (item) {
      if (!this.search) return true;
      var hay = (item.label || '') + ' ' + (item.id || '') + ' ' + (item.href || '');
      return hay.toLowerCase().indexOf(this.search) !== -1;
    },

    // Does a group (or any descendant) match the current search?
    groupMatches: function (group) {
      var term = this.search;
      if (!term) return true;
      var hit = false;
      (function rec(items) {
        (items || []).forEach(function (it) {
          if (hit) return;
          var hay = (it.label || '') + ' ' + (it.id || '') + ' ' + (it.href || '');
          if (hay.toLowerCase().indexOf(term) !== -1) { hit = true; return; }
          if (it.children) rec(it.children);
        });
      })(group.links || []);
      if (!hit) {
        var gl = (group.label || '') + ' ' + (group.id || '');
        if (gl.toLowerCase().indexOf(term) !== -1) hit = true;
      }
      return hit;
    },

    renderGroup: function (group, gi, total) {
      if (!this.groupMatches(group)) return '';

      var collapsed = !!this.collapsed['grp:' + group.id];
      var links = group.links || [];
      var nodesHtml = '';
      for (var i = 0; i < links.length; i++) {
        nodesHtml += this.renderNode(links[i], 1);
      }

      return '' +
        '<div class="sgm-group' + (collapsed ? ' collapsed' : '') + '" data-group-id="' + esc(group.id) + '">' +
          '<div class="sgm-group-head" draggable="true" data-group-id="' + esc(group.id) + '">' +
            '<span class="material-symbols-outlined sgm-drag" aria-hidden="true">drag_indicator</span>' +
            '<button type="button" class="sgm-group-caret" data-toggle-group="' + esc(group.id) + '" aria-expanded="' + (collapsed ? 'false' : 'true') + '" aria-label="Toggle group">' +
              '<span class="material-symbols-outlined" aria-hidden="true">expand_more</span>' +
            '</button>' +
            (group.icon ? iconHtml(group.icon) : '') +
            '<span class="sgm-group-name">' + esc(group.label || '(untitled group)') + '</span>' +
            '<span class="sgm-group-count">' + this.itemCount(group) + '</span>' +
            '<span class="sgm-node-actions">' +
              '<button type="button" class="cms-icon-btn" title="Move group up" data-move-group="-1" data-group-id="' + esc(group.id) + '"' + (gi === 0 ? ' disabled' : '') + '><span class="material-symbols-outlined" style="font-size:16px">arrow_upward</span></button>' +
              '<button type="button" class="cms-icon-btn" title="Move group down" data-move-group="1" data-group-id="' + esc(group.id) + '"' + (gi === total - 1 ? ' disabled' : '') + '><span class="material-symbols-outlined" style="font-size:16px">arrow_downward</span></button>' +
              '<button type="button" class="cms-icon-btn" title="Rename group" data-rename-group="' + esc(group.id) + '"><span class="material-symbols-outlined" style="font-size:16px">edit</span></button>' +
              '<button type="button" class="cms-icon-btn" title="Add item to group" data-add-item-to="' + esc(group.id) + '"><span class="material-symbols-outlined" style="font-size:16px">add</span></button>' +
              '<button type="button" class="cms-icon-btn danger" title="Delete group" data-delete-group="' + esc(group.id) + '"><span class="material-symbols-outlined" style="font-size:16px">delete</span></button>' +
            '</span>' +
          '</div>' +
          '<div class="sgm-group-links">' + nodesHtml + '</div>' +
        '</div>';
    },

    renderNode: function (item, depth) {
      var self = this;

      // Search filtering: keep ancestors of matching descendants.
      var hasChildren = !!(item.children && item.children.length);
      var childMatches = false;
      if (this.search) {
        (function rec(n) {
          (n.children || []).forEach(function (c) {
            if (self.matchesSearch(c)) childMatches = true;
            rec(c);
          });
        })(item);
        if (!this.matchesSearch(item) && !childMatches) return '';
      }

      var collapsed = !!this.collapsed[item.id];
      var selected = item.id === this.selectedId;
      var hidden = item.visible === false;

      var childrenHtml = '';
      if (hasChildren) {
        childrenHtml = '<div class="sgm-node-children">';
        for (var i = 0; i < item.children.length; i++) {
          childrenHtml += this.renderNode(item.children[i], depth + 1);
        }
        childrenHtml += '</div>';
      }

      return '' +
        '<div class="sgm-node' + (collapsed ? ' collapsed' : '') + (selected ? ' selected' : '') + (hidden ? ' is-hidden' : '') + '"' +
          ' data-nav-id="' + esc(item.id) + '" draggable="true" role="treeitem" aria-level="' + depth + '"' +
          ' aria-selected="' + (selected ? 'true' : 'false') + '" tabindex="-1">' +
          (hasChildren
            ? '<button type="button" class="sgm-node-caret" data-toggle-node="' + esc(item.id) + '" aria-expanded="' + (collapsed ? 'false' : 'true') + '" aria-label="Toggle children"><span class="material-symbols-outlined" aria-hidden="true">expand_more</span></button>'
            : '<span class="sgm-node-caret placeholder" aria-hidden="true"><span class="material-symbols-outlined" style="font-size:16px">expand_more</span></span>') +
          (item.icon ? '<span class="material-symbols-outlined sgm-node-icon" aria-hidden="true">' + esc(item.icon) + '</span>' : '<span class="sgm-node-icon" aria-hidden="true"></span>') +
          '<span class="sgm-node-label">' + esc(item.label || item.id) + '</span>' +
          (item.badge ? '<span class="sv-badge">' + esc(item.badge) + '</span>' : '') +
          (item.locked ? '<span class="cms-pill cms-pill-lock">Mandatory</span>' : '') +
          '<span class="sgm-node-actions">' +
            '<button type="button" class="cms-icon-btn" title="Move up" data-move-item="-1" data-nav-id="' + esc(item.id) + '"><span class="material-symbols-outlined" style="font-size:16px">arrow_upward</span></button>' +
            '<button type="button" class="cms-icon-btn" title="Move down" data-move-item="1" data-nav-id="' + esc(item.id) + '"><span class="material-symbols-outlined" style="font-size:16px">arrow_downward</span></button>' +
            (item.locked
              ? '<span class="cms-icon-btn" title="Mandatory item"><span class="material-symbols-outlined" style="font-size:16px">lock</span></span>'
              : '<button type="button" class="cms-icon-btn" title="' + (hidden ? 'Show item' : 'Hide item') + '" data-toggle-visible="' + esc(item.id) + '"><span class="material-symbols-outlined" style="font-size:16px">' + (hidden ? 'visibility_off' : 'visibility') + '</span></button>') +
            '<button type="button" class="cms-icon-btn" title="Add child item" data-add-child="' + esc(item.id) + '"><span class="material-symbols-outlined" style="font-size:16px">subdirectory_arrow_right</span></button>' +
            (item.locked
              ? ''
              : '<button type="button" class="cms-icon-btn danger" title="Remove item" data-delete-item="' + esc(item.id) + '"><span class="material-symbols-outlined" style="font-size:16px">delete</span></button>') +
          '</span>' +
        '</div>' + childrenHtml;
    },

    onTreeClick: function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== 'function') return;

      var toggleGroup = t.closest('[data-toggle-group]');
      if (toggleGroup) { this.toggleGroup(toggleGroup.dataset.toggleGroup); return; }

      var toggleNode = t.closest('[data-toggle-node]');
      if (toggleNode) { this.toggleNode(toggleNode.dataset.toggleNode); return; }

      var moveGroup = t.closest('[data-move-group]');
      if (moveGroup) { this.moveGroup(moveGroup.dataset.groupId, parseInt(moveGroup.dataset.moveGroup, 10)); return; }

      var renameGroup = t.closest('[data-rename-group]');
      if (renameGroup) { this.renameGroup(renameGroup.dataset.renameGroup); return; }

      var addTo = t.closest('[data-add-item-to]');
      if (addTo) { this.addItem(addTo.dataset.addItemTo, null); return; }

      var delGroup = t.closest('[data-delete-group]');
      if (delGroup) { this.deleteGroup(delGroup.dataset.deleteGroup); return; }

      var moveItem = t.closest('[data-move-item]');
      if (moveItem) { this.moveItem(moveItem.dataset.navId, parseInt(moveItem.dataset.moveItem, 10)); return; }

      var toggleVis = t.closest('[data-toggle-visible]');
      if (toggleVis) { this.toggleVisible(toggleVis.dataset.toggleVisible); return; }

      var addChild = t.closest('[data-add-child]');
      if (addChild) { this.addChild(addChild.dataset.addChild); return; }

      var delItem = t.closest('[data-delete-item]');
      if (delItem) { this.deleteItem(delItem.dataset.deleteItem); return; }

      var node = t.closest('.sgm-node');
      if (node) { this.select(node.dataset.navId); }
    },

    onTreeKeydown: function (e) {
      var node = e.target && e.target.closest ? e.target.closest('.sgm-node') : null;
      if (!node) return;
      var id = node.dataset.navId;

      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        var nodes = Array.prototype.slice.call(this.dom.tree.querySelectorAll('.sgm-node'));
        var idx = nodes.indexOf(node);
        var next = e.key === 'ArrowDown' ? idx + 1 : idx - 1;
        if (next >= 0 && next < nodes.length) nodes[next].focus();
        return;
      }
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.select(id);
        return;
      }
      // Keyboard reorder alternative (Alt + Arrow)
      if (e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
        e.preventDefault();
        this.moveItem(id, e.key === 'ArrowUp' ? -1 : 1);
      }
    },

    select: function (id) {
      this.selectedId = id;
      this.editSessionOpen = false;
      Array.prototype.forEach.call(this.dom.tree.querySelectorAll('.sgm-node'), function (n) {
        var on = n.dataset.navId === id;
        n.classList.toggle('selected', on);
        n.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      this.renderPreview();
      this.renderSettings();
    },

    toggleGroup: function (gid) {
      var k = 'grp:' + gid;
      this.collapsed[k] = !this.collapsed[k];
      this.renderTree();
    },

    toggleNode: function (id) {
      this.collapsed[id] = !this.collapsed[id];
      this.renderTree();
    },

    // ────────────────────────────────────────────────────────────
    // Structural mutations
    // ────────────────────────────────────────────────────────────

    moveItem: function (id, dir) {
      var loc = this.findNode(id);
      if (!loc) return;
      var target = loc.meta.index + dir;
      if (target < 0 || target >= loc.meta.siblings.length) return;
      this.pushUndo();
      var arr = loc.meta.siblings;
      var tmp = arr[loc.meta.index];
      arr[loc.meta.index] = arr[target];
      arr[target] = tmp;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
    },

    moveGroup: function (gid, dir) {
      var groups = this.working.groups || [];
      var idx = -1;
      for (var i = 0; i < groups.length; i++) if (groups[i].id === gid) idx = i;
      if (idx < 0) return;
      var target = idx + dir;
      if (target < 0 || target >= groups.length) return;
      this.pushUndo();
      var tmp = groups[idx];
      groups[idx] = groups[target];
      groups[target] = tmp;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
    },

    toggleVisible: function (id) {
      var loc = this.findNode(id);
      if (!loc) return;
      if (loc.item.locked) return;
      this.pushUndo();
      loc.item.visible = loc.item.visible === false ? true : false;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
    },

    renameGroup: function (gid) {
      var loc = this.findGroup(gid);
      if (!loc) return;
      var name = window.prompt('Group name', loc.group.label || '');
      if (name == null) return;
      name = name.trim();
      if (!name || name === loc.group.label) return;
      this.pushUndo();
      loc.group.label = name;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
    },

    deleteGroup: function (gid) {
      var loc = this.findGroup(gid);
      if (!loc) return;
      var hasLocked = false;
      (function rec(items) {
        (items || []).forEach(function (it) {
          if (it.locked) hasLocked = true;
          if (it.children) rec(it.children);
        });
      })(loc.group.links || []);
      if (hasLocked) {
        window.alert('This group contains mandatory navigation items and cannot be removed.');
        return;
      }
      if (!window.confirm('Remove the group “' + (loc.group.label || gid) + '” and all its items from the draft navigation?')) return;
      this.pushUndo();
      this.working.groups.splice(loc.index, 1);
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
    },

    deleteItem: function (id) {
      var loc = this.findNode(id);
      if (!loc) return;
      if (loc.item.locked) {
        window.alert('This is mandatory system navigation and cannot be removed. You can reorder it, but it must remain.');
        return;
      }
      if (!window.confirm('Remove “' + (loc.item.label || id) + '” from the draft navigation? Backend modules and records are not deleted.')) return;
      this.pushUndo();
      loc.meta.siblings.splice(loc.meta.index, 1);
      if (this.selectedId === id) this.selectedId = null;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
    },

    addGroup: function () {
      var name = window.prompt('New navigation group name', 'New Group');
      if (name == null) return;
      name = name.trim();
      if (!name) return;
      this.pushUndo();
      this.working.groups = this.working.groups || [];
      this.working.groups.push({ id: uid('grp'), label: name, links: [] });
      this.markDirty();
      this.renderTree();
      this.renderPreview();
    },

    addItem: function (groupId, parentId) {
      var groups = this.working.groups || [];
      if (!groups.length) {
        window.alert('Create a navigation group first.');
        return;
      }
      var gid = groupId;
      if (!gid) gid = this.selectedGroupId() || groups[0].id;

      var item = {
        id: uid('nav'),
        label: 'New Item',
        icon: 'chevron_right',
        href: '',
        visible: true
      };

      this.pushUndo();
      if (parentId) {
        var ploc = this.findNode(parentId);
        if (ploc) {
          ploc.item.children = ploc.item.children || [];
          ploc.item.children.push(item);
        }
      } else {
        var gloc = this.findGroup(gid);
        if (gloc) {
          gloc.group.links = gloc.group.links || [];
          gloc.group.links.push(item);
        }
      }
      this.selectedId = item.id;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
      this.flashSettings();
    },

    addChild: function (parentId) {
      var ploc = this.findNode(parentId);
      if (!ploc) return;
      this.pushUndo();
      var item = {
        id: uid('nav'), label: 'New Sub-item', icon: '', href: '', visible: true
      };
      ploc.item.children = ploc.item.children || [];
      ploc.item.children.push(item);
      this.selectedId = item.id;
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
      this.flashSettings();
    },

    selectedGroupId: function () {
      if (!this.selectedId) return null;
      var loc = this.findNode(this.selectedId);
      return loc ? loc.meta.group.id : null;
    },

    flashSettings: function () {
      var el = this.dom.settings;
      if (!el) return;
      var input = el.querySelector('[data-field="label"]');
      if (input) { input.focus(); input.select(); }
    },

    changeGroup: function (id, groupId) {
      var loc = this.findNode(id);
      var target = this.findGroup(groupId);
      if (!loc || !target) return;
      if (loc.meta.group.id === groupId && loc.meta.parent == null) return;
      this.pushUndo();
      this.extractItem(id);
      target.group.links = target.group.links || [];
      target.group.links.push(loc.item);
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
    },

    changeParent: function (id, parentId) {
      var loc = this.findNode(id);
      if (!loc) return;
      if (parentId && (parentId === id || this.isDescendant(id, parentId))) return;
      this.pushUndo();
      var item = this.extractItem(id);
      if (!item) { this.undoStack.pop(); this.updateUndoBtn(); return; }
      if (parentId) {
        var ploc = this.findNode(parentId);
        if (!ploc) { this.undoStack.pop(); this.updateUndoBtn(); return; }
        ploc.item.children = ploc.item.children || [];
        ploc.item.children.push(item);
      } else {
        var g = this.findGroup(loc.meta.group.id);
        g.group.links = g.group.links || [];
        g.group.links.push(item);
      }
      this.markDirty();
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
    },

    // ────────────────────────────────────────────────────────────
    // Drag and drop
    // ────────────────────────────────────────────────────────────

    onDragStart: function (e) {
      var node = e.target.closest('.sgm-node');
      var group = e.target.closest('.sgm-group-head');
      if (node) {
        this.drag = { type: 'item', id: node.dataset.navId };
        node.classList.add('dragging');
      } else if (group) {
        this.drag = { type: 'group', id: group.dataset.groupId };
        group.classList.add('dragging');
      } else {
        return;
      }
      try { e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', this.drag.id); } catch (err) {}
    },

    computeDrop: function (e) {
      if (!this.drag) return null;
      var nodeEl = e.target.closest ? e.target.closest('.sgm-node') : null;
      var grpEl = e.target.closest ? e.target.closest('.sgm-group-head') : null;

      if (nodeEl && this.drag.type === 'item') {
        var targetId = nodeEl.dataset.navId;
        if (targetId === this.drag.id) return null;
        if (this.isDescendant(this.drag.id, targetId)) return null;
        var r = nodeEl.getBoundingClientRect();
        var after = (e.clientY - r.top) > r.height / 2;
        return { kind: after ? 'nodeAfter' : 'nodeBefore', targetId: targetId, el: nodeEl, nodeEl: nodeEl };
      }
      if (grpEl) {
        var gid = grpEl.dataset.groupId;
        if (this.drag.type === 'group') {
          if (gid === this.drag.id) return null;
          return { kind: 'groupBefore', targetId: gid, el: grpEl, grpEl: grpEl };
        }
        return { kind: 'groupInto', targetId: gid, el: grpEl, grpEl: grpEl };
      }
      return null;
    },

    onDragOver: function (e) {
      var plan = this.computeDrop(e);
      this.clearDropIndicators();
      this.dropPlan = plan;
      if (!plan) return;
      e.preventDefault();
      try { e.dataTransfer.dropEffect = 'move'; } catch (err) {}
      if (plan.kind === 'nodeBefore') plan.nodeEl.classList.add('drop-before');
      else if (plan.kind === 'nodeAfter') plan.nodeEl.classList.add('drop-after');
      else if (plan.grpEl) plan.grpEl.classList.add('drop-into');
    },

    onDragLeave: function (e) {
      if (e.target === this.dom.tree) {
        this.clearDropIndicators();
        this.dropPlan = null;
      }
    },

    onDrop: function (e) {
      e.preventDefault();
      var plan = this.dropPlan;
      this.clearDropIndicators();
      if (!plan || !this.drag) { this.dropPlan = null; return; }

      if (this.drag.type === 'item') {
        if (plan.kind === 'groupInto') {
          if (this.drag.id === plan.targetId) { this.dropPlan = null; return; }
          this.pushUndo();
          var item = this.extractItem(this.drag.id);
          var grp = this.findGroup(plan.targetId);
          if (item && grp) {
            grp.group.links = grp.group.links || [];
            grp.group.links.push(item);
          }
        } else {
          this.pushUndo();
          var it = this.extractItem(this.drag.id);
          var loc = this.findNode(plan.targetId);
          if (it && loc) {
            var idx = loc.meta.index + (plan.kind === 'nodeAfter' ? 1 : 0);
            loc.meta.siblings.splice(idx, 0, it);
          }
        }
      } else {
        var groups = this.working.groups || [];
        var from = -1;
        for (var i = 0; i < groups.length; i++) if (groups[i].id === this.drag.id) from = i;
        if (from < 0) { this.dropPlan = null; return; }
        this.pushUndo();
        var moved = groups.splice(from, 1)[0];
        var to = -1;
        for (var j = 0; j < groups.length; j++) if (groups[j].id === plan.targetId) to = j;
        if (to < 0) to = groups.length;
        groups.splice(to, 0, moved);
      }

      this.selectedId = this.drag.id;
      this.markDirty();
      this.dropPlan = null;
      this.drag = null;
      this.renderTree();
      this.renderPreview();
      this.renderSettings();
    },

    clearDropIndicators: function () {
      if (!this.dom.tree) return;
      Array.prototype.forEach.call(
        this.dom.tree.querySelectorAll('.drop-before, .drop-after, .drop-into'),
        function (el) { el.classList.remove('drop-before', 'drop-after', 'drop-into'); }
      );
      this.dom.tree.classList.remove('drop-tail');
    },

    clearDrag: function () {
      if (this.dom.tree) {
        Array.prototype.forEach.call(this.dom.tree.querySelectorAll('.dragging'), function (el) {
          el.classList.remove('dragging');
        });
      }
      this.clearDropIndicators();
      this.drag = null;
      this.dropPlan = null;
    },

    // ────────────────────────────────────────────────────────────
    // Live preview
    // ────────────────────────────────────────────────────────────

    renderPreview: function () {
      var el = this.dom.preview;
      if (!el || !this.working) return;
      el.className = 'sgm-preview mode-' + this.viewport + (this.previewCollapsed ? ' is-collapsed' : '');

      var groups = (this.working.groups || []).filter(function (g) { return g.visible !== false; });
      var self = this;

      var nav = groups.map(function (g) {
        var links = (g.links || []).filter(function (l) { return l.visible !== false; });
        var inner = links.map(function (l) { return self.previewItem(l, 1); }).join('');
        return '' +
          '<div class="sv-group">' +
            (g.label ? '<div class="sv-group-label">' + esc(g.label) + '</div>' : '') +
            inner +
          '</div>';
      }).join('');

      if (!nav) nav = '<div class="sgm-preview-empty">No visible navigation items.</div>';

      var active = this.selectedId;

      el.innerHTML = '' +
        '<div class="sv-brand">' +
          '<span class="sv-brand-crest material-symbols-outlined" aria-hidden="true">shield_person</span>' +
          '<span class="sv-brand-text">' +
            '<span class="sv-brand-name">NGIS · ' + esc(this.portalRoleLabel()) + '</span>' +
            '<span class="sv-brand-meta">' + esc(this.working.meta || 'New Gateway International School') + '</span>' +
          '</span>' +
        '</div>' +
        '<nav class="sv-nav">' + nav + '</nav>' +
        '<div class="sv-foot">' +
          '<div class="sv-link"><span class="material-symbols-outlined" aria-hidden="true">help_outline</span><span class="sv-link-label">Help &amp; Support</span></div>' +
          '<div class="sv-link"><span class="material-symbols-outlined" aria-hidden="true">logout</span><span class="sv-link-label">Log out</span></div>' +
        '</div>';

      // mark active
      if (active) {
        var activeEl = el.querySelector('[data-preview-id="' + CSS.escape(active) + '"]');
        if (activeEl) activeEl.classList.add('active');
      }
    },

    portalRoleLabel: function () {
      var p = this.portals.filter(function (x) { return x.portal === this.portal; }.bind(this))[0];
      if (p) return String(p.label || '').replace(' Sidebar', '');
      return this.portal.charAt(0).toUpperCase() + this.portal.slice(1);
    },

    previewItem: function (item, depth) {
      var self = this;
      var hidden = item.visible === false;

      if (item.children && item.children.length) {
        var kids = item.children
          .filter(function (c) { return c.visible !== false; })
          .map(function (c) { return self.previewItem(c, depth + 1); })
          .join('');
        return '' +
          '<div class="sv-subgroup-label" data-preview-id="' + esc(item.id) + '">' +
            (item.icon ? iconHtml(item.icon) : '') +
            '<span class="sv-link-label">' + esc(item.label) + '</span>' +
            '<span class="material-symbols-outlined sv-chevron" aria-hidden="true">expand_more</span>' +
          '</div>' +
          '<div>' + kids + '</div>';
      }

      var cls = 'sv-link' + (depth === 2 ? ' sv-sub' : depth >= 3 ? ' sv-sub2' : '');
      return '' +
        '<div class="' + cls + '" data-preview-id="' + esc(item.id) + '">' +
          (item.icon ? iconHtml(item.icon) : '') +
          '<span class="sv-link-label">' + esc(item.label) + '</span>' +
          (item.badge ? '<span class="sv-badge">' + esc(item.badge) + '</span>' : '') +
          (item.locked ? '<span class="material-symbols-outlined sv-lock" aria-hidden="true">lock</span>' : '') +
        '</div>';
    },

    // ────────────────────────────────────────────────────────────
    // Item settings
    // ────────────────────────────────────────────────────────────

    renderSettings: function () {
      var el = this.dom.settings;
      if (!el) return;

      var loc = this.selectedId ? this.findNode(this.selectedId) : null;
      if (!loc) {
        el.innerHTML = '<div class="cms-empty">Select an item in the navigation tree to edit its label, icon, destination, and visibility.</div>';
        return;
      }

      var item = loc.item;
      var groups = this.working.groups || [];
      var groupOptions = groups.map(function (g) {
        return '<option value="' + esc(g.id) + '"' + (g.id === loc.meta.group.id ? ' selected' : '') + '>' + esc(g.label || g.id) + '</option>';
      }).join('');

      var parentOptions = '<option value="">Top level</option>';
      // Parents: top-level nodes of the same group excluding self & descendants
      var sibs = loc.meta.group.links || [];
      var self2 = this;
      sibs.forEach(function (n) {
        if (n.id === item.id) return;
        if (self2.isDescendant(item.id, n.id)) return;
        parentOptions += '<option value="' + esc(n.id) + '"' + (loc.meta.parent && loc.meta.parent.id === n.id ? ' selected' : '') + '>' + esc(n.label || n.id) + '</option>';
      });

      var iconList = '<datalist id="sgmIconList">' + COMMON_ICONS.map(function (i) {
        return '<option value="' + esc(i) + '"></option>';
      }).join('') + '</datalist>';

      var lockNotice = item.locked
        ? '<div class="sgm-locked-note"><span class="material-symbols-outlined" aria-hidden="true">lock</span><span>Mandatory system navigation — it can be reordered but must remain accessible.</span></div>'
        : '';

      el.innerHTML = '' +
        iconList +
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium" for="sgmFieldLabel">Display Label</label>' +
          '<input type="text" id="sgmFieldLabel" class="cms-input" data-field="label" value="' + esc(item.label || '') + '">' +
        '</div>' +
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium" for="sgmFieldSubtitle">Subtitle <span style="color:var(--cms-slate-muted)">(optional tooltip)</span></label>' +
          '<input type="text" id="sgmFieldSubtitle" class="cms-input" data-field="subtitle" value="' + esc(item.subtitle || '') + '">' +
        '</div>' +
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium" for="sgmFieldIcon">Icon identifier</label>' +
          '<input type="text" id="sgmFieldIcon" class="cms-input" data-field="icon" list="sgmIconList" value="' + esc(item.icon || '') + '" placeholder="e.g. dashboard">' +
          '<div class="sgm-icon-preview">Preview: ' + (item.icon ? iconHtml(item.icon) : '<span>—</span>') + '<span>' + esc(item.icon || 'no icon') + '</span></div>' +
        '</div>' +
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium" for="sgmFieldHref">Destination (registered route)</label>' +
          '<div style="display:flex; gap:6px;">' +
            '<input type="text" id="sgmFieldHref" class="cms-input" data-field="href" value="' + esc(item.href || '') + '" placeholder="pages/…/*.html or https://…">' +
            '<button type="button" class="cms-btn cms-btn-secondary" id="sgmBtnBrowseRoute" style="flex-shrink:0">Browse</button>' +
          '</div>' +
          '<div class="cms-hint">Only registered routes or external URLs are accepted. Cross-portal destinations are blocked.</div>' +
        '</div>' +
        '<div class="sgm-field-row">' +
          '<div class="cms-form-group">' +
            '<label class="cms-label font-medium" for="sgmFieldGroup">Navigation Group</label>' +
            '<select id="sgmFieldGroup" class="cms-form-select" data-field="group">' + groupOptions + '</select>' +
          '</div>' +
          '<div class="cms-form-group">' +
            '<label class="cms-label font-medium" for="sgmFieldParent">Parent</label>' +
            '<select id="sgmFieldParent" class="cms-form-select" data-field="parent">' + parentOptions + '</select>' +
          '</div>' +
        '</div>' +
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium">Position in group</label>' +
          '<div class="sgm-order-btns">' +
            '<button type="button" class="cms-btn cms-btn-secondary" data-order="-1"><span class="material-symbols-outlined" style="font-size:15px">arrow_upward</span><span>Move up</span></button>' +
            '<button type="button" class="cms-btn cms-btn-secondary" data-order="1"><span class="material-symbols-outlined" style="font-size:15px">arrow_downward</span><span>Move down</span></button>' +
          '</div>' +
        '</div>' +
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium" style="display:flex; align-items:center; gap:8px; cursor:pointer;">' +
            '<input type="checkbox" data-field="visible"' + (item.visible === false ? '' : ' checked') + (item.locked ? ' disabled' : '') + '>' +
            '<span>Visible in the published sidebar</span>' +
          '</label>' +
        '</div>' +
        lockNotice +
        '<div class="sgm-info-row"><span>Role scope (governed by portal)</span><span>' + esc(PORTAL_ROLE_SCOPE[this.portal] || '—') + '</span></div>' +
        '<div class="sgm-info-row"><span>Visibility is not authorization</span><span>Backend access is unchanged</span></div>' +
        '<div class="sgm-settings-actions">' +
          (item.locked ? '' : '<button type="button" class="cms-btn cms-btn-warm" data-settings-delete><span class="material-symbols-outlined" style="font-size:15px">delete</span><span>Remove item</span></button>') +
          '<button type="button" class="cms-btn cms-btn-secondary" data-settings-add-child><span class="material-symbols-outlined" style="font-size:15px">subdirectory_arrow_right</span><span>Add sub-item</span></button>' +
        '</div>';
    },

    onSettingsInput: function (e) {
      var f = e.target && e.target.dataset ? e.target.dataset.field : null;
      if (!f) return;
      var loc = this.selectedId ? this.findNode(this.selectedId) : null;
      if (!loc) return;

      if (f === 'label') loc.item.label = e.target.value;
      else if (f === 'subtitle') loc.item.subtitle = e.target.value;
      else if (f === 'href') loc.item.href = e.target.value.trim();
      else if (f === 'icon') {
        loc.item.icon = e.target.value.trim();
        var prev = this.dom.settings.querySelector('.sgm-icon-preview');
        if (prev) prev.innerHTML = 'Preview: ' + (loc.item.icon ? iconHtml(loc.item.icon) : '<span>—</span>') + '<span>' + esc(loc.item.icon || 'no icon') + '</span>';
      } else {
        return;
      }
      this.markDirty();
      this.renderTree();
      this.renderPreview();
    },

    onSettingsChange: function (e) {
      var f = e.target && e.target.dataset ? e.target.dataset.field : null;
      if (!f) return;
      var loc = this.selectedId ? this.findNode(this.selectedId) : null;
      if (!loc) return;

      if (f === 'visible') {
        if (loc.item.locked) return;
        this.pushUndo();
        loc.item.visible = e.target.checked;
        this.markDirty();
        this.renderTree();
        this.renderPreview();
        this.renderSettings();
      } else if (f === 'group') {
        this.changeGroup(this.selectedId, e.target.value);
      } else if (f === 'parent') {
        this.changeParent(this.selectedId, e.target.value);
      }
    },

    onSettingsClick: function (e) {
      var t = e.target;
      if (!t || typeof t.closest !== 'function') return;

      var order = t.closest('[data-order]');
      if (order) { this.moveItem(this.selectedId, parseInt(order.dataset.order, 10)); return; }

      var browse = t.closest('#sgmBtnBrowseRoute');
      if (browse) { this.openRoutePicker(); return; }

      var del = t.closest('[data-settings-delete]');
      if (del) { this.deleteItem(this.selectedId); return; }

      var addChild = t.closest('[data-settings-add-child]');
      if (addChild) { this.addChild(this.selectedId); return; }
    },

    // ────────────────────────────────────────────────────────────
    // Route picker
    // ────────────────────────────────────────────────────────────

    openRoutePicker: function () {
      var self = this;
      var routes = this.routes || [];

      function build(filter) {
        filter = (filter || '').toLowerCase();
        var list = routes.filter(function (r) { return !filter || r.toLowerCase().indexOf(filter) !== -1; });
        if (!list.length) return '<div class="cms-empty">No matching registered routes.</div>';
        return list.map(function (r) {
          return '<button type="button" class="cms-visibility-row" style="width:100%; text-align:left; cursor:pointer" data-pick-route="' + esc(r) + '">' +
            '<span>' + esc(r) + '</span><span class="cms-pill cms-pill-on">select</span></button>';
        }).join('');
      }

      var html = '' +
        '<div class="cms-form-group">' +
          '<input type="search" class="cms-input" id="sgmRouteFilter" placeholder="Filter registered routes…" aria-label="Filter routes">' +
        '</div>' +
        '<div id="sgmRouteList" style="max-height:340px; overflow-y:auto; display:flex; flex-direction:column; gap:6px;">' + build('') + '</div>';

      window.CMS.openModal('Select a registered destination', html, null, null);

      var filterEl = document.getElementById('sgmRouteFilter');
      var listEl = document.getElementById('sgmRouteList');
      if (filterEl && listEl) {
        filterEl.addEventListener('input', function () { listEl.innerHTML = build(this.value); });
      }
      if (listEl) {
        listEl.addEventListener('click', function (ev) {
          var btn = ev.target.closest('[data-pick-route]');
          if (!btn) return;
          var loc = self.selectedId ? self.findNode(self.selectedId) : null;
          if (loc) {
            self.pushUndo();
            loc.item.href = btn.dataset.pickRoute;
            self.markDirty();
            self.renderTree();
            self.renderPreview();
            self.renderSettings();
          }
          window.CMS.closeModal();
        });
      }
    },

    // ────────────────────────────────────────────────────────────
    // Validation / health
    // ────────────────────────────────────────────────────────────

    payload: function () {
      return {
        brand: this.working.brand,
        meta: this.working.meta,
        groups: this.working.groups || []
      };
    },

    hideHealth: function () {
      if (this.dom.health) { this.dom.health.hidden = true; this.dom.health.innerHTML = ''; }
    },

    renderFindings: function (title, findings) {
      var el = this.dom.health;
      if (!el) return;
      el.hidden = false;
      el.innerHTML = this.findingsHtml(title, findings);
      el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    },

    findingsHtml: function (title, findings) {
      findings = findings || [];
      var counts = { high: 0, medium: 0, low: 0 };
      findings.forEach(function (f) { if (counts[f.severity] != null) counts[f.severity] += 1; });

      var head = '' +
        '<div class="sgm-health-head">' +
          '<span class="sgm-health-title">' + esc(title) + '</span>' +
          '<span class="sgm-health-counts">' +
            '<span class="cms-pill cms-pill-lock">' + counts.high + ' high</span>' +
            '<span class="cms-pill cms-pill-off">' + counts.medium + ' med</span>' +
            '<span class="cms-pill cms-pill-off">' + counts.low + ' low</span>' +
          '</span>' +
        '</div>';

      if (!findings.length) {
        return head + '<div class="sgm-health-clean"><span class="material-symbols-outlined" aria-hidden="true">check_circle</span>No issues found in the checked navigation.</div>';
      }

      var rows = findings.map(function (f) {
        return '' +
          '<div class="sgm-finding">' +
            '<span class="sgm-sev sgm-sev-' + esc(f.severity) + '">' + esc(f.severity) + '</span>' +
            '<span style="flex:1">' + esc(f.message) +
              (f.item ? ' <span class="sgm-finding-code">(' + esc(f.item) + ')</span>' : '') +
              (f.code ? ' <span class="sgm-finding-code">· ' + esc(f.code) + '</span>' : '') +
            '</span>' +
          '</div>';
      }).join('');

      return head + '<div class="sgm-health-list">' + rows + '</div>';
    },

    validateDraft: function () {
      var self = this;
      fetch('/api/nav/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portal: this.portal, payload: this.payload() })
      })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        var findings = (res && res.success && res.data) ? res.data.findings : [];
        self.renderFindings('Draft validation · ' + self.portalLabel(), findings);
      })
      .catch(function () {
        self.renderFindings('Draft validation', [{ severity: 'high', code: 'network', message: 'Unable to reach the validation endpoint.', item: null }]);
      });
    },

    loadHealth: function () {
      var self = this;
      fetch('/api/nav/health?portal=' + encodeURIComponent(this.portal))
        .then(function (r) { return r.json(); })
        .then(function (res) {
          var findings = (res && res.success && res.data) ? res.data.findings : [];
          self.renderFindings('Navigation health · ' + self.portalLabel(), findings);
        })
        .catch(function () {
          self.renderFindings('Navigation health', [{ severity: 'high', code: 'network', message: 'Unable to reach the health endpoint.', item: null }]);
        });
    },

    // ────────────────────────────────────────────────────────────
    // Persistence: save draft / publish / versions / defaults
    // ────────────────────────────────────────────────────────────

    saveDraft: function (silent) {
      var self = this;
      return fetch('/api/nav/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portal: this.portal, payload: this.payload() })
      })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res && res.success) {
          self.dirty = false;
          self.undoStack = [];
          self.updateUndoBtn();
          if (res.data) { self.state = res.data; self.updateStatusChip(res.data.status); }
          if (!silent) window.CMS.showToast('Navigation draft saved for the ' + self.portalLabel() + '.');
        } else if (!silent) {
          window.alert('Failed to save draft: ' + ((res && res.error) || 'Server error'));
        }
        return res;
      })
      .catch(function (err) {
        if (!silent) window.alert('Network error saving draft.');
        throw err;
      });
    },

    publish: function () {
      var self = this;
      if (!window.confirm('Validate and publish the navigation changes to the live ' + this.portalLabel() + '?')) return;

      var doPublish = function () {
        return fetch('/api/nav/publish', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ portal: self.portal, summary: 'Published navigation updates for ' + self.portal })
        }).then(function (r) { return r.json().then(function (body) { return { ok: r.ok, body: body }; }); });
      };

      var chain = this.dirty ? this.saveDraft(true) : Promise.resolve();
      chain.then(doPublish).then(function (out) {
        var res = out.body;
        if (res && res.success) {
          self.dirty = false;
          self.undoStack = [];
          self.updateUndoBtn();
          if (res.state) { self.state = res.state; self.updateStatusChip('published'); }
          window.CMS.showToast('Published live. Version ' + ((res.data && res.data.version_id) || '') + '.');
          self.hideHealth();
          return self.reloadState();
        }
        // Publication blocked by validation
        var err = res && res.error;
        if (err && typeof err === 'object' && err.findings) {
          self.renderFindings('Publication blocked · ' + self.portalLabel(), err.findings);
          window.CMS.showToast('Publication blocked: resolve the high-severity findings.');
        } else {
          window.alert('Publish failed: ' + ((err && err.message) || err || 'Unknown error'));
        }
      }).catch(function () {
        window.alert('Network error during publish.');
      });
    },

    openVersions: function () {
      var self = this;
      fetch('/api/nav/versions?portal=' + encodeURIComponent(this.portal))
        .then(function (r) { return r.json(); })
        .then(function (res) {
          var versions = (res && res.success) ? (res.data || []) : [];
          var html = '<div style="display:flex; flex-direction:column; gap:10px;">';
          if (!versions.length) {
            html += '<div class="cms-empty">No published version snapshots yet for the ' + esc(self.portalLabel()) + '.</div>';
          } else {
            versions.forEach(function (v) {
              html += '' +
                '<div style="padding:12px; border:1px solid var(--cms-border); border-radius:10px; background:var(--cms-off-white); display:flex; align-items:center; justify-content:space-between; gap:10px;">' +
                  '<div style="min-width:0">' +
                    '<div class="text-xs font-medium text-slate-800">' + esc(v.version_id) + ' · ' + esc(v.summary || 'Snapshot') + '</div>' +
                    '<div class="text-[11px] text-slate-500 mt-1">' + esc(self.fmt(v.timestamp)) + ' · ' + esc(v.author_name || v.author || 'System') + '</div>' +
                  '</div>' +
                  '<button type="button" class="cms-btn cms-btn-secondary" data-restore="' + esc(v.version_id) + '"><span class="material-symbols-outlined" style="font-size:15px">restore</span><span>Restore</span></button>' +
                '</div>';
            });
          }
          html += '</div>';
          window.CMS.openModal('Navigation version history · ' + self.portalLabel(), html, null, null);

          var body = document.getElementById('cmsModalBody');
          if (body) {
            body.addEventListener('click', function (ev) {
              var btn = ev.target.closest('[data-restore]');
              if (!btn) return;
              self.restoreVersion(btn.dataset.restore);
            });
          }
        });
    },

    restoreVersion: function (versionId) {
      var self = this;
      if (!window.confirm('Restore the ' + this.portalLabel() + ' navigation from version ' + versionId + '?')) return;
      fetch('/api/nav/restore', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ version_id: versionId })
      })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res && res.success) {
          window.CMS.closeModal();
          window.CMS.showToast('Restored navigation from ' + versionId + '.');
          self.selectPortal(self.portal);
        } else {
          window.alert('Restore failed: ' + ((res && res.error) || 'Server error'));
        }
      });
    },

    restoreDefaults: function () {
      var self = this;
      if (!window.confirm('Restore the factory navigation for the ' + this.portalLabel() + '? Unpublished draft changes will be discarded.')) return;
      fetch('/api/nav/defaults', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portal: this.portal })
      })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res && res.success) {
          window.CMS.showToast('Factory navigation restored for the ' + self.portalLabel() + '.');
          self.selectPortal(self.portal);
        } else {
          window.alert('Reset failed: ' + ((res && res.error) || 'Server error'));
        }
      });
    },

    // ────────────────────────────────────────────────────────────
    // Misc
    // ────────────────────────────────────────────────────────────

    portalLabel: function () {
      var p = this.portals.filter(function (x) { return x.portal === this.portal; }.bind(this))[0];
      return p ? p.label : (this.portal.charAt(0).toUpperCase() + this.portal.slice(1) + ' Sidebar');
    },

    fmt: function (iso) {
      if (!iso) return '—';
      var d = new Date(iso);
      if (isNaN(d.getTime())) return String(iso);
      return d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    }
  };

  window.NavMgr = NavMgr;

  function boot() {
    // Initialize early so the panel is ready when CMS activates it.
    NavMgr.init();
    if (window.CMS && typeof window.CMS.onPanelShow === 'function') {
      var orig = window.CMS.onPanelShow;
      window.CMS.onPanelShow = function (panelId) {
        orig.call(this, panelId);
        if (panelId === 'tabSections') NavMgr.ensureLoaded();
      };
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
