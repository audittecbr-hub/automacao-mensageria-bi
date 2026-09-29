$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
ROW(
    "CountComRT",
    COUNTROWS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            [Honorários aprovados] > 0
        )
    ),
    "SumComRT",
    SUMX(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            [Honorários aprovados] > 0
        ),
        [Honorários aprovados]
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    Write-Output "Count: $($rdr.GetValue(0)) | Sum: $($rdr.GetValue(1))"
}
$rdr.Close()
$conn.Close()
