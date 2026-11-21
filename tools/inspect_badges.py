import re

def check_file(path):
    print(f"=== {path} ===")
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    badges = re.findall(r'class="[^"]*(?:badge|pill|tag|chip|dot)[^"]*"', text)
    for b in sorted(set(badges)):
        print(" ", b)

if __name__ == '__main__':
    check_file('pages/student/student-calendar.html')
    check_file('assets/js/academic-calendar.js')
    check_file('pages/student/student.html')
    check_file('pages/student/js/workspace.js')
