with open('pages/student/student-assignments.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace row 1 actions
old_r1 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap">
                    <div class="inline-flex items-center gap-1.5">
                      <button onclick="showFeedback('Differentiation Worksheet', 'Excellent mastery of the chain rule. Solutions were clearly organized with accurate mathematical notation.', 'Mr. Chea Sophea', '95/100 · Grade A')" class="p-1.5 rounded-lg text-ink-muted transition-colors flex items-center gap-1 text-[11px] font-normal" title="View Instructor Feedback">
                        <span data-ngis-icon="mail" class="text-[16px] text-forest-700"></span>
                        <span>Feedback</span>
                      </button>
                      <button onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="p-1.5 rounded-lg text-ink-muted transition-colors" title="Download Graded Paper">
                        <span data-ngis-icon="download" class="text-[17px]"></span>
                      </button>
                    </div>
                  </td>'''

new_r1 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap table-actions">
                    <div class="action-group">
                      <button type="button" onclick="showFeedback('Differentiation Worksheet', 'Excellent mastery of the chain rule. Solutions were clearly organized with accurate mathematical notation.', 'Mr. Chea Sophea', '95/100 · Grade A')" class="action-icon-btn" title="View Instructor Feedback" aria-label="View Instructor Feedback">
                        <span data-ngis-icon="mail"></span>
                      </button>
                      <button type="button" onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="action-icon-btn" title="Download Graded Paper" aria-label="Download Graded Paper">
                        <span data-ngis-icon="download"></span>
                      </button>
                    </div>
                  </td>'''

# Replace row 2 actions
old_r2 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap">
                    <div class="inline-flex items-center gap-1.5">
                      <button onclick="showFeedback('Newton’s Laws Lab Report', 'Good experimental data. The error analysis section in Table 3 needs deeper interpretation of friction factors.', 'Ms. Rathana Chea', '88/100 · Grade B+')" class="p-1.5 rounded-lg text-ink-muted transition-colors flex items-center gap-1 text-[11px] font-normal" title="View Instructor Feedback">
                        <span data-ngis-icon="mail" class="text-[16px] text-forest-700"></span>
                        <span>Feedback</span>
                      </button>
                      <button onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="p-1.5 rounded-lg text-ink-muted transition-colors" title="Download Graded Paper">
                        <span data-ngis-icon="download" class="text-[17px]"></span>
                      </button>
                    </div>
                  </td>'''

new_r2 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap table-actions">
                    <div class="action-group">
                      <button type="button" onclick="showFeedback('Newton’s Laws Lab Report', 'Good experimental data. The error analysis section in Table 3 needs deeper interpretation of friction factors.', 'Ms. Rathana Chea', '88/100 · Grade B+')" class="action-icon-btn" title="View Instructor Feedback" aria-label="View Instructor Feedback">
                        <span data-ngis-icon="mail"></span>
                      </button>
                      <button type="button" onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="action-icon-btn" title="Download Graded Paper" aria-label="Download Graded Paper">
                        <span data-ngis-icon="download"></span>
                      </button>
                    </div>
                  </td>'''

# Replace row 3 actions
old_r3 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap">
                    <div class="inline-flex items-center gap-1.5">
                      <button onclick="showFeedback('Hamlet Thematic Analysis Essay', 'Compelling thesis statement on existential dread. Strengthen textual quotes integration in paragraphs 4-5.', 'Dr. Vance Miller', '82/100 · Grade B')" class="p-1.5 rounded-lg text-ink-muted transition-colors flex items-center gap-1 text-[11px] font-normal" title="View Instructor Feedback">
                        <span data-ngis-icon="mail" class="text-[16px] text-forest-700"></span>
                        <span>Feedback</span>
                      </button>
                      <button onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="p-1.5 rounded-lg text-ink-muted transition-colors" title="Download Graded Paper">
                        <span data-ngis-icon="download" class="text-[17px]"></span>
                      </button>
                    </div>
                  </td>'''

new_r3 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap table-actions">
                    <div class="action-group">
                      <button type="button" onclick="showFeedback('Hamlet Thematic Analysis Essay', 'Compelling thesis statement on existential dread. Strengthen textual quotes integration in paragraphs 4-5.', 'Dr. Vance Miller', '82/100 · Grade B')" class="action-icon-btn" title="View Instructor Feedback" aria-label="View Instructor Feedback">
                        <span data-ngis-icon="mail"></span>
                      </button>
                      <button type="button" onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="action-icon-btn" title="Download Graded Paper" aria-label="Download Graded Paper">
                        <span data-ngis-icon="download"></span>
                      </button>
                    </div>
                  </td>'''

# Replace row 4 actions
old_r4 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap">
                    <div class="inline-flex items-center gap-1.5">
                      <button onclick="showFeedback('Python Sorting Algorithms', 'Clean algorithmic implementation. Quicksort pivot selection handled duplicates exceptionally well.', 'Mr. Sovannarith Khun', '98/100 · Grade A+')" class="p-1.5 rounded-lg text-ink-muted transition-colors flex items-center gap-1 text-[11px] font-normal" title="View Instructor Feedback">
                        <span data-ngis-icon="mail" class="text-[16px] text-forest-700"></span>
                        <span>Feedback</span>
                      </button>
                      <button onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="p-1.5 rounded-lg text-ink-muted transition-colors" title="Download Graded Paper">
                        <span data-ngis-icon="download" class="text-[17px]"></span>
                      </button>
                    </div>
                  </td>'''

new_r4 = '''                  <td class="py-3.5 px-4 text-right whitespace-nowrap table-actions">
                    <div class="action-group">
                      <button type="button" onclick="showFeedback('Python Sorting Algorithms', 'Clean algorithmic implementation. Quicksort pivot selection handled duplicates exceptionally well.', 'Mr. Sovannarith Khun', '98/100 · Grade A+')" class="action-icon-btn" title="View Instructor Feedback" aria-label="View Instructor Feedback">
                        <span data-ngis-icon="mail"></span>
                      </button>
                      <button type="button" onclick="if(window.toast) window.toast('Downloading graded paper…','info'); else alert('Downloading graded submission')" class="action-icon-btn" title="Download Graded Paper" aria-label="Download Graded Paper">
                        <span data-ngis-icon="download"></span>
                      </button>
                    </div>
                  </td>'''

for old, new, label in [(old_r1, new_r1, 'Row 1'), (old_r2, new_r2, 'Row 2'), (old_r3, new_r3, 'Row 3'), (old_r4, new_r4, 'Row 4')]:
    if old in text:
        text = text.replace(old, new)
        print(f"Updated {label} in student-assignments.html")
    else:
        print(f"Warning: {label} not matched in student-assignments.html")

with open('pages/student/student-assignments.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved student-assignments.html")

