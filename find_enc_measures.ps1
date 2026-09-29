
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
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
