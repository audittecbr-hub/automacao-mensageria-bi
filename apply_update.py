import subprocess
import json
import sys

def main():
    with open(r'c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\updated_painel_repasses_expr.txt', 'r', encoding='utf-8') as f:
        expr = f.read()

    print(f"Read updated expression: {len(expr)} characters.")

    proc = subprocess.Popen(
        [r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.5.3-win32-x64\server\powerbi-modeling-mcp.exe', '--start', '--skipconfirmation'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    def send_rpc(msg_id, method, params):
        req = {
            'jsonrpc': '2.0',
            'id': msg_id,
            'method': method,
            'params': params
        }
        proc.stdin.write(json.dumps(req) + '\n')
        proc.stdin.flush()
        line = proc.stdout.readline()
        return json.loads(line)

    # 1. Initialize
    init_res = send_rpc(1, 'initialize', {
        'protocolVersion': '2024-11-05',
        'capabilities': {},
        'clientInfo': {'name': 'updater', 'version': '1.0'}
    })
    print("Initialized MCP.")

    # Notification initialized
    proc.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
    proc.stdin.flush()

    # 2. Connect to localhost:63519
    conn_res = send_rpc(2, 'tools/call', {
        'name': 'connection_operations',
        'arguments': {
            'request': {
                'operation': 'Connect',
                'connectionString': 'Data Source=localhost:63519;Application Name=MCP-PBIModeling'
            }
        }
    })
    print("Connect response:", conn_res.get('result', conn_res.get('error')))

    # 3. Update measure
    update_res = send_rpc(3, 'tools/call', {
        'name': 'measure_operations',
        'arguments': {
            'request': {
                'operation': 'Update',
                'connectionName': 'PBIDesktop--63519',
                'definitions': [
                    {
                        'tableName': 'medidas_html',
                        'name': 'Painel_Repasses',
                        'expression': expr
                    }
                ]
            }
        }
    })
    print("Update result:")
    print(json.dumps(update_res, indent=2))

    proc.terminate()

if __name__ == '__main__':
    main()
