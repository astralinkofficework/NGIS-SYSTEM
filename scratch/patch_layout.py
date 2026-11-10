with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if '/* UI States Master Engine */' in line:
        start_idx = i
    if start_idx is not None and 'window.toast = function' in line:
        end_idx = i
        break

print(f"Found block: {start_idx} to {end_idx}")

new_lines = [
    '    /* UI States & Master Components Engine (Rules 1-5 Reusable Standards) */\n',
    '    if (!document.querySelector(\'link[href*="ui-states.css"]\')) {\n',
    '      const lu = document.createElement("link");\n',
    '      lu.rel = "stylesheet";\n',
    '      lu.href = _P + "assets/css/ui-states.css";\n',
    '      document.head.appendChild(lu);\n',
    '    }\n',
    '\n',
    '    const sharedComponents = [\n',
    '      "assets/js/error-messages.js",\n',
    '      "assets/js/error-boundary.js",\n',
    '      "assets/components/skeleton.js",\n',
    '      "assets/components/error-state.js",\n',
    '      "assets/components/empty-state.js",\n',
    '      "assets/components/primary-button.js",\n',
    '      "assets/components/cancel-dialog.js",\n',
    '      "assets/components/onboarding-layout.js",\n',
    '      "assets/js/ui-states.js"\n',
    '    ];\n',
    '\n',
    '    sharedComponents.forEach(scriptPath => {\n',
    '      const scriptTag = document.createElement("script");\n',
    '      scriptTag.src = _P + scriptPath;\n',
    '      scriptTag.defer = true;\n',
    '      document.body.appendChild(scriptTag);\n',
    '    });\n',
    '  }\n',
    '\n'
]

lines[start_idx:end_idx] = new_lines

with open('assets/js/layout.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Successfully replaced block in layout.js")
