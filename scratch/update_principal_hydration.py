import re

path = 'pages/principal/principal.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the hydration script with the matched layout hydration
old_script_pattern = r'// 2\. Pending approvals widgets.*?// 3\. Live management audit feed'

new_script = '''// 2. Pending approvals & action items widgets (exact match to gold design standard)
  const dtList = document.getElementById('dtApprovalsList');
  if (dtList) {
    if (!pendingItems.length) {
      dtList.innerHTML = '<div style="padding:14px;font-size:12px;color:#000000;opacity:0.6;display:flex;align-items:center;gap:6px"><span class="material-symbols-outlined" style="font-size:18px;color:#202F63">check_circle</span>Queue clear &mdash; nothing awaiting your review</div>';
    } else {
      dtList.innerHTML = pendingItems.slice(0, 6).map(it => `
        <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
          <div class="ov-inner-item-t">${escapeHtml(it.title)}</div>
          <div class="ov-inner-item-s">Submitted by ${escapeHtml(it.submittedBy || 'Faculty')} &middot; ${escapeHtml(it.category || 'Approval')}</div>
        </div>`).join('');
    }
  }

  // Column 3: Pending Clearances & Actions
  const clearancesList = document.getElementById('dtClearancesList');
  if (clearancesList && pendingItems.length) {
    clearancesList.innerHTML = pendingItems.slice(0, 3).map((it, idx) => {
      const dotColor = idx === 0 ? '#92243D' : (idx === 1 ? '#000000' : '#202F63');
      const tagClass = idx === 0 ? 'ov-tag ov-tag-urgent' : (idx === 1 ? 'ov-tag ov-tag-soon' : 'ov-tag ov-tag-neutral');
      const tagText = idx === 0 ? 'Urgent' : (idx === 1 ? 'Soon' : 'On track');
      return `
        <div class="ov-deadline-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
          <div class="ov-deadline-dot" style="background:${dotColor}"></div>
          <div class="ov-deadline-info">
            <div class="ov-deadline-item-t">${escapeHtml(it.title)}</div>
            <div class="ov-deadline-meta">
              <span class="ov-deadline-item-s">Due: ${escapeHtml(fmtDate(it.submittedAt) || 'Today, 17:00')}</span>
              <span class="${tagClass}">${tagText}</span>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  // 3. Live management audit feed'''

content = re.sub(old_script_pattern, new_script, content, flags=re.DOTALL)

# Add id="dtClearancesList" to Section 1 in Column 3
content = content.replace(
    '<div class="ov-deadline-panel">\n            <div class="ov-deadline-head">\n              <span class="material-symbols-outlined" style="color:#92243D">assignment</span>Pending Clearances\n            </div>',
    '<div class="ov-deadline-panel">\n            <div class="ov-deadline-head">\n              <span class="material-symbols-outlined" style="color:#92243D">assignment</span>Pending Clearances\n            </div>\n            <div id="dtClearancesList">'
)
content = content.replace(
    '<!-- Section 2: Executive Audits & Sign-offs -->',
    '</div>\n          <!-- Section 2: Executive Audits & Sign-offs -->'
)

# In audit feed rendering:
old_audit_render = r"feedList\.innerHTML = auditEvents\.slice\(0, 5\)\.map\(.*?\}\)\.join\(''\);"
new_audit_render = '''feedList.innerHTML = auditEvents.slice(0, 5).map((ev, i) => {
        const action = String(ev.action || '');
        const isUrgent = action.includes('GRADE') || action.includes('ATTENDANCE');
        const barColor = isUrgent ? (i === 0 ? '#92243D' : '#202F63') : '#000000';
        const tagLabel = action.includes('GRADE') ? 'Grade' : (action.includes('ATTEND') ? 'Attend' : (action.includes('CLEAR') ? 'Clear' : 'Audit'));
        const tagColor = isUrgent ? '#92243D' : '#202F63';
        const details = `${ev.actor_role || ''} · ${action.replace(/_/g, ' ').toLowerCase()}`;
        const sub = ev.reason ? String(ev.reason).slice(0, 45) : (ev.entity_type ? `Target: ${ev.entity_type}` : 'Logged by Executive Registry');
        return `
          <div style="display:flex;border-bottom:1px solid #F3F3F5">
            <div style="width:3px;flex-shrink:0;background:${barColor}"></div>
            <div style="flex:1;min-width:0;padding:7px 9px">
              <div style="display:flex;align-items:center;gap:5px;margin-bottom:2px">
                <span style="flex-shrink:0;font-size:9px;font-weight:400;text-transform:uppercase;letter-spacing:.05em;color:${tagColor};background:#F3F3F5;padding:1px 5px;border-radius:3px;white-space:nowrap">${tagLabel}</span>
                <span style="font-size:10px;color:#77777F;margin-left:auto;flex-shrink:0;white-space:nowrap">${escapeHtml(fmtDate(ev.created_at) || 'Recent')}</span>
              </div>
              <div style="font-size:11.5px;font-weight:400;color:#000000;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escapeHtml(action.replace(/_/g, ' '))}</div>
              <div style="font-size:10px;color:#77777F;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${escapeHtml(sub)}</div>
            </div>
          </div>`;
      }).join('');'''

content = re.sub(old_audit_render, new_audit_render, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated principal hydration script to match reference design.")

