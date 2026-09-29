$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
ROW(
    "Total_Aprov_Negoc", CALCULATE(
        SUMX(
            vw_powerbi_relatorio_aprovacao,
            COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] +
            vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
        ),
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO" &&
            vw_powerbi_relatorio_aprovacao[AREA_ATUAL] IN {"AJUÍZAMENTO", "COMPENSAÇÃO", "ENTREGA", "IMPLANTAÇÃO", "RETIFICAÇÃO"}
        )
    ),
    "Cnt", CALCULATE(
        COUNTROWS(vw_powerbi_relatorio_aprovacao),
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR] = "NEGOCIAÇÃO" &&
            vw_powerbi_relatorio_aprovacao[AREA_ATUAL] IN {"AJUÍZAMENTO", "COMPENSAÇÃO", "ENTREGA", "IMPLANTAÇÃO", "RETIFICAÇÃO"}
        )
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$dt | Format-List | Out-File -FilePath "aprov_negoc_test2.txt" -Encoding UTF8
Write-Output "Saved aprov_negoc_test2.txt"
$conn.Close()
