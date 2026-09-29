$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
FILTER(
    SELECTCOLUMNS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        ),
        "Job", vw_powerbi_relatorio_aprovacao[JOB],
        "Cli", vw_powerbi_relatorio_aprovacao[NOME],
        "AreaAtual", vw_powerbi_relatorio_aprovacao[AREA_ATUAL],
        "DataRT", vw_powerbi_relatorio_aprovacao[DATA_RT],
        "DataMov", vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR],
        "Iniciais", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + 0,
        "Comp", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + 0,
        "Rest", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + 0,
        "Ajuiz", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO] + 0,
        "Val", [Honorários aprovados]
    ),
    [Val] > 0
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
$cnt = 0
$sum = 0
while ($rdr.Read()) {
    $cnt++
    $v = $rdr.GetValue(9)
    $sum += $v
}
Write-Output "Total rows: $cnt | Total sum: $sum"
$rdr.Close()
$conn.Close()
