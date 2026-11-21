with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update teacher config
old_cfg = '''      teacher: {
        title: 'Exam Schedule Management',
        subtitle: 'Create and manage examination schedules for your assigned subjects and classes.',
        actions: '<button type="button" class="exw-btn exw-btn-primary" data-action="new">New examination</button>',
        tabs: ''
      },'''

new_cfg = '''      teacher: {
        title: 'Examination & Quiz Notices',
        subtitle: 'Publish examination notices, quiz schedules, and revision materials for student cohorts.',
        actions: '<button type="button" class="exw-btn exw-btn-primary" data-action="new"><span class="material-symbols-outlined text-sm align-middle mr-1">add</span>Create Notice</button>',
        tabs: ''
      },'''

code = code.replace(old_cfg, new_cfg)

# 2. Update modal titles
old_modal_title = "title: exam ? 'Correct examination schedule' : 'Create examination schedule',"
new_modal_title = "title: exam ? 'Edit Examination Notice' : 'Create Examination & Quiz Notice',"
code = code.replace(old_modal_title, new_modal_title)

# 3. Add success notification in saveForm
old_save_op = '''      await op(
        exam ? 'Updating schedule…' : (submitNow ? 'Submitting schedule…' : 'Saving draft…'),
        api(exam ? '/api/exams/simple/' + encodeURIComponent(exam.id) : '/api/exams/simple', {
          method: exam ? 'PUT' : 'POST',
          body: payload
        }),
        exam ? 'Schedule updated.' : (submitNow ? 'Schedule submitted for Principal review.' : 'Draft saved.')
      );
      closeModal();
      await reload();'''

new_save_op = '''      await op(
        exam ? 'Updating schedule…' : (submitNow ? 'Submitting notice…' : 'Saving notice draft…'),
        api(exam ? '/api/exams/simple/' + encodeURIComponent(exam.id) : '/api/exams/simple', {
          method: exam ? 'PUT' : 'POST',
          body: payload
        }),
        exam ? 'Notice updated.' : (submitNow ? 'Notice submitted for Principal review.' : 'Notice draft saved.')
      );
      closeModal();
      await reload();
      if (window.NGIS_showOperationSuccess) {
        window.NGIS_showOperationSuccess({
          title: submitNow ? 'Notice Submitted' : 'Notice Saved',
          message: submitNow
            ? 'Examination notice has been submitted for approval and scheduled for publication.'
            : 'Examination notice draft saved to your workspace.'
        });
      }'''

code = code.replace(old_save_op, new_save_op)

# 4. Add selected-row support to table rows
old_row = "return '<tr>' +"
new_row = "return '<tr class=\"transition-colors hover:bg-slate-50 cursor-pointer\" data-id=\"' + esc(e.id) + '\" onclick=\"if(!event.target.closest(\\'button, a, input\\')) { document.querySelectorAll(\\'.exw-table tr\\').forEach(function(r) { r.classList.remove(\\'selected-row\\'); }); this.classList.add(\\'selected-row\\'); }\">' +"

code = code.replace(old_row, new_row)

with open('assets/js/exams-simple.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated exams-simple.js successfully.")
