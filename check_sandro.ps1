$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's check if the visual was using a measure or if a column in the visual has 47186526.49
# In Image 1, Row 1 has Sandro Renato Barb with 14.511,22. Let's see what row that is:
$query = @"
EVALUATE
FILTER(
    SUMMARIZECOLUMNS(
        vw_powerbi_relatorio_aprovacao[JOB],
        vw_powerbi_relatorio_aprovacao[NOME],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO],
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APROVADO]
    ),
    vw_powerbi_relatorio_aprovacao[JOB] = "86730-FTX"
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-Table -AutoSize | Out-File -FilePath "sandro_check.txt" -Encoding UTF8
$conn.Close()
