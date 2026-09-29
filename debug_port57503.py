import subprocess
import json

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'

def test_q(query):
    p = subprocess.Popen([exe_path, '--start'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')
    def send(msg):
        p.stdin.write(json.dumps(msg) + '\n')
        p.stdin.flush()
        return json.loads(p.stdout.readline())
    send({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'sync', 'version': '1.0'}}})
    send({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:57503;Application Name=MCP-Direct'}}}})
    resp = send({'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'dax_query_operations', 'arguments': {'request': {'operation': 'Execute', 'query': query}}}})
    p.terminate()
    return resp

print('Test 1 {1}:', test_q('EVALUATE { 1 }'))
print('Test 2 COUNTROWS(Recebido):', test_q('EVALUATE { COUNTROWS(Recebido) }'))
print('Test 3 COUNTROWS(medidas_html):', test_q('EVALUATE { COUNTROWS(medidas_html) }'))
