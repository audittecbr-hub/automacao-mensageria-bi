$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "Hon_Encontrados_Card", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Hon_Apresentados_Card", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APRESENTADO]),
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA",
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Hon_Aprovados_Card", CALCULATE(
        SUMX(
            vw_powerbi_relatorio_aprovacao,
            COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
        ),
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Hon_Negociacao_Card", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_EM_NEGOCIACAO]),
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA",
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "NEGOCIAÇÃO",
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Hon_Perdidos_Card", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO",
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM",
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Hon_NaoAprov_Card", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_NAO_APROVADO]),
        vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "REUNIÃO TÉCNICA",
        vw_powerbi_relatorio_aprovacao[AREA_ATUAL] = "FIM",
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-List | Out-File -FilePath "all_hon_cards.txt" -Encoding UTF8
$conn.Close()
