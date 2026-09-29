$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Host "=== PROJECT_QBERT_JOBS: COLUNAS DE 85206 ==="
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT JOB, PERCENTUAL, CODIGO_UNIDADE, DATA_RECEBIMENTO, DATA_CADASTRO FROM PROJECT_QBERT_JOBS WHERE JOB = '85206'"
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-Table -AutoSize

Write-Host "=== COMPARATIVO: A.PERCENTUAL vs Func_JOB_CALCULAR_HONORARIO(JOB, 'O') ==="
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = @"
SELECT 
    A.JOB,
    A.CODIGO_UNIDADE,
    U.UniNome,
    A.PERCENTUAL AS QBERT_STATIC_PERCENTUAL,
    [dbo].[Func_JOB_CALCULAR_HONORARIO](A.JOB, 'O') AS DYNAMIC_FUNC_PERCENTUAL
FROM PROJECT_QBERT_JOBS A
LEFT JOIN SMART_UNIDADES U ON U.UniCodigo = A.CODIGO_UNIDADE
WHERE A.CODIGO_UNIDADE = 1960
"@
$adapter2 = New-Object System.Data.SqlClient.SqlDataAdapter($cmd2)
$dt2 = New-Object System.Data.DataTable
$adapter2.Fill($dt2) | Out-Null
$dt2 | Format-Table -AutoSize

$conn.Close()
