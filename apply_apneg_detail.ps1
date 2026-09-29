$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$exprPath = "C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\HTML_Detalhamento_Aprovados_Negociacao.dax"
$expr = [System.IO.File]::ReadAllText($exprPath, [System.Text.Encoding]::UTF8)

$table = $model.Tables["medidas_html"]
$measureName = "HTML_Detalhamento_Aprovados_Negociacao"
if ($table.Measures.Contains($measureName)) {
    $table.Measures[$measureName].Expression = $expr
} else {
    $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
    $m.Name = $measureName
    $m.Expression = $expr
    $table.Measures.Add($m)
}

$model.SaveChanges()
Write-Output "SUCCESS_APNEG_DETAIL_SAVED"
$server.Disconnect()
