import re

# Read student-grades.html
with open('pages/student/student-grades.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Let's check the head
head_part = orig[:orig.find('<body')]

# Craft new body content
new_html = head_part + '''<body data-page="student" data-role="student" class="student-dashboard font-sans selection:bg-forest-100 selection:text-forest-800 bg-[#F7F9F7]">
<main class="main">

  <!-- ═══════════════ TOPBAR / HERO HEADER ═══════════════ -->
  <header id="heroBanner" role="banner"></header>

  <!-- ═══════════════ EDITORIAL WORKSPACE ═══════════════ -->
  <div class="subpage-container space-y-6">

    <!-- Header Banner -->
    <div class="bg-white rounded-2xl border border-surface-border p-5 sm:p-6 shadow-xs">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-normal bg-forest-50 text-forest-800 border border-forest-200">
              <span class="material-symbols-outlined text-[13px] text-forest-700">verified</span>
              Official Academic Records
            </span>
            <span class="text-xs text-ink-soft">Academic Year 2025–2026</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-normal text-forest-800 tracking-tight font-display">
            Academic Results &amp; Documents
          </h1>
          <p class="text-xs sm:text-sm text-ink-muted mt-1 max-w-2xl leading-relaxed">
            Official teacher-uploaded transcripts, evaluations, and released academic records. View or download authentic verified documents directly.
          </p>
        </div>

        <div class="flex items-center gap-2 self-start sm:self-auto shrink-0">
          <a href="student-notifications.html" class="px-3.5 py-2 rounded-xl border border-surface-border text-forest-800 bg-white hover:bg-surface-subtle flex items-center gap-1.5 transition-all text-xs font-normal shadow-xs">
            <span class="material-symbols-outlined text-[16px] text-forest-700">notifications</span>
            <span>Result Notifications</span>
          </a>
        </div>
      </div>
    </div>

    <!-- Results List Container (Loaded from /api/academic/transcripts) -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display flex items-center gap-2">
          <span>Released Academic Documents</span>
          <span id="resultsCountBadge" class="text-xs font-normal px-2.5 py-0.5 rounded-full bg-forest-100 text-forest-800 border border-forest-200">Loading…</span>
        </h2>
      </div>

      <!-- Loading Skeleton -->
      <div id="resultsLoading" class="bg-white rounded-2xl border border-surface-border p-8 text-center space-y-3">
        <div class="w-8 h-8 border-2 border-forest-700 border-t-transparent rounded-full animate-spin mx-auto"></div>
        <p class="text-xs text-ink-muted font-normal">Loading official teacher-uploaded documents…</p>
      </div>

      <!-- Real Cards Grid / List -->
      <div id="resultsList" class="space-y-4 hidden"></div>

      <!-- Empty State -->
      <div id="resultsEmpty" class="hidden bg-white rounded-2xl border border-surface-border p-10 text-center space-y-3">
        <div class="w-12 h-12 rounded-2xl bg-surface-subtle text-ink-muted flex items-center justify-center mx-auto">
          <span class="material-symbols-outlined text-2xl">description</span>
        </div>
        <h3 class="text-base font-normal text-forest-800 font-display">No Academic Documents Released Yet</h3>
        <p class="text-xs text-ink-muted max-w-md mx-auto">When your teachers upload verified evaluation documents or transcripts for your enrolled classes, they will be listed here automatically.</p>
      </div>

      <!-- In Progress / Upcoming Term Notification Card -->
      <article class="bg-white rounded-2xl border border-surface-border shadow-xs p-4 sm:p-5">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div class="flex items-center gap-3.5 min-w-[240px]">
            <div class="w-11 h-11 rounded-2xl bg-amber-50 border border-amber-200 text-amber-700 flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[22px]">pending_actions</span>
            </div>
            <div>
              <div class="font-normal text-forest-800 text-base leading-tight font-display">Semester 2 (2025–26)</div>
              <div class="text-xs text-ink-soft mt-0.5">Current Term • In Progress</div>
            </div>
          </div>

          <div class="shrink-0">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-normal bg-amber-50 text-amber-800 border border-amber-200">
              <span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
              Term Active
            </span>
          </div>

          <div class="flex-1 max-w-xl text-xs text-ink-muted leading-relaxed">
            <div class="font-normal text-ink-main">Assessments and coursework are currently in progress.</div>
            <div class="text-[11px] text-ink-soft mt-0.5">Official evaluation documents will be published following examination review.</div>
          </div>

          <div class="shrink-0">
            <button type="button" id="btnNotifySem2" onclick="toggleResultNotification()" class="px-4 py-2 rounded-xl border border-surface-border text-forest-800 font-normal bg-white hover:bg-surface-subtle flex items-center gap-1.5 transition-all text-xs shadow-xs cursor-pointer">
              <span class="material-symbols-outlined text-[16px] text-forest-700" id="iconNotifySem2">notifications_active</span>
              <span id="textNotifySem2">Notify When Ready</span>
            </button>
          </div>
        </div>
      </article>

    </div>

    <!-- Official Registry Footer Strip -->
    <div class="p-4 px-6 bg-white rounded-2xl border border-surface-border shadow-xs flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-ink-soft">
      <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-[16px] text-forest-700">verified</span>
        <span>Official Academic Records • All documents authenticated by Office of Academic Registry</span>
      </div>
      <div class="text-ink-muted font-normal">
        Academic Session: 2025–2026
      </div>
    </div>

  </div>
</main>

<!-- ════════════════════════════════════════════════════════════════ -->
<!-- RESULT DOCUMENT VIEWER MODAL (Real Teacher-Uploaded Document)     -->
<!-- ════════════════════════════════════════════════════════════════ -->
<div id="resultViewerModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/60 backdrop-blur-xs transition-opacity" role="dialog" aria-modal="true" aria-labelledby="viewerDocTitle">
  <div class="fixed inset-0 cursor-pointer" data-close-modal="true" onclick="closeDocumentViewer()"></div>
  
  <div class="relative w-full max-w-5xl bg-white dark:bg-slate-900 rounded-2xl sm:rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col max-h-[94vh] max-h-[94dvh] overflow-hidden z-10 transition-transform">
    <!-- Modal Toolbar -->
    <div class="sticky top-0 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md z-20 border-b border-surface-border px-4 sm:px-6 py-3.5 flex items-center justify-between gap-3">
      <div class="min-w-0 flex-1">
        <div class="flex items-center gap-2 flex-wrap">
          <span id="viewerDocTypeBadge" class="px-2 py-0.5 rounded-full text-[11px] font-normal bg-forest-100 text-forest-800 border border-forest-200">Document</span>
          <span id="viewerDocTermBadge" class="text-xs text-ink-soft font-normal">Semester 1</span>
        </div>
        <h2 id="viewerDocTitle" class="text-sm sm:text-base text-forest-800 dark:text-slate-100 font-normal truncate mt-0.5 font-display">
          Document Title
        </h2>
        <div id="viewerDocMeta" class="text-[11px] text-ink-muted truncate font-normal">
          Uploaded by Faculty
        </div>
      </div>

      <!-- Controls: Zoom In, Zoom Out, Fullscreen, Download, Close -->
      <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
        <div class="hidden sm:flex items-center gap-1 bg-surface-subtle p-1 rounded-xl border border-surface-borderLight">
          <button type="button" onclick="zoomViewer(-15)" class="w-8 h-8 rounded-lg flex items-center justify-center text-ink-muted hover:text-forest-800 hover:bg-white transition cursor-pointer" title="Zoom Out" aria-label="Zoom Out">
            <span class="material-symbols-outlined text-[18px]">zoom_out</span>
          </button>
          <span id="viewerZoomLabel" class="text-[11px] font-normal text-ink-muted w-10 text-center">100%</span>
          <button type="button" onclick="zoomViewer(15)" class="w-8 h-8 rounded-lg flex items-center justify-center text-ink-muted hover:text-forest-800 hover:bg-white transition cursor-pointer" title="Zoom In" aria-label="Zoom In">
            <span class="material-symbols-outlined text-[18px]">zoom_in</span>
          </button>
          <button type="button" onclick="resetViewerZoom()" class="px-2 h-8 rounded-lg text-[11px] font-normal text-ink-muted hover:text-forest-800 hover:bg-white transition cursor-pointer" title="Reset Zoom">
            Reset
          </button>
        </div>

        <button type="button" id="viewerDownloadBtn" onclick="downloadCurrentDocument()" class="px-3 h-8 sm:h-9 rounded-xl border border-surface-border text-forest-800 bg-white hover:bg-surface-subtle flex items-center gap-1.5 transition text-xs font-normal shadow-xs cursor-pointer" title="Download Original File">
          <span class="material-symbols-outlined text-[16px] text-forest-700">download</span>
          <span class="hidden md:inline">Download Original</span>
        </button>

        <button type="button" onclick="toggleViewerFullscreen()" class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl border border-surface-border text-forest-800 bg-white hover:bg-surface-subtle flex items-center justify-center transition cursor-pointer" title="Toggle Fullscreen" aria-label="Toggle Fullscreen">
          <span id="viewerFsIcon" class="material-symbols-outlined text-[18px]">fullscreen</span>
        </button>

        <!-- Working Close (X) button -->
        <button type="button" onclick="closeDocumentViewer()" class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-surface-subtle hover:bg-surface-border text-ink-muted hover:text-forest-800 flex items-center justify-center transition cursor-pointer" title="Close Viewer (Esc)" aria-label="Close">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
    </div>

    <!-- Viewer Document Body -->
    <div id="viewerContentArea" class="flex-1 overflow-auto p-4 sm:p-6 bg-slate-100/70 dark:bg-slate-950/60 flex items-center justify-center min-h-[400px] sm:min-h-[560px]">
      <!-- Image Container -->
      <div id="viewerImgContainer" class="w-full h-full flex items-center justify-center overflow-auto hidden">
        <img id="viewerImg" src="" alt="Academic Result Document" class="max-w-full max-h-[75vh] object-contain rounded-lg shadow-md transition-transform duration-150 origin-center bg-white" />
      </div>

      <!-- PDF / Document Iframe Container -->
      <div id="viewerPdfContainer" class="w-full h-full min-h-[500px] sm:min-h-[600px] hidden">
        <iframe id="viewerPdf" src="" class="w-full h-full min-h-[500px] sm:min-h-[600px] rounded-lg border border-slate-200 bg-white" title="Academic Result PDF Viewer"></iframe>
      </div>
    </div>
  </div>
</div>

<!-- Page Config & NGIS Scripts -->
<script>
window.PAGE = { role: 'student', active: 'grades' };
(function () {
  try { var _t = localStorage.getItem('ngis-theme'); if (_t) document.documentElement.setAttribute('data-theme', _t); } catch (e) {}
  var saved = null;
  try { saved = JSON.parse(localStorage.getItem('ngis_chat_user') || 'null'); } catch (e) {}
  if (saved) { window.PAGE.role = saved.role || 'student'; window.CURRENT_USER = saved; }
  document.body.classList.add('ready');
})();
</script>

<script>
window.PAGE = {"role":"student","active":"grades"};
window.HERO_CONFIG = {
  title: 'Academic Performance & Report Cards',
  greeting: 'Official semester records, monthly reviews, and performance evaluations',
  name: 'Nrinphouneta Hok',
  id: 'Student ID: 2026-STD-0142',
  grade: 'Grade 10',
  avatar: '../../assets/images/dashboard-student-portrait.jpg',
  avatarSm: '../../assets/images/dashboard-student-portrait.jpg',
  homeLink: 'student.html',
  signOutLink: '../../index.html',
  profileLink: 'student-profile.html',
  notifLink: 'student-notifications.html',
  chatLink: 'student-notifications.html',
  notifCount: 3,
  breadcrumbs: [
    { label: 'Dashboard', href: 'student.html' },
    { label: 'Report Cards & Performance' }
  ],
  ddRows: [
    { icon: 'school', text: 'Grade 10 — Science Stream' },
    { icon: 'class', text: 'Class 10A · SS2 KH' },
    { icon: 'email', text: 'nrinphouneta.hok@ciaschool.edu.kh' },
    { icon: 'calendar_today', text: 'Academic Year: 2025–2026' }
  ]
};
</script>
<script src="js/hero.js"></script>
<script src="../../assets/js/layout.js"></script>

<script>
/* ═══════════════════════════════════════════════════════════════════
   STUDENT ACADEMIC RESULTS ENGINE
   Reuses real teacher uploads from /api/academic/transcripts
   ═══════════════════════════════════════════════════════════════════ */
var CURRENT_TRANSCRIPTS = [];
var ACTIVE_DOC = null;
var CURRENT_ZOOM = 100;
var SAVED_SCROLL_POS = 0;

async function loadStudentTranscripts() {
  const loading = document.getElementById('resultsLoading');
  const listEl = document.getElementById('resultsList');
  const emptyEl = document.getElementById('resultsEmpty');
  const countBadge = document.getElementById('resultsCountBadge');

  try {
    const res = await fetch('/api/academic/transcripts?studentId=2026-STD-0142');
    if (!res.ok) throw new Error('API returned HTTP ' + res.status);
    const json = await res.json();
    CURRENT_TRANSCRIPTS = json.data || [];

    if (loading) loading.classList.add('hidden');

    if (!CURRENT_TRANSCRIPTS.length) {
      if (emptyEl) emptyEl.classList.remove('hidden');
      if (countBadge) countBadge.textContent = '0 Documents';
      return;
    }

    if (countBadge) countBadge.textContent = CURRENT_TRANSCRIPTS.length + ' Available';
    if (listEl) {
      listEl.innerHTML = CURRENT_TRANSCRIPTS.map((t, idx) => renderTranscriptCard(t, idx)).join('');
      listEl.classList.remove('hidden');
    }
  } catch (err) {
    console.error('Failed to load transcripts:', err);
    if (loading) loading.classList.add('hidden');
    if (listEl) {
      listEl.innerHTML = `
        <div class="bg-amber-50 border border-amber-200 rounded-2xl p-6 text-center text-xs text-amber-800">
          <p class="font-normal mb-1">Could not load academic documents from the registry.</p>
          <button type="button" onclick="loadStudentTranscripts()" class="mt-2 px-3 py-1.5 bg-amber-600 text-white rounded-xl text-xs font-normal">Retry</button>
        </div>
      `;
      listEl.classList.remove('hidden');
    }
  }
}

function renderTranscriptCard(t, idx) {
  const isPdf = (t.fileType || '').toLowerCase().includes('pdf') || (t.fileUrl || '').toLowerCase().endsWith('.pdf');
  const typeLabel = isPdf ? 'Official PDF Document' : 'High-Resolution Document (PNG)';
  const icon = isPdf ? 'picture_as_pdf' : 'image';
  const term = t.term || 'Semester 1 (2025–26)';
  const teacher = t.uploadedBy || 'Lead Academic Faculty';
  const dateStr = t.uploadedAt ? new Date(t.uploadedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Official Released';

  return `
    <article class="bg-white rounded-2xl border border-surface-border shadow-xs hover:border-forest-300 transition-all p-4 sm:p-5">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div class="flex items-center gap-3.5 min-w-[260px]">
          <div class="w-12 h-12 rounded-2xl bg-forest-50 border border-forest-200 text-forest-800 flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined text-[24px] text-forest-700">${icon}</span>
          </div>
          <div>
            <div class="font-normal text-forest-800 text-base leading-tight font-display">${term}</div>
            <div class="text-xs text-ink-soft mt-0.5">Uploaded by ${teacher}</div>
          </div>
        </div>

        <div class="shrink-0 flex items-center gap-2">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-normal bg-forest-50 text-forest-800 border border-forest-200">
            <span class="material-symbols-outlined text-[13px] text-forest-700">verified</span>
            ${t.status || 'Official Released'}
          </span>
          <span class="text-xs text-ink-muted hidden sm:inline">• ${dateStr}</span>
        </div>

        <div class="flex-1 max-w-md text-xs text-ink-muted leading-relaxed">
          <div class="font-normal text-ink-main">${typeLabel}</div>
          <div class="text-[11px] text-ink-soft mt-0.5 truncate">${t.fileName || 'Verified evaluation record'}</div>
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <button type="button" onclick="openDocumentViewer(${idx})" class="px-4 py-2 border border-surface-border text-forest-800 font-normal rounded-xl bg-white hover:bg-surface-subtle flex items-center gap-1.5 transition-all text-xs shadow-xs cursor-pointer">
            <span class="material-symbols-outlined text-[16px] text-forest-700">visibility</span>
            <span>View Document</span>
          </button>
          <a href="${t.fileUrl}" download="${t.fileName || 'transcript'}" class="px-3 py-2 border border-surface-border text-ink-muted hover:text-forest-800 rounded-xl bg-white hover:bg-surface-subtle flex items-center justify-center transition-all text-xs shadow-xs" title="Download file" aria-label="Download original document">
            <span class="material-symbols-outlined text-[16px]">download</span>
          </a>
        </div>
      </div>
    </article>
  `;
}

/* ═══════════════════════════════════════════════════════════════════
   DOCUMENT VIEWER POPUP CONTROLS
   ═══════════════════════════════════════════════════════════════════ */
function openDocumentViewer(idx) {
  ACTIVE_DOC = CURRENT_TRANSCRIPTS[idx];
  if (!ACTIVE_DOC) return;

  SAVED_SCROLL_POS = window.scrollY || window.pageYOffset || 0;

  const modal = document.getElementById('resultViewerModal');
  const title = document.getElementById('viewerDocTitle');
  const meta = document.getElementById('viewerDocMeta');
  const termBadge = document.getElementById('viewerDocTermBadge');
  const typeBadge = document.getElementById('viewerDocTypeBadge');
  const imgBox = document.getElementById('viewerImgContainer');
  const pdfBox = document.getElementById('viewerPdfContainer');
  const imgEl = document.getElementById('viewerImg');
  const pdfEl = document.getElementById('viewerPdf');

  title.textContent = ACTIVE_DOC.term + ' — ' + (ACTIVE_DOC.fileName || 'Academic Record');
  meta.textContent = 'Uploaded by ' + (ACTIVE_DOC.uploadedBy || 'Faculty') + ' • Authenticated Official Copy';
  termBadge.textContent = ACTIVE_DOC.term || 'Official Document';

  const isPdf = (ACTIVE_DOC.fileType || '').toLowerCase().includes('pdf') || (ACTIVE_DOC.fileUrl || '').toLowerCase().endsWith('.pdf');
  typeBadge.textContent = isPdf ? 'PDF Document' : 'Image PNG';

  resetViewerZoom();

  if (isPdf) {
    if (imgBox) imgBox.classList.add('hidden');
    if (pdfBox) {
      pdfBox.classList.remove('hidden');
      pdfEl.src = ACTIVE_DOC.fileUrl + '#toolbar=0';
    }
  } else {
    if (pdfBox) {
      pdfBox.classList.add('hidden');
      pdfEl.src = '';
    }
    if (imgBox) {
      imgBox.classList.remove('hidden');
      imgEl.src = ACTIVE_DOC.fileUrl;
    }
  }

  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
  }
}

function closeDocumentViewer() {
  const modal = document.getElementById('resultViewerModal');
  const pdfEl = document.getElementById('viewerPdf');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
  if (pdfEl) pdfEl.src = '';
  document.body.classList.remove('modal-open');
  document.body.style.overflow = '';

  // Preserve scroll position
  if (typeof SAVED_SCROLL_POS === 'number') {
    window.scrollTo(0, SAVED_SCROLL_POS);
  }
}

function zoomViewer(delta) {
  CURRENT_ZOOM = Math.max(50, Math.min(250, CURRENT_ZOOM + delta));
  applyZoom();
}

function resetViewerZoom() {
  CURRENT_ZOOM = 100;
  applyZoom();
}

function applyZoom() {
  const img = document.getElementById('viewerImg');
  const label = document.getElementById('viewerZoomLabel');
  if (label) label.textContent = CURRENT_ZOOM + '%';
  if (img) {
    img.style.transform = `scale(${CURRENT_ZOOM / 100})`;
  }
}

function toggleViewerFullscreen() {
  const modalBox = document.querySelector('#resultViewerModal > div:last-child');
  if (!modalBox) return;
  const icon = document.getElementById('viewerFsIcon');

  if (!document.fullscreenElement) {
    if (modalBox.requestFullscreen) {
      modalBox.requestFullscreen();
    } else if (modalBox.webkitRequestFullscreen) {
      modalBox.webkitRequestFullscreen();
    }
    if (icon) icon.textContent = 'fullscreen_exit';
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
    if (icon) icon.textContent = 'fullscreen';
  }
}

document.addEventListener('fullscreenchange', () => {
  const icon = document.getElementById('viewerFsIcon');
  if (!document.fullscreenElement && icon) {
    icon.textContent = 'fullscreen';
  }
});

function downloadCurrentDocument() {
  if (!ACTIVE_DOC || !ACTIVE_DOC.fileUrl) return;
  const a = document.createElement('a');
  a.href = ACTIVE_DOC.fileUrl;
  a.download = ACTIVE_DOC.fileName || 'academic-document';
  a.target = '_blank';
  a.rel = 'noopener noreferrer';
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { if (a.parentNode) a.parentNode.removeChild(a); }, 150);
}

/* ═══════════════════════════════════════════════════════════════════
   RESULT NOTIFICATIONS INTEGRATION
   ═══════════════════════════════════════════════════════════════════ */
let isSubscribedSem2 = false;
function toggleResultNotification() {
  isSubscribedSem2 = !isSubscribedSem2;
  const btn = document.getElementById('btnNotifySem2');
  const icon = document.getElementById('iconNotifySem2');
  const text = document.getElementById('textNotifySem2');

  if (isSubscribedSem2) {
    btn.className = 'px-4 py-2 rounded-xl border border-forest-300 text-forest-800 font-normal bg-forest-50 flex items-center gap-1.5 transition-all text-xs cursor-pointer shadow-xs';
    icon.className = 'material-symbols-outlined text-[16px] text-forest-700';
    icon.textContent = 'check_circle';
    text.textContent = 'Subscribed';
    try {
      localStorage.setItem('ngis_notif_sub_sem2', '1');
    } catch (_) {}
    if (window.toast) window.toast('Subscribed to Semester 2 official publication notifications', 'success');
  } else {
    btn.className = 'px-4 py-2 rounded-xl border border-surface-border text-forest-800 font-normal bg-white hover:bg-surface-subtle flex items-center gap-1.5 transition-all text-xs shadow-xs cursor-pointer';
    icon.className = 'material-symbols-outlined text-[16px] text-forest-700';
    icon.textContent = 'notifications_active';
    text.textContent = 'Notify When Ready';
    try {
      localStorage.removeItem('ngis_notif_sub_sem2');
    } catch (_) {}
    if (window.toast) window.toast('Unsubscribed from Semester 2 notifications', 'info');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  loadStudentTranscripts();
  try {
    if (localStorage.getItem('ngis_notif_sub_sem2') === '1') {
      toggleResultNotification();
    }
  } catch (_) {}
});
</script>
</body>
</html>
'''

with open('pages/student/student-grades.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('Updated student-grades.html successfully. Length:', len(new_html))
