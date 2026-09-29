$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = 'EVALUATE ROW("Html", [HTML_Detalhamento_Aprovados])'
$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetValue(0)
    [System.IO.File]::WriteAllText("dump_aprovados_fixed.html", $html, [System.Text.Encoding]::UTF8)
    Write-Output "Saved dump_aprovados_fixed.html, length: $($html.Length)"
}
$conn.Close()
