import subprocess

out = subprocess.check_output(['git', 'log', '-S', 'hero-greeting', '-p'], encoding='utf-8', errors='ignore')
print(out[:4000])
