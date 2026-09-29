
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$json = Get-Content -Raw -Encoding UTF8 "create_detalhe_negociacao.json" | ConvertFrom-Json

foreach ($item in $json) {
    $table = $model.Tables[$item.tableName]
    if ($table) {
        $m = $table.Measures[$item.name]
        if (-not $m) {
            $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
            $m.Name = $item.name
            $table.Measures.Add($m)
            Write-Output "Created new measure: $($item.name)"
        } else {
            Write-Output "Updating existing measure: $($item.name)"
        }
        $m.Expression = $item.expression
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_SAVED"
$server.Disconnect()
