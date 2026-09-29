$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

# Let's check how many jobs have A.PERCENTUAL > 0 vs NULL/0
$cmd = $conn.CreateCommand()
$cmd.CommandText = @"
SELECT 
    COUNT(*) as TotalJobs,
    SUM(CASE WHEN ISNULL(PERCENTUAL, 0) > 0 THEN 1 ELSE 0 END) as WithPerc,
    SUM(CASE WHEN ISNULL(PERCENTUAL, 0) = 0 THEN 1 ELSE 0 END) as WithoutPerc
FROM PROJECT_QBERT_JOBS WITH (NOLOCK)
WHERE JOB IS NOT NULL
"@
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "Total: $($r['TotalJobs']) | With Perc: $($r['WithPerc']) | Without Perc: $($r['WithoutPerc'])"
}
$r.Close()

$conn.Close()
