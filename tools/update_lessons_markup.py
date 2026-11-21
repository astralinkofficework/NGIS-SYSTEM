import re

with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update uploadModal backdrop and close buttons
# Replace uploadModal container tag
html = html.replace(
    'id="uploadModal">',
    'id="uploadModal" onclick="if(event.target === this) closeUploadModal()">'
)

# Fix closeUploadBtn
html = html.replace(
    '<button type="button" class="w-8 h-8 rounded-lg border border-outline-variant/60 flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container-low transition-colors" id="closeUploadBtn" title="Close dialog">',
    '<button type="button" onclick="closeUploadModal()" class="w-8 h-8 rounded-lg border border-outline-variant/60 flex items-center justify-center text-on-surface-variant hover:text-on-surface hover:bg-surface-container-low transition-colors" id="closeUploadBtn" title="Close dialog" aria-label="Close dialog">'
)

# Fix cancelUploadBtn
html = html.replace(
    '<button class="px-space-md py-2 rounded-lg border border-outline-variant/70 bg-surface-container-lowest font-label-md text-label-md text-on-surface hover:bg-surface-container transition-colors" id="cancelUploadBtn" type="button">',
    '<button onclick="closeUploadModal()" class="px-space-md py-2 rounded-lg border border-outline-variant/70 bg-surface-container-lowest font-label-md text-label-md text-on-surface hover:bg-surface-container transition-colors" id="cancelUploadBtn" type="button">'
)

# 2. Update File Attachment Area to support multi-file upload with drag-and-drop and chip list
old_dropzone = '''      <!-- Field 4: File Upload Area -->
      <div>
        <label class="block font-label-md text-label-md text-on-surface mb-1 font-medium">
          File Attachment <span class="text-error">*</span>
        </label>
        <div class="p-space-md border-2 border-dashed border-outline-variant rounded-xl bg-surface-container-low/50 text-center cursor-pointer flex flex-col items-center justify-center">
          <div class="w-12 h-12 rounded-full bg-surface-container flex items-center justify-center text-primary-container mb-2">
            <span class="material-symbols-outlined text-[24px]">cloud_upload</span>
          </div>
          <p class="font-headline-sm text-label-md text-on-surface font-medium">Drag &amp; drop file here, or browse files</p>
          <p class="font-body-sm text-[12px] text-on-surface-variant mt-0.5">Supports PDF, DOCX, PPTX up to 50MB</p>
          <!-- Attached sample file chip -->
          <div class="mt-space-sm inline-flex items-center gap-2 px-space-sm py-1 rounded bg-surface-container-lowest border border-outline-variant/70 text-on-surface font-body-sm text-[12px] shadow-xs">
            <span class="material-symbols-outlined text-error text-[16px]">picture_as_pdf</span>
            <span class="font-mono font-medium">calculus_chain_rule_handout.pdf</span>
            <span class="text-outline">· 4.2 MB</span>
          </div>
        </div>
      </div>'''

new_dropzone = '''      <!-- Field 4: File Upload Area (Multi-file Support) -->
      <div>
        <div class="flex items-center justify-between mb-1">
          <label class="block font-label-md text-label-md text-on-surface font-medium">
            Course Documents &amp; Materials <span class="text-error">*</span>
          </label>
          <span class="text-xs text-outline font-normal" id="uploadFileCount">0 files attached</span>
        </div>
        <div id="lessonDropzone" onclick="document.getElementById('lessonFileInput').click()" class="p-4 border-2 border-dashed border-outline-variant rounded-xl bg-surface-container-low/50 hover:bg-surface-container-low text-center cursor-pointer flex flex-col items-center justify-center transition-colors">
          <input type="file" id="lessonFileInput" multiple accept=".pdf,.doc,.docx,.ppt,.pptx,.xls,.xlsx,.zip" class="hidden" onchange="handleLessonFilesSelect(this.files)" />
          <div class="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center text-primary-container mb-2">
            <span class="material-symbols-outlined text-[22px]">cloud_upload</span>
          </div>
          <p class="font-headline-sm text-sm text-on-surface font-medium">Drag &amp; drop files here, or <span class="text-[#0F5132] underline">browse files</span></p>
          <p class="text-xs text-on-surface-variant mt-0.5">Supports PDF, DOCX, PPTX up to 50MB per file (multi-file allowed)</p>
        </div>

        <!-- Attached files list container -->
        <div id="attachedFilesList" class="mt-2.5 space-y-1.5 max-h-40 overflow-y-auto"></div>
      </div>'''

if old_dropzone in html:
    html = html.replace(old_dropzone, new_dropzone)
    print("Replaced dropzone successfully.")
else:
    print("Could not find exact old_dropzone string, trying normalized match...")

with open('pages/teacher/teacher-lessons.html', 'w', encoding='utf-8') as f:
    f.write(html)
