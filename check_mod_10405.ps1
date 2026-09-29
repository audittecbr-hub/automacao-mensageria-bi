$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT * FROM SMART_UNIDADES_MODELOS WHERE ModCodigo = 10405
SELECT * FROM SMART_UNIDADES_MODELOS_PERC_PROD WHERE SppModCodigo = 10405
SELECT * FROM SMART_UNIDADES_MODELOS_PERC_FIXO WHERE SpfModCodigo = 10405
SELECT * FROM vw_participantes_unidades WHERE UNIDADE_ID = 2153
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
