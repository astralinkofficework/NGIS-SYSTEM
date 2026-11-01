# 1. Update overlap.css
with open('pages/student/css/overlap.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix promo-text padding
css = css.replace('padding: 0 36px;', 'padding: 0 58px;')

# Fix ov-inner-grid
css = css.replace('grid-template-columns: repeat(3, minmax(0, 1fr));\n  gap: 10px;',
                  'grid-template-columns: 0.95fr 0.95fr 1.25fr;\n  gap: 14px;')

# Fix laptop breakpoint
css = css.replace('grid-template-columns: 215px minmax(0, 1fr) 240px;\n    gap: 12px;',
                  'grid-template-columns: 220px minmax(0, 1fr) 250px;\n    gap: 14px;')

with open('pages/student/css/overlap.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Updated overlap.css!')

# 2. Add 3rd exam item to student.html for vertical balance
with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    student_html = f.read()

exam_target = '''      <div class="ov-deadline-dot" style="background:#f59e0b"></div>
      <div>
        <div class="ov-deadline-item-t">Science Test</div>
        <div class="ov-deadline-item-s">Jul 12, 09:00 AM</div>
        <span class="ov-tag ov-tag-amber">Prepare</span>
      </div>
    </div>
  </div>
</div>'''

exam_replacement = '''      <div class="ov-deadline-dot" style="background:#f59e0b"></div>
      <div>
        <div class="ov-deadline-item-t">Science Test</div>
        <div class="ov-deadline-item-s">Jul 12, 09:00 AM</div>
        <span class="ov-tag ov-tag-amber">Prepare</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#10b981"></div>
      <div>
        <div class="ov-deadline-item-t">English Oral Quiz</div>
        <div class="ov-deadline-item-s">Jul 16, 10:30 AM</div>
        <span class="ov-tag ov-tag-green">Scheduled</span>
      </div>
    </div>
  </div>
</div>'''

if exam_target in student_html and 'English Oral Quiz' not in student_html:
    student_html = student_html.replace(exam_target, exam_replacement)
    with open('pages/student/student.html', 'w', encoding='utf-8') as f:
        f.write(student_html)
    print('Added English Oral Quiz to student.html!')

# 3. Add 4th admin item to teacher.html for vertical balance
with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    teacher_html = f.read()

teach_target = '''      <div class="ov-deadline-dot" style="background:#3b82f6"></div>
      <div>
        <div class="ov-deadline-item-t">Parent-Teacher Conference</div>
        <div class="ov-deadline-item-s">Oct 29 &middot; 02:00 PM</div>
        <span class="ov-tag ov-tag-blue">Scheduled</span>
      </div>
    </div>
  </div>
</div>'''

teach_replacement = '''      <div class="ov-deadline-dot" style="background:#3b82f6"></div>
      <div>
        <div class="ov-deadline-item-t">Parent-Teacher Conference</div>
        <div class="ov-deadline-item-s">Oct 29 &middot; 02:00 PM</div>
        <span class="ov-tag ov-tag-blue">Scheduled</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#8b5cf6"></div>
      <div>
        <div class="ov-deadline-item-t">Curriculum Planning Review</div>
        <div class="ov-deadline-item-s">Nov 03 &middot; 14:00 &middot; Room 302</div>
        <span class="ov-tag ov-tag-purple">Planned</span>
      </div>
    </div>
  </div>
</div>'''

if teach_target in teacher_html and 'Curriculum Planning Review' not in teacher_html:
    teacher_html = teacher_html.replace(teach_target, teach_replacement)
    with open('pages/teacher/teacher.html', 'w', encoding='utf-8') as f:
        f.write(teacher_html)
    print('Added Curriculum Review to teacher.html!')

