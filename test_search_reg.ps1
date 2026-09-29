$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
FILTER(
    SUMMARIZECOLUMNS(
        vw_powerbi_relatorio_aprovacao[Regional],
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR],
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL],
        "Hon_Total", SUMX(
            vw_powerbi_relatorio_aprovacao,
            COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
        )
    ),
    SEARCH("NEGOCI", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR], 1, 0) > 0 &&
    (
        SEARCH("AJU", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
        SEARCH("COMP", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
        SEARCH("ENTR", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
        SEARCH("IMPL", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0 ||
        SEARCH("RETIF", vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 1, 0) > 0
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$lines = @()
foreach ($r in $dt.Rows) {
    $lines += "Regional: '$($r[0])' | Ant: '$($r[1])' | Atual: '$($r[2])' | Hon_Total: $($r[3])"
}
[System.IO.File]::WriteAllLines("aprov_negoc_regional.txt", $lines, [System.Text.Encoding]::UTF8)
Write-Output "Saved aprov_negoc_regional.txt, count: $($dt.Rows.Count)"
$conn.Close()
