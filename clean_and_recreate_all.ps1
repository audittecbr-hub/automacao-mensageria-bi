
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model
$table = $model.Tables["vw_powerbi_relatorio_aprovacao"]

# Remove all existing measures
$toRemove = @()
foreach ($m in $table.Measures) {
    $toRemove += $m
}
foreach ($m in $toRemove) {
    $table.Measures.Remove($m)
}
$model.SaveChanges()
Write-Output "Removed all existing measures in table"

$dict = [System.Collections.Specialized.OrderedDictionary]::new()

$dict["Honorários encontrados"] = "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO])"
$dict["Honorários apresentados"] = "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO])"
$dict["Honorários aprovados"] = @"
SUMX(
    vw_powerbi_relatorio_aprovacao,
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) +
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)
)
"@
$dict["Honorários perdidos"] = "SUM(vw_powerbi_relatorio_aprovacao[HONORARIOS_ATUAL])"
$dict["Honorários não aprovados"] = "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO])"
$dict["Honorário negociação"] = "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO])"

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
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0)
)
"@

$dict["Honorários aprovados negociação compensação"] = @"
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
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0)
)
"@

$dict["Honorários aprovados negociação restituição"] = @"
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
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0)
)
"@

$dict["Honorários aprovados negociação ajuizamento"] = @"
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
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)
)
"@

foreach ($k in $dict.Keys) {
    $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
    $m.Name = $k
    $m.Expression = $dict[$k]
    $table.Measures.Add($m)
    Write-Output "Added measure: $k"
}

$model.SaveChanges()

# Re-apply Mockup_Honorarios_Matriz
$exprMatriz = [System.IO.File]::ReadAllText("matriz_perfect.dax", [System.Text.Encoding]::UTF8)
$model.Tables["medidas_html"].Measures["Mockup_Honorarios_Matriz"].Expression = $exprMatriz
$model.SaveChanges()
Write-Output "SUCCESS_ALL_SYNCED"

$server.Disconnect()
