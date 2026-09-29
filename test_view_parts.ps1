$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Output "--- Testing Part 1 (PROJECT_QBERT_JOBS) ---"
try {
    $cmd1 = $conn.CreateCommand()
    $cmd1.CommandTimeout = 30
    $cmd1.CommandText = "
    SELECT TOP 10
        A.JOB,
        A.CODIGO,
        A.PERCENTUAL AS PERC_HONORARIOS_JOB,
        A.DATA_CADASTRO,
        U.PERC_FRANQUEADO AS PERC_HONORARIOS_FRANQUEADO,
        U.UNIDADE_ID AS UNIDADE_ID,
        U.UNIDADE_NOME,
        U.UNIDADE_EMAIL AS UNIDADE_EMAIL,
        U.PARTICIPANTE_CPF AS CNPJ_UNIDADE,
        U.TIPO_FRANQUIA_CODIGO,
        U.TIPO_FRANQUIA_NOME,
        U.PARTICIPANTE_ID,
        (SELECT TOP 1 P.ParRazao FROM SMART_PARTICIPANTES P WITH (NOLOCK) WHERE P.ParCodigo = U.PARTICIPANTE_ID AND P.ParTipo = 1) AS PARTICIPANTE_CLIENTE,
        (SELECT TOP 1 P.ParRazao FROM SMART_PARTICIPANTES P WITH (NOLOCK) WHERE P.ParCodigo = U.PARTICIPANTE_ID AND P.ParTipo = 3) AS PARTICIPANTE_FRANQUEADO,
        U.PARTICIPANTE_RAZAO_SOCIAL,
        U.PARTICIPANTE_CPF,
        U.PARTICIPANTE_CONTATO_NOME,
        U.PERC_FRANQUEADO,
        RD.SURDNOME AS REDE_DISTRIBUICAO,
        TF.SUTFNOME AS REDE_DISTRIBUICAO_OLD,
        CASE WHEN A.COBRANCA_GROSSUP = 1 THEN 'N' ELSE 'S' END AS COBRANCA_GROSSUP,
        CASE WHEN ISNULL(U.UNIRETEMIMPOSTO, 0) = 1 THEN CAST(0.00 AS NUMERIC(5,2)) WHEN A.COBRANCA_GROSSUP = 1 AND A.DATA_CADASTRO > '20260301' THEN CAST(19.53 AS NUMERIC(5,2)) ELSE CAST(0.00 AS NUMERIC(5,2)) END AS RETENCAO,
        CASE WHEN U.UNIRETEMIMPOSTO = 1 THEN 'N' ELSE 'S' END AS UNIRETEMIMPOSTO
    FROM vw_powerbi_participantes_unidades U WITH (NOLOCK)
    INNER JOIN PROJECT_QBERT_JOBS AS A WITH (NOLOCK) ON U.PARTICIPANTE_ID = A.CODIGO_CLIENTE
    LEFT JOIN SMART_UNIDADES_REDE_DISTRIBUICAO RD ON U.ModRedeDistribuicao = RD.SurdCodigo
    LEFT JOIN SMART_UNIDADES_TIPO_FRANQUIA TF ON U.ModTipoFranquia = TF.SutfCodigo
    "
    $r1 = $cmd1.ExecuteReader()
    Write-Output "Part 1 executed successfully!"
    $r1.Close()
} catch {
    Write-Output ("Part 1 Error: " + $_.Exception.Message)
}

Write-Output "`n--- Testing Part 2 (PROJECT_CP_CONTRATO) ---"
try {
    $cmd2 = $conn.CreateCommand()
    $cmd2.CommandTimeout = 30
    $cmd2.CommandText = "
    SELECT TOP 10
        CAST(C.CctCodigo AS VARCHAR(50)) AS JOB,
        C.CctCodigo AS CODIGO,
        [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS PERC_HONORARIOS_JOB,
        C.CctDataCadastro AS DATA_CADASTRO,
        [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS PERC_HONORARIOS_FRANQUEADO,
        ISNULL(C.CctUnidadeFranqCom, ISNULL(C.CctUnidadeFranqOp, 2153)) AS UNIDADE_ID,
        ISNULL(UCom.UniNome, 'STUDIO CONTABILIDADE LTDA - PILOTO') AS UNIDADE_NOME,
        UCom.UniEmail AS UNIDADE_EMAIL,
        '' AS CNPJ_UNIDADE,
        0 AS TIPO_FRANQUIA_CODIGO,
        '' AS TIPO_FRANQUIA_NOME,
        C.CctCliente AS PARTICIPANTE_ID,
        (SELECT TOP 1 P.ParRazao FROM SMART_PARTICIPANTES P WITH (NOLOCK) WHERE P.ParCodigo = C.CctCliente AND P.ParTipo = 1) AS PARTICIPANTE_CLIENTE,
        (SELECT TOP 1 P.ParRazao FROM SMART_PARTICIPANTES P WITH (NOLOCK) WHERE P.ParCodigo = C.CctCliente AND P.ParTipo = 3) AS PARTICIPANTE_FRANQUEADO,
        '' AS PARTICIPANTE_RAZAO_SOCIAL,
        '' AS PARTICIPANTE_CPF,
        '' AS PARTICIPANTE_CONTATO_NOME,
        [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS PERC_FRANQUEADO,
        CAST('' AS VARCHAR(250)) AS REDE_DISTRIBUICAO,
        CAST('' AS VARCHAR(250)) AS REDE_DISTRIBUICAO_OLD,
        'N' AS COBRANCA_GROSSUP,
        CAST(0.00 AS NUMERIC(5,2)) AS RETENCAO,
        CASE WHEN ISNULL(UCom.UniRetemImposto, 0) = 1 THEN 'N' ELSE 'S' END AS UNIRETEMIMPOSTO
    FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
    LEFT JOIN SMART_UNIDADES UCom WITH (NOLOCK) ON UCom.UniCodigo = ISNULL(C.CctUnidadeFranqCom, ISNULL(C.CctUnidadeFranqOp, 2153))
    WHERE C.CctCodigo IS NOT NULL
    "
    $r2 = $cmd2.ExecuteReader()
    Write-Output "Part 2 executed successfully!"
    $r2.Close()
} catch {
    Write-Output ("Part 2 Error: " + $_.Exception.Message)
}

$conn.Close()
