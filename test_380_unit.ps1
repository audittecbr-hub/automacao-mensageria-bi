$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    C.CctCodigo,
    C.CctCliente,
    C.CctUnidadeFranqCom,
    C.CctUnidadeFranqOp,
    C.CctDataCadastro,
    UCom.UniCodigo,
    UCom.UniNome,
    PU_Com.UNIDADE_ID as PU_Com_UnidadeId,
    PU_Com.UNIDADE_NOME as PU_Com_UnidadeNome,
    PU_Cli.UNIDADE_ID as PU_Cli_UnidadeId,
    PU_Cli.UNIDADE_NOME as PU_Cli_UnidadeNome
FROM PROJECT_CP_CONTRATO C
LEFT JOIN SMART_UNIDADES UCom ON UCom.UniCodigo = C.CctUnidadeFranqCom
LEFT JOIN vw_powerbi_participantes_unidades PU_Com ON PU_Com.UNIDADE_ID = C.CctUnidadeFranqCom
LEFT JOIN vw_powerbi_participantes_unidades PU_Cli ON PU_Cli.PARTICIPANTE_ID = C.CctCliente
WHERE C.CctCodigo = 380
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
