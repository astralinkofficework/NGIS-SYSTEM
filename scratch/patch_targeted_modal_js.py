with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace from `function populateUploadStudentSelect()` to `// PREVIEW MODAL & TRANSCRIPT VIEWING`
start_marker = '  // ═══════════════════════════════════════════════════════════════════\n  // MODAL: UPLOAD & ASSIGN STUDENT TRANSCRIPT'
end_marker = '  // ═══════════════════════════════════════════════════════════════════\n  // PREVIEW MODAL & TRANSCRIPT VIEWING'

new_upload_js = '''  // ═══════════════════════════════════════════════════════════════════
  // MODAL: UPLOAD & ASSIGN STUDENT TRANSCRIPT
  // ═══════════════════════════════════════════════════════════════════
  function populateUploadStudentSelect() {
    const sel = document.getElementById('selectUploadStudent');
    if (!sel) return;
    sel.innerHTML = reportsData.map(s => `
      <option value="${s.id}">${s.name} (${s.id}) &bull; ${s.class}</option>
    `).join('');
  }

  window.toggleStudentSelector = function(showDropdown) {
    const card = document.getElementById('targetStudentInfoCard');
    const container = document.getElementById('studentSelectContainer');
    if (showDropdown) {
      if (card) card.classList.add('hidden');
      if (container) container.classList.remove('hidden');
    } else {
      if (card) card.classList.remove('hidden');
      if (container) container.classList.add('hidden');
    }
  };

  window.onSelectStudentChange = function(studentId) {
    setModalTargetStudent(studentId, true);
    window.toggleStudentSelector(false);
  };

  function setModalTargetStudent(studentId, allowChange) {
    const student = reportsData.find(s => s.id === studentId) || reportsData[0];
    if (!student) return;

    const nameEl = document.getElementById('targetStudentName');
    const metaEl = document.getElementById('targetStudentMeta');
    const initEl = document.getElementById('targetStudentInitials');
    const hiddenId = document.getElementById('hiddenUploadStudentId');
    const sel = document.getElementById('selectUploadStudent');
    const titleEl = document.getElementById('modalUploadTitle');
    const changeBtn = document.getElementById('btnChangeTargetStudent');
    const submitText = document.getElementById('btnSubmitUploadText');

    if (nameEl) nameEl.textContent = student.name;
    if (metaEl) metaEl.textContent = `ID: ${student.id} • Class: ${student.class} • ${student.term}`;
    if (initEl) initEl.textContent = student.name.split(' ').map(p => p[0]).join('').slice(0, 2).toUpperCase();
    if (hiddenId) hiddenId.value = student.id;
    if (sel) sel.value = student.id;
    if (titleEl) titleEl.textContent = `Upload Transcript for ${student.name.split(' ')[0]}`;
    if (changeBtn) {
      if (allowChange) changeBtn.classList.remove('hidden');
      else changeBtn.classList.add('hidden');
    }

    const card = document.getElementById('targetStudentInfoCard');
    const container = document.getElementById('studentSelectContainer');
    if (card) card.classList.remove('hidden');
    if (container) container.classList.add('hidden');

    if (submitText) {
      const fileInput = document.getElementById('modalFileInput');
      if (fileInput && fileInput.files && fileInput.files[0]) {
        submitText.textContent = `Push Transcript to ${student.name.split(' ')[0]}`;
      } else {
        submitText.textContent = 'Push Transcript';
      }
    }
  }

  window.openUploadTranscriptModal = function(studentId) {
    populateUploadStudentSelect();

    // If specific student ID passed from row action, lock to that student only (no dropdown)
    if (studentId) {
      setModalTargetStudent(studentId, false);
    } else {
      // Opened globally: default to first student, allow changing
      const curId = (reportsData[0] && reportsData[0].id) || '2026-STD-0142';
      setModalTargetStudent(curId, true);
    }

    clearSelectedUploadFile();
    const alertEl = document.getElementById('uploadErrorAlert');
    if (alertEl) alertEl.classList.add('hidden');
    const loadingEl = document.getElementById('uploadLoadingState');
    if (loadingEl) loadingEl.classList.add('hidden');
    const submitBtn = document.getElementById('btnSubmitUpload');
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.classList.remove('opacity-75', 'cursor-not-allowed', 'ring-2', 'ring-emerald-500/25', 'bg-emerald-700');
      submitBtn.classList.add('bg-[#1e4d38]');
      submitBtn.innerHTML = '<span class="material-symbols-outlined text-[16px] transition-transform duration-200">publish</span><span id="btnSubmitUploadText">Push Transcript</span>';
    }

    const modal = document.getElementById('modalUploadTranscript');
    if (modal) modal.classList.remove('hidden');
  };

  window.closeUploadTranscriptModal = function() {
    const modal = document.getElementById('modalUploadTranscript');
    if (modal) modal.classList.add('hidden');
    clearSelectedUploadFile();
  };

  window.onModalFileSelected = function(input) {
    const file = input.files && input.files[0];
    if (!file) return;

    const alertEl = document.getElementById('uploadErrorAlert');
    const msgEl = document.getElementById('uploadErrorMessage');

    const ext = (file.name.split('.').pop() || '').toLowerCase();
    const allowed = ['pdf', 'png', 'jpg', 'jpeg', 'webp'];
    if (!allowed.includes(ext)) {
      if (alertEl) alertEl.classList.remove('hidden');
      if (msgEl) msgEl.textContent = `File format .${ext} is not allowed. Only PDF and image formats (.png, .jpg, .webp) are accepted.`;
      input.value = '';
      return;
    }

    if (file.size > 15 * 1024 * 1024) {
      if (alertEl) alertEl.classList.remove('hidden');
      if (msgEl) msgEl.textContent = `File size (${(file.size / (1024*1024)).toFixed(1)} MB) exceeds the 15 MB limit. Please select a smaller file.`;
      input.value = '';
      return;
    }

    if (alertEl) alertEl.classList.add('hidden');

    const promptEl = document.getElementById('dropzonePrompt');
    const badgeEl = document.getElementById('dropzoneSelectedFile');
    const nameEl = document.getElementById('selectedFileName');
    const sizeEl = document.getElementById('selectedFileSize');
    const iconEl = document.getElementById('selectedFileIcon');
    const submitBtn = document.getElementById('btnSubmitUpload');
    const submitText = document.getElementById('btnSubmitUploadText');

    if (promptEl) promptEl.classList.add('hidden');
    if (badgeEl) {
      badgeEl.classList.remove('hidden');
      badgeEl.classList.add('flex', 'animate-dropzone-pop');
      setTimeout(() => badgeEl.classList.remove('animate-dropzone-pop'), 400);
    }
    if (nameEl) nameEl.textContent = file.name;
    if (sizeEl) sizeEl.textContent = (file.size < 1024*1024 ? (file.size/1024).toFixed(1) + ' KB' : (file.size/(1024*1024)).toFixed(2) + ' MB');
    if (iconEl) iconEl.textContent = ext === 'pdf' ? 'picture_as_pdf' : 'image';

    // Responsive animation: update button with Ready to Push status
    const studentName = document.getElementById('targetStudentName').textContent || 'Student';
    const firstName = studentName.split(' ')[0];
    if (submitText) submitText.textContent = `Push Transcript to ${firstName}`;
    if (submitBtn) {
      submitBtn.classList.add('ring-2', 'ring-emerald-500/25');
    }
  };

  window.clearSelectedUploadFile = function(e) {
    if (e) e.stopPropagation();
    const input = document.getElementById('modalFileInput');
    if (input) input.value = '';

    const promptEl = document.getElementById('dropzonePrompt');
    const badgeEl = document.getElementById('dropzoneSelectedFile');
    const submitBtn = document.getElementById('btnSubmitUpload');
    const submitText = document.getElementById('btnSubmitUploadText');

    if (promptEl) promptEl.classList.remove('hidden');
    if (badgeEl) {
      badgeEl.classList.add('hidden');
      badgeEl.classList.remove('flex');
    }
    if (submitText) submitText.textContent = 'Push Transcript';
    if (submitBtn) submitBtn.classList.remove('ring-2', 'ring-emerald-500/25');
  };

  window.submitTranscriptUpload = async function(event) {
    event.preventDefault();
    const hiddenId = document.getElementById('hiddenUploadStudentId');
    const sel = document.getElementById('selectUploadStudent');
    const studentId = (hiddenId && hiddenId.value) || (sel && sel.value) || '';
    const studentObj = reportsData.find(s => s.id === studentId);
    const studentName = studentObj ? studentObj.name : studentId;
    const classGrade = studentObj ? studentObj.class : 'Grade 10A';

    const termSel = document.getElementById('selectUploadTerm');
    const notesInput = document.getElementById('inputUploadNotes');
    const fileInput = document.getElementById('modalFileInput');
    const alertEl = document.getElementById('uploadErrorAlert');
    const msgEl = document.getElementById('uploadErrorMessage');
    const loadingEl = document.getElementById('uploadLoadingState');
    const loadingText = document.getElementById('uploadLoadingText');
    const progressPct = document.getElementById('uploadProgressPct');
    const progressBar = document.getElementById('uploadProgressBar');
    const submitBtn = document.getElementById('btnSubmitUpload');

    const file = fileInput && fileInput.files && fileInput.files[0];
    if (!file) {
      if (alertEl) alertEl.classList.remove('hidden');
      if (msgEl) msgEl.textContent = 'Please choose a transcript file (PDF or image) to upload.';
      return;
    }

    const term = termSel ? termSel.value : 'Semester 1 (2025–26)';
    const notes = notesInput ? notesInput.value.trim() : '';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('studentId', studentId);
    formData.append('studentName', studentName);
    formData.append('classGrade', classGrade);
    formData.append('term', term);
    formData.append('notes', notes);

    // Responsive uploading animation
    if (alertEl) alertEl.classList.add('hidden');
    if (loadingEl) loadingEl.classList.remove('hidden');
    if (progressBar) {
      progressBar.style.width = '20%';
      progressBar.classList.remove('bg-emerald-600');
      progressBar.classList.add('bg-[#1e4d38]');
    }
    if (progressPct) progressPct.textContent = '20%';
    if (loadingText) loadingText.textContent = 'Packaging & encrypting transcript...';

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
      submitBtn.innerHTML = `
        <svg class="animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Pushing to Student Portal...</span>
      `;
    }

    // Step 2 of progress animation
    setTimeout(() => {
      if (progressBar && progressPct && loadingText && submitBtn && submitBtn.disabled) {
        progressBar.style.width = '65%';
        progressPct.textContent = '65%';
        loadingText.textContent = `Assigning to ${studentName}...`;
      }
    }, 280);

    try {
      const token = (window.NGISAuth && NGISAuth.getToken()) || 'mock-jwt-token-teacher';
      const res = await fetch('/api/academic/transcripts/upload', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
      });

      const json = await res.json();
      if (!res.ok || !json.success) {
        throw new Error((json && json.error && json.error.message) || json.message || 'Upload failed');
      }

      // Responsive Upload Done Animation
      if (progressBar) {
        progressBar.style.width = '100%';
        progressBar.classList.remove('bg-[#1e4d38]');
        progressBar.classList.add('bg-emerald-600');
      }
      if (progressPct) progressPct.textContent = '100%';
      if (loadingText) {
        loadingText.innerHTML = `
          <span class="text-emerald-700 font-medium flex items-center gap-1.5 animate-in fade-in">
            <span class="material-symbols-outlined text-[16px] text-emerald-600">check_circle</span>
            Pushed Successfully &bull; Live in Student Portal
          </span>
        `;
      }

      if (submitBtn) {
        submitBtn.classList.remove('bg-[#1e4d38]', 'ring-emerald-500/25');
        submitBtn.classList.add('bg-emerald-700');
        submitBtn.innerHTML = `
          <span class="material-symbols-outlined text-[16px] text-white">done_all</span>
          <span>Pushed &amp; Live</span>
        `;
      }

      // Smooth delay to celebrate completion before auto-closing
      setTimeout(async () => {
        await loadServerTranscripts();
        closeUploadTranscriptModal();

        // Responsive row highlight pulse on table
        const row = document.querySelector(`tr[data-student-id="${studentId}"]`);
        if (row) {
          row.classList.add('animate-row-highlight');
          row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          setTimeout(() => row.classList.remove('animate-row-highlight'), 2200);
        }

        if (window.toast) {
          window.toast(`Transcript pushed to ${studentName} and live in student portal!`, 'success');
        }

        // If preview modal was open for this student, update it
        const previewModal = document.getElementById('modalReportCard');
        if (previewModal && !previewModal.classList.contains('hidden') && activePreviewStudentId === studentId) {
          previewReport(studentId);
        }
      }, 750);

    } catch (err) {
      if (loadingEl) loadingEl.classList.add('hidden');
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75', 'cursor-not-allowed', 'bg-emerald-700');
        submitBtn.classList.add('bg-[#1e4d38]');
        submitBtn.innerHTML = `
          <span class="material-symbols-outlined text-[16px]">publish</span>
          <span id="btnSubmitUploadText">Push Transcript</span>
        `;
      }
      if (alertEl) alertEl.classList.remove('hidden');
      if (msgEl) msgEl.textContent = err.message || 'Network error occurred during upload. Please try again.';
    }
  };\n\n'

start_idx = text.find(start_marker)
if start_idx == -1:
    start_idx = text.find(start_marker.replace('\n', '\r\n'))

end_idx = text.find(end_marker)
if end_idx == -1:
    end_idx = text.find(end_marker.replace('\n', '\r\n'))

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_upload_js + text[end_idx:]
    print("Replaced upload JS block successfully!")
else:
    print(f"Indices: start={start_idx}, end={end_idx}")

with open('pages/teacher/teacher-reports.html', 'w', encoding='utf-8') as f:
    f.write(text)

