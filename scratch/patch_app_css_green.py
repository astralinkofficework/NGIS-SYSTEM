import re

with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Foundation variable replacements
replacements = [
    # Hex color replacements
    (r'--charcoal-blue:\s*#052659;', '--charcoal-blue: #176B45;'),
    (r'--light-blue:\s*#EAF6FF;', '--light-blue: #E8F3ED;'),
    (r'--ghost-white:\s*#EAF6FF;', '--ghost-white: #F7F9F7;'),
    (r'--surface-3:\s*#EAF6FF;', '--surface-3: #E8F3ED;'),
    (r'--color-primary:\s*#052659;', '--color-primary: #176B45;'),
    (r'--color-primary-hover:\s*#052659;', '--color-primary-hover: #125638;'),
    (r'--color-primary-soft:\s*#EAF6FF;', '--color-primary-soft: #E8F3ED;'),
    (r'--color-background:\s*#EAF6FF;', '--color-background: #F7F9F7;'),
    (r'--color-surface-secondary:\s*#EAF6FF;', '--color-surface-secondary: #E8F3ED;'),
    (r'--color-text-secondary:\s*#052659;', '--color-text-secondary: #64746A;'),
    (r'--color-border:\s*#DCE8F3;', '--color-border: #E1E9E3;'),
    
    # Midnight & Deep blue to Forest Green #176B45
    ('var(--color-midnight, #021024)', 'var(--color-primary, #176B45)'),
    ('var(--color-deep-blue, #052659)', 'var(--color-primary, #176B45)'),
    ('var(--color-royal-blue, #052659)', 'var(--color-primary, #176B45)'),
    ('var(--color-light-blue, #C1E8FF)', 'var(--color-mint, #E8F3ED)'),
    ('var(--color-muted-blue, #7DA0CA)', 'var(--color-text-secondary, #64746A)'),
    ('rgba(193, 232, 255, 0.1)', 'rgba(232, 243, 237, 0.15)'),
    ('rgba(220, 232, 243, 0.12)', 'rgba(225, 233, 227, 0.15)'),
    ('rgba(220, 232, 243, 0.2)', 'rgba(225, 233, 227, 0.2)'),
    
    # Active navigation link in sidebar
    ("""/* Active State: Light Blue #C1E8FF Container with Midnight Navy #021024 Text & Icon */
.sidebar .nav-link.active,
.nav-group-label-link.active {
  background: var(--color-mint, #E8F3ED) !important;
  background-color: var(--color-mint, #E8F3ED) !important;
  border: 1px solid var(--color-mint, #E8F3ED) !important;
  border-radius: 10px !important;
  color: var(--color-primary, #176B45) !important;
  font-weight: 500 !important;
  box-shadow: none !important;
}""", """/* Active State: Soft Mint #E8F3ED Container with Forest Green #176B45 Text & Icon */
.sidebar .nav-link.active,
.nav-group-label-link.active {
  background: var(--color-mint, #E8F3ED) !important;
  background-color: var(--color-mint, #E8F3ED) !important;
  border: 1px solid var(--color-mint, #E8F3ED) !important;
  border-radius: 10px !important;
  color: var(--color-primary, #176B45) !important;
  font-weight: 500 !important;
  box-shadow: none !important;
}"""),

    # Direct hex substitutions where appropriate
    ('border: 1px solid #DCE8F3', 'border: 1px solid #E1E9E3'),
    ('border-color: #DCE8F3', 'border-color: #E1E9E3'),
    ('background: #052659', 'background: #176B45'),
    ('background-color: #052659', 'background-color: #176B45'),
    ('border-color: #052659', 'border-color: #176B45'),
    ('border: 2px solid #052659', 'border: 2px solid #176B45'),
    ('border: 1.5px solid #052659', 'border: 1.5px solid #176B45'),
    ('background: #EAF6FF', 'background: #F7F9F7'),
    ('background-color: #EAF6FF', 'background-color: #F7F9F7'),
    ('background: var(--token-accent-soft, #EAF6FF)', 'background: var(--token-surface-subtle, #E8F3ED)'),
    ('background: var(--token-surface-subtle, #EAF6FF)', 'background: var(--token-surface-subtle, #E8F3ED)'),
    ('border: 1px solid var(--token-border, #DCE8F3)', 'border: 1px solid var(--token-border, #E1E9E3)'),
    ('border-color: var(--token-border, #DCE8F3)', 'border-color: var(--token-border, #E1E9E3)'),
    ('border-color: var(--token-accent-border, #DCE8F3)', 'border-color: var(--token-accent-border, #E1E9E3)'),
    ('background: #021024', 'background: #176B45'),
    ('background: linear-gradient(135deg, #052659, #021024)', 'linear-gradient(135deg, #125638, #176B45)'),
    ('.bn-badge { animation: none !important; box-shadow: none !important; background: #052659 !important; }',
     '.bn-badge { animation: none !important; box-shadow: none !important; background: #F28C28 !important; color: #FFFFFF !important; }')
]

for src, dst in replacements:
    text = text.replace(src, dst)

# Specific fixes for active text color inside active nav links
text = text.replace(
    'color: var(--color-midnight, #021024) !important;',
    'color: var(--color-primary, #176B45) !important;'
)

# Sidebar mobile close button
text = text.replace(
    'border: 1px solid #DCE8F3 !important;\n    background: #ffffff !important;\n    color: #000000 !important;',
    'border: 1px solid #E1E9E3 !important;\n    background: #ffffff !important;\n    color: #29352E !important;'
)
text = text.replace(
    'background: #EAF6FF !important;',
    'background: #E8F3ED !important;'
)

with open('assets/css/app.css', 'w', encoding='utf-8') as f:
    f.write(text)

print('app.css updated successfully.')

