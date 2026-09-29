$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    C.CctCodigo,
    C.CctCliente,
    C.CctUnidadeFranqCom,
    C.CctUnidadeFranqOp,
    C.CctDataCadastro,
    UCom.UniCodigo as UnidadeId_Com,
    UCom.UniNome as UnidadeNome_Com,
    UOp.UniCodigo as UnidadeId_Op,
    UOp.UniNome as UnidadeNome_Op,
    PU.UNIDADE_ID as PU_UnidadeId,
    PU.UNIDADE_NOME as PU_UnidadeNome
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN SMART_UNIDADES UCom WITH (NOLOCK) ON UCom.UniCodigo = C.CctUnidadeFranqCom
LEFT JOIN SMART_UNIDADES UOp WITH (NOLOCK) ON UOp.UniCodigo = C.CctUnidadeFranqOp
OUTER APPLY (
    SELECT TOP 1 UNIDADE_ID, UNIDADE_NOME
    FROM vw_powerbi_participantes_unidades PU WITH (NOLOCK)
    WHERE PU.PARTICIPANTE_ID = C.CctCliente
) PU
WHERE C.CctCodigo IN (380, 679, 141, 343, 429, 428, 427, 426, 425, 423, 422, 421, 420, 419, 418, 417, 416, 415)
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
