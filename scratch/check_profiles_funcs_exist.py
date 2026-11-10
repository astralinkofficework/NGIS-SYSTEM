with open('assets/js/ngis-profiles.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of ngis-profiles.js:", len(text))
print("Contains openProfile:", "openProfile" in text)
print("Contains renderProfileShell:", "renderProfileShell" in text)
print("Contains tabBody:", "tabBody" in text)
print("Contains docsTabMarkup:", "docsTabMarkup" in text)
print("Contains uploadDoc:", "uploadDoc" in text)
print("Contains deleteDoc:", "deleteDoc" in text)
print("Contains confirmDlg:", "confirmDlg" in text)

