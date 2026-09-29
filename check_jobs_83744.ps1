$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 'PROJECT_QBERT_JOBS' as Tbl, JOB, CODIGO_CLIENTE, CODIGO_UNIDADE, DATA_CADASTRO
FROM PROJECT_QBERT_JOBS WITH (NOLOCK)
WHERE JOB IN ('83744', '83745', '83743', '2025/00007', '188/2')

SELECT 'PROJECT_CP_CONTRATO' as Tbl, CctCodigo, CctCliente, CctUnidadeFranqCom, CctUnidadeFranqOp, CctDataCadastro
FROM PROJECT_CP_CONTRATO WITH (NOLOCK)
WHERE CctCodigo IN (83744, 83745, 83743)
"@
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = $query
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$ds = New-Object System.Data.DataSet
$adapter.Fill($ds) | Out-Null
$conn.Close()
foreach ($dt in $ds.Tables) {
    $dt | Format-Table -AutoSize
}
