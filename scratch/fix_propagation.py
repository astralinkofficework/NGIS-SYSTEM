with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace onclick="event.stopPropagation()" in Col 5
text = text.replace("onclick=\"event.stopPropagation()\"", "")

# In wireShell, ensure e.stopPropagation() inside the listener
old_wire = """    var dirRows = $id('dirRows');
    if (dirRows) {
      dirRows.addEventListener('click', function (e) {
        var actBtn = e.target.closest('[data-act]');
        if (!actBtn) return;
        var act = actBtn.getAttribute('data-act');
        var id = actBtn.getAttribute('data-id');

        if (act === 'toggle-expand') {
          toggleRowAccordion(id);
        } else if (act === 'edit-row') {
          openRowEditor(id);
        } else if (act === 'cancel-editor') {
          closeRowEditor(id);
        } else if (act === 'reset-editor') {
          resetRowEditor(id);
        } else if (act === 'save-editor') {
          saveRowEditor(id);
        } else if (act === 'view') {
          openProfile(id);
        } else if (act === 'toggle') {
          toggleStatus(id);
        }
      });
    }"""

new_wire = """    var dirRows = $id('dirRows');
    if (dirRows) {
      dirRows.addEventListener('click', function (e) {
        var actBtn = e.target.closest('[data-act]');
        if (!actBtn) return;
        var act = actBtn.getAttribute('data-act');
        var id = actBtn.getAttribute('data-id');

        if (act === 'toggle-expand') {
          toggleRowAccordion(id);
        } else if (act === 'edit-row') {
          openRowEditor(id);
        } else if (act === 'cancel-editor') {
          closeRowEditor(id);
        } else if (act === 'reset-editor') {
          resetRowEditor(id);
        } else if (act === 'save-editor') {
          saveRowEditor(id);
        } else if (act === 'view') {
          openProfile(id);
        } else if (act === 'toggle') {
          toggleStatus(id);
        }
      });
    }"""

with open(r'c:\Users\oudom\OneDrive\Desktop\NGIS-SYSTEM\assets\js\ngis-profiles.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated event propagation in ngis-profiles.js")

