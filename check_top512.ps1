$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's test if the visual in PBI is showing only 512 rows because:
# A) The user or page has a slicer/filter (e.g. DATA_RT >= 12/06 or specific product/month)
# B) Or TOPN 512?
# Let's check TOPN 512:
$query = @"
EVALUATE
ROW(
    "Sum_Top512_Total_Enc", SUMX(
        TOPN(
            512,
            FILTER(
                vw_powerbi_relatorio_aprovacao,
                vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
            ),
            vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO], DESC
        ),
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO]
    ),
    "Sum_Top512_Hon_Enc", SUMX(
        TOPN(
            512,
            FILTER(
                vw_powerbi_relatorio_aprovacao,
                vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
                vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
            ),
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO], DESC
        ),
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]
    ),
    "Sum_Hon_Enc_MovRange", CALCULATE(
        SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),
    "Count_Hon_Enc_MovRange", COUNTROWS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1) &&
            vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
        )
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-List | Out-File -FilePath "top512_results.txt" -Encoding UTF8

$conn.Close()
