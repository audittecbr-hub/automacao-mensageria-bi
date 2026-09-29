$port = 52151
$connStr = "Provider=MSOLAP;Data Source=localhost:$port;Initial Catalog=;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
try {
    $conn.Open()
    $tmsl = Get-Content -Path "update_measure.tmsl" -Raw -Encoding UTF8
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = $tmsl
    $cmd.ExecuteNonQuery() | Out-Null
    Write-Host "TMSL executed successfully! Measure updated in memory."
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
