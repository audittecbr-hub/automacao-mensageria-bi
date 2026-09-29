$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$expr = [System.IO.File]::ReadAllText("matriz_perfect.dax", [System.Text.Encoding]::UTF8)

# Remove BOM if present
if ($expr.StartsWith([char]0xFEFF)) {
    $expr = $expr.Substring(1)
}

$query = "EVALUATE ROW(`"Test`", " + $expr + ")"
try {
    $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
    $rdr = $cmd.ExecuteReader()
    Write-Output "SUCCESS evaluating entire expression directly!"
    $rdr.Close()
} catch {
    [System.IO.File]::WriteAllText("full_dax_error.txt", $_.Exception.ToString(), [System.Text.Encoding]::UTF8)
    Write-Output "Saved full_dax_error.txt"
}
$conn.Close()
