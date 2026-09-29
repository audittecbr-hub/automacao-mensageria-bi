$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$sql = @"
SELECT 
    CAST(CctCodigo AS VARCHAR(50)) AS numero_contrato,
    dbo.Func_JOB_CALCULAR_HONORARIO(CAST(CctCodigo AS VARCHAR(10)), 'C') AS honorario
FROM PROJECT_CP_CONTRATO WITH (NOLOCK)
WHERE CctCodigo IS NOT NULL
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
