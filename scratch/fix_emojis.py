with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace graduation emoji with school icon
text = text.replace('🎓 Student', '<span class="status-dot"></span>Student')

# Replace attendance/grade/assignment emojis with clean status badges with status dots
text = text.replace('<td>🟢 Present</td>', '<td><span class="status-pill active"><span class="status-dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#176B45;margin-right:6px"></span>Present</span></td>')
text = text.replace('<td>🟡 Excused Absence</td>', '<td><span class="status-pill warning"><span class="status-dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#F28C28;margin-right:6px"></span>Excused Absence</span></td>')
text = text.replace('<td>🟢 Pass</td>', '<td><span class="status-pill active"><span class="status-dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#176B45;margin-right:6px"></span>Pass</span></td>')
text = text.replace('<td>🟢 Submitted (On-time)</td>', '<td><span class="status-pill active"><span class="status-dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#176B45;margin-right:6px"></span>Submitted (On-time)</span></td>')
text = text.replace('<td>🟡 Not Submitted Yet</td>', '<td><span class="status-pill warning"><span class="status-dot" style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#F28C28;margin-right:6px"></span>Not Submitted Yet</span></td>')

with open('pages/admin/admin-users.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated pages/admin/admin-users.html successfully")

# Fix student-id.html
with open('pages/student/student-id.html', 'r', encoding='utf-8') as f:
    sid_text = f.read()

sid_text = sid_text.replace('Phoenix House 🔴', 'Phoenix House')

with open('pages/student/student-id.html', 'w', encoding='utf-8') as f:
    f.write(sid_text)

print("Updated pages/student/student-id.html successfully")

