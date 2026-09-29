import subprocess
import json
import os

exe_path = r'C:\Users\cristhofer.maciel.GRUPOSTUDIO\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe'

with open('clean_painel_repasses_expr.txt', 'r', encoding='utf-8') as f:
    clean_expr = f.read()

# Start process with --start flag
p = subprocess.Popen(
    [exe_path, '--start'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    encoding='utf-8'
)

def send_msg(msg):
    raw = json.dumps(msg)
    p.stdin.write(raw + '\n')
    p.stdin.flush()
    resp_raw = p.stdout.readline()
    try:
        return json.loads(resp_raw)
    except:
        return resp_raw

# 1. Initialize
init_msg = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "1.0"}
    }
}
resp1 = send_msg(init_msg)
print('Init response:', resp1)

# 2. Connect to port 57503
conn_msg = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "connection_operations",
        "arguments": {
            "request": {
                "operation": "Connect",
                "connectionString": "Data Source=localhost:57503;Application Name=MCP-Direct"
            }
        }
    }
}
resp2 = send_msg(conn_msg)
print('Connect response:', resp2)

# 3. Update Measure Painel_Repasses
update_msg = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "measure_operations",
        "arguments": {
            "request": {
                "operation": "Update",
                "definitions": [
                    {
                        "tableName": "medidas_html",
                        "name": "Painel_Repasses",
                        "expression": clean_expr
                    }
                ]
            }
        }
    }
}
resp3 = send_msg(update_msg)
print('Update response:', resp3)

# Close
p.stdin.close()
p.terminate()
p.wait()
