import subprocess
import json

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'

with open('painel_repasses_fixed_expr.txt', 'r', encoding='utf-8') as f:
    full_expr = f.read()

# Let's test evaluating parts of full_expr
def test_eval(dax_block):
    p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')
    def send(msg):
        p.stdin.write(json.dumps(msg) + '\n')
        p.stdin.flush()
        return json.loads(p.stdout.readline())
    send({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'sync', 'version': '1.0'}}})
    send({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:57503;Application Name=MCP-Direct'}}}})
    resp = send({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'dax_query_operations', 'arguments': {'request': {'operation': 'Execute', 'query': f'EVALUATE {{ {dax_block} }}'}}}})
    p.terminate()
    return resp

print('Testing full_expr as measure...')
resp = test_eval(full_expr)
print('Result:', resp.get('result', {}).get('content', [{}])[0].get('text', ''))
