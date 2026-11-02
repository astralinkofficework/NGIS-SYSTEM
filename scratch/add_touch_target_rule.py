with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    css = f.read()

rule = """
/* Mandatory Mobile Hamburger Minimum Touch Target (38-44px) */
.hamburger-btn,
.mobile-hamburger-btn,
.htb-hamburger,
button[data-action="toggle-sidebar"] {
  min-width: 38px !important;
  min-height: 38px !important;
}
"""

if 'Mandatory Mobile Hamburger Minimum Touch Target' not in css:
    css += '\n' + rule
    with open('assets/css/app.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added mobile touch target rule')
else:
    print('Already present')

