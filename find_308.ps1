$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 'SMART_PARTICIPANTES' as Tbl, ParCodigo, ParRazao, ParCpfCnpj, ParUnidade, ParResponsavel, ParVendedor
FROM SMART_PARTICIPANTES WITH (NOLOCK)
WHERE ParCodigo = 32070 OR ParCpfCnpj LIKE '%28342882%'

SELECT 'vw_powerbi_participantes_unidades' as Tbl, *
FROM vw_powerbi_participantes_unidades WITH (NOLOCK)
WHERE PARTICIPANTE_ID = 32070 OR PARTICIPANTE_CPF LIKE '%28342882%' OR CNPJ_UNIDADE LIKE '%28342882%'

SELECT 'SMART_CLIENTES' as Tbl, *
FROM SMART_CLIENTES WITH (NOLOCK)
WHERE CliCodigo = 32070 OR CliCNPJCPF LIKE '%28342882%'

SELECT 'PROJECT_QBERT_JOBS' as Tbl, JOB, CODIGO_CLIENTE, CODIGO_UNIDADE, UNIDADE
FROM PROJECT_QBERT_JOBS WITH (NOLOCK)
WHERE CODIGO_CLIENTE = 32070 OR CNPJ_CPF LIKE '%28342882%'
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
