import os

path = 'assets/js/ui-states.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read().replace('\r\n', '\n')

old_showSkeleton = '''    showSkeleton(container, type = "table", count = 5) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      container.setAttribute("aria-busy", "true");

      // Save previous content in dataset if not already saved
      if (!container.dataset.ngisPrevContent) {
        container.dataset.ngisPrevContent = container.innerHTML || "";
      }

      let skeletonHtml = "";
      if (type === "table") {'''

new_showSkeleton = '''    showSkeleton(container, type = "list", count = 5) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      container.setAttribute("aria-busy", "true");

      // Save previous content in dataset if not already saved
      if (!container.dataset.ngisPrevContent) {
        container.dataset.ngisPrevContent = container.innerHTML || "";
      }

      if (window.NGISSkeleton && window.NGISSkeleton.templates && window.NGISSkeleton.templates[type]) {
        container.innerHTML = window.NGISSkeleton.templates[type](count);
        return;
      }

      let skeletonHtml = "";
      if (type === "table") {'''

if old_showSkeleton in content:
    content = content.replace(old_showSkeleton, new_showSkeleton)
    print("showSkeleton patched")
else:
    print("showSkeleton NOT found")

old_error_state = '''    renderErrorState(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;'''

new_error_state = '''    renderErrorState(container, options = {}) {
      if (typeof container === "string") container = document.querySelector(container);
      if (!container) return;

      if (window.NGISErrorState && typeof window.NGISErrorState.render === "function") {
        window.NGISErrorState.render(container, options);
        return;
      }'''

if old_error_state in content:
    content = content.replace(old_error_state, new_error_state)
    print("renderErrorState patched")
else:
    print("renderErrorState NOT found")

target_methods = '''    /* Global Initialization */'''
new_methods = '''    /* Rule 2: Honest 1-Tap Confirmation Dialog */
    confirmAction(options = {}) {
      if (window.NGISCancelDialog) {
        return window.NGISCancelDialog.open(options);
      }
      const proceed = window.confirm((options.title || "Confirm Action") + "\\n\\n" + (options.description || "") + "\\n\\nWhat happens next: " + (options.consequence || "Changes will be updated safely."));
      if (proceed && typeof options.onConfirm === "function") options.onConfirm();
      else if (!proceed && typeof options.onCancel === "function") options.onCancel();
    },

    /* Rule 1: Dedicated Screen Skeletons */
    showDashboardSkeleton(container) { return this.showSkeleton(container, "dashboard"); },
    showFeedSkeleton(container, count = 3) { return this.showSkeleton(container, "feed", count); },
    showListSkeleton(container, count = 6) { return this.showSkeleton(container, "list", count); },
    showDetailSkeleton(container) { return this.showSkeleton(container, "detail"); },
    showProfileSkeleton(container) { return this.showSkeleton(container, "profile"); },

    /* Global Initialization */'''

if target_methods in content:
    content = content.replace(target_methods, new_methods)
    print("methods added")
else:
    print("target_methods NOT found")

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Finished patching ui-states.js")

