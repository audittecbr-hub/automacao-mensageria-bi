$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT 'QBERT' as origem, CAST(JOB AS VARCHAR(50)) AS numero_contrato, dbo.Func_JOB_CALCULAR_HONORARIO(JOB, 'O') AS honorario FROM PROJECT_QBERT_JOBS WHERE JOB = '380'
UNION ALL
SELECT 'CONTRATO' as origem, CAST(CctCodigo AS VARCHAR(50)) AS numero_contrato, dbo.Func_JOB_CALCULAR_HONORARIO(CctCodigo, 'C') AS honorario FROM PROJECT_CP_CONTRATO WHERE CctCodigo = 380
"@
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    $adapter.Fill($dt) | Out-Null
    $dt | Format-Table -AutoSize | Out-String | Write-Host
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
