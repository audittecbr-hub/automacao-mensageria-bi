import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$table = $model.Tables["vw_powerbi_relatorio_aprovacao"]
if ($table) {
    Write-Output "Table found: $($table.Name)"
    foreach ($col in $table.Columns) {
        Write-Output "  Col: $($col.Name) ($($col.DataType))"
    }
    foreach ($m in $table.Measures) {
        Write-Output "  Measure: $($m.Name) = $($m.Expression)"
    }
} else {
    Write-Output "Table NOT found"
}

$server.Disconnect()
"""

with open('get_aprovacao_tom.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_aprovacao_tom.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(f"Error: {res.stderr}")
