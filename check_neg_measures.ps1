$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$t = $model.Tables["medidas_html"]
foreach ($m in $t.Measures) {
    if ($m.Name -like "*Negoc*" -or $m.Name -like "*Perdido*" -or $m.Name -like "*Nao_Aprov*") {
        Write-Output "Measure: $($m.Name)"
    }
}
$server.Disconnect()
