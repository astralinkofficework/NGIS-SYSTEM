with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """  function fixInlineColors() {
    document.querySelectorAll("[style]").forEach(el => {"""

new_code = """  function fixInlineColors() {
    /* Only target legacy notification items, never overlap decks or modern components */
    document.querySelectorAll(".notifications-feed .notif-item-raw[style]").forEach(el => {"""

if old_code in content:
    content = content.replace(old_code, new_code, 1)
    with open('assets/js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("OLD CODE NOT FOUND")

