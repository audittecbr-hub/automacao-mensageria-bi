import subprocess

ps = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

foreach ($t in $model.Tables) {
    foreach ($m in $t.Measures) {
        if ($m.Name -like "*Encontrad*") {
            Write-Output "Table: $($t.Name) | Measure: $($m.Name)"
        }
    }
}
$server.Disconnect()
"""

with open('find_enc_measures.ps1', 'w', encoding='utf-8') as f:
    f.write(ps)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "find_enc_measures.ps1"], capture_output=True, text=True)
print(res.stdout)
