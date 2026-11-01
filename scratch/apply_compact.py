import re

def update_student_html():
    with open("pages/student/student.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update desktop media query in <style>
    old_desktop_mq = re.compile(
        r'/\* Clean 3-column deck on desktop matching original reference layout \*/\s*'
        r'@media \(min-width: 992px\) \{.*?'
        r'height: 100% !important;\s*'
        r'\}\s*\}',
        re.DOTALL
    )
    
    new_desktop_mq = (
        "/* Clean, compact 3-column deck on desktop matching user-drawn reference */\n"
        "@media (min-width: 992px) {\n"
        "  .dash-overlap {\n"
        "    display: grid !important;\n"
        "    grid-template-columns: 240px minmax(0, 1fr) 280px !important;\n"
        "    gap: 16px !important;\n"
        "    max-width: 1280px !important;\n"
        "    margin: -48px auto 0 !important;\n"
        "    padding: 0 24px !important;\n"
        "    align-items: stretch !important;\n"
        "  }\n"
        "  .ov-profile, .ov-upcoming, .ov-deadlines {\n"
        "    grid-column: auto !important;\n"
        "    grid-row: 1 !important;\n"
        "    height: 335px !important;\n"
        "    max-height: 335px !important;\n"
        "  }\n"
        "}"
    )
    
    assert old_desktop_mq.search(content) is not None, "Could not find desktop MQ in student.html"
    content = old_desktop_mq.sub(new_desktop_mq, content)

    # 2. Update School Activity Feed scroll max-height
    content = content.replace(
        '<div style="overflow-y:auto;max-height:243px">',
        '<div style="overflow-y:auto;max-height:232px;height:232px">'
    )

    # 3. Update deadlines items structure
    old_deadlines = """  <!-- Assessments -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#e11d48">assignment</span>Assessments
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#ef4444"></div>
      <div>
        <div class="ov-deadline-item-t">History Essay</div>
        <div class="ov-deadline-item-s">Due: Jun 27, 11:59 PM</div>
        <span class="ov-tag ov-tag-red">Urgent</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#f59e0b"></div>
      <div>
        <div class="ov-deadline-item-t">Math Problem Set</div>
        <div class="ov-deadline-item-s">Due: Jun 29, 11:59 PM</div>
        <span class="ov-tag ov-tag-amber">Soon</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#16a34a"></div>
      <div>
        <div class="ov-deadline-item-t">Science Report</div>
        <div class="ov-deadline-item-s">Due: Jul 3</div>
        <span class="ov-tag ov-tag-green">On track</span>
      </div>
    </div>
  </div>
  <!-- Exam & Quizzes -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#7c3aed">quiz</span>Exam &amp; Quizzes
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#ef4444"></div>
      <div>
        <div class="ov-deadline-item-t">Midterm Exam</div>
        <div class="ov-deadline-item-s">Jul 5 – Jul 9</div>
        <span class="ov-tag ov-tag-red">Upcoming</span>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#f59e0b"></div>
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
  </div>"""

    new_deadlines = """  <!-- Assessments -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#e11d48">assignment</span>Assessments
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#ef4444"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">History Essay</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Due: Jun 27, 11:59 PM</span>
          <span class="ov-tag ov-tag-red">Urgent</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#f59e0b"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Math Problem Set</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Due: Jun 29, 11:59 PM</span>
          <span class="ov-tag ov-tag-amber">Soon</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#16a34a"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Science Report</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Due: Jul 3</span>
          <span class="ov-tag ov-tag-green">On track</span>
        </div>
      </div>
    </div>
  </div>
  <!-- Exam & Quizzes -->
  <div class="ov-deadline-panel">
    <div class="ov-deadline-head">
      <span class="mi" style="color:#7c3aed">quiz</span>Exam &amp; Quizzes
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#ef4444"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Midterm Exam</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Jul 5 – Jul 9</span>
          <span class="ov-tag ov-tag-red">Upcoming</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#f59e0b"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">Science Test</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Jul 12, 09:00 AM</span>
          <span class="ov-tag ov-tag-amber">Prepare</span>
        </div>
      </div>
    </div>
    <div class="ov-deadline-item">
      <div class="ov-deadline-dot" style="background:#10b981"></div>
      <div class="ov-deadline-info">
        <div class="ov-deadline-item-t">English Oral Quiz</div>
        <div class="ov-deadline-meta">
          <span class="ov-deadline-item-s">Jul 16, 10:30 AM</span>
          <span class="ov-tag ov-tag-green">Scheduled</span>
        </div>
      </div>
    </div>
  </div>"""

    # Normalize CRLF for replacement
    content = content.replace(old_deadlines.replace('\n', '\r\n'), new_deadlines.replace('\n', '\r\n'))
    if old_deadlines in content:
        content = content.replace(old_deadlines, new_deadlines)

    with open("pages/student/student.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated pages/student/student.html successfully")

def update_overlap_css():
    with open("pages/student/css/overlap.css", "r", encoding="utf-8") as f:
        css = f.read()

    # 1. Profile header padding & avatar
    css = re.sub(
        r'\.ov-profile-header\s*\{[^}]*\}',
        """.ov-profile-header {
  background: #ffffff;
  padding: 14px 12px 10px;
  text-align: center;
  position: relative;
  flex-shrink: 0;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  align-items: center;
}""",
        css
    )

    css = re.sub(
        r'\.ov-avatar\s*\{[^}]*\}',
        """.ov-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid #e2e8f0;
  object-fit: cover;
  display: block;
  margin: 0 auto 6px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}""",
        css
    )

    css = re.sub(
        r'\.ov-profile-name\s*\{[^}]*\}',
        """.ov-profile-name {
  color: #182329;
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  letter-spacing: -0.01em;
}""",
        css
    )

    css = re.sub(
        r'\.ov-profile-grade\s*\{[^}]*\}',
        """.ov-profile-grade {
  color: #586f7c;
  font-size: 11px;
  font-weight: 400;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}""",
        css
    )

    css = re.sub(
        r'\.ov-profile-badge\s*\{[^}]*\}',
        """.ov-profile-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
  font-size: 9.5px;
  font-weight: 500;
  padding: 1.5px 8px;
  border-radius: 999px;
  white-space: nowrap;
}""",
        css
    )

    # 2. Profile body & actions
    css = re.sub(
        r'\.ov-profile-body\s*\{[^}]*\}',
        """.ov-profile-body {
  padding: 8px 14px 4px;
  display: flex;
  flex-direction: column;
  gap: 0;
  flex: 1;
}""",
        css
    )

    css = re.sub(
        r'\.ov-info-row\s*\{[^}]*\}',
        """.ov-info-row {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 11px;
  font-weight: 400;
  color: #334155;
  padding: 4.5px 0;
  border-bottom: 1px solid #f1f5f9;
  line-height: 1.35;
  min-width: 0;
  overflow: hidden;
}""",
        css
    )

    css = re.sub(
        r'\.ov-actions\s*\{[^}]*\}',
        """.ov-actions {
  padding: 10px 14px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  flex-shrink: 0;
}""",
        css
    )

    css = re.sub(
        r'\.ov-btn-main\s*\{[^}]*\}',
        """.ov-btn-main {
  flex: 1;
  min-width: 0;
  background: #182329;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  padding: 7.5px 8px;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: inherit;
  white-space: nowrap;
}""",
        css
    )

    css = re.sub(
        r'\.ov-btn-ic\s*\{[^}]*\}',
        """.ov-btn-ic {
  width: 32px;
  height: 32px;
  min-width: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #ffffff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #64748b;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}""",
        css
    )

    # 3. Upcoming section
    css = re.sub(
        r'\.ov-upcoming\s*\{[^}]*\}',
        """.ov-upcoming {
  padding: 14px 16px;
}""",
        css
    )

    css = re.sub(
        r'\.ov-card-head\s*\{[^}]*\}',
        """.ov-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  flex-shrink: 0;
}""",
        css
    )

    css = re.sub(
        r'\.ov-card-title\s*\{[^}]*\}',
        """.ov-card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #182329;
}""",
        css
    )

    css = re.sub(
        r'\.ov-inner-grid\s*\{[^}]*\}',
        """.ov-inner-grid {
  display: grid;
  grid-template-columns: 0.95fr 0.95fr 1.25fr;
  gap: 12px;
  flex: 1;
  min-height: 0;
}""",
        css
    )

    css = re.sub(
        r'\.ov-inner-head\s*\{[^}]*\}',
        """.ov-inner-head {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: #1e293b;
  padding-bottom: 3px;
  border-bottom: none !important;
  margin-bottom: 3px;
  flex-shrink: 0;
}""",
        css
    )

    css = re.sub(
        r'\.ov-inner-item\s*\{[^}]*\}',
        """.ov-inner-item {
  padding: 2px 0;
  border-bottom: none !important;
}""",
        css
    )

    css = re.sub(
        r'\.ov-inner-item-t\s*\{[^}]*\}',
        """.ov-inner-item-t {
  font-size: 10.5px;
  font-weight: 500;
  color: #1e293b;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}""",
        css
    )

    css = re.sub(
        r'\.ov-inner-item-s\s*\{[^}]*\}',
        """.ov-inner-item-s {
  font-size: 9.5px;
  font-weight: 400;
  color: #64748b;
  margin-top: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}""",
        css
    )

    # 4. Deadlines section
    css = re.sub(
        r'\.ov-deadlines\s*\{[^}]*\}',
        """.ov-deadlines {
  padding: 14px 16px;
}""",
        css
    )

    css = re.sub(
        r'\.ov-deadline-panel\s*\{[^}]*\}',
        """.ov-deadline-panel {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  padding: 0 2px !important;
  display: flex;
  flex-direction: column;
  margin-bottom: 8px;
}""",
        css
    )

    css = re.sub(
        r'\.ov-deadline-head\s*\{[^}]*\}',
        """.ov-deadline-head {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: #1e293b;
  padding-bottom: 3px;
  border-bottom: none !important;
  margin-bottom: 3px;
  flex-shrink: 0;
}""",
        css
    )

    css = re.sub(
        r'\.ov-deadline-item\s*\{[^}]*\}',
        """.ov-deadline-item {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 3px 0;
  border-bottom: none !important;
}""",
        css
    )

    css = re.sub(
        r'\.ov-deadline-item-t\s*\{[^}]*\}',
        """.ov-deadline-item-t {
  font-size: 10.5px;
  font-weight: 500;
  color: #1e293b;
  line-height: 1.25;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}""",
        css
    )

    css = re.sub(
        r'\.ov-deadline-item-s\s*\{[^}]*\}',
        """.ov-deadline-item-s {
  font-size: 9.5px;
  font-weight: 400;
  color: #64748b;
  margin-top: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}""",
        css
    )

    # Insert .ov-deadline-meta if not present
    if '.ov-deadline-meta' not in css:
        css = css.replace(
            '.ov-deadline-info {\n  flex: 1;\n  min-width: 0;\n}',
            """.ov-deadline-info {
  flex: 1;
  min-width: 0;
}

.ov-deadline-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  margin-top: 1px;
}"""
        )

    css = re.sub(
        r'\.ov-tag\s*\{[^}]*\}',
        """.ov-tag {
  display: inline-block;
  font-size: 8.5px;
  font-weight: 500;
  padding: 1px 6px;
  border-radius: 999px;
  white-space: nowrap;
  flex-shrink: 0;
  margin-left: 4px;
  line-height: 1.2;
}""",
        css
    )

    # 5. Promo banner section
    css = re.sub(
        r'\.dash-banner-section,\s*body\[data-role="student"\] \.dash-banner-section\s*\{[^}]*\}',
        """.dash-banner-section,
body[data-role="student"] .dash-banner-section {
  max-width: 1280px;
  margin: 18px auto;
  padding: 0 24px;
  position: relative;
  z-index: 10;
  width: 100%;
  box-sizing: border-box;
}""",
        css
    )

    css = re.sub(
        r'\.promo-slideshow,\s*body\[data-role="student"\] \.promo-slideshow\s*\{[^}]*\}',
        """.promo-slideshow,
body[data-role="student"] .promo-slideshow {
  width: 100%;
  height: 165px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background: linear-gradient(135deg, #0e7490 0%, #13829b 50%, #1e3a8a 100%);
  box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.08);
  border: 1px solid rgba(184, 219, 217, 0.35);
  box-sizing: border-box;
}""",
        css
    )

    with open("pages/student/css/overlap.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("Updated pages/student/css/overlap.css successfully")

update_student_html()
update_overlap_css()

