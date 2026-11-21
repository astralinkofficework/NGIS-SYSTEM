with open('assets/css/interactions.css', 'r', encoding='utf-8') as f:
    it = f.read()

# Replace .portal-card in base rule in interactions.css:
it = it.replace(".demo-pill, .portal-card,", ".demo-pill, /* .portal-card, */")

with open('assets/css/interactions.css', 'w', encoding='utf-8') as f:
    f.write(it)

with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    ds = f.read()

# Exempt interactive cards from a[href]:hover:
ds = ds.replace("a[href]:hover,", "a[href]:not(.portal-card):not(.card-hover):not(.ql-card):not(.module-card):not(.dept-card):not(.task-card):not(.ann-card):not(.exam-card):not(.subj-card):not(.interactive-card):hover,")

with open('assets/css/design-system.css', 'w', encoding='utf-8') as f:
    f.write(ds)

print("Updated interactions.css and design-system.css successfully!")
