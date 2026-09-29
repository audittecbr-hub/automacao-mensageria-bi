import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$t = $model.Tables["medidas_html"]

foreach ($name in @("HTML_Detalhamento_Encontrados", "HTML_Detalhamento_Apresentados", "HTML_Detalhamento_Aprovados", "HTML_Detalhamento_Negociacao", "HTML_Detalhamento_Perdidos", "HTML_Detalhamento_Nao_Aprovados")) {
    $m = $t.Measures[$name]
    if ($m) {
        Write-Output "=== $name ==="
        Write-Output $m.Expression
    }
}
$server.Disconnect()
"""

with open('dump_detalhes_dax.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "dump_detalhes_dax.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
with open('detalhes_expressions.txt', 'w', encoding='utf-8') as f:
    f.write(res.stdout.decode('latin1', errors='replace'))

print("Saved detalhes_expressions.txt")
