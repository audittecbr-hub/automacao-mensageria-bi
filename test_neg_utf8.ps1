$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
FILTER(
    SUMMARIZECOLUMNS(
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR],
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL],
        "Cnt", COUNTROWS(vw_powerbi_relatorio_aprovacao),
        "Hon_Iniciais", SUM(vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS]),
        "Hon_Comp", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]),
        "Hon_Rest", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]),
        "Hon_Ajuiz", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]),
        "Hon_Total", SUMX(
            vw_powerbi_relatorio_aprovacao,
            COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
        )
    ),
    SEARCH("NEGOCI", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR], 1, 0) > 0
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$lines = @()
foreach ($r in $dt.Rows) {
    $lines += "Ant: '$($r[0])' | Atual: '$($r[1])' | Cnt: $($r[2]) | Iniciais: $($r[3]) | Comp: $($r[4]) | Rest: $($r[5]) | Ajuiz: $($r[6]) | Total: $($r[7])"
}
[System.IO.File]::WriteAllLines("negoc_results.txt", $lines, [System.Text.Encoding]::UTF8)
Write-Output "Saved negoc_results.txt"
$conn.Close()
