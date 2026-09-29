$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 10
$cmd.CommandText = "
SELECT 
    r.session_id,
    r.blocking_session_id,
    r.wait_type,
    r.wait_time,
    r.command,
    s.login_name,
    s.program_name,
    t.text
FROM sys.dm_exec_requests r
JOIN sys.dm_exec_sessions s ON r.session_id = s.session_id
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id <> @@SPID
"
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "SPID: $($r['session_id']) | BlockedBy: $($r['blocking_session_id']) | Wait: $($r['wait_type']) ($($r['wait_time'])ms) | Program: $($r['program_name'])"
    Write-Host "SQL: $($r['text'].Substring(0, [Math]::Min(100, $r['text'].Length)))"
}
$r.Close()
$conn.Close()
