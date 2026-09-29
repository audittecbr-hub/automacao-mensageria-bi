$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$exprPath = "C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\matriz_updated.dax"
$expr = [System.IO.File]::ReadAllText($exprPath, [System.Text.Encoding]::UTF8)

$table = $model.Tables["medidas_html"]
$m = $table.Measures["Mockup_Honorarios_Matriz"]
$m.Expression = $expr

$model.SaveChanges()
Write-Output "SUCCESS_MATRIZ_UPDATED"
$server.Disconnect()
