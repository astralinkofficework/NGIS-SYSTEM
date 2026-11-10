/**
 * NGIS Admin Dashboard Content Management System (CMS) Controller
 * Real-time two-panel workspace, reactive preview, dynamic tokens,
 * version rollback, media uploads, and multi-portal orchestration.
 */

(function () {
  'use strict';

  var CMS = {
    portal: 'student',
    campus: 'all',
    viewport: 'desktop',
    isVisualMode: false,
    activeBannerIdx: 0,
    activePanel: 'tabSections',
    navCollapsed: false,
    config: null,
    configError: false,
    currentData: null,
    hasUnsavedChanges: false,
    debounceTimer: null,

    // Contextual copy for the shared editor workspace heading
    PANEL_META: {
      panelOverview:   { title: 'Overview',                sub: 'Summary of the currently selected portal content.' },
      tabSections:     { title: 'Global Sidebar Manager',  sub: 'Configure, preview, and publish sidebar navigation across school portals.' },
      tabHero:         { title: 'Hero Content',            sub: 'Manage the welcome heading, greeting template, and dynamic date badge.' },
      tabBanners:      { title: 'Dashboard Banners',       sub: 'Create, edit, and order promotional carousel slides.' },
      tabMedia:        { title: 'Media Library',           sub: 'Upload and manage banner image assets.' },
      panelPublishing: { title: 'Publishing & Visibility', sub: 'Control publication state and review content visibility.' },
      panelActivity:   { title: 'Activity History',        sub: 'Recent content changes and published versions.' }
    },

    init: function () {
      this.bindDOM();
      this.applyNavCollapsed();
      this.bindEvents();
      this.activatePanel(this.activePanel, false);
      this.bindHashNavigation();
      this.loadConfig();
    },

    bindDOM: function () {
      this.dom = {
        portalSelect: document.getElementById('cmsPortalSelect'),
        campusSelect: document.getElementById('cmsCampusSelect'),
        statusBadge: document.getElementById('cmsStatusBadge'),
        btnSaveDraft: document.getElementById('cmsBtnSaveDraft'),
        btnPublish: document.getElementById('cmsBtnPublish'),
        btnSchedule: document.getElementById('cmsBtnSchedule'),
        btnVersions: document.getElementById('cmsBtnVersions'),
        btnVisualMode: document.getElementById('cmsBtnVisualMode'),

        // Internal CMS sidebar navigation + panels
        nav: document.getElementById('cmsNav'),
        navList: document.querySelector('.cms-nav-list'),
        navItems: document.querySelectorAll('.cms-nav-item'),
        navCollapse: document.getElementById('cmsNavCollapse'),
        navToggle: document.getElementById('cmsNavToggle'),
        navToggleLabel: document.getElementById('cmsNavToggleLabel'),
        navBackdrop: document.getElementById('cmsNavBackdrop'),
        workspace: document.querySelector('.cms-workspace'),
        panelTitle: document.getElementById('cmsPanelTitle'),
        panelSub: document.getElementById('cmsPanelSub'),
        panelContents: document.querySelectorAll('.cms-tab-content'),

        // Overview / Publishing / Activity panels
        overviewBody: document.getElementById('cmsOverviewBody'),
        publishStatus: document.getElementById('cmsPublishStatus'),
        visibilityList: document.getElementById('cmsVisibilityList'),
        activityList: document.getElementById('cmsActivityList'),
        btnRefreshActivity: document.getElementById('cmsBtnRefreshActivity'),
        btnOpenVersions: document.getElementById('cmsBtnOpenVersions'),

        // Hero inputs
        heroTitle: document.getElementById('cmsHeroTitle'),
        heroDescription: document.getElementById('cmsHeroDescription'),
        heroGreeting: document.getElementById('cmsHeroGreeting'),
        heroDateVisible: document.getElementById('cmsHeroDateVisible'),
        heroDateFormat: document.getElementById('cmsHeroDateFormat'),
        heroAlignment: document.getElementById('cmsHeroAlignment'),
        tokenChips: document.querySelectorAll('.cms-token-chip'),

        // Banner inputs
        bannerList: document.getElementById('cmsBannerList'),
        bannerName: document.getElementById('cmsBannerName'),
        bannerHeading: document.getElementById('cmsBannerHeading'),
        bannerSubtitle: document.getElementById('cmsBannerSubtitle'),
        bannerDescription: document.getElementById('cmsBannerDescription'),
        bannerImageUrl: document.getElementById('cmsBannerImageUrl'),
        bannerAltText: document.getElementById('cmsBannerAltText'),
        bannerBtnLabel: document.getElementById('cmsBannerBtnLabel'),
        bannerBtnUrl: document.getElementById('cmsBannerBtnUrl'),
        bannerActive: document.getElementById('cmsBannerActive'),
        btnBrowseMedia: document.getElementById('cmsBtnBrowseMedia'),
        btnAddNewBanner: document.getElementById('cmsBtnAddNewBanner'),

        // Carousel inputs
        carouselAutoplay: document.getElementById('cmsCarouselAutoplay'),
        carouselInterval: document.getElementById('cmsCarouselInterval'),
        carouselArrows: document.getElementById('cmsCarouselArrows'),
        carouselDots: document.getElementById('cmsCarouselDots'),

        // Media Dropzone
        mediaDropzone: document.getElementById('cmsMediaDropzone'),
        mediaFileInput: document.getElementById('cmsMediaFileInput'),
        mediaGrid: document.getElementById('cmsMediaGrid'),

        // Live preview elements
        previewViewport: document.getElementById('cmsPreviewViewport'),
        viewportBtns: document.querySelectorAll('.cms-viewport-btn'),
        pvHero: document.getElementById('pvHero'),
        pvHeroDate: document.getElementById('pvHeroDate'),
        pvHeroTitle: document.getElementById('pvHeroTitle'),
        pvHeroGreeting: document.getElementById('pvHeroGreeting'),
        pvBannerTrack: document.getElementById('pvBannerTrack'),
        pvPromoImg: document.getElementById('pvPromoImg'),
        pvPromoHeading: document.getElementById('pvPromoHeading'),
        pvPromoSub: document.getElementById('pvPromoSub'),
        pvPromoBtn: document.getElementById('pvPromoBtn'),

        // Modals
        modalBackdrop: document.getElementById('cmsModalBackdrop'),
        modalTitle: document.getElementById('cmsModalTitle'),
        modalBody: document.getElementById('cmsModalBody'),
        modalCloseBtn: document.getElementById('cmsModalCloseBtn'),
        toast: document.getElementById('cmsToast')
      };
    },

    bindEvents: function () {
      var self = this;

      // Portal & Campus change
      if (this.dom.portalSelect) {
        this.dom.portalSelect.addEventListener('change', function () {
          self.portal = this.value;
          self.activeBannerIdx = 0;
          self.populateEditor();
          self.fetchRuntimePreview();
          self.refreshActivePanel();
        });
      }

      if (this.dom.campusSelect) {
        this.dom.campusSelect.addEventListener('change', function () {
          self.campus = this.value;
          self.fetchRuntimePreview();
        });
      }

      // Viewport Switcher
      this.dom.viewportBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          self.dom.viewportBtns.forEach(function (b) { b.classList.remove('active'); });
          btn.classList.add('active');
          var mode = btn.dataset.viewport;
          self.viewport = mode;
          self.dom.previewViewport.className = 'cms-preview-viewport mode-' + mode;
        });
      });

      // Visual Mode Toggle ("Edit on Preview")
      if (this.dom.btnVisualMode) {
        this.dom.btnVisualMode.addEventListener('click', function () {
          self.isVisualMode = !self.isVisualMode;
          this.classList.toggle('cms-btn-active-toggle', self.isVisualMode);
          self.dom.previewViewport.classList.toggle('cms-visual-mode', self.isVisualMode);
          self.showToast(self.isVisualMode ? 'Visual Edit Mode Enabled. Click elements on preview to edit.' : 'Visual Edit Mode Disabled.');
        });
      }

      // Internal CMS sidebar navigation
      this.dom.navItems.forEach(function (btn) {
        btn.addEventListener('click', function () {
          self.activatePanel(btn.dataset.panel, true);
        });
      });

      // Keyboard navigation (ARIA tabs pattern: arrow keys move + activate)
      if (this.dom.navList) {
        this.dom.navList.addEventListener('keydown', function (e) {
          var keys = ['ArrowDown', 'ArrowUp', 'Home', 'End'];
          if (keys.indexOf(e.key) === -1) return;
          e.preventDefault();
          var items = Array.prototype.slice.call(self.dom.navItems);
          var cur = items.indexOf(document.activeElement);
          if (cur === -1) cur = 0;
          var next = cur;
          if (e.key === 'ArrowDown') next = Math.min(items.length - 1, cur + 1);
          else if (e.key === 'ArrowUp') next = Math.max(0, cur - 1);
          else if (e.key === 'Home') next = 0;
          else if (e.key === 'End') next = items.length - 1;
          var target = items[next];
          if (target) {
            target.focus();
            self.activatePanel(target.dataset.panel, true);
          }
        });
      }

      // Collapse the internal sidebar into an icon-only rail (desktop)
      if (this.dom.navCollapse) {
        this.dom.navCollapse.addEventListener('click', function () {
          self.toggleNavCollapsed();
        });
      }

      // Mobile slide-out drawer controls
      if (this.dom.navToggle) {
        this.dom.navToggle.addEventListener('click', function () {
          self.openNavDrawer();
        });
      }
      if (this.dom.navBackdrop) {
        this.dom.navBackdrop.addEventListener('click', function () {
          self.closeNavDrawer();
        });
      }
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') self.closeNavDrawer();
      });

      // Delegated quick actions (Overview shortcuts + Publishing lifecycle)
      document.addEventListener('click', function (e) {
        var el = e.target;
        if (!el || typeof el.closest !== 'function') return;

        var goto = el.closest('[data-goto]');
        if (goto) { self.activatePanel(goto.dataset.goto, true); return; }

        var act = el.closest('[data-action]');
        if (act) {
          var a = act.dataset.action;
          if (a === 'save-draft') self.saveDraft();
          else if (a === 'publish') self.publishContent();
          else if (a === 'schedule') self.openScheduleModal();
          else if (a === 'versions') self.openVersionsModal();
        }
      });

      if (this.dom.btnRefreshActivity) {
        this.dom.btnRefreshActivity.addEventListener('click', function () {
          self.renderActivity();
        });
      }
      if (this.dom.btnOpenVersions) {
        this.dom.btnOpenVersions.addEventListener('click', function () {
          self.openVersionsModal();
        });
      }

      // Guard unsaved edits when leaving the page
      window.addEventListener('beforeunload', function (e) {
        if (self.hasUnsavedChanges) {
          e.preventDefault();
          e.returnValue = '';
          return '';
        }
      });

      // Hero inputs reactive typing
      var heroInputs = [
        this.dom.heroTitle, this.dom.heroDescription, this.dom.heroGreeting,
        this.dom.heroDateVisible, this.dom.heroDateFormat, this.dom.heroAlignment
      ];
      heroInputs.forEach(function (el) {
        if (!el) return;
        el.addEventListener('input', function () {
          self.markUnsaved();
          self.debounceSync();
        });
        el.addEventListener('change', function () {
          self.markUnsaved();
          self.debounceSync();
        });
      });

      // Token chip click insertion
      this.dom.tokenChips.forEach(function (chip) {
        chip.addEventListener('click', function () {
          var token = this.dataset.token;
          var input = self.dom.heroGreeting;
          if (!input) return;
          var start = input.selectionStart || input.value.length;
          var end = input.selectionEnd || input.value.length;
          input.value = input.value.substring(0, start) + token + input.value.substring(end);
          input.focus();
          input.selectionStart = input.selectionEnd = start + token.length;
          self.markUnsaved();
          self.debounceSync();
        });
      });

      // Banner inputs reactive typing
      var bannerInputs = [
        this.dom.bannerName, this.dom.bannerHeading, this.dom.bannerSubtitle,
        this.dom.bannerDescription, this.dom.bannerImageUrl, this.dom.bannerAltText,
        this.dom.bannerBtnLabel, this.dom.bannerBtnUrl, this.dom.bannerActive
      ];
      bannerInputs.forEach(function (el) {
        if (!el) return;
        el.addEventListener('input', function () {
          self.saveActiveBannerFormToMemory();
          self.markUnsaved();
          self.debounceSync();
        });
        el.addEventListener('change', function () {
          self.saveActiveBannerFormToMemory();
          self.markUnsaved();
          self.debounceSync();
        });
      });

      // Carousel inputs
      var carouselInputs = [
        this.dom.carouselAutoplay, this.dom.carouselInterval,
        this.dom.carouselArrows, this.dom.carouselDots
      ];
      carouselInputs.forEach(function (el) {
        if (!el) return;
        el.addEventListener('change', function () {
          self.markUnsaved();
        });
      });

      // Add New Banner Button
      if (this.dom.btnAddNewBanner) {
        this.dom.btnAddNewBanner.addEventListener('click', function () {
          self.addNewBanner();
        });
      }

      // Browse Media Button
      if (this.dom.btnBrowseMedia) {
        this.dom.btnBrowseMedia.addEventListener('click', function () {
          self.openMediaPickerModal();
        });
      }

      // Actions: Save Draft, Publish, Schedule, Versions
      if (this.dom.btnSaveDraft) {
        this.dom.btnSaveDraft.addEventListener('click', function () {
          self.saveDraft();
        });
      }

      if (this.dom.btnPublish) {
        this.dom.btnPublish.addEventListener('click', function () {
          self.publishContent();
        });
      }

      if (this.dom.btnSchedule) {
        this.dom.btnSchedule.addEventListener('click', function () {
          self.openScheduleModal();
        });
      }

      if (this.dom.btnVersions) {
        this.dom.btnVersions.addEventListener('click', function () {
          self.openVersionsModal();
        });
      }

      // Modal close button
      if (this.dom.modalCloseBtn) {
        this.dom.modalCloseBtn.addEventListener('click', function () {
          self.closeModal();
        });
      }

      // Media File Upload Dropzone
      if (this.dom.mediaDropzone && this.dom.mediaFileInput) {
        this.dom.mediaDropzone.addEventListener('click', function () {
          self.dom.mediaFileInput.click();
        });
        this.dom.mediaFileInput.addEventListener('change', function () {
          if (this.files && this.files[0]) {
            self.uploadFile(this.files[0]);
          }
        });
        this.dom.mediaDropzone.addEventListener('dragover', function (e) {
          e.preventDefault();
          this.style.borderColor = 'var(--cms-forest-green)';
        });
        this.dom.mediaDropzone.addEventListener('dragleave', function () {
          this.style.borderColor = 'var(--cms-border)';
        });
        this.dom.mediaDropzone.addEventListener('drop', function (e) {
          e.preventDefault();
          this.style.borderColor = 'var(--cms-border)';
          if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            self.uploadFile(e.dataTransfer.files[0]);
          }
        });
      }

      // Interactive Preview element click ("Edit on Preview")
      if (this.dom.pvHero) {
        this.dom.pvHero.addEventListener('click', function () {
          if (!self.isVisualMode) return;
          self.switchTab('tabHero');
          self.dom.heroTitle.focus();
        });
      }

      var pvBannerBox = document.getElementById('pvBannerBlock');
      if (pvBannerBox) {
        pvBannerBox.addEventListener('click', function () {
          if (!self.isVisualMode) return;
          self.switchTab('tabBanners');
          self.dom.bannerHeading.focus();
        });
      }
    },

    // ── Internal sidebar navigation ──

    activatePanel: function (panelId, updateHash) {
      var target = document.getElementById(panelId);
      if (!target || !target.classList.contains('cms-tab-content')) return;

      this.activePanel = panelId;

      // Roving tabindex (active item is the only tab stop)
      this.dom.navItems.forEach(function (btn) {
        var on = btn.dataset.panel === panelId;
        btn.classList.toggle('active', on);
        btn.setAttribute('aria-selected', on ? 'true' : 'false');
        btn.setAttribute('tabindex', on ? '0' : '-1');
      });

      this.dom.panelContents.forEach(function (c) {
        c.classList.toggle('active', c.id === panelId);
      });

      // The Global Sidebar Manager uses a dedicated full-width workspace:
      // the dashboard preview column is hidden while managing navigation.
      if (this.dom.workspace) {
        this.dom.workspace.classList.toggle('cms-sgm-active', panelId === 'tabSections');
      }

      var meta = (this.PANEL_META && this.PANEL_META[panelId]) || null;
      if (meta) {
        if (this.dom.panelTitle) this.dom.panelTitle.textContent = meta.title;
        if (this.dom.panelSub) this.dom.panelSub.textContent = meta.sub;
        if (this.dom.navToggleLabel) this.dom.navToggleLabel.textContent = meta.title;
      }

      if (updateHash && location.hash !== '#' + panelId) {
        history.pushState(null, '', '#' + panelId);
      }

      this.closeNavDrawer();
      this.onPanelShow(panelId);
    },

    // Kept for the "Edit on Preview" handlers that jump to a specific panel
    switchTab: function (tabId) {
      this.activatePanel(tabId, true);
    },

    onPanelShow: function (panelId) {
      if (panelId === 'panelOverview') this.renderOverview();
      else if (panelId === 'panelPublishing') this.renderPublishing();
      else if (panelId === 'panelActivity') this.renderActivity();
      else if (panelId === 'tabMedia') this.renderMediaLibrary();
      else if (panelId === 'tabSections' && window.NavMgr) window.NavMgr.ensureLoaded();
    },

    refreshActivePanel: function () {
      var p = this.activePanel;
      if (p === 'panelOverview') this.renderOverview();
      else if (p === 'panelPublishing') this.renderPublishing();
      else if (p === 'panelActivity') this.renderActivity();
    },

    bindHashNavigation: function () {
      var self = this;
      window.addEventListener('popstate', function () {
        var fromHash = self.panelFromHash();
        self.activatePanel(fromHash || self.activePanel, false);
      });
      var initial = this.panelFromHash();
      if (initial) this.activatePanel(initial, false);
    },

    panelFromHash: function () {
      var raw = (location.hash || '').replace(/^#/, '');
      if (!raw) return null;
      var el = document.getElementById(raw);
      if (el && el.classList.contains('cms-tab-content')) return raw;
      return null;
    },

    applyNavCollapsed: function () {
      var stored = null;
      try { stored = localStorage.getItem('cms-nav-collapsed'); } catch (err) { stored = null; }
      this.navCollapsed = stored === '1';
      if (this.dom.workspace) this.dom.workspace.classList.toggle('nav-collapsed', this.navCollapsed);
      if (this.dom.navCollapse) this.dom.navCollapse.setAttribute('aria-expanded', this.navCollapsed ? 'false' : 'true');
    },

    toggleNavCollapsed: function () {
      this.navCollapsed = !this.navCollapsed;
      if (this.dom.workspace) this.dom.workspace.classList.toggle('nav-collapsed', this.navCollapsed);
      if (this.dom.navCollapse) this.dom.navCollapse.setAttribute('aria-expanded', this.navCollapsed ? 'false' : 'true');
      try { localStorage.setItem('cms-nav-collapsed', this.navCollapsed ? '1' : '0'); } catch (err) {}
    },

    openNavDrawer: function () {
      if (this.dom.nav) this.dom.nav.classList.add('open');
      if (this.dom.navBackdrop) { this.dom.navBackdrop.hidden = false; }
      if (this.dom.navToggle) this.dom.navToggle.setAttribute('aria-expanded', 'true');
    },

    closeNavDrawer: function () {
      if (this.dom.nav) this.dom.nav.classList.remove('open');
      if (this.dom.navBackdrop) { this.dom.navBackdrop.hidden = true; }
      if (this.dom.navToggle) this.dom.navToggle.setAttribute('aria-expanded', 'false');
    },

    // ── Panel renderers (Overview / Publishing / Activity) ──

    escapeHtml: function (s) {
      return String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    },

    formatTimestamp: function (iso) {
      if (!iso) return '—';
      var d = new Date(iso);
      if (isNaN(d.getTime())) return String(iso);
      return d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    },

    portalLabel: function (p) {
      var map = { student: 'Student Portal', teacher: 'Teacher Portal', principal: 'Principal Portal', admin: 'Admin Portal' };
      return map[p] || p;
    },

    campusLabel: function (c) {
      var map = { all: 'All Campuses', main: 'Phnom Penh Main Campus', toul_kork: 'Toul Kork Campus' };
      return map[c] || c;
    },

    statusLabel: function (status) {
      if (status === 'draft') return 'Draft';
      if (status === 'scheduled') return 'Scheduled';
      return 'Published';
    },

    kvRow: function (k, v) {
      return '<div class="cms-kv-row"><span class="cms-kv-key">' + k + '</span><span class="cms-kv-val">' + v + '</span></div>';
    },

    currentPortalConfig: function () {
      if (!this.config || !this.config.portals_config) return {};
      return this.config.portals_config[this.portal] || {};
    },

    renderOverview: function () {
      var body = this.dom.overviewBody;
      if (!body) return;

      if (this.configError) {
        body.innerHTML = '<div class="cms-error">Unable to load CMS configuration from the server. Reload the page or verify the /api/cms/dashboard/config endpoint.</div>';
        return;
      }
      if (!this.config || !this.currentData) {
        body.innerHTML = '<div class="cms-loading"><span class="cms-spinner" aria-hidden="true"></span><span>Loading overview…</span></div>';
        return;
      }

      var cfg = this.currentPortalConfig();
      var cur = this.currentData || {};
      var banners = cur.banners || [];
      var sections = cur.page_sections || [];
      var activeBanners = banners.filter(function (b) { return b.active !== false; }).length;
      var visibleSections = sections.filter(function (s) { return s.visible !== false; }).length;
      var status = cfg.draft ? 'draft' : (cfg.status || 'published');
      var heroTitle = (cur.hero && cur.hero.title) || '—';

      var statusPill = '<span class="cms-pill ' + (status === 'published' ? 'cms-pill-on' : 'cms-pill-lock') + '">' + this.statusLabel(status) + '</span>';

      var html =
        '<div class="cms-stat-grid">' +
          '<div class="cms-stat-card"><div class="cms-stat-label">Banner slides</div><div class="cms-stat-value">' + activeBanners + ' / ' + banners.length + '</div></div>' +
          '<div class="cms-stat-card"><div class="cms-stat-label">Page sections</div><div class="cms-stat-value">' + visibleSections + ' / ' + sections.length + '</div></div>' +
          '<div class="cms-stat-card"><div class="cms-stat-label">Media assets</div><div class="cms-stat-value" id="cmsStatMedia">—</div></div>' +
          '<div class="cms-stat-card"><div class="cms-stat-label">Publication status</div><div class="cms-stat-value">' + statusPill + '</div></div>' +
        '</div>' +
        '<div class="cms-block-title">Content summary</div>' +
        '<div class="cms-kv-list">' +
          this.kvRow('Portal', this.escapeHtml(this.portalLabel(this.portal))) +
          this.kvRow('Campus scope', this.escapeHtml(this.campusLabel(this.campus))) +
          this.kvRow('Hero heading', this.escapeHtml(heroTitle)) +
          this.kvRow('Last published', this.formatTimestamp(cfg.last_published)) +
          this.kvRow('Published by', this.escapeHtml(cfg.published_by || '—')) +
        '</div>';

      body.innerHTML = html;

      // Live media count from the media library endpoint (no hardcoded values)
      fetch('/api/cms/dashboard/media')
        .then(function (r) { return r.json(); })
        .then(function (res) {
          var el = document.getElementById('cmsStatMedia');
          if (el && res && res.success) el.textContent = String((res.data || []).length);
        })
        .catch(function () {
          var el = document.getElementById('cmsStatMedia');
          if (el) el.textContent = 'n/a';
        });
    },

    renderPublishing: function () {
      var el = this.dom.publishStatus;
      if (!el) return;

      if (this.configError) {
        el.innerHTML = '<div class="cms-error">Unable to load publication status. Verify the server connection and reload.</div>';
        return;
      }
      if (!this.config || !this.currentData) {
        el.innerHTML = '<div class="cms-loading"><span class="cms-spinner" aria-hidden="true"></span><span>Loading publication status…</span></div>';
        return;
      }

      var cfg = this.currentPortalConfig();
      var status = cfg.draft ? 'draft' : (cfg.status || 'published');
      var statusPill = '<span class="cms-pill ' + (status === 'published' ? 'cms-pill-on' : 'cms-pill-lock') + '">' + this.statusLabel(status) + '</span>';

      el.innerHTML =
        this.kvRow('Publication status', statusPill) +
        this.kvRow('Last published', this.formatTimestamp(cfg.last_published)) +
        this.kvRow('Published by', this.escapeHtml(cfg.published_by || '—')) +
        this.kvRow('Draft updated', this.formatTimestamp(cfg.draft_updated_at)) +
        this.kvRow('Scheduled at', this.formatTimestamp(cfg.scheduled_at));

      this.renderVisibility();
    },

    renderVisibility: function () {
      var el = this.dom.visibilityList;
      if (!el) return;
      var self = this;
      var cur = this.currentData || {};
      var hero = cur.hero || {};
      var rows = '';

      rows += '<div class="cms-visibility-row"><span>Hero section</span><span class="cms-pill ' +
        (hero.visible !== false ? 'cms-pill-on' : 'cms-pill-off') + '">' +
        (hero.visible !== false ? 'Visible' : 'Hidden') + '</span></div>';

      (cur.page_sections || []).forEach(function (s) {
        var lock = s.locked ? ' <span class="cms-pill cms-pill-lock">Essential</span>' : '';
        rows += '<div class="cms-visibility-row"><span>' + self.escapeHtml(s.name || 'Section') + lock + '</span>' +
          '<span class="cms-pill ' + (s.visible !== false ? 'cms-pill-on' : 'cms-pill-off') + '">' +
          (s.visible !== false ? 'Visible' : 'Hidden') + '</span></div>';
      });

      var banners = cur.banners || [];
      var active = banners.filter(function (b) { return b.active !== false; }).length;
      rows += '<div class="cms-visibility-row"><span>Banner carousel</span>' +
        '<span class="cms-pill ' + (active > 0 ? 'cms-pill-on' : 'cms-pill-off') + '">' +
        active + ' active / ' + banners.length + '</span></div>';

      el.innerHTML = rows;
    },

    activityIcon: function (action) {
      var map = {
        content_published: 'publish',
        draft_saved: 'save',
        content_scheduled: 'event_upcoming',
        version_restored: 'restore',
        media_uploaded: 'cloud_upload',
        media_deleted: 'delete'
      };
      return map[action] || 'history';
    },

    activityLabel: function (action) {
      var map = {
        content_published: 'Published',
        draft_saved: 'Draft saved',
        content_scheduled: 'Scheduled',
        version_restored: 'Version restored',
        media_uploaded: 'Media uploaded',
        media_deleted: 'Media deleted'
      };
      return map[action] || (action || 'Activity');
    },

    renderActivity: function () {
      var self = this;
      var el = this.dom.activityList;
      if (!el) return;

      el.innerHTML = '<div class="cms-loading"><span class="cms-spinner" aria-hidden="true"></span><span>Loading activity…</span></div>';

      fetch('/api/cms/dashboard/audit?portal=' + encodeURIComponent(this.portal) + '&limit=40')
        .then(function (r) { return r.json(); })
        .then(function (res) {
          var logs = (res && res.success && res.data) ? res.data : [];
          if (!logs.length) {
            el.innerHTML = '<div class="cms-empty">No recorded CMS activity for the ' + self.escapeHtml(self.portalLabel(self.portal)) + ' yet.</div>';
            return;
          }
          var html = '';
          logs.forEach(function (ev) {
            html +=
              '<div class="cms-activity-item">' +
                '<div class="cms-activity-icon"><span class="material-symbols-outlined" style="font-size:16px" aria-hidden="true">' + self.activityIcon(ev.action) + '</span></div>' +
                '<div class="cms-activity-main">' +
                  '<div class="cms-activity-title">' + self.escapeHtml(ev.details || self.activityLabel(ev.action)) + '</div>' +
                  '<div class="cms-activity-meta">' + self.escapeHtml(self.activityLabel(ev.action)) + ' · ' +
                    self.escapeHtml(ev.actor_name || ev.actor_email || 'System') + ' · ' + self.formatTimestamp(ev.timestamp) + '</div>' +
                '</div>' +
                '<span class="cms-pill ' + (ev.outcome === 'SUCCESS' ? 'cms-pill-on' : 'cms-pill-off') + '">' + self.escapeHtml(ev.outcome || 'SUCCESS') + '</span>' +
              '</div>';
          });
          el.innerHTML = html;
        })
        .catch(function () {
          el.innerHTML = '<div class="cms-error">Unable to load activity history. Check the server connection and try again.</div>';
        });
    },

    loadConfig: function () {
      var self = this;
      fetch('/api/cms/dashboard/config')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (res.success && res.data) {
            self.config = res.data;
            self.configError = false;
            self.populateEditor();
            self.fetchRuntimePreview();
          } else {
            self.configError = true;
          }
          self.refreshActivePanel();
        })
        .catch(function (err) {
          self.configError = true;
          console.error('[CMS] Failed to load configuration:', err);
          self.refreshActivePanel();
        });
    },

    populateEditor: function () {
      if (!this.config || !this.config.portals_config) return;
      var portalCfg = this.config.portals_config[this.portal];
      if (!portalCfg) return;

      var current = portalCfg.draft || portalCfg;
      this.currentData = JSON.parse(JSON.stringify(current));

      // Status Badge
      this.updateStatusBadge(portalCfg.draft ? 'draft' : portalCfg.status || 'published');

      // Populate Hero
      var hero = this.currentData.hero || {};
      var dateCfg = hero.date_config || {};
      if (this.dom.heroTitle) this.dom.heroTitle.value = hero.title || '';
      if (this.dom.heroDescription) this.dom.heroDescription.value = hero.description || '';
      if (this.dom.heroGreeting) this.dom.heroGreeting.value = hero.greeting_template || '';
      if (this.dom.heroDateVisible) this.dom.heroDateVisible.checked = dateCfg.visible !== false;
      if (this.dom.heroDateFormat) this.dom.heroDateFormat.value = dateCfg.format || 'full';
      if (this.dom.heroAlignment) this.dom.heroAlignment.value = hero.text_alignment || 'left';

      // Populate Carousel Settings
      var car = this.currentData.carousel_settings || {};
      if (this.dom.carouselAutoplay) this.dom.carouselAutoplay.checked = car.autoplay !== false;
      if (this.dom.carouselInterval) this.dom.carouselInterval.value = car.interval_seconds || 6;
      if (this.dom.carouselArrows) this.dom.carouselArrows.checked = car.show_arrows !== false;
      if (this.dom.carouselDots) this.dom.carouselDots.checked = car.show_dots !== false;

      // Populate Banner list and form
      this.renderBannerList();
      this.loadBannerForm(this.activeBannerIdx);
    },

    renderBannerList: function () {
      var self = this;
      var banners = this.currentData.banners || [];
      var html = '';

      banners.forEach(function (b, idx) {
        var isEditing = idx === self.activeBannerIdx;
        html +=
          '<div class="cms-banner-item' + (isEditing ? ' active-editing' : '') + '" data-idx="' + idx + '">' +
            '<img class="cms-banner-thumb" src="' + (b.image_url || 'assets/images/logo.png') + '" alt="' + (b.alt_text || 'Banner') + '">' +
            '<div class="cms-banner-meta" onclick="CMS.selectBanner(' + idx + ')">' +
              '<div class="cms-banner-name font-medium">' + (b.name || 'Untitled Slide') + '</div>' +
              '<div class="cms-banner-sub">Order ' + (idx + 1) + ' · ' + (b.active ? '<span class="text-emerald-700">Active</span>' : '<span class="text-slate-400">Hidden</span>') + '</div>' +
            '</div>' +
            '<div class="cms-item-actions">' +
              '<button type="button" class="cms-icon-btn" title="Move Up" onclick="CMS.moveBanner(' + idx + ', -1)"' + (idx === 0 ? ' disabled' : '') + '><span class="mi" style="font-size:16px">arrow_upward</span></button>' +
              '<button type="button" class="cms-icon-btn" title="Move Down" onclick="CMS.moveBanner(' + idx + ', 1)"' + (idx === banners.length - 1 ? ' disabled' : '') + '><span class="mi" style="font-size:16px">arrow_downward</span></button>' +
              '<button type="button" class="cms-icon-btn danger" title="Delete" onclick="CMS.deleteBanner(' + idx + ')"><span class="mi" style="font-size:16px">delete</span></button>' +
            '</div>' +
          '</div>';
      });

      if (this.dom.bannerList) this.dom.bannerList.innerHTML = html;
    },

    selectBanner: function (idx) {
      this.saveActiveBannerFormToMemory();
      this.activeBannerIdx = idx;
      this.renderBannerList();
      this.loadBannerForm(idx);
      this.debounceSync();
    },

    loadBannerForm: function (idx) {
      var banners = this.currentData.banners || [];
      var b = banners[idx];
      if (!b) return;

      if (this.dom.bannerName) this.dom.bannerName.value = b.name || '';
      if (this.dom.bannerHeading) this.dom.bannerHeading.value = b.heading || '';
      if (this.dom.bannerSubtitle) this.dom.bannerSubtitle.value = b.subtitle || '';
      if (this.dom.bannerDescription) this.dom.bannerDescription.value = b.description || '';
      if (this.dom.bannerImageUrl) this.dom.bannerImageUrl.value = b.image_url || '';
      if (this.dom.bannerAltText) this.dom.bannerAltText.value = b.alt_text || '';
      if (this.dom.bannerBtnLabel) this.dom.bannerBtnLabel.value = b.button_label || '';
      if (this.dom.bannerBtnUrl) this.dom.bannerBtnUrl.value = b.button_url || '';
      if (this.dom.bannerActive) this.dom.bannerActive.checked = b.active !== false;
    },

    saveActiveBannerFormToMemory: function () {
      var banners = this.currentData.banners || [];
      if (!banners[this.activeBannerIdx]) return;
      var b = banners[this.activeBannerIdx];

      if (this.dom.bannerName) b.name = this.dom.bannerName.value;
      if (this.dom.bannerHeading) b.heading = this.dom.bannerHeading.value;
      if (this.dom.bannerSubtitle) b.subtitle = this.dom.bannerSubtitle.value;
      if (this.dom.bannerDescription) b.description = this.dom.bannerDescription.value;
      if (this.dom.bannerImageUrl) b.image_url = this.dom.bannerImageUrl.value;
      if (this.dom.bannerAltText) b.alt_text = this.dom.bannerAltText.value;
      if (this.dom.bannerBtnLabel) b.button_label = this.dom.bannerBtnLabel.value;
      if (this.dom.bannerBtnUrl) b.button_url = this.dom.bannerBtnUrl.value;
      if (this.dom.bannerActive) b.active = this.dom.bannerActive.checked;
    },

    addNewBanner: function () {
      this.saveActiveBannerFormToMemory();
      var banners = this.currentData.banners || [];
      var newId = 'ban-' + this.portal.substring(0, 3) + '-' + (banners.length + 1).toString().padStart(3, '0');
      var newBanner = {
        id: newId,
        name: 'New Promotional Slide',
        heading: 'Special Announcement',
        subtitle: 'Highlights and key events for students',
        description: 'Detailed information regarding academic schedule',
        image_url: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=320&fit=crop',
        alt_text: 'School campus',
        button_label: 'Learn More',
        button_url: '#',
        target_portals: [this.portal],
        target_campuses: ['all'],
        order: banners.length + 1,
        status: 'published',
        active: true
      };
      banners.push(newBanner);
      this.activeBannerIdx = banners.length - 1;
      this.renderBannerList();
      this.loadBannerForm(this.activeBannerIdx);
      this.markUnsaved();
      this.debounceSync();
      this.showToast('Added new slide.');
    },

    moveBanner: function (idx, delta) {
      this.saveActiveBannerFormToMemory();
      var banners = this.currentData.banners || [];
      var targetIdx = idx + delta;
      if (targetIdx < 0 || targetIdx >= banners.length) return;

      var temp = banners[idx];
      banners[idx] = banners[targetIdx];
      banners[targetIdx] = temp;

      // Re-index order
      banners.forEach(function (b, i) { b.order = i + 1; });
      this.activeBannerIdx = targetIdx;
      this.renderBannerList();
      this.loadBannerForm(targetIdx);
      this.markUnsaved();
      this.debounceSync();
    },

    deleteBanner: function (idx) {
      var banners = this.currentData.banners || [];
      if (banners.length <= 1) {
        alert('At least one banner must be retained for the portal layout.');
        return;
      }
      if (!confirm('Are you sure you want to remove this banner slide?')) return;

      banners.splice(idx, 1);
      banners.forEach(function (b, i) { b.order = i + 1; });
      this.activeBannerIdx = Math.max(0, idx - 1);
      this.renderBannerList();
      this.loadBannerForm(this.activeBannerIdx);
      this.markUnsaved();
      this.debounceSync();
      this.showToast('Banner slide deleted.');
    },

    renderPageSections: function () {
      // Superseded by the Global Sidebar Manager (assets/js/admin-sidebar-manager.js).
      // Dashboard page-section data is retained in the CMS payload; navigation is
      // now managed through the centralized navigation configuration store.
    },

    debounceSync: function () {
      var self = this;
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(function () {
        self.updateLivePreviewDOM();
      }, 120);
    },

    updateLivePreviewDOM: function () {
      // 1. Hero text update
      var title = this.dom.heroTitle ? this.dom.heroTitle.value : 'Welcome to your dashboard';
      var greetingTmpl = this.dom.heroGreeting ? this.dom.heroGreeting.value : 'Hello, {first_name}!';
      var dateVisible = this.dom.heroDateVisible ? this.dom.heroDateVisible.checked : true;
      var dateFormat = this.dom.heroDateFormat ? this.dom.heroDateFormat.value : 'full';
      var alignment = this.dom.heroAlignment ? this.dom.heroAlignment.value : 'left';

      // Resolve greeting token sample
      var names = { student: 'Nrinphouneta', teacher: 'Sarah', principal: 'Ly Bunheng', admin: 'Panha' };
      var resolvedGreeting = greetingTmpl
        .replace(/{first_name}/g, names[this.portal] || 'Scholar')
        .replace(/{full_name}/g, (names[this.portal] || 'Scholar') + ' Hok')
        .replace(/{role}/g, this.portal.toUpperCase())
        .replace(/{school_name}/g, "New Gateway International School")
        .replace(/{campus_name}/g, "Phnom Penh Main Campus")
        .replace(/{academic_year}/g, "2026–2027");

      if (this.dom.pvHeroTitle) this.dom.pvHeroTitle.textContent = title;
      if (this.dom.pvHeroGreeting) this.dom.pvHeroGreeting.textContent = resolvedGreeting;
      if (this.dom.pvHeroDate) {
        this.dom.pvHeroDate.style.display = dateVisible ? 'block' : 'none';
        var d = new Date();
        this.dom.pvHeroDate.textContent = dateFormat === 'iso' ? d.toISOString().split('T')[0] : 'Monday, November 9, 2026';
      }
      if (this.dom.pvHero) {
        this.dom.pvHero.style.textAlign = alignment;
      }

      // 2. Banner update
      var banners = this.currentData.banners || [];
      var activeBanner = banners[this.activeBannerIdx] || banners[0];
      if (activeBanner) {
        if (this.dom.pvPromoImg) this.dom.pvPromoImg.src = activeBanner.image_url || '';
        if (this.dom.pvPromoHeading) this.dom.pvPromoHeading.innerHTML = activeBanner.heading || '';
        if (this.dom.pvPromoSub) this.dom.pvPromoSub.textContent = activeBanner.subtitle || '';
        if (this.dom.pvPromoBtn) {
          this.dom.pvPromoBtn.textContent = activeBanner.button_label || 'Explore';
          this.dom.pvPromoBtn.style.display = activeBanner.button_label ? 'inline-flex' : 'none';
        }
      }

      // 3. Page Section Visibility simulation
      var sections = this.currentData.page_sections || [];
      var bannerSec = sections.find(function (s) { return s.id === 'sec-banner'; });
      var pvBannerBlock = document.getElementById('pvBannerBlock');
      if (pvBannerBlock && bannerSec) {
        pvBannerBlock.style.display = bannerSec.visible ? 'block' : 'none';
      }
    },

    fetchRuntimePreview: function () {
      var self = this;
      fetch('/api/cms/dashboard/content?portal=' + this.portal + '&campus=' + this.campus + '&mode=draft')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (res.success && res.data) {
            self.updateLivePreviewDOM();
          }
        });
    },

    markUnsaved: function () {
      this.hasUnsavedChanges = true;
      this.updateStatusBadge('draft');
    },

    updateStatusBadge: function (status) {
      if (!this.dom.statusBadge) return;
      var el = this.dom.statusBadge;
      if (status === 'draft') {
        el.className = 'cms-status-pill cms-status-draft';
        el.innerHTML = '<span class="mi" style="font-size:14px">edit_note</span>Draft (Unpublished Changes)';
      } else if (status === 'scheduled') {
        el.className = 'cms-status-pill cms-status-scheduled';
        el.innerHTML = '<span class="mi" style="font-size:14px">schedule</span>Scheduled for Publication';
      } else {
        el.className = 'cms-status-pill cms-status-published';
        el.innerHTML = '<span class="mi" style="font-size:14px">check_circle</span>Published (Live)';
      }
    },

    assemblePayload: function () {
      this.saveActiveBannerFormToMemory();
      return {
        hero: {
          title: this.dom.heroTitle.value,
          description: this.dom.heroDescription.value,
          greeting_template: this.dom.heroGreeting.value,
          text_alignment: this.dom.heroAlignment.value,
          visible: true,
          date_config: {
            visible: this.dom.heroDateVisible.checked,
            format: this.dom.heroDateFormat.value,
            timezone: 'Asia/Phnom_Penh',
            language: 'en'
          },
          appearance: { height: 'default', overlay_strength: 35 }
        },
        banners: this.currentData.banners || [],
        carousel_settings: {
          autoplay: this.dom.carouselAutoplay.checked,
          interval_seconds: parseInt(this.dom.carouselInterval.value, 10) || 6,
          show_arrows: this.dom.carouselArrows.checked,
          show_dots: this.dom.carouselDots.checked,
          pause_on_hover: true,
          respect_reduced_motion: true
        },
        page_sections: this.currentData.page_sections || []
      };
    },

    saveDraft: function () {
      var self = this;
      var payload = this.assemblePayload();
      fetch('/api/cms/dashboard/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portal: this.portal, draft: payload })
      })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (res.success) {
          self.hasUnsavedChanges = false;
          self.updateStatusBadge('draft');
          self.showToast('Draft saved successfully without affecting live dashboard.');
        } else {
          alert('Failed to save draft: ' + (res.error || 'Server error'));
        }
      });
    },

    publishContent: function () {
      var self = this;
      if (!confirm('Publish all changes immediately to the live ' + this.portal.toUpperCase() + ' dashboard?')) return;

      var payload = this.assemblePayload();
      fetch('/api/cms/dashboard/publish', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          portal: this.portal,
          payload: payload,
          summary: 'Published content updates for ' + this.portal + ' dashboard'
        })
      })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (res.success) {
          self.hasUnsavedChanges = false;
          self.updateStatusBadge('published');
          self.showToast('Published live successfully! (Version: ' + res.version.version_id + ')');
          self.loadConfig();
        } else {
          alert('Publish error: ' + (res.error || 'Unknown error'));
        }
      });
    },

    openScheduleModal: function () {
      var self = this;
      var html =
        '<div class="cms-form-group">' +
          '<label class="cms-label font-medium">Select Publication Date & Time</label>' +
          '<input type="datetime-local" class="cms-input" id="cmsScheduleTimeInput">' +
          '<div class="cms-hint">System will automatically promote this draft to live at the specified timestamp.</div>' +
        '</div>';

      this.openModal('Schedule Future Publication', html, function () {
        var dt = document.getElementById('cmsScheduleTimeInput').value;
        if (!dt) { alert('Please select a valid date and time.'); return; }
        var payload = self.assemblePayload();

        fetch('/api/cms/dashboard/schedule', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ portal: self.portal, scheduled_at: dt, payload: payload })
        })
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (res.success) {
            self.closeModal();
            self.updateStatusBadge('scheduled');
            self.showToast('Publication scheduled for ' + dt);
          } else {
            alert('Scheduling failed: ' + res.error);
          }
        });
      }, 'Schedule Publication');
    },

    openVersionsModal: function () {
      var self = this;
      fetch('/api/cms/dashboard/versions?portal=' + this.portal)
        .then(function (res) { return res.json(); })
        .then(function (res) {
          var versions = (res.success && res.data) ? res.data : [];
          var html = '<div style="display:flex; flex-direction:column; gap:10px;">';

          if (versions.length === 0) {
            html += '<div class="text-sm text-slate-500 py-4 text-center">No past version snapshots available for this portal.</div>';
          } else {
            versions.forEach(function (v) {
              html +=
                '<div style="padding:12px; border:1px solid var(--cms-border); border-radius:10px; background:var(--cms-off-white); display:flex; align-items:center; justify-content:space-between;">' +
                  '<div>' +
                    '<div class="text-xs font-medium text-slate-800">' + v.version_id + ' · ' + (v.summary || 'Content snapshot') + '</div>' +
                    '<div class="text-[11px] text-slate-500 mt-1">' + v.timestamp + ' by ' + (v.author_name || v.author) + '</div>' +
                  '</div>' +
                  '<button type="button" class="cms-btn cms-btn-secondary" onclick="CMS.restoreVersion(\'' + v.version_id + '\')"><span class="mi" style="font-size:15px">restore</span>Restore</button>' +
                '</div>';
            });
          }
          html += '</div>';

          self.openModal('Version History & Instant Rollback', html, null, null);
        });
    },

    restoreVersion: function (versionId) {
      var self = this;
      if (!confirm('Revert all ' + this.portal.toUpperCase() + ' dashboard settings to snapshot ' + versionId + '?')) return;

      fetch('/api/cms/dashboard/restore', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ version_id: versionId })
      })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (res.success) {
          self.closeModal();
          self.showToast('Reverted to version ' + versionId);
          self.loadConfig();
        } else {
          alert('Restore failed: ' + res.error);
        }
      });
    },

    renderMediaLibrary: function () {
      var self = this;
      fetch('/api/cms/dashboard/media')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          var media = (res.success && res.data) ? res.data : [];
          var html = '';
          media.forEach(function (m) {
            html +=
              '<div class="cms-media-card" title="' + m.filename + '">' +
                '<img src="' + m.url + '" alt="' + (m.alt_text || 'Media') + '">' +
                '<div class="cms-media-card-info">' +
                  '<div class="truncate font-medium text-slate-700">' + m.filename + '</div>' +
                  '<div class="text-slate-400 text-[10px]">' + m.width + 'x' + m.height + ' · ' + m.size_kb + 'KB</div>' +
                '</div>' +
                '<button type="button" class="cms-icon-btn danger" style="position:absolute; top:4px; right:4px; background:rgba(255,255,255,0.9)" onclick="CMS.deleteMediaItem(\'' + m.id + '\')"><span class="mi" style="font-size:15px">delete</span></button>' +
              '</div>';
          });
          if (self.dom.mediaGrid) self.dom.mediaGrid.innerHTML = html;
        });
    },

    openMediaPickerModal: function () {
      var self = this;
      fetch('/api/cms/dashboard/media')
        .then(function (res) { return res.json(); })
        .then(function (res) {
          var media = (res.success && res.data) ? res.data : [];
          var html = '<div class="cms-media-grid" style="max-height:420px; overflow-y:auto;">';
          media.forEach(function (m) {
            html +=
              '<div class="cms-media-card" onclick="CMS.selectMediaForBanner(\'' + m.url + '\', \'' + (m.alt_text || '') + '\')">' +
                '<img src="' + m.url + '" alt="' + m.alt_text + '">' +
                '<div class="cms-media-card-info">' +
                  '<div class="truncate font-medium">' + m.filename + '</div>' +
                  '<div class="text-[10px] text-slate-400">' + m.width + 'x' + m.height + '</div>' +
                '</div>' +
              '</div>';
          });
          html += '</div>';

          self.openModal('Select Image from Media Library', html, null, null);
        });
    },

    selectMediaForBanner: function (url, alt) {
      if (this.dom.bannerImageUrl) this.dom.bannerImageUrl.value = url;
      if (this.dom.bannerAltText && alt) this.dom.bannerAltText.value = alt;
      this.saveActiveBannerFormToMemory();
      this.closeModal();
      this.markUnsaved();
      this.debounceSync();
      this.showToast('Banner image selected.');
    },

    uploadFile: function (file) {
      var self = this;
      var formData = new FormData();
      formData.append('file', file);
      formData.append('alt_text', file.name.split('.')[0]);

      fetch('/api/cms/dashboard/media/upload', {
        method: 'POST',
        body: formData
      })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (res.success && res.data) {
          self.showToast('Image uploaded successfully (' + res.data.width + 'x' + res.data.height + 'px).');
          self.renderMediaLibrary();
        } else {
          alert('Upload failed: ' + (res.error || 'Server error'));
        }
      });
    },

    deleteMediaItem: function (mediaId) {
      var self = this;
      if (!confirm('Are you sure you want to delete this media item?')) return;

      fetch('/api/cms/dashboard/media/' + mediaId, { method: 'DELETE' })
        .then(function (res) { return res.json(); })
        .then(function (res) {
          if (res.success) {
            self.showToast('Media deleted.');
            self.renderMediaLibrary();
          } else {
            alert('Cannot delete: ' + res.error);
          }
        });
    },

    openModal: function (title, bodyHTML, onConfirm, confirmText) {
      this.dom.modalTitle.textContent = title;
      this.dom.modalBody.innerHTML = bodyHTML;
      var footer = document.getElementById('cmsModalFooter');
      if (onConfirm) {
        footer.style.display = 'flex';
        var btn = document.getElementById('cmsModalConfirmBtn');
        btn.textContent = confirmText || 'Confirm';
        btn.onclick = onConfirm;
      } else {
        footer.style.display = 'none';
      }
      this.dom.modalBackdrop.classList.add('open');
    },

    closeModal: function () {
      this.dom.modalBackdrop.classList.remove('open');
    },

    showToast: function (msg) {
      if (!this.dom.toast) return;
      var t = this.dom.toast;
      t.textContent = msg;
      t.style.opacity = '1';
      t.style.transform = 'translateY(0)';
      setTimeout(function () {
        t.style.opacity = '0';
        t.style.transform = 'translateY(12px)';
      }, 3500);
    }
  };

  window.CMS = CMS;
  document.addEventListener('DOMContentLoaded', function () {
    CMS.init();
  });
})();

