$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "Super_Apv_RT", LEN(
        CONCATENATEX(
            FILTER(
                vw_powerbi_relatorio_aprovacao,
                (COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0 &&
                vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
            ),
            SWITCH(vw_powerbi_relatorio_aprovacao[Regional], "Regional Sul", "S", "Regional Sudeste", "SP", "Regional Sudeste 2", "SD", "Regional NNCO", "N", "O") & "|" & 
            LEFT(vw_powerbi_relatorio_aprovacao[AREA_ATUAL], 12) & "|" & 
            SUBSTITUTE(LEFT(vw_powerbi_relatorio_aprovacao[NOME], 22), "|", " ") & "|" & 
            vw_powerbi_relatorio_aprovacao[JOB] & "|" & 
            LEFT(vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO], 15) & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd") & "|" & 
            FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM-dd") & "|" & 
            FORMAT((COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]), "0.00"),
            "~"
        )
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    Write-Output "Super_Apv_RT length: $($rdr.GetValue(0)) bytes"
}
$conn.Close()
