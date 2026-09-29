$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 60
$cmd.CommandText = "
SELECT COUNT(*) AS TotalJobs,
       SUM(CASE WHEN A.PERCENTUAL IS NULL OR A.PERCENTUAL = 0 THEN 1 ELSE 0 END) AS NullOrZeroPerc
FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
WHERE A.JOB IS NOT NULL
"
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "Total Jobs: $($r['TotalJobs']) | Null or Zero Perc: $($r['NullOrZeroPerc'])"
}
$r.Close()
$conn.Close()
