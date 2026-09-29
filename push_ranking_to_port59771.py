import re
import json
import subprocess

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'
tmdl_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.SemanticModel\definition\tables\Medidas_Repasse.tmdl'

with open(tmdl_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract measures
measure_blocks = re.findall(r'measure\s+([^\=]+)=([\s\S]*?)(?=\n\tmeasure|\Z)', text)

measures_to_update = []
target_names = [
    'valor_Tax_Repasse',
    'Valor_Corporate_Repasse',
    'Valor_PJ_Repasse',
    'Valor_Expansao_Repasse',
    'Valor_Franchising_Repasse',
    'Valor_Educacao_Repasse'
]

for name_raw, body in measure_blocks:
    name = name_raw.strip()
    if name in target_names:
        m = re.search(r'```([\s\S]*?)```', body)
        if m:
            expr = m.group(1).strip()
            lines = [l.replace('\t\t\t', '') for l in expr.splitlines()]
            clean_expr = '\n'.join(lines)
            measures_to_update.append({
                'Name': name,
                'TableName': 'Medidas_Repasse',
                'Expression': clean_expr
            })

print(f'Found {len(measures_to_update)} measures to update live.')

# Start MCP
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

# 1. Initialize
send({'jsonrpc': '2.0', 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'sync', 'version': '1.0'}}})

# 2. Connect to Port 59771
conn_resp = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'connection_operations',
        'arguments': {
            'request': {
                'operation': 'Connect',
                'connectionString': 'Data Source=localhost:59771;Application Name=MCP-Direct'
            }
        }
    }
})
print('Connect to 59771:', conn_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

# 3. Update measures in Medidas_Repasse
upd_resp = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'measure_operations',
        'arguments': {
            'request': {
                'operation': 'Update',
                'Definitions': measures_to_update
            }
        }
    }
})
print('Update result:', upd_resp.get('result', {}).get('content', [{}])[0].get('text', ''))

# 4. Run DAX test query to verify calculations
test_dax = send({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {
        'name': 'dax_query_operations',
        'arguments': {
            'request': {
                'operation': 'Execute',
                'query': '''
                EVALUATE 
                ROW(
                    "Tax", [valor_Tax_Repasse],
                    "Corporate", [Valor_Corporate_Repasse],
                    "PJ", [Valor_PJ_Repasse],
                    "Expansao", [Valor_Expansao_Repasse],
                    "Franchising", [Valor_Franchising_Repasse],
                    "Educacao", [Valor_Educacao_Repasse],
                    "Total", [total_repasse]
                )
                '''
            }
        }
    }
})
print('DAX Test Result:')
for c in test_dax.get('result', {}).get('content', []):
    if 'resource' in c:
        print(c['resource']['text'])

p.terminate()
