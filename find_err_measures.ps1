$tabularDll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

foreach ($table in $model.Tables) {
    foreach ($m in $table.Measures) {
        if (![string]::IsNullOrEmpty($m.ErrorMessage)) {
            Write-Output "Table: $($table.Name) | Measure: $($m.Name) | Error: $($m.ErrorMessage)"
        }
    }
}
$server.Disconnect()
