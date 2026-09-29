$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "
SELECT 
    s.session_id,
    s.login_name,
    s.host_name,
    s.program_name,
    s.client_interface_name,
    r.start_time,
    r.total_elapsed_time / 1000 AS elapsed_sec,
    r.cpu_time,
    r.reads
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
WHERE s.session_id IN (139, 146)
"
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "SPID: $($r['session_id']) | Host: $($r['host_name']) | User: $($r['login_name']) | Elapsed: $($r['elapsed_sec'])s | CPU: $($r['cpu_time']) | Reads: $($r['reads'])"
}
$r.Close()
$conn.Close()
