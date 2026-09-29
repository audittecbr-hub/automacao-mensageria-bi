$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
SUMMARIZE(
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)
    ),
    vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO],
    "SumTrib", [Honorários aprovados]
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
while ($rdr.Read()) {
    $v = $rdr.GetValue(1)
    if ($v -gt 0) {
        Write-Output "Tributo: '$($rdr.GetValue(0))' | Sum: $v"
    }
}
$rdr.Close()
$conn.Close()
