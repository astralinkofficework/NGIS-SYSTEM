import re

clearance_pill = '''      <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
        <i class="ph ph-chalkboard-teacher text-xs"></i>
        <span>Dr. Sarah Jenkins</span>
      </span>
      <!-- Principal Clearance Status Pill -->
      <span id="principalClearanceBadge" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#202F63]/10 text-[#202F63] border border-[#202F63]/30">
        <span class="w-1.5 h-1.5 rounded-full bg-[#202F63]"></span>
        <span id="principalClearanceText">Verified &amp; Published by Academic Principal</span>
      </span>'''

revision_banner = '''<!-- END: AcademicOfficialBanner -->
<div id="principalRevisionBanner" class="hidden"></div>'''

script_block = '''
<script>
// Live Principal Clearance Synchronization
async function refreshClearanceStatus() {
  try {
    const cohort = document.getElementById('cohortSelect')?.value || '10A';
    const classId = 'cls-' + cohort.toLowerCase();
    const examType = document.getElementById('examTypeSelect')?.value || 'sem2';
    const periodId = examType === 'sem1' ? 'gp-q1' : 'gp-sem2';

    const res = await fetch(`/api/academic/gradebook/clearance-status?classId=${classId}&periodId=${periodId}`);
    if (res.ok) {
      const data = await res.json();
      const badge = document.getElementById('principalClearanceBadge');
      const text = document.getElementById('principalClearanceText');
      const banner = document.getElementById('principalRevisionBanner');
      
      if (!badge || !text) return;

      if (data.status === 'approved' || data.workflow === 'published') {
        badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#202F63]/10 text-[#202F63] border border-[#202F63]/30';
        badge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-[#202F63]"></span><span>Verified &amp; Published by Academic Principal</span>';
        if (banner) banner.classList.add('hidden');
      } else if (data.status === 'pending' || data.workflow === 'submitted') {
        badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#92243D]/10 text-[#92243D] border border-[#92243D]/30';
        badge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-[#92243D] animate-pulse"></span><span>Pending Principal Clearance</span>';
        if (banner) banner.classList.add('hidden');
      } else if (data.status === 'needs_correction' || data.workflow === 'returned') {
        badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#92243D] text-white';
        badge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-white animate-ping"></span><span>Revisions Requested by Principal</span>';
        if (banner) {
          banner.className = 'p-3 rounded-xl bg-[#92243D]/10 border border-[#92243D] text-xs text-[#92243D] flex items-center justify-between my-3';
          banner.innerHTML = `<div><span class="font-medium">Principal Revision Note:</span> "${data.decisionNote || 'Please verify assessment weights and resubmit.'}"</div><button onclick="saveAllScores()" class="px-3 py-1 bg-[#92243D] text-white rounded-lg text-xs font-medium hover:bg-[#7A1D32]">Resubmit for Clearance</button>`;
          banner.classList.remove('hidden');
        }
      } else {
        badge.className = 'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-[#F3F3F5] text-[#000000] border border-[#E5E5E8]';
        badge.innerHTML = '<span class="w-1.5 h-1.5 rounded-full bg-[#000000]"></span><span>Draft Score Sheet</span>';
        if (banner) banner.classList.add('hidden');
      }
    }
  } catch(e) {
    console.warn('Failed to refresh clearance status:', e);
  }
}

document.addEventListener('DOMContentLoaded', refreshClearanceStatus);
setTimeout(refreshClearanceStatus, 500);
</script>
'''

target_teacher_span = '''      <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
        <i class="ph ph-chalkboard-teacher text-xs"></i>
        <span>Dr. Sarah Jenkins</span>
      </span>'''

for fname in ['pages/teacher/teacher-grades.html', 'pages/teacher/teacher-gradebook.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    if target_teacher_span in content and 'principalClearanceBadge' not in content:
        content = content.replace(target_teacher_span, clearance_pill)
    
    if '<!-- END: AcademicOfficialBanner -->' in content and 'principalRevisionBanner' not in content:
        content = content.replace('<!-- END: AcademicOfficialBanner -->', revision_banner)
    
    if 'refreshClearanceStatus' not in content:
        content = content.replace('</body>', script_block + '\n</body>')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {fname} with live Principal clearance synchronization.")

