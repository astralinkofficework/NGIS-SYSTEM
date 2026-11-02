with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = """        <button id="btnDownloadZip" onclick="downloadAttachmentsZip()" class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 hover:text-slate-900 transition shadow-xs active:scale-95" type="button">
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Download Attachments (.ZIP)</span>
        </button>

        <button id="btnUploadAssignmentOrWork" onclick="openUploadModal()" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-white bg-[#202F63] hover:bg-[#18234D] border border-[#202F63] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#202F63]" type="button">
          <svg class="w-3.5 h-3.5 text-[#000000]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Upload Assignment / Work</span>
        </button>

        <button id="btnBatchPublish" onclick="batchPublishGrades()" class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 hover:text-slate-900 transition shadow-xs active:scale-95" type="button">
          <svg class="w-3.5 h-3.5 text-[#000000]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Batch Publish Grades</span>
        </button>"""

replacement = """        <button id="btnUploadAssignmentOrWork" onclick="openUploadModal()" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-white bg-[#202F63] hover:bg-[#18234D] border border-[#202F63] rounded-lg shadow-xs transition active:scale-95 focus:ring-2 focus:ring-offset-2 focus:ring-[#202F63]" type="button">
          <svg class="w-3.5 h-3.5 text-[#000000]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          <span>Upload Assignment / Work</span>
        </button>"""

target_crlf = target.replace('\r\n', '\n').replace('\n', '\r\n')
replacement_crlf = replacement.replace('\r\n', '\n').replace('\n', '\r\n')

if target in c:
    c = c.replace(target, replacement)
    print('Replaced LF')
elif target_crlf in c:
    c = c.replace(target_crlf, replacement_crlf)
    print('Replaced CRLF')
else:
    print('Target not matched')

with open('pages/teacher/teacher-submissions.html', 'w', encoding='utf-8') as f:
    f.write(c)

