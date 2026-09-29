$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    Write-Output "Testing SELECT TOP 100 * FROM dbo.vw_powerbi_job_repasse..."
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "SELECT COUNT(*) FROM dbo.vw_powerbi_job_repasse"
    $count = $cmd.ExecuteScalar()
    Write-Output "Total rows: $count"

    Write-Output "Testing full read..."
    $cmd2 = $conn.CreateCommand()
    $cmd2.CommandText = "SELECT * FROM dbo.vw_powerbi_job_repasse"
    $r = $cmd2.ExecuteReader()
    $readCount = 0
    while ($r.Read()) {
        $readCount++
    }
    $r.Close()
    Write-Output "Read $readCount rows successfully!"
} catch {
    Write-Output ("Error: " + $_.Exception.ToString())
} finally {
    $conn.Close()
}
