$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$table = $model.Tables["vw_powerbi_relatorio_aprovacao"]
foreach ($m in $table.Measures) {
    if ($m.Name -like "*negocia*" -or $m.Name -like "*aprov*") {
        Write-Output "Measure: '$($m.Name)'"
    }
}
$server.Disconnect()
