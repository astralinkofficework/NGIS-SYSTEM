import re

path = 'pages/principal/principal.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ensure Approvals Queue in desktop view has id="dtApprovalsList"
old_panel2 = re.search(r'<!-- Panel 2: Pending Approvals Queue -->.*?</div>\s*</div>\s*<!-- Live Campus Operations Feed -->', content, re.DOTALL)
if old_panel2:
    new_panel2 = '''<!-- Panel 2: Pending Approvals Queue -->
            <div class="ov-inner-panel">
              <div class="ov-inner-head" style="display:flex;justify-content:space-between;align-items:center">
                <span style="display:flex;align-items:center;gap:6px"><span class="material-symbols-outlined" style="color:#202F63">verified_user</span>Approvals Queue (<span id="dtApprovalsCount">3</span>)</span>
                <a href="principal-approvals.html" style="font-size:11px;color:#92243D;text-decoration:none;font-weight:500">Manage &rarr;</a>
              </div>
              <div id="dtApprovalsList">
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Grade Correction: Grade 11 Calculus</div>
                  <div class="ov-inner-item-s">Submitted by Dr. Sarah Jenkins &middot; Grade Amendment</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Grade 10-A Pure Mathematics Battery</div>
                  <div class="ov-inner-item-s">Submitted by Dr. Sarah Jenkins &middot; Academic Grades</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">AP Physics Unit 4 Syllabus Amendment</div>
                  <div class="ov-inner-item-s">Submitted by Mr. Robert Fox &middot; Curriculum</div>
                </div>
              </div>
            </div>

            <!-- Live Campus Operations Feed -->'''
    content = content[:old_panel2.start()] + new_panel2 + content[old_panel2.end() - len('<!-- Live Campus Operations Feed -->'):]

# 2. Ensure Live Campus Operations Feed has id="dtCampusFeedList"
old_feed = re.search(r'<div class="ov-feed-list">.*?</div>\s*</div>\s*</div>\s*</div>\s*<!-- Column 3', content, re.DOTALL)
if old_feed:
    new_feed = '''<div class="ov-feed-list" id="dtCampusFeedList">
                <div class="ov-feed-item">
                  <span class="material-symbols-outlined ov-feed-icon" style="color:#000000">how_to_reg</span>
                  <div class="ov-feed-text">Daily attendance synchronization logged: <span class="font-medium">95.4% attendance</span> school-wide.</div>
                  <span class="ov-feed-time">6m ago</span>
                </div>
                <div class="ov-feed-item">
                  <span class="material-symbols-outlined ov-feed-icon" style="color:#202F63">assignment_turned_in</span>
                  <div class="ov-feed-text">Grade 11-A Calculus Midterm submissions completed by <span class="font-medium">32 students</span>.</div>
                  <span class="ov-feed-time">22m ago</span>
                </div>
                <div class="ov-feed-item">
                  <span class="material-symbols-outlined ov-feed-icon" style="color:#000000">security</span>
                  <div class="ov-feed-text">Main Campus security checklist completed by <span class="font-medium">Facilities Operations</span>.</div>
                  <span class="ov-feed-time">1h ago</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Column 3'''
    content = content[:old_feed.start()] + new_feed + content[old_feed.end() - len('<!-- Column 3'):]

# 3. Task list in column 3
old_tasks = re.search(r'<div class="ov-task-list">.*?</div>\s*</div>\s*</div>\s*<!-- Secondary Row', content, re.DOTALL)
if old_tasks:
    new_tasks = '''<div class="ov-task-list" id="dtTaskList">
            <div class="ov-task-card" style="cursor:pointer;border-left:3px solid #92243D" onclick="window.location.href='principal-approvals.html'">
              <div class="ov-task-top">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-[#92243D]/10 text-[#92243D]">Urgent Clearance</span>
                <span class="ov-task-due">Today 17:00</span>
              </div>
              <div class="ov-task-title font-medium text-sm">Cambridge Coursework Inspection Sign-off</div>
              <div class="ov-task-sub text-xs text-[#000000]/60">Quality assurance clearance for Grade 11 &amp; 12</div>
            </div>
            <div class="ov-task-card" style="cursor:pointer;border-left:3px solid #202F63" onclick="window.location.href='principal-approvals.html'">
              <div class="ov-task-top">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-[#202F63]/10 text-[#202F63]">Pending Review</span>
                <span class="ov-task-due">Tomorrow 12:00</span>
              </div>
              <div class="ov-task-title font-medium text-sm">Faculty Gradebook Submission Clearance</div>
              <div class="ov-task-sub text-xs text-[#000000]/60">Mathematics &amp; Statistics score sheet validation</div>
            </div>
            <div class="ov-task-card" style="cursor:pointer;border-left:3px solid #000000" onclick="window.location.href='principal-approvals.html'">
              <div class="ov-task-top">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium bg-[#F3F3F5] text-[#000000]">Scheduled</span>
                <span class="ov-task-due">Oct 24</span>
              </div>
              <div class="ov-task-title font-medium text-sm">STEM Integration Department Workshop</div>
              <div class="ov-task-sub text-xs text-[#000000]/60">Professional development budget authorization</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Secondary Row'''
    content = content[:old_tasks.start()] + new_tasks + content[old_tasks.end() - len('<!-- Secondary Row'):]

# 4. Clean Quick Action <b> tags
content = content.replace('<b>Academic Reports</b>', '<span class="font-medium text-sm text-gray-900">Academic Reports</span>')
content = content.replace('<b>Approval Workflow</b>', '<span class="font-medium text-sm text-gray-900">Approval Workflow</span>')
content = content.replace('<b>Faculty Directory</b>', '<span class="font-medium text-sm text-gray-900">Faculty Directory</span>')
content = content.replace('<b>Class Cohorts</b>', '<span class="font-medium text-sm text-gray-900">Class Cohorts</span>')

# 5. Mobile Hero clean colors & add IDs
old_mob_hero = re.search(r'<!-- Executive Status Hero Card -->.*?<!-- 4-Tile Quick Action Grid -->', content, re.DOTALL)
if old_mob_hero:
    new_mob_hero = '''<!-- Executive Status Hero Card -->
      <div class="rounded-2xl bg-[#202F63] text-white p-5 shadow-xs border border-[#202F63] relative overflow-hidden">
        <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div class="flex items-center justify-between mb-3">
          <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-white/10 text-white backdrop-blur-md">
            <span class="w-1.5 h-1.5 rounded-full bg-[#FFFFFF] animate-pulse"></span>
            Campus Operations &middot; Nominal
          </span>
          <span class="text-xs text-white/70">MoEYS &amp; Cambridge</span>
        </div>
        <div class="text-2xl font-medium tracking-tight">Main Campus Executive</div>
        <div class="text-xs text-white/80 mt-1">Phnom Penh Campus &middot; Academic Year 2025–26</div>

        <div class="grid grid-cols-2 gap-3 mt-4 pt-3 border-t border-white/10">
          <div>
            <div class="text-[11px] uppercase tracking-wider text-white/60 font-medium">Students</div>
            <div class="text-xl font-medium text-white" id="mobStatStudents">1,480</div>
          </div>
          <div>
            <div class="text-[11px] uppercase tracking-wider text-white/60 font-medium">Faculty Staff</div>
            <div class="text-xl font-medium text-white" id="mobStatTeachers">86 Active</div>
          </div>
        </div>
      </div>

      <!-- 4-Tile Quick Action Grid -->'''
    content = content[:old_mob_hero.start()] + new_mob_hero + content[old_mob_hero.end() - len('<!-- 4-Tile Quick Action Grid -->'):]

# 6. Mobile Attendance value id
content = content.replace('<span class="absolute text-[12px] font-medium text-gray-900">96.4%</span>', '<span class="absolute text-[12px] font-medium text-gray-900" id="mobAttendanceVal">95.4%</span>')

# 7. Mobile Approvals List
old_mob_appr = re.search(r'<!-- Urgent Authorizations List -->.*?</div>\s*</div>\s*</div>\s*</div>\s*</main>', content, re.DOTALL)
if old_mob_appr:
    new_mob_appr = '''<!-- Urgent Authorizations List -->
      <div class="bg-white rounded-2xl p-4 border border-[#E5E5E8] shadow-xs space-y-3">
        <div class="flex items-center justify-between">
          <div class="text-[13px] font-medium text-gray-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-[#92243D]"></span>
            Pending Principal Approvals (<span id="mobApprovalsCount">3</span>)
          </div>
          <a href="principal-approvals.html" class="text-[11px] font-medium text-[#92243D] hover:underline">Review All &rarr;</a>
        </div>

        <div class="space-y-2.5" id="mobApprovalsList">
          <div class="p-3 rounded-xl bg-[#F3F3F5] border border-[#E5E5E8]">
            <div class="flex items-center justify-between">
              <span class="text-[12px] font-medium text-gray-900">Grade Correction (+4 pts)</span>
              <span class="text-[10px] font-medium text-[#202F63] bg-white px-2 py-0.5 rounded-full border border-[#E5E5E8]">Grade 11-A</span>
            </div>
            <div class="text-[11px] text-gray-600 mt-1">Submitted by Dr. Sarah Jenkins (Math Dept.)</div>
            <div class="mt-2.5 flex items-center gap-2">
              <a href="principal-approvals.html" class="flex-1 text-center py-1.5 bg-[#92243D] text-white text-[11px] font-medium rounded-lg shadow-xs hover:bg-[#7A1D32]">Authorize</a>
              <a href="principal-approvals.html" class="px-3 py-1.5 bg-white text-[#000000] border border-[#E5E5E8] text-[11px] font-medium rounded-lg hover:bg-[#F3F3F5]">Inspect</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>'''
    content = content[:old_mob_appr.start()] + new_mob_appr + content[old_mob_appr.end() - len('</main>'):]

# 8. Add Dashboard live hydration script
script_injection = '''
<script>
// Live Principal Executive Dashboard Data Hydration
async function loadPrincipalDashboardData() {
  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  try {
    // 1. Fetch Executive Stats
    const statsRes = await fetch('/api/principal/stats');
    if (statsRes.ok) {
      const stats = await statsRes.json();
      const stEl = document.getElementById('statStudents');
      if (stEl) stEl.textContent = Number(stats.totalStudents || 1480).toLocaleString();
      const mobSt = document.getElementById('mobStatStudents');
      if (mobSt) mobSt.textContent = Number(stats.totalStudents || 1480).toLocaleString();

      const tcEl = document.getElementById('statTeachers');
      if (tcEl) tcEl.textContent = stats.totalTeachers || 86;
      const mobTc = document.getElementById('mobStatTeachers');
      if (mobTc) mobTc.textContent = (stats.totalTeachers || 86) + ' Active';

      const attEl = document.getElementById('statAttendance');
      if (attEl) attEl.textContent = stats.attendanceRate || '95.4%';
      const mobAtt = document.getElementById('mobAttendanceVal');
      if (mobAtt) mobAtt.textContent = stats.attendanceRate || '95.4%';

      const pCount = stats.pendingApprovals ?? 0;
      const appEl = document.getElementById('statApprovals');
      if (appEl) {
        appEl.textContent = pCount;
        appEl.style.color = pCount > 0 ? '#92243D' : '#202F63';
      }
      const dtCount = document.getElementById('dtApprovalsCount');
      if (dtCount) dtCount.textContent = pCount;
      const mobCount = document.getElementById('mobApprovalsCount');
      if (mobCount) mobCount.textContent = pCount;
    }

    // 2. Fetch Pending Approvals for queue widgets
    const apprRes = await fetch('/api/principal/approvals?status=pending');
    if (apprRes.ok) {
      const data = await apprRes.json();
      const items = data.items || [];
      
      // Desktop Queue Panel
      const dtList = document.getElementById('dtApprovalsList');
      if (dtList) {
        if (items.length === 0) {
          dtList.innerHTML = '<div style="padding:14px;font-size:12px;color:#000000;opacity:0.6;display:flex;align-items:center;gap:6px"><span class="material-symbols-outlined" style="font-size:18px;color:#202F63">check_circle</span>All items cleared & up to date</div>';
        } else {
          dtList.innerHTML = items.slice(0, 3).map(it => `
            <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
              <div class="ov-inner-item-t">${escapeHtml(it.title)}</div>
              <div class="ov-inner-item-s">Submitted by ${escapeHtml(it.submittedBy || 'Faculty')} &middot; ${escapeHtml(it.category || 'Approval')}</div>
            </div>
          `).join('');
        }
      }

      // Desktop Column 3 Task List
      const taskList = document.getElementById('dtTaskList');
      if (taskList && items.length > 0) {
        taskList.innerHTML = items.slice(0, 3).map((it, idx) => {
          const isUrgent = idx === 0;
          const borderCol = isUrgent ? '#92243D' : (idx === 1 ? '#202F63' : '#000000');
          const badgeBg = isUrgent ? 'rgba(146,36,61,0.1)' : (idx === 1 ? 'rgba(32,47,99,0.1)' : '#F3F3F5');
          const badgeText = isUrgent ? '#92243D' : (idx === 1 ? '#202F63' : '#000000');
          const badgeLabel = isUrgent ? 'Urgent Clearance' : (idx === 1 ? 'Pending Review' : 'Scheduled');
          return `
            <div class="ov-task-card" style="cursor:pointer;border-left:3px solid ${borderCol}" onclick="window.location.href='principal-approvals.html'">
              <div class="ov-task-top">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium" style="background:${badgeBg};color:${badgeText}">${badgeLabel}</span>
                <span class="ov-task-due">${isUrgent ? 'Today 17:00' : 'Pending'}</span>
              </div>
              <div class="ov-task-title font-medium text-sm">${escapeHtml(it.title)}</div>
              <div class="ov-task-sub text-xs text-[#000000]/60">${escapeHtml(it.scope || it.category || '')} &middot; ${escapeHtml(it.submittedBy || '')}</div>
            </div>
          `;
        }).join('');
      }

      // Mobile Approvals List
      const mobList = document.getElementById('mobApprovalsList');
      if (mobList) {
        if (items.length === 0) {
          mobList.innerHTML = '<div class="p-3 text-center text-xs text-gray-500">No items pending executive approval.</div>';
        } else {
          mobList.innerHTML = items.slice(0, 3).map(it => `
            <div class="p-3 rounded-xl bg-[#F3F3F5] border border-[#E5E5E8]">
              <div class="flex items-center justify-between">
                <span class="text-[12px] font-medium text-gray-900">${escapeHtml(it.title)}</span>
                <span class="text-[10px] font-medium text-[#202F63] bg-white px-2 py-0.5 rounded-full border border-[#E5E5E8]">${escapeHtml(it.category || 'Academic')}</span>
              </div>
              <div class="text-[11px] text-gray-600 mt-1">Submitted by ${escapeHtml(it.submittedBy || 'Faculty')}</div>
              <div class="mt-2.5 flex items-center gap-2">
                <a href="principal-approvals.html" class="flex-1 text-center py-1.5 bg-[#92243D] text-white text-[11px] font-medium rounded-lg shadow-xs hover:bg-[#7A1D32]">Authorize</a>
                <a href="principal-approvals.html" class="px-3 py-1.5 bg-white text-[#000000] border border-[#E5E5E8] text-[11px] font-medium rounded-lg hover:bg-[#F3F3F5]">Inspect</a>
              </div>
            </div>
          `).join('');
        }
      }
    }

    // 3. Fetch Live Campus Audit Feed
    const auditRes = await fetch('/api/principal/audit');
    if (auditRes.ok) {
      const aData = await auditRes.json();
      const events = aData.items || [];
      const feedList = document.getElementById('dtCampusFeedList');
      if (feedList && events.length > 0) {
        feedList.innerHTML = events.slice(0, 3).map((ev, i) => {
          const icon = ev.action.includes('GRADE') ? 'assignment_turned_in' : (ev.action.includes('ATTENDANCE') ? 'how_to_reg' : 'verified');
          const iconColor = i === 0 ? '#202F63' : '#000000';
          const timeAgo = 'Just now';
          return `
            <div class="ov-feed-item">
              <span class="material-symbols-outlined ov-feed-icon" style="color:${iconColor}">${icon}</span>
              <div class="ov-feed-text">${escapeHtml(ev.description || ev.action)}</div>
              <span class="ov-feed-time">${timeAgo}</span>
            </div>
          `;
        }).join('');
      }
    }
  } catch(err) {
    console.warn('[NGIS] Principal dashboard live hydration failed:', err);
  }
}

document.addEventListener('DOMContentLoaded', loadPrincipalDashboardData);
loadPrincipalDashboardData();
</script>
'''

if 'loadPrincipalDashboardData' not in content:
    content = content.replace('</body>', script_injection + '\n</body>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Principal dashboard upgraded successfully.")

