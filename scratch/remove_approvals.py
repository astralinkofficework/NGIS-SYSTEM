import re

def update_layouts():
    for path in ['layout.js', 'assets/js/layout.js']:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Remove Waiting for Approval link from sidebar
        old_link = '          { id: "approvals", label: "Waiting for Approval", icon: "task_alt", href: "pages/principal/principal-approvals.html", badge: "3" },\n'
        if old_link in content:
            content = content.replace(old_link, '')
            print(f'Removed sidebar link from {path}')
        else:
            print(f'Warning: old_link not found in {path}')

        # 2. Update bottomNav principal list
        old_bnav = '{ id:"approvals",  label:"Approvals",  icon:"verified",       href:"pages/principal/principal-approvals.html" },'
        new_bnav = '{ id:"classes",    label:"Classes",    icon:"class",          href:"pages/principal/principal-classes.html" },'
        if old_bnav in content:
            content = content.replace(old_bnav, new_bnav)
            print(f'Updated bottomNav in {path}')
        else:
            print(f'Warning: old_bnav not found in {path}')

        # 3. Update phosphor bottomNav
        old_ph = '{ id: "approvals", label: "Approvals", icon: "ph-bold ph-check-circle", href: "pages/principal/principal-approvals.html" },'
        new_ph = '{ id: "classes", label: "Classes", icon: "ph-bold ph-chalkboard-simple", href: "pages/principal/principal-classes.html" },'
        if old_ph in content:
            content = content.replace(old_ph, new_ph)
            print(f'Updated phosphor bottomNav in {path}')
        else:
            print(f'Warning: old_ph not found in {path}')

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

def update_principal_html():
    path = 'pages/principal/principal.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop quick action button
    old_quick = '''        <a class="dash-quick-btn" href="principal-approvals.html">

          <span class="material-symbols-outlined" style="color:#000000">verified</span>

          <span><span class="font-medium text-sm text-gray-900">Approval Workflow</span><small>Grade corrections &amp; clearances</small></span>

        </a>'''
    new_quick = '''        <a class="dash-quick-btn" href="principal-classes.html">

          <span class="material-symbols-outlined" style="color:#176B45">class</span>

          <span><span class="font-medium text-sm text-gray-900">School Classes</span><small>Schedules &amp; enrollments</small></span>

        </a>'''
    if old_quick in content:
        content = content.replace(old_quick, new_quick)
        print('Updated desktop quick button in principal.html')
    else:
        print('Warning: old_quick not found in principal.html')

    # Mobile quick action button
    old_mob_quick = '''        <a href="principal-approvals.html" class="flex flex-col items-center p-3 bg-white rounded-xl border border-gray-100 shadow-xs  transition text-center relative">

          <div class="w-10 h-10 rounded-lg bg-[#F7F9F7] text-[#000000] flex items-center justify-center mb-1.5">

            <i class="ph ph-seal-check text-xl"></i>

          </div>

          <span class="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#176B45]"></span>

          <span class="text-[11px] font-medium text-gray-800">Approvals</span>

        </a>'''
    new_mob_quick = '''        <a href="principal-classes.html" class="flex flex-col items-center p-3 bg-white rounded-xl border border-gray-100 shadow-xs  transition text-center">

          <div class="w-10 h-10 rounded-lg bg-[#F7F9F7] text-[#176B45] flex items-center justify-center mb-1.5">

            <i class="ph ph-chalkboard-simple text-xl"></i>

          </div>

          <span class="text-[11px] font-medium text-gray-800">Classes</span>

        </a>'''
    if old_mob_quick in content:
        content = content.replace(old_mob_quick, new_mob_quick)
        print('Updated mobile quick button in principal.html')
    else:
        print('Warning: old_mob_quick not found in principal.html')

    # Column 3 Action items link
    content = content.replace('<a class="ov-card-link" href="principal-approvals.html">View All</a>',
                              '<a class="ov-card-link" href="principal-services.html">View All</a>')

    # Subpanel 2 header and items
    old_subpanel = '''            <!-- Subpanel 2: Approvals Queue -->
            <div class="ov-inner-panel">
              <div class="ov-inner-head">
                <span class="material-symbols-outlined" style="color:#29352E">verified_user</span>Approvals Queue (<span id="dtApprovalsCount">3</span>)
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
            </div>'''
    new_subpanel = '''            <!-- Subpanel 2: Service Requests -->
            <div class="ov-inner-panel">
              <div class="ov-inner-head">
                <span class="material-symbols-outlined" style="color:#29352E">grid_view</span>Service Requests (<span id="dtApprovalsCount">3</span>)
              </div>
              <div id="dtApprovalsList">
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-services.html'">
                  <div class="ov-inner-item-t">Official Transcript Request</div>
                  <div class="ov-inner-item-s">Submitted by Nrinphouneta Hok</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-services.html'">
                  <div class="ov-inner-item-t">Enrollment Verification Letter</div>
                  <div class="ov-inner-item-s">Submitted by Channary Meas</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-services.html'">
                  <div class="ov-inner-item-t">Student ID Replacement</div>
                  <div class="ov-inner-item-s">Submitted by Dara Seng</div>
                </div>
                <div class="ov-inner-item" style="cursor:pointer" onclick="window.location.href='principal-services.html'">
                  <div class="ov-inner-item-t">Transfer Clearance Certificate</div>
                  <div class="ov-inner-item-s">Submitted by Somnang Srun</div>
                </div>
              </div>
            </div>'''
    if old_subpanel in content:
        content = content.replace(old_subpanel, new_subpanel)
        print('Updated subpanel 2 in principal.html')
    else:
        print('Warning: old_subpanel not found in principal.html')

    # Mobile urgent card link
    content = content.replace('<a href="principal-approvals.html" class="text-[11px] font-medium text-[#176B45] hover:underline">Review All &rarr;</a>',
                              '<a href="principal-services.html" class="text-[11px] font-medium text-[#176B45] hover:underline">Review All &rarr;</a>')

    # Mobile urgent card label
    content = content.replace('Waiting for Principal Approval (<span id="mobApprovalsCount">—</span>)',
                              'Pending Service Requests (<span id="mobApprovalsCount">—</span>)')

    # Remaining js dynamic links in principal.html
    content = content.replace("onclick=\"window.location.href='principal-approvals.html'\"",
                              "onclick=\"window.location.href='principal-services.html'\"")
    content = content.replace('<a href="principal-approvals.html" class="flex-1 text-center py-1.5 bg-[#176B45] text-white text-[11px] font-medium rounded-lg shadow-xs">Open Queue</a>',
                              '<a href="principal-services.html" class="flex-1 text-center py-1.5 bg-[#176B45] text-white text-[11px] font-medium rounded-lg shadow-xs">Open Hub</a>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated pages/principal/principal.html')

def update_tests():
    # 1. test_principal_e2e.py
    p_test = 'test_principal_e2e.py'
    with open(p_test, 'r', encoding='utf-8') as f:
        t_content = f.read()
    old_entry = "    '/pages/principal/principal-approvals.html',\n"
    if old_entry in t_content:
        t_content = t_content.replace(old_entry, '')
        with open(p_test, 'w', encoding='utf-8') as f:
            f.write(t_content)
        print('Updated test_principal_e2e.py')

    # 2. tests/e2e-portals.test.py
    p_e2e = 'tests/e2e-portals.test.py'
    with open(p_e2e, 'r', encoding='utf-8') as f:
        e_content = f.read()
    old_e2e_entry = '            "pages/principal/principal-approvals.html",\n'
    if old_e2e_entry in e_content:
        e_content = e_content.replace(old_e2e_entry, '')
        with open(p_e2e, 'w', encoding='utf-8') as f:
            f.write(e_content)
        print('Updated tests/e2e-portals.test.py')

if __name__ == '__main__':
    update_layouts()
    update_principal_html()
    update_tests()

