$tabularDll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

foreach ($t in $model.Tables) {
    foreach ($m in $t.Measures) {
        if ($m.Expression -like "*CRÉDITO SEM HON*" -or $m.Expression -like "*CREDITO SEM HON*") {
            Write-Output "Table: $($t.Name) | Measure: $($m.Name)"
        }
    }
}
$server.Disconnect()
