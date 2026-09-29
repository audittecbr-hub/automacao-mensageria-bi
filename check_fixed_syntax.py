import subprocess

with open('dump_apresentados_fixed.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('<script>') + len('<script>')
end = html.find('</script>')
js = html[start:end]

with open('test_fixed.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(["node", "-c", "test_fixed.js"], capture_output=True, text=True)
print("FIXED NODE SYNTAX CHECK:")
print("RETURNCODE:", res.returncode)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
