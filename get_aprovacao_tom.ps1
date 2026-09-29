
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
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
