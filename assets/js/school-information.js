/**
 * NGIS School Information & Academic Configuration Module
 * Client controller powering admin-school-information.html & principal-school-information.html
 */

(function (window, document) {
  'use strict';

  var SI = window.SCHOOL_INFO = window.SI = {};

  var state = {
    role: 'admin',
    user: null,
    activeSection: 'school_overview',
    config: null,
    permissions: null,
    loading: true,
    filterCalendarCat: 'all',
    auditFilterSection: 'all',
    auditQuery: ''
  };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function toast(msg, type) {
    var existing = document.getElementById('siToast');
    if (existing) existing.remove();
    var t = document.createElement('div');
    t.id = 'siToast';
    var cls = type === 'error' ? 'si-toast-error' : (type === 'info' ? 'si-toast-info' : 'si-toast-success');
    t.className = 'si-toast ' + cls;
    t.innerHTML = '<span class="material-symbols-outlined text-sm">' + (type === 'error' ? 'error' : (type === 'info' ? 'info' : 'check_circle')) + '</span><span>' + esc(msg) + '</span>';
    document.body.appendChild(t);
    setTimeout(function () {
      t.style.opacity = '0';
      t.style.transform = 'translateY(10px)';
      setTimeout(function () { t.remove(); }, 300);
    }, 3500);
  }

  function apiCall(endpoint, method, data) {
    var opts = {
      method: method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Role': state.role,
        'X-User-Id': state.user ? state.user.id : (state.role === 'principal' ? 'PRN-2024-001' : (state.role === 'editor' ? 'USR-006' : 'ADM-2024-001')),
        'X-User-Name': state.user ? (state.user.firstName + ' ' + state.user.lastName) : (state.role === 'principal' ? 'Dr. Ly Bunheng' : (state.role === 'editor' ? 'Ms. Keo Sreymom' : 'Mr. Heng Samnang')),
        'X-User-Campus': state.role === 'editor' ? 'TK-MAIN' : 'ALL'
      }
    };
    if (data && method !== 'GET') {
      opts.body = JSON.stringify(data);
    }
    return fetch(endpoint, opts).then(function (res) {
      return res.json().then(function (json) {
        if (!res.ok && res.status !== 202) {
          throw new Error(json.message || ('Server returned HTTP ' + res.status));
        }
        return json;
      });
    });
  }

  SI.init = function (containerId, initialRole) {
    state.role = initialRole || (window.PAGE && window.PAGE.role) || 'admin';
    if (window.NGISAuth) {
      state.user = NGISAuth.getUser();
    }
    SI.loadData(containerId);
  };

  SI.loadData = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;
    root.innerHTML = '<div class="flex items-center justify-center py-24 text-slate-400 gap-3"><span class="w-2.5 h-2.5 rounded-full bg-[#176B45] animate-ping"></span><span class="text-sm font-medium">Loading institutional configuration & permissions...</span></div>';

    apiCall('/api/school-config/full')
      .then(function (res) {
        state.config = res;
        state.permissions = res.userPermissions || {};
        SI.render(containerId);
      })
      .catch(function (err) {
        root.innerHTML = '<div class="p-6 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-sm">Failed to load school settings: ' + esc(err.message) + '</div>';
      });
  };

  SI.switchSection = function (secId) {
    state.activeSection = secId;
    var panel = document.getElementById('siActivePanel');
    if (panel) {
      panel.innerHTML = SI.renderActivePanel();
    }
    // Update left nav active classes
    var navItems = document.querySelectorAll('.si-nav-item');
    navItems.forEach(function (btn) {
      if (btn.dataset.sec === secId) btn.classList.add('active');
      else btn.classList.remove('active');
    });
    // Update mobile tabs
    var mobTabs = document.querySelectorAll('.si-mobile-tab');
    mobTabs.forEach(function (btn) {
      if (btn.dataset.sec === secId) {
        btn.classList.add('active');
        try {
          btn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        } catch (e) {}
      } else {
        btn.classList.remove('active');
      }
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  SI.switchRole = function (targetRole) {
    state.role = targetRole;
    if (window.NGISAuth) {
      NGISAuth.setDemoUser(targetRole);
    }
    toast('Switched view persona to: ' + targetRole.toUpperCase(), 'info');
    SI.loadData('schoolInfoRoot');
  };

  SI.render = function (containerId) {
    var root = document.getElementById(containerId);
    if (!root) return;

    var navSections = [
      { id: 'school_overview', label: 'School Overview', icon: 'dashboard', badge: 'Active' },
      { id: 'school_profile', label: 'School Profile', icon: 'account_balance' },
      { id: 'academic_years', label: 'Academic Years', icon: 'calendar_month', badge: '2026–27' },
      { id: 'campuses', label: 'Campuses', icon: 'apartment', badge: '3' },
      { id: 'school_days', label: 'School Days & Hours', icon: 'schedule' },
      { id: 'bell_schedule', label: 'Bell Schedule & Periods', icon: 'alarm', badge: '10' },
      { id: 'academic_calendar', label: 'Academic Calendar', icon: 'event', badge: '8 Events' },
      { id: 'departments', label: 'Departments & Grades', icon: 'layers' },
      { id: 'timetable_rules', label: 'Timetable Rules', icon: 'tune' },
      { id: 'staff_policies', label: 'Staff & Academic Policies', icon: 'policy' },
      { id: 'permissions_access', label: 'Permissions & Access', icon: 'security', adminOnly: true },
      { id: 'change_history', label: 'Change History', icon: 'history' }
    ];

    var permitted = state.permissions.permittedSections || [];

    var leftNavHtml = navSections.map(function (sec) {
      if (sec.adminOnly && state.role !== 'admin') return '';
      var isPermitted = (state.role === 'admin' || permitted.indexOf(sec.id) !== -1);
      var activeCls = (state.activeSection === sec.id) ? ' active' : '';
      var lockIcon = !isPermitted ? '<span class="material-symbols-outlined text-[14px] text-slate-300 ml-auto" title="Read Only / Requires Authorization">lock</span>' : '';
      return '<button type="button" class="si-nav-item' + activeCls + '" data-sec="' + sec.id + '" onclick="SCHOOL_INFO.switchSection(\'' + sec.id + '\')">' +
        '<span class="material-symbols-outlined si-nav-icon">' + sec.icon + '</span>' +
        '<span>' + esc(sec.label) + '</span>' +
        (sec.badge ? '<span class="si-nav-badge">' + esc(sec.badge) + '</span>' : '') +
        lockIcon +
      '</button>';
    }).join('');

    var mobileNavHtml = navSections.map(function (sec) {
      if (sec.adminOnly && state.role !== 'admin') return '';
      var activeCls = (state.activeSection === sec.id) ? ' active' : '';
      return '<button type="button" class="si-mobile-tab' + activeCls + '" data-sec="' + sec.id + '" onclick="SCHOOL_INFO.switchSection(\'' + sec.id + '\')">' +
        '<span class="material-symbols-outlined text-[16px]">' + sec.icon + '</span>' +
        '<span>' + esc(sec.label) + '</span>' +
      '</button>';
    }).join('');

    root.innerHTML = '' +
      '<div class="si-root">' +
        '<div class="space-y-4">' +
          
          '<!-- Top Header Toolbar -->' +
          '<div class="flex items-center justify-between pb-1">' +
            '<div>' +
              '<h1 class="si-title">School Information & Settings</h1>' +
            '</div>' +
          '</div>' +

          '<!-- Mobile Section Selector Bar -->' +
          '<div class="si-mobile-nav">' +
            mobileNavHtml +
          '</div>' +

          '<!-- Two Column Workspace Layout -->' +
          '<div class="si-layout">' +
            
            '<!-- Left Column: Navigation Sidebar -->' +
            '<div class="si-nav-card desktop-only">' +
              '<div class="si-nav-header">' +
                '<span class="text-xs font-medium text-slate-400 uppercase tracking-wider">Configuration Modules</span>' +
              '</div>' +
              '<div class="py-1.5">' +
                leftNavHtml +
              '</div>' +
              '<div class="p-3 bg-slate-50 border-t border-[#E1E9E3] text-[11px] text-slate-500 flex items-center justify-between">' +
                '<span>NGIS ERP v3.2</span>' +
                '<span class="font-mono text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">SYNC OK</span>' +
              '</div>' +
            '</div>' +

            '<!-- Right Column: Active Settings Panel -->' +
            '<div id="siActivePanel" class="si-panel">' +
              SI.renderActivePanel() +
            '</div>' +

          '</div>' +
        '</div>' +
      '</div>';
  };

  // ══════════════════════════════════════════════════════════════
  // Active Panel Router & Renderers
  // ══════════════════════════════════════════════════════════════

  SI.renderActivePanel = function () {
    switch (state.activeSection) {
      case 'school_overview': return SI.renderOverview();
      case 'school_profile': return SI.renderProfile();
      case 'academic_years': return SI.renderAcademicYears();
      case 'campuses': return SI.renderCampuses();
      case 'school_days': return SI.renderSchoolDays();
      case 'bell_schedule': return SI.renderBellSchedule();
      case 'academic_calendar': return SI.renderCalendar();
      case 'departments': return SI.renderDepartments();
      case 'timetable_rules': return SI.renderTimetableRules();
      case 'staff_policies': return SI.renderStaffPolicies();
      case 'permissions_access': return SI.renderPermissions();
      case 'change_history': return SI.renderChangeHistory();
      default: return SI.renderOverview();
    }
  };

  // 1. School Overview Renderer
  SI.renderOverview = function () {
    var c = state.config || {};
    var info = c.school_info || {};
    var years = c.academic_years || [];
    var actYear = years.find(function (y) { return y.isCurrent || y.status === 'active'; }) || {};
    var campuses = c.campuses || [];
    var sched = c.operating_schedule || {};
    var openDays = (sched.weeklyDays || []).filter(function (d) { return d.open; });
    var audit = c.audit_log || [];
    var lastAud = audit[0] || {};

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Institutional Overview</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Authoritative source of truth for New Gateway International School configuration.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            '<span class="si-badge si-badge-green"><span class="w-1.5 h-1.5 rounded-full bg-[#176B45]"></span><span>Active & Synchronized</span></span>' +
          '</div>' +
        '</div>' +

        '<!-- Institutional Hero Card -->' +
        '<div class="bg-gradient-to-r from-emerald-50/70 via-slate-50 to-emerald-50/40 p-4 sm:p-5 rounded-2xl border border-emerald-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">' +
          '<div class="flex items-center gap-3.5 sm:gap-4 min-w-0">' +
            '<div class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-white border border-[#E2E8F0] shadow-xs flex items-center justify-center p-2 shrink-0">' +
              '<img src="../../assets/images/logo.png" alt="NGIS" class="w-full h-full object-contain" onerror="this.src=\'../../assets/images/logo.png\'">' +
            '</div>' +
            '<div class="min-w-0 flex-1">' +
              '<h3 class="text-sm sm:text-base font-medium text-slate-900 truncate">' + esc(info.nameEnglish) + '</h3>' +
              '<p class="text-xs text-slate-600 font-khmer mt-0.5 truncate">' + esc(info.nameKhmer) + '</p>' +
              '<p class="text-[11px] text-slate-400 mt-1 font-mono truncate">License: ' + esc(info.moeysCode) + ' · Established ' + esc(info.establishedYear) + '</p>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center gap-2 flex-wrap w-full sm:w-auto">' +
            '<button type="button" class="si-btn si-btn-outline si-btn-sm flex-1 sm:flex-initial" onclick="SCHOOL_INFO.switchSection(\'school_profile\')">' +
              '<span class="material-symbols-outlined text-[16px]">edit</span><span>Edit Profile</span>' +
            '</button>' +
            '<button type="button" class="si-btn si-btn-primary si-btn-sm flex-1 sm:flex-initial" onclick="SCHOOL_INFO.switchSection(\'academic_years\')">' +
              '<span class="material-symbols-outlined text-[16px]">calendar_month</span><span>Academic Years</span>' +
            '</button>' +
          '</div>' +
        '</div>' +

        '<!-- Real Metrics Grid -->' +
        '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">' +
          
          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Active Academic Year</span>' +
            '<span class="text-base font-medium text-[#176B45] mt-1 block">' + esc(actYear.year || '2026–2027') + '</span>' +
            '<span class="text-[10px] text-slate-500 mt-0.5 block">' + esc(actYear.startDate) + ' to ' + esc(actYear.endDate) + '</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Campuses Operating</span>' +
            '<span class="text-base font-medium text-slate-800 mt-1 block">' + campuses.length + ' Facilities</span>' +
            '<span class="text-[10px] text-emerald-700 mt-0.5 block">100% active operational</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Weekly Operating Days</span>' +
            '<span class="text-base font-medium text-slate-800 mt-1 block">' + openDays.length + ' Days / Week</span>' +
            '<span class="text-[10px] text-slate-500 mt-0.5 block">' + (sched.saturdayEnabled ? 'Mon–Sat (Sat Morning)' : 'Mon–Fri') + '</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Operating Hours</span>' +
            '<span class="text-base font-medium text-slate-800 mt-1 block">07:00 – 17:10</span>' +
            '<span class="text-[10px] text-slate-500 mt-0.5 block">10 Academic Periods / Day</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Academic Departments</span>' +
            '<span class="text-base font-medium text-slate-800 mt-1 block">8 Divisions</span>' +
            '<span class="text-[10px] text-slate-500 mt-0.5 block">Math, Science, Languages, ICT</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Grade Levels Offered</span>' +
            '<span class="text-base font-medium text-slate-800 mt-1 block">6 Cohorts (G7–G12)</span>' +
            '<span class="text-[10px] text-slate-500 mt-0.5 block">Lower & Upper Secondary</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Current Term / Semester</span>' +
            '<span class="text-base font-medium text-slate-800 mt-1 block">Semester 1</span>' +
            '<span class="text-[10px] text-emerald-700 mt-0.5 block">Instructional week 9 of 20</span>' +
          '</div>' +

          '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl">' +
            '<span class="text-[11px] text-slate-400 block font-normal">Pending Revisions</span>' +
            '<span class="text-base font-medium ' + (c.pending_reviews && c.pending_reviews.length ? 'text-[#F28C28]' : 'text-slate-800') + ' mt-1 block">' + (c.pending_reviews ? c.pending_reviews.length : 0) + ' Requests</span>' +
            '<span class="text-[10px] text-slate-500 mt-0.5 block">' + (c.pending_reviews && c.pending_reviews.length ? 'Awaiting administrator review' : 'All approved') + '</span>' +
          '</div>' +

        '</div>' +

        '<!-- Quick Navigation Actions -->' +
        '<div class="pt-2">' +
          '<span class="text-xs font-medium text-slate-400 uppercase tracking-wider block mb-3">Quick Configuration Modules</span>' +
          '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">' +
            
            '<button type="button" class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-[#176B45] hover:shadow-xs transition text-left flex items-start gap-3 group" onclick="SCHOOL_INFO.switchSection(\'campuses\')">' +
              '<span class="p-2 bg-emerald-50 text-[#176B45] rounded-lg material-symbols-outlined text-xl">apartment</span>' +
              '<div>' +
                '<span class="text-xs font-medium text-slate-800 group-hover:text-[#176B45] block">Manage Campuses</span>' +
                '<p class="text-[11px] text-slate-500 mt-0.5">Tuol Kork Main, Chamkarmon, and STEM Robotics Hub.</p>' +
              '</div>' +
            '</button>' +

            '<button type="button" class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-[#176B45] hover:shadow-xs transition text-left flex items-start gap-3 group" onclick="SCHOOL_INFO.switchSection(\'school_days\')">' +
              '<span class="p-2 bg-emerald-50 text-[#176B45] rounded-lg material-symbols-outlined text-xl">schedule</span>' +
              '<div>' +
                '<span class="text-xs font-medium text-slate-800 group-hover:text-[#176B45] block">Operating Days & Hours</span>' +
                '<p class="text-[11px] text-slate-500 mt-0.5">Opening/closing times, shifts, and Saturday toggle.</p>' +
              '</div>' +
            '</button>' +

            '<button type="button" class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-[#176B45] hover:shadow-xs transition text-left flex items-start gap-3 group" onclick="SCHOOL_INFO.switchSection(\'bell_schedule\')">' +
              '<span class="p-2 bg-emerald-50 text-[#176B45] rounded-lg material-symbols-outlined text-xl">alarm</span>' +
              '<div>' +
                '<span class="text-xs font-medium text-slate-800 group-hover:text-[#176B45] block">Bell Schedule & Periods</span>' +
                '<p class="text-[11px] text-slate-500 mt-0.5">10 periods, recess preservation, and lunch break.</p>' +
              '</div>' +
            '</button>' +

            '<button type="button" class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-[#176B45] hover:shadow-xs transition text-left flex items-start gap-3 group" onclick="SCHOOL_INFO.switchSection(\'academic_calendar\')">' +
              '<span class="p-2 bg-emerald-50 text-[#176B45] rounded-lg material-symbols-outlined text-xl">event</span>' +
              '<div>' +
                '<span class="text-xs font-medium text-slate-800 group-hover:text-[#176B45] block">Academic Calendar</span>' +
                '<p class="text-[11px] text-slate-500 mt-0.5">National holidays, semester milestones, and exam periods.</p>' +
              '</div>' +
            '</button>' +

            '<button type="button" class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-[#176B45] hover:shadow-xs transition text-left flex items-start gap-3 group" onclick="SCHOOL_INFO.switchSection(\'timetable_rules\')">' +
              '<span class="p-2 bg-emerald-50 text-[#176B45] rounded-lg material-symbols-outlined text-xl">tune</span>' +
              '<div>' +
                '<span class="text-xs font-medium text-slate-800 group-hover:text-[#176B45] block">Timetable Generation Rules</span>' +
                '<p class="text-[11px] text-slate-500 mt-0.5">MoEYS 2-hr consecutive limit & double-booking prevention.</p>' +
              '</div>' +
            '</button>' +

            '<button type="button" class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-[#176B45] hover:shadow-xs transition text-left flex items-start gap-3 group" onclick="SCHOOL_INFO.switchSection(\'change_history\')">' +
              '<span class="p-2 bg-emerald-50 text-[#176B45] rounded-lg material-symbols-outlined text-xl">history</span>' +
              '<div>' +
                '<span class="text-xs font-medium text-slate-800 group-hover:text-[#176B45] block">Audit Log & History</span>' +
                '<p class="text-[11px] text-slate-500 mt-0.5">Authoritative change log with user, time, and revisions.</p>' +
              '</div>' +
            '</button>' +

          '</div>' +
        '</div>' +

        '<!-- Last Update Footer -->' +
        '<div class="pt-4 border-t border-[#E1E9E3] flex items-center justify-between text-xs text-slate-500 flex-wrap gap-2">' +
          '<span>Configuration last updated on: <span class="font-medium text-slate-700">' + esc(lastAud.timestamp || '2026-07-08 14:20') + '</span> by <span class="font-medium text-slate-700">' + esc(lastAud.userName || 'Administrator') + '</span></span>' +
          '<span class="text-emerald-700 flex items-center gap-1"><span class="material-symbols-outlined text-[16px]">verified</span><span>Dynamic ERP Broadcast Enabled</span></span>' +
        '</div>' +

      '</div>';
  };

  // 2. School Profile Renderer
  SI.renderProfile = function () {
    var c = state.config || {};
    var p = c.school_info || {};
    var canEdit = state.role === 'admin' || (state.permissions.permittedSections && state.permissions.permittedSections.indexOf('school_profile') !== -1);

    return '' +
      '<form id="formSchoolProfile" onsubmit="SCHOOL_INFO.saveProfile(event)" class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">School Profile & Institutional Identity</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Configure institutional names, official licenses, leadership, and public contact information.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="submit" class="si-btn si-btn-primary"><span class="material-symbols-outlined text-[16px]">save</span><span>Save Profile</span></button>' :
              '<span class="si-badge si-badge-amber"><span class="material-symbols-outlined text-[14px]">lock</span><span>Read Only Scope</span></span>') +
          '</div>' +
        '</div>' +

        '<!-- General Information Section -->' +
        '<div class="space-y-4">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">General Information</h3>' +
          
          '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Official School Name (English)</label>' +
              '<input type="text" name="nameEnglish" class="si-input" value="' + esc(p.nameEnglish) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Official School Name (Khmer)</label>' +
              '<input type="text" name="nameKhmer" class="si-input font-khmer" value="' + esc(p.nameKhmer) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
          '</div>' +

          '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Short Name / Acronym</label>' +
              '<input type="text" name="shortName" class="si-input" value="' + esc(p.shortName || 'NGIS') + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">MoEYS Registration Code</label>' +
              '<input type="text" name="moeysCode" class="si-input font-mono" value="' + esc(p.moeysCode) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Established Year</label>' +
              '<input type="number" name="establishedYear" class="si-input" value="' + esc(p.establishedYear) + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
          '</div>' +

          '<div class="si-form-group">' +
            '<label class="si-label">Institutional Description</label>' +
            '<textarea name="description" rows="2" class="si-textarea" ' + (!canEdit ? 'disabled' : '') + '>' + esc(p.description) + '</textarea>' +
          '</div>' +

          '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Accreditation Authorities</label>' +
              '<input type="text" name="accreditation" class="si-input" value="' + esc(p.accreditation) + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">School Motto / Vision</label>' +
              '<input type="text" name="motto" class="si-input" value="' + esc(p.motto) + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
          '</div>' +
        '</div>' +

        '<!-- Leadership & Administration -->' +
        '<div class="space-y-4 pt-3 border-t border-[#E1E9E3]">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Institutional Leadership</h3>' +
          
          '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Executive Principal</label>' +
              '<input type="text" name="principal" class="si-input" value="' + esc(p.principal) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Academic Director</label>' +
              '<input type="text" name="academicDirector" class="si-input" value="' + esc(p.academicDirector || 'Dr. Pov Sophea') + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">School Administrator</label>' +
              '<input type="text" name="administrator" class="si-input" value="' + esc(p.administrator) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
          '</div>' +
        '</div>' +

        '<!-- Contact & Location Information -->' +
        '<div class="space-y-4 pt-3 border-t border-[#E1E9E3]">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Contact & Location</h3>' +
          
          '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Primary Telephone</label>' +
              '<input type="text" name="phone" class="si-input" value="' + esc(p.phone) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Official Email</label>' +
              '<input type="email" name="email" class="si-input" value="' + esc(p.email) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Official Website</label>' +
              '<input type="url" name="website" class="si-input" value="' + esc(p.website) + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
          '</div>' +

          '<div class="si-form-group">' +
            '<label class="si-label">Main Physical Address</label>' +
            '<input type="text" name="address" class="si-input" value="' + esc(p.address) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +

          '<div class="grid grid-cols-1 md:grid-cols-3 gap-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Province / City</label>' +
              '<input type="text" name="provinceCity" class="si-input" value="' + esc(p.provinceCity || 'Phnom Penh') + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Country</label>' +
              '<input type="text" name="country" class="si-input" value="' + esc(p.country || 'Cambodia') + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Default Time Zone</label>' +
              '<input type="text" name="timezone" class="si-input" value="' + esc(p.timezone || 'Asia/Phnom_Penh (UTC+07:00)') + '" ' + (!canEdit ? 'disabled' : '') + '>' +
            '</div>' +
          '</div>' +
        '</div>' +

      '</form>';
  };

  SI.saveProfile = function (e) {
    if (e) e.preventDefault();
    var form = document.getElementById('formSchoolProfile');
    if (!form) return;
    var fd = new FormData(form);
    var payload = {};
    fd.forEach(function (val, key) { payload[key] = val; });

    apiCall('/api/school-config/profile', 'PUT', payload)
      .then(function (res) {
        toast('School profile updated and saved successfully.');
        state.config.school_info = res.data;
      })
      .catch(function (err) {
        toast(err.message, 'error');
      });
  };

  // 3. Academic Years Renderer
  SI.renderAcademicYears = function () {
    var c = state.config || {};
    var years = c.academic_years || [];
    var canEdit = state.role === 'admin' || state.role === 'principal';

    var rowsHtml = years.map(function (y) {
      var statusBadge = '';
      if (y.isCurrent || y.status === 'active') {
        statusBadge = '<span class="si-badge si-badge-green"><span class="w-1.5 h-1.5 rounded-full bg-[#176B45]"></span><span>Active Year</span></span>';
      } else if (y.status === 'upcoming') {
        statusBadge = '<span class="si-badge si-badge-blue">Upcoming</span>';
      } else if (y.status === 'draft') {
        statusBadge = '<span class="si-badge si-badge-amber">Draft</span>';
      } else {
        statusBadge = '<span class="si-badge si-badge-gray">Completed</span>';
      }

      var termsHtml = (y.terms || []).map(function (t) {
        return '<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-medium">' +
          esc(t.name) + ' (' + esc(t.startDate) + ' to ' + esc(t.endDate) + ')' +
        '</span>';
      }).join(' ');

      var activateBtn = '';
      if (!y.isCurrent && y.status !== 'active') {
        activateBtn = '<button type="button" class="si-btn si-btn-outline si-btn-sm" onclick="SCHOOL_INFO.confirmActivateYear(\'' + y.id + '\', \'' + esc(y.year) + '\')">' +
          '<span class="material-symbols-outlined text-[15px]">check_circle</span><span>Set Active</span>' +
        '</button>';
      }

      return '' +
        '<div class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-slate-300 transition space-y-3 ' + (y.isCurrent ? 'ring-1 ring-emerald-500 bg-emerald-50/20' : '') + '">' +
          '<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">' +
            '<div class="flex items-center gap-3">' +
              '<span class="w-9 h-9 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center material-symbols-outlined text-lg">calendar_month</span>' +
              '<div>' +
                '<span class="text-sm font-medium text-slate-900">' + esc(y.year) + '</span>' +
                '<span class="text-xs text-slate-400 block">' + esc(y.displayName || ('Academic Year ' + y.year)) + '</span>' +
              '</div>' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              statusBadge +
              activateBtn +
            '</div>' +
          '</div>' +
          '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-600 pt-2 border-t border-slate-100">' +
            '<div><span class="text-slate-400 font-normal">Academic Duration:</span> ' + esc(y.startDate) + ' to ' + esc(y.endDate) + '</div>' +
            '<div><span class="text-slate-400 font-normal">Enrollment Window:</span> ' + esc(y.enrollmentStart || '2026-07-01') + ' to ' + esc(y.enrollmentEnd || '2026-08-25') + '</div>' +
          '</div>' +
          '<div class="pt-2 flex items-center gap-2 flex-wrap">' +
            '<span class="text-[11px] text-slate-400">Semesters:</span>' +
            termsHtml +
          '</div>' +
        '</div>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Academic Year Management</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Define school years, term sequences, and activate the authoritative academic calendar scope.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="button" class="si-btn si-btn-primary" onclick="SCHOOL_INFO.showAddYearModal()"><span class="material-symbols-outlined text-[16px]">add</span><span>New Academic Year</span></button>' :
              '<span class="si-badge si-badge-amber">Editor: Activation Requires Approval</span>') +
          '</div>' +
        '</div>' +

        '<div class="space-y-3.5">' +
          rowsHtml +
        '</div>' +

        '<div class="p-3.5 bg-amber-50/70 border border-amber-200 rounded-xl text-xs text-amber-900 flex items-start gap-2.5">' +
          '<span class="material-symbols-outlined text-amber-700 text-lg flex-shrink-0 mt-0.5">info</span>' +
          '<p class="font-normal leading-relaxed">Safety Protection: Activating a new academic year updates the active scope across Timetables, Attendance, and Gradebook modules. Historical student records, past grades, and archived transcripts remain intact and immutable.</p>' +
        '</div>' +
      '</div>';
  };

  SI.showAddYearModal = function () {
    var modalHtml = '' +
      '<div class="si-modal-backdrop" id="modalBackdrop">' +
        '<div class="si-modal">' +
          '<div class="si-modal-header">' +
            '<h3 class="text-sm font-medium text-slate-900">Create New Academic Year</h3>' +
            '<button type="button" class="text-slate-400 hover:text-slate-600 material-symbols-outlined text-lg" onclick="SCHOOL_INFO.closeModal()">close</button>' +
          '</div>' +
          '<form onsubmit="SCHOOL_INFO.submitNewYear(event)" class="si-modal-body space-y-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Academic Year (Format: YYYY–YYYY)</label>' +
              '<input type="text" id="newYearName" class="si-input" placeholder="2027–2028" required>' +
            '</div>' +
            '<div class="grid grid-cols-2 gap-3">' +
              '<div class="si-form-group">' +
                '<label class="si-label">Instructional Start Date</label>' +
                '<input type="date" id="newYearStart" class="si-input" value="2027-09-01" required>' +
              '</div>' +
              '<div class="si-form-group">' +
                '<label class="si-label">Instructional End Date</label>' +
                '<input type="date" id="newYearEnd" class="si-input" value="2028-06-30" required>' +
              '</div>' +
            '</div>' +
            '<div class="grid grid-cols-2 gap-3">' +
              '<div class="si-form-group">' +
                '<label class="si-label">Enrollment Start</label>' +
                '<input type="date" id="newYearEnrollStart" class="si-input" value="2027-07-01">' +
              '</div>' +
              '<div class="si-form-group">' +
                '<label class="si-label">Enrollment Deadline</label>' +
                '<input type="date" id="newYearEnrollEnd" class="si-input" value="2027-08-25">' +
              '</div>' +
            '</div>' +
            '<div class="si-modal-footer -mx-5 -mb-5 mt-4">' +
              '<button type="button" class="si-btn si-btn-outline" onclick="SCHOOL_INFO.closeModal()">Cancel</button>' +
              '<button type="submit" class="si-btn si-btn-primary">Create Year</button>' +
            '</div>' +
          '</form>' +
        '</div>' +
      '</div>';

    var wrap = document.createElement('div');
    wrap.id = 'siModalContainer';
    wrap.innerHTML = modalHtml;
    document.body.appendChild(wrap);
  };

  SI.closeModal = function () {
    var m = document.getElementById('siModalContainer');
    if (m) m.remove();
  };

  SI.submitNewYear = function (e) {
    e.preventDefault();
    var yName = document.getElementById('newYearName').value.trim();
    var sDate = document.getElementById('newYearStart').value;
    var eDate = document.getElementById('newYearEnd').value;
    var enrollStart = document.getElementById('newYearEnrollStart').value;
    var enrollEnd = document.getElementById('newYearEnrollEnd').value;

    if (!yName) return;

    apiCall('/api/school-config/academic-years', 'POST', {
      year: yName,
      startDate: sDate,
      endDate: eDate,
      enrollmentStart: enrollStart,
      enrollmentEnd: enrollEnd,
      status: 'draft'
    }).then(function (res) {
      toast('Academic Year ' + yName + ' created successfully.');
      SI.closeModal();
      SI.loadData('schoolInfoRoot');
    }).catch(function (err) {
      toast(err.message, 'error');
    });
  };

  SI.confirmActivateYear = function (yearId, yearName) {
    var isEditor = (state.role === 'editor');
    var noticeText = isEditor ? 
      'As an Editor, your request to activate Academic Year ' + yearName + ' will be submitted to the Principal and Super Administrator for formal approval.' :
      'Are you sure you want to activate Academic Year ' + yearName + '? This will immediately broadcast as the active academic scope for Timetables, Attendance, and Class Registrations.';

    var modalHtml = '' +
      '<div class="si-modal-backdrop" id="modalBackdrop">' +
        '<div class="si-modal max-w-md">' +
          '<div class="si-modal-header">' +
            '<h3 class="text-sm font-medium text-slate-900">' + (isEditor ? 'Submit Activation Request' : 'Confirm Academic Year Activation') + '</h3>' +
            '<button type="button" class="text-slate-400 hover:text-slate-600 material-symbols-outlined text-lg" onclick="SCHOOL_INFO.closeModal()">close</button>' +
          '</div>' +
          '<div class="si-modal-body space-y-3">' +
            '<p class="text-xs text-slate-600 leading-relaxed font-normal">' + esc(noticeText) + '</p>' +
            '<div class="p-3 bg-emerald-50 text-emerald-800 rounded-lg text-xs font-mono">Target: ' + esc(yearName) + ' (' + esc(yearId) + ')</div>' +
          '</div>' +
          '<div class="si-modal-footer">' +
            '<button type="button" class="si-btn si-btn-outline" onclick="SCHOOL_INFO.closeModal()">Cancel</button>' +
            '<button type="button" class="si-btn si-btn-primary" onclick="SCHOOL_INFO.doActivateYear(\'' + yearId + '\')">' + (isEditor ? 'Submit Request' : 'Activate Now') + '</button>' +
          '</div>' +
        '</div>' +
      '</div>';

    var wrap = document.createElement('div');
    wrap.id = 'siModalContainer';
    wrap.innerHTML = modalHtml;
    document.body.appendChild(wrap);
  };

  SI.doActivateYear = function (yearId) {
    apiCall('/api/school-config/academic-years/' + yearId + '/activate', 'POST')
      .then(function (res) {
        SI.closeModal();
        toast(res.message);
        SI.loadData('schoolInfoRoot');
      })
      .catch(function (err) {
        toast(err.message, 'error');
      });
  };

  // 4. Campuses Renderer
  SI.renderCampuses = function () {
    var c = state.config || {};
    var campuses = c.campuses || [];
    var canEdit = state.role === 'admin' || state.role === 'principal';

    var cardsHtml = campuses.map(function (cmp) {
      return '' +
        '<div class="p-4 bg-white border border-[#E1E9E3] rounded-xl hover:border-slate-300 transition space-y-3">' +
          '<div class="flex items-start justify-between gap-2">' +
            '<div class="flex items-start gap-3">' +
              '<span class="w-10 h-10 rounded-xl bg-emerald-50 text-[#176B45] flex items-center justify-center material-symbols-outlined text-xl flex-shrink-0">apartment</span>' +
              '<div>' +
                '<h3 class="text-sm font-medium text-slate-900">' + esc(cmp.name) + '</h3>' +
                '<span class="text-xs text-slate-400 font-mono">Code: ' + esc(cmp.code) + ' · ' + esc(cmp.type) + '</span>' +
              '</div>' +
            '</div>' +
            '<span class="si-badge ' + (cmp.status === 'active' ? 'si-badge-green' : 'si-badge-gray') + '">' + esc(cmp.status.toUpperCase()) + '</span>' +
          '</div>' +
          '<p class="text-xs text-slate-600 font-normal"><span class="text-slate-400">Address:</span> ' + esc(cmp.address) + '</p>' +
          '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-600 pt-2 border-t border-slate-100">' +
            '<div><span class="text-slate-400 font-normal">Principal / Head:</span> ' + esc(cmp.principal || 'Dr. Ly Bunheng') + '</div>' +
            '<div><span class="text-slate-400 font-normal">Administrator:</span> ' + esc(cmp.administrator || 'Mr. Heng Samnang') + '</div>' +
            '<div><span class="text-slate-400 font-normal">Contact:</span> ' + esc(cmp.phone) + '</div>' +
            '<div><span class="text-slate-400 font-normal">Saturday Sessions:</span> ' + (cmp.saturdayEnabled ? '<span class="text-emerald-700 font-medium">Enabled (Morning)</span>' : 'Disabled') + '</div>' +
          '</div>' +
          '<div class="pt-2 flex items-center gap-1.5 flex-wrap">' +
            '<span class="text-[11px] text-slate-400">Levels:</span>' +
            (cmp.academicLevels || []).map(function (lvl) { return '<span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[10px] font-medium">' + esc(lvl) + '</span>'; }).join('') +
          '</div>' +
        '</div>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Campus Facility Management</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Manage institutional branches, facility administrators, and campus operating schedules.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="button" class="si-btn si-btn-primary" onclick="SCHOOL_INFO.showAddCampusModal()"><span class="material-symbols-outlined text-[16px]">add</span><span>New Campus</span></button>' :
              '<span class="si-badge si-badge-amber">Scope: ' + esc(state.permissions.campusScope || 'TK-MAIN') + '</span>') +
          '</div>' +
        '</div>' +

        '<div class="grid grid-cols-1 gap-4">' +
          cardsHtml +
        '</div>' +
      '</div>';
  };

  SI.showAddCampusModal = function () {
    var modalHtml = '' +
      '<div class="si-modal-backdrop" id="modalBackdrop">' +
        '<div class="si-modal">' +
          '<div class="si-modal-header">' +
            '<h3 class="text-sm font-medium text-slate-900">Add New Campus Facility</h3>' +
            '<button type="button" class="text-slate-400 hover:text-slate-600 material-symbols-outlined text-lg" onclick="SCHOOL_INFO.closeModal()">close</button>' +
          '</div>' +
          '<form onsubmit="SCHOOL_INFO.submitNewCampus(event)" class="si-modal-body space-y-4">' +
            '<div class="grid grid-cols-2 gap-3">' +
              '<div class="si-form-group">' +
                '<label class="si-label">Campus Name</label>' +
                '<input type="text" id="newCmpName" class="si-input" placeholder="e.g. Sensok Campus" required>' +
              '</div>' +
              '<div class="si-form-group">' +
                '<label class="si-label">Campus Code</label>' +
                '<input type="text" id="newCmpCode" class="si-input font-mono" placeholder="SS-BRANCH" required>' +
              '</div>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Physical Address</label>' +
              '<input type="text" id="newCmpAddress" class="si-input" placeholder="Phnom Penh" required>' +
            '</div>' +
            '<div class="grid grid-cols-2 gap-3">' +
              '<div class="si-form-group">' +
                '<label class="si-label">Telephone</label>' +
                '<input type="text" id="newCmpPhone" class="si-input" value="+855 23 888 780">' +
              '</div>' +
              '<div class="si-form-group">' +
                '<label class="si-label">Campus Principal</label>' +
                '<input type="text" id="newCmpPrincipal" class="si-input" value="Dr. Ly Bunheng">' +
              '</div>' +
            '</div>' +
            '<div class="si-modal-footer -mx-5 -mb-5 mt-4">' +
              '<button type="button" class="si-btn si-btn-outline" onclick="SCHOOL_INFO.closeModal()">Cancel</button>' +
              '<button type="submit" class="si-btn si-btn-primary">Save Campus</button>' +
            '</div>' +
          '</form>' +
        '</div>' +
      '</div>';

    var wrap = document.createElement('div');
    wrap.id = 'siModalContainer';
    wrap.innerHTML = modalHtml;
    document.body.appendChild(wrap);
  };

  SI.submitNewCampus = function (e) {
    e.preventDefault();
    var name = document.getElementById('newCmpName').value.trim();
    var code = document.getElementById('newCmpCode').value.trim().toUpperCase();
    var address = document.getElementById('newCmpAddress').value.trim();
    var phone = document.getElementById('newCmpPhone').value.trim();
    var prn = document.getElementById('newCmpPrincipal').value.trim();

    apiCall('/api/school-config/campuses', 'POST', {
      name: name,
      code: code,
      address: address,
      phone: phone,
      principal: prn,
      status: 'active'
    }).then(function (res) {
      toast('Campus ' + name + ' added successfully.');
      SI.closeModal();
      SI.loadData('schoolInfoRoot');
    }).catch(function (err) {
      toast(err.message, 'error');
    });
  };

  // 5. School Days & Operating Hours Renderer
  SI.renderSchoolDays = function () {
    var c = state.config || {};
    var sched = c.operating_schedule || {};
    var days = sched.weeklyDays || [];
    var canEdit = state.role === 'admin' || (state.permissions.permittedSections && state.permissions.permittedSections.indexOf('school_days') !== -1);

    var rowsHtml = days.map(function (d, idx) {
      return '' +
        '<tr>' +
          '<td class="font-medium text-slate-800">' +
            '<label class="inline-flex items-center gap-2 cursor-pointer">' +
              '<input type="checkbox" name="day_open_' + idx + '" class="rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]" ' + (d.open ? 'checked' : '') + ' ' + (!canEdit ? 'disabled' : '') + '>' +
              '<span>' + esc(d.day) + '</span>' +
              '<span class="text-slate-400 font-khmer text-[11px]">(' + esc(d.khmer) + ')</span>' +
            '</label>' +
          '</td>' +
          '<td>' +
            (d.open ? '<span class="si-badge si-badge-green">Open</span>' : '<span class="si-badge si-badge-gray">Closed</span>') +
          '</td>' +
          '<td>' +
            '<input type="time" name="open_time_' + idx + '" class="si-input py-1 px-2 text-xs w-28" value="' + (d.openTime !== '—' ? esc(d.openTime) : '07:00') + '" ' + (!d.open || !canEdit ? 'disabled' : '') + '>' +
          '</td>' +
          '<td>' +
            '<input type="time" name="close_time_' + idx + '" class="si-input py-1 px-2 text-xs w-28" value="' + (d.closeTime !== '—' ? esc(d.closeTime) : '17:00') + '" ' + (!d.open || !canEdit ? 'disabled' : '') + '>' +
          '</td>' +
          '<td class="text-slate-400 text-[11px]">' +
            (d.day === 'Saturday' ? 'Secondary Lab Electives' : (d.day === 'Sunday' ? 'Campus Maintenance' : 'Regular Dual-Shift Sessions')) +
          '</td>' +
        '</tr>';
    }).join('');

    return '' +
      '<form id="formSchoolDays" onsubmit="SCHOOL_INFO.saveSchoolDays(event)" class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Weekly Operating Days & Shift Schedule</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Configure operational days of the week, shift bell hours, and weekend elective sessions.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="submit" class="si-btn si-btn-primary"><span class="material-symbols-outlined text-[16px]">save</span><span>Save Schedule</span></button>' :
              '<span class="si-badge si-badge-amber">View Only</span>') +
          '</div>' +
        '</div>' +

        '<div class="si-table-wrap">' +
          '<table class="si-table">' +
            '<thead>' +
              '<tr>' +
                '<th>Day of Week</th>' +
                '<th>Operating Status</th>' +
                '<th>Opening Time</th>' +
                '<th>Closing Time</th>' +
                '<th>Instructional Notes</th>' +
              '</tr>' +
            '</thead>' +
            '<tbody>' +
              rowsHtml +
            '</tbody>' +
          '</table>' +
        '</div>' +

        '<div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-3 border-t border-[#E1E9E3]">' +
          '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">' +
            '<span class="text-xs font-medium text-slate-800">Saturday Elective Sessions Policy</span>' +
            '<p class="text-[11px] text-slate-500 font-normal">When Saturday is enabled, Timetable Builder automatically provides Saturday morning slot scheduling for Robotics and Cambridge electives.</p>' +
            '<label class="inline-flex items-center gap-2 mt-2 cursor-pointer">' +
              '<input type="checkbox" id="chkSatEnabled" class="rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]" ' + (sched.saturdayEnabled ? 'checked' : '') + ' ' + (!canEdit ? 'disabled' : '') + '>' +
              '<span class="text-xs font-medium text-slate-700">Enable Saturday Morning Academic Instruction</span>' +
            '</label>' +
          '</div>' +

          '<div class="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">' +
            '<span class="text-xs font-medium text-slate-800">Shift Timings Summary</span>' +
            '<ul class="text-[11px] text-slate-600 space-y-1 font-normal">' +
              '<li>• Morning Shift: 07:00 – 11:30 (Periods 1 to 5)</li>' +
              '<li>• Protected Morning Recess: 08:40 – 09:00 (20 min)</li>' +
              '<li>• Mid-day Lunch Break: 11:30 – 13:00 (90 min)</li>' +
              '<li>• Afternoon Shift: 13:00 – 17:10 (Periods 6 to 10)</li>' +
            '</ul>' +
          '</div>' +
        '</div>' +
      '</form>';
  };

  SI.saveSchoolDays = function (e) {
    if (e) e.preventDefault();
    var c = state.config.operating_schedule || {};
    var days = c.weeklyDays || [];
    var satChk = document.getElementById('chkSatEnabled');

    var updatedDays = days.map(function (d, idx) {
      var openInp = document.querySelector('input[name="day_open_' + idx + '"]');
      var openTimeInp = document.querySelector('input[name="open_time_' + idx + '"]');
      var closeTimeInp = document.querySelector('input[name="close_time_' + idx + '"]');

      var isOpen = openInp ? openInp.checked : d.open;
      return {
        day: d.day,
        khmer: d.khmer,
        open: isOpen,
        openTime: isOpen ? (openTimeInp ? openTimeInp.value : d.openTime) : '—',
        closeTime: isOpen ? (closeTimeInp ? closeTimeInp.value : d.closeTime) : '—',
        optional: d.optional
      };
    });

    apiCall('/api/school-config/operating-schedule', 'PUT', {
      weeklyDays: updatedDays,
      saturdayEnabled: satChk ? satChk.checked : true,
      shifts: c.shifts,
      closureDays: c.closureDays
    }).then(function (res) {
      toast('Operating schedule updated and synchronized.');
      state.config.operating_schedule = res.data;
    }).catch(function (err) {
      toast(err.message, 'error');
    });
  };

  // 6. Bell Schedule & Periods Renderer
  SI.renderBellSchedule = function () {
    var c = state.config || {};
    var bell = c.bell_schedule || {};
    var periods = bell.periods || [];
    var canEdit = state.role === 'admin' || (state.permissions.permittedSections && state.permissions.permittedSections.indexOf('bell_schedule') !== -1);

    var rowsHtml = periods.map(function (p, idx) {
      var typeBadge = p.isBreak ? '<span class="si-badge si-badge-amber">Break / Recess</span>' : '<span class="si-badge si-badge-blue">Instructional</span>';
      return '' +
        '<tr>' +
          '<td class="font-medium text-slate-800">' +
            (p.isBreak ? '—' : ('Period ' + p.number)) +
          '</td>' +
          '<td>' +
            '<span class="font-medium text-slate-800">' + esc(p.label) + '</span>' +
          '</td>' +
          '<td>' +
            '<span class="text-xs font-mono">' + esc(p.start) + '</span>' +
          '</td>' +
          '<td>' +
            '<span class="text-xs font-mono">' + esc(p.end) + '</span>' +
          '</td>' +
          '<td>' +
            '<span class="text-xs text-slate-600">' + p.duration + ' min</span>' +
          '</td>' +
          '<td>' +
            typeBadge +
          '</td>' +
        '</tr>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Bell Schedule & Period Times</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Authoritative 10-period dual-shift bell schedule strictly following Cambodian MoEYS standards.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            '<span class="si-badge si-badge-green"><span class="material-symbols-outlined text-[14px]">verified</span><span>MoEYS Validated (50 Min Slots)</span></span>' +
          '</div>' +
        '</div>' +

        '<div class="si-table-wrap">' +
          '<table class="si-table">' +
            '<thead>' +
              '<tr>' +
                '<th>Slot #</th>' +
                '<th>Period Label</th>' +
                '<th>Start Time</th>' +
                '<th>End Time</th>' +
                '<th>Duration</th>' +
                '<th>Classification</th>' +
              '</tr>' +
            '</thead>' +
            '<tbody>' +
              rowsHtml +
            '</tbody>' +
          '</table>' +
        '</div>' +

        '<div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-start gap-2.5">' +
          '<span class="material-symbols-outlined text-[#176B45] text-lg flex-shrink-0 mt-0.5">lock_clock</span>' +
          '<p class="font-normal leading-relaxed">Timetable Integration: This bell schedule feeds directly into the Timetable Builder matrix. Morning periods (1 to 5) and Afternoon periods (6 to 10) are protected against faculty double-booking and room collisions.</p>' +
        '</div>' +
      '</div>';
  };

  // 7. Academic Calendar Events Renderer
  SI.renderCalendar = function () {
    var c = state.config || {};
    var events = c.academic_calendar || [];
    var canEdit = state.role === 'admin' || (state.permissions.permittedSections && state.permissions.permittedSections.indexOf('academic_calendar') !== -1);

    var filtered = events;
    if (state.filterCalendarCat !== 'all') {
      filtered = events.filter(function (e) { return e.category === state.filterCalendarCat; });
    }

    var listHtml = filtered.map(function (e) {
      var catBadge = '';
      if (e.category === 'holiday') catBadge = '<span class="si-badge si-badge-amber">Public Holiday</span>';
      else if (e.category === 'exam') catBadge = '<span class="si-badge si-badge-rose">Examination</span>';
      else if (e.category === 'term_start') catBadge = '<span class="si-badge si-badge-green">Term Milestone</span>';
      else catBadge = '<span class="si-badge si-badge-blue">Professional Dev</span>';

      return '' +
        '<div class="p-3.5 bg-white border border-[#E1E9E3] rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-slate-300 transition">' +
          '<div class="flex items-start gap-3">' +
            '<span class="w-9 h-9 rounded-lg bg-emerald-50 text-[#176B45] flex items-center justify-center material-symbols-outlined text-lg flex-shrink-0 mt-0.5">event</span>' +
            '<div>' +
              '<h4 class="text-xs font-medium text-slate-900">' + esc(e.title) + '</h4>' +
              '<p class="text-[11px] text-slate-500 font-normal mt-0.5">' + esc(e.description) + '</p>' +
              '<div class="flex items-center gap-2 mt-1.5 text-[11px] text-slate-400 font-mono">' +
                '<span>' + esc(e.startDate) + (e.startDate !== e.endDate ? (' to ' + esc(e.endDate)) : '') + '</span>' +
                '<span>•</span>' +
                '<span>' + esc((e.campuses || []).join(', ')) + '</span>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="flex items-center gap-2 flex-shrink-0 self-start sm:self-center">' +
            catBadge +
            (canEdit ? '<button type="button" class="text-rose-600 hover:text-rose-800 p-1 rounded material-symbols-outlined text-[18px]" onclick="SCHOOL_INFO.deleteCalendarEvent(\'' + e.id + '\')" title="Remove event">delete</button>' : '') +
          '</div>' +
        '</div>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Academic Calendar & Institutional Events</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Schedule school holidays, exam blocks, professional development days, and term dates.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="button" class="si-btn si-btn-primary" onclick="SCHOOL_INFO.showAddEventModal()"><span class="material-symbols-outlined text-[16px]">add</span><span>New Event</span></button>' :
              '<span class="si-badge si-badge-amber">View Only</span>') +
          '</div>' +
        '</div>' +

        '<!-- Category Filter Pills -->' +
        '<div class="flex items-center gap-2 flex-wrap text-xs">' +
          '<button type="button" class="px-3 py-1 rounded-full transition ' + (state.filterCalendarCat === 'all' ? 'bg-[#176B45] text-white font-medium' : 'bg-slate-100 text-slate-600 hover:bg-slate-200') + '" onclick="SCHOOL_INFO.filterCalendar(\'all\')">All Events (' + events.length + ')</button>' +
          '<button type="button" class="px-3 py-1 rounded-full transition ' + (state.filterCalendarCat === 'holiday' ? 'bg-[#176B45] text-white font-medium' : 'bg-slate-100 text-slate-600 hover:bg-slate-200') + '" onclick="SCHOOL_INFO.filterCalendar(\'holiday\')">Holidays</button>' +
          '<button type="button" class="px-3 py-1 rounded-full transition ' + (state.filterCalendarCat === 'exam' ? 'bg-[#176B45] text-white font-medium' : 'bg-slate-100 text-slate-600 hover:bg-slate-200') + '" onclick="SCHOOL_INFO.filterCalendar(\'exam\')">Exams</button>' +
          '<button type="button" class="px-3 py-1 rounded-full transition ' + (state.filterCalendarCat === 'term_start' ? 'bg-[#176B45] text-white font-medium' : 'bg-slate-100 text-slate-600 hover:bg-slate-200') + '" onclick="SCHOOL_INFO.filterCalendar(\'term_start\')">Term Milestones</button>' +
          '<button type="button" class="px-3 py-1 rounded-full transition ' + (state.filterCalendarCat === 'pd_day' ? 'bg-[#176B45] text-white font-medium' : 'bg-slate-100 text-slate-600 hover:bg-slate-200') + '" onclick="SCHOOL_INFO.filterCalendar(\'pd_day\')">Faculty PD</button>' +
        '</div>' +

        '<div class="space-y-2.5">' +
          (listHtml || '<div class="p-8 text-center text-slate-400 text-xs">No events found in this category.</div>') +
        '</div>' +
      '</div>';
  };

  SI.filterCalendar = function (cat) {
    state.filterCalendarCat = cat;
    var panel = document.getElementById('siActivePanel');
    if (panel) panel.innerHTML = SI.renderCalendar();
  };

  SI.showAddEventModal = function () {
    var modalHtml = '' +
      '<div class="si-modal-backdrop" id="modalBackdrop">' +
        '<div class="si-modal">' +
          '<div class="si-modal-header">' +
            '<h3 class="text-sm font-medium text-slate-900">Add Academic Calendar Event</h3>' +
            '<button type="button" class="text-slate-400 hover:text-slate-600 material-symbols-outlined text-lg" onclick="SCHOOL_INFO.closeModal()">close</button>' +
          '</div>' +
          '<form onsubmit="SCHOOL_INFO.submitNewEvent(event)" class="si-modal-body space-y-4">' +
            '<div class="si-form-group">' +
              '<label class="si-label">Event Title</label>' +
              '<input type="text" id="newEvtTitle" class="si-input" placeholder="e.g. Mid-Term Examination Block" required>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Event Category</label>' +
              '<select id="newEvtCat" class="si-select">' +
                '<option value="holiday">Public / School Holiday</option>' +
                '<option value="exam">Examination Period</option>' +
                '<option value="term_start">Term Milestone / Orientation</option>' +
                '<option value="pd_day">Faculty Professional Development</option>' +
                '<option value="event">School Activity / Event</option>' +
              '</select>' +
            '</div>' +
            '<div class="grid grid-cols-2 gap-3">' +
              '<div class="si-form-group">' +
                '<label class="si-label">Start Date</label>' +
                '<input type="date" id="newEvtStartDate" class="si-input" value="2026-11-15" required>' +
              '</div>' +
              '<div class="si-form-group">' +
                '<label class="si-label">End Date</label>' +
                '<input type="date" id="newEvtEndDate" class="si-input" value="2026-11-20" required>' +
              '</div>' +
            '</div>' +
            '<div class="si-form-group">' +
              '<label class="si-label">Description & Notes</label>' +
              '<textarea id="newEvtDesc" rows="2" class="si-textarea" placeholder="Details about this calendar date..."></textarea>' +
            '</div>' +
            '<div class="si-modal-footer -mx-5 -mb-5 mt-4">' +
              '<button type="button" class="si-btn si-btn-outline" onclick="SCHOOL_INFO.closeModal()">Cancel</button>' +
              '<button type="submit" class="si-btn si-btn-primary">Add Event</button>' +
            '</div>' +
          '</form>' +
        '</div>' +
      '</div>';

    var wrap = document.createElement('div');
    wrap.id = 'siModalContainer';
    wrap.innerHTML = modalHtml;
    document.body.appendChild(wrap);
  };

  SI.submitNewEvent = function (e) {
    e.preventDefault();
    var title = document.getElementById('newEvtTitle').value.trim();
    var cat = document.getElementById('newEvtCat').value;
    var sDate = document.getElementById('newEvtStartDate').value;
    var eDate = document.getElementById('newEvtEndDate').value;
    var desc = document.getElementById('newEvtDesc').value.trim();

    apiCall('/api/school-config/calendar', 'POST', {
      title: title,
      category: cat,
      startDate: sDate,
      endDate: eDate,
      description: desc,
      campuses: ["All Campuses"],
      status: "scheduled"
    }).then(function (res) {
      toast('Event ' + title + ' scheduled.');
      SI.closeModal();
      SI.loadData('schoolInfoRoot');
    }).catch(function (err) {
      toast(err.message, 'error');
    });
  };

  SI.deleteCalendarEvent = function (evtId) {
    if (!confirm('Are you sure you want to remove this event from the academic calendar?')) return;
    apiCall('/api/school-config/calendar/' + evtId, 'DELETE')
      .then(function (res) {
        toast('Calendar event removed.');
        SI.loadData('schoolInfoRoot');
      })
      .catch(function (err) {
        toast(err.message, 'error');
      });
  };

  // 8. Departments & Grade Levels Renderer
  SI.renderDepartments = function () {
    var departments = [
      { code: 'dept-mat', name: 'Mathematics Department', head: 'Dr. Sarah Jenkins', faculty: 8, subjects: 6 },
      { code: 'dept-sci', name: 'Science Department', head: 'Dr. Pov Sophea', faculty: 10, subjects: 8 },
      { code: 'dept-eng', name: 'English Department', head: 'Ms. Rin Lina', faculty: 9, subjects: 5 },
      { code: 'dept-khm', name: 'Khmer Studies Department', head: 'Mr. Chhem Sokha', faculty: 7, subjects: 4 },
      { code: 'dept-chn', name: 'Chinese Language Department', head: 'Ms. Li Wei', faculty: 4, subjects: 3 },
      { code: 'dept-hum', name: 'Humanities & Social Sciences', head: 'Mr. John Vance', faculty: 6, subjects: 5 },
      { code: 'dept-art', name: 'Arts & Physical Education', head: 'Coach Samreth Bora', faculty: 5, subjects: 4 },
      { code: 'dept-ict', name: 'ICT & Computer Science', head: 'Muthukumaran Pakkirisamy', faculty: 5, subjects: 4 }
    ];

    var grades = [
      { code: 'G7', name: 'Grade 7 (Lower Secondary)', minCredits: 28, cohorts: '7A, 7B, 7C' },
      { code: 'G8', name: 'Grade 8 (Lower Secondary)', minCredits: 28, cohorts: '8A, 8B, 8C' },
      { code: 'G9', name: 'Grade 9 (MoEYS Diploma Prep)', minCredits: 30, cohorts: '9A, 9B, 9C' },
      { code: 'G10', name: 'Grade 10 (Senior High I)', minCredits: 32, cohorts: '10A, 10B, 10C' },
      { code: 'G11', name: 'Grade 11 (Senior High II / IGCSE)', minCredits: 34, cohorts: '11A, 11B' },
      { code: 'G12', name: 'Grade 12 (National Baccalaureate)', minCredits: 36, cohorts: '12A, 12B' }
    ];

    var deptRows = departments.map(function (d) {
      return '' +
        '<tr>' +
          '<td class="font-medium text-slate-800">' + esc(d.name) + '</td>' +
          '<td class="font-mono text-xs text-slate-500">' + esc(d.code) + '</td>' +
          '<td class="text-slate-700">' + esc(d.head) + '</td>' +
          '<td class="text-slate-600">' + d.faculty + ' Teachers</td>' +
          '<td class="text-slate-600">' + d.subjects + ' Curriculum Courses</td>' +
        '</tr>';
    }).join('');

    var gradeRows = grades.map(function (g) {
      return '' +
        '<tr>' +
          '<td class="font-medium text-slate-800 font-mono">' + esc(g.code) + '</td>' +
          '<td class="text-slate-800">' + esc(g.name) + '</td>' +
          '<td class="text-slate-600 font-mono text-xs">' + esc(g.cohorts) + '</td>' +
          '<td class="text-slate-600">' + g.minCredits + ' Weekly Periods</td>' +
        '</tr>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Academic Structure: Departments & Grade Levels</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Unified organizational mapping between academic divisions, subject curricula, and student cohorts.</p>' +
          '</div>' +
        '</div>' +

        '<div class="space-y-4">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Faculty Departments</h3>' +
          '<div class="si-table-wrap">' +
            '<table class="si-table">' +
              '<thead>' +
                '<tr>' +
                  '<th>Department Name</th>' +
                  '<th>Code</th>' +
                  '<th>Department Head</th>' +
                  '<th>Faculty Count</th>' +
                  '<th>Subjects</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody>' +
                deptRows +
              '</tbody>' +
            '</table>' +
          '</div>' +
        '</div>' +

        '<div class="space-y-4 pt-3 border-t border-[#E1E9E3]">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Secondary Grade Levels & Cohorts</h3>' +
          '<div class="si-table-wrap">' +
            '<table class="si-table">' +
              '<thead>' +
                '<tr>' +
                  '<th>Code</th>' +
                  '<th>Grade Level</th>' +
                  '<th>Current Cohorts</th>' +
                  '<th>Weekly Instructional Period Requirement</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody>' +
                gradeRows +
              '</tbody>' +
            '</table>' +
          '</div>' +
        '</div>' +
      '</div>';
  };

  // 9. Timetable Rules Renderer
  SI.renderTimetableRules = function () {
    var c = state.config || {};
    var r = c.timetable_rules || {};
    var canEdit = state.role === 'admin' || state.role === 'principal';

    return '' +
      '<form id="formTimetableRules" onsubmit="SCHOOL_INFO.saveTimetableRules(event)" class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Timetable Generation & Scheduling Constraints</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Authoritative rules enforced by the Timetable Builder algorithm and Khmer Suite Engine.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="submit" class="si-btn si-btn-primary"><span class="material-symbols-outlined text-[16px]">save</span><span>Save Rules</span></button>' :
              '<span class="si-badge si-badge-amber">View Only</span>') +
          '</div>' +
        '</div>' +

        '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">' +
          '<div class="si-form-group">' +
            '<label class="si-label">Target Weekly Periods Per Cohort</label>' +
            '<input type="number" name="weeklyPeriodsTarget" class="si-input" value="' + esc(r.weeklyPeriodsTarget || 34) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '<span class="text-[11px] text-slate-400">MoEYS National standard: 34 to 40 periods weekly.</span>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Maximum Periods Per Day Per Student Cohort</label>' +
            '<input type="number" name="maxPeriodsPerDay" class="si-input" value="' + esc(r.maxPeriodsPerDay || 7) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Max Consecutive Hours Per Faculty (MoEYS Rule)</label>' +
            '<input type="number" name="maxConsecutiveHoursFaculty" class="si-input" value="' + esc(r.maxConsecutiveHoursFaculty || 2) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
            '<span class="text-[11px] text-slate-400">Prevents teacher fatigue; enforces break intervals.</span>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Max Consecutive Hours Per Subject</label>' +
            '<input type="number" name="maxConsecutiveHoursSubject" class="si-input" value="' + esc(r.maxConsecutiveHoursSubject || 2) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
        '</div>' +

        '<div class="pt-3 border-t border-[#E1E9E3] space-y-3">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Automated Conflict Prevention Constraints</h3>' +
          
          '<label class="flex items-center gap-3 p-3 bg-white border border-[#E1E9E3] rounded-xl cursor-pointer hover:border-slate-300 transition">' +
            '<input type="checkbox" name="protectMorningRecess" class="rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]" ' + (r.protectMorningRecess ? 'checked' : '') + ' ' + (!canEdit ? 'disabled' : '') + '>' +
            '<div>' +
              '<span class="text-xs font-medium text-slate-900 block">Strict Morning Recess Protection (08:40 – 09:00)</span>' +
              '<span class="text-[11px] text-slate-500 font-normal">Blocks any lessons from being scheduled during official national morning recess.</span>' +
            '</div>' +
          '</label>' +

          '<label class="flex items-center gap-3 p-3 bg-white border border-[#E1E9E3] rounded-xl cursor-pointer hover:border-slate-300 transition">' +
            '<input type="checkbox" name="strictFacultyDoubleBooking" class="rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]" ' + (r.strictFacultyDoubleBooking ? 'checked' : '') + ' ' + (!canEdit ? 'disabled' : '') + '>' +
            '<div>' +
              '<span class="text-xs font-medium text-slate-900 block">Zero Faculty Double-Booking Allowance</span>' +
              '<span class="text-[11px] text-slate-500 font-normal">Algorithm rejects slot placement if the faculty member is teaching another cohort at the same time.</span>' +
            '</div>' +
          '</label>' +

          '<label class="flex items-center gap-3 p-3 bg-white border border-[#E1E9E3] rounded-xl cursor-pointer hover:border-slate-300 transition">' +
            '<input type="checkbox" name="strictRoomDoubleBooking" class="rounded border-slate-300 text-[#176B45] focus:ring-[#176B45]" ' + (r.strictRoomDoubleBooking ? 'checked' : '') + ' ' + (!canEdit ? 'disabled' : '') + '>' +
            '<div>' +
              '<span class="text-xs font-medium text-slate-900 block">Zero Classroom / Laboratory Collision Allowance</span>' +
              '<span class="text-[11px] text-slate-500 font-normal">Prevents two cohorts from being assigned to the same physical room simultaneously.</span>' +
            '</div>' +
          '</label>' +
        '</div>' +
      '</form>';
  };

  SI.saveTimetableRules = function (e) {
    if (e) e.preventDefault();
    var form = document.getElementById('formTimetableRules');
    if (!form) return;
    var fd = new FormData(form);
    var payload = {
      weeklyPeriodsTarget: parseInt(fd.get('weeklyPeriodsTarget') || 34, 10),
      maxPeriodsPerDay: parseInt(fd.get('maxPeriodsPerDay') || 7, 10),
      maxConsecutiveHoursFaculty: parseInt(fd.get('maxConsecutiveHoursFaculty') || 2, 10),
      maxConsecutiveHoursSubject: parseInt(fd.get('maxConsecutiveHoursSubject') || 2, 10),
      protectMorningRecess: !!fd.get('protectMorningRecess'),
      strictFacultyDoubleBooking: !!fd.get('strictFacultyDoubleBooking'),
      strictRoomDoubleBooking: !!fd.get('strictRoomDoubleBooking'),
      activeAcademicYear: state.config.timetable_rules.activeAcademicYear || '2026–2027'
    };

    apiCall('/api/school-config/timetable-rules', 'PUT', payload)
      .then(function (res) {
        toast('Timetable generation rules saved.');
        state.config.timetable_rules = res.data;
      })
      .catch(function (err) {
        toast(err.message, 'error');
      });
  };

  // 10. Staff & Academic Policies Renderer
  SI.renderStaffPolicies = function () {
    var c = state.config || {};
    var p = c.staff_policies || {};
    var canEdit = state.role === 'admin' || state.role === 'principal';

    return '' +
      '<form id="formStaffPolicies" onsubmit="SCHOOL_INFO.saveStaffPolicies(event)" class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Staff Workload & Academic Operational Policies</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Faculty workload thresholds, attendance cutoff times, and grade publication requirements.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            (canEdit ? 
              '<button type="submit" class="si-btn si-btn-primary"><span class="material-symbols-outlined text-[16px]">save</span><span>Save Policies</span></button>' :
              '<span class="si-badge si-badge-amber">View Only</span>') +
          '</div>' +
        '</div>' +

        '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">' +
          '<div class="si-form-group">' +
            '<label class="si-label">Maximum Daily Teaching Periods Per Teacher</label>' +
            '<input type="number" name="maxDailyTeachingPeriods" class="si-input" value="' + esc(p.maxDailyTeachingPeriods || 6) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Maximum Weekly Teaching Periods Target</label>' +
            '<input type="number" name="maxWeeklyTeachingPeriods" class="si-input" value="' + esc(p.maxWeeklyTeachingPeriods || 24) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Morning Attendance Cutoff Time</label>' +
            '<input type="time" name="attendanceCutoffMorning" class="si-input" value="' + esc(p.attendanceCutoffMorning || '07:15') + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Afternoon Attendance Cutoff Time</label>' +
            '<input type="time" name="attendanceCutoffAfternoon" class="si-input" value="' + esc(p.attendanceCutoffAfternoon || '13:15') + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Late Arrival Grace Period (Minutes)</label>' +
            '<input type="number" name="lateArrivalGracePeriodMinutes" class="si-input" value="' + esc(p.lateArrivalGracePeriodMinutes || 10) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
          '<div class="si-form-group">' +
            '<label class="si-label">Exam Grade Submission Deadline (Days After Exam)</label>' +
            '<input type="number" name="gradeSubmissionDeadlineDaysAfterExam" class="si-input" value="' + esc(p.gradeSubmissionDeadlineDaysAfterExam || 5) + '" ' + (!canEdit ? 'disabled' : '') + ' required>' +
          '</div>' +
        '</div>' +
      '</form>';
  };

  SI.saveStaffPolicies = function (e) {
    if (e) e.preventDefault();
    var form = document.getElementById('formStaffPolicies');
    if (!form) return;
    var fd = new FormData(form);
    var payload = {
      maxDailyTeachingPeriods: parseInt(fd.get('maxDailyTeachingPeriods') || 6, 10),
      maxWeeklyTeachingPeriods: parseInt(fd.get('maxWeeklyTeachingPeriods') || 24, 10),
      attendanceCutoffMorning: fd.get('attendanceCutoffMorning') || '07:15',
      attendanceCutoffAfternoon: fd.get('attendanceCutoffAfternoon') || '13:15',
      lateArrivalGracePeriodMinutes: parseInt(fd.get('lateArrivalGracePeriodMinutes') || 10, 10),
      gradeSubmissionDeadlineDaysAfterExam: parseInt(fd.get('gradeSubmissionDeadlineDaysAfterExam') || 5, 10),
      excusedAbsenceCategories: ["Medical Certificate", "Official School Duty", "Family Bereavement", "Approved MoEYS Representation"]
    };

    apiCall('/api/school-config/staff-policies', 'PUT', payload)
      .then(function (res) {
        toast('Staff & academic policies updated.');
        state.config.staff_policies = res.data;
      })
      .catch(function (err) {
        toast(err.message, 'error');
      });
  };

  // 11. Permissions & Access Control Renderer
  SI.renderPermissions = function () {
    var c = state.config || {};
    var pm = c.permissions_matrix || {};
    var editors = pm.assignedEditors || [];

    var editorRows = editors.map(function (ed) {
      return '' +
        '<tr>' +
          '<td class="font-medium text-slate-800">' + esc(ed.name) + '</td>' +
          '<td class="text-xs text-slate-500 font-mono">' + esc(ed.id) + '</td>' +
          '<td class="text-slate-600">' + esc(ed.assignedCampus) + '</td>' +
          '<td>' +
            '<div class="flex items-center gap-1 flex-wrap">' +
              (ed.permittedSections || []).map(function (sec) { return '<span class="px-2 py-0.5 rounded bg-emerald-50 border border-emerald-200 text-emerald-800 text-[10px] font-medium">' + esc(sec) + '</span>'; }).join('') +
            '</div>' +
          '</td>' +
          '<td><span class="si-badge si-badge-green">' + esc(ed.status.toUpperCase()) + '</span></td>' +
        '</tr>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Role-Based Access Control & Editor Permissions</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Configure granular section edit permissions and facility scopes for administrators, principals, and editors.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            '<span class="si-badge si-badge-green">Backend Enforced</span>' +
          '</div>' +
        '</div>' +

        '<!-- Permission Matrix Table -->' +
        '<div class="space-y-3">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Access Capability Matrix</h3>' +
          '<div class="si-table-wrap">' +
            '<table class="si-table">' +
              '<thead>' +
                '<tr>' +
                  '<th>System Module / Section</th>' +
                  '<th>Super Administrator</th>' +
                  '<th>Executive Principal</th>' +
                  '<th>Authorized Editor</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody>' +
                '<tr><td>School Profile & Contacts</td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Permitted (If Assigned)</span></td></tr>' +
                '<tr><td>Academic Years Activation</td><td><span class="text-emerald-700 font-medium">Immediate Activation</span></td><td><span class="text-emerald-700 font-medium">Immediate Activation</span></td><td><span class="text-amber-700 font-medium">Requires Admin Approval</span></td></tr>' +
                '<tr><td>Campuses Management</td><td><span class="text-emerald-700 font-medium">All Campuses</span></td><td><span class="text-slate-700 font-medium">Assigned Campuses Only</span></td><td><span class="text-slate-400">Read Only</span></td></tr>' +
                '<tr><td>Operating Schedule & Days</td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Permitted (If Assigned)</span></td></tr>' +
                '<tr><td>Bell Schedule & Periods</td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Permitted (If Assigned)</span></td></tr>' +
                '<tr><td>Academic Calendar</td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Permitted (If Assigned)</span></td></tr>' +
                '<tr><td>Timetable Rules</td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-emerald-700 font-medium">Full Edit</span></td><td><span class="text-slate-400">Read Only</span></td></tr>' +
                '<tr><td>Permissions & Security</td><td><span class="text-emerald-700 font-medium">Full Control</span></td><td><span class="text-slate-400">No Access</span></td><td><span class="text-slate-400">No Access</span></td></tr>' +
                '<tr><td>Audit Trail Rollback</td><td><span class="text-emerald-700 font-medium">Authorized</span></td><td><span class="text-slate-400">View Only</span></td><td><span class="text-slate-400">View Only</span></td></tr>' +
              '</tbody>' +
            '</table>' +
          '</div>' +
        '</div>' +

        '<!-- Assigned Editors -->' +
        '<div class="space-y-3 pt-3 border-t border-[#E1E9E3]">' +
          '<h3 class="text-xs font-medium text-slate-400 uppercase tracking-wider">Assigned Editor Accounts</h3>' +
          '<div class="si-table-wrap">' +
            '<table class="si-table">' +
              '<thead>' +
                '<tr>' +
                  '<th>Staff Name</th>' +
                  '<th>User ID</th>' +
                  '<th>Campus Scope</th>' +
                  '<th>Permitted Sections</th>' +
                  '<th>Status</th>' +
                '</tr>' +
              '</thead>' +
              '<tbody>' +
                editorRows +
              '</tbody>' +
            '</table>' +
          '</div>' +
        '</div>' +
      '</div>';
  };

  // 12. Change History & Audit Log Renderer
  SI.renderChangeHistory = function () {
    var c = state.config || {};
    var logs = c.audit_log || [];

    // Filter
    if (state.auditFilterSection !== 'all') {
      logs = logs.filter(function (l) { return (l.section || '').toLowerCase() === state.auditFilterSection.toLowerCase(); });
    }
    if (state.auditQuery) {
      var q = state.auditQuery.toLowerCase();
      logs = logs.filter(function (l) {
        return (l.action && l.action.toLowerCase().indexOf(q) !== -1) ||
               (l.notes && l.notes.toLowerCase().indexOf(q) !== -1) ||
               (l.userName && l.userName.toLowerCase().indexOf(q) !== -1);
      });
    }

    var rowsHtml = logs.map(function (l) {
      return '' +
        '<tr>' +
          '<td class="font-mono text-xs text-slate-500 whitespace-nowrap">' + esc(l.timestamp) + '</td>' +
          '<td class="font-medium text-slate-900 whitespace-nowrap">' + esc(l.userName) + ' <span class="text-[10px] text-slate-400 font-mono">(' + esc(l.userRole) + ')</span></td>' +
          '<td><span class="si-badge si-badge-blue">' + esc(l.section) + '</span></td>' +
          '<td class="font-mono text-xs text-slate-700">' + esc(l.action) + '</td>' +
          '<td class="text-xs text-slate-600 max-w-xs truncate" title="' + esc(l.notes) + '">' + esc(l.notes) + '</td>' +
          '<td><span class="si-badge si-badge-green">' + esc(l.status.toUpperCase()) + '</span></td>' +
        '</tr>';
    }).join('');

    return '' +
      '<div class="space-y-6">' +
        '<div class="si-panel-header">' +
          '<div>' +
            '<h2 class="text-lg font-medium text-slate-900">Change History & Audit Trail</h2>' +
            '<p class="text-xs text-slate-500 mt-0.5">Immutable audit log recording configuration updates, administrator approvals, and timestamped revisions.</p>' +
          '</div>' +
          '<div class="flex items-center gap-2">' +
            '<span class="si-badge si-badge-green">Total Events: ' + logs.length + '</span>' +
          '</div>' +
        '</div>' +

        '<div class="flex items-center gap-3 flex-wrap">' +
          '<div class="flex-1 min-w-[200px]">' +
            '<input type="search" id="inpAuditSearch" class="si-input" placeholder="Search audit events by user, action, or note..." value="' + esc(state.auditQuery) + '" oninput="SCHOOL_INFO.searchAudit(this.value)">' +
          '</div>' +
          '<div>' +
            '<select class="si-select text-xs" onchange="SCHOOL_INFO.filterAuditSection(this.value)">' +
              '<option value="all">All Sections</option>' +
              '<option value="Academic Years">Academic Years</option>' +
              '<option value="School Profile">School Profile</option>' +
              '<option value="Campuses">Campuses</option>' +
              '<option value="Operating Schedule">Operating Schedule</option>' +
              '<option value="Bell Schedule">Bell Schedule</option>' +
              '<option value="Timetable Rules">Timetable Rules</option>' +
            '</select>' +
          '</div>' +
        '</div>' +

        '<div class="si-table-wrap">' +
          '<table class="si-table">' +
            '<thead>' +
              '<tr>' +
                '<th>Date & Time</th>' +
                '<th>Author</th>' +
                '<th>Module Section</th>' +
                '<th>Operation</th>' +
                '<th>Change Description</th>' +
                '<th>Status</th>' +
              '</tr>' +
            '</thead>' +
            '<tbody>' +
              (rowsHtml || '<tr><td colspan="6" class="text-center py-8 text-slate-400 text-xs">No audit logs matching query.</td></tr>') +
            '</tbody>' +
          '</table>' +
        '</div>' +
      '</div>';
  };

  SI.searchAudit = function (val) {
    state.auditQuery = val;
    var panel = document.getElementById('siActivePanel');
    if (panel) panel.innerHTML = SI.renderChangeHistory();
  };

  SI.filterAuditSection = function (sec) {
    state.auditFilterSection = sec;
    var panel = document.getElementById('siActivePanel');
    if (panel) panel.innerHTML = SI.renderChangeHistory();
  };

})(window, document);

