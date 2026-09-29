$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT ModCodigo, UNIDADE_ID, UNIDADE_NOME, PERC_FRANQUEADO, TIPO_CONTRATO_CODIGO, TIPO_CONTRATO_NOME
FROM vw_participantes_unidades 
WHERE UNIDADE_ID = 2153
"@
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = $query
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()
$dt | Format-Table -AutoSize
