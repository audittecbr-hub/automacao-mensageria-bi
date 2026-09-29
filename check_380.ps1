$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    C.CctCodigo, 
    C.CctCliente, 
    C.CctUnidadeFranqCom, 
    C.CctUnidadeFranqOp, 
    C.CctDataCadastro, 
    UCom.UniNome as NomeUnidadeCom,
    UOp.UniNome as NomeUnidadeOp,
    PU.UNIDADE_ID,
    PU.UNIDADE_NOME,
    PU.PERC_FRANQUEADO,
    [dbo].[Func_JOB_CALCULAR_HONORARIO](C.CctCodigo, 'C') as HonorarioCalc
FROM PROJECT_CP_CONTRATO C
LEFT JOIN SMART_UNIDADES UCom ON UCom.UniCodigo = C.CctUnidadeFranqCom
LEFT JOIN SMART_UNIDADES UOp ON UOp.UniCodigo = C.CctUnidadeFranqOp
OUTER APPLY (
    SELECT TOP 1 UNIDADE_ID, UNIDADE_NOME, PERC_FRANQUEADO
    FROM vw_participantes_unidades PU
    WHERE PU.PARTICIPANTE_ID = C.CctCliente
) PU
WHERE C.CctCodigo IN (380, 679, 141, 343)
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
