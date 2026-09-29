$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    CAST(C.CctCodigo AS VARCHAR(50)) AS JOB,
    C.CctCodigo AS CODIGO,
    [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS PERC_HONORARIOS_JOB,
    C.CctDataCadastro AS DATA_CADASTRO,
    U.PERC_FRANQUEADO AS PERC_HONORARIOS_FRANQUEADO,
    U.UNIDADE_ID AS UNIDADE_ID,
    U.UNIDADE_NOME AS UNIDADE_NOME,
    U.UNIDADE_EMAIL AS UNIDADE_EMAIL,
    U.PARTICIPANTE_CPF AS CNPJ_UNIDADE,
    U.TIPO_FRANQUIA_CODIGO,
    U.TIPO_FRANQUIA_NOME,
    U.PARTICIPANTE_ID,
    U.PARTICIPANTE_RAZAO_SOCIAL,
    U.PARTICIPANTE_CPF,
    U.PARTICIPANTE_CONTATO_NOME,
    U.PERC_FRANQUEADO,
    'N' AS COBRANCA_GROSSUP,
    0 AS RETENCAO,
    CASE U.UNIRETEMIMPOSTO WHEN 1 THEN 'N' ELSE 'S' END AS UNIRETEMIMPOSTO
FROM PROJECT_CP_CONTRATO C (NOLOCK)
INNER JOIN vw_powerbi_participantes_unidades U 
    ON U.PARTICIPANTE_ID = C.CctCliente
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
