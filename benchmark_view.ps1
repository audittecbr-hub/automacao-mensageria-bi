$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 300
$cmd.CommandText = "SELECT COUNT(*) FROM dbo.vw_powerbi_job_repasse"
$cnt = $cmd.ExecuteScalar()
$sw.Stop()
Write-Host "Count: $cnt rows, elapsed: $($sw.ElapsedMilliseconds) ms"
$conn.Close()
