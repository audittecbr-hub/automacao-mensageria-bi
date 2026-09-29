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
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
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
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
)
"@

$dict["Honorários aprovados negociação iniciais"] = @"
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
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS]
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
Write-Output "SUCCESS_BASE_MEASURES_CLEAN"
$server.Disconnect()
