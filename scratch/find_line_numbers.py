with open('assets/js/khmer-suite-ui.js', encoding='utf-8') as f:
    for i, line in enumerate(f):
        for term in ['viewSwitcher', 'MoEYS Guidelines', 'វិទ្យាល័យ ហ្គេតវេ', 'Standard Cambodian National Curriculum']:
            if term in line:
                print(f'{i+1}: [{term}] -> {line.strip()[:100]}')

