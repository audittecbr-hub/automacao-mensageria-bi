$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$m = $model.Tables["medidas_html"].Measures["Mockup_Honorarios_Matriz"]
if ($m) {
    [System.IO.File]::WriteAllText("Mockup_Honorarios_Matriz_Current.dax", $m.Expression, [System.Text.Encoding]::UTF8)
    Write-Output "DUMPED"
}
$server.Disconnect()
