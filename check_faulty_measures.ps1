$tabularDll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$t = $model.Tables["medidas_html"]
foreach ($name in @("HTML_Detalhamento_Reforma", "HTML_Detalhamento_Supply", "HTML_Detalhamento_Transacao")) {
    $m = $t.Measures[$name]
    if ($m) {
        Write-Output "=== $name ==="
        Write-Output $m.Expression.Substring(0, [Math]::Min(300, $m.Expression.Length))
    }
}
$server.Disconnect()
