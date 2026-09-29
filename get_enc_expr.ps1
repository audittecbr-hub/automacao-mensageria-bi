
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$t = $server.Databases[0].Model.Tables["medidas_html"]
$m = $t.Measures["HTML_Detalhamento_Encontrados"]
Write-Output $m.Expression
$server.Disconnect()
