with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_tasks = '''  <!-- Grading & Submissions -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#92243D">assignment</span>Pending Grading
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#92243D"></div>
      <div>
        <div class="ov-deadline-item-t">Calculus Problem Set 3</div>
        <div class="ov-deadline-item-s">Due: Today, 11:59 PM</div>
        <span class="ov-tag ov-tag-red">Urgent</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#000000"></div>
      <div>
        <div class="ov-deadline-item-t">Statistics Quiz Review</div>
        <div class="ov-deadline-item-s">Due: Oct 24, 05:00 PM</div>
        <span class="ov-tag ov-tag-amber">Soon</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#000000"></div>
      <div>
        <div class="ov-deadline-item-t">Pure Math Problem Set</div>
        <div class="ov-deadline-item-s">Due: Oct 28</div>
        <span class="ov-tag ov-tag-green">On track</span>
      </div>
    </div>
  </div>
  <!-- Registers & Admin -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#202F63">how_to_reg</span>Registers &amp; Admin
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#92243D"></div>
      <div>
        <div class="ov-deadline-item-t">Mark Grade 10-C Register</div>
        <div class="ov-deadline-item-s">Next: 10:15 AM · Room 305</div>
        <span class="ov-tag ov-tag-red">Upcoming</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#000000"></div>
      <div>
        <div class="ov-deadline-item-t">Cambridge Exam Moderation</div>
        <div class="ov-deadline-item-s">Oct 25, 03:00 PM</div>
        <span class="ov-tag ov-tag-amber">Prepare</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#202F63"></div>
      <div>
        <div class="ov-deadline-item-t">Parent-Teacher Conference</div>
        <div class="ov-deadline-item-s">Oct 29 · 02:00 PM</div>
        <span class="ov-tag" style="background:#F3F3F5;color:#202F63">Scheduled</span>
      </div>
    </div>
  </div>'''

new_tasks = '''  <!-- Grading & Submissions -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#92243D">assignment</span>Pending Grading
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#92243D"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Calculus Problem Set 3</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Due: Today, 11:59 PM</span>
          <span class="ov-tag" style="background:#92243D;color:#ffffff">Urgent</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#000000"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Statistics Quiz Review</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Due: Oct 24, 05:00 PM</span>
          <span class="ov-tag" style="background:#F3F3F5;color:#202F63;border:1px solid #202F63">Soon</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#000000"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Pure Math Problem Set</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Due: Oct 28</span>
          <span class="ov-tag" style="background:#F3F3F5;color:#000000;border:1px solid #E5E5E8">On track</span>
        </div>
      </div>
    </div>
  </div>
  <!-- Registers & Admin -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#202F63">how_to_reg</span>Registers &amp; Admin
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#92243D"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Mark Grade 10-C Register</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Next: 10:15 AM · Room 305</span>
          <span class="ov-tag" style="background:#92243D;color:#ffffff">Upcoming</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#000000"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Cambridge Exam Moderation</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Oct 25, 03:00 PM</span>
          <span class="ov-tag" style="background:#F3F3F5;color:#000000;border:1px solid #E5E5E8">Prepare</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#202F63"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Parent-Teacher Conference</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Oct 29 · 02:00 PM</span>
          <span class="ov-tag" style="background:#F3F3F5;color:#202F63">Scheduled</span>
        </div>
      </div>
    </div>
  </div>'''

norm_content = content.replace('\r\n', '\n')
norm_old = old_tasks.replace('\r\n', '\n')

if norm_old in norm_content:
    norm_content = norm_content.replace(norm_old, new_tasks)
    with open('pages/teacher/teacher.html', 'w', encoding='utf-8') as f:
        f.write(norm_content)
    print('Tasks updated successfully!')
else:
    print('Pattern not found!')

