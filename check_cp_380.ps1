$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT
    CAST(C.CctCodigo AS VARCHAR(50)) AS JOB,
    C.CctCodigo AS CODIGO,
    [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS PERC_HONORARIOS_JOB,
    C.CctDataCadastro AS DATA_CADASTRO,
    ISNULL(U.PERC_FRANQUEADO, [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C')) AS PERC_HONORARIOS_FRANQUEADO,
    ISNULL(C.CctUnidadeFranqCom, ISNULL(U.UNIDADE_ID, C.CctUnidadeFranqOp)) AS UNIDADE_ID,
    ISNULL(UCom.UniNome, ISNULL(U.UNIDADE_NOME, UOp.UniNome)) AS UNIDADE_NOME,
    U.UNIDADE_EMAIL AS UNIDADE_EMAIL,
    U.PARTICIPANTE_CPF AS CNPJ_UNIDADE,
    U.TIPO_FRANQUIA_CODIGO,
    U.TIPO_FRANQUIA_NOME,
    U.PARTICIPANTE_ID,
    U.PARTICIPANTE_RAZAO_SOCIAL,
    U.PARTICIPANTE_CPF,
    U.PARTICIPANTE_CONTATO_NOME,
    ISNULL(U.PERC_FRANQUEADO, [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C')) AS PERC_FRANQUEADO,
    'N' AS COBRANCA_GROSSUP,
    0 AS RETENCAO,
    CASE ISNULL(U.UNIRETEMIMPOSTO, 0) WHEN 1 THEN 'N' ELSE 'S' END AS UNIRETEMIMPOSTO
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN SMART_UNIDADES UCom WITH (NOLOCK) ON UCom.UniCodigo = C.CctUnidadeFranqCom
LEFT JOIN SMART_UNIDADES UOp WITH (NOLOCK) ON UOp.UniCodigo = C.CctUnidadeFranqOp
OUTER APPLY (
    SELECT TOP 1 *
    FROM vw_powerbi_participantes_unidades PU WITH (NOLOCK)
    WHERE PU.UNIDADE_ID = C.CctUnidadeFranqCom OR (C.CctUnidadeFranqCom IS NULL AND PU.PARTICIPANTE_ID = C.CctCliente)
    ORDER BY PU.ModAtivo DESC
) U
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
