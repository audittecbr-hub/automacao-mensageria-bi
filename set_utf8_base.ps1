
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model
$table = $model.Tables["vw_powerbi_relatorio_aprovacao"]

# Remove all measures
$toRemove = @()
foreach ($m in $table.Measures) { $toRemove += $m }
foreach ($m in $toRemove) { $table.Measures.Remove($m) }
$model.SaveChanges()

$dict = [System.Collections.Specialized.OrderedDictionary]::new()
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários encontrados")), "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO])")
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários apresentados")), "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO])")
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários aprovados")), @"
SUMX(
    vw_powerbi_relatorio_aprovacao,
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
)
"@)
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários perdidos")), "SUM(vw_powerbi_relatorio_aprovacao[HONORARIOS_ATUAL])")
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários não aprovados")), "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO])")
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorário negociação")), "SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO])")
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários aprovados em negociação")), @"
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
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
)
"@)
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários aprovados negociação iniciais")), @"
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
    COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0)
)
"@)
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários aprovados negociação compensação")), @"
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
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]
)
"@)
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários aprovados negociação restituição")), @"
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
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]
)
"@)
$dict.Add([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::UTF8.GetBytes("Honorários aprovados negociação ajuizamento")), @"
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
    vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
)
"@)

foreach ($k in $dict.Keys) {
    $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
    $m.Name = $k
    $m.Expression = $dict[$k]
    $table.Measures.Add($m)
}
$model.SaveChanges()
Write-Output "SUCCESS_UTF8_BASE_MEASURES"
$server.Disconnect()
