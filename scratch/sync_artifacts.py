import shutil, os

art_dir = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"

files = [
    "timetable_builder_desktop_1440.png",
    "timetable_builder_tablet_768.png",
    "timetable_builder_mobile_390.png",
    "timetables_master_desktop_1440.png",
    "timetables_master_mobile_390.png",
    "assignment_matrix_desktop_1440.png",
    "assignment_matrix_mobile_390.png",
    "data_entry_records_desktop_1440.png",
    "data_entry_records_mobile_390.png",
    "builder_mobile_sidebar_open.png"
]

for f in files:
    src = os.path.join("scratch", f)
    if os.path.exists(src):
        dst = os.path.join(art_dir, f)
        shutil.copyfile(src, dst)
        print(f"Copied {f} to artifacts directory.")

print("Artifact image sync complete!")

