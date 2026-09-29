$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$expr = [System.IO.File]::ReadAllText("matriz_perfect.dax", [System.Text.Encoding]::UTF8)
if ($expr.StartsWith([char]0xFEFF)) {
    $expr = $expr.Substring(1)
}

# Evaluate Mockup_Honorarios_Matriz
$q = 'EVALUATE ROW("Html", ' + $expr + ')'
$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetValue(0)
    [System.IO.File]::WriteAllText("dump_fresh_direct_eval.html", $html, [System.Text.Encoding]::UTF8)
    Write-Output "Saved dump_fresh_direct_eval.html"
}
$conn.Close()
