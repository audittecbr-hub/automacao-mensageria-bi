$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
SUMMARIZECOLUMNS(
    vw_powerbi_relatorio_aprovacao[Regional],
    "Total_Com_RT", CALCULATE(
        SUMX(
            vw_powerbi_relatorio_aprovacao,
            COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
        ),
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO",
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL] IN {"AJUÍZAMENTO", "COMPENSAÇÃO", "ENTREGA", "IMPLANTAÇÃO", "RETIFICAÇÃO"},
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Total_Sem_RT", CALCULATE(
        SUMX(
            vw_powerbi_relatorio_aprovacao,
            COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
        ),
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO",
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL] IN {"AJUÍZAMENTO", "COMPENSAÇÃO", "ENTREGA", "IMPLANTAÇÃO", "RETIFICAÇÃO"},
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$lines = @()
foreach ($r in $dt.Rows) {
    $lines += "Regional: $($r[0]) | Com RT: $($r[1]) | Sem RT: $($r[2])"
}
[System.IO.File]::WriteAllLines("aprov_negoc_regional.txt", $lines, [System.Text.Encoding]::UTF8)
Write-Output "Saved aprov_negoc_regional.txt"
$conn.Close()
