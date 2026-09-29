$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
FILTER(
    vw_powerbi_relatorio_aprovacao,
    vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO] = "VALUATION M&A"
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
while ($rdr.Read()) {
    $vals = @()
    for ($i = 0; $i -lt $rdr.FieldCount; $i++) {
        $n = $rdr.GetName($i)
        $v = $rdr.GetValue($i)
        if ($n -like "*HONORARIO*" -or $n -like "*TOTAL*" -or $n -like "*DATA*" -or $n -eq "[JOB]") {
            $vals += "${n}: ${v}"
        }
    }
    Write-Output ($vals -join " | ")
}
$rdr.Close()
$conn.Close()
