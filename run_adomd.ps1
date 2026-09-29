$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "TOTAL_ENCONTRADO_All", SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]),
    "HONORARIO_TOTAL_ENCONTRADO_All", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
    "HONORARIO_TOTAL_ENCONTRADO_RT12", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "HONORARIO_TOTAL_ENCONTRADO_MovRange", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "TOTAL_APRESENTADO_All", SUM(vw_powerbi_relatorio_aprovacao[TOTAL_APRESENTADO]),
    "HONORARIO_TOTAL_APRESENTADO_All", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
    "HONORARIO_TOTAL_APRESENTADO_RT12", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "TOTAL_ENCONTRADO_RT12_MovRange", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "TOTAL_APRESENTADO_RT12_MovRange", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[TOTAL_APRESENTADO]),
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$dt | Format-List | Out-File -FilePath "adomd_results.txt" -Encoding UTF8
$conn.Close()
Write-Output "FINISHED_ADOMD_OK"
