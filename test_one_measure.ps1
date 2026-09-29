$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = 'EVALUATE ROW("Test", LEN([HTML_Detalhamento_Encontrados]))'
$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
try {
    $rdr = $cmd.ExecuteReader()
    if ($rdr.Read()) {
        Write-Output "SUCCESS: $($rdr.GetValue(0))"
    }
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}
$conn.Close()
