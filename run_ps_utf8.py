import subprocess

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_aprovacao_tom.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = res.stdout.decode('utf-8', errors='replace')
print(text)
