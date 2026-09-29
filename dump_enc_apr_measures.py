import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$t = $model.Tables["vw_powerbi_relatorio_aprovacao"]
foreach ($m in $t.Measures) {
    if ($m.Name -like "*encontrado*" -or $m.Name -like "*apresentado*") {
        Write-Output "=== $($m.Name) ==="
        Write-Output $m.Expression
    }
}

$server.Disconnect()
"""

with open('dump_enc_apr_measures.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "dump_enc_apr_measures.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(res.stdout.decode('latin1', errors='replace'))
