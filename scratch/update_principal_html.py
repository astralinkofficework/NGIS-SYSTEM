with open('pages/principal/principal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update upcoming column headers
html = html.replace('Approvals Queue ( 11 )', 'Approvals Queue')
html = html.replace('Approvals Queue ( <span id="dtApprovalsCount">11</span> )', 'Approvals Queue')
html = html.replace('Approvals Queue (<span id="dtApprovalsCount">11</span>)', 'Approvals Queue')
html = html.replace('>Campus Ac...', '>Activity Feed')
html = html.replace('>Campus Activity Feed<', '>Activity Feed<')

# 2. Update dtCampusFeedList rendering
old_feed_logic = """  const feedList = document.getElementById('dtCampusFeedList');
  if (feedList) {
    if (!auditEvents.length) {
      feedList.innerHTML = '<div class="ov-feed-item"><span class="material-symbols-outlined ov-feed-icon" style="color:#202F63">hourglass_top</span><div class="ov-feed-text">No management actions recorded yet.</div><span class="ov-feed-time">—</span></div>';
    } else {
      feedList.innerHTML = auditEvents.slice(0, 5).map((ev, i) => {
        const action = String(ev.action || '');
        const icon = action.includes('GRADE') ? 'assignment_turned_in'
          : action.includes('ATTENDANCE') ? 'how_to_reg'
          : action.includes('APPROVE') ? 'verified'
          : action.includes('STUDENT') ? 'person' : 'receipt_long';
        const iconColor = i === 0 ? '#202F63' : '#000000';
        const details = `${ev.actor_role || ''} · ${action.replace(/_/g, ' ').toLowerCase()}`;
        const sub = ev.reason ? ` <span style="opacity:.7">${escapeHtml(String(ev.reason).slice(0, 60))}</span>` : '';
        return `
          <div class="ov-feed-item">
            <span class="material-symbols-outlined ov-feed-icon" style="color:${iconColor}">${icon}</span>
            <div class="ov-feed-text"><span class="font-medium">${escapeHtml(action.replace(/_/g, ' '))}</span> <span style="opacity:.65;font-size:11px">${escapeHtml(details)}</span>${sub}</div>
            <span class="ov-feed-time">${escapeHtml(fmtDate(ev.created_at))}</span>
          </div>`;
      }).join('');
    }
  }"""

new_feed_logic = """  const feedList = document.getElementById('dtCampusFeedList');
  if (feedList) {
    if (!auditEvents.length) {
      feedList.innerHTML = '<div style="padding:14px;font-size:12px;color:#77777F;text-align:center">No management actions recorded yet.</div>';
    } else {
      feedList.innerHTML = auditEvents.slice(0, 6).map((ev, i) => {
        const action = String(ev.action || '');
        const badge = action.includes('GRADE') ? 'Grade'
          : action.includes('ATTEND') ? 'Attend'
          : action.includes('APPROVE') ? 'Clearance'
          : action.includes('STUDENT') ? 'Record' : 'Audit';
        const barColor = badge === 'Clearance' ? '#92243D' : (badge === 'Grade' || badge === 'Attend' ? '#202F63' : '#000000');
        const badgeColor = badge === 'Clearance' ? '#92243D' : (badge === 'Grade' ? '#202F63' : '#000000');
        const title = ev.reason ? escapeHtml(String(ev.reason).slice(0, 42)) : escapeHtml(action.replace(/_/g, ' '));
        const sub = `${escapeHtml(ev.actor_role || 'Principal')} · ${escapeHtml(fmtDate(ev.created_at))}`;
        return `
          <div style="display:flex;border-bottom:1px solid #F3F3F5">
            <div style="width:3px;flex-shrink:0;background:${barColor}"></div>
            <div style="flex:1;min-width:0;padding:7px 9px">
              <div style="display:flex;align-items:center;gap:5px;margin-bottom:2px">
                <span style="flex-shrink:0;font-size:9px;font-weight:400;text-transform:uppercase;letter-spacing:.05em;color:${badgeColor};background:#F3F3F5;padding:1px 5px;border-radius:3px;white-space:nowrap">${badge}</span>
                <span style="font-size:10px;color:#77777F;margin-left:auto;flex-shrink:0;white-space:nowrap">${escapeHtml(fmtDate(ev.created_at) || 'Recent')}</span>
              </div>
              <div style="font-size:11.5px;font-weight:400;color:#000000;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${title}</div>
              <div style="font-size:10px;color:#77777F;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${sub}</div>
            </div>
          </div>`;
      }).join('');
    }
  }"""

if old_feed_logic in html:
    html = html.replace(old_feed_logic, new_feed_logic)
    print("Replaced feed logic successfully")
else:
    print("Old feed logic not found exactly, searching partial...")

with open('pages/principal/principal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated principal.html")

