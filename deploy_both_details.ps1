$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model
$table = $model.Tables["medidas_html"]

function SetMeasure($name, $file) {
    $expr = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)
    if ($table.Measures.Contains($name)) {
        $table.Measures[$name].Expression = $expr
    } else {
        $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
        $m.Name = $name
        $m.Expression = $expr
        $table.Measures.Add($m)
    }
    Write-Output "Set measure: $name"
}

SetMeasure "HTML_Detalhamento_Aprovados" "HTML_Detalhamento_Aprovados_final.dax"
SetMeasure "HTML_Detalhamento_Aprovados_Negociacao" "HTML_Detalhamento_Aprovados_Negociacao_final.dax"

$model.SaveChanges()
Write-Output "SUCCESS_SAVED_ALL_DETAIL_MEASURES"
$server.Disconnect()
