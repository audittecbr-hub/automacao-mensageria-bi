# Let's inspect the exact lines of HTML_Detalhamento_Encontrados expression in the model
import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$t = $server.Databases[0].Model.Tables["medidas_html"]
$m = $t.Measures["HTML_Detalhamento_Encontrados"]
Write-Output $m.Expression
$server.Disconnect()
"""

with open('get_enc_expr.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_enc_expr.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
with open('enc_expr.txt', 'w', encoding='utf-8') as f:
    f.write(res.stdout.decode('latin1', errors='replace'))

with open('enc_expr.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if any(k in line for k in ['FILTER', 'CONCATENATEX', 'RETURN', 'VAR _linhas', 'vw_powerbi']):
            print(line.strip())
