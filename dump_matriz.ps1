$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = 'EVALUATE ROW("Html", [Mockup_Honorarios_Matriz])'
$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetValue(0)
    [System.IO.File]::WriteAllText("dump_matriz_updated.html", $html, [System.Text.Encoding]::UTF8)
    Write-Output "Saved dump_matriz_updated.html, length: $($html.Length)"
}
$conn.Close()
