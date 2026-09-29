
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$results = @()
foreach ($t in $model.Tables) {
    foreach ($m in $t.Measures) {
        if ($m.Expression -match "TOTAL_ENCONTRADO|TOTAL_APRESENTADO|TOTAL_APROVADO|TOTAL_NAO_APROVADO|TOTAL_EM_NEGOCIACAO") {
            $results += "Table: $($t.Name) | Measure: $($m.Name)"
        }
    }
}
$results | Out-File -FilePath "measures_using_total.txt" -Encoding UTF8
$server.Disconnect()
