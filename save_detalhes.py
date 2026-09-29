import subprocess

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_detalhes.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = res.stdout.decode('latin1', errors='replace')
with open('detalhes_list.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved detalhes_list.txt")
