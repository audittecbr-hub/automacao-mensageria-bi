$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "Count_Enc_Total_Encontrado_MovRange", COUNTROWS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        )
    ),
    "Sum_Enc_Total_Encontrado_MovRange", SUMX(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        ),
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]
    ),
    "Count_Enc_Hon_Total_Encontrado_MovRange", COUNTROWS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        )
    ),
    "Sum_Enc_Hon_Total_Encontrado_MovRange", SUMX(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        ),
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]
    ),
    "Count_Enc_RT_Total_Encontrado", COUNTROWS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        )
    ),
    "Sum_Enc_RT_Total_Encontrado", SUMX(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        ),
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]
    ),
    "Count_Enc_RT_Hon_Encontrado", COUNTROWS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        )
    ),
    "Sum_Enc_RT_Hon_Encontrado", SUMX(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        ),
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$dt | Format-List | Out-File -FilePath "enc_counts.txt" -Encoding UTF8
$conn.Close()
