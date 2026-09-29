$tabularDll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$m = $model.Tables["medidas_html"].Measures["Mockup_Honorarios_Matriz"]
[System.IO.File]::WriteAllText("matriz_current.dax", $m.Expression, [System.Text.Encoding]::UTF8)
Write-Output "Saved matriz_current.dax"
$server.Disconnect()
