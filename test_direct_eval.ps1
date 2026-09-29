$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$expr = [System.IO.File]::ReadAllText("matriz_with_apneg.dax", [System.Text.Encoding]::UTF8)

# Let's test evaluating the expression directly in an EVALUATE query:
$query = "EVALUATE ROW(`"Test`", " + $expr + ")"
try {
    $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
    $rdr = $cmd.ExecuteReader()
    Write-Output "SUCCESS evaluating entire expression directly!"
    $rdr.Close()
} catch {
    Write-Output "DIRECT EVAL ERROR: $($_.Exception.Message)"
}
$conn.Close()
