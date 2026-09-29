$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's test different combinations of filters:
# 1. Regional?
# 2. Produto?
# 3. Mes?
# 4. Status / Area?
# 5. DATA_RT >= 12/06 with some regional?

$query = @"
EVALUATE
SUMMARIZECOLUMNS(
    vw_powerbi_relatorio_aprovacao[Regional],
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 &&
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Count", COUNTROWS(vw_powerbi_relatorio_aprovacao),
    "Sum", SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO])
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-Table -AutoSize | Out-File -FilePath "regional_enc.txt" -Encoding UTF8

$conn.Close()
