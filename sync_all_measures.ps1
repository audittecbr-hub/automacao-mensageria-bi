$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$table = $model.Tables["vw_powerbi_relatorio_aprovacao"]
$dict = [System.Collections.Specialized.OrderedDictionary]::new()

$dict["Honorários aprovados"] = @"
SUMX(
    vw_powerbi_relatorio_aprovacao,
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)
)
"@

$dict["Honorários aprovados em negociação"] = @"
SUMX(
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        SEARCH("NEGOCI", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR], 1, 0) > 0 &&
        (
            SEARCH("AJU", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
            SEARCH("COMP", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
            SEARCH("ENTR", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
            SEARCH("IMPL", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
            SEARCH("RETIF", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0
        )
    ),
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)
)
"@

foreach ($k in $dict.Keys) {
    if ($table.Measures.Contains($k)) {
        $table.Measures[$k].Expression = $dict[$k]
    } else {
        $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
        $m.Name = $k
        $m.Expression = $dict[$k]
        $table.Measures.Add($m)
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_BASE_MEASURES_SYNCHRONIZED"

# Re-save Mockup_Honorarios_Matriz so it re-evaluates all measures
$exprMatriz = [System.IO.File]::ReadAllText("matriz_perfect.dax", [System.Text.Encoding]::UTF8)
$model.Tables["medidas_html"].Measures["Mockup_Honorarios_Matriz"].Expression = $exprMatriz
$model.SaveChanges()
Write-Output "SUCCESS_MATRIZ_RECALCULATED"

$server.Disconnect()
