$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$raw = [System.IO.File]::ReadAllText("matriz_perfect.dax", [System.Text.Encoding]::UTF8)
$vars = $raw -split '(?m)^VAR '

Write-Output "Total VARs: $($vars.Count)"

$accum = ""
for ($i = 1; $i -lt $vars.Count; $i++) {
    $v = "VAR " + $vars[$i]
    $eqIdx = $vars[$i].IndexOf('=')
    if ($eqIdx -lt 0) { continue }
    $varName = $vars[$i].Substring(0, $eqIdx).Trim()
    
    # Try as scalar first, then as table
    $testScalar = $accum + "`n" + $v + "`nRETURN `"OK`""
    $q = "EVALUATE ROW(`"Test`", " + $testScalar + ")"
    try {
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
        $rdr = $cmd.ExecuteReader()
        $rdr.Close()
        Write-Output "VAR ${i} ($varName) OK"
        $accum += "`n" + $v
    } catch {
        Write-Output "SYNTAX ERROR AT VAR ${i} ($varName)"
        Write-Output "Error: $($_.Exception.Message)"
        break
    }
}

$conn.Close()
