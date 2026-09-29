$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "
        SELECT TOP 5
            CAST(JOB AS VARCHAR(50)) AS numero_contrato,
            dbo.Func_JOB_CALCULAR_HONORARIO(JOB, 'C') AS honorario
        FROM PROJECT_QBERT_JOBS WITH (NOLOCK)
        WHERE JOB IS NOT NULL;
    "
    $r = $cmd.ExecuteReader()
    Write-Output "Results with dbo.Func_JOB_CALCULAR_HONORARIO(JOB, 'C'):"
    while ($r.Read()) {
        Write-Output ($r['numero_contrato'].ToString() + " -> " + $r['honorario'].ToString())
    }
    $r.Close()
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
} finally {
    $conn.Close()
}
