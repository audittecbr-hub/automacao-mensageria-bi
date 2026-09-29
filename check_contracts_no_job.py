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
send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'connection_operations', 'arguments': {'request': {'operation': 'Connect', 'connectionString': 'Data Source=localhost:52661;Application Name=MCP-Audit'}}}})

# Run DAX query to inspect contracts without job in Agosto TAX
dax = '''
EVALUATE
VAR _DataCorte = DATE(2026, 8, 1)
VAR _BaseSemJob = 
    CALCULATETABLE(
        SUMMARIZE(
            Metas,
            Metas[codigo_lancamento_omie],
            Metas[numero_contrato],
            Metas[cnpj_cpf],
            Metas[razao_social],
            Metas[bandeira]
        ),
        Metas[data_emissao] >= _DataCorte,
        UPPER(Metas[categoria]) = "TAX",
        (ISBLANK(Metas[numero_contrato]) || Metas[numero_contrato] = ""),
        Calendario[MesNome] = "Agosto",
        Calendario[Ano] = 2026
    )

VAR _ComValor = 
    ADDCOLUMNS(
        _BaseSemJob,
        "ValorConta", CALCULATE(SUM(Metas[valor_conta]))
    )

RETURN
_ComValor
'''

r = send({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'dax_query_operations', 'arguments': {'request': {'operation': 'Execute', 'query': dax}}}})
print("=== CONTRACTS WITHOUT JOB IN AGOSTO TAX ===")
for c in r.get('result', {}).get('content', []):
    if 'resource' in c:
        print(c['resource']['text'][:2000])

p.terminate()
