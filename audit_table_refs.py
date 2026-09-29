import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'
p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
msg_id = 1
def send(msg):
    global msg_id
    msg['id'] = msg_id
    msg_id += 1
    p.stdin.write(json.dumps(msg) + '\n')
    p.stdin.flush()
    return json.loads(p.stdout.readline())

send({'jsonrpc': '2.0', 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'audit', 'version': '1.0'}}})
send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:59771;Application Name=MCP-Audit'}}}})

res = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'measure_operations', 'arguments': {'request': {'operation': 'List'}}}})
measures = res.get('result', {}).get('content', [{}])[0]
# The list returns names. Let's do ExportTMDL or Get
names = [m['name'] for m in json.loads(measures.get('text', '{}')).get('data', [])]
print(f'Total measures: {len(names)}')

# Let's get definitions in batches
t_search = ['metas_bruto', 'unidadesporcnpj', 'honorariosporjob', 'departamentos', 'vw_powerbi_job_repasse']
matches = {t: [] for t in t_search}

for name in names:
    r = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'measure_operations', 'arguments': {'request': {'operation': 'Get', 'references': [{'name': name}]}}}})
    content = r.get('result', {}).get('content', [{}])[0].get('text', '')
    content_lower = content.lower()
    for t in t_search:
        if t in content_lower:
            matches[t].append(name)

print("\n--- MEASURE REFERENCES AUDIT ---")
for t, m_list in matches.items():
    print(f"Table '{t}': referenced in {len(m_list)} measures: {m_list}")

p.terminate()
