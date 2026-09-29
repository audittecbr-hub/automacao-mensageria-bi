$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "Ultra_Enc_All", LEN(
        CONCATENATEX(
            FILTER(
                vw_powerbi_relatorio_aprovacao,
                vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
            ),
            vw_powerbi_relatorio_aprovacao[Regional] & "|" & 
            vw_powerbi_relatorio_aprovacao[AREA_ATUAL] & "|" & 
            SUBSTITUTE(LEFT(vw_powerbi_relatorio_aprovacao[NOME], 30), "|", " ") & "|" & 
            vw_powerbi_relatorio_aprovacao[JOB] & "|" & 
            vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd") & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM-dd") & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], "0.00"),
            "~"
        )
    ),
    "Ultra_Enc_RT", LEN(
        CONCATENATEX(
            FILTER(
                vw_powerbi_relatorio_aprovacao,
                vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
                vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
            ),
            vw_powerbi_relatorio_aprovacao[Regional] & "|" & 
            vw_powerbi_relatorio_aprovacao[AREA_ATUAL] & "|" & 
            SUBSTITUTE(LEFT(vw_powerbi_relatorio_aprovacao[NOME], 30), "|", " ") & "|" & 
            vw_powerbi_relatorio_aprovacao[JOB] & "|" & 
            vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd") & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM-dd") & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], "0.00"),
            "~"
        )
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    Write-Output "Ultra_Enc_All length: $($rdr.GetValue(0)) bytes"
    Write-Output "Ultra_Enc_RT length: $($rdr.GetValue(1)) bytes"
}
$conn.Close()
