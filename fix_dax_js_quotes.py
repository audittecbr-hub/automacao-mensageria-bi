import os
import re
import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'
tmdl_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl'

with open(tmdl_path, 'r', encoding='utf-8') as f:
    full_tmdl = f.read()

# Fix getCompositeKey to use single quotes
full_tmdl = full_tmdl.replace('return "";', "return '';")
full_tmdl = full_tmdl.replace('(r.job || "")', "(r.job || '')")
full_tmdl = full_tmdl.replace('(r.nf || "")', "(r.nf || '')")
full_tmdl = full_tmdl.replace('(r.bandeira || "")', "(r.bandeira || '')")
full_tmdl = full_tmdl.replace('(r.cnpj || "")', "(r.cnpj || '')")
full_tmdl = full_tmdl.replace('(j + "___" + n + "___" + b + "___" + c)', "(j + '___' + n + '___' + b + '___' + c)")
full_tmdl = full_tmdl.replace('compKey !== "______"', "compKey !== '______'")

# Write to TMDL files
for p in [r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl', r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\repasse.SemanticModel\definition\tables\medidas_html.tmdl']:
    if os.path.exists(p):
        with open(p, 'w', encoding='utf-8') as f:
            f.write(full_tmdl)
        print(f'Successfully updated TMDL: {p}')

# Extract DAX expression
pos_start = full_tmdl.find('measure Painel_Repasses =')
pos_end = full_tmdl.find('\n\tmeasure ', pos_start + 1)
if pos_end == -1: pos_end = len(full_tmdl)
painel_new = full_tmdl[pos_start:pos_end]

m = re.search(r'```([\s\S]*?)```', painel_new)
if m:
    lines = [l.replace('\t\t\t', '') for l in m.group(1).strip().splitlines()]
    raw_expr = '\n'.join(lines)

# Push live to Port 57503
p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
msg_id = 1
def send(msg):
    global msg_id
    msg['id'] = msg_id
    msg_id += 1
    p.stdin.write(json.dumps(msg) + '\n')
    p.stdin.flush()
    res = p.stdout.readline()
    try:
        return json.loads(res)
    except:
        return res

send({'jsonrpc': '2.0', 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'sync', 'version': '1.0'}}})
conn_resp = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:57503;Application Name=MCP-Direct'}}}})
print('Connect to 57503:', conn_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

upd_resp = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'measure_operations',
        'arguments': {
            'request': {
                'operation': 'Update',
                'Definitions': [
                    {
                        'Name': 'Painel_Repasses',
                        'TableName': 'medidas_html',
                        'Expression': raw_expr
                    }
                ]
            }
        }
    }
})
print('Update measure result:', upd_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

test_dax = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'dax_query_operations',
        'arguments': {
            'request': {
                'operation': 'Execute',
                'query': 'EVALUATE { LEN(medidas_html[Painel_Repasses]) }'
            }
        }
    }
})
for c in test_dax.get('result', {}).get('content', []):
    if 'resource' in c:
        print('DAX test result:', c['resource']['text'])

p.terminate()
