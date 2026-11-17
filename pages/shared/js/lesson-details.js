/* ══════════════════════════════════════════════════════════════
   NGIS Lesson Details — dedicated full-page lesson viewer
   Route: lesson-details.html?id={lessonId}&dept={subject}&portal={role}
   Reuses the shared RESOURCES data model (lesson-data.js), the
   shared bookmark store, and the global NGIS layout engine.
   ══════════════════════════════════════════════════════════════ */

/* ── State ── */
var _ldDept      = '';
var _ldLesson    = null;
var _ldLessonIdx = -1;
var _ldList      = [];
var _ldPage      = 1;
var _ldPageTotal = 1;
var _ldZoom      = 100;
var _ldLoadTimer = null;
var _ldExpanded  = false;

/* ── Element helpers ── */
function _ldEl(id) { return document.getElementById(id); }
function _ldShow(el, display) { if (el) el.style.display = display || ''; }

/* ════════════════════════════════════
   Boot
════════════════════════════════════ */
function ldInit() {
  var params = new URLSearchParams(window.location.search);
  var id = params.get('id') || params.get('lesson') || '';
  var dept = (params.get('dept') || params.get('subject') || '').toLowerCase();
  var role = (window.PAGE && window.PAGE.role) || 'student';

  /* Contextual back links keep the caller's portal + subject */
  var backUrl = 'lessons.html?dept=' + encodeURIComponent(dept || 'math') + '&portal=' + encodeURIComponent(role);
  var backLinks = ['ldBackLink', 'ldErrorBack', 'ldNavHome', 'ldCrumbSubject'];
  backLinks.forEach(function (bid) {
    var a = _ldEl(bid);
    if (a) a.href = backUrl;
  });

  if (!id) { ldShowError('No lesson selected', 'Open the Subject Library and choose a learning material to read.'); return; }

  /* Resolve the subject list — dynamic across every existing subject */
  if (dept && RESOURCES[dept]) {
    _ldDept = dept;
    _ldList = RESOURCES[dept];
  } else {
    /* Fallback: locate the lesson across all known subjects */
    var found = null;
    Object.keys(RESOURCES).some(function (key) {
      var hit = (RESOURCES[key] || []).find(function (x) { return x.id === id; });
      if (hit) { found = key; return true; }
      return false;
    });
    if (!found) { ldShowError('Resource not found', 'This learning material may have been removed, unpublished, or is not available to your account.'); return; }
    _ldDept = found;
    _ldList = RESOURCES[found];
  }

  /* Access validation: the lesson must exist inside the resolved subject
     scope. Unknown or out-of-scope ids never render. (Backend authorization
     hooks into the same check once the lessons API is wired.) */
  var idx = _ldList.findIndex(function (x) { return x.id === id; });
  if (idx === -1) {
    ldShowError('Resource not found', 'This learning material may have been removed, unpublished, or is not available to your account.');
    return;
  }

  _ldLessonIdx = idx;
  _ldLesson = _ldList[idx];

  /* Brief skeleton pass keeps loading feedback consistent, then render.
     Cancelled immediately when the user switches lessons. */
  if (_ldLoadTimer) clearTimeout(_ldLoadTimer);
  _ldShow(_ldEl('ldError'), 'none');
  _ldShow(_ldEl('ldContent'), 'none');
  _ldShow(_ldEl('ldLoading'), 'flex');
  document.title = 'NGIS — ' + (_ldLesson.fullName || _ldLesson.name);
  _ldLoadTimer = setTimeout(function () {
    _ldLoadTimer = null;
    _ldShow(_ldEl('ldLoading'), 'none');
    _ldShow(_ldEl('ldContent'), 'flex');
    ldRender();
  }, 220);
}

function ldRetry() { ldInit(); }

function ldShowError(title, text) {
  if (_ldLoadTimer) { clearTimeout(_ldLoadTimer); _ldLoadTimer = null; }
  _ldShow(_ldEl('ldLoading'), 'none');
  _ldShow(_ldEl('ldContent'), 'none');
  var t = _ldEl('ldErrorTitle'); if (t) t.textContent = title;
  var d = _ldEl('ldErrorText'); if (d) d.textContent = text;
  _ldShow(_ldEl('ldError'), 'flex');
  document.title = 'NGIS — Lesson unavailable';
}

/* ════════════════════════════════════
   Render
════════════════════════════════════ */
function ldRender() {
  var r = _ldLesson;
  if (!r) return;
  var role = (window.PAGE && window.PAGE.role) || 'student';
  var subjectName = OAK_SUBJECT_TITLES[_ldDept]
    ? (OAK_SUBJECT_TITLES[_ldDept].charAt(0) + OAK_SUBJECT_TITLES[_ldDept].slice(1).toLowerCase() + ' Library')
    : (_ldDept.charAt(0).toUpperCase() + _ldDept.slice(1) + ' Library');

  /* ── Header ── */
  var titleEl = _ldEl('ldTitle');
  if (titleEl) titleEl.textContent = r.fullName || r.name;
  var crumbSubject = _ldEl('ldCrumbSubject');
  if (crumbSubject) crumbSubject.textContent = subjectName;
  var crumbTopic = _ldEl('ldCrumbTopic');
  if (crumbTopic) crumbTopic.textContent = r.topic || typeMeta(r.type).label;

  /* Truthful meta line — only fields that exist in the data model */
  var metaBits = [];
  if (r.date) metaBits.push('Published ' + fmtDate(r.date));
  metaBits.push(typeMeta(r.type).label);
  if (r.fileType && r.fileType !== 'quiz') metaBits.push(String(r.fileType).toUpperCase());
  if (r.pages) metaBits.push(r.pages + ' pages');
  if (r.size && r.size !== '—') metaBits.push(r.size);
  var metaEl = _ldEl('ldMeta');
  if (metaEl) {
    metaEl.innerHTML = metaBits.map(function (b) { return '<span>' + escHtml(b) + '</span>'; }).join('');
  }

  /* ── Bookmark ── */
  ldSyncBookmark();

  /* ── Download visibility ── */
  var canDownload = r.fileType !== 'link' && r.fileType !== 'video' && r.src;
  ['ldDownloadBtn', 'ldToolDownloadBtn'].forEach(function (bid) {
    var b = _ldEl(bid);
    if (b) b.style.display = canDownload ? '' : 'none';
  });

  /* ── Description + info rows ── */
  var descEl = _ldEl('ldDesc');
  if (descEl) {
    descEl.textContent = getDesc(r);
    if (r.desc && r.desc.length > 0) descEl.textContent = r.desc;
    descEl.classList.remove('clamped');
  }
  var toggleBtn = _ldEl('ldDescToggle');
  if (toggleBtn) {
    toggleBtn.style.display = 'none';
    toggleBtn.textContent = 'Show more';
    toggleBtn.setAttribute('aria-expanded', 'false');
    /* Show More only when the description is genuinely long */
    if (descEl && descEl.textContent.length > 180) {
      toggleBtn.style.display = '';
      descEl.classList.add('clamped');
    }
  }

  var rowsEl = _ldEl('ldInfoRows');
  if (rowsEl) {
    var rows = [
      ['Subject', OAK_SUBJECT_TITLES[_ldDept] || _ldDept.toUpperCase()],
      ['Type', typeMeta(r.type).label]
    ];
    if (r.topic) rows.push(['Topic', r.topic]);
    if (r.fileType) rows.push(['Format', String(r.fileType).toUpperCase()]);
    if (r.pages) rows.push(['Pages', String(r.pages)]);
    if (r.questions) rows.push(['Questions', String(r.questions)]);
    if (r.size && r.size !== '—') rows.push(['File size', r.size]);
    if (r.downloads) rows.push(['Downloads', r.downloads.toLocaleString()]);
    if (r.date) rows.push(['Published', fmtDate(r.date)]);
    rowsEl.innerHTML = rows.map(function (row) {
      return '<li><span class="lbl">' + escHtml(row[0]) + '</span><span class="val">' + escHtml(row[1]) + '</span></li>';
    }).join('');
  }

  /* ── Related materials: same subject, prefer same topic ── */
  ldRenderRelated(r);

  /* ── Prev / next lesson navigation ── */
  ldRenderLessonNav(role);

  /* ── Viewer ── */
  _ldPage = 1;
  _ldZoom = 100;
  _ldSetExpanded(false);
  ldRenderViewer(r);
}

/* ── Description Show more / Show less ── */
function ldToggleDesc() {
  var descEl = _ldEl('ldDesc');
  var toggleBtn = _ldEl('ldDescToggle');
  if (!descEl || !toggleBtn) return;
  var clamped = descEl.classList.toggle('clamped');
  toggleBtn.textContent = clamped ? 'Show more' : 'Show less';
  toggleBtn.setAttribute('aria-expanded', clamped ? 'false' : 'true');
}

/* ── Related list ── */
function ldRenderRelated(r) {
  var card = _ldEl('ldRelatedCard');
  var list = _ldEl('ldRelatedList');
  if (!card || !list) return;

  var others = _ldList.filter(function (x) { return x.id !== r.id; });
  /* Same topic/chapter first, then the rest — no invented recommendations */
  others.sort(function (a, b) {
    var aSame = (a.topic && a.topic === r.topic) ? 0 : 1;
    var bSame = (b.topic && b.topic === r.topic) ? 0 : 1;
    return aSame - bSame;
  });
  var related = others.slice(0, 4);

  if (related.length === 0) { card.style.display = 'none'; return; }
  card.style.display = '';
  var role = (window.PAGE && window.PAGE.role) || 'student';
  list.innerHTML = related.map(function (x) {
    var m = typeMeta(x.type);
    var subBits = [x.topic || m.label];
    if (x.size && x.size !== '—') subBits.push(x.size);
    /* Page-box image thumbnail (asset-backed, no generated previews) */
    return '<a class="ld-related-item" href="' + lessonDetailsUrl(x.id, _ldDept, role) + '" onclick="ldGoTo(event,\'' + x.id + '\')">'
      + '<span class="ld-related-thumb"><img src="../../assets/images/lesson-page-box.svg" alt="" loading="lazy"></span>'
      + '<span class="ld-related-body">'
      + '<span class="ld-related-name">' + escHtml(x.fullName || x.name) + '</span>'
      + '<span class="ld-related-sub">' + escHtml(subBits.join(' • ')) + '</span>'
      + '</span>'
      + '<span class="ld-related-arrow" data-ngis-icon="chevronRight"></span>'
      + '</a>';
  }).join('');
  if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(list);
}

/* ── Previous / next lesson bar ── */
function ldRenderLessonNav(role) {
  var prev = _ldLessonIdx > 0 ? _ldList[_ldLessonIdx - 1] : null;
  var next = _ldLessonIdx < _ldList.length - 1 ? _ldList[_ldLessonIdx + 1] : null;

  var prevBtn = _ldEl('ldPrevLesson');
  var nextBtn = _ldEl('ldNextLesson');
  if (prevBtn) {
    prevBtn.disabled = !prev;
    prevBtn.title = prev ? (prev.fullName || prev.name) : 'No previous lesson';
  }
  if (nextBtn) {
    nextBtn.disabled = !next;
    nextBtn.title = next ? (next.fullName || next.name) : 'No next lesson';
  }
}

/* ── Navigate to another lesson (updates URL + view, keeps history) ── */
function ldGoTo(e, resId) {
  if (e) e.preventDefault();
  var idx = _ldList.findIndex(function (x) { return x.id === resId; });
  if (idx === -1) return;
  var role = (window.PAGE && window.PAGE.role) || 'student';
  var url = lessonDetailsUrl(resId, _ldDept, role);
  try { window.history.pushState({}, '', url); } catch (err) { window.location.href = url; return; }
  ldInit();
}

function ldGoRelative(delta) {
  var idx = _ldLessonIdx + delta;
  if (idx < 0 || idx >= _ldList.length) return;
  ldGoTo(null, _ldList[idx].id);
}

window.addEventListener('popstate', function () { ldInit(); });

/* ════════════════════════════════════
   Bookmark & download
════════════════════════════════════ */
function ldSyncBookmark() {
  var btn = _ldEl('ldBookmarkBtn');
  if (!btn || !_ldLesson) return;
  var active = NGISBookmarks.has(_ldLesson.id);
  var ico = btn.querySelector('[data-ngis-icon]');
  if (ico) ico.setAttribute('data-ngis-icon', active ? 'bookmarkAdded' : 'bookmark');
  btn.classList.toggle('active', active);
  btn.setAttribute('aria-pressed', active ? 'true' : 'false');
  if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(btn);
}

function ldToggleBookmark() {
  if (!_ldLesson) return;
  var active = NGISBookmarks.toggle(_ldLesson.id);
  ldSyncBookmark();
  if (window.toast) window.toast(active ? 'Saved to Bookmarks' : 'Removed from Bookmarks', 'info');
}

function ldDownload() {
  if (!_ldLesson || !_ldLesson.src) return;
  if (window.toast) window.toast('Preparing download of "' + (_ldLesson.fullName || _ldLesson.name) + '"…', 'info');
  ngisDownloadFile(_ldLesson.src, (_ldLesson.fullName || _ldLesson.name));
}

function ldOpenInNewTab() {
  if (_ldLesson && _ldLesson.src) window.open(_ldLesson.src, '_blank', 'noopener');
}

/* ════════════════════════════════════
   Document viewer
════════════════════════════════════ */
function _ldToolbarMode(mode) {
  /* Show/hide toolbar groups per viewer type */
  var pageGroup = _ldEl('ldPageGroup');
  var zoomGroup = _ldEl('ldZoomGroup');
  var fsBtn = _ldEl('ldFullscreenBtn');
  var openBtn = _ldEl('ldOpenTabBtn');
  if (pageGroup) pageGroup.style.display = (mode === 'pdf') ? '' : 'none';
  if (zoomGroup) zoomGroup.style.display = (mode === 'pdf' || mode === 'image') ? '' : 'none';
  if (fsBtn) fsBtn.style.display = (mode === 'pdf' || mode === 'image' || mode === 'video') ? '' : 'none';
  if (openBtn) openBtn.style.display = _ldLesson && _ldLesson.src ? '' : 'none';
}

function ldRenderViewer(r) {
  var body = _ldEl('ldViewerBody');
  if (!body) return;
  body.innerHTML = '';

  if (!r.src) { _ldToolbarMode('none'); _ldRenderUnsupported(r, body); return; }

  if (r.fileType === 'pdf' || r.fileType === 'quiz') {
    _ldToolbarMode('pdf');
    _ldPageTotal = r.pages || 1;
    _ldUpdatePageIndicator();
    var frame = document.createElement('iframe');
    frame.id = 'ldPdfFrame';
    frame.src = r.src + '#page=1&view=FitH';
    frame.title = r.fullName || r.name;
    frame.loading = 'lazy';
    frame.setAttribute('allow', 'fullscreen');
    body.appendChild(frame);
    body.classList.add('mode-pdf');
  } else if (r.fileType === 'image') {
    _ldToolbarMode('image');
    body.classList.add('mode-image');
    var wrap = document.createElement('div');
    wrap.className = 'ld-img-wrap';
    var img = document.createElement('img');
    img.src = r.src;
    img.alt = r.fullName || r.name;
    img.loading = 'lazy';
    img.addEventListener('error', function () {
      body.innerHTML = '';
      _ldToolbarMode('none');
      _ldRenderLoadFail(r, body);
    });
    wrap.appendChild(img);
    body.appendChild(wrap);
  } else if (r.fileType === 'video') {
    _ldToolbarMode('video');
    body.classList.add('mode-video');
    var vwrap = document.createElement('div');
    vwrap.className = 'ld-video-wrap';
    var vf = document.createElement('iframe');
    vf.src = r.src;
    vf.title = r.fullName || r.name;
    vf.setAttribute('allowfullscreen', '');
    vf.setAttribute('allow', 'fullscreen; encrypted-media; picture-in-picture');
    vwrap.appendChild(vf);
    body.appendChild(vwrap);
  } else if (r.fileType === 'link') {
    _ldToolbarMode('none');
    body.classList.remove('mode-pdf', 'mode-image', 'mode-video');
    body.innerHTML =
      '<div class="ld-unsupported">'
      + '<span class="material-symbols-outlined">open_in_new</span>'
      + '<h3>' + escHtml(r.fullName || r.name) + '</h3>'
      + '<p>This is an external learning resource. It opens in a new tab and is not stored on school servers.</p>'
      + '<a class="ld-btn ld-btn-primary" href="' + escHtml(r.src) + '" target="_blank" rel="noopener noreferrer">'
      + '<span data-ngis-icon="open"></span> Open Link</a>'
      + '</div>';
  } else {
    /* Unsupported / unrenderable format — never a broken iframe or
       endless spinner: explain and offer the file itself. */
    _ldToolbarMode('none');
    _ldRenderUnsupported(r, body);
  }

  if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(body);
}

function _ldRenderUnsupported(r, body) {
  body.classList.remove('mode-pdf', 'mode-image', 'mode-video');
  body.innerHTML =
    '<div class="ld-unsupported">'
    + '<span class="material-symbols-outlined">description</span>'
    + '<h3>' + escHtml(r.fullName || r.name) + '</h3>'
    + '<div class="ld-file-chips">'
    + '<span class="ld-file-chip">Format: ' + escHtml((r.fileType || 'unknown').toUpperCase()) + '</span>'
    + (r.size && r.size !== '—' ? '<span class="ld-file-chip">Size: ' + escHtml(r.size) + '</span>' : '')
    + '</div>'
    + '<p>This file format cannot be safely displayed inside the browser viewer. You can download it to open with a compatible application.</p>'
    + (r.src ? '<button class="ld-btn ld-btn-primary" onclick="ldDownload()"><span data-ngis-icon="download"></span> Download File</button>' : '')
    + '</div>';
}

function _ldRenderLoadFail(r, body) {
  body.innerHTML =
    '<div class="ld-unsupported">'
    + '<span class="material-symbols-outlined">cloud_off</span>'
    + '<h3>Document could not be loaded</h3>'
    + '<p>The file server may be unreachable or the resource may have been moved. Check your connection and try again.</p>'
    + '<div style="display:flex; gap:10px; flex-wrap:wrap; justify-content:center;">'
    + '<button class="ld-btn ld-btn-primary" onclick="ldRender()"><span data-ngis-icon="view"></span> Retry</button>'
    + (r.src ? '<a class="ld-btn ld-btn-ghost" href="' + escHtml(r.src) + '" target="_blank" rel="noopener noreferrer"><span data-ngis-icon="open"></span> Open in new tab</a>' : '')
    + '</div>'
    + '</div>';
}

/* ── PDF pagination (real page count from the data model) ── */
function _ldUpdatePageIndicator() {
  var cur = _ldEl('ldPageCur');
  var tot = _ldEl('ldPageTotal');
  if (cur) cur.textContent = String(_ldPage);
  if (tot) tot.textContent = String(_ldPageTotal);
  var prev = _ldEl('ldPagePrev');
  var next = _ldEl('ldPageNext');
  if (prev) prev.disabled = _ldPage <= 1;
  if (next) next.disabled = _ldPage >= _ldPageTotal;
}

function ldPageStep(delta) {
  if (_ldPageTotal <= 1) return;
  var target = Math.min(_ldPageTotal, Math.max(1, _ldPage + delta));
  if (target === _ldPage) return;
  _ldPage = target;
  _ldUpdatePageIndicator();
  var frame = _ldEl('ldPdfFrame');
  if (frame && _ldLesson) {
    frame.src = _ldLesson.src + '#page=' + _ldPage + '&view=FitH' + (_ldZoom !== 100 ? '&zoom=' + _ldZoom : '');
  }
}

/* ── Zoom (PDF via native viewer params · image via CSS scale) ── */
function _ldApplyZoom() {
  var fitBtn = _ldEl('ldZoomFit');
  if (fitBtn) fitBtn.textContent = _ldZoom + '%';
  var img = document.querySelector('#ldViewerBody .ld-img-wrap img');
  if (img) img.style.transform = 'scale(' + (_ldZoom / 100) + ')';
}

function ldZoom(delta) {
  _ldZoom = Math.min(200, Math.max(50, _ldZoom + delta));
  _ldApplyZoom();
  if (_ldLesson && (_ldLesson.fileType === 'pdf' || _ldLesson.fileType === 'quiz')) {
    var frame = _ldEl('ldPdfFrame');
    if (frame) frame.src = _ldLesson.src + '#page=' + _ldPage + '&zoom=' + _ldZoom;
  }
}

function ldZoomFit() {
  _ldZoom = 100;
  _ldApplyZoom();
  if (_ldLesson && (_ldLesson.fileType === 'pdf' || _ldLesson.fileType === 'quiz')) {
    var frame = _ldEl('ldPdfFrame');
    if (frame) frame.src = _ldLesson.src + '#page=' + _ldPage + '&view=FitH';
  }
}

/* ════════════════════════════════════
   Expanded reading mode (fullscreen with in-page fallback)
════════════════════════════════════ */
function _ldSetExpanded(on) {
  _ldExpanded = !!on;
  document.body.classList.toggle('ld-expanded', _ldExpanded);
  var btn = _ldEl('ldFullscreenBtn');
  if (btn) {
    var ico = btn.querySelector('[data-ngis-icon]');
    if (ico) ico.setAttribute('data-ngis-icon', _ldExpanded ? 'collapse' : 'expand');
    btn.title = _ldExpanded ? 'Exit expanded reading mode' : 'Expanded reading mode';
    if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(btn);
  }
}

function ldToggleFullscreen() {
  var card = _ldEl('ldViewerCard');
  if (!card) return;
  var fsEl = document.fullscreenElement || document.webkitFullscreenElement;
  if (!fsEl && card.requestFullscreen) {
    card.requestFullscreen().then(function () { _ldSetExpanded(true); }).catch(function () {
      /* Fullscreen unavailable (iOS Safari) — reliable in-page expansion */
      _ldSetExpanded(!_ldExpanded);
    });
  } else if (!fsEl && card.webkitRequestFullscreen) {
    card.webkitRequestFullscreen();
    _ldSetExpanded(true);
  } else if (document.exitFullscreen) {
    document.exitFullscreen().catch(function () {});
    _ldSetExpanded(false);
  } else {
    _ldSetExpanded(!_ldExpanded);
  }
}

document.addEventListener('fullscreenchange', function () {
  var fsEl = document.fullscreenElement || document.webkitFullscreenElement;
  _ldSetExpanded(!!fsEl);
});
document.addEventListener('webkitfullscreenchange', function () {
  var fsEl = document.fullscreenElement || document.webkitFullscreenElement;
  _ldSetExpanded(!!fsEl);
});

/* Escape exits in-page expanded mode */
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape' && _ldExpanded && !(document.fullscreenElement || document.webkitFullscreenElement)) {
    _ldSetExpanded(false);
  }
  /* Left/Right arrow page stepping for PDFs when the viewer is focused */
  if (_ldLesson && (_ldLesson.fileType === 'pdf' || _ldLesson.fileType === 'quiz') && _ldPageTotal > 1) {
    if (e.target && e.target.matches && e.target.matches('input, textarea, select')) return;
    if (e.key === 'ArrowLeft') ldPageStep(-1);
    if (e.key === 'ArrowRight') ldPageStep(1);
  }
});

/* ── Boot ── */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', ldInit);
} else {
  ldInit();
}
