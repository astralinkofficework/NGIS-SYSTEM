import re

def inspect_lost_found():
    with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
        text = f.read()
    modals = re.findall(r'id="([^"]*modal[^"]*)"', text, re.IGNORECASE)
    print("Lost Found Modals:", set(modals))
    
    # Check JS functions
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
    print("JS Functions:", funcs[:20])

def inspect_services():
    with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
        text = f.read()
    modals = re.findall(r'id="([^"]*modal[^"]*)"', text, re.IGNORECASE)
    print("Student Services Modals:", set(modals))
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
    print("Student Services Functions:", funcs[:20])

inspect_lost_found()
inspect_services()

