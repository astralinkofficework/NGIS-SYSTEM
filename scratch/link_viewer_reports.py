with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    content = f.read()

c = content.replace('\r\n', '\n')

old_header_btn = """        <button type="button" onclick="closePreviewModal()" class="text-white/70 hover:text-white p-1 rounded-lg hover:bg-white/10 transition" title="Close Preview">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>"""

new_header_btn = """        <div class="flex items-center gap-2">
          <a id="btnOpenFullTranscript" href="../shared/transcript-viewer.html" target="_blank" class="px-2.5 py-1 text-xs font-medium rounded-lg bg-emerald-700/60 hover:bg-emerald-700 text-white transition flex items-center gap-1.5" title="Open Official Academic Transcript Viewer">
            <span class="material-symbols-outlined text-[16px]">open_in_new</span>
            <span>Full Viewer</span>
          </a>
          <button type="button" onclick="closePreviewModal()" class="text-white/70 hover:text-white p-1 rounded-lg hover:bg-white/10 transition" title="Close Preview">
            <span class="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>"""

if old_header_btn in c:
    c = c.replace(old_header_btn, new_header_btn)
    print("Modal header button updated")
else:
    print("Modal header button NOT found")

# Update previewReport JS
old_js = """    if (nameEl) nameEl.textContent = r.name;
    if (idEl) idEl.textContent = `ID: ${r.id} · Class: ${r.class}`;
    if (initEl) initEl.textContent = initials;
    if (gpaEl) gpaEl.textContent = (r.gpa || 3.85).toFixed(2);"""

new_js = """    if (nameEl) nameEl.textContent = r.name;
    if (idEl) idEl.textContent = `ID: ${r.id} · Class: ${r.class}`;
    if (initEl) initEl.textContent = initials;
    if (gpaEl) gpaEl.textContent = (r.gpa || 3.85).toFixed(2);

    const btnFull = document.getElementById('btnOpenFullTranscript');
    if (btnFull) {
      btnFull.href = `../shared/transcript-viewer.html?name=${encodeURIComponent(r.name)}&id=${encodeURIComponent(r.id)}&gpa=${(r.gpa || 3.88).toFixed(2)}`;
    }"""

if old_js in c:
    c = c.replace(old_js, new_js)
    print("JS previewReport updated")
else:
    # try with character variation
    import re
    pattern = r'if \(nameEl\) nameEl\.textContent = r\.name;[\s\S]*?if \(gpaEl\) gpaEl\.textContent = \(r\.gpa \|\| 3\.85\)\.toFixed\(2\);'
    m = re.search(pattern, c)
    if m:
        c = c[:m.start()] + new_js + c[m.end():]
        print("JS previewReport updated with regex")
    else:
        print("JS previewReport NOT found")

with open('pages/teacher/teacher-reports.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("UPDATE COMPLETE")

