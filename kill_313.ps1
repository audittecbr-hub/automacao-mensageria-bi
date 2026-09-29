$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "KILL 313"
try {
    $cmd.ExecuteNonQuery() | Out-Null
    Write-Host "Killed 313 successfully"
} catch {
    Write-Host $_.Exception.Message
}
$conn.Close()
