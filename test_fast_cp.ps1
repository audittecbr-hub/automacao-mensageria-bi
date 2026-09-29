$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
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
    '' AS PARTICIPANTE_RAZAO_SOCIAL,
    '' AS PARTICIPANTE_CPF,
    '' AS PARTICIPANTE_CONTATO_NOME,
    [dbo].[Func_JOB_CALCULAR_HONORARIO](CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS PERC_FRANQUEADO,
    'N' AS COBRANCA_GROSSUP,
    0 AS RETENCAO,
    CASE ISNULL(UCom.UniRetemImposto, 0) WHEN 1 THEN 'N' ELSE 'S' END AS UNIRETEMIMPOSTO
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN SMART_UNIDADES UCom WITH (NOLOCK) ON UCom.UniCodigo = ISNULL(C.CctUnidadeFranqCom, ISNULL(C.CctUnidadeFranqOp, 2153))
WHERE C.CctCodigo IS NOT NULL
"@
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = $query
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$sw.Stop()
$conn.Close()
Write-Host "Fetched $($dt.Rows.Count) rows in $($sw.ElapsedMilliseconds) ms!"
$dt | Where-Object { $_.JOB -in '308', '380', '141', '343' } | Format-Table -AutoSize
