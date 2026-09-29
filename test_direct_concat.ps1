$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "Test_Compact",
    CONCATENATEX(
        TOPN(
            5,
            FILTER(
                vw_powerbi_relatorio_aprovacao,
                vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0
            ),
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], DESC
        ),
        vw_powerbi_relatorio_aprovacao[Regional] & "|" & 
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL] & "|" & 
        SUBSTITUTE(LEFT(vw_powerbi_relatorio_aprovacao[NOME], 35), "|", " ") & "|" & 
        vw_powerbi_relatorio_aprovacao[JOB] & "|" & 
        vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] & "|" & 
        FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "dd/MM/yyyy") & "|" & 
        FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "dd/MM/yyyy") & "|" & 
        FORMAT(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], "0.00") & "|" & 
        FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") & "|" & 
        FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd") & "|" & 
        FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM-dd"),
        "~"
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    Write-Output "SUCCESS:"
    Write-Output $rdr.GetValue(0)
}
$conn.Close()
