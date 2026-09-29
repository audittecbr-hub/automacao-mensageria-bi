import subprocess

# Let's run a node script to parse the javascript in dump_apresentados.html
with open('dump_apresentados.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract script
start = html.find('<script>') + len('<script>')
end = html.find('</script>')
js = html[start:end]

with open('test_script.js', 'w', encoding='utf-8') as f:
    f.write(js)

res = subprocess.run(["node", "-c", "test_script.js"], capture_output=True, text=True)
print("NODE SYNTAX CHECK:")
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
