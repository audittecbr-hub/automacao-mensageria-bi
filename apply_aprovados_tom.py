import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$json = Get-Content -Raw -Encoding UTF8 "update_aprovados_payload.json" | ConvertFrom-Json

foreach ($item in $json) {
    $table = $model.Tables[$item.tableName]
    if ($table) {
        $m = $table.Measures[$item.name]
        if ($m) {
            $m.Expression = $item.expression
            Write-Output "Updated measure: $($item.name) in table $($item.tableName)"
        } else {
            Write-Output "Measure NOT found: $($item.name)"
        }
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_SAVED"
$server.Disconnect()
"""

with open('apply_aprovados_update.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "apply_aprovados_update.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(res.stdout.decode('latin1', errors='replace'))
if res.stderr:
    print(res.stderr.decode('latin1', errors='replace'))
