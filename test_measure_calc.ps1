$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Check measure in ADOMD query
$q = 'EVALUATE ROW("ExprVal", CALCULATE([Honorários aprovados], vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = "VALUATION M&A"))'
$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    Write-Output "Valuation M&A evaluated via [Honorários aprovados]: $($rdr.GetValue(0))"
}
$rdr.Close()
$conn.Close()
