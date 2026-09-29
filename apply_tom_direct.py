import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:57299")
$model = $server.Databases[0].Model

$measuresJson = Get-Content -Raw -Encoding UTF8 "updated_html_measures.json" | ConvertFrom-Json

foreach ($m in $measuresJson) {
    $table = $model.Tables[$m.tableName]
    if ($table) {
        $measure = $table.Measures[$m.name]
        if ($measure) {
            $measure.Expression = $m.expression
            Write-Output "Updated measure: $($m.name)"
        } else {
            Write-Output "Measure NOT found: $($m.name)"
        }
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_ALL_MEASURES_SAVED"
$server.Disconnect()
"""

with open('apply_measures_direct.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "apply_measures_direct.ps1"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(f"Error: {res.stderr}")
