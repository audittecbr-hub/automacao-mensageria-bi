$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT TOP 1 * FROM SMART_PARTICIPANTES WHERE ParCodigo = 32070
SELECT TOP 1 * FROM SMART_CLIENTES WHERE CliCodigo = 32070
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
    $dt | Format-List
}
