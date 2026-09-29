$tabularDll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$t = $model.Tables["medidas_html"]
$m = $t.Measures["HTML_Detalhamento_Negociacao"]
if ($m) {
    [System.IO.File]::WriteAllText("negociacao_err.txt", $m.ErrorMessage, [System.Text.Encoding]::UTF8)
    Write-Output "WROTE_ERR"
}
$server.Disconnect()
