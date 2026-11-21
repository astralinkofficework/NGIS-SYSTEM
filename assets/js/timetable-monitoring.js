/**
 * NGIS — Admin Timetable Monitoring (read-only oversight)
 * --------------------------------------------------------
 * Renders the Timetable Monitoring workspace:
 *   4 summary metrics → filterable/sortable/paginated class status table
 *   → read-only class detail (draft & published previews) → reminders.
 *
 * This module NEVER edits the timetable: no drag/drop, no publish, no grid
 * mutations are sent from here. Editing stays with the Principal builder.
 */
(function () {
  'use strict';

  var API = '/api/timetable';
  var state = {
    filters: { campus: '', department: '', grade: '', status: '', search: '', sort: 'attention' },
    page: 1, pageSize: 10,
    data: null, meta: null, summary: null,
    remindCtx: null, detail: null, previewMode: 'draft'
  };

  /* ── actor headers (authenticated user identity for backend guards) ── */
  function actorHeaders() {
    var user = null;
    try { user = window.NGISAuth && window.NGISAuth.getUser ? window.NGISAuth.getUser() : null; } catch (e) { /* noop */ }
    var name = 'Admin';
    var email = '', role = 'admin', id = '';
    if (user) {
      name = ((user.firstName || '') + ' ' + (user.lastName || '')).trim() || user.name || user.email || 'Admin';
      email = user.email || '';
      role = (user.role || 'admin').toLowerCase();
      id = user.id || user.userId || user.username || '';
    } else if (window.PAGE && window.PAGE.role) {
      role = String(window.PAGE.role).toLowerCase();
    }
    var h = { 'X-Actor': name, 'X-Actor-Role': role };
    if (email) h['X-Actor-Email'] = email;
    if (id) h['X-Actor-Id'] = id;
    return h;
  }

  function fetchJSON(url, opts) {
    opts = opts || {};
    opts.headers = Object.assign({ 'Content-Type': 'application/json' }, actorHeaders(), opts.headers || {});
    return fetch(url, opts).then(function (res) {
      return res.json().then(function (body) { return { status: res.status, body: body }; });
    });
  }

  /* ── status badge ── */
  var BADGES = {
    published:        { cls: 'text-emerald-700 bg-emerald-50 border-emerald-200', dot: 'bg-emerald-600', label: 'Published' },
    update_in_draft:  { cls: 'text-teal-700 bg-teal-50 border-teal-200', dot: 'bg-teal-600', label: 'Update in Draft' },
    ready_to_publish: { cls: 'text-lime-700 bg-lime-50 border-lime-200', dot: 'bg-lime-600', label: 'Ready to Publish' },
    in_progress:      { cls: 'text-amber-700 bg-amber-50 border-amber-200', dot: 'bg-amber-500', label: 'In Progress' },
    not_started:      { cls: 'text-slate-600 bg-slate-50 border-slate-200', dot: 'bg-slate-400', label: 'Not Started' },
    needs_attention:  { cls: 'text-rose-700 bg-rose-50 border-rose-200', dot: 'bg-rose-600', label: 'Needs Attention' }
  };
  function badge(status, label) {
    var b = BADGES[status] || BADGES.not_started;
    var displayLabel = label || b.label || status;
    return '<span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium border ' + b.cls + '">' +
      '<span class="w-1.5 h-1.5 rounded-full ' + b.dot + '"></span>' + esc(displayLabel) + '</span>';
  }

  function esc(v) {
    return String(v == null || v === '' ? '—' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function fmtDate(iso) {
    if (!iso) return '—';
    var d = new Date(String(iso).replace(' ', 'T'));
    if (isNaN(d.getTime())) return esc(iso);
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) +
      ' ' + d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
  }

  /* ═══ KPIs ═══ */
  function renderSummary() {
    var s = state.summary || {};
    var set = function (id, v) { var el = document.getElementById(id); if (el) el.textContent = v; };
    set('monKpiTotal', s.total_classes || 0);
    set('monKpiPublished', s.published || 0);
    set('monKpiDraft', s.draft_in_progress || 0);
    set('monKpiNotStarted', s.not_started || 0);
    var sub = document.getElementById('monKpiDraftSub');
    if (sub && s.breakdown) {
      var parts = [];
      if (s.breakdown.in_progress) parts.push(s.breakdown.in_progress + ' in progress');
      if (s.breakdown.ready_to_publish) parts.push(s.breakdown.ready_to_publish + ' ready to publish');
      if (s.breakdown.needs_attention) parts.push(s.breakdown.needs_attention + ' need attention');
      if (s.breakdown.update_in_draft) parts.push(s.breakdown.update_in_draft + ' pending updates');
      sub.textContent = parts.length ? parts.join(' · ') : 'No active drafts in review';
    }
    var pubSub = document.getElementById('monKpiPublishedSub');
    if (pubSub && s.breakdown) {
      pubSub.textContent = s.breakdown.update_in_draft
        ? s.breakdown.update_in_draft + ' with pending draft update'
        : 'Live on teacher & student portals';
    }
  }

  /* ═══ Filters ═══ */
  function fillSelect(id, values, labelFn) {
    var el = document.getElementById(id);
    if (!el) return;
    var current = el.value;
    var options = '<option value="">' + (el.getAttribute('data-placeholder') || 'All') + '</option>';
    values.forEach(function (v) {
      var val = typeof v === 'object' ? v.value : v;
      var lab = typeof v === 'object' ? v.label : (labelFn ? labelFn(v) : v);
      options += '<option value="' + esc(val) + '">' + esc(lab) + '</option>';
    });
    el.innerHTML = options;
    if (current) el.value = current;
  }

  function renderFilters() {
    var m = state.meta || {};
    fillSelect('monFilterCampus', m.campuses || []);
    fillSelect('monFilterDept', m.departments || []);
    fillSelect('monFilterGrade', m.grades || []);
    fillSelect('monFilterStatus', m.statuses || []);
    fillSelect('monFilterSort', m.sorts || []);
    var ay = document.getElementById('monFilterYear');
    if (ay && m.academic_year) {
      ay.innerHTML = '<option value="">' + esc(m.academic_year) + '</option>';
      ay.value = '';
    }
  }

  /* ═══ Table ═══ */
  function completionCell(r) {
    if (!r.completion_available) return '<span class="text-slate-400 text-[11px]">Not available</span>';
    var pct = Math.round(r.completion_pct || 0);
    var color = pct >= 100 ? 'bg-emerald-600' : pct > 0 ? 'bg-amber-500' : 'bg-slate-300';
    return '<div class="flex items-center gap-2 min-w-[90px]">' +
      '<div class="w-16 sm:w-20 bg-slate-100 rounded-full h-1.5 overflow-hidden">' +
      '<div class="h-full rounded-full ' + color + '" style="width:' + Math.min(pct, 100) + '%"></div></div>' +
      '<span class="text-[11px] text-slate-500 tabular-nums font-medium">' + pct + '%</span></div>';
  }

  function renderTable() {
    var tbody = document.getElementById('monTableBody');
    var d = state.data;
    if (!tbody) return;
    if (!d || !d.rows || !d.rows.length) {
      tbody.innerHTML = '<tr><td colspan="12" class="px-4 py-12 text-center text-xs text-slate-400">' +
        '<span class="material-symbols-outlined text-3xl block mb-2 text-slate-300">search_off</span>' +
        'No classes match the current filter selection.</td></tr>';
      renderPagination();
      return;
    }
    tbody.innerHTML = d.rows.map(function (r) {
      var resp = r.responsible || {};
      var pubBits = [];
      if (r.published) pubBits.push('v' + r.published_version);
      if (r.update_in_draft) pubBits.push('<span class="text-teal-700">update in draft</span>');
      var gradeDisplay = r.grade && r.section ? 'Grade ' + r.grade + ' - ' + r.section : (r.class_display || '');
      return '<tr class="hover:bg-slate-50/80 transition group border-b border-slate-100">' +
        '<td class="py-3 pl-4 sm:pl-6 pr-4 sticky-col-first bg-white group-hover:bg-slate-50/80 transition border-r sm:border-r-0 border-slate-100">' +
          '<div class="flex items-center gap-2.5">' +
            '<div class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium flex items-center justify-center text-xs shrink-0">' +
              esc(r.class_display) +
            '</div>' +
            '<div>' +
              '<span class="font-medium text-slate-900 block leading-tight text-xs">' + esc(gradeDisplay) + '</span>' +
              '<span class="text-[11px] text-slate-400 font-khmer block">' + esc(r.room) + ' · ' + (r.student_count || 0) + ' students</span>' +
            '</div>' +
          '</div>' +
        '</td>' +
        '<td class="px-4 py-3"><span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700">' + esc(r.campus) + '</span></td>' +
        '<td class="px-4 py-3 font-medium text-slate-800 text-xs">' + esc(r.department) + '</td>' +
        '<td class="px-4 py-3"><div><span class="font-medium text-slate-900 block text-xs">' + esc(resp.name || 'Unassigned') + '</span><span class="text-[11px] text-emerald-800 font-medium">' + esc(resp.role || 'Teacher') + '</span></div></td>' +
        '<td class="px-4 py-3">' + completionCell(r) + '</td>' +
        '<td class="px-4 py-3 text-xs">' + (r.draft_exists
          ? '<span class="inline-flex items-center gap-1 text-slate-600 font-medium text-[11px]"><span class="material-symbols-outlined text-[14px] text-slate-400">edit_note</span>Saved</span>'
          : '<span class="text-slate-400 text-[11px]">None</span>') + '</td>' +
        '<td class="px-4 py-3">' + badge(r.status, r.status_label) +
        (pubBits.length ? '<div class="text-[10px] text-slate-400 mt-0.5">' + pubBits.join(' · ') + '</div>' : '') + '</td>' +
        '<td class="px-4 py-3 text-xs text-slate-600 hidden xl:table-cell">' + esc(r.last_edited_by || 'Unrecorded') + '</td>' +
        '<td class="px-4 py-3 text-[11px] text-slate-500 hidden xl:table-cell">' + fmtDate(r.last_edited_at) + '</td>' +
        '<td class="px-4 py-3 text-xs text-slate-600 hidden lg:table-cell">' + esc(r.published_by) + '</td>' +
        '<td class="px-4 py-3 text-[11px] text-slate-500 hidden lg:table-cell">' + fmtDate(r.published_at) + '</td>' +
        '<td class="pr-4 sm:pr-6 pl-4 py-3 text-right"><div class="inline-flex items-center justify-end gap-1">' +
          '<button type="button" data-act="view" data-class="' + esc(r.class_id) + '" title="View Schedule" class="p-1.5 rounded-lg text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 transition border border-transparent hover:border-emerald-200 active:scale-95">' +
            '<span class="material-symbols-outlined text-[16px]">visibility</span></button>' +
          '<button type="button" data-act="remind" data-class="' + esc(r.class_id) + '" title="Send Reminder" class="p-1.5 rounded-lg text-slate-500 hover:text-amber-700 hover:bg-amber-50 transition border border-transparent hover:border-amber-200 active:scale-95">' +
            '<span class="material-symbols-outlined text-[16px]">notifications_active</span></button>' +
        '</div></td></tr>';
    }).join('');
    renderPagination();
  }

  function renderPagination() {
    var d = state.data; var p = (d && d.pagination) || {};
    var wrap = document.getElementById('monPagination');
    if (!wrap) return;
    var info = document.getElementById('monPageInfo');
    if (info) info.textContent = 'Showing ' + ((d.rows && d.rows.length) || 0) + ' of ' + (p.total || 0) + ' classes';
    var prev = document.getElementById('monPagePrev'), next = document.getElementById('monPageNext');
    if (prev) prev.disabled = (p.page || 1) <= 1;
    if (next) next.disabled = (p.page || 1) >= (p.total_pages || 1);
    var label = document.getElementById('monPageLabel');
    if (label) label.textContent = 'Page ' + (p.page || 1) + ' / ' + (p.total_pages || 1);
  }

  /* ═══ data loading ═══ */
  function queryString() {
    var f = state.filters;
    var q = { campus: f.campus, department: f.department, grade: f.grade,
              status: f.status, search: f.search, sort: f.sort,
              page: state.page, page_size: state.pageSize };
    return Object.keys(q).filter(function (k) { return q[k] !== '' && q[k] != null; })
      .map(function (k) { return k + '=' + encodeURIComponent(q[k]); }).join('&');
  }

  function load() {
    var empty = document.getElementById('monTableBody');
    if (empty) {
      empty.innerHTML = (function() {
        if (window.NGIS_SKELETON) {
          var out = '';
          for (var k = 0; k < 6; k++) {
            out += '<tr><td colspan="12" class="p-3">' +
              '<div class="flex items-center gap-3">' +
                window.NGIS_SKELETON.text({ width: "25%", size: "sm" }) +
                window.NGIS_SKELETON.text({ width: "35%", size: "sm" }) +
                window.NGIS_SKELETON.badge({ width: "65px" }) +
              '</div></td></tr>';
          }
          return out;
        }
        return '<tr><td colspan="12" class="px-4 py-8 text-center text-xs text-slate-400">Loading monitoring data…</td></tr>';
      })();
    }
    return fetchJSON(API + '/monitoring/classes?' + queryString()).then(function (res) {
      if (!res.body || res.body.success === false) throw new Error(res.body && res.body.message || 'load failed');
      state.data = res.body;
      state.summary = res.body.summary;
      state.meta = res.body.meta;
      renderSummary(); renderFilters(); renderTable();
      loadDraftStatus();
    }).catch(function (err) {
      if (empty) empty.innerHTML = '<tr><td colspan="12" class="px-4 py-10 text-center text-xs text-rose-600">Failed to load monitoring data: ' + esc(err.message) + '</td></tr>';
    });
  }

  /* ═══ principal draft review & approval workflow ═══ */
  function loadDraftStatus() {
    return fetchJSON(API + '/draft-status').then(function (res) {
      if (res && res.body && res.body.draft_metadata) {
        state.draftMetadata = res.body.draft_metadata;
        renderDraftReviewBanner();
      }
    }).catch(function (e) {
      console.warn('[Timetable Monitoring] Could not load draft status:', e);
    });
  }

  function renderDraftReviewBanner() {
    var sec = document.getElementById('principalRequestsSection');
    if (!sec) return;
    var meta = state.draftMetadata || { status: 'draft' };

    if (meta.status === 'submitted') {
      sec.className = 'p-4 bg-amber-50/90 border border-amber-300 rounded-2xl flex flex-col lg:flex-row lg:items-center justify-between gap-3 shadow-xs';
      sec.innerHTML =
        '<div class="flex items-start gap-3">' +
          '<div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center shrink-0 mt-0.5">' +
            '<span class="material-symbols-outlined text-xl">assignment_turned_in</span>' +
          '</div>' +
          '<div>' +
            '<div class="text-xs font-medium text-amber-900 flex items-center gap-2 flex-wrap">' +
              '<span>Principal Draft Submitted for Admin Review</span>' +
              '<span class="px-2 py-0.5 rounded-full text-[10px] bg-amber-200 text-amber-900 font-medium">Awaiting Publishing</span>' +
            '</div>' +
            '<p class="text-[11px] text-amber-800 mt-0.5">' +
              esc(meta.submitted_by || 'Dr. Ly Bunheng (Principal)') + ' submitted the weekly timetable draft on ' + (meta.submitted_at ? new Date(meta.submitted_at).toLocaleDateString() : 'recently') + '.' +
              (meta.submission_note ? ' Note: "' + esc(meta.submission_note) + '"' : '') +
            '</p>' +
          '</div>' +
        '</div>' +
        '<div class="flex items-center gap-2 shrink-0 flex-wrap">' +
          '<button type="button" id="btnAdminCompareDraft" class="px-3 py-1.5 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl transition shadow-2xs cursor-pointer flex items-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[15px] text-slate-500">difference</span>' +
            '<span>Compare Changes</span>' +
          '</button>' +
          '<button type="button" id="btnAdminRequestRevision" class="px-3 py-1.5 text-xs font-medium text-rose-700 bg-white hover:bg-rose-50 border border-rose-300 rounded-xl transition shadow-2xs cursor-pointer flex items-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[15px] text-rose-600">feedback</span>' +
            '<span>Request Revision</span>' +
          '</button>' +
          '<button type="button" id="btnAdminApprovePublish" class="px-3.5 py-1.5 text-xs font-medium text-white bg-[#176B45] hover:bg-[#14532D] rounded-xl transition shadow-2xs cursor-pointer flex items-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[15px]">rocket_launch</span>' +
            '<span>Approve &amp; Publish</span>' +
          '</button>' +
        '</div>';

      var btnComp = sec.querySelector('#btnAdminCompareDraft');
      if (btnComp) btnComp.addEventListener('click', openCompareDiffModal);
      var btnRev = sec.querySelector('#btnAdminRequestRevision');
      if (btnRev) btnRev.addEventListener('click', promptRevisionRequest);
      var btnApp = sec.querySelector('#btnAdminApprovePublish');
      if (btnApp) btnApp.addEventListener('click', executeApproveAndPublish);
    } else if (meta.status === 'needs_revision') {
      sec.className = 'p-4 bg-rose-50/80 border border-rose-200 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs';
      sec.innerHTML =
        '<div class="flex items-center gap-3">' +
          '<div class="w-10 h-10 rounded-xl bg-rose-100 text-rose-800 flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-xl">feedback</span>' +
          '</div>' +
          '<div>' +
            '<div class="text-xs font-medium text-rose-900 flex items-center gap-2">' +
              '<span>Revision Requested from Principal</span>' +
              '<span class="px-2 py-0.5 rounded-full text-[10px] bg-rose-200 text-rose-900 font-medium">Pending Update</span>' +
            '</div>' +
            '<p class="text-[11px] text-rose-700 mt-0.5">Awaiting revised draft from ' + esc(meta.submitted_by || 'Principal') + '. Note: "' + esc(meta.revision_note || 'Revisions required.') + '"</p>' +
          '</div>' +
        '</div>';
    } else if (meta.status === 'approved') {
      sec.className = 'p-4 bg-emerald-50/80 border border-emerald-200 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs';
      sec.innerHTML =
        '<div class="flex items-center gap-3">' +
          '<div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-xl">check_circle</span>' +
          '</div>' +
          '<div>' +
            '<div class="text-xs font-medium text-emerald-900 flex items-center gap-2">' +
              '<span>Principal Draft Approved</span>' +
              '<span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-200 text-emerald-900 font-medium">Ready to Publish</span>' +
            '</div>' +
            '<p class="text-[11px] text-emerald-700 mt-0.5">The draft schedule has been approved and is ready to be published to student and teacher portals.</p>' +
          '</div>' +
        '</div>' +
        '<div class="flex items-center gap-2 shrink-0">' +
          '<button type="button" id="btnAdminApprovePublish" class="px-3.5 py-1.5 text-xs font-medium text-white bg-[#176B45] hover:bg-[#14532D] rounded-xl transition shadow-2xs cursor-pointer flex items-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[15px]">rocket_launch</span>' +
            '<span>Publish Timetable</span>' +
          '</button>' +
        '</div>';
      var btnPub = sec.querySelector('#btnAdminApprovePublish');
      if (btnPub) btnPub.addEventListener('click', executeApproveAndPublish);
    } else {
      sec.className = 'p-4 bg-slate-50 border border-slate-200 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs';
      sec.innerHTML =
        '<div class="flex items-center gap-3">' +
          '<div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">' +
            '<span class="material-symbols-outlined text-xl">verified</span>' +
          '</div>' +
          '<div>' +
            '<div class="text-xs font-medium text-slate-900 flex items-center gap-2">' +
              '<span>Master Timetable Overview</span>' +
              '<span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-50 text-emerald-800 border border-emerald-200 font-medium">Active Monitoring</span>' +
            '</div>' +
            '<p class="text-[11px] text-slate-500 mt-0.5">Principal can draft and propose weekly schedules. Administration reviews and publishes official timetables.</p>' +
          '</div>' +
        '</div>' +
        '<div class="flex items-center gap-2 shrink-0">' +
          '<a href="../principal/principal-timetable-builder.html" class="px-3.5 py-1.5 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-xl transition shadow-2xs flex items-center gap-1.5">' +
            '<span class="material-symbols-outlined text-[15px] text-slate-500">grid_view</span>' +
            '<span>Open Timetable Builder</span>' +
          '</a>' +
        '</div>';
    }
  }

  function executeApproveAndPublish() {
    if (!confirm('Approve and publish this timetable to live Student and Teacher portals?')) return;
    return fetchJSON(API + '/publish', {
      method: 'POST',
      body: JSON.stringify({ published_by: 'Admin', note: 'Approved and published by School Administrator' })
    }).then(function (res) {
      if (res.status !== 200 || !res.body || !res.body.success) {
        throw new Error(res.body && (res.body.message || res.body.error) || 'Publish failed');
      }
      if (window.NGISUI && window.NGISUI.toast) {
        window.NGISUI.toast('Timetable approved and published successfully!', 'success');
      } else {
        alert('Timetable approved and published successfully!');
      }
      loadDraftStatus();
      load();
    }).catch(function (err) {
      if (window.NGISUI && window.NGISUI.toast) {
        window.NGISUI.toast('Error: ' + err.message, 'error');
      } else {
        alert('Error: ' + err.message);
      }
    });
  }

  function promptRevisionRequest() {
    var note = prompt('Please specify revision instructions for the Principal:', 'Please adjust Friday afternoon science period allocations.');
    if (!note) return;
    return fetchJSON(API + '/request-revision', {
      method: 'POST',
      body: JSON.stringify({ reviewed_by: 'Admin', note: note })
    }).then(function (res) {
      if (res.status !== 200 || !res.body || !res.body.success) {
        throw new Error(res.body && (res.body.message || res.body.error) || 'Revision request failed');
      }
      if (window.NGISUI && window.NGISUI.toast) {
        window.NGISUI.toast('Revision request sent to Principal.', 'info');
      } else {
        alert('Revision request sent to Principal.');
      }
      loadDraftStatus();
    }).catch(function (err) {
      alert('Error: ' + err.message);
    });
  }

  function openCompareDiffModal() {
    return fetchJSON(API + '/publication/diff').then(function (res) {
      var diff = res.body && res.body.diff || { changed: 0, changes: [] };
      alert('Draft Changes vs Published Schedule:\nTotal changes: ' + diff.changed + ' periods\n' +
        (diff.changes || []).slice(0, 5).map(function(c) { return '• ' + c.day + ' P' + c.period + ' (' + c.class_id + '): ' + c.kind; }).join('\n'));
    }).catch(function (err) {
      alert('Error: ' + err.message);
    });
  }

  /* ═══ detail modal ═══ */
  function openDetail(classId) {
    var modal = document.getElementById('monDetailModal');
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.classList.add('open', 'is-open');
    var body = document.getElementById('monDetailBody');
    if (body) {
      body.innerHTML = window.NGIS_SKELETON
        ? window.NGIS_SKELETON.table({ rows: 4 })
        : '<div class="py-12 text-center text-xs text-slate-400">Loading timetable details…</div>';
    }
    fetchJSON(API + '/monitoring/classes/' + encodeURIComponent(classId)).then(function (res) {
      if (res.status !== 200 || !res.body.success) throw new Error(res.body.message || 'not found');
      state.detail = res.body;
      state.previewMode = res.body.row.published ? 'published' : 'draft';
      renderDetail();
    }).catch(function (err) {
      if (body) body.innerHTML = '<div class="py-12 text-center text-xs text-rose-600">' + esc(err.message) + '</div>';
    });
  }

  function previewGrid(lessons) {
    var d = state.detail; if (!d) return '';
    var days = ['ច័ន្ទ (Mon)', 'អង្គារ (Tue)', 'ពុធ (Wed)', 'ព្រហស្បតិ៍ (Thu)', 'សុក្រ (Fri)'];
    var bySlot = {};
    (lessons || []).forEach(function (l) {
      var dKey = l.day || '';
      bySlot[dKey + '|' + l.shift + '|' + l.period] = l;
    });
    var periods = [1, 2, 3, 4, 5];
    var shifts = [
      { key: 'ព្រឹក', label: 'Morning / ព្រឹក' },
      { key: 'រសៀល', label: 'Afternoon / រសៀល' }
    ];
    var html = '<div class="overflow-x-auto rounded-xl border border-slate-200 bg-white"><table class="w-full text-xs min-w-[620px] border-collapse"><thead><tr class="bg-slate-50 text-slate-600 text-[11px] border-b border-slate-200">' +
      '<th class="px-3 py-2 text-left font-medium border-r border-slate-200 w-28">Shift & Period</th>';
    days.forEach(function (day) { html += '<th class="px-3 py-2 text-center font-medium border-r border-slate-200 last:border-r-0">' + esc(day) + '</th>'; });
    html += '</tr></thead><tbody class="divide-y divide-slate-100">';
    shifts.forEach(function (shiftObj) {
      periods.forEach(function (p) {
        html += '<tr class="hover:bg-slate-50/50 transition">';
        html += '<td class="px-3 py-2 border-r border-slate-200 text-slate-500 whitespace-nowrap text-[11px] font-medium bg-slate-50/60">' + esc(shiftObj.label) + ' P' + p + '</td>';
        days.forEach(function (day) {
          var khmerDay = day.split(' ')[0];
          var l = bySlot[khmerDay + '|' + shiftObj.key + '|' + p] || bySlot[day + '|' + shiftObj.key + '|' + p];
          html += '<td class="p-1.5 border-r border-slate-100 last:border-r-0 align-top">';
          if (l) {
            html += '<div class="rounded-lg p-2 ' + (state.previewMode === 'published'
              ? 'bg-emerald-50 border border-emerald-200 text-emerald-900' : 'bg-amber-50 border border-amber-200 text-amber-900') + '">' +
              '<div class="font-medium text-xs truncate" title="' + esc(l.subject) + '">' + esc(l.subject) + '</div>' +
              '<div class="text-[10px] text-slate-500 truncate mt-0.5">' + esc(l.teacher) + '</div></div>';
          } else {
            html += '<div class="h-10 rounded-lg border border-dashed border-slate-200/80 bg-slate-50/30 flex items-center justify-center text-[10px] text-slate-300">Open Slot</div>';
          }
          html += '</td>';
        });
        html += '</tr>';
      });
    });
    html += '</tbody></table></div>';
    return html;
  }

  function renderDetail() {
    var d = state.detail; if (!d) return;
    var r = d.row, ci = d.class_info, prep = d.preparation, pub = d.publication;
    var body = document.getElementById('monDetailBody');
    if (!body) return;

    var titleEl = document.getElementById('monDetailTitle');
    if (titleEl) titleEl.textContent = (r.grade && r.section ? 'Grade ' + r.grade + ' - ' + r.section : ci.class) + ' (' + ci.class + ')';
    var badgeEl = document.getElementById('monDetailStatusBadge');
    if (badgeEl) badgeEl.innerHTML = badge(prep.status, prep.status_label);
    var subEl = document.getElementById('monDetailSubtitle');
    if (subEl) subEl.textContent = ci.campus + ' · ' + ci.department + ' · ' + ci.room + ' (' + (ci.student_count || 0) + ' students)';

    var completionBits = prep.completion_available
      ? prep.placed_periods + ' / ' + prep.required_periods + ' periods placed'
        + (prep.missing_periods ? ' · <span class="text-amber-700 font-medium">' + prep.missing_periods + ' missing</span>' : ' · complete')
      : 'Requirement data not available';

    var conflictsHtml = prep.conflicts && prep.conflicts.length
      ? prep.conflicts.map(function (c) {
          return '<li class="text-[11px] text-rose-700 flex items-start gap-1.5"><span class="material-symbols-outlined text-[14px] mt-0.5">error</span><span>' +
            esc(c.message_en || c.type) + ' <span class="text-slate-400">(' + esc(c.key) + ')</span></span></li>';
        }).join('')
      : '<li class="text-[11px] text-emerald-700 flex items-center gap-1.5"><span class="material-symbols-outlined text-[14px]">check_circle</span>No unresolved scheduling conflicts</li>';

    var pubBits = pub.has_publication
      ? '<div class="grid grid-cols-2 gap-x-4 gap-y-2 text-[11px]">' +
        row2('Version', 'v' + pub.version) +
        row2('Published by', esc(pub.published_by || '—')) +
        row2('Published at', fmtDate(pub.published_at)) +
        row2('Effective from', esc(pub.effective_from || '—')) +
        row2('This class in publication', pub.class_in_publication ? '<span class="text-emerald-700 font-medium">Included</span>' : '<span class="text-amber-700 font-medium">Not included</span>') +
        row2('Pending draft update', pub.update_pending ? '<span class="text-teal-700 font-medium">Yes — newer draft exists</span>' : 'No') +
        '</div>'
      : '<p class="text-[11px] text-slate-500">No timetable has been published yet. Portals show an official "not published" notice.</p>';

    var actHtml = (d.activity_history || []).length
      ? d.activity_history.map(function (e) {
          var icon = e.type === 'publication' ? 'publish' : e.type === 'reminder' ? 'notifications_active' : 'edit_note';
          return '<li class="flex items-start gap-2.5 py-1.5 border-b border-slate-100 last:border-0">' +
            '<span class="w-6 h-6 flex items-center justify-center shrink-0 text-slate-500"><span class="material-symbols-outlined text-[13px]">' + icon + '</span></span>' +
            '<div class="min-w-0"><div class="text-[11px] text-slate-700">' + esc(e.action) + '</div>' +
            '<div class="text-[10px] text-slate-400">' + esc(e.actor) + ' · ' + fmtDate(e.at) + '</div></div></li>';
        }).join('')
      : '<li class="text-[11px] text-slate-400 py-2">No recorded audit activity for this class yet.</li>';

    var draftCount = (d.preview && d.preview.draft || []).length;
    var pubCount = (d.preview && d.preview.published || []).length;

    var subjectsListHtml = '';
    if (prep.subjects && prep.subjects.length) {
      subjectsListHtml = '<div class="mt-4 rounded-xl border border-slate-200 p-4 bg-slate-50/40">' +
        '<h4 class="text-xs font-medium text-slate-800 flex items-center gap-1.5 mb-2.5"><span class="material-symbols-outlined text-[16px] text-emerald-700">menu_book</span>Curriculum Subject Allocation (' + prep.required_periods + ' Total Periods Required)</h4>' +
        '<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">' +
        prep.subjects.map(function(s) {
          return '<div class="bg-white border border-slate-200/80 rounded-lg p-2.5 shadow-2xs">' +
            '<div class="flex items-center justify-between text-xs mb-1">' +
              '<span class="font-medium text-slate-900 truncate" title="' + esc(s.subject_name) + '">' + esc(s.subject_name) + '</span>' +
              '<span class="text-[10px] px-1.5 py-0.5 rounded font-medium ' + (s.complete ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600') + '">' + s.placed + '/' + s.required + 'p</span>' +
            '</div>' +
            '<div class="text-[10px] text-slate-400 truncate">' + esc(s.assigned_teacher || 'Unassigned') + '</div>' +
          '</div>';
        }).join('') +
        '</div></div>';
    }

    body.innerHTML =
      '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">' +
        '<section class="rounded-xl border border-slate-200 p-4 space-y-2 bg-white">' +
          '<h4 class="text-xs font-medium text-slate-800 flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px] text-emerald-700">school</span>Class Information</h4>' +
          '<div class="grid grid-cols-2 gap-x-4 gap-y-2 text-[11px]">' +
            row2('Class Code', esc(ci.class)) + row2('Campus', esc(ci.campus)) +
            row2('Department', esc(ci.department)) + row2('Academic Year', esc(ci.academic_year)) +
            row2('Responsible Faculty', esc(ci.responsible.name) + ' (' + esc(ci.responsible.role) + ')') +
            row2('Cohort Size', String(ci.student_count || 0) + ' Students') +
          '</div></section>' +
        '<section class="rounded-xl border border-slate-200 p-4 space-y-2 bg-white">' +
          '<h4 class="text-xs font-medium text-slate-800 flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px] text-amber-600">pending_actions</span>Preparation Status</h4>' +
          '<div class="text-[11px] text-slate-600">' + badge(prep.status, prep.status_label) + ' <span class="ml-2">' + completionBits + '</span></div>' +
          (prep.completion_available ? '<div class="h-1.5 rounded-full bg-slate-100 overflow-hidden"><div class="h-full rounded-full ' + ((prep.completion_pct || 0) >= 100 ? 'bg-emerald-600' : 'bg-amber-500') + '" style="width:' + Math.min(prep.completion_pct || 0, 100) + '%"></div></div>' : '') +
          '<ul class="space-y-1 pt-1">' + conflictsHtml + '</ul>' +
        '</section>' +
      '</div>' +
      subjectsListHtml +
      '<section class="rounded-xl border border-slate-200 p-4 space-y-2 mt-4 bg-white">' +
        '<h4 class="text-xs font-medium text-slate-800 flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px] text-emerald-700">verified</span>Publication Information</h4>' +
        pubBits +
      '</section>' +
      '<section class="rounded-xl border border-slate-200 p-4 mt-4 bg-white">' +
        '<h4 class="text-xs font-medium text-slate-800 flex items-center gap-1.5 mb-2"><span class="material-symbols-outlined text-[16px] text-slate-500">history</span>Activity History</h4>' +
        '<ul class="max-h-44 overflow-y-auto pr-1">' + actHtml + '</ul>' +
      '</section>' +
      '<section class="rounded-xl border border-slate-200 p-4 mt-4 bg-white">' +
        '<div class="flex items-center justify-between gap-3 flex-wrap mb-3">' +
          '<h4 class="text-xs font-medium text-slate-800 flex items-center gap-1.5"><span class="material-symbols-outlined text-[16px] text-slate-500">calendar_view_week</span>Timetable Matrix Preview (Read-Only)</h4>' +
          '<div class="inline-flex rounded-lg border border-slate-200 overflow-hidden text-[11px]">' +
            '<button type="button" data-act="preview-draft" class="px-3 py-1 font-medium transition ' + (state.previewMode === 'draft' ? 'bg-amber-500 text-white' : 'bg-white text-slate-600 hover:bg-slate-50') + '">Draft (' + draftCount + ')</button>' +
            '<button type="button" data-act="preview-published" class="px-3 py-1 font-medium transition border-l border-slate-200 ' + (state.previewMode === 'published' ? 'bg-emerald-600 text-white' : 'bg-white text-slate-600 hover:bg-slate-50') + '">Published (' + pubCount + ')</button>' +
          '</div>' +
        '</div>' +
        previewGrid(state.previewMode === 'published' ? d.preview.published : d.preview.draft) +
        '<p class="text-[10px] text-slate-400 mt-2.5">Monitoring preview is read-only. Timetable generation, editing, and official publication are performed exclusively by the Principal in the Master Timetable Builder.</p>' +
      '</section>';

    bindDetailActions();
  }

  function row2(label, value) {
    return '<div><div class="text-slate-400 text-[10px]">' + label + '</div><div class="text-slate-700 font-medium">' + value + '</div></div>';
  }

  function closeDetail() {
    var modal = document.getElementById('monDetailModal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('open', 'is-open');
    }
    state.detail = null;
  }

  /* ═══ reminder modal ═══ */
  function openRemind(classId) {
    var r = findRow(classId);
    if (!r) return;
    state.remindCtx = r;
    var modal = document.getElementById('monRemindModal');
    if (!modal) return;
    var set = function (id, v) { var el = document.getElementById(id); if (el) el.textContent = v; };
    set('monRemindClass', (r.grade && r.section ? 'Grade ' + r.grade + ' - ' + r.section : r.class_display) + ' (' + r.class_display + ') · ' + (r.campus || ''));
    set('monRemindStatus', r.status_label);
    set('monRemindRecipient', (r.responsible.name || 'Unassigned') + ' (' + (r.responsible.role || '') + ')');
    set('monRemindDeficiency', r.required_periods
      ? (r.missing_periods ? r.missing_periods + ' of ' + r.required_periods + ' periods unplaced' : 'timetable complete but unpublished')
      : 'no timetable prepared');
    var msg = document.getElementById('monRemindMessage');
    if (msg) msg.value = '';
    var warn = document.getElementById('monRemindCooldown');
    if (warn) warn.classList.add('hidden');
    var force = document.getElementById('monRemindForce');
    if (force) force.value = 'false';
    var dl = document.getElementById('monRemindDeadline');
    if (dl) dl.value = '';
    modal.classList.remove('hidden');
    modal.classList.add('open', 'is-open');
  }

  function closeRemind() {
    var modal = document.getElementById('monRemindModal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('open', 'is-open');
    }
    state.remindCtx = null;
  }

  function findRow(classId) {
    var d = state.data;
    return d && d.rows ? d.rows.find(function (x) { return x.class_id === classId; }) : null;
  }

  function submitRemind() {
    var ctx = state.remindCtx;
    if (!ctx) return;
    var btn = document.getElementById('monRemindSubmit');
    if (btn) { btn.disabled = true; btn.classList.add('opacity-60'); }
    var payload = {
      message: (document.getElementById('monRemindMessage') || {}).value || '',
      deadline: (document.getElementById('monRemindDeadline') || {}).value || '',
      force_duplicate: (document.getElementById('monRemindForce') || {}).value === 'true'
    };
    fetchJSON(API + '/monitoring/classes/' + encodeURIComponent(ctx.class_id) + '/remind', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    }).then(function (res) {
      var body = res.body || {};
      if (res.status === 409 && body.cooldown_warning) {
        var warn = document.getElementById('monRemindCooldown');
        var txt = document.getElementById('monRemindCooldownText');
        if (warn) warn.classList.remove('hidden');
        if (txt) txt.textContent = body.message || 'A reminder was already sent recently.';
        var force = document.getElementById('monRemindForce');
        if (force) force.value = 'true';
        return;
      }
      if (res.status === 200 && body.success) {
        closeRemind();
        toast(body.message || 'Reminder sent successfully.', 'success');
        load();
      } else {
        toast(body.message || body.error || 'Reminder failed to send.', 'error');
      }
    }).catch(function () { toast('Reminder delivery failed (network error).', 'error'); })
      .finally(function () { if (btn) { btn.disabled = false; btn.classList.remove('opacity-60'); } });
  }

  /* ═══ toast ═══ */
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

  /* ═══ events ═══ */
  function bindDetailActions() {
    document.querySelectorAll('#monDetailBody [data-act]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var act = btn.getAttribute('data-act');
        if (act === 'preview-draft') { state.previewMode = 'draft'; renderDetail(); }
        if (act === 'preview-published') { state.previewMode = 'published'; renderDetail(); }
      });
    });
  }

  function bindEvents() {
    // filter selects
    ['monFilterCampus', 'monFilterDept', 'monFilterGrade', 'monFilterStatus', 'monFilterSort'].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.addEventListener('change', function () {
        if (id === 'monFilterCampus') state.filters.campus = el.value;
        if (id === 'monFilterDept') state.filters.department = el.value;
        if (id === 'monFilterGrade') state.filters.grade = el.value;
        if (id === 'monFilterStatus') state.filters.status = el.value;
        if (id === 'monFilterSort') state.filters.sort = el.value || 'attention';
        state.page = 1; load();
      });
    });
    // search (debounced)
    var searchEl = document.getElementById('monSearch');
    if (searchEl) {
      var t = null;
      searchEl.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () { state.filters.search = searchEl.value.trim(); state.page = 1; load(); }, 300);
      });
    }
    // clear filters
    var clearBtn = document.getElementById('monClearFilters');
    if (clearBtn) clearBtn.addEventListener('click', function () {
      state.filters = { campus: '', department: '', grade: '', status: '', search: '', sort: 'attention' };
      state.page = 1;
      ['monFilterCampus', 'monFilterDept', 'monFilterGrade', 'monFilterStatus'].forEach(function (id) {
        var el = document.getElementById(id); if (el) el.value = '';
      });
      if (searchEl) searchEl.value = '';
      var sortEl = document.getElementById('monFilterSort'); if (sortEl) sortEl.value = 'attention';
      load();
    });
    // pagination
    var prev = document.getElementById('monPagePrev'), next = document.getElementById('monPageNext');
    if (prev) prev.addEventListener('click', function () { if (state.page > 1) { state.page--; load(); } });
    if (next) next.addEventListener('click', function () { state.page++; load(); });
    // refresh
    var refresh = document.getElementById('monRefresh');
    if (refresh) refresh.addEventListener('click', function () { load(); });
    // export (preserves filters)
    var exportBtn = document.getElementById('monExport');
    if (exportBtn) exportBtn.addEventListener('click', function () {
      var q = queryString().replace(/page=\d+&?/, '').replace(/page_size=\d+&?/, '');
      var headers = actorHeaders();
      fetch(API + '/monitoring/export' + (q ? '?' + q : ''), { headers: headers })
        .then(function (res) { return res.blob(); })
        .then(function (blob) {
          var a = document.createElement('a');
          a.href = URL.createObjectURL(blob);
          a.download = 'timetable-monitoring.csv';
          a.click(); URL.revokeObjectURL(a.href);
        });
    });
    // table actions (event delegation)
    var tbody = document.getElementById('monTableBody');
    if (tbody) tbody.addEventListener('click', function (ev) {
      var btn = ev.target.closest('[data-act]');
      if (!btn) return;
      var classId = btn.getAttribute('data-class');
      if (btn.getAttribute('data-act') === 'view') openDetail(classId);
      if (btn.getAttribute('data-act') === 'remind') openRemind(classId);
    });
    // modal close
    document.querySelectorAll('[data-close="monDetail"]').forEach(function (b) { b.addEventListener('click', closeDetail); });
    document.querySelectorAll('[data-close="monRemind"]').forEach(function (b) { b.addEventListener('click', closeRemind); });
    var submit = document.getElementById('monRemindSubmit');
    if (submit) submit.addEventListener('click', submitRemind);
    // ESC closes modals
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') { closeDetail(); closeRemind(); }
    });
  }

  function init() {
    bindEvents();
    return load();
  }

  window.TIMETABLE_MONITORING = { init: init, refresh: load, openDetail: openDetail };
})();
