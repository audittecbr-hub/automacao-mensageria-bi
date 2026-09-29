$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = @"
SELECT TOP 10 
    A.JOB, 
    A.PERCENTUAL,
    [dbo].[Func_JOB_CALCULAR_HONORARIO](A.JOB, 'O') as FuncHon
FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
WHERE A.JOB IS NOT NULL AND ISNULL(A.PERCENTUAL, 0) > 0
"@
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "Job: $($r['JOB']) | Perc: $($r['PERCENTUAL']) | Func: $($r['FuncHon'])"
}
$r.Close()

$conn.Close()
