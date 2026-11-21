import re

with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Additional 6 task cards to make a total of 10 tasks
extra_cards = '''
          <!-- Task Card 5: Computer Science -->
          <div class="task-card bg-white rounded-3xl p-4 sm:p-6" data-course="Computer Science" data-due="week" data-type="this-week">
            <div class="flex items-start gap-3.5 sm:gap-4">
              <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#F7F9F7] flex items-center justify-center text-forest-700 shrink-0">
                <span class="material-symbols-outlined text-[20px] sm:text-[22px]">terminal</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="asgn-status asgn-status-neutral">
                      4 Days Remaining
                    </span>
                    <span class="asgn-subject">
                      Computer Science
                    </span>
                  </div>
                  <span class="text-xs font-normal text-ink-muted">Weight: 15%</span>
                </div>
                <h3 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display mb-1">
                  Data Structures — Binary Search Trees &amp; Graph Traversal
                </h3>
                <p class="text-xs text-ink-muted flex items-center gap-2 flex-wrap mb-3.5">
                  <span class="flex items-center gap-1 font-medium text-ink-main"><span class="material-symbols-outlined text-[15px] text-forest-700">schedule</span> Due: Feb 04 • 11:59 PM</span>
                  <span>•</span>
                  <span>Python Source Implementation (.py)</span>
                </p>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 pt-3 border-t border-surface-borderLight">
                  <button type="button" onclick="if(window.toast) window.toast('Downloading Starter Code…','info'); else alert('Starter Code')" class="asgn-sub-btn">
                    <span data-ngis-icon="code" class="text-[16px]"></span>
                    <span>Starter Code</span>
                  </button>
                  <button type="button" onclick="openUpload('Data Structures — Binary Search Trees','Computer Science','Feb 04 • 11:59 PM','Ms. SreyLeak Kem','Class 10A','15% of Term')" class="asgn-primary-btn">
                    <span data-ngis-icon="upload" class="text-[16px]"></span>
                    <span>Upload</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Task Card 6: Chemistry -->
          <div class="task-card bg-white rounded-3xl p-4 sm:p-6" data-course="Chemistry" data-due="week" data-type="this-week">
            <div class="flex items-start gap-3.5 sm:gap-4">
              <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#F7F9F7] flex items-center justify-center text-forest-700 shrink-0">
                <span class="material-symbols-outlined text-[20px] sm:text-[22px]">science</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="asgn-status asgn-status-neutral">5 Days Remaining</span>
                    <span class="asgn-subject">Chemistry</span>
                  </div>
                  <span class="text-xs font-normal text-ink-muted">Weight: 20%</span>
                </div>
                <h3 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display mb-1">
                  Organic Chemistry — Reaction Mechanisms &amp; Synthesis Pathway
                </h3>
                <p class="text-xs text-ink-muted flex items-center gap-2 flex-wrap mb-3.5">
                  <span class="flex items-center gap-1 font-medium text-ink-main"><span class="material-symbols-outlined text-[15px] text-forest-700">schedule</span> Due: Feb 05 • 11:59 PM</span>
                  <span>•</span>
                  <span>Lab Report Document (PDF)</span>
                </p>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 pt-3 border-t border-surface-borderLight">
                  <button type="button" onclick="if(window.toast) window.toast('Downloading Synthesis Guidelines…','info'); else alert('Guidelines')" class="asgn-sub-btn">
                    <span data-ngis-icon="book" class="text-[16px]"></span>
                    <span>Guidelines</span>
                  </button>
                  <button type="button" onclick="openUpload('Organic Chemistry — Reaction Mechanisms','Chemistry','Feb 05 • 11:59 PM','Dr. Vuthy Seng','Class 10A','20% of Term')" class="asgn-primary-btn">
                    <span data-ngis-icon="upload" class="text-[16px]"></span>
                    <span>Upload</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Task Card 7: Biology -->
          <div class="task-card bg-white rounded-3xl p-4 sm:p-6" data-course="Biology" data-due="next-week" data-type="next-week">
            <div class="flex items-start gap-3.5 sm:gap-4">
              <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#F7F9F7] flex items-center justify-center text-forest-700 shrink-0">
                <span class="material-symbols-outlined text-[20px] sm:text-[22px]">biotech</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="asgn-status asgn-status-neutral">1 Week Remaining</span>
                    <span class="asgn-subject">Biology</span>
                  </div>
                  <span class="text-xs font-normal text-ink-muted">Weight: 10%</span>
                </div>
                <h3 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display mb-1">
                  Cellular Respiration &amp; Photosynthesis Lab Analysis
                </h3>
                <p class="text-xs text-ink-muted flex items-center gap-2 flex-wrap mb-3.5">
                  <span class="flex items-center gap-1 font-medium text-ink-main"><span class="material-symbols-outlined text-[15px] text-forest-700">schedule</span> Due: Feb 07 • 11:59 PM</span>
                  <span>•</span>
                  <span>Experimental Data Analysis</span>
                </p>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 pt-3 border-t border-surface-borderLight">
                  <button type="button" onclick="if(window.toast) window.toast('Downloading Lab Data…','info'); else alert('Lab Data')" class="asgn-sub-btn">
                    <span data-ngis-icon="list" class="text-[16px]"></span>
                    <span>Lab Data</span>
                  </button>
                  <button type="button" onclick="openUpload('Cellular Respiration Lab Analysis','Biology','Feb 07 • 11:59 PM','Dr. Vuthy Seng','Class 10A','10% of Term')" class="asgn-primary-btn">
                    <span data-ngis-icon="upload" class="text-[16px]"></span>
                    <span>Upload</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Task Card 8: Linear Algebra -->
          <div class="task-card bg-white rounded-3xl p-4 sm:p-6" data-course="Advanced Mathematics" data-due="next-week" data-type="next-week">
            <div class="flex items-start gap-3.5 sm:gap-4">
              <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#F7F9F7] flex items-center justify-center text-forest-700 shrink-0">
                <span class="material-symbols-outlined text-[20px] sm:text-[22px]">calculate</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="asgn-status asgn-status-neutral">8 Days Remaining</span>
                    <span class="asgn-subject">Advanced Mathematics</span>
                  </div>
                  <span class="text-xs font-normal text-ink-muted">Weight: 15%</span>
                </div>
                <h3 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display mb-1">
                  Linear Algebra — Matrix Inverses &amp; Vector Spaces
                </h3>
                <p class="text-xs text-ink-muted flex items-center gap-2 flex-wrap mb-3.5">
                  <span class="flex items-center gap-1 font-medium text-ink-main"><span class="material-symbols-outlined text-[15px] text-forest-700">schedule</span> Due: Feb 08 • 11:59 PM</span>
                  <span>•</span>
                  <span>Problem Set 4 (PDF)</span>
                </p>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 pt-3 border-t border-surface-borderLight">
                  <button type="button" onclick="if(window.toast) window.toast('Downloading Problem Set 4…','info'); else alert('Problem Set 4')" class="asgn-sub-btn">
                    <span data-ngis-icon="download" class="text-[16px]"></span>
                    <span>Problem Set</span>
                  </button>
                  <button type="button" onclick="openUpload('Linear Algebra — Matrix Inverses','Advanced Mathematics','Feb 08 • 11:59 PM','Dr. Sarah Jenkins','Class 10A','15% of Term')" class="asgn-primary-btn">
                    <span data-ngis-icon="upload" class="text-[16px]"></span>
                    <span>Upload</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Task Card 9: Khmer Literature -->
          <div class="task-card bg-white rounded-3xl p-4 sm:p-6" data-course="Khmer Literature" data-due="next-week" data-type="next-week">
            <div class="flex items-start gap-3.5 sm:gap-4">
              <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#F7F9F7] flex items-center justify-center text-forest-700 shrink-0">
                <span class="material-symbols-outlined text-[20px] sm:text-[22px]">history_edu</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="asgn-status asgn-status-neutral">10 Days Remaining</span>
                    <span class="asgn-subject">Khmer Literature</span>
                  </div>
                  <span class="text-xs font-normal text-ink-muted">Weight: 20%</span>
                </div>
                <h3 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display mb-1">
                  Classical Khmer Prose Analysis &amp; Literary Essay
                </h3>
                <p class="text-xs text-ink-muted flex items-center gap-2 flex-wrap mb-3.5">
                  <span class="flex items-center gap-1 font-medium text-ink-main"><span class="material-symbols-outlined text-[15px] text-forest-700">schedule</span> Due: Feb 10 • 11:59 PM</span>
                  <span>•</span>
                  <span>Essay Document (PDF / DOCX)</span>
                </p>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 pt-3 border-t border-surface-borderLight">
                  <button type="button" onclick="if(window.toast) window.toast('Viewing Khmer Essay Prompts…','info'); else alert('Prompts')" class="asgn-sub-btn">
                    <span data-ngis-icon="book" class="text-[16px]"></span>
                    <span>Prompt Guide</span>
                  </button>
                  <button type="button" onclick="openUpload('Classical Khmer Prose Analysis','Khmer Literature','Feb 10 • 11:59 PM','Mr. Sovann Sok','Class 10A','20% of Term')" class="asgn-primary-btn">
                    <span data-ngis-icon="upload" class="text-[16px]"></span>
                    <span>Upload</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Task Card 10: Chinese Language -->
          <div class="task-card bg-white rounded-3xl p-4 sm:p-6" data-course="Chinese Language" data-due="next-week" data-type="next-week">
            <div class="flex items-start gap-3.5 sm:gap-4">
              <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#F7F9F7] flex items-center justify-center text-forest-700 shrink-0">
                <span class="material-symbols-outlined text-[20px] sm:text-[22px]">translate</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 flex-wrap mb-1.5">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="asgn-status asgn-status-neutral">12 Days Remaining</span>
                    <span class="asgn-subject">Chinese Language</span>
                  </div>
                  <span class="text-xs font-normal text-ink-muted">Weight: 15%</span>
                </div>
                <h3 class="text-base sm:text-lg font-normal text-forest-800 tracking-tight font-display mb-1">
                  HSK 3 Reading Comprehension &amp; Character Writing Practice
                </h3>
                <p class="text-xs text-ink-muted flex items-center gap-2 flex-wrap mb-3.5">
                  <span class="flex items-center gap-1 font-medium text-ink-main"><span class="material-symbols-outlined text-[15px] text-forest-700">schedule</span> Due: Feb 12 • 11:59 PM</span>
                  <span>•</span>
                  <span>Practice Worksheet &amp; Audio Recording</span>
                </p>
                <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 pt-3 border-t border-surface-borderLight">
                  <button type="button" onclick="if(window.toast) window.toast('Downloading HSK 3 Worksheet…','info'); else alert('Worksheet')" class="asgn-sub-btn">
                    <span data-ngis-icon="download" class="text-[16px]"></span>
                    <span>Worksheet</span>
                  </button>
                  <button type="button" onclick="openUpload('HSK 3 Reading Practice','Chinese Language','Feb 12 • 11:59 PM','Ms. Lin Meiling','Class 10A','15% of Term')" class="asgn-primary-btn">
                    <span data-ngis-icon="upload" class="text-[16px]"></span>
                    <span>Upload</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
'''

pagination_html = '''
        <!-- Active & Pending Tasks Pagination Controls -->
        <div id="tasksPagination" class="bg-white rounded-2xl border border-surface-border p-3.5 sm:p-4 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-xs mt-4">
          <div class="text-xs text-ink-muted font-normal" id="tasksPaginationSummary">
            Showing 1–4 of 10 assignments
          </div>
          <div class="flex items-center gap-1.5 sm:gap-2">
            <button type="button" id="tasksPrevBtn" onclick="changeTasksPage(-1)" class="px-3 py-1.5 rounded-xl border border-surface-border bg-white hover:bg-surface-subtle text-forest-800 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1 text-xs font-normal transition shadow-xs cursor-pointer">
              <span class="material-symbols-outlined text-[16px]">chevron_left</span>
              <span>Previous</span>
            </button>
            <span id="tasksPageIndicator" class="px-3 py-1.5 text-xs font-medium text-forest-800 bg-surface-subtle rounded-xl border border-surface-borderLight">
              Page 1 of 3
            </span>
            <button type="button" id="tasksNextBtn" onclick="changeTasksPage(1)" class="px-3 py-1.5 rounded-xl border border-surface-border bg-white hover:bg-surface-subtle text-forest-800 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1 text-xs font-normal transition shadow-xs cursor-pointer">
              <span>Next</span>
              <span class="material-symbols-outlined text-[16px]">chevron_right</span>
            </button>
          </div>
        </div>
'''

# Find insertion point before </div>\n      </div>\n\n      <!-- ═════════ RIGHT COLUMN
target_marker = '<!-- Task Card 4: English Essay -->'
# Find the end of Task Card 4
t4_idx = content.find(target_marker)
if t4_idx != -1:
    end_of_tasks_list = content.find('</div>\n      </div>\n\n      <!-- ═════════ RIGHT COLUMN', t4_idx)
    if end_of_tasks_list != -1:
        new_content = (
            content[:end_of_tasks_list] + 
            extra_cards + 
            '\n        </div>\n' + 
            pagination_html + 
            '\n      </div>\n\n      <!-- ═════════ RIGHT COLUMN' + 
            content[end_of_tasks_list + len('</div>\n      </div>\n\n      <!-- ═════════ RIGHT COLUMN'):]
        )
        with open('pages/student/student-assignments.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Successfully added 10 cards and pagination HTML to student-assignments.html')
    else:
        print('Could not find end of tasksList div marker')
else:
    print('Could not find Task Card 4 marker')
