$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
try {
    $cmd.CommandText = "KILL 139;"
    $cmd.ExecuteNonQuery() | Out-Null
    Write-Host "Killed 139"
} catch {
    Write-Host "Could not kill 139: $($_.Exception.Message)"
}
try {
    $cmd.CommandText = "KILL 146;"
    $cmd.ExecuteNonQuery() | Out-Null
    Write-Host "Killed 146"
} catch {
    Write-Host "Could not kill 146: $($_.Exception.Message)"
}
$conn.Close()
