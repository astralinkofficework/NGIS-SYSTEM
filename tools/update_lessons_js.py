with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the modal helpers section
old_section = '''  // Modal helpers
  window.openUploadModal = function() {
    const modal = document.getElementById('uploadModal');
    if (modal) {
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }
  };

  window.closeUploadModal = function() {
    const modal = document.getElementById('uploadModal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }
  };

  window.previewLessonById = function(id) {
    const m = materials.find(x => x.id === id) || materials[0];
    if (!m) return;
    document.getElementById('previewTitle').textContent = m.title;
    document.getElementById('previewClass').textContent = m.cohortLabel;
    document.getElementById('previewSubject').textContent = m.subject;
    document.getElementById('previewFormat').textContent = m.formatLabel + ' Document';
    const modal = document.getElementById('previewModal');
    if (modal) {
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }
  };

  window.closePreviewModal = function() {
    const modal = document.getElementById('previewModal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }
  };

  window.downloadLesson = function(id) {
    const m = materials.find(x => x.id === id);
    if (window.toast) {
      window.toast(`Downloading ${m ? m.fileName : 'material'}...`, 'info');
    } else {
      alert(`Downloading ${m ? m.fileName : 'material'}...`);
    }
  };

  window.downloadPreviewDoc = function() {
    closePreviewModal();
    if (window.toast) window.toast('Downloading document...', 'info');
  };

  window.deleteLesson = function(id) {
    if (!confirm('Are you sure you want to delete this course material?')) return;
    materials = materials.filter(m => m.id !== id);
    filterTable();
    if (window.toast) window.toast('Material deleted from repository', 'success');
  };

  window.handleLessonSubmit = function(e) {
    e.preventDefault();
    const title = document.getElementById('inputLessonTitle').value.trim();
    const cohort = document.getElementById('selectClassId').value;
    const subject = document.getElementById('selectSubjectId').value;
    const format = document.querySelector('input[name="resource_format"]:checked').value;

    const newMat = {
      id: Date.now(),
      title: title || 'New Lesson Topic',
      fileName: (title || 'lesson').toLowerCase().replace(/[^a-z0-9]/g, '_') + '.' + (format === 'deck' ? 'pptx' : format === 'doc' ? 'docx' : 'pdf'),
      fileSize: '3.4 MB',
      cohort: cohort,
      cohortLabel: cohort === '10A' ? 'Grade 10A' : 'Grade 11B',
      subject: subject,
      format: format,
      formatLabel: format.toUpperCase(),
      date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
      views: '0 views',
      reachPercent: 0
    };

    materials.unshift(newMat);
    closeUploadModal();
    filterTable();
    if (window.toast) window.toast('Lesson published to class vault', 'success');
  };'''

new_section = '''  // Multi-file state and management
  let attachedFiles = [
    { name: 'calculus_chain_rule_handout.pdf', size: '4.2 MB', type: 'application/pdf' }
  ];

  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  window.handleLessonFilesSelect = function(files) {
    if (!files || !files.length) return;
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      if (!attachedFiles.some(f => f.name === file.name)) {
        attachedFiles.push({
          name: file.name,
          size: formatBytes(file.size),
          type: file.type || 'application/octet-stream'
        });
      }
    }
    renderAttachedFiles();
  };

  window.removeAttachedFile = function(index) {
    attachedFiles.splice(index, 1);
    renderAttachedFiles();
  };

  window.renderAttachedFiles = function() {
    const list = document.getElementById('attachedFilesList');
    const countEl = document.getElementById('uploadFileCount');
    if (countEl) countEl.textContent = `${attachedFiles.length} file${attachedFiles.length === 1 ? '' : 's'} attached`;
    if (!list) return;

    if (attachedFiles.length === 0) {
      list.innerHTML = `
        <div class="p-2 rounded bg-surface-container-lowest border border-dashed border-outline-variant/60 text-center text-xs text-outline">
          No files attached yet. Click above or drag files to add.
        </div>
      `;
      return;
    }

    list.innerHTML = attachedFiles.map((file, idx) => {
      const isPdf = file.name.endsWith('.pdf');
      const isSlide = file.name.endsWith('.ppt') || file.name.endsWith('.pptx');
      const iconName = isPdf ? 'picture_as_pdf' : (isSlide ? 'slideshow' : 'description');
      const iconColor = isPdf ? 'text-error' : 'text-[#0F5132]';
      return `
        <div class="flex items-center justify-between px-3 py-1.5 rounded-lg bg-surface-container-lowest border border-outline-variant/70 text-on-surface text-xs shadow-xs">
          <div class="flex items-center gap-2 min-w-0">
            <span class="material-symbols-outlined ${iconColor} text-[18px] shrink-0">${iconName}</span>
            <span class="font-mono font-medium truncate max-w-[280px]">${esc(file.name)}</span>
            <span class="text-outline shrink-0">· ${file.size}</span>
          </div>
          <button type="button" onclick="removeAttachedFile(${idx})" class="w-6 h-6 rounded flex items-center justify-center text-outline hover:text-error hover:bg-error-container/20 transition-colors" title="Remove file" aria-label="Remove ${esc(file.name)}">
            <span class="material-symbols-outlined text-[16px]">close</span>
          </button>
        </div>
      `;
    }).join('');
  };

  // Modal helpers
  window.openUploadModal = function() {
    const modal = document.getElementById('uploadModal');
    if (modal) {
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      document.body.style.overflow = 'hidden';
      document.body.classList.add('modal-open');
      renderAttachedFiles();
    }
  };

  window.closeUploadModal = function() {
    const modal = document.getElementById('uploadModal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      document.body.style.overflow = '';
      document.body.classList.remove('modal-open');
    }
  };

  window.previewLessonById = function(id) {
    const m = materials.find(x => x.id === id) || materials[0];
    if (!m) return;
    // Seamless routing to shared interactive lesson details
    const targetUrl = `../shared/lesson-details.html?id=${m.id}&dept=${encodeURIComponent(m.subject.toLowerCase())}&portal=teacher`;
    window.location.href = targetUrl;
  };

  window.closePreviewModal = function() {
    const modal = document.getElementById('previewModal');
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
      document.body.style.overflow = '';
      document.body.classList.remove('modal-open');
    }
  };

  window.downloadLesson = function(id) {
    const m = materials.find(x => x.id === id);
    if (window.toast) {
      window.toast(`Downloading ${m ? m.fileName : 'material'}...`, 'info');
    } else {
      alert(`Downloading ${m ? m.fileName : 'material'}...`);
    }
  };

  window.downloadPreviewDoc = function() {
    closePreviewModal();
    if (window.toast) window.toast('Downloading document...', 'info');
  };

  window.deleteLesson = function(id) {
    if (!confirm('Are you sure you want to delete this course material?')) return;
    materials = materials.filter(m => m.id !== id);
    filterTable();
    if (window.toast) window.toast('Material deleted from repository', 'success');
  };

  window.handleLessonSubmit = function(e) {
    e.preventDefault();
    const title = document.getElementById('inputLessonTitle').value.trim();
    const cohort = document.getElementById('selectClassId').value;
    const subject = document.getElementById('selectSubjectId').value;
    const format = document.querySelector('input[name="resource_format"]:checked').value;

    if (attachedFiles.length === 0) {
      alert('Please attach at least one lesson document or handout.');
      return;
    }

    const primaryFile = attachedFiles[0];
    const newMat = {
      id: Date.now(),
      title: title || 'New Lesson Topic',
      fileName: primaryFile.name,
      fileSize: primaryFile.size + (attachedFiles.length > 1 ? ` (+${attachedFiles.length - 1} more)` : ''),
      cohort: cohort,
      cohortLabel: cohort === '10A' ? 'Grade 10A' : 'Grade 11B',
      subject: subject,
      format: format,
      formatLabel: format.toUpperCase(),
      date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
      views: '0 views',
      reachPercent: 0
    };

    materials.unshift(newMat);
    closeUploadModal();
    filterTable();

    if (window.NGIS_showOperationSuccess) {
      window.NGIS_showOperationSuccess({
        title: 'Lesson Material Published',
        message: `"${newMat.title}" with ${attachedFiles.length} file(s) has been successfully published to Grade ${cohort}.`
      });
    } else if (window.toast) {
      window.toast('Lesson published to class vault', 'success');
    }
  };'''

if old_section in code:
    code = code.replace(old_section, new_section)
    print("Replaced modal helpers successfully.")
else:
    print("Error: Could not find exact old_section.")

# Also add drag and drop event listeners inside DOMContentLoaded
old_listeners = '''    if (closeUploadBtn) closeUploadBtn.addEventListener('click', closeUploadModal);
    if (cancelUploadBtn) cancelUploadBtn.addEventListener('click', closeUploadModal);'''

new_listeners = '''    if (closeUploadBtn) closeUploadBtn.addEventListener('click', closeUploadModal);
    if (cancelUploadBtn) cancelUploadBtn.addEventListener('click', closeUploadModal);

    const dropzone = document.getElementById('lessonDropzone');
    if (dropzone) {
      ['dragenter', 'dragover'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzone.classList.add('border-primary', 'bg-primary-container/10');
        });
      });
      ['dragleave', 'drop'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropzone.classList.remove('border-primary', 'bg-primary-container/10');
        });
      });
      dropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer && e.dataTransfer.files) {
          handleLessonFilesSelect(e.dataTransfer.files);
        }
      });
    }'''

if old_listeners in code:
    code = code.replace(old_listeners, new_listeners)
    print("Added drag and drop listeners successfully.")

with open('pages/teacher/teacher-lessons.html', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated teacher-lessons.html")
