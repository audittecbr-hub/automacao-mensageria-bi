$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
FILTER(
    SUMMARIZECOLUMNS(
        vw_powerbi_relatorio_aprovacao[JOB],
        vw_powerbi_relatorio_aprovacao[NOME],
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO],
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]
    ),
    vw_powerbi_relatorio_aprovacao[JOB] = "86730-FTX"
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-List | Out-File -FilePath "sandro_all_cols.txt" -Encoding UTF8
$conn.Close()
