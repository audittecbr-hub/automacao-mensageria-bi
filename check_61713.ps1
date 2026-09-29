$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Output "--- Querying 61713 in vw_powerbi_job_repasse ---"
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM dbo.vw_powerbi_job_repasse WHERE JOB = '61713'"
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Output "=== Found 61713 ==="
    for ($i=0; $i -lt $r.FieldCount; $i++) {
        Write-Output ($r.GetName($i) + ': ' + $r.GetValue($i))
    }
}
if (!$r.HasRows) { Write-Output "Job 61713 NOT found in vw_powerbi_job_repasse!" }
$r.Close()

Write-Output "`n--- Searching 61713 in PROJECT_QBERT_JOBS ---"
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "SELECT * FROM PROJECT_QBERT_JOBS WHERE JOB LIKE '%61713%'"
$r2 = $cmd2.ExecuteReader()
while ($r2.Read()) {
    Write-Output "=== Found in PROJECT_QBERT_JOBS ==="
    for ($i=0; $i -lt $r2.FieldCount; $i++) {
        Write-Output ($r2.GetName($i) + ': ' + $r2.GetValue($i))
    }
}
$r2.Close()

$conn.Close()
