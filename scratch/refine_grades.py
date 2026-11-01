with open('pages/student/student-grades.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the top controls & table wrapping with clean stats strip + clean card head
old_top_section = '''      <!-- Section Controls & View Switcher -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 class="text-xl sm:text-2xl font-normal font-display text-forest-800 tracking-tight">
            Academic Report Cards &amp; Evaluation Record
          </h2>
          <p class="text-xs sm:text-sm text-ink-muted mt-0.5 font-medium">
            Official semester records, monthly reviews, and performance evaluations
          </p>
        </div>
        <div class="flex items-center gap-2.5 self-start sm:self-auto">
          <!-- Transcript Export Button -->
          <button type="button" onclick="openReportCardModal()" class="flex items-center gap-1.5 px-3.5 py-2 text-xs font-normal rounded-xl bg-white border border-surface-border text-ink-main shadow-xs hover:bg-surface-subtle transition-all">
            <span class="material-symbols-outlined text-[17px] text-forest-700">description</span>
            <span>Export Official PDF</span>
          </button>
        </div>
      </div>'''

new_top_section = '''  <!-- Summary Stats Strip -->
  <div class="stat-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px;">
    <div class="stat" style="background:#ffffff; border-radius:16px; border:1px solid rgba(184,219,217,0.45); padding:16px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
        <div style="width:36px; height:36px; border-radius:10px; background:rgba(46,111,94,0.12); color:#2e6f5e; display:flex; align-items:center; justify-content:center;">
          <span class="material-symbols-outlined fill">star</span>
        </div>
        <span style="font-size:11px; padding:2px 8px; border-radius:999px; background:rgba(46,111,94,0.1); color:#2e6f5e; font-weight:500;">Top 5%</span>
      </div>
      <div style="font-size:24px; font-weight:500; color:#13829b;">3.88 / 4.00</div>
      <div style="font-size:12px; color:var(--txt3, #586f7c); margin-top:2px;">Cumulative GPA</div>
    </div>
    
    <div class="stat" style="background:#ffffff; border-radius:16px; border:1px solid rgba(184,219,217,0.45); padding:16px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
        <div style="width:36px; height:36px; border-radius:10px; background:rgba(47,69,80,0.1); color:#2f4550; display:flex; align-items:center; justify-content:center;">
          <span class="material-symbols-outlined fill">school</span>
        </div>
        <span style="font-size:11px; padding:2px 8px; border-radius:999px; background:rgba(47,69,80,0.08); color:#2f4550; font-weight:500;">Honors</span>
      </div>
      <div style="font-size:24px; font-weight:500; color:var(--txt, #111b15);">28.0 Credits</div>
      <div style="font-size:12px; color:var(--txt3, #586f7c); margin-top:2px;">Completed Units</div>
    </div>

    <div class="stat" style="background:#ffffff; border-radius:16px; border:1px solid rgba(184,219,217,0.45); padding:16px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
        <div style="width:36px; height:36px; border-radius:10px; background:rgba(140,98,43,0.12); color:#8c622b; display:flex; align-items:center; justify-content:center;">
          <span class="material-symbols-outlined fill">pending_actions</span>
        </div>
        <span style="font-size:11px; padding:2px 8px; border-radius:999px; background:rgba(140,98,43,0.1); color:#8c622b; font-weight:500;">Active</span>
      </div>
      <div style="font-size:24px; font-weight:500; color:var(--txt, #111b15);">Semester 2</div>
      <div style="font-size:12px; color:var(--txt3, #586f7c); margin-top:2px;">Current Academic Term</div>
    </div>

    <div class="stat" style="background:#ffffff; border-radius:16px; border:1px solid rgba(184,219,217,0.45); padding:16px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
      <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
        <div style="width:36px; height:36px; border-radius:10px; background:rgba(30,77,56,0.12); color:#1e4d38; display:flex; align-items:center; justify-content:center;">
          <span class="material-symbols-outlined fill">military_tech</span>
        </div>
        <span style="font-size:11px; padding:2px 8px; border-radius:999px; background:rgba(30,77,56,0.1); color:#1e4d38; font-weight:500;">Standing</span>
      </div>
      <div style="font-size:24px; font-weight:500; color:#1e4d38;">Tier 1 Dean's List</div>
      <div style="font-size:12px; color:var(--txt3, #586f7c); margin-top:2px;">Academic Status</div>
    </div>
  </div>

  <div class="card" style="background:#ffffff; border-radius:16px; border:1px solid rgba(184,219,217,0.45); box-shadow:0 1px 3px rgba(15,23,42,0.04); overflow:hidden; margin-bottom:24px;">
    <div style="padding:16px 20px; border-bottom:1px solid rgba(184,219,217,0.35); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
      <div>
        <h3 style="font-size:16px; margin:0; color:var(--txt, #111b15); font-weight:500;">Authoritative Academic Record</h3>
        <div style="font-size:12px; color:var(--txt3, #586f7c); margin-top:2px;">Official semester report cards, continuous assessments, and transcripts</div>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <button type="button" onclick="openReportCardModal()" style="display:inline-flex; align-items:center; gap:6px; padding:7px 14px; border-radius:8px; background:#13829b; color:#ffffff; font-size:12.5px; font-weight:500; transition:all 0.15s ease;">
          <span class="material-symbols-outlined text-[16px]">description</span>
          <span>Export Official PDF</span>
        </button>
      </div>
    </div>'''

if old_top_section in c:
    c = c.replace(old_top_section, new_top_section)
    # Also adjust closing tag of the card
    c = c.replace('      <!-- Comprehensive Editorial Table View -->\n      <div class="bg-white rounded-3xl border border-surface-border shadow-xs overflow-hidden">', '')
    with open('pages/student/student-grades.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Replaced top section in student-grades.html")
else:
    print("Old top section not found")

