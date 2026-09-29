$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 300
$cmd.CommandText = "SELECT TOP 5000 * FROM dbo.vw_powerbi_job_repasse"
$reader = $cmd.ExecuteReader()
$cnt = 0
while ($reader.Read()) {
    $cnt++
}
$reader.Close()
$sw.Stop()
Write-Host "Read $cnt rows, elapsed: $($sw.ElapsedMilliseconds) ms"
$conn.Close()
