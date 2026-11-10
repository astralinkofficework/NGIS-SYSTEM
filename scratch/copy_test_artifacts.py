import shutil
import os

art_dir = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"
files = [
    "test_search_sarah.png",
    "test_add_teacher_form.png",
    "test_excel_paste_modal.png",
    "test_mobile_390.png",
    "test_mobile_320.png"
]

for f in files:
    src = os.path.join("scratch", f)
    dst = os.path.join(art_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {f}: {os.path.getsize(dst)} bytes")

