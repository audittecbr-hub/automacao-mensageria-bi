$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
SUMMARIZECOLUMNS(
    vw_powerbi_relatorio_aprovacao[NOME_LIDER_EQUIPE_RECEITA],
    "Cnt", CALCULATE(COUNTROWS(vw_powerbi_relatorio_aprovacao), vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)),
    "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31))
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

foreach ($r in $dt.Rows) {
    Write-Output "Lider: $($r[0]) | Cnt: $($r[1]) | Sum: $($r[2])"
}
$conn.Close()
