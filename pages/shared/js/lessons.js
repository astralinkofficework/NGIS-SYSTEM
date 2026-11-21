/* ══════════════════════════════════════
   NGIS Resource Library — lessons.js
   ══════════════════════════════════════ */

/* ── State ── */
var _previewSrc      = '';
var _previewName     = '';
var _currentType     = 'all';
var _currentSearch   = '';
var _currentName     = '';
var _activeId        = null;
var _currentResources = [];
var _currentSubjectId = '';

/* ════════════════════════════════════
   Type meta helpers
════════════════════════════════════ */
function isMobileLibraryView() {
  return window.matchMedia('(max-width: 640px)').matches;
}

/* ════════════════════════════════════
   STEP 1 — Subject Selection
════════════════════════════════════ */
function filterSubjects(q) {
  var cards = document.querySelectorAll('.subj-card');
  var empty = document.getElementById('subjEmptyState');
  var lower = (q || '').toLowerCase();
  var found = 0;
  cards.forEach(function(c){
    var match = !lower || c.dataset.name.toLowerCase().includes(lower);
    c.style.display = match ? '' : 'none';
    if (match) found++;
  });
  if (empty) empty.hidden = found > 0;
}

function openSubject(id, name, sub, icon, color, bg, teacher, subject, semester, dept, desc, count) {
  closeMobileSidebar();
  _currentSubjectId = id;
  _currentResources = RESOURCES[id] || [];
  _activeId         = null;
  _currentType      = 'all';
  _currentSearch    = '';
  _currentName      = '';

  document.getElementById('stepSubjects').hidden = true;
  document.getElementById('stepLibrary').hidden  = false;

  document.getElementById('libTitle').textContent = name;
  document.getElementById('libSub').textContent   = sub + ' · Teacher: ' + teacher;
  document.getElementById('teacherName').textContent    = teacher;
  document.getElementById('teacherDept').textContent    = dept;
  document.getElementById('panelTeacherName').textContent = teacher;
  document.getElementById('panelTeacherDept').textContent = dept;
  document.getElementById('siSubject').textContent  = subject || name;
  document.getElementById('siSemester').textContent = semester;
  document.getElementById('siDept').textContent     = dept;
  document.getElementById('siDesc').textContent     = desc;
  var ds = document.getElementById('detailSubject'), ds2 = document.getElementById('detailSemester');
  if (ds)  ds.textContent  = name;
  if (ds2) ds2.textContent = semester;

  var si = document.getElementById('sidebarSearch');
  if (si) si.value = '';

  /* reset tab */
  document.querySelectorAll('.lib-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.type === 'all');
  });

  buildSidebarList();
  renderFileList();
  showViewerPlaceholder();
}

function backToSubjects() {
  document.getElementById('stepLibrary').hidden  = true;
  document.getElementById('stepSubjects').hidden = false;
  document.getElementById('subjectSearch').value = '';
  filterSubjects('');
}

/* ════════════════════════════════════
   Sidebar — individual lesson names
════════════════════════════════════ */
function buildSidebarList() {
  var role      = (window.PAGE && window.PAGE.role) || 'student';
  var isTeacher = role === 'teacher' || role === 'admin';
  var label     = document.getElementById('sidebarListLabel');
  var list      = document.getElementById('folderList');
  if (!list) return;
  
  if (label) {
    label.innerHTML = '<div style="display:flex; align-items:center; gap:8px; font-weight: 400; color:var(--fg); font-size:15px; margin-bottom:12px;">'
      + '<span class="material-symbols-outlined" style="color:var(--accent); font-size:18px;">book</span>'
      + '<span>' + (isTeacher ? 'All Files' : 'All Lessons') + '</span>'
      + '<span class="tab-badge" style="background:var(--accent-light); color:var(--accent); margin-left:auto; font-size:11px; padding:2px 8px; border-radius:12px;">' + _currentResources.length + '</span>'
      + '</div>';
  }

  var html = '';

  _currentResources.forEach(function(r){
    var m = typeMeta(r.type);
    var fts = fileTypeStyle(r.fileType);
    
    // Custom tag format
    var typeTag = '<span class="px-2 py-0.5 text-[10px] font-normal rounded uppercase" style="background:' + fts.bg + '; color:' + fts.color + '">' + m.label.toUpperCase() + '</span>';
    var formatTag = '<span class="px-2 py-0.5 text-[10px] font-normal rounded uppercase text-white bg-accent-600">' + r.fileType.toUpperCase() + '</span>';
    
    // Custom detail or duration
    var detail = r.fileType === 'video' ? '15 min' : 'Updated ' + fmtDate(r.date);
    
    // Active class logic
    var activeClass = _activeId === r.id ? ' active' : '';

    html += '<button class="lib-folder-item' + activeClass + '" data-item-id="' + r.id + '" onclick="filterByItem(this,\'' + r.id + '\')" style="display:flex; flex-direction:column; align-items:flex-start; gap:8px; padding:16px; border:1px solid var(--border); border-radius:14px; background:#fff; margin-bottom:10px; width:100%; transition:all 0.2s ease; cursor:pointer; text-align:left;">'
      + '  <div style="font-size:14px; font-weight: 400; color:var(--fg); line-height:1.4; word-break:break-word;">' + escHtml(r.name) + '</div>'
      + '  <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; width:100%;">'
      + '    ' + formatTag
      + '    ' + typeTag
      + '    <span style="font-size:11px; color:var(--muted); margin-left:auto; font-weight: 400;">' + detail + '</span>'
      + '  </div>'
      + '</button>';
  });
  list.innerHTML = html;
}

function filterByItem(btn, itemId) {
  _currentName = itemId;
  document.querySelectorAll('.lib-folder-item').forEach(function(el){
    el.classList.toggle('active', el.dataset.itemId === itemId);
  });

  if (itemId) {
    /* find and open that resource directly in viewer */
    var r = _currentResources.find(function(x){ return x.id === itemId; });
    if (r) {
      openInViewer(r);
      if (isMobileLibraryView()) openPreview(r.name, r, r.src);
    }
    applyFilters();
  } else {
    showViewerPlaceholder();
    applyFilters();
  }
}

/* ════════════════════════════════════
   Render file list
════════════════════════════════════ */
function renderFileList() {
  var list = document.getElementById('resourceList');
  if (!list) return;
  var html = '';
  _currentResources.forEach(function(r){
    var m = typeMeta(r.type);
    html += '<div class="lib-file-row" data-type="' + r.type + '" data-name="' + escHtml(r.name.toLowerCase()) + '" data-id="' + r.id + '" data-date="' + r.date + '"'
      + ' onclick="selectFile(\'' + r.id + '\')" tabindex="0" role="button" aria-label="' + escHtml(r.name) + '">'
      + '<span class="lib-ftype-ico ' + m.cls + '">' + m.label.slice(0,4).toUpperCase() + '</span>'
      + '<div class="lib-file-row-body">'
      + '<div class="lib-file-row-name">' + escHtml(r.name) + '</div>'
      + '<div class="lib-file-row-sub">' + fmtDate(r.date) + (r.size !== '—' ? ' · ' + r.size : '') + (r.downloads ? ' · ' + r.downloads + ' downloads' : '') + '</div>'
      + '</div>'
      + '<div class="lib-file-row-tags">'
      + r.tags.slice(0,2).map(function(t){ return '<span class="lib-tag">' + t + '</span>'; }).join('')
      + '</div>'
      + '<div class="lib-file-row-actions" onclick="event.stopPropagation()">'
      /* Primary action: Preview (bi-eye via the shared engine). Rows are
         compact, so icon-only with a discoverable tooltip + accessible name. */
      + '<button class="icon-btn lib-preview-btn" title="Preview resource" aria-label="Preview ' + escHtml(r.name) + '" onclick="selectFile(\'' + r.id + '\')">'
      + '<span data-ngis-icon="view"></span></button>'
      /* Secondary: Save / bookmark (bi-bookmark, bi-bookmark-fill when saved). */
      + '<button class="icon-btn lib-bm-btn" title="Save resource" aria-label="Save ' + escHtml(r.name) + '" onclick="toggleBookmark(this)">'
      + '<span data-ngis-icon="bookmark"></span></button>'
      /* Secondary: Download — only offered when the resource is downloadable. */
      + (r.fileType !== 'link' && r.fileType !== 'video' ?
        '<button class="icon-btn" title="Download file" aria-label="Download ' + escHtml(r.name) + '" onclick="downloadFile(\'' + escAttr(r.src) + '\',\'' + escAttr(r.name) + '\')">'
        + '<span data-ngis-icon="download"></span></button>' : '')
      + '</div>'
      + '</div>';
  });
  list.innerHTML = html;

  /* keyboard support */
  list.querySelectorAll('.lib-file-row').forEach(function(row){
    row.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectFile(row.dataset.id); }
    });
  });
}

function selectFile(id) {
  _activeId = id;
  var r = _currentResources.find(function(x){ return x.id === id; });
  if (!r) return;

  /* highlight row */
  document.querySelectorAll('.lib-file-row').forEach(function(el){
    el.classList.toggle('active', el.dataset.id === id);
  });
  /* sync sidebar */
  document.querySelectorAll('.lib-folder-item').forEach(function(el){
    el.classList.toggle('active', el.dataset.itemId === id);
  });
  openInViewer(r);
  if (isMobileLibraryView()) openPreview(r.name, r, r.src);
}

/* ════════════════════════════════════
   Premium Resource Preview (rpv-*)
════════════════════════════════════ */

/* zoom / rotate state */
var _rpvZoom   = 100;
var _rpvRotate = 0;
var _rpvBm     = false;   /* bookmark state for current file */

/* ── Page data for inline lesson preview (resource m2) ── */
var LESSON_PAGES = [
  /* Page 1 */
  '<div class="page-content" id="page1">'
  + '  <div class="text-center mb-10">'
  + '    <div class="text-xs font-normal text-surface-400 uppercase tracking-widest mb-2">Grade 9 Mathematics</div>'
  + '    <h2 class="text-3xl font-normal text-surface-900 tracking-tight mb-1">Chapter 3</h2>'
  + '    <h3 class="text-xl font-normal text-accent-600">Linear Equations &amp; Inequalities</h3>'
  + '    <div class="w-16 h-1 bg-accent-500 rounded-full mx-auto mt-4" style="width: 64px; height: 4px; background: var(--accent); border-radius: 9999px; margin-left: auto; margin-right: auto; margin-top: 16px;"></div>'
  + '  </div>'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">3.1 What is a Linear Equation?</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      A <span>linear equation in one variable</span> is an equation that can be written in the form:'
  + '    </p>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-5 text-center mb-4" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:20px; text-align:center; margin-bottom:16px;">'
  + '      <span class="math-eq text-xl" style="font-size:20px; font-weight: 400;">ax + b = 0</span>'
  + '    </div>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      where <span class="math-eq">a</span> and <span class="math-eq">b</span> are real numbers and <span class="math-eq">a ≠ 0</span>. The solution is <span class="math-eq">x = −b/a</span>.'
  + '    </p>'
  + '  </div>'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">3.2 Solving Linear Equations</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-3" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:12px;">'
  + '      To solve a linear equation, isolate the variable on one side using inverse operations.'
  + '    </p>'
  + '    <div class="bg-accent-50 border border-accent-200 rounded-2xl p-5" style="background:var(--accent-light); border:1px solid #bbf7d0; border-radius:16px; padding:20px;">'
  + '      <div class="text-xs font-normal text-accent-700 uppercase tracking-wider mb-2" style="font-size:12px; font-weight: 400; color:var(--accent); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Example 1</div>'
  + '      <p class="text-sm text-surface-700 mb-2" style="font-size:14px; color:var(--fg); margin-bottom:8px;">Solve: <span class="math-eq">3x + 7 = 22</span></p>'
  + '      <div class="space-y-1.5 text-sm text-surface-600 pl-4 border-l-2 border-accent-200" style="display:flex; flex-direction:column; gap:6px; padding-left:16px; border-left:2px solid var(--accent); font-size:14px; color:var(--muted);">'
  + '        <p style="margin:0;"><span class="math-eq">3x = 22 − 7</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">3x = 15</span></p>'
  + '        <p style="margin:0;"><span class="math-eq font-normal text-accent-700" style="font-weight: 400; color:var(--accent);">x = 5</span></p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-6">'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-5" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:20px;">'
  + '      <div class="text-xs font-normal text-surface-500 uppercase tracking-wider mb-2" style="font-size:12px; font-weight: 400; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Example 2</div>'
  + '      <p class="text-sm text-surface-700 mb-2" style="font-size:14px; color:var(--fg); margin-bottom:8px;">Solve: <span class="math-eq">5(x − 2) = 3x + 6</span></p>'
  + '      <div class="space-y-1.5 text-sm text-surface-600 pl-4 border-l-2 border-surface-300" style="display:flex; flex-direction:column; gap:6px; padding-left:16px; border-left:2px solid var(--border); font-size:14px; color:var(--muted);">'
  + '        <p style="margin:0;"><span class="math-eq">5x − 10 = 3x + 6</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">5x − 3x = 6 + 10</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">2x = 16</span></p>'
  + '        <p style="margin:0;"><span class="math-eq font-normal text-accent-700" style="font-weight: 400; color:var(--accent);">x = 8</span></p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 2 */
  '<div class="page-content" id="page2">'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">3.3 Linear Inequalities</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      A <span>linear inequality</span> looks similar to a linear equation but uses inequality symbols instead of an equals sign:'
  + '    </p>'
  + '    <div class="grid grid-cols-2 gap-3 mb-5" style="display:grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px;">'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x &lt; a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Less than</div>'
  + '      </div>'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x ≤ a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Less than or equal</div>'
  + '      </div>'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x &gt; a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Greater than</div>'
  + '      </div>'
  + '      <div class="bg-surface-50 border border-surface-200 rounded-xl p-3 text-center" style="background:#fafafa; border:1px solid var(--border); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq text-lg" style="font-size:18px;">x ≥ a</span>'
  + '        <div class="text-xs text-surface-400 mt-1" style="font-size:12px; color:var(--muted); margin-top:4px;">Greater than or equal</div>'
  + '      </div>'
  + '    </div>'
  + '    <div class="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex gap-3" style="display:flex; gap:12px; align-items:flex-start; background:#fffbeb; border:1px solid #fef3c7; border-radius:16px; padding:16px;">'
  + '      <i class="fa-solid fa-triangle-exclamation text-amber-500 mt-0.5" style="color:#d97706; margin-top:2px;"></i>'
  + '      <p class="text-sm text-amber-800 leading-relaxed m-0" style="font-size:14px; color:#92400e; line-height:1.625; margin:0;">'
  + '        <span>Important:</span> When you multiply or divide both sides of an inequality by a negative number, you must <em>reverse</em> the inequality symbol.'
  + '      </p>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-8">'
  + '    <div class="bg-accent-50 border border-accent-200 rounded-2xl p-5" style="background:var(--accent-light); border:1px solid #bbf7d0; border-radius:16px; padding:20px;">'
  + '      <div class="text-xs font-normal text-accent-700 uppercase tracking-wider mb-2" style="font-size:12px; font-weight: 400; color:var(--accent); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Example 3</div>'
  + '      <p class="text-sm text-surface-700 mb-2" style="font-size:14px; color:var(--fg); margin-bottom:8px;">Solve: <span class="math-eq">−2x + 5 &gt; 11</span></p>'
  + '      <div class="space-y-1.5 text-sm text-surface-600 pl-4 border-l-2 border-accent-200" style="display:flex; flex-direction:column; gap:6px; padding-left:16px; border-left:2px solid var(--accent); font-size:14px; color:var(--muted);">'
  + '        <p style="margin:0;"><span class="math-eq">−2x &gt; 11 − 5</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">−2x &gt; 6</span></p>'
  + '        <p style="margin:0;"><span class="math-eq">x &lt; −3</span> <span class="text-xs text-amber-600" style="font-size:12px; color:#d97706;">(reversed sign)</span></p>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-6">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">3.4 Graphing Inequalities on a Number Line</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      To graph an inequality on a number line, use an open circle for strict inequalities (&lt;, &gt;) and a closed circle for inclusive inequalities (≤, ≥).'
  + '    </p>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-6" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:24px;">'
  + '      <div class="flex items-center justify-center gap-1 mb-2" style="display:flex; align-items:center; justify-content:center; gap:4px;">'
  + '        <div class="w-2 h-2 rounded-full border-2 border-accent-600 bg-white flex-shrink-0" style="width:8px; height:8px; border-radius:50%; border:2px solid var(--accent); background:#fff; flex-shrink:0;"></div>'
  + '        <div class="h-0.5 bg-surface-300 flex-1 relative" style="height:2px; background:#e5e5e5; flex:1; position:relative;">'
  + '          <div class="absolute left-0 top-1/2 -translate-y-1/2 w-[60%] h-0.5 bg-accent-500 rounded-full" style="position:absolute; left:0; top:50%; transform:translateY(-50%); width:60%; height:2px; background:var(--accent);"></div>'
  + '        </div>'
  + '        <div class="text-xs text-surface-400" style="font-size:12px; color:var(--muted);">5</div>'
  + '      </div>'
  + '      <p class="text-center text-sm text-surface-500 mt-2 m-0" style="text-align:center; font-size:14px; color:var(--muted); margin-top:8px; margin-bottom:0;"><span class="math-eq">x &lt; 5</span></p>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 3 */
  '<div class="page-content" id="page3">'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">3.5 Real-Life Applications</h4>'
  + '    <p class="text-[15px] text-surface-600 leading-relaxed mb-4" style="font-size:15px; color:var(--muted); line-height:1.625; margin-bottom:16px;">'
  + '      Linear equations and inequalities are used extensively in real-world problem solving. Below are some common scenarios:'
  + '    </p>'
  + '    <div class="bg-blue-50 border border-blue-200 rounded-2xl p-5 mb-5" style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:16px; padding:20px; margin-bottom:20px;">'
  + '      <div class="text-xs font-normal text-blue-700 uppercase tracking-wider mb-2" style="color:#1d4ed8; font-weight: 400; font-size:12px; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Application 1 — Budgeting</div>'
  + '      <p class="text-sm text-blue-900 mb-2" style="color:#1e3a8a; font-size:14px; margin-bottom:8px;">You have $50 to spend on notebooks and pens. Notebooks cost $8 each and pens cost $2 each. Write an inequality:</p>'
  + '      <div class="bg-white/60 rounded-xl p-3 text-center" style="background:rgba(255,255,255,0.6); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq">8n + 2p ≤ 50</span>'
  + '      </div>'
  + '    </div>'
  + '    <div class="bg-purple-50 border border-purple-200 rounded-2xl p-5 mb-5" style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:16px; padding:20px; margin-bottom:20px;">'
  + '      <div class="text-xs font-normal text-purple-700 uppercase tracking-wider mb-2" style="color:#7e22ce; font-weight: 400; font-size:12px; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Application 2 — Temperature</div>'
  + '      <p class="text-sm text-purple-900 mb-2" style="color:#581c87; font-size:14px; margin-bottom:8px;">Water boils at 100°C at standard pressure. The temperature <span class="math-eq">T</span> must satisfy:</p>'
  + '      <div class="bg-white/60 rounded-xl p-3 text-center" style="background:rgba(255,255,255,0.6); border-radius:12px; padding:12px; text-align:center;">'
  + '        <span class="math-eq">T ≥ 100°C</span> for boiling to occur'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mb-6">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">3.6 Word Problem Strategy</h4>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-5" style="background:#fafafa; border:1px solid var(--border); border-radius:16px; padding:20px;">'
  + '      <ol class="text-sm text-surface-600 space-y-2.5" style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">1</span><span>Read the problem carefully. Identify what is given and what is asked.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">2</span><span>Define a variable to represent the unknown quantity.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">3</span><span>Write an equation or inequality based on the relationships described.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">4</span><span>Solve the equation or inequality.</span></li>'
  + '        <li class="flex gap-3" style="display:flex; gap:12px; align-items:flex-start;"><span class="w-6 h-6 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:50%; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">5</span><span>Check your answer in the context of the problem.</span></li>'
  + '      </ol>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 4 */
  '<div class="page-content" id="page4">'
  + '  <div class="text-center mb-8">'
  + '    <h4 class="text-xl font-normal text-surface-900 mb-1" style="font-size:20px; font-weight: 400; color:var(--fg); margin-bottom:4px;">Practice Problems</h4>'
  + '    <p class="text-sm text-surface-400 m-0" style="font-size:14px; color:var(--muted); margin:0;">Solve each equation or inequality. Show all working.</p>'
  + '  </div>'
  + '  <div class="space-y-4" style="display:flex; flex-direction:column; gap:16px;">'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">1</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">7x − 3 = 4x + 12</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">2</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">2(3y − 1) = 5y + 7</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">3</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">−4x + 9 ≥ 21</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">4</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">3(m + 4) &lt; 2m − 1</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">5</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">(x + 2)/3 − (x − 1)/4 = 2</span></p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">6</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;">A taxi charges $3 plus $1.50 per kilometer. If a passenger has $24, what is the maximum distance they can travel?</p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">7</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;">The sum of two consecutive even numbers is 54. Find the numbers.</p>'
  + '    </div>'
  + '    <div class="bg-surface-50 border border-surface-200 rounded-2xl p-4 flex gap-4 items-start" style="display:flex; gap:16px; align-items:flex-start; padding:16px; background:#fafafa; border:1px solid var(--border); border-radius:16px;">'
  + '      <span class="w-8 h-8 rounded-xl bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-normal flex-shrink-0" style="width:32px; height:32px; border-radius:12px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:14px; font-weight: 400; flex-shrink:0;">8</span>'
  + '      <p class="text-sm text-surface-700 pt-1 m-0" style="font-size:14px; color:var(--fg); margin:0; padding-top:4px;"><span class="math-eq">5 − 3(2p + 1) ≤ 2p − 7</span></p>'
  + '    </div>'
  + '  </div>'
  + '</div>',

  /* Page 5 */
  '<div class="page-content" id="page5">'
  + '  <div class="mb-8">'
  + '    <h4 class="text-lg font-normal text-surface-900 mb-3" style="font-size:18px; font-weight: 400; color:var(--fg); margin-bottom:12px;">Answer Key</h4>'
  + '    <div class="space-y-3" style="display:flex; flex-direction:column; gap:12px;">'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">1</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">x = 5</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">2</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">y = 9</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">3</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">x ≤ −3</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">4</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">m &lt; −13</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">5</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">x = 26</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">6</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">14 km</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">7</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">26 and 28</span></span>'
  + '      </div>'
  + '      <div class="flex items-center gap-4 p-3 rounded-xl bg-accent-50/50" style="display:flex; gap:16px; align-items:center; padding:12px; background:rgba(240,253,244,0.5); border-radius:12px;">'
  + '        <span class="w-6 h-6 rounded-lg bg-accent-100 text-accent-700 flex items-center justify-center text-xs font-normal flex-shrink-0" style="width:24px; height:24px; border-radius:8px; background:var(--accent-light); color:var(--accent); display:flex; align-items:center; justify-content:center; font-size:12px; font-weight: 400; flex-shrink:0;">8</span>'
  + '        <span class="text-sm text-surface-700"><span class="math-eq">p ≥ 1</span></span>'
  + '      </div>'
  + '    </div>'
  + '  </div>'
  + '  <div class="mt-10 pt-6 border-t border-surface-200 text-center" style="margin-top:40px; padding-top:24px; border-top:1px solid #e5e5e5; text-align:center;">'
  + '    <p class="text-xs text-surface-400 m-0" style="font-size:12px; color:#a3a3a3; margin:0;">End of Chapter 3 — Linear Equations &amp; Inequalities</p>'
  + '    <p class="text-xs text-surface-300 mt-1 m-0" style="font-size:12px; color:#d4d4d4; margin-top:4px; margin-bottom:0;">Prepared by Mr. Chea Sophea | Academic Year 2025–2026</p>'
  + '  </div>'
  + '</div>'
];

/* ── Inline pager state (only used when lesson preview is active) ── */
var _lsnPage  = 1;
var _lsnTotal = 5;

function _lsnGoTo(page) {
  if (page < 1 || page > _lsnTotal) return;
  _lsnPage = page;
  var paper = document.getElementById('rpvFrameWrap');
  if (!paper) return;
  var el = paper.querySelector('.lesson-preview-paper');
  if (el) el.innerHTML = LESSON_PAGES[_lsnPage - 1];
  /* sync the main toolbar page indicator */
  var cur = document.getElementById('rpvPageCur');
  if (cur) cur.textContent = _lsnPage;
  /* highlight active thumbnail */
  paper.querySelectorAll('.lsn-thumb').forEach(function(t) {
    t.classList.toggle('active', parseInt(t.dataset.page) === _lsnPage);
  });
}

function buildLessonPreviewMarkup(r) {
  /* Works for any resource that has inline HTML pages defined.
     Falls back gracefully — callers already check r.id === 'm2' upstream
     but we keep the guard so this is safe to call generically. */
  _lsnPage  = 1;
  _lsnTotal = LESSON_PAGES.length;

  return '<div class="lesson-preview-shell" id="lsnShell">'
    + '<div class="lesson-preview-body">'
    + '<div class="lesson-preview-paper" id="lsnPaper">'
    + LESSON_PAGES[0]
    + '</div>'
    + '</div>'
    + '</div>';
}

function showViewerPlaceholder() {
  var ph = document.getElementById('viewerPlaceholder');
  var ws = document.getElementById('rpvWorkspace');
  if (ph) ph.hidden = false;
  if (ws) ws.hidden = true;
}

function openInViewer(r) {
  _previewSrc    = r.src;
  _previewName   = r.name;
  _rpvZoom       = 100;
  _rpvRotate     = 0;
  _rpvBm         = false;

  var ph = document.getElementById('viewerPlaceholder');
  var ws = document.getElementById('rpvWorkspace');
  if (ph) ph.hidden = true;
  if (ws) ws.hidden = false;

  var m   = typeMeta(r.type);
  var fts = fileTypeStyle(r.fileType);

  /* ── Card 1: Resource Info ── */
  var iconWrap = document.getElementById('rpvFileIconWrap');
  var icon     = document.getElementById('rpvFileIcon');
  var badge    = document.getElementById('rpvFtypeBadge');
  var resTitle = document.getElementById('rpvResTitle');
  var resDesc  = document.getElementById('rpvResDesc');
  var metaDate = document.getElementById('rpvMetaDate');
  var metaTch  = document.getElementById('rpvMetaTeacher');
  var metaSz   = document.getElementById('rpvMetaSize');
  var metaDl   = document.getElementById('rpvMetaDownloads');
  var tagsEl   = document.getElementById('rpvTags');
  var dlBtn    = document.getElementById('rpvDlBtn');
  var bmBtn    = document.getElementById('rpvBmBtn');
  var bmBarBtn = document.getElementById('rpvBmBarBtn');

  if (iconWrap) { iconWrap.style.background = fts.bg; iconWrap.style.border = 'none'; }
  if (icon)     { icon.textContent = fts.icon; icon.style.color = fts.color; }
  if (badge)    { badge.className = 'rpv-ftype-badge ' + fts.badge; badge.textContent = m.label.toUpperCase(); }
  if (resTitle) {
    resTitle.textContent = r.id === 'm2' ? 'Chapter 3 — Linear Equations & Inequalities' : r.name;
  }
  if (resDesc) {
    resDesc.textContent = r.id === 'm2' ? 'Introduction to solving linear equations and inequalities in one variable.' : getDesc(r);
  }
  if (metaDate) metaDate.textContent = fmtDate(r.date);
  if (metaTch) {
    var tname = document.getElementById('teacherName');
    metaTch.textContent = (tname && tname.textContent) ? tname.textContent : 'Teacher';
  }
  if (metaSz)   metaSz.textContent  = r.size !== '—' ? r.size : 'N/A';
  if (metaDl)   metaDl.textContent  = r.downloads ? r.downloads.toLocaleString() : '0';
  if (tagsEl)   tagsEl.innerHTML    = r.tags.map(function(t){ return '<span class="rpv-tag">' + escHtml(t) + '</span>'; }).join('');
  if (dlBtn)    dlBtn.style.display = r.fileType === 'link' ? 'none' : '';

  /* reset bookmark */
  _rpvBm = false;
  _rpvSyncBmBtns();

  /* thumbnail placeholder — show type icon */
  var thumbPh = document.getElementById('rpvThumbPlaceholder');
  if (thumbPh) {
    thumbPh.innerHTML = '<span class="material-symbols-outlined" style="font-size:48px;color:' + fts.color + ';font-variation-settings:\'FILL\' 1">' + fts.icon + '</span>';
    thumbPh.style.background = fts.bg;
  }

  /* ── Right Panel: Teacher/Resource Details Stats ── */
  var rightViews = document.getElementById('rpvRightViews');
  var rightDls = document.getElementById('rpvRightDownloads');
  var rightSize = document.getElementById('rpvRightSize');
  var rightRelated = document.getElementById('rpvRightRelated');
  
  if (rightViews) rightViews.textContent = r.downloads ? (r.downloads * 4 + 15).toLocaleString() : '12';
  if (rightDls) rightDls.textContent = r.downloads ? r.downloads.toLocaleString() : '0';
  if (rightSize) rightSize.textContent = r.size !== '—' ? r.size : 'N/A';
  
  if (rightRelated) {
    var rels = RES_RELATED[r.id] || [];
    if (rels.length === 0) {
      rightRelated.innerHTML = '<div style="font-size: 12px; color: var(--muted); text-align: center; padding: 24px 0;">No related resources found.</div>';
    } else {
      rightRelated.innerHTML = rels.slice(0, 4).map(function(a) {
        var cls = FILE_TYPE_ICO_CLASS[a.type] || 'pdf-ic';
        var lbl = FILE_TYPE_ICO_LABEL[a.type] || 'FILE';
        return '<div class="rpv-related-card" style="margin-bottom:8px">'
          + '<span class="rpv-rc-ico lib-ftype-ico ' + cls + '">' + lbl + '</span>'
          + '<div class="rpv-rc-name">' + escHtml(a.name) + '</div>'
          + '<div class="rpv-rc-sub">' + escHtml(a.size) + '</div>'
          + '</div>';
      }).join('');
    }
  }

  /* ── Card 2: Embedded Viewer ── */
  rpvZoomLabel();
  var frameWrap = document.getElementById('rpvFrameWrap');
  if (frameWrap) {
    var frameHtml = '';
    if (r.id === 'm2') {
      frameHtml = buildLessonPreviewMarkup(r);
    } else if (r.fileType === 'pdf') {
      frameHtml = '<iframe src="' + r.src + '#toolbar=0&view=FitH" title="' + escHtml(r.name) + '" loading="lazy" style="width:100%;min-height:520px;border:none;display:block"></iframe>';
    } else if (r.fileType === 'image') {
      frameHtml = '<div class="viewer-img-wrap" style="min-height:420px;background:#fff"><img src="' + r.src + '" alt="' + escHtml(r.name) + '"></div>';
    } else if (r.fileType === 'video') {
      frameHtml = '<div style="background:#000;display:flex;align-items:center;justify-content:center;min-height:420px">'
        + '<iframe src="' + r.src + '" title="' + escHtml(r.name) + '" allowfullscreen style="width:100%;aspect-ratio:16/9;border:none"></iframe></div>';
    } else if (r.fileType === 'link') {
      frameHtml = '<div class="viewer-link-wrap">'
        + '<span class="material-symbols-outlined" style="font-size:56px;color:' + fts.color + '">open_in_new</span>'
        + '<div class="viewer-link-name">' + escHtml(r.name) + '</div>'
        + '<p>This is an external resource that opens in a new tab.</p>'
        + '<a href="' + escHtml(r.src) + '" target="_blank" rel="noopener noreferrer" class="btn btn-primary">'
        + '<span data-ngis-icon="open"></span>Open Link</a>'
        + '</div>';
    }
    frameWrap.innerHTML = frameHtml;
  }

  /* ── Wire page indicator & toolbar prev/next for inline lesson preview ── */
  var pageCur   = document.getElementById('rpvPageCur');
  var pageTotal = document.getElementById('rpvPageTotal');
  if (r.id === 'm2') {
    _lsnPage  = 1;
    _lsnTotal = LESSON_PAGES.length;
    if (pageCur)   pageCur.textContent   = '1';
    if (pageTotal) pageTotal.textContent = String(_lsnTotal);
    /* wire the toolbar prev / next buttons (by position in toolbar) */
    var toolbar = document.querySelector('.rpv-embed-toolbar');
    if (toolbar) {
      var prevBtn = toolbar.querySelector('[aria-label="Previous page"]');
      var nextBtn = toolbar.querySelector('[aria-label="Next page"]');
      if (prevBtn) {
        prevBtn.onclick = function() {
          _lsnGoTo(_lsnPage - 1);
          var cur = document.getElementById('rpvPageCur');
          if (cur) cur.textContent = _lsnPage;
        };
      }
      if (nextBtn) {
        nextBtn.onclick = function() {
          _lsnGoTo(_lsnPage + 1);
          var cur = document.getElementById('rpvPageCur');
          if (cur) cur.textContent = _lsnPage;
        };
      }
    }
    /* keyboard left/right arrow support for inline pages */
    document._lsnKeyHandler && document.removeEventListener('keydown', document._lsnKeyHandler);
    document._lsnKeyHandler = function(e) {
      if (e.target.matches('input, textarea, select')) return;
      if (e.key === 'ArrowLeft')  { e.preventDefault(); _lsnGoTo(_lsnPage - 1); var c = document.getElementById('rpvPageCur'); if(c) c.textContent = _lsnPage; }
      if (e.key === 'ArrowRight') { e.preventDefault(); _lsnGoTo(_lsnPage + 1); var c = document.getElementById('rpvPageCur'); if(c) c.textContent = _lsnPage; }
    };
    document.addEventListener('keydown', document._lsnKeyHandler);
  } else {
    if (pageCur)   pageCur.textContent   = '1';
    if (pageTotal) pageTotal.textContent = '—';
    /* reset prev/next to no-ops for non-paginated resources */
    var toolbar2 = document.querySelector('.rpv-embed-toolbar');
    if (toolbar2) {
      var pb = toolbar2.querySelector('[aria-label="Previous page"]');
      var nb = toolbar2.querySelector('[aria-label="Next page"]');
      if (pb) pb.onclick = null;
      if (nb) nb.onclick = null;
    }
    document._lsnKeyHandler && document.removeEventListener('keydown', document._lsnKeyHandler);
    document._lsnKeyHandler = null;
  }

  /* ── Populate tabs for resource m2 ── */
  _rpvPopulateTabs(r);

  /* ── Card 3: Teacher notes (fallback for resources without tab data) ── */
  var notesTeacher = document.getElementById('rpvNotesTeacher');
  var notesAvatar  = document.getElementById('rpvNotesAvatar');
  var notesText    = document.getElementById('rpvNotesText');
  var tname2       = document.getElementById('teacherName');
  var tavatar      = document.getElementById('teacherAvatar');
  if (notesTeacher && tname2) notesTeacher.textContent = tname2.textContent;
  if (notesAvatar  && tavatar) notesAvatar.src = tavatar.src;
  /* only set notes text if _rpvPopulateTabs didn't already supply specific notes */
  if (notesText && !RES_NOTES[r.id]) notesText.textContent = getDesc(r);

  /* ── Card 3: Description tab ── */
  var descText = document.getElementById('rpvDescText');
  var descMeta = document.getElementById('rpvDescMeta');
  if (descText) {
    descText.textContent = r.id === 'm2' ? 'This chapter introduces the basic concepts of linear equations, solving methods, and real-life applications. Students will learn to identify, set up, and solve linear equations and inequalities in one variable.' : getDesc(r);
  }
  if (descMeta) {
    descMeta.innerHTML = r.id === 'm2'
      ? '<span class="lib-tag">#Algebra</span><span class="lib-tag">#Chapter3</span><span class="lib-tag">#Worksheet</span>'
      : r.tags.map(function(t){ return '<span class="lib-tag">' + escHtml(t) + '</span>'; }).join('');
  }

  /* reset tabs to Description */
  rpvSwitchTabById('description');
}

function expandViewer() {
  openPreview(_previewName, _currentResources.find(function(r){ return r.id === _activeId; }) || {}, _previewSrc);
}

/* ════════════════════════════════════
   Tab data for m2 (and any resource)
════════════════════════════════════ */
var RES_ATTACHMENTS = {
  m2: [
    { name:'Ch3_AnswerKey.pdf',        size:'245 KB',  type:'pdf'   },
    { name:'NumberLine_Diagrams.png',  size:'1.2 MB',  type:'image' },
    { name:'Ch3_Extra_Practice.docx',  size:'380 KB',  type:'word'  },
    { name:'Student_Scores_Ch3.xlsx',  size:'156 KB',  type:'excel' },
    { name:'Ch3_Lesson_Slides.pptx',   size:'4.7 MB',  type:'ppt'   }
  ]
};
var RES_RELATED = {
  m2: [
    { name:'Ch2_Polynomials.pdf',          size:'1.8 MB', type:'pdf'   },
    { name:'Ch4_Systems_Equations.pdf',    size:'2.3 MB', type:'pdf'   },
    { name:'Algebra_Formulas_Sheet.docx',  size:'520 KB', type:'word'  },
    { name:'Grade9_Progress_Tracker.xlsx', size:'890 KB', type:'excel' },
    { name:'Midterm_Review_Pack.pdf',      size:'3.1 MB', type:'pdf'   },
    { name:'Inequalities_Visual_Guide.pptx',size:'2.8 MB',type:'ppt'   },
    { name:'Ch1_Real_Numbers.pdf',         size:'1.5 MB', type:'pdf'   },
    { name:'Graph_Paper_Template.png',     size:'210 KB', type:'image' }
  ]
};
var RES_REFS = {
  m2: [
    { title:'Singapore Math — Secondary 2 Workbook',   detail:'Marshall Cavendish Education, 2024. Chapter 5: Linear Equations.' },
    { title:'Algebra I — Glencoe Mathematics',          detail:'McGraw-Hill, 2023. Pages 142–178.' },
    { title:'Khan Academy — Linear Equations & Inequalities', detail:'Online resource. Accessed June 2026.' },
    { title:'MoEYS Mathematics Curriculum — Grade 9',  detail:'Ministry of Education, Youth and Sport, Cambodia. 2025 Edition.' }
  ]
};
var RES_LINKS = {
  m2: [
    { name:'Khan Academy — Algebra Foundations', url:'https://www.khanacademy.org/math/algebra',   domain:'khanacademy.org' },
    { name:'GeoGebra — Interactive Graphing Tool', url:'https://www.geogebra.org',                domain:'geogebra.org'    }
  ]
};
var RES_NOTES = {
  m2: 'Lesson Pacing: Allocate 2 class periods (80 min total). Sections 3.1–3.2 in period 1, 3.3–3.4 in period 2. Practice problems can be assigned as homework.\n\nCommon Misconceptions: Students frequently forget to reverse the inequality sign when multiplying/dividing by a negative number. Emphasise this with multiple examples.\n\nAssessment: Short quiz (10 min) at start of next class covering 3.1–3.4. Chapter test scheduled for Week 8.'
};

var FILE_TYPE_ICO_CLASS = {
  pdf:'pdf-ic', word:'word-ic', excel:'xls-ic', ppt:'ppt-ic', image:'img-ic', video:'vid-ic', link:'link-ic'
};
var FILE_TYPE_ICO_LABEL = {
  pdf:'PDF', word:'DOC', excel:'XLS', ppt:'PPT', image:'IMG', video:'VID', link:'LINK'
};

function _rpvPopulateTabs(r) {
  /* ── Attachments ── */
  var attEmpty = document.getElementById('rpvAttachmentsEmpty');
  var attList  = document.getElementById('rpvAttachmentsList');
  var attBtn   = document.querySelector('.rpv-tab[data-tab="attachments"] .rpv-tab-count');
  var atts     = RES_ATTACHMENTS[r.id] || [];
  if (attEmpty) attEmpty.hidden = atts.length > 0;
  if (attList)  {
    attList.hidden = atts.length === 0;
    attList.innerHTML = atts.map(function(a) {
      var cls = FILE_TYPE_ICO_CLASS[a.type] || 'pdf-ic';
      var lbl = FILE_TYPE_ICO_LABEL[a.type] || 'FILE';
      return '<div class="rpv-attach-item">'
        + '<span class="lib-ftype-ico ' + cls + '" style="height:28px;line-height:28px">' + lbl + '</span>'
        + '<div class="rpv-attach-body"><div class="rpv-attach-name">' + escHtml(a.name) + '</div>'
        + '<div class="rpv-attach-sub">' + escHtml(a.size) + '</div></div>'
        + '<button class="rpv-tool-btn" style="width:28px;height:28px;color:var(--muted)" title="Download" aria-label="Download '+ escHtml(a.name) +'">'
        + '<span style="font-size:16px" data-ngis-icon="download"></span></button>'
        + '</div>';
    }).join('');
  }
  if (attBtn) attBtn.textContent = atts.length;

  /* ── Related Files ── */
  var relEmpty = document.getElementById('rpvRelatedEmpty');
  var relGrid  = document.getElementById('rpvRelatedGrid');
  var relBtn   = document.querySelector('.rpv-tab[data-tab="related"] .rpv-tab-count');
  var rels     = RES_RELATED[r.id] || [];
  if (relEmpty) relEmpty.hidden = rels.length > 0;
  if (relGrid)  {
    relGrid.hidden = rels.length === 0;
    relGrid.innerHTML = rels.map(function(a) {
      var cls = FILE_TYPE_ICO_CLASS[a.type] || 'pdf-ic';
      var lbl = FILE_TYPE_ICO_LABEL[a.type] || 'FILE';
      return '<div class="rpv-related-card">'
        + '<span class="rpv-rc-ico lib-ftype-ico ' + cls + '">' + lbl + '</span>'
        + '<div class="rpv-rc-name">' + escHtml(a.name) + '</div>'
        + '<div class="rpv-rc-sub">' + escHtml(a.size) + '</div>'
        + '</div>';
    }).join('');
  }
  if (relBtn) relBtn.textContent = rels.length;

  /* ── References ── */
  var refsEmpty = document.getElementById('rpvRefsEmpty');
  var refsList  = document.getElementById('rpvRefsList');
  var refs      = RES_REFS[r.id] || [];
  if (refsEmpty) refsEmpty.hidden = refs.length > 0;
  if (refsList) {
    refsList.hidden = refs.length === 0;
    refsList.innerHTML = refs.map(function(ref, i) {
      return '<li>'
        + '<span class="material-symbols-outlined">link</span>'
        + '<div><span style="font-size:13px;color:var(--heading)">' + escHtml(ref.title) + '</span>'
        + '<div style="font-size:11px;color:var(--faint);margin-top:2px">' + escHtml(ref.detail) + '</div></div>'
        + '</li>';
    }).join('');
  }

  /* ── External Links ── */
  var linksEmpty = document.getElementById('rpvLinksEmpty');
  var linksList  = document.getElementById('rpvLinksList');
  var linksBtn   = document.querySelector('.rpv-tab[data-tab="links"] .rpv-tab-count');
  var links      = RES_LINKS[r.id] || [];
  if (linksEmpty) linksEmpty.hidden = links.length > 0;
  if (linksList) {
    linksList.hidden = links.length === 0;
    linksList.innerHTML = links.map(function(lnk) {
      return '<a href="' + escHtml(lnk.url) + '" target="_blank" rel="noopener noreferrer" class="rpv-ext-link">'
        + '<div class="rpv-ext-ico"><span class="material-symbols-outlined">open_in_new</span></div>'
        + '<div class="rpv-ext-body">'
        + '<div class="rpv-ext-name">' + escHtml(lnk.name) + '</div>'
        + '<div class="rpv-ext-url">' + escHtml(lnk.domain) + '</div>'
        + '</div>'
        + '<span class="rpv-ext-arrow" data-ngis-icon="chevronRight"></span>'
        + '</a>';
    }).join('');
  }
  if (linksBtn) linksBtn.textContent = links.length;

  /* ── Teacher notes ── */
  var notesText = document.getElementById('rpvNotesText');
  var noteDate  = document.getElementById('rpvNotesDate');
  if (notesText) notesText.textContent = RES_NOTES[r.id] || getDesc(r);
  if (noteDate) {
    var tname3 = document.getElementById('teacherName');
    noteDate.textContent = 'Posted by ' + ((tname3 && tname3.textContent) ? tname3.textContent : 'Teacher');
  }
}

/* ── Zoom ── */
function rpvZoom(delta) {
  _rpvZoom = Math.min(200, Math.max(50, _rpvZoom + delta));
  rpvZoomLabel();
  /* target the inline lesson paper if active, else the rpvPaper wrapper */
  var target = document.getElementById('lsnPaper') || document.getElementById('rpvPaper');
  if (target) {
    target.style.transformOrigin = 'top center';
    target.style.transform = 'scale(' + (_rpvZoom / 100) + ') rotate(' + _rpvRotate + 'deg)';
  }
}
function rpvZoomLabel() {
  var lbl = document.getElementById('rpvZoomLabel');
  if (lbl) lbl.textContent = _rpvZoom + '%';
}

/* ── Rotate ── */
function rpvRotate() {
  _rpvRotate = (_rpvRotate + 90) % 360;
  var target = document.getElementById('lsnPaper') || document.getElementById('rpvPaper');
  if (target) {
    target.style.transformOrigin = 'top center';
    target.style.transform = 'scale(' + (_rpvZoom / 100) + ') rotate(' + _rpvRotate + 'deg)';
  }
}

/* ── Bookmark (preview panel) ── */
function _rpvSyncBmBtns() {
  var bmBtn    = document.getElementById('rpvBmBtn');
  var bmBarBtn = document.getElementById('rpvBmBarBtn');
  [bmBtn, bmBarBtn].forEach(function(btn) {
    if (!btn) return;
    var ico = btn.querySelector('[data-ngis-icon]');
    if (ico) ico.setAttribute('data-ngis-icon', _rpvBm ? 'bookmarkAdded' : 'bookmark');
    btn.classList.toggle('bookmarked', _rpvBm);
    if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(btn);
  });
}
function togglePreviewBookmark() {
  _rpvBm = !_rpvBm;
  _rpvSyncBmBtns();
  /* also sync the row bookmark btn if available */
  if (_activeId) {
    var row = document.querySelector('.lib-file-row[data-id="' + _activeId + '"] .lib-bm-btn');
    if (row) {
      var ico = row.querySelector('[data-ngis-icon]');
      if (ico) ico.setAttribute('data-ngis-icon', _rpvBm ? 'bookmarkAdded' : 'bookmark');
      row.classList.toggle('bookmarked', _rpvBm);
      if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(row);
    }
  }
}

/* ── Tab switching ── */
function rpvSwitchTab(btn, tabId) {
  document.querySelectorAll('.rpv-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.tab === tabId);
    el.setAttribute('aria-selected', el.dataset.tab === tabId ? 'true' : 'false');
  });
  document.querySelectorAll('.rpv-tab-pane').forEach(function(el){
    el.classList.toggle('active', el.id === 'rpv-tab-' + tabId);
  });
}
function rpvSwitchTabById(tabId) {
  document.querySelectorAll('.rpv-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.tab === tabId);
    el.setAttribute('aria-selected', el.dataset.tab === tabId ? 'true' : 'false');
  });
  document.querySelectorAll('.rpv-tab-pane').forEach(function(el){
    el.classList.toggle('active', el.id === 'rpv-tab-' + tabId);
  });
}

/* ════════════════════════════════════
   Filtering & Search
════════════════════════════════════ */
function filterType(btn, type) {
  _currentType = type;
  _currentName = '';
  _activeId    = null;
  document.querySelectorAll('.lib-tab').forEach(function(el){
    el.classList.toggle('active', el.dataset.type === type);
  });
  document.querySelectorAll('.lib-folder-item').forEach(function(el){
    el.classList.toggle('active', el.dataset.itemId === '');
  });
  showViewerPlaceholder();
  applyFilters();
}

function searchResources(q) {
  _currentSearch = (q || '').toLowerCase();
  applyFilters();
}

function sortResources(value) {
  var list = document.getElementById('resourceList');
  if (!list) return;
  var rows = Array.from(list.querySelectorAll('.lib-file-row'));
  rows.sort(function(a,b){
    if (value === 'name')   return (a.dataset.name||'').localeCompare(b.dataset.name||'');
    var da = new Date(a.dataset.date||0), db = new Date(b.dataset.date||0);
    return value === 'newest' ? db - da : da - db;
  });
  rows.forEach(function(r){ list.appendChild(r); });
}

function applyFilters() {
  var rows  = document.querySelectorAll('#resourceList .lib-file-row');
  var empty = document.getElementById('resourceEmpty');
  var vis   = 0;
  rows.forEach(function(el){
    var typeOk   = _currentType === 'all' || el.dataset.type === _currentType;
    var nameOk   = !_currentSearch || (el.dataset.name||'').includes(_currentSearch);
    var itemOk   = !_currentName   || el.dataset.id === _currentName;
    var show     = typeOk && nameOk && itemOk;
    el.style.display = show ? '' : 'none';
    if (show) vis++;
  });
  if (empty) empty.hidden = vis > 0;
}

/* ════════════════════════════════════
   Bookmark
════════════════════════════════════ */
function toggleBookmark(btn) {
  var active = btn.classList.toggle('bookmarked');
  var ico = btn.querySelector('[data-ngis-icon]');
  if (ico) ico.setAttribute('data-ngis-icon', active ? 'bookmarkAdded' : 'bookmark');
  if (window.NGIS && window.NGIS.hydrate) window.NGIS.hydrate(btn);
}

/* ════════════════════════════════════
   Copy link / Download
════════════════════════════════════ */
function copyLink(btn) {
  navigator.clipboard && navigator.clipboard.writeText(window.location.href);
  var ico = btn && btn.querySelector('.material-symbols-outlined');
  if (ico) { ico.textContent='check'; setTimeout(function(){ ico.textContent='link'; },1800); }
}
function copyLinkGeneric() { navigator.clipboard && navigator.clipboard.writeText(window.location.href); }
function downloadPreview() { downloadFile(_previewSrc, _previewName); }
function downloadFile(src, name) {
  if (!src) return;
  var a = document.createElement('a');
  a.href=src; a.download=name||'download'; a.target='_blank'; a.rel='noopener';
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
}

/* ════════════════════════════════════
   Mobile sidebar
════════════════════════════════════ */
function toggleMobileSidebar() {
  var sb=document.getElementById('libSidebar'), scrim=document.getElementById('libScrim');
  if (!sb) return;
  var open=sb.classList.toggle('open');
  if (scrim) scrim.classList.toggle('show',open);
  document.body.style.overflow = open ? 'hidden' : '';
}
function closeMobileSidebar() {
  var sb=document.getElementById('libSidebar'), scrim=document.getElementById('libScrim');
  if (sb) sb.classList.remove('open');
  if (scrim) scrim.classList.remove('show');
  document.body.style.overflow='';
}

/* ════════════════════════════════════
   Full-screen Preview Modal
════════════════════════════════════ */
function openPreview(name, rOrObj, src) {
  var r = (typeof rOrObj === 'object' && rOrObj.fileType) ? rOrObj
        : (_currentResources.find(function(x){ return x.id === _activeId; }) || { fileType:'pdf' });
  _previewSrc  = src  || _previewSrc;
  _previewName = name || _previewName;

  document.getElementById('previewTitle').textContent = _previewName;
  var icon = document.getElementById('previewTypeIcon');
  var sub  = document.getElementById('previewType');
  var body = document.getElementById('previewBody');
  var m    = typeMeta(r.type || 'lesson');
  if (icon) icon.textContent = m.mdIcon;
  if (sub)  sub.textContent  = m.label;

  if (r.fileType === 'pdf' || !r.fileType) {
    body.innerHTML = '<iframe src="' + _previewSrc + '#toolbar=1&view=FitH" title="' + escHtml(_previewName) + '"></iframe>';
  } else if (r.fileType === 'image') {
    body.innerHTML = '<div class="preview-img-wrap"><img src="' + _previewSrc + '" alt="' + escHtml(_previewName) + '"></div>';
  } else if (r.fileType === 'video') {
    body.innerHTML = '<div style="flex:1;display:flex;align-items:center;justify-content:center;padding:24px;background:var(--surface-2)">'
      + '<iframe src="' + _previewSrc + '" allowfullscreen style="width:100%;aspect-ratio:16/9;border:none;border-radius:10px"></iframe></div>';
  } else {
    body.innerHTML = '<div class="lib-empty" style="flex:1;height:100%">'
      + '<span class="material-symbols-outlined">open_in_new</span>'
      + '<h4>' + escHtml(_previewName) + '</h4>'
      + '<a href="' + _previewSrc + '" target="_blank" rel="noopener" class="btn btn-primary" style="margin-top:16px">'
      + '<span data-ngis-icon="open"></span>Open Link</a></div>';
  }

  document.getElementById('previewModal').hidden = false;
  document.body.style.overflow = 'hidden';
}

function closePreview() {
  document.getElementById('previewModal').hidden = true;
  document.body.style.overflow = '';
  document.getElementById('previewBody').innerHTML = '';
}

var pm = document.getElementById('previewModal');
if (pm) {
  pm.addEventListener('click', function(e){
    if (e.target === this) closePreview();
  });
}
document.addEventListener('keydown', function(e){
  if (e.key === 'Escape') {
    closePreview();
    oakClosePreview();
    oakCloseQuiz();
  }
});

/* no-op for removed view toggle — kept so any stray refs don't error */
function setView(){}

function toggleDetailsPanel() {
  var ws = document.querySelector('.lib-workspace');
  var btn = document.getElementById('toggleDetailsBtn');
  var icon = document.getElementById('toggleDetailsIcon');
  if (ws) {
    var isCollapsed = ws.classList.toggle('right-collapsed');
    if (btn) {
      btn.title = isCollapsed ? "Show details panel" : "Hide details panel";
    }
    if (icon) {
      if (isCollapsed) {
        icon.className = 'fa-solid fa-angles-left';
      } else {
        icon.className = 'fa-solid fa-angles-right';
      }
    }
  }
}

/* ══════════════════════════════════════════════════════════════
   OAKHAVEN / NGIS LESSON LIBRARY CONTROLLER
   ══════════════════════════════════════════════════════════════ */
var _oakCurrentSubject = 'math';
var _oakCurrentTab = 'all';
var _oakCurrentSearch = '';
var _oakCurrentView = 'grid';
var _oakSortDesc = true;
var _oakBookmarkedIds = {};

function oakInit() {
  var params = new URLSearchParams(window.location.search);
  var subjParam = params.get('subject') || params.get('dept');
  if (subjParam && RESOURCES[subjParam]) {
    _oakCurrentSubject = subjParam;
  }
  oakSwitchSubject(_oakCurrentSubject);
}

function oakSwitchSubject(subjId) {
  _oakCurrentSubject = subjId || 'math';
  _currentSubjectId = _oakCurrentSubject;
  var rawTitle = OAK_SUBJECT_TITLES[_oakCurrentSubject] || _oakCurrentSubject.toUpperCase();
  var libTitle = rawTitle.split(' ').map(function(w){ return w.charAt(0) + w.slice(1).toLowerCase(); }).join(' ') + ' Library';

  var titleEl = document.getElementById('curSubjName');
  if (titleEl) {
    titleEl.textContent = rawTitle;
  }
  var icoEl = document.getElementById('curSubjIcon');
  if (icoEl && OAK_SUBJECT_ICONS[_oakCurrentSubject]) {
    icoEl.textContent = OAK_SUBJECT_ICONS[_oakCurrentSubject].icon;
    icoEl.style.color = OAK_SUBJECT_ICONS[_oakCurrentSubject].color;
  }
  var htbCrumb = document.querySelector('.htb-crumb-cur');
  if (htbCrumb) {
    htbCrumb.textContent = libTitle;
  }
  var heroTitle = document.querySelector('#heroBanner .hero-title, #heroBanner h1');
  if (heroTitle) {
    heroTitle.textContent = libTitle;
  }
  document.title = 'NGIS — ' + libTitle;

  try {
    var u = new URL(window.location.href);
    u.searchParams.set('dept', _oakCurrentSubject);
    window.history.replaceState({}, '', u.toString());
  } catch(e) {}

  document.querySelectorAll('.oak-subj-item').forEach(function(el) {
    el.classList.toggle('active', el.getAttribute('onclick') && el.getAttribute('onclick').includes("'" + _oakCurrentSubject + "'"));
  });
  var dd = document.getElementById('oakSubjDropdown');
  if (dd) dd.classList.remove('show');

  var searchInput = document.getElementById('oakFilterInput');
  if (searchInput) searchInput.value = '';
  _oakCurrentSearch = '';

  oakRenderCards();
}

function oakToggleSubjDropdown(e) {
  if (e && e.stopPropagation) e.stopPropagation();
  var dd = document.getElementById('oakSubjDropdown');
  if (dd) dd.classList.toggle('show');
}
document.addEventListener('click', function(e) {
  var crumb = document.getElementById('curSubjBreadcrumb');
  var dd = document.getElementById('oakSubjDropdown');
  if (dd && dd.classList.contains('show')) {
    if (crumb && !crumb.contains(e.target) && !dd.contains(e.target)) {
      dd.classList.remove('show');
    }
  }
});

function oakFilterTab(tabName) {
  _oakCurrentTab = tabName;
  document.querySelectorAll('.oak-tab-btn').forEach(function(btn) {
    btn.classList.remove('active');
    btn.setAttribute('aria-selected', 'false');
  });
  var activeBtn = document.getElementById('tab' + tabName.charAt(0).toUpperCase() + tabName.slice(1));
  if (activeBtn) {
    activeBtn.classList.add('active');
    activeBtn.setAttribute('aria-selected', 'true');
  }
  oakRenderCards();
}

function oakSearchResources(query) {
  _oakCurrentSearch = (query || '').toLowerCase().trim();
  oakRenderCards();
}

function oakGlobalSearch(query) {
  _oakCurrentSearch = (query || '').toLowerCase().trim();
  var filterInput = document.getElementById('oakFilterInput');
  if (filterInput) filterInput.value = query;
  oakRenderCards();
}

function oakSetView(mode) {
  _oakCurrentView = mode;
  var gridBtn = document.getElementById('oakViewGridBtn');
  var listBtn = document.getElementById('oakViewListBtn');
  var gridEl = document.getElementById('resourceGrid');
  var listEl = document.getElementById('resourceList');

  if (gridBtn) gridBtn.classList.toggle('active', mode === 'grid');
  if (listBtn) listBtn.classList.toggle('active', mode === 'list');

  if (gridEl) gridEl.style.display = mode === 'grid' ? 'grid' : 'none';
  if (listEl) listEl.style.display = mode === 'list' ? 'flex' : 'none';
}

var _oakSortActive = false;
var _oakSortDesc = true;

function oakToggleSort() {
  _oakSortActive = true;
  _oakSortDesc = !_oakSortDesc;
  var btn = document.getElementById('oakSortBtn');
  if (btn) {
    var label = btn.querySelector('span');
    if (label) label.textContent = _oakSortDesc ? 'Sort by Date' : 'Sort by Date (Oldest)';
  }
  oakRenderCards();
}

function oakRenderCards() {
  var rawList = RESOURCES[_oakCurrentSubject] || [];
  var filtered = rawList.filter(function(r) {
    if (_oakCurrentTab === 'documents') {
      if (r.type !== 'lesson' && r.type !== 'exam') return false;
    } else if (_oakCurrentTab === 'worksheets') {
      if (r.type !== 'worksheet') return false;
    } else if (_oakCurrentTab === 'notes') {
      if (r.type !== 'formula' && r.type !== 'note') return false;
    }
    if (_oakCurrentSearch) {
      var matchName = (r.name || '').toLowerCase().includes(_oakCurrentSearch);
      var matchFull = (r.fullName || '').toLowerCase().includes(_oakCurrentSearch);
      var matchTopic = (r.topic || '').toLowerCase().includes(_oakCurrentSearch);
      var matchDesc = (r.desc || '').toLowerCase().includes(_oakCurrentSearch);
      var matchTags = (r.tags || []).some(function(t) { return t.toLowerCase().includes(_oakCurrentSearch); });
      if (!matchName && !matchFull && !matchTopic && !matchDesc && !matchTags) return false;
    }
    return true;
  });

  if (_oakSortActive) {
    filtered.sort(function(a, b) {
      var da = new Date(a.date || '2026-01-01').getTime();
      var db = new Date(b.date || '2026-01-01').getTime();
      return _oakSortDesc ? db - da : da - db;
    });
  }

  var countEl = document.getElementById('oakResCount');
  if (countEl) countEl.textContent = filtered.length;

  var gridEl = document.getElementById('resourceGrid');
  var listEl = document.getElementById('resourceList');
  var emptyEl = document.getElementById('resourceEmpty');

  if (filtered.length === 0) {
    if (gridEl) gridEl.innerHTML = '';
    if (listEl) listEl.innerHTML = '';
    if (emptyEl) emptyEl.style.display = 'block';
    return;
  }
  if (emptyEl) emptyEl.style.display = 'none';

  if (gridEl) {
    var gridHtml = '';
    filtered.forEach(function(r) {
      var isQuiz = !!r.isQuiz;
      var tone = r.tone || 'tone-blue';
      var formulasText = Array.isArray(r.formulas) ? r.formulas.join('\n') : (r.formulas || '');
      var topicText = r.topic || 'Resource';
      var badgeHtml = '';
      if (r.badge && r.badge !== topicText) {
        badgeHtml = '<span class="oak-badge-pill ' + (r.badgeClass || 'pill-green') + '">' + escHtml(r.badge) + '</span>';
      }
      var isBookmarked = NGISBookmarks.has(r.id);
      var bookmarkedClass = isBookmarked ? ' active' : '';

      /* Primary action: opens the dedicated lesson page. Independent actions
         (bookmark / download / quiz) stop propagation so they never trigger
         card navigation. */
      var actionBtnHtml = isQuiz
        ? '<button class="oak-btn-quiz" onclick="event.stopPropagation(); oakOpenQuiz(\'' + r.id + '\')"><span data-ngis-icon="play"></span> Start Quiz</button>'
        : '<button class="oak-btn-view" onclick="event.stopPropagation(); oakOpenLesson(\'' + r.id + '\')"><span data-ngis-icon="book"></span> View Lesson</button>';

      var iconBadgeHtml = isQuiz
        ? '<div class="oak-banner-icon-badge type-quiz"><span class="material-symbols-outlined">task_alt</span></div>'
        : '<div class="oak-banner-icon-badge type-pdf"><span class="material-symbols-outlined">picture_as_pdf</span></div>';

      /* Truthful file information — only fields that exist in the data model */
      var metaBits = [typeMeta(r.type).label];
      if (r.pages) metaBits.push(r.pages + ' pages');
      if (r.size && r.size !== '—') metaBits.push(r.size);
      var metaText = metaBits.join(' • ');

      var downloadBtnHtml = (r.fileType !== 'link' && r.fileType !== 'video')
        ? '<button class="oak-icon-action" title="Download file" aria-label="Download ' + escHtml(r.name) + '" onclick="event.stopPropagation(); oakDownload(\'' + r.id + '\')">'
          + '<span data-ngis-icon="download"></span>'
          + '</button>'
        : '';

      gridHtml += '<article class="oak-card oak-card-clickable" data-id="' + r.id + '" role="button" tabindex="0"'
        + ' aria-label="Open ' + escHtml(r.fullName || r.name) + '"'
        + ' onclick="oakCardNavigate(event,\'' + r.id + '\')"'
        + ' onkeydown="oakCardKeydown(event,\'' + r.id + '\')">'
        + '  <div class="oak-card-banner ' + tone + '">'
        + '    <div class="oak-banner-top">'
        + '      ' + iconBadgeHtml
        + '      <div class="oak-banner-formulas">' + escHtml(formulasText) + '</div>'
        + '    </div>'
        + '    <div class="oak-banner-bottom">'
        + '      <span class="oak-topic-pill">' + escHtml(topicText) + '</span>'
        + '      ' + badgeHtml
        + '    </div>'
        + '  </div>'
        + '  <div class="oak-card-body">'
        + '    <div class="oak-card-metarow">'
        + '      <span class="oak-card-pages">' + escHtml(metaText) + '</span>'
        + (r.readTime ? '<span class="oak-card-time">' + escHtml(r.readTime) + '</span>' : '')
        + '    </div>'
        + '    <h3 class="oak-card-title">' + escHtml(r.fullName || r.name) + '</h3>'
        + '    <p class="oak-card-desc">' + escHtml(r.desc || '') + '</p>'
        + '    <div class="oak-card-actions">'
        + '      ' + actionBtnHtml
        + '      <div class="oak-act-icons">'
        + '        <button class="oak-icon-action' + bookmarkedClass + '" title="Save resource" aria-label="Save ' + escHtml(r.name) + '" onclick="event.stopPropagation(); oakToggleBookmark(this,\'' + r.id + '\')">'
        + '          <span data-ngis-icon="' + (isBookmarked ? 'bookmarkAdded' : 'bookmark') + '"></span>'
        + '        </button>'
        + '        ' + downloadBtnHtml
        + '      </div>'
        + '    </div>'
        + '  </div>'
        + '</article>';
    });
    gridEl.innerHTML = gridHtml;
  }

  if (listEl) {
    var listHtml = '';
    filtered.forEach(function(r) {
      var isQuiz = !!r.isQuiz;
      var isBookmarked = NGISBookmarks.has(r.id);
      var bookmarkedClass = isBookmarked ? ' active' : '';

      var metaBits = [typeMeta(r.type).label];
      if (r.pages) metaBits.push(r.pages + ' pages');
      if (r.size && r.size !== '—') metaBits.push(r.size);
      var metaText = metaBits.join(' • ');

      var downloadBtnHtml = (r.fileType !== 'link' && r.fileType !== 'video')
        ? '<button class="oak-icon-action" title="Download file" aria-label="Download ' + escHtml(r.name) + '" onclick="event.stopPropagation(); oakDownload(\'' + r.id + '\')">'
          + '<span data-ngis-icon="download"></span>'
          + '</button>'
        : '';

      listHtml += '<article class="oak-list-row oak-card-clickable" role="button" tabindex="0"'
        + ' aria-label="Open ' + escHtml(r.fullName || r.name) + '"'
        + ' onclick="oakCardNavigate(event,\'' + r.id + '\')"'
        + ' onkeydown="oakCardKeydown(event,\'' + r.id + '\')">'
        + '  <div class="oak-list-left">'
        + '    <div class="oak-banner-icon-badge ' + (isQuiz ? 'type-quiz' : 'type-pdf') + '">'
        + '      <span class="material-symbols-outlined">' + (isQuiz ? 'task_alt' : 'picture_as_pdf') + '</span>'
        + '    </div>'
        + '    <div class="oak-list-title-wrap">'
        + '      <div class="oak-list-title">' + escHtml(r.fullName || r.name) + '</div>'
        + '      <div class="oak-list-sub">'
        + '        <span>' + escHtml(metaText) + '</span>'
        + (r.readTime ? '<span>•</span><span>' + escHtml(r.readTime) + '</span>' : '')
        + '        <span>•</span>'
        + '        <span class="oak-topic-pill" style="font-size:10.5px; padding:1px 8px;">' + escHtml(r.topic || 'Resource') + '</span>'
        + '      </div>'
        + '    </div>'
        + '  </div>'
        + '  <div class="oak-list-right">'
        + (isQuiz ? '<button class="oak-btn-quiz" onclick="event.stopPropagation(); oakOpenQuiz(\'' + r.id + '\')"><span data-ngis-icon="play"></span> Start Quiz</button>'
                 : '<button class="oak-btn-view" onclick="event.stopPropagation(); oakOpenLesson(\'' + r.id + '\')"><span data-ngis-icon="book"></span> View Lesson</button>')
        + '    <button class="oak-icon-action' + bookmarkedClass + '" title="Save resource" aria-label="Save ' + escHtml(r.name) + '" onclick="event.stopPropagation(); oakToggleBookmark(this,\'' + r.id + '\')">'
        + '      <span data-ngis-icon="' + (isBookmarked ? 'bookmarkAdded' : 'bookmark') + '"></span>'
        + '    </button>'
        + '    ' + downloadBtnHtml
        + '  </div>'
        + '</article>';
    });
    listEl.innerHTML = listHtml;
  }
}

/* ════════════════════════════════════
   Dedicated lesson page navigation
════════════════════════════════════ */
function oakOpenLesson(resId) {
  var rawList = RESOURCES[_oakCurrentSubject] || [];
  var r = rawList.find(function(x) { return x.id === resId; });
  if (!r) return;
  var role = (window.PAGE && window.PAGE.role) || 'student';
  window.location.href = lessonDetailsUrl(resId, _oakCurrentSubject, role);
}

/* Whole-card click → lesson page. Interactive controls (buttons, links)
   and text selections inside the card are excluded from navigation. */
function oakCardNavigate(e, resId) {
  if (e.target.closest && e.target.closest('button, a, input, select, textarea')) return;
  try {
    var sel = window.getSelection();
    if (sel && String(sel).length > 0) return;
  } catch (err) {}
  oakOpenLesson(resId);
}

/* Keyboard activation for the clickable card */
function oakCardKeydown(e, resId) {
  if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
    e.preventDefault();
    oakOpenLesson(resId);
  }
}

/* ── Interactive Document Preview Modal ── */
var _oakActivePreviewRes = null;
function oakOpenPreview(resId) {
  var rawList = RESOURCES[_oakCurrentSubject] || [];
  var r = rawList.find(function(x) { return x.id === resId; }) || rawList[0];
  if (!r) return;
  _oakActivePreviewRes = r;

  var titleEl = document.getElementById('oakModalTitle');
  var subEl = document.getElementById('oakModalSub');
  if (titleEl) titleEl.textContent = r.fullName || r.name;
  if (subEl) subEl.textContent = 'Uploaded ' + fmtDate(r.date) + ' • ' + (r.size || '2.0 MB') + ' • ' + (r.pages || 16) + ' pages';

  var deptName = OAK_SUBJECT_TITLES[_oakCurrentSubject] || 'ACADEMICS';
  var paperDept = document.getElementById('oakPaperDept');
  var paperHeading = document.getElementById('oakPaperHeading');
  var paperDesc = document.getElementById('oakPaperDesc');
  var paperCallout = document.getElementById('oakPaperCallout');

  if (paperDept) {
    paperDept.textContent = 'Academic Handout • Department of ' + deptName.charAt(0) + deptName.slice(1).toLowerCase();
  }
  if (paperHeading) {
    paperHeading.textContent = r.fullName || r.name;
  }
  if (paperDesc) {
    paperDesc.textContent = r.desc || 'Learning materials and syllabus guide covering core course concepts and practice exercises.';
  }
  if (paperCallout) {
    if (r.formulas && r.formulas.length) {
      paperCallout.textContent = Array.isArray(r.formulas) ? r.formulas[0] : r.formulas;
    } else {
      paperCallout.textContent = (r.topic ? ('Focus: ' + r.topic) : 'Foundational Syllabus Unit') + (r.tags && r.tags.length ? (' (' + r.tags.join(', ') + ')') : '');
    }
  }

  var modal = document.getElementById('oakPreviewModal');
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function oakClosePreview() {
  var modal = document.getElementById('oakPreviewModal');
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
}

function oakDownloadCurrent() {
  if (_oakActivePreviewRes) {
    oakDownload(_oakActivePreviewRes.id);
  }
}

function oakDownload(resId) {
  var rawList = RESOURCES[_oakCurrentSubject] || [];
  var r = rawList.find(function(x) { return x.id === resId; });
  var name = (r && (r.fullName || r.name)) || 'Resource Material';
  if (window.toast) {
    /* Neutral in-progress wording — never claim the download succeeded
       before it actually has. */
    window.toast('Preparing download of "' + name + '"…', 'info');
  } else {
    alert('Preparing download of "' + name + '"');
  }
  downloadFile((r && r.src) || 'https://www.africau.edu/images/default/sample.pdf', name + '.pdf');
}

function oakToggleBookmark(btn, resId) {
  var active = NGISBookmarks.toggle(resId);
  NGISBookmarks.syncButton(btn, resId);
  _oakBookmarkedIds[resId] = active;
  if (window.toast) {
    window.toast(active ? 'Saved to Bookmarks' : 'Removed from Bookmarks', 'info');
  }
}

/* ── Interactive Practice Quiz Modal ── */
var QUIZ_DATA = {
  m7: [
    {
      q: '1. What are the roots of the quadratic equation x² - 5x + 6 = 0?',
      options: ['A) x = 2 and x = 3', 'B) x = -2 and x = -3', 'C) x = 1 and x = 6', 'D) x = -1 and x = 5'],
      correct: 0,
      hint: 'Factor as (x - 2)(x - 3) = 0.'
    },
    {
      q: '2. Find the determinant of matrix M = [[2, 1], [4, 3]].',
      options: ['A) 10', 'B) 2', 'C) -2', 'D) 8'],
      correct: 1,
      hint: 'det(M) = (2)(3) - (1)(4) = 6 - 4 = 2.'
    },
    {
      q: '3. Solve the system: 2x + y = 7 and x - y = 2.',
      options: ['A) x = 3, y = 1', 'B) x = 2, y = 3', 'C) x = 4, y = -1', 'D) x = 1, y = 5'],
      correct: 0,
      hint: 'Adding both equations gives 3x = 9 => x = 3, y = 1.'
    }
  ]
};

var _oakQuizSelected = {};

function oakOpenQuiz(resId) {
  _oakQuizSelected = {};
  var questions = QUIZ_DATA[resId] || QUIZ_DATA['m7'];
  var container = document.getElementById('quizQuestionsContainer');
  if (!container) return;

  var html = '';
  questions.forEach(function(item, qIdx) {
    html += '<div class="quiz-q-card">'
      + '  <div class="quiz-q-title">' + escHtml(item.q) + '</div>'
      + '  <div class="quiz-options">';
    item.options.forEach(function(opt, optIdx) {
      html += '    <button class="quiz-opt-btn" onclick="oakSelectQuizOpt(' + qIdx + ',' + optIdx + ',this)">' + escHtml(opt) + '</button>';
    });
    html += '  </div>'
      + '  <div class="quiz-feedback" id="quizFeedback_' + qIdx + '" style="display:none"></div>'
      + '</div>';
  });
  container.innerHTML = html;

  var scoreText = document.getElementById('quizScoreText');
  if (scoreText) scoreText.textContent = 'Score: 0 / ' + questions.length + ' answered';

  var modal = document.getElementById('oakQuizModal');
  if (modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  }
}

function oakSelectQuizOpt(qIdx, optIdx, btn) {
  _oakQuizSelected[qIdx] = optIdx;
  var card = btn.closest('.quiz-q-card');
  if (!card) return;
  card.querySelectorAll('.quiz-opt-btn').forEach(function(b) {
    b.style.borderColor = '#cbd5e1';
    b.style.background = '#ffffff';
  });
  btn.style.borderColor = '#159a9c';
  btn.style.background = '#f0fdfa';

  var questions = QUIZ_DATA['m7'];
  var answered = Object.keys(_oakQuizSelected).length;
  var scoreText = document.getElementById('quizScoreText');
  if (scoreText) scoreText.textContent = 'Answered: ' + answered + ' / ' + questions.length;
}

function oakSubmitQuiz() {
  var questions = QUIZ_DATA['m7'];
  var correctCount = 0;
  questions.forEach(function(item, qIdx) {
    var chosen = _oakQuizSelected[qIdx];
    var feedbackEl = document.getElementById('quizFeedback_' + qIdx);
    var card = feedbackEl ? feedbackEl.closest('.quiz-q-card') : null;
    var btns = card ? card.querySelectorAll('.quiz-opt-btn') : [];

    if (chosen === undefined) {
      if (feedbackEl) {
        feedbackEl.style.display = 'block';
        feedbackEl.className = 'quiz-feedback bad';
        feedbackEl.textContent = 'Please choose an answer.';
      }
      return;
    }

    if (chosen === item.correct) {
      correctCount++;
      if (btns[chosen]) btns[chosen].className = 'quiz-opt-btn correct';
      if (feedbackEl) {
        feedbackEl.style.display = 'block';
        feedbackEl.className = 'quiz-feedback good';
        feedbackEl.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;margin-right:4px;"><polyline points="20 6 9 17 4 12"></polyline></svg>Correct! ' + (item.hint || '');
      }
    } else {
      if (btns[chosen]) btns[chosen].className = 'quiz-opt-btn wrong';
      if (btns[item.correct]) btns[item.correct].className = 'quiz-opt-btn correct';
      if (feedbackEl) {
        feedbackEl.style.display = 'block';
        feedbackEl.className = 'quiz-feedback bad';
        feedbackEl.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block;vertical-align:middle;margin-right:4px;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>Incorrect. ' + (item.hint || '');
      }
    }
  });

  var scoreText = document.getElementById('quizScoreText');
  if (scoreText) {
    scoreText.textContent = 'Score: ' + correctCount + ' / ' + questions.length + ' (' + Math.round((correctCount/questions.length)*100) + '%)';
  }
  if (window.toast) {
    window.toast('Quiz graded: ' + correctCount + ' / ' + questions.length + ' correct!', correctCount === questions.length ? 'success' : 'info');
  }
}

function oakCloseQuiz() {
  var modal = document.getElementById('oakQuizModal');
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
  }
}

// Auto-initialize when ready
document.addEventListener('DOMContentLoaded', function() {
  oakInit();
});
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  oakInit();
}
