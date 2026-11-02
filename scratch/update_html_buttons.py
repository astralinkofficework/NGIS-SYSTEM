import os, re

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

# Let's inspect what buttons have bg-[#202F63] or bg-brand-700 or bg-primary
# We want to convert PRIMARY buttons to Burgundy #92243D
# BUT we want to preserve secondary buttons and tabs/filters (e.g. category filter tabs like 'active' tab should not be confused with primary action buttons)

actions_to_burgundy = []

for path in html_files:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    orig = content
    
    # 1. Primary buttons with explicit bg-[#202F63] that are actions:
    # e.g., btnUploadAssignmentOrWork, btnAddClass, btnAddStudent, saveScore, submit, etc.
    # Replace bg-[#202F63] hover:bg-[#18234D] with bg-[#92243D] hover:bg-[#7A1D32]
    content = content.replace('bg-[#202F63] hover:bg-[#18234D]', 'bg-[#92243D] hover:bg-[#7A1D32]')
    content = content.replace('bg-[#202F63] hover:bg-[#000000]', 'bg-[#92243D] hover:bg-[#7A1D32]')
    content = content.replace('hover:bg-[#202F63] bg-[#202F63]', 'hover:bg-[#7A1D32] bg-[#92243D]')
    
    # 2. In teacher-submissions.html, teacher-classes.html, teacher-lost-found.html, teacher-services.html:
    # Specific primary action buttons:
    # #btnUploadAssignmentOrWork, saveAndPublishMark, btnSubmitUpload, submitHandover, submitComment
    
    # 3. In admin pages:
    # Save Section, Create Department, Add Class, Add Student
    content = re.sub(r'bg-brand-700\s+hover:bg-brand-800\s+text-white', 'bg-[#92243D] hover:bg-[#7A1D32] text-white', content)
    content = re.sub(r'bg-brand-700\s+text-white\s+hover:bg-brand-800', 'bg-[#92243D] text-white hover:bg-[#7A1D32]', content)
    
    # 4. In forms with type="submit":
    # If it has bg-[#202F63]
    content = re.sub(r'(<button[^>]*type="submit"[^>]*class="[^"]*)\bbg-\[#202F63\]\b([^"]*")', r'\1bg-[#92243D]\2', content)
    
    # 5. In teacher-submissions.html:
    # <button type="button" onclick="saveAndPublishMark()" class="flex-1 py-2 px-3 text-xs font-medium text-white bg-[#202F63]
    # <button type="button" id="btnSubmitUpload" onclick="submitUploadModal()" class="px-4 py-2 text-xs font-medium text-white bg-[#202F63]
    content = content.replace("bg-[#202F63] text-white font-medium text-xs rounded-xl", "bg-[#92243D] text-white font-medium text-xs rounded-xl")
    
    # 6. In teacher-lost-found.html:
    # submitHandover, verifyClaim
    content = content.replace('text-xs font-medium bg-[#202F63] text-white rounded-lg hover:bg-[#18234D]', 'text-xs font-medium bg-[#92243D] text-white rounded-lg hover:bg-[#7A1D32]')
    content = content.replace('px-4 py-1.5 text-xs font-medium bg-[#202F63] text-white rounded-lg', 'px-4 py-1.5 text-xs font-medium bg-[#92243D] text-white rounded-lg')
    content = content.replace("px-2.5 py-1 bg-[#202F63] text-white text-[11px] font-medium rounded-md", "px-2.5 py-1 bg-[#92243D] text-white text-[11px] font-medium rounded-md")
    
    # 7. In teacher-services.html:
    # submitComment, newRequestBtn
    content = content.replace('px-3.5 py-2 bg-[#202F63] text-white text-xs font-medium rounded-xl', 'px-3.5 py-2 bg-[#92243D] text-white text-xs font-medium rounded-xl')
    
    # 8. In teacher-reports.html:
    # btnSubmitUpload
    content = content.replace('text-xs font-medium text-white bg-[#202F63] hover:bg-[#18234D]', 'text-xs font-medium text-white bg-[#92243D] hover:bg-[#7A1D32]')
    content = content.replace('bg-brand-700 text-white rounded-lg hover:bg-brand-800', 'bg-[#92243D] text-white rounded-lg hover:bg-[#7A1D32]')

    # 9. In admin pages:
    content = content.replace('bg-[#202F63] text-white text-xs font-medium rounded-xl', 'bg-[#92243D] text-white text-xs font-medium rounded-xl')
    content = content.replace('border-[#202F63] bg-[#202F63]', 'border-[#92243D] bg-[#92243D]')
    content = content.replace('focus:ring-[#202F63]', 'focus:ring-[#92243D]')

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        actions_to_burgundy.append(path)

print(f'Updated primary action buttons in {len(actions_to_burgundy)} HTML files.')

