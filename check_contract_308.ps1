$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    C.*,
    UCom.UniNome as NomeUniCom,
    UOp.UniNome as NomeUniOp
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN SMART_UNIDADES UCom WITH (NOLOCK) ON UCom.UniCodigo = C.CctUnidadeFranqCom
LEFT JOIN SMART_UNIDADES UOp WITH (NOLOCK) ON UOp.UniCodigo = C.CctUnidadeFranqOp
WHERE C.CctCodigo = 308
"@
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = $query
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()
$dt | Format-List
