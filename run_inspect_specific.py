import subprocess

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "inspect_specific_detalhes.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = res.stdout.decode('latin1', errors='replace')
with open('specific_detalhes_output.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved specific_detalhes_output.txt")
