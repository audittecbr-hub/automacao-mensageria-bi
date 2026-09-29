import subprocess

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_aprovacao_tom.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = res.stdout.decode('latin1', errors='replace')
with open('aprovacao_info.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved aprovacao_info.txt")
