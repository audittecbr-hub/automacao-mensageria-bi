$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Host "=== TESTE FUNC_JOB_CALCULAR_HONORARIO COM TIPOCONTRATO 'O' vs 'C' ==="
$cmd = $conn.CreateCommand()
$cmd.CommandText = @"
SELECT 
    '85206' AS JOB,
    [dbo].[Func_JOB_CALCULAR_HONORARIO]('85206', 'O') AS Hon_O,
    [dbo].[Func_JOB_CALCULAR_HONORARIO]('85206', 'C') AS Hon_C,
    [dbo].[Func_JOB_CALCULAR_HONORARIO]('85206', 'F') AS Hon_F
"@
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-Table -AutoSize

Write-Host "=== REGISTROS DE 85206 EM PROJECT_QBERT_JOBS ==="
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "SELECT JOB, CODIGO_UNIDADE, PERCENTUAL, PERCENTUAL_FRANQUEADO, MODELO_NEGOCIO, DATA_RECEBIMENTO, DATA_CADASTRO, COBRANCA_GROSSUP FROM PROJECT_QBERT_JOBS WHERE JOB = '85206'"
$adapter2 = New-Object System.Data.SqlClient.SqlDataAdapter($cmd2)
$dt2 = New-Object System.Data.DataTable
$adapter2.Fill($dt2) | Out-Null
$dt2 | Format-List

Write-Host "=== REGISTROS DA UNIDADE 1960 EM SMART_UNIDADES_MODELOS e SMART_UNIDADES_MODELOS_PERC_FIXO ==="
$cmd3 = $conn.CreateCommand()
$cmd3.CommandText = @"
SELECT 
    M.ModCodigo,
    M.ModUnidade,
    M.ModModelo,
    M.ModTipoFranquia,
    M.ModRedeDistribuicao,
    M.ModData,
    M.ModDataTermino,
    M.ModDataInativo,
    M.ModAtivo,
    F.SpfCodigo,
    F.SpfPerc,
    F.SpfCadData
FROM SMART_UNIDADES_MODELOS M
LEFT JOIN SMART_UNIDADES_MODELOS_PERC_FIXO F ON F.SpfModCodigo = M.ModCodigo
WHERE M.ModUnidade = 1960
"@
$adapter3 = New-Object System.Data.SqlClient.SqlDataAdapter($cmd3)
$dt3 = New-Object System.Data.DataTable
$adapter3.Fill($dt3) | Out-Null
$dt3 | Format-Table -AutoSize

Write-Host "=== VW_PARTICIPANTES_UNIDADES PARA 1960 ==="
$cmd4 = $conn.CreateCommand()
$cmd4.CommandText = "SELECT * FROM vw_participantes_unidades WHERE UNIDADE_ID = 1960"
$adapter4 = New-Object System.Data.SqlClient.SqlDataAdapter($cmd4)
$dt4 = New-Object System.Data.DataTable
$adapter4.Fill($dt4) | Out-Null
$dt4 | Format-Table -AutoSize

$conn.Close()
