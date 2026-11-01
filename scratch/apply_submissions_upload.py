import re

with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Desktop Quick Action Controls:
# Replace lines around btnExportCSV, btnDownloadZip, btnBatchPublish
old_desktop_actions = """        <button id="btnBatchPublish" onclick="batchPublishGrades()" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-white bg-[#1e4d38] hover:bg-[#163b2a] border border-[#1e4d38] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#1e4d38]" type="button">
          <svg class="w-3.5 h-3.5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Batch Publish Grades</span>
        </button>"""

new_desktop_actions = """        <button id="btnUploadAssignmentOrWork" onclick="openUploadModal()" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-white bg-[#1e4d38] hover:bg-[#163b2a] border border-[#1e4d38] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#1e4d38]" type="button">
          <svg class="w-3.5 h-3.5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Upload Assignment / Work</span>
        </button>

        <button id="btnBatchPublish" onclick="batchPublishGrades()" class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 hover:text-slate-900 transition shadow-xs active:scale-95" type="button">
          <svg class="w-3.5 h-3.5 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Batch Publish Grades</span>
        </button>"""

# 2. Update Mobile Header Action Buttons:
old_mobile_actions = """    <div class="flex items-center gap-2 flex-shrink-0">
      <button type="button" onclick="exportSubmissionsCSV()" class="p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition" title="Export CSV">
        <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
      </button>
      <button type="button" onclick="batchPublishGrades()" class="px-3 py-1.5 rounded-lg bg-[#1e4d38] text-white font-medium text-xs shadow-xs active:scale-95 transition flex items-center gap-1.5" title="Publish Grades">
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span>Publish</span>
      </button>
    </div>"""

new_mobile_actions = """    <div class="flex items-center gap-2 flex-shrink-0">
      <button type="button" onclick="openUploadModal()" class="px-2.5 py-1.5 rounded-lg bg-[#1e4d38] text-white font-medium text-xs shadow-xs active:scale-95 transition flex items-center gap-1.5" title="Upload Assignment / Work">
        <svg class="w-3.5 h-3.5 text-emerald-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span>Upload</span>
      </button>
      <button type="button" onclick="exportSubmissionsCSV()" class="p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition" title="Export CSV">
        <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
      </button>
      <button type="button" onclick="batchPublishGrades()" class="px-2.5 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-700 font-medium text-xs shadow-xs active:scale-95 transition flex items-center gap-1.5" title="Publish Grades">
        <svg class="w-3.5 h-3.5 text-emerald-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span>Publish</span>
      </button>
    </div>"""

# 3. Modal HTML to insert right before </main>
modal_html = """
  <!-- ===================================================================
       UPLOAD ASSIGNMENT OR STUDENT WORK MODAL
       =================================================================== -->
  <div id="uploadWorkModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-900/60 backdrop-blur-xs transition-opacity duration-200 hidden" role="dialog" aria-modal="true" aria-labelledby="uploadModalTitle" onclick="if(event.target === this) closeUploadModal()">
    <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-2xl w-full max-h-[92vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200" onclick="event.stopPropagation()">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/80 flex-shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-[#1e4d38] border border-emerald-200/70 flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
          </div>
          <div>
            <h3 id="uploadModalTitle" class="text-base font-medium text-slate-900 leading-snug">Upload Assignment or Work</h3>
            <p class="text-xs text-slate-500 mt-0.5">Publish coursework to classes or upload verified student work directly.</p>
          </div>
        </div>
        <button type="button" onclick="closeUploadModal()" class="w-8 h-8 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 flex items-center justify-center transition active:scale-95" aria-label="Close dialog">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </button>
      </div>

      <!-- Segmented Mode Switcher -->
      <div class="px-6 pt-4 pb-1 bg-white flex-shrink-0">
        <div class="p-1 bg-slate-100 rounded-xl flex items-center gap-1 border border-slate-200/80">
          <button type="button" id="tabModeAssignment" onclick="switchUploadMode('assignment')" class="flex-1 py-2 px-3 text-xs font-medium rounded-lg transition bg-white text-slate-900 shadow-xs border border-slate-200/80 flex items-center justify-center gap-1.5">
            <svg class="w-3.5 h-3.5 text-[#1e4d38]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            <span>Create / Upload Assignment</span>
          </button>
          <button type="button" id="tabModeWork" onclick="switchUploadMode('work')" class="flex-1 py-2 px-3 text-xs font-medium rounded-lg transition text-slate-600 hover:text-slate-900 flex items-center justify-center gap-1.5">
            <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            <span>Upload Student Work</span>
          </button>
        </div>
      </div>

      <!-- Modal Body (Scrollable) -->
      <div class="px-6 py-4 overflow-y-auto space-y-4 flex-1 custom-scrollbar text-xs">
        
        <!-- TAB 1: NEW ASSIGNMENT FORM -->
        <form id="formNewAssignment" class="space-y-4" onsubmit="event.preventDefault(); submitUploadModal();">
          <div>
            <label for="newAsgnTitle" class="block font-medium text-slate-700 mb-1">Assignment Title <span class="text-rose-500">*</span></label>
            <input type="text" id="newAsgnTitle" placeholder="e.g. Calculus Problem Set 4: Integration by Parts" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900" required>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label for="newAsgnCohort" class="block font-medium text-slate-700 mb-1">Target Cohort / Class <span class="text-rose-500">*</span></label>
              <select id="newAsgnCohort" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
                <option value="Grade 10A (Adv Math)" selected>Grade 10A (Adv Math)</option>
                <option value="Grade 10B (Adv Math)">Grade 10B (Adv Math)</option>
                <option value="Grade 11A (Calculus BC)">Grade 11A (Calculus BC)</option>
                <option value="Grade 12B (Applied Stats)">Grade 12B (Applied Stats)</option>
              </select>
            </div>
            <div>
              <label for="newAsgnSubject" class="block font-medium text-slate-700 mb-1">Subject Stream</label>
              <select id="newAsgnSubject" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
                <option value="Advanced Mathematics" selected>Advanced Mathematics</option>
                <option value="AP Physics C">AP Physics C</option>
                <option value="Cambridge Chemistry">Cambridge Chemistry</option>
                <option value="Khmer Literature & Essay">Khmer Literature & Essay</option>
                <option value="English Literature">English Literature</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label for="newAsgnDueDate" class="block font-medium text-slate-700 mb-1">Due Date <span class="text-rose-500">*</span></label>
              <input type="date" id="newAsgnDueDate" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
            </div>
            <div>
              <label for="newAsgnDueTime" class="block font-medium text-slate-700 mb-1">Due Time</label>
              <input type="time" id="newAsgnDueTime" value="23:59" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
            </div>
            <div>
              <label for="newAsgnMaxScore" class="block font-medium text-slate-700 mb-1">Max Score</label>
              <input type="number" id="newAsgnMaxScore" value="100" min="1" max="1000" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
            </div>
          </div>

          <div>
            <label for="newAsgnInstructions" class="block font-medium text-slate-700 mb-1">Instructions &amp; Criteria</label>
            <textarea id="newAsgnInstructions" rows="3" placeholder="Provide problem numbers, guidelines, submission format requirements..." class="w-full text-xs p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900"></textarea>
          </div>

          <!-- File Upload Dropzone for Assignment Brief -->
          <div>
            <label class="block font-medium text-slate-700 mb-1">Attach Brief or Problem Sheet (.PDF, .DOCX, .ZIP)</label>
            <div id="asgnDropZone" class="border-2 border-dashed border-slate-300 hover:border-[#1e4d38] rounded-xl p-5 text-center transition cursor-pointer bg-slate-50/50 hover:bg-emerald-50/20" onclick="document.getElementById('asgnFileInput').click()">
              <input type="file" id="asgnFileInput" class="hidden" accept=".pdf,.doc,.docx,.zip,.png,.jpg" onchange="handleFileSelect(this.files, 'assignment')">
              <div class="flex flex-col items-center justify-center gap-1.5">
                <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">
                  <svg class="w-5 h-5 text-[#1e4d38]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                </div>
                <p class="text-xs font-medium text-slate-700"><span class="text-[#1e4d38] underline">Click to browse</span> or drag and drop files here</p>
                <p class="text-[11px] text-slate-400">PDF, Word, or Zip archive up to 50 MB</p>
              </div>
            </div>
            <div id="asgnSelectedFiles" class="mt-2 space-y-1.5 empty:hidden"></div>
          </div>
        </form>

        <!-- TAB 2: UPLOAD STUDENT WORK FORM -->
        <form id="formStudentWork" class="space-y-4 hidden" onsubmit="event.preventDefault(); submitUploadModal();">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label for="workTargetAsgn" class="block font-medium text-slate-700 mb-1">Target Assignment <span class="text-rose-500">*</span></label>
              <select id="workTargetAsgn" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
                <option value="Calculus Problem Set 3" selected>Calculus Problem Set 3 (Active)</option>
                <option value="Statistics Quiz 2">Statistics Quiz 2</option>
                <option value="Calculus Problem Set 2">Calculus Problem Set 2</option>
                <option value="Trigonometric Proofs Task">Trigonometric Proofs Task</option>
              </select>
            </div>
            <div>
              <label for="workTargetStudent" class="block font-medium text-slate-700 mb-1">Select Student <span class="text-rose-500">*</span></label>
              <select id="workTargetStudent" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
                <!-- Dynamically populated from submissionsData -->
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label for="workStatus" class="block font-medium text-slate-700 mb-1">Submission Status <span class="text-rose-500">*</span></label>
              <select id="workStatus" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
                <option value="Submitted" selected>Submitted (On-time)</option>
                <option value="Late">Late Submission</option>
                <option value="Graded">Graded / Verified</option>
              </select>
            </div>
            <div>
              <label for="workGrade" class="block font-medium text-slate-700 mb-1">Initial Grade (Optional)</label>
              <input type="number" id="workGrade" min="0" max="100" placeholder="e.g. 85 (or leave blank if pending)" class="w-full text-xs py-2 px-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900">
            </div>
          </div>

          <div>
            <label for="workFeedback" class="block font-medium text-slate-700 mb-1">Teacher Remarks / Notes</label>
            <textarea id="workFeedback" rows="2" placeholder="Submission notes, physical paper turn-in timestamp, or initial remarks..." class="w-full text-xs p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#1e4d38] focus:border-[#1e4d38] transition bg-white text-slate-900"></textarea>
          </div>

          <!-- File Upload Dropzone for Student Submission -->
          <div>
            <label class="block font-medium text-slate-700 mb-1">Student Work Attachment <span class="text-rose-500">*</span></label>
            <div id="workDropZone" class="border-2 border-dashed border-slate-300 hover:border-[#1e4d38] rounded-xl p-5 text-center transition cursor-pointer bg-slate-50/50 hover:bg-emerald-50/20" onclick="document.getElementById('workFileInput').click()">
              <input type="file" id="workFileInput" class="hidden" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg" onchange="handleFileSelect(this.files, 'work')">
              <div class="flex flex-col items-center justify-center gap-1.5">
                <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">
                  <svg class="w-5 h-5 text-[#1e4d38]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                </div>
                <p class="text-xs font-medium text-slate-700"><span class="text-[#1e4d38] underline">Click to browse</span> or drag and drop student document</p>
                <p class="text-[11px] text-slate-400">PDF, Word, or scanned images up to 50 MB</p>
              </div>
            </div>
            <div id="workSelectedFiles" class="mt-2 space-y-1.5 empty:hidden"></div>
          </div>
        </form>

      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-3.5 border-t border-slate-200 bg-slate-50/80 flex items-center justify-between flex-shrink-0">
        <div class="hidden sm:flex items-center gap-1.5 text-[11px] text-slate-500">
          <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
          <span>NGIS Verified Academic Submissions Engine</span>
        </div>
        <div class="flex items-center gap-2.5 w-full sm:w-auto justify-end">
          <button type="button" onclick="closeUploadModal()" class="px-3.5 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition shadow-xs">
            Cancel
          </button>
          <button type="button" id="btnSubmitUpload" onclick="submitUploadModal()" class="px-4 py-2 text-xs font-medium text-white bg-[#1e4d38] hover:bg-[#163b2a] rounded-lg shadow-xs transition active:scale-95 flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            <span id="submitUploadBtnText">Publish Assignment</span>
          </button>
        </div>
      </div>

    </div>
  </div>
"""

# 4. Javascript logic to append to main script
js_code = """
  // -------------------------------------------------------------------------
  // UPLOAD ASSIGNMENT / WORK MODAL LOGIC
  // -------------------------------------------------------------------------
  let currentUploadMode = 'assignment';
  let uploadedAssignmentFile = null;
  let uploadedWorkFile = null;

  window.openUploadModal = function(mode = 'assignment') {
    const modal = document.getElementById('uploadWorkModal');
    if (!modal) return;
    
    // Populate student select dropdown if empty
    const studentSelect = document.getElementById('workTargetStudent');
    if (studentSelect && studentSelect.options.length === 0) {
      submissionsData.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = `${s.name} (${s.id}) — ${s.class}`;
        studentSelect.appendChild(opt);
      });
      if (selectedStudentId) studentSelect.value = selectedStudentId;
    }

    // Set default due date to 7 days from now
    const dueInput = document.getElementById('newAsgnDueDate');
    if (dueInput && !dueInput.value) {
      const nextWeek = new Date();
      nextWeek.setDate(nextWeek.getDate() + 7);
      dueInput.value = nextWeek.toISOString().split('T')[0];
    }

    switchUploadMode(mode);
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  };

  window.closeUploadModal = function() {
    const modal = document.getElementById('uploadWorkModal');
    if (!modal) return;
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  };

  window.switchUploadMode = function(mode) {
    currentUploadMode = mode;
    const tabAsgn = document.getElementById('tabModeAssignment');
    const tabWork = document.getElementById('tabModeWork');
    const formAsgn = document.getElementById('formNewAssignment');
    const formWork = document.getElementById('formStudentWork');
    const submitBtnText = document.getElementById('submitUploadBtnText');

    if (mode === 'assignment') {
      if (tabAsgn) tabAsgn.className = "flex-1 py-2 px-3 text-xs font-medium rounded-lg transition bg-white text-slate-900 shadow-xs border border-slate-200/80 flex items-center justify-center gap-1.5";
      if (tabWork) tabWork.className = "flex-1 py-2 px-3 text-xs font-medium rounded-lg transition text-slate-600 hover:text-slate-900 flex items-center justify-center gap-1.5";
      if (formAsgn) formAsgn.classList.remove('hidden');
      if (formWork) formWork.classList.add('hidden');
      if (submitBtnText) submitBtnText.textContent = "Publish Assignment";
    } else {
      if (tabWork) tabWork.className = "flex-1 py-2 px-3 text-xs font-medium rounded-lg transition bg-white text-slate-900 shadow-xs border border-slate-200/80 flex items-center justify-center gap-1.5";
      if (tabAsgn) tabAsgn.className = "flex-1 py-2 px-3 text-xs font-medium rounded-lg transition text-slate-600 hover:text-slate-900 flex items-center justify-center gap-1.5";
      if (formWork) formWork.classList.remove('hidden');
      if (formAsgn) formAsgn.classList.add('hidden');
      if (submitBtnText) submitBtnText.textContent = "Upload Student Work";
    }
  };

  window.handleFileSelect = function(files, context) {
    if (!files || files.length === 0) return;
    const file = files[0];
    const containerId = context === 'assignment' ? 'asgnSelectedFiles' : 'workSelectedFiles';
    const container = document.getElementById(containerId);
    if (!container) return;

    if (context === 'assignment') uploadedAssignmentFile = file;
    else uploadedWorkFile = file;

    const sizeStr = file.size < 1024 * 1024 
      ? (file.size / 1024).toFixed(1) + ' KB'
      : (file.size / (1024 * 1024)).toFixed(1) + ' MB';

    container.innerHTML = `
      <div class="flex items-center justify-between p-2.5 rounded-lg border border-emerald-200 bg-emerald-50/50">
        <div class="flex items-center gap-2 min-w-0">
          <svg class="w-5 h-5 text-[#1e4d38] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
          <div class="min-w-0">
            <p class="text-xs font-medium text-slate-800 truncate">${file.name}</p>
            <p class="text-[11px] text-slate-500">${sizeStr} · Ready to upload</p>
          </div>
        </div>
        <button type="button" onclick="removeUploadedFile('${context}')" class="p-1 rounded-md text-slate-400 hover:text-rose-600 hover:bg-white transition" title="Remove file">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        </button>
      </div>
    `;
  };

  window.removeUploadedFile = function(context) {
    if (context === 'assignment') {
      uploadedAssignmentFile = null;
      const fileInput = document.getElementById('asgnFileInput');
      if (fileInput) fileInput.value = '';
      const c = document.getElementById('asgnSelectedFiles');
      if (c) c.innerHTML = '';
    } else {
      uploadedWorkFile = null;
      const fileInput = document.getElementById('workFileInput');
      if (fileInput) fileInput.value = '';
      const c = document.getElementById('workSelectedFiles');
      if (c) c.innerHTML = '';
    }
  };

  window.submitUploadModal = function() {
    if (currentUploadMode === 'assignment') {
      const title = document.getElementById('newAsgnTitle')?.value.trim();
      const cohort = document.getElementById('newAsgnCohort')?.value || 'Grade 10A';
      const subject = document.getElementById('newAsgnSubject')?.value || 'Advanced Mathematics';
      const dueDate = document.getElementById('newAsgnDueDate')?.value || '';
      const dueTime = document.getElementById('newAsgnDueTime')?.value || '23:59';
      const maxScore = document.getElementById('newAsgnMaxScore')?.value || '100';

      if (!title) {
        alert('Please enter an assignment title.');
        document.getElementById('newAsgnTitle')?.focus();
        return;
      }

      // Add to assignment select in toolbar
      const selectAsgn = document.getElementById('selectAssignment');
      if (selectAsgn) {
        const newOpt = document.createElement('option');
        newOpt.textContent = `${title} (Active)`;
        newOpt.selected = true;
        selectAsgn.insertBefore(newOpt, selectAsgn.firstChild);
      }

      // Update header label
      const lbl = document.getElementById('assignmentHeaderLabel');
      if (lbl) lbl.textContent = `Assignment Records: ${title}`;

      // Show toast
      if (window.toast) {
        window.toast(`Assignment "${title}" successfully published to ${cohort}!`, 'success');
      } else {
        alert(`Assignment "${title}" successfully published to ${cohort}!`);
      }

      // Reset form & close
      document.getElementById('formNewAssignment')?.reset();
      removeUploadedFile('assignment');
      closeUploadModal();

    } else {
      // Work submission upload
      const asgn = document.getElementById('workTargetAsgn')?.value;
      const studentId = document.getElementById('workTargetStudent')?.value;
      const status = document.getElementById('workStatus')?.value || 'Submitted';
      const rawGrade = document.getElementById('workGrade')?.value;
      const grade = rawGrade !== '' && !isNaN(rawGrade) ? parseInt(rawGrade, 10) : null;
      const feedback = document.getElementById('workFeedback')?.value.trim();

      if (!studentId) {
        alert('Please select a student.');
        return;
      }

      const file = uploadedWorkFile;
      const fileName = file ? file.name : 'Uploaded_Work_Submission.pdf';
      const sizeStr = file ? (file.size / (1024 * 1024)).toFixed(1) + ' MB' : '1.9 MB';
      const todayStr = 'Oct 24, 2026';

      // Find or update in submissionsData
      let target = submissionsData.find(s => s.id === studentId);
      if (target) {
        target.status = status;
        target.grade = grade;
        target.submittedDate = todayStr;
        target.submittedTime = '03:45 PM (Verified Upload)';
        target.fileName = fileName;
        target.fileMeta = `Submitted ${todayStr} · ${sizeStr} · Verified Upload`;
        if (feedback) target.feedback = feedback;
        if (grade !== null) {
          target.status = 'Graded';
          target.rubric = {
            c1: Math.round(grade * 0.4),
            c2: Math.round(grade * 0.4),
            c3: Math.round(grade * 0.2)
          };
        }
      }

      // Re-render table and drawer
      renderTable();
      updateKpis();
      selectStudent(studentId);

      if (window.toast) {
        window.toast(`Student work for ${target ? target.name : studentId} uploaded successfully!`, 'success');
      } else {
        alert(`Student work uploaded successfully!`);
      }

      // Reset & close
      document.getElementById('formStudentWork')?.reset();
      removeUploadedFile('work');
      closeUploadModal();
    }
  };

  // Setup Drag & Drop Listeners
  document.addEventListener('DOMContentLoaded', () => {
    ['asgnDropZone', 'workDropZone'].forEach(id => {
      const zone = document.getElementById(id);
      if (!zone) return;
      const context = id === 'asgnDropZone' ? 'assignment' : 'work';

      zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.classList.add('border-[#1e4d38]', 'bg-emerald-50/40');
      });
      zone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        zone.classList.remove('border-[#1e4d38]', 'bg-emerald-50/40');
      });
      zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('border-[#1e4d38]', 'bg-emerald-50/40');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
          handleFileSelect(e.dataTransfer.files, context);
        }
      });
    });

    // Esc key closes modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeUploadModal();
    });
  });
"""

# Apply modifications
c = html.replace('\r\n', '\n')

# 1. Desktop quick action
if old_desktop_actions.replace('\r\n', '\n') in c:
    c = c.replace(old_desktop_actions.replace('\r\n', '\n'), new_desktop_actions.replace('\r\n', '\n'))
    print("Desktop actions updated successfully")
else:
    print("Desktop actions NOT found")

# 2. Mobile header action
if old_mobile_actions.replace('\r\n', '\n') in c:
    c = c.replace(old_mobile_actions.replace('\r\n', '\n'), new_mobile_actions.replace('\r\n', '\n'))
    print("Mobile header actions updated successfully")
else:
    print("Mobile header actions NOT found")

# 3. Modal HTML right before </main>
if '</main>' in c:
    c = c.replace('</main>', modal_html.replace('\r\n', '\n') + '\n</main>')
    print("Modal HTML inserted successfully")
else:
    print("</main> NOT found")

# 4. JS code right before the closing of main script: })();
if '  // Initialization\n  document.addEventListener(\'DOMContentLoaded\', () => {' in c:
    c = c.replace('  // Initialization\n  document.addEventListener(\'DOMContentLoaded\', () => {', js_code.replace('\r\n', '\n') + '\n  // Initialization\n  document.addEventListener(\'DOMContentLoaded\', () => {')
    print("JavaScript functions inserted successfully")
else:
    print("Main script initialization marker NOT found")

with open('pages/teacher/teacher-submissions.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("FILE UPDATE COMPLETE")

