$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$sql = @"
SELECT TOP 1000
    A.JOB,
    H.Honorario
FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
CROSS APPLY (
    SELECT CAST(ISNULL([dbo].[Func_JOB_CALCULAR_HONORARIO](A.JOB, 'O'), A.PERCENTUAL) AS FLOAT) AS Honorario
) H
WHERE A.JOB IS NOT NULL
"@

$sw = [System.Diagnostics.Stopwatch]::StartNew()
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 60
$cmd.CommandText = $sql
$reader = $cmd.ExecuteReader()
$cnt = 0
while ($reader.Read()) {
    $cnt++
}
$reader.Close()
$sw.Stop()
Write-Host "Read $cnt rows in $($sw.ElapsedMilliseconds) ms!"

$conn.Close()
