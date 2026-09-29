$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
SUMMARIZE(
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    vw_powerbi_relatorio_aprovacao[Regional],
    "SumAprovados",
    SUMX(
        vw_powerbi_relatorio_aprovacao,
        COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], 0) + 
        COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO], 0) + 
        COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO], 0) + 
        COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO], 0)
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
while ($rdr.Read()) {
    Write-Output "Regional: $($rdr.GetValue(0)) | Sum: $($rdr.GetValue(1))"
}
$rdr.Close()
$conn.Close()
