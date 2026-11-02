import re

path = 'pages/principal/principal.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update <style> with exact deck and deadline styles
style_target = '''  b, strong, th, h1, h2, h3, h4, h5, h6,
  .font-medium, .font-medium, .font-medium, .font-medium,
  [class*="font-medium"], [class*="font-medium"], [class*="font-medium"], [class*="font-medium"] {
    font-weight: 500 !important;
  }
</style>'''

style_replacement = '''  b, strong, th, h1, h2, h3, h4, h5, h6,
  .font-medium,
  [class*="font-medium"] {
    font-weight: 500 !important;
  }

  /* Clean, compact 3-column deck on desktop matching user reference */
  @media (min-width: 992px) {
    .dash-overlap {
      display: grid !important;
      grid-template-columns: 240px minmax(0, 1fr) 280px !important;
      gap: 16px !important;
      max-width: 1280px !important;
      margin: -48px auto 0 !important;
      padding: 0 24px !important;
      align-items: stretch !important;
    }
    .ov-profile, .ov-upcoming, .ov-deadlines {
      grid-column: auto !important;
      grid-row: 1 !important;
      height: 335px !important;
      max-height: 335px !important;
    }
  }

  /* Keep all inner panels completely transparent with no border lines */
  .ov-inner-panel,
  .ov-deadline-panel,
  .ov-panel-feed {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
  }

  .ov-deadline-panel {
    padding: 0 14px 10px;
  }
  .ov-deadline-head {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 500;
    color: #000000;
    margin-bottom: 6px;
  }
  .ov-deadline-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 5px 0;
  }
  .ov-deadline-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
  }
  .ov-deadline-info {
    flex: 1;
    min-width: 0;
  }
  .ov-deadline-item-t {
    font-size: 11.5px;
    font-weight: 500;
    color: #000000;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .ov-deadline-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-top: 1px;
  }
  .ov-deadline-item-s {
    font-size: 10px;
    color: #77777F;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .ov-tag {
    font-size: 9.5px;
    font-weight: 500;
    padding: 1px 7px;
    border-radius: 999px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .ov-tag-urgent {
    background: #92243D;
    color: #FFFFFF;
  }
  .ov-tag-soon {
    background: #F3F3F5;
    color: #202F63;
    border: 1px solid #202F63;
  }
  .ov-tag-neutral {
    background: #F3F3F5;
    color: #000000;
    border: 1px solid #E5E5E8;
  }

  @keyframes feedPulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.15); opacity: 0.6; }
    100% { transform: scale(1); opacity: 1; }
  }
</style>'''

content = content.replace(style_target, style_replacement)

# 2. Replace the entire .dash-overlap block with the clean reference design
dash_overlap_pattern = r'<div class="dash-overlap anim-up">.*?</div>\s*<!-- Secondary Row'

new_dash_overlap = '''<div class="dash-overlap anim-up">

        <!-- Column 1: Executive Profile Card -->
        <div class="ov-profile">
          <div class="ov-profile-header">
            <img class="ov-avatar" src="https://images.pexels.com/photos/2182970/pexels-photo-2182970.jpeg?auto=compress&cs=tinysrgb&w=160" alt="Dr. Ly Bunheng">
            <div class="ov-profile-name" id="dtPrincipalName">Dr. Ly Bunheng</div>
            <div class="ov-profile-grade" id="dtPrincipalTitle">Executive Principal &middot; Main Campus</div>
            <span class="ov-profile-badge" style="background:#F3F3F5;color:#202F63;border:1px solid #E5E5E8">Campus Leadership</span>
          </div>
          <div class="ov-profile-body">
            <div class="ov-info-row" title="principal@ngis.edu.kh">
              <span class="material-symbols-outlined">mail</span>
              <span class="ov-info-text">principal@ngis.edu.kh</span>
            </div>
            <div class="ov-info-row" title="Executive Suite · Admin Building A">
              <span class="material-symbols-outlined">location_on</span>
              <span class="ov-info-text">Exec Suite &middot; Admin Bldg A</span>
            </div>
            <div class="ov-info-row" title="MoEYS & Cambridge International">
              <span class="material-symbols-outlined">verified</span>
              <span class="ov-info-text">Cambridge &middot; MoEYS Accredited</span>
            </div>
          </div>
          <div class="ov-actions">
            <button class="ov-btn-main" id="viewIdBtn"><span class="material-symbols-outlined">badge</span>Executive Pass</button>
            <button class="ov-btn-ic" title="Campus Announcements" aria-label="Announcements" onclick="window.location.href='../messaging/campus-announcements.html'"><span class="material-symbols-outlined">notifications</span></button>
            <button class="ov-btn-ic" title="Academic Reports" aria-label="Reports" onclick="window.location.href='principal-reports.html'"><span class="material-symbols-outlined">assessment</span></button>
          </div>
        </div>

        <!-- Column 2: Campus Leadership Agenda & Live Activity Feed -->
        <div class="ov-upcoming">
          <div class="ov-card-head">
            <div class="ov-card-title">
              <span class="material-symbols-outlined">event_note</span>Campus Leadership Agenda
            </div>
            <a href="principal-reports.html" class="ov-card-link">View All</a>
          </div>
          <div class="ov-inner-grid">

            <!-- Subpanel 1: Today's Briefings -->
            <div class="ov-inner-panel">
              <div class="ov-inner-head">
                <span class="material-symbols-outlined" style="color:#000000">domain</span>Today's Briefings
              </div>
              <div class="ov-inner-item">
                <div class="ov-inner-item-t">Executive Cabinet Briefing</div>
                <div class="ov-inner-item-s">09:00–10:30 &middot; Board Room A</div>
              </div>
              <div class="ov-inner-item">
                <div class="ov-inner-item-t">Cambridge Audit Review</div>
                <div class="ov-inner-item-s">11:30–12:30 &middot; Conference Hall</div>
              </div>
              <div class="ov-inner-item">
                <div class="ov-inner-item-t">Parent Council Representatives</div>
                <div class="ov-inner-item-s">14:00–15:30 &middot; Reception Suite</div>
              </div>
              <div class="ov-inner-item">
                <div class="ov-inner-item-t">Academic Dept Coordination</div>
                <div class="ov-inner-item-s">15:45–16:45 &middot; Suite 301</div>
              </div>
              <div class="ov-inner-item">
                <div class="ov-inner-item-t">MoEYS Accreditation Liaison</div>
                <div class="ov-inner-item-s">Tomorrow &middot; 08:30 AM</div>
              </div>
              <div class="ov-inner-item">
                <div class="ov-inner-item-t">Campus Facilities Inspection</div>
                <div class="ov-inner-item-s">Tomorrow &middot; 14:00 PM</div>
              </div>
            </div>

            <!-- Subpanel 2: Approvals Queue -->
            <div class="ov-inner-panel">
              <div class="ov-inner-head">
                <span class="material-symbols-outlined" style="color:#202F63">verified_user</span>Approvals Queue (<span id="dtApprovalsCount">3</span>)
              </div>
              <div id="dtApprovalsList">
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Grade Correction: Grade 11 Calculus</div>
                  <div class="ov-inner-item-s">Submitted by Dr. Sarah Jenkins</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Grade 10-A Pure Math Battery</div>
                  <div class="ov-inner-item-s">Submitted by Dr. Sarah Jenkins</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Physics Lab Unit 4 Amendment</div>
                  <div class="ov-inner-item-s">Submitted by Mr. Robert Fox</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Official Transcript Request</div>
                  <div class="ov-inner-item-s">Submitted by Nrinphouneta Hok</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Biology Dept Term 1 Release</div>
                  <div class="ov-inner-item-s">Submitted by Dr. Michael Chen</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-approvals.html'">
                  <div class="ov-inner-item-t">Science Fair Clearance Notice</div>
                  <div class="ov-inner-item-s">Submitted by Admin Communications</div>
                </div>
              </div>
            </div>

            <!-- Subpanel 3: Campus Activity Feed (LIVE) -->
            <div class="ov-inner-panel" style="padding:0;overflow:hidden;display:flex;flex-direction:column;align-self:start">
              <div class="ov-inner-head" style="padding:8px 10px;margin:0;flex-shrink:0;border-bottom:1px solid #F3F3F5">
                <span class="material-symbols-outlined" style="color:#92243D;flex-shrink:0">rss_feed</span>
                <span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Campus Activity Feed</span>
                <span style="flex-shrink:0;display:inline-flex;align-items:center;gap:3px;font-size:10px;font-weight:400;color:#92243D;letter-spacing:.04em">
                  <span style="width:6px;height:6px;border-radius:50%;background:#92243D;animation:feedPulse 1.4s ease-in-out infinite"></span>LIVE
                </span>
              </div>
              <div style="overflow-y:auto;max-height:243px" id="dtCampusFeedList">
                <div style="display:flex;border-bottom:1px solid #F3F3F5">
                  <div style="width:3px;flex-shrink:0;background:#202F63"></div>
                  <div style="flex:1;min-width:0;padding:7px 9px">
                    <div style="display:flex;align-items:center;gap:5px;margin-bottom:2px">
                      <span style="flex-shrink:0;font-size:9px;font-weight:400;text-transform:uppercase;letter-spacing:.05em;color:#202F63;background:#F3F3F5;padding:1px 5px;border-radius:3px;white-space:nowrap">Grade</span>
                      <span style="font-size:10px;color:#77777F;margin-left:auto;flex-shrink:0;white-space:nowrap">12m ago</span>
                    </div>
                    <div style="font-size:11.5px;font-weight:400;color:#000000;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Grade 11-A Calculus Midterm logged</div>
                    <div style="font-size:10px;color:#77777F;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Submitted by Dr. Sarah Jenkins (32 students)</div>
                  </div>
                </div>
                <div style="display:flex;border-bottom:1px solid #F3F3F5">
                  <div style="width:3px;flex-shrink:0;background:#000000"></div>
                  <div style="flex:1;min-width:0;padding:7px 9px">
                    <div style="display:flex;align-items:center;gap:5px;margin-bottom:2px">
                      <span style="flex-shrink:0;font-size:9px;font-weight:400;text-transform:uppercase;letter-spacing:.05em;color:#000000;background:#F3F3F5;padding:1px 5px;border-radius:3px;white-space:nowrap">Attend</span>
                      <span style="font-size:10px;color:#77777F;margin-left:auto;flex-shrink:0;white-space:nowrap">24m ago</span>
                    </div>
                    <div style="font-size:11.5px;font-weight:400;color:#000000;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Campus Attendance Sync Complete</div>
                    <div style="font-size:10px;color:#77777F;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">95.4% present across all cohorts today</div>
                  </div>
                </div>
                <div style="display:flex;border-bottom:1px solid #F3F3F5">
                  <div style="width:3px;flex-shrink:0;background:#000000"></div>
                  <div style="flex:1;min-width:0;padding:7px 9px">
                    <div style="display:flex;align-items:center;gap:5px;margin-bottom:2px">
                      <span style="flex-shrink:0;font-size:9px;font-weight:400;text-transform:uppercase;letter-spacing:.05em;color:#000000;background:#F3F3F5;padding:1px 5px;border-radius:3px;white-space:nowrap">Facility</span>
                      <span style="font-size:10px;color:#77777F;margin-left:auto;flex-shrink:0;white-space:nowrap">1h ago</span>
                    </div>
                    <div style="font-size:11.5px;font-weight:400;color:#000000;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Building A &amp; Science Labs Cleared</div>
                    <div style="font-size:10px;color:#77777F;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Completed by Facilities Operations</div>
                  </div>
                </div>
                <div style="display:flex;border-bottom:1px solid #F3F3F5">
                  <div style="width:3px;flex-shrink:0;background:#202F63"></div>
                  <div style="flex:1;min-width:0;padding:7px 9px">
                    <div style="display:flex;align-items:center;gap:5px;margin-bottom:2px">
                      <span style="flex-shrink:0;font-size:9px;font-weight:400;text-transform:uppercase;letter-spacing:.05em;color:#202F63;background:#F3F3F5;padding:1px 5px;border-radius:3px;white-space:nowrap">Registry</span>
                      <span style="font-size:10px;color:#77777F;margin-left:auto;flex-shrink:0;white-space:nowrap">2h ago</span>
                    </div>
                    <div style="font-size:11.5px;font-weight:400;color:#000000;line-height:1.35;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Official Cambridge Transcript Issued</div>
                    <div style="font-size:10px;color:#77777F;margin-top:1px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Certified by Principal Registry Office</div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Column 3: Priority Institutional Action Items & Clearances -->
        <div class="ov-deadlines">
          <div class="ov-card-head">
            <div class="ov-card-title">
              <span class="material-symbols-outlined" style="color:#92243D">schedule</span>Action Items
            </div>
            <a class="ov-card-link" href="principal-approvals.html">View All</a>
          </div>

          <!-- Section 1: Pending Clearances -->
          <div class="ov-deadline-panel">
            <div class="ov-deadline-head">
              <span class="material-symbols-outlined" style="color:#92243D">assignment</span>Pending Clearances
            </div>
            <div class="ov-deadline-item">
              <div class="ov-deadline-dot" style="background:#92243D"></div>
              <div class="ov-deadline-info">
                <div class="ov-deadline-item-t">Cambridge Coursework Sign-off</div>
                <div class="ov-deadline-meta">
                  <span class="ov-deadline-item-s">Due: Today, 17:00</span>
                  <span class="ov-tag ov-tag-urgent">Urgent</span>
                </div>
              </div>
            </div>
            <div class="ov-deadline-item">
              <div class="ov-deadline-dot" style="background:#000000"></div>
              <div class="ov-deadline-info">
                <div class="ov-deadline-item-t">Grade 10-A Math Gradebook</div>
                <div class="ov-deadline-meta">
                  <span class="ov-deadline-item-s">Due: Tomorrow, 12:00</span>
                  <span class="ov-tag ov-tag-soon">Soon</span>
                </div>
              </div>
            </div>
            <div class="ov-deadline-item">
              <div class="ov-deadline-dot" style="background:#000000"></div>
              <div class="ov-deadline-info">
                <div class="ov-deadline-item-t">Physics Lab Syllabus Revision</div>
                <div class="ov-deadline-meta">
                  <span class="ov-deadline-item-s">Due: Oct 28</span>
                  <span class="ov-tag ov-tag-neutral">On track</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Section 2: Executive Audits & Sign-offs -->
          <div class="ov-deadline-panel">
            <div class="ov-deadline-head">
              <span class="material-symbols-outlined" style="color:#202F63">verified_user</span>Executive Audits
            </div>
            <div class="ov-deadline-item">
              <div class="ov-deadline-dot" style="background:#92243D"></div>
              <div class="ov-deadline-info">
                <div class="ov-deadline-item-t">Faculty Workload Allocation</div>
                <div class="ov-deadline-meta">
                  <span class="ov-deadline-item-s">Oct 25, 03:00 PM</span>
                  <span class="ov-tag ov-tag-urgent">Upcoming</span>
                </div>
              </div>
            </div>
            <div class="ov-deadline-item">
              <div class="ov-deadline-dot" style="background:#000000"></div>
              <div class="ov-deadline-info">
                <div class="ov-deadline-item-t">Term 1 Assessment Audit</div>
                <div class="ov-deadline-meta">
                  <span class="ov-deadline-item-s">Oct 29, 09:00 AM</span>
                  <span class="ov-tag ov-tag-neutral">Prepare</span>
                </div>
              </div>
            </div>
            <div class="ov-deadline-item">
              <div class="ov-deadline-dot" style="background:#202F63"></div>
              <div class="ov-deadline-info">
                <div class="ov-deadline-item-t">STEM Integration Workshop</div>
                <div class="ov-deadline-meta">
                  <span class="ov-deadline-item-s">Nov 02, 14:00 PM</span>
                  <span class="ov-tag ov-tag-soon">Scheduled</span>
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Secondary Row'''

content = re.sub(dash_overlap_pattern, new_dash_overlap, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied exact gold-standard dashboard structure to principal.html.")

