
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$t = $model.Tables["vw_powerbi_relatorio_aprovacao"]
foreach ($m in $t.Measures) {
    if ($m.Name -like "*encontrado*" -or $m.Name -like "*apresentado*") {
        Write-Output "=== $($m.Name) ==="
        Write-Output $m.Expression
    }
}

$server.Disconnect()
