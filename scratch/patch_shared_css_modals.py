with open("assets/css/shared-components.css", "r", encoding="utf-8") as f:
    text = f.read()

target = """.modal-backdrop,
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--token-space-4);
}

.modal,
.modal-dialog,
.ngis-modal {
  background-color: var(--token-surface);
  border: 1px solid var(--token-border);
  border-radius: var(--token-radius-card);
  box-shadow: var(--token-shadow-float);
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  z-index: 101;
  text-align: left;
}"""

replacement = """.modal-backdrop,
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(15, 23, 42, 0.42);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal,
.modal-dialog,
.modal-card,
.ngis-modal {
  background-color: var(--token-surface, #FFFFFF);
  border: 1px solid var(--token-border, #E1E9E3);
  border-radius: 1rem;
  box-shadow: 0 25px 60px -15px rgba(15, 23, 42, 0.22);
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  z-index: 101;
  text-align: left;
}"""

if target in text:
    text = text.replace(target, replacement, 1)
    print("Modals section replaced!")
else:
    print("Modals section target not matched!")

target_mobile = """/* Mobile Fullscreen Modals */
@media (max-width: 639px) {
  .modal-dialog,
  .modal {
    max-width: 100% !important;
    height: 100% !important;
    max-height: 100vh !important;
    border-radius: 0 !important;
    margin: 0 !important;
  }
}"""

replacement_mobile = """/* Mobile Responsive Modern Sheet Modals */
@media (max-width: 639px) {
  .modal-backdrop,
  .drawer-backdrop {
    padding: 0.75rem !important;
    align-items: flex-end !important;
  }
  .modal-dialog,
  .modal,
  .modal-card {
    max-width: 100% !important;
    max-height: 92vh !important;
    border-radius: 1.25rem !important;
    margin: 0 auto !important;
  }
}"""

if target_mobile in text:
    text = text.replace(target_mobile, replacement_mobile, 1)
    print("Mobile modal section replaced!")
else:
    print("Mobile modal target not matched!")

with open("assets/css/shared-components.css", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated shared-components.css")

