$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$json = Get-Content -Raw -Encoding UTF8 "update_mockup_font_payload.json" | ConvertFrom-Json

foreach ($item in $json) {
    $table = $model.Tables[$item.tableName]
    if ($table) {
        $m = $table.Measures[$item.name]
        if ($m) {
            $m.Expression = $item.expression
            Write-Output "Updated measure: $($item.name) in table $($item.tableName)"
        }
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_SAVED"
$server.Disconnect()
