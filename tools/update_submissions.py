with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update rowBg
old_row_bg = "const rowBg = isSelected ? 'bg-[#F7F9F7]/50 font-medium' : '';"
new_row_bg = "const rowBg = isSelected ? 'selected-row border-l-4 border-[#0F5132]' : '';"
if old_row_bg in text:
    text = text.replace(old_row_bg, new_row_bg, 1)

# 2. Update actionBtn in renderTable
old_action_block = """        } else if (s.status === 'Graded') {
          actionBtn = `
            <div class="action-group justify-center">
              <button type="button" onclick="window.selectStudent('${s.id}')" class="action-icon-btn" data-ngis-icon="edit" title="Edit Mark (${s.grade}/100)" aria-label="Edit Mark for ${s.name}"></button>
            </div>`;
        } else {
          actionBtn = `
            <div class="action-group justify-center">
              <button type="button" onclick="window.selectStudent('${s.id}')" class="action-icon-btn primary" data-ngis-icon="view" title="Review &amp; Grade Submission" aria-label="Review &amp; Grade submission for ${s.name}"></button>
            </div>`;
        }"""

new_action_block = """        } else if (s.status === 'Graded') {
          actionBtn = `
            <div class="action-group justify-center">
              <button type="button" onclick="window.openSubmissionPreview('${s.id}')" class="action-icon-btn" data-ngis-icon="view" title="Preview Submission (${s.grade}/100)" aria-label="Preview Submission for ${s.name}"></button>
            </div>`;
        } else {
          actionBtn = `
            <div class="action-group justify-center">
              <button type="button" onclick="window.openSubmissionPreview('${s.id}')" class="action-icon-btn primary" data-ngis-icon="checkCircle" title="Review &amp; Preview Submission" aria-label="Review Submission for ${s.name}"></button>
            </div>`;
        }"""

assert old_action_block in text, "Could not find old_action_block"
text = text.replace(old_action_block, new_action_block, 1)

# 3. Update getFilteredSubmissions
old_filter = """    // Search query filter
    if (searchQuery) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(s => s.name.toLowerCase().includes(q) || s.id.toLowerCase().includes(q));
    }"""

new_filter = """    // Search query filter (names, IDs, cohort/classes, and status)
    if (searchQuery) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(s => 
        (s.name && s.name.toLowerCase().includes(q)) || 
        (s.id && s.id.toLowerCase().includes(q)) ||
        (s.cohort && s.cohort.toLowerCase().includes(q)) ||
        (s.status && s.status.toLowerCase().includes(q))
      );
    }"""

assert old_filter in text, "Could not find old_filter"
text = text.replace(old_filter, new_filter, 1)

# 4. Insert preview modal HTML before the uploadWorkModal
preview_modal_html = """
  <!-- ===================================================================
       STUDENT SUBMISSION PREVIEW MODAL (Section 4)
       =================================================================== -->
  <div id="submissionPreviewModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-3 sm:p-6 bg-black/60 backdrop-blur-sm transition-opacity hidden" role="dialog" aria-modal="true" aria-labelledby="subPreviewStudentName">
    <div class="fixed inset-0 cursor-pointer" onclick="closeSubmissionPreviewModal()"></div>
    <div class="modal relative w-full max-w-4xl bg-white dark:bg-slate-900 rounded-2xl sm:rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 flex flex-col max-h-[92vh] overflow-hidden z-10 animate-in fade-in zoom-in-95" role="document">
      
      <!-- Modal Header -->
      <div class="sticky top-0 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md px-5 sm:px-6 py-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between z-20 flex-shrink-0">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-10 h-10 rounded-full bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-[#0F5132] font-medium text-xs flex-shrink-0">
            <span id="subPreviewStudentInitials">SC</span>
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <h3 id="subPreviewStudentName" class="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">Sophea Chan</h3>
              <span id="subPreviewStatusBadge"></span>
            </div>
            <p id="subPreviewStudentMeta" class="text-xs text-slate-500 dark:text-slate-400 truncate mt-0.5">ID: 2026-STD-0144 • Grade 10A • Calculus Problem Set 3</p>
          </div>
        </div>

        <!-- Viewer Controls & Close -->
        <div class="flex items-center gap-1.5 sm:gap-2 flex-shrink-0">
          <button type="button" id="subPreviewZoomOutBtn" onclick="zoomSubPreview(-0.15)" class="p-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition cursor-pointer" title="Zoom Out" aria-label="Zoom Out">
            <span data-ngis-icon="zoomOut"></span>
          </button>
          <button type="button" id="subPreviewZoomInBtn" onclick="zoomSubPreview(0.15)" class="p-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition cursor-pointer" title="Zoom In" aria-label="Zoom In">
            <span data-ngis-icon="zoomIn"></span>
          </button>
          <button type="button" id="subPreviewDownloadBtn" onclick="downloadSubPreviewFile()" class="p-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition cursor-pointer" title="Download Document" aria-label="Download Document">
            <span data-ngis-icon="download"></span>
          </button>
          <button type="button" id="subPreviewFullscreenBtn" onclick="toggleSubPreviewFullscreen()" class="p-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition cursor-pointer" title="Fullscreen" aria-label="Toggle Fullscreen">
            <span data-ngis-icon="fullscreen"></span>
          </button>
          <div class="h-4 w-[1px] bg-slate-200 dark:bg-slate-700 mx-1"></div>
          <button type="button" id="closeSubPreviewBtn" onclick="closeSubmissionPreviewModal()" class="p-2 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition cursor-pointer" title="Close" aria-label="Close">
            <span data-ngis-icon="close"></span>
          </button>
        </div>
      </div>

      <!-- Modal Body (Split: Document Viewer on Left, Details on Right) -->
      <div class="flex-1 overflow-y-auto grid grid-cols-1 lg:grid-cols-12 gap-0">
        <!-- Document Canvas View -->
        <div id="subPreviewDocContainer" class="lg:col-span-8 bg-slate-100 dark:bg-slate-950 p-4 sm:p-6 flex items-center justify-center min-h-[380px] overflow-auto border-b lg:border-b-0 lg:border-r border-slate-200 dark:border-slate-800">
          <div id="subPreviewDocSheet" class="w-full max-w-xl bg-white shadow-md border border-slate-200 rounded-xl p-6 sm:p-8 text-slate-800 transition-transform origin-center">
            <div class="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-[#0F5132]"></span>
                <span class="text-[11px] font-medium tracking-wide uppercase text-slate-500">Student Submission Document</span>
              </div>
              <span id="subPreviewDocPageCount" class="text-[10px] text-slate-400 font-mono">Page 1 of 4</span>
            </div>
            <div class="space-y-4 text-xs font-serif leading-relaxed text-slate-700">
              <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg font-sans">
                <div class="text-xs font-medium text-slate-800" id="subPreviewSheetTitle">Calculus Problem Set 3: Derivatives &amp; Optimization</div>
                <div class="text-[11px] text-slate-500 mt-0.5" id="subPreviewSheetAuthor">Author: Sophea Chan (Grade 10A)</div>
              </div>
              <p class="italic text-slate-600">Problem 1: Find the critical points of f(x) = x^3 - 6x^2 + 9x + 2 and classify each using the Second Derivative Test.</p>
              <div class="bg-emerald-50/50 p-3 rounded-lg border border-emerald-100 font-mono text-[11px] text-slate-800">
                f'(x) = 3x^2 - 12x + 9 = 3(x - 1)(x - 3) = 0<br>
                Critical points at x = 1 and x = 3.<br>
                f''(x) = 6x - 12.<br>
                f''(1) = -6 &lt; 0 &rarr; Local Maximum at (1, 6).<br>
                f''(3) = 6 &gt; 0 &rarr; Local Minimum at (3, 2).
              </div>
              <p class="text-slate-600">Verified working sheet uploaded directly by student from NGIS E-Learning portal.</p>
            </div>
          </div>
        </div>

        <!-- Submission Details & Metadata Sidebar -->
        <div class="lg:col-span-4 p-5 sm:p-6 bg-white dark:bg-slate-900 flex flex-col justify-between space-y-5">
          <div class="space-y-4">
            <div>
              <span class="text-[10px] font-medium text-slate-400 uppercase tracking-wider block mb-1">Assignment Information</span>
              <div class="text-xs font-medium text-slate-800 dark:text-slate-200" id="subPreviewAssignmentDetail">Calculus Problem Set 3</div>
              <div class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Faculty of Mathematics • Term 1</div>
            </div>

            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-800 space-y-2 text-xs">
              <div class="flex justify-between">
                <span class="text-slate-500 dark:text-slate-400">Submission Date:</span>
                <span id="subPreviewDate" class="text-slate-800 dark:text-slate-200 font-medium">Oct 23, 2026, 11:42 AM</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500 dark:text-slate-400">Attached File:</span>
                <span id="subPreviewFileName" class="text-[#0F5132] font-medium truncate max-w-[150px]">Sophea_Chan_Set3.pdf</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500 dark:text-slate-400">File Size:</span>
                <span id="subPreviewFileSize" class="text-slate-600 dark:text-slate-300">2.4 MB</span>
              </div>
            </div>

            <div>
              <span class="text-[10px] font-medium text-slate-400 uppercase tracking-wider block mb-1">Current Assessment Status</span>
              <div class="p-3 rounded-xl border border-slate-200 dark:border-slate-800 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-slate-600 dark:text-slate-300">Recorded Score:</span>
                  <div id="subPreviewScoreDisplay" class="text-sm font-medium text-[#0F5132]">88 / 100</div>
                </div>
                <div class="text-[11px] text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800/80 pt-1.5">
                  <span class="font-medium text-slate-700 dark:text-slate-300 block mb-0.5">Teacher Feedback:</span>
                  <p id="subPreviewFeedbackText" class="italic">Excellent derivation of optimization boundaries.</p>
                </div>
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center gap-2">
            <button type="button" onclick="closeSubmissionPreviewModal()" class="flex-1 py-2 px-3 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-normal text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition cursor-pointer">
              Close Preview
            </button>
            <button type="button" onclick="openGradingFromPreview()" class="flex-1 py-2 px-3 rounded-xl bg-[#0F5132] hover:bg-[#0B3D26] text-white text-xs font-normal transition cursor-pointer">
              Enter Marks &amp; Rubric
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

target_upload_modal = '<div id="uploadWorkModal"'
assert target_upload_modal in text, "Could not find target_upload_modal"
text = text.replace(target_upload_modal, preview_modal_html + "\n  " + target_upload_modal, 1)

# 5. Add JavaScript functions for submission preview
js_preview_logic = """
  let subPreviewZoom = 1.0;
  window.openSubmissionPreview = function(studentId) {
    window.selectStudent(studentId);
    const student = submissionsData.find(s => s.id === studentId);
    if (!student) return;

    const modal = document.getElementById('submissionPreviewModal');
    if (!modal) return;

    const elInitials = document.getElementById('subPreviewStudentInitials');
    const elName = document.getElementById('subPreviewStudentName');
    const elMeta = document.getElementById('subPreviewStudentMeta');
    const elAsgn = document.getElementById('subPreviewAssignmentDetail');
    const elDate = document.getElementById('subPreviewDate');
    const elFileName = document.getElementById('subPreviewFileName');
    const elFileSize = document.getElementById('subPreviewFileSize');
    const elScore = document.getElementById('subPreviewScoreDisplay');
    const elFeedback = document.getElementById('subPreviewFeedbackText');
    const elBadge = document.getElementById('subPreviewStatusBadge');
    const elAuthor = document.getElementById('subPreviewSheetAuthor');

    const inits = student.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase();
    if (elInitials) elInitials.textContent = inits || 'ST';
    if (elName) elName.textContent = student.name;
    if (elMeta) elMeta.textContent = `ID: ${student.id} • ${student.cohort || 'Grade 10A'} • Calculus Problem Set 3`;
    if (elAsgn) elAsgn.textContent = 'Calculus Problem Set 3: Derivatives & Optimization';
    if (elAuthor) elAuthor.textContent = `Author: ${student.name} (${student.cohort || 'Grade 10A'})`;

    const subDateStr = student.submittedDate ? `${student.submittedDate}, ${student.submittedTime}` : 'Oct 23, 2026, 11:42 AM';
    if (elDate) elDate.textContent = subDateStr;
    const fclean = student.name.replace(/\\s+/g, '_') + '_Set3.pdf';
    if (elFileName) elFileName.textContent = student.fileName || fclean;
    if (elFileSize) elFileSize.textContent = student.fileMeta ? (student.fileMeta.split('•')[1] || '2.4 MB').trim() : '2.4 MB';

    if (elBadge) elBadge.innerHTML = getStatusBadgeHTML(student.status);

    if (elScore) {
      if (student.grade !== null && student.grade !== undefined) {
        elScore.innerHTML = `<span class="text-base font-medium text-[#0F5132]">${student.grade}</span> <span class="text-xs text-slate-400 font-normal">/ 100</span>`;
      } else {
        elScore.innerHTML = `<span class="text-xs text-slate-400 italic font-normal">Pending Evaluation</span>`;
      }
    }

    if (elFeedback) {
      elFeedback.textContent = student.feedback || 'No teacher feedback has been recorded yet. Click "Enter Marks & Rubric" to evaluate.';
    }

    subPreviewZoom = 1.0;
    const sheet = document.getElementById('subPreviewDocSheet');
    if (sheet) sheet.style.transform = 'scale(1)';

    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';

    if (window.hydrateActionIcons) window.hydrateActionIcons(modal);
  };

  window.closeSubmissionPreviewModal = function() {
    const modal = document.getElementById('submissionPreviewModal');
    if (!modal) return;
    modal.classList.remove('flex');
    modal.classList.add('hidden');
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
  };

  window.zoomSubPreview = function(delta) {
    subPreviewZoom = Math.max(0.6, Math.min(1.8, subPreviewZoom + delta));
    const sheet = document.getElementById('subPreviewDocSheet');
    if (sheet) sheet.style.transform = `scale(${subPreviewZoom})`;
  };

  window.toggleSubPreviewFullscreen = function() {
    const cont = document.getElementById('subPreviewDocContainer');
    if (!cont) return;
    if (!document.fullscreenElement) {
      if (cont.requestFullscreen) cont.requestFullscreen();
      else if (cont.webkitRequestFullscreen) cont.webkitRequestFullscreen();
    } else {
      if (document.exitFullscreen) document.exitFullscreen();
    }
  };

  window.downloadSubPreviewFile = function() {
    const student = submissionsData.find(s => s.id === selectedStudentId);
    const fname = student && student.fileName ? student.fileName : 'Student_Submission.pdf';
    const blob = new Blob([`%PDF-1.4\\n% NGIS Student Submission: ${fname}\\nStudent: ${student ? student.name : 'Student'}\\nDate: Oct 2026\\n`], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fname;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
    if (window.toast) window.toast(`Downloading ${fname}…`, 'info');
  };

  window.openGradingFromPreview = function() {
    window.closeSubmissionPreviewModal();
    const scoreInp = document.getElementById('drawerScoreInput');
    if (scoreInp) {
      scoreInp.scrollIntoView({ behavior: 'smooth', block: 'center' });
      scoreInp.focus();
    }
  };
"""

target_select_student = "selectStudent = function(id) {"
assert target_select_student in text, "Could not find target_select_student"
text = text.replace(target_select_student, js_preview_logic + "\n  " + target_select_student, 1)

# 6. Call window.NGIS_showOperationSuccess on saveEvaluationDraft and saveAndPublishMark
old_save_draft = "if (window.toast) window.toast(`Evaluation draft for ${student.name} saved`, 'info');"
new_save_draft = """if (window.NGIS_showOperationSuccess) {
      window.NGIS_showOperationSuccess({ title: 'Evaluation Saved', message: `Evaluation draft for ${student.name} saved successfully.` });
    } else if (window.toast) {
      window.toast(`Evaluation draft for ${student.name} saved`, 'info');
    }"""
if old_save_draft in text:
    text = text.replace(old_save_draft, new_save_draft, 1)

old_pub_mark = "if (window.toast) window.toast(`Published mark ${finalMark}/100 for ${student.name}`, 'success');"
new_pub_mark = """if (window.NGIS_showOperationSuccess) {
      window.NGIS_showOperationSuccess({ title: 'Mark Published', message: `Published mark ${finalMark}/100 for ${student.name}. Student records updated.` });
    } else if (window.toast) {
      window.toast(`Published mark ${finalMark}/100 for ${student.name}`, 'success');
    }"""
if old_pub_mark in text:
    text = text.replace(old_pub_mark, new_pub_mark, 1)

with open('pages/teacher/teacher-submissions.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated teacher-submissions.html successfully!')
