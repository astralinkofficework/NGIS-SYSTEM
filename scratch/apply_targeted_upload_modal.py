import re

with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add CSS animations in <style data-purpose="custom-rules">
css_target = '/* Crisp hairline spreadsheet dividers */'
css_replacement = '''  /* Upload & Responsive Motion Animations */
  @keyframes dropzonePop {
    0% { transform: scale(0.97); opacity: 0.8; }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); opacity: 1; }
  }
  .animate-dropzone-pop {
    animation: dropzonePop 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }

  @keyframes rowHighlight {
    0% { background-color: rgba(16, 185, 129, 0.24); }
    50% { background-color: rgba(16, 185, 129, 0.12); }
    100% { background-color: transparent; }
  }
  .animate-row-highlight {
    animation: rowHighlight 2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  }

  /* Crisp hairline spreadsheet dividers */'''

def do_replace(content, old, new):
    if old in content:
        return content.replace(old, new)
    elif old.replace('\n', '\r\n') in content:
        return content.replace(old.replace('\n', '\r\n'), new.replace('\n', '\r\n'))
    return content

text = do_replace(text, css_target, css_replacement)

# 2. Update Modal HTML inside #modalUploadTranscript
modal_target = '''        <!-- Student Selection -->
        <div>
          <label class="block text-xs font-medium text-slate-700 mb-1" for="selectUploadStudent">
            Select Student <span class="text-rose-500">*</span>
          </label>
          <select id="selectUploadStudent" required class="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:border-brand-700 focus:ring-1 focus:ring-brand-700 text-slate-800 cursor-pointer">
            <!-- Populated dynamically via JS -->
          </select>
        </div>'''

modal_replacement = '''        <!-- Target Student Profile Card (Shows only the selected student's info, not all students) -->
        <div id="targetStudentInfoCard" class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between gap-3 transition-all duration-200 shadow-2xs">
          <div class="flex items-center gap-3 min-w-0">
            <div class="w-10 h-10 rounded-xl bg-[#1e4d38] text-white flex items-center justify-center font-medium text-sm flex-shrink-0 shadow-2xs" id="targetStudentInitials">
              NH
            </div>
            <div class="min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="text-xs sm:text-sm font-medium text-slate-900 truncate" id="targetStudentName">Nrinphouneta Hok</span>
                <span class="inline-flex items-center gap-1 text-[10px] font-medium text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 flex-shrink-0">
                  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Targeted Student
                </span>
              </div>
              <div class="text-[11px] text-slate-500 mt-0.5 font-mono truncate" id="targetStudentMeta">
                ID: 2026-STD-0142 &bull; Class: Grade 10A &bull; Semester 1
              </div>
            </div>
          </div>
          <button type="button" id="btnChangeTargetStudent" onclick="toggleStudentSelector(true)" class="text-[11px] text-[#1e4d38] hover:underline font-medium flex-shrink-0 hidden">
            Change
          </button>
        </div>

        <!-- Optional Student Selector (Only if opened globally without pre-selected student) -->
        <div id="studentSelectContainer" class="hidden">
          <label class="block text-xs font-medium text-slate-700 mb-1" for="selectUploadStudent">
            Select Student <span class="text-rose-500">*</span>
          </label>
          <select id="selectUploadStudent" onchange="onSelectStudentChange(this.value)" class="w-full px-3 py-2 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:bg-white focus:border-brand-700 text-slate-800 cursor-pointer">
            <!-- Populated dynamically via JS -->
          </select>
        </div>

        <input type="hidden" id="hiddenUploadStudentId" value="">'''

text = do_replace(text, modal_target, modal_replacement)

# 3. Update File Dropzone HTML with "Ready to Push" badge & styling
dropzone_file_old = '''            <!-- File selected badge -->
            <div id="dropzoneSelectedFile" class="hidden items-center justify-between bg-white border border-emerald-300 rounded-lg p-3 text-left">
              <div class="flex items-center gap-2.5 min-w-0">
                <span class="material-symbols-outlined text-[24px] text-emerald-600 flex-shrink-0" id="selectedFileIcon">description</span>
                <div class="min-w-0 truncate">
                  <div class="font-medium text-slate-900 truncate" id="selectedFileName">filename.pdf</div>
                  <div class="text-[11px] text-slate-500 font-mono" id="selectedFileSize">0 KB</div>
                </div>
              </div>
              <button type="button" onclick="clearSelectedUploadFile(event)" class="text-slate-400 hover:text-rose-600 p-1" title="Change file">
                <span class="material-symbols-outlined text-[16px]">close</span>
              </button>
            </div>'''

dropzone_file_new = '''            <!-- File selected badge with responsive Ready to Push animation -->
            <div id="dropzoneSelectedFile" class="hidden items-center justify-between bg-white border border-emerald-300 rounded-xl p-3.5 text-left transition-all duration-300 shadow-xs">
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center flex-shrink-0 border border-emerald-200">
                  <span class="material-symbols-outlined text-[24px]" id="selectedFileIcon">picture_as_pdf</span>
                </div>
                <div class="min-w-0 truncate">
                  <div class="flex items-center gap-2">
                    <span class="font-medium text-slate-900 truncate text-xs" id="selectedFileName">filename.pdf</span>
                    <span id="readyToPushBadge" class="inline-flex items-center gap-1 text-[10px] font-medium text-emerald-800 bg-emerald-100/70 border border-emerald-300 px-2 py-0.5 rounded-full animate-pulse flex-shrink-0">
                      <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Ready to Push
                    </span>
                  </div>
                  <div class="text-[11px] text-slate-500 font-mono mt-0.5" id="selectedFileSize">0 KB</div>
                </div>
              </div>
              <button type="button" onclick="clearSelectedUploadFile(event)" class="text-slate-400 hover:text-rose-600 p-1.5 rounded-lg hover:bg-slate-50 transition" title="Change file">
                <span class="material-symbols-outlined text-[16px]">close</span>
              </button>
            </div>'''

text = do_replace(text, dropzone_file_old, dropzone_file_new)

# 4. Update Loading/Progress State HTML
loading_old = '''        <!-- Loading / Progress State -->
        <div id="uploadLoadingState" class="hidden p-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 space-y-2">
          <div class="flex items-center justify-between text-[11px]">
            <span class="flex items-center gap-1.5 font-medium">
              <svg class="animate-spin h-3.5 w-3.5 text-brand-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              Uploading &amp; securely storing file...
            </span>
            <span class="font-mono text-slate-500" id="uploadProgressPct">Saving...</span>
          </div>
          <div class="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
            <div id="uploadProgressBar" class="bg-brand-700 h-1.5 rounded-full transition-all duration-300 w-3/4 animate-pulse"></div>
          </div>
        </div>'''

loading_new = '''        <!-- Loading / Progress State with Responsive Animation -->
        <div id="uploadLoadingState" class="hidden p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-700 space-y-2.5 transition-all duration-300">
          <div class="flex items-center justify-between text-[11px]">
            <span class="flex items-center gap-2 font-medium text-slate-800" id="uploadStatusLabel">
              <svg class="animate-spin h-3.5 w-3.5 text-emerald-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              <span id="uploadLoadingText">Pushing transcript to student portal...</span>
            </span>
            <span class="font-mono text-emerald-700 font-medium" id="uploadProgressPct">0%</span>
          </div>
          <div class="w-full bg-slate-200 rounded-full h-2 overflow-hidden">
            <div id="uploadProgressBar" class="bg-[#1e4d38] h-full rounded-full transition-all duration-300 ease-out" style="width: 15%"></div>
          </div>
        </div>'''

text = do_replace(text, loading_old, loading_new)

# 5. Update Submit Button inside modal
btn_old = '''          <button type="submit" id="btnSubmitUpload" class="px-4 py-2 text-xs font-medium rounded-lg bg-[#1e4d38] text-white hover:bg-[#163b2a] shadow-xs transition active:scale-95 inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">upload</span>
            <span>Upload &amp; Assign</span>
          </button>'''

btn_new = '''          <button type="submit" id="btnSubmitUpload" class="px-4 py-2 text-xs font-medium rounded-lg bg-[#1e4d38] text-white hover:bg-[#163b2a] shadow-xs transition active:scale-95 inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px] transition-transform duration-200">publish</span>
            <span id="btnSubmitUploadText">Push Transcript</span>
          </button>'''

text = do_replace(text, btn_old, btn_new)

with open('pages/teacher/teacher-reports.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("HTML structure updated for targeted student info card and responsive animations!")

