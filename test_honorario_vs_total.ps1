
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")

$query = @"
EVALUATE
ROW(
    'TOTAL_ENCONTRADO', CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    'HONORARIO_TOTAL_ENCONTRADO', CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    'TOTAL_APRESENTADO', CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[TOTAL_APRESENTADO]),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    'HONORARIO_TOTAL_APRESENTADO', CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    )
)
"@

$cmd = $server.Connection.CreateCommand()
$cmd.CommandText = $query
$rdr = $cmd.ExecuteReader()
while ($rdr.Read()) {
    Write-Output "TOTAL_ENCONTRADO: $($rdr.GetValue(0))"
    Write-Output "HONORARIO_TOTAL_ENCONTRADO: $($rdr.GetValue(1))"
    Write-Output "TOTAL_APRESENTADO: $($rdr.GetValue(2))"
    Write-Output "HONORARIO_TOTAL_APRESENTADO: $($rdr.GetValue(3))"
}

$server.Disconnect()
