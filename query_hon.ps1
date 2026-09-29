$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$db = $server.Databases[0]

$connStr = "Provider=MSOLAP;Data Source=localhost:54175;Initial Catalog=" + $db.Name
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

$query = @"
EVALUATE
ROW(
    'TOTAL_ENCONTRADO_All', SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]),
    'HONORARIO_TOTAL_ENCONTRADO_All', SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
    'HONORARIO_TOTAL_ENCONTRADO_RT12', CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    'TOTAL_APRESENTADO_All', SUM(vw_powerbi_relatorio_aprovacao[TOTAL_APRESENTADO]),
    'HONORARIO_TOTAL_APRESENTADO_All', SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
    'HONORARIO_TOTAL_APRESENTADO_RT12', CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12))
)
"@

$cmd = New-Object System.Data.OleDb.OleDbCommand($query, $conn)
$adapter = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$dt | Format-List | Out-File -FilePath "query_hon_results.txt" -Encoding UTF8
$conn.Close()
$server.Disconnect()
Write-Output "FINISHED_QUERY"
