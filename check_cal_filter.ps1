$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's test if there is a filter on Calendario or any other table
$query = @"
EVALUATE
FILTER(
    SUMMARIZECOLUMNS(
        Calendario[Date],
        "Cnt", CALCULATE(COUNTROWS(vw_powerbi_relatorio_aprovacao), vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)),
        "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31))
    ),
    [Cnt] = 201 || ([Sum] > 47000000 && [Sum] < 48000000)
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
try {
    $adapter.Fill($dt) | Out-Null
    Write-Output "Found in Calendario: $($dt.Rows.Count)"
} catch {
    Write-Output "Error: $_"
}
$conn.Close()
