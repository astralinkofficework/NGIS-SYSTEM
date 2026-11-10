profiles_path = r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js'

with open(profiles_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace input value for subject in teacherRowHtml
old_subj_input = """          <div>
            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edSubject_' + r.id + '">Primary Subject <span class="text-rose-500">*</span></label>
            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edSubject_' + r.id + '" type="text" value="' + esc(r.subject || '') + '">
          </div>"""

new_subj_input = """          <div>
            <label class="block text-[10px] font-medium uppercase tracking-wider text-slate-500 mb-1" for="edSubject_' + r.id + '">Primary Subject <span class="text-rose-500">*</span></label>
            <input class="w-full text-xs py-2 px-2.5 rounded-lg border border-[#E1E9E3] bg-white text-slate-800 focus:ring-1 focus:ring-[#176B45] focus:border-[#176B45]" id="edSubject_' + r.id + '" type="text" value="' + esc(r.subject || r.department || 'General') + '">
          </div>"""

# Replace saveRowEditor validation
old_save_val = """    var name = fv('edName_' + id);
    var email = fv('edEmail_' + id);
    var department = fv('edDept_' + id);
    var subject = fv('edSubject_' + id);

    if (!name || !department || !subject || !email) {
      toast('Name, Department, Subject, and Email are required.', true);
      return;
    }"""

new_save_val = """    var name = fv('edName_' + id);
    var email = fv('edEmail_' + id);
    var department = fv('edDept_' + id) || 'General';
    var subject = fv('edSubject_' + id) || department || 'General';

    if (!name || !email) {
      toast('Name and Email are required.', true);
      return;
    }"""

assert old_subj_input in text, "old_subj_input not found"
assert old_save_val in text, "old_save_val not found"

text = text.replace(old_subj_input, new_subj_input, 1)
text = text.replace(old_save_val, new_save_val, 1)

with open(profiles_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed subject fallback and validation in ngis-profiles.js")

