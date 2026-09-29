$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    C.CctCodigo,
    C.CctCliente,
    C.CctDataCadastro,
    C.CctLogUserCad,
    C.CctUnidadeFranqCom,
    C.CctUnidadeFranqOp,
    C.CctModeloNegocio,
    P.ParRazao,
    P.ParCNPJ,
    P.ParUnidade
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN SMART_PARTICIPANTES P WITH (NOLOCK) ON P.ParCodigo = C.CctCliente
WHERE C.CctCodigo = 308 OR C.CctUnidadeFranqCom IS NULL OR C.CctUnidadeFranqCom = 0
ORDER BY C.CctCodigo DESC
"@
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = $query
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()
$dt | Select-Object -First 20 | Format-Table -AutoSize
