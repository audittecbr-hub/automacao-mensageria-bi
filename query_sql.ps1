$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Host "=== VW_POWERBI_JOB_REPASSE PARA 85206 e UNIDADE 1960 ==="
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT JOB, UNIDADE_ID, UNIDADE_NOME, PERC_HONORARIOS_JOB, PERC_HONORARIOS_FRANQUEADO, REDE_DISTRIBUICAO, DATA_CADASTRO FROM dbo.vw_powerbi_job_repasse WHERE JOB = '85206' OR UNIDADE_ID = 1960"
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-Table -AutoSize

Write-Host "=== FUNCTION / PROCEDURE QUE BUSCA HONORARIO NO SQL ==="
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "SELECT ROUTINE_NAME, ROUTINE_TYPE FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME LIKE '%honorario%' OR ROUTINE_NAME LIKE '%repasse%'"
$adapter2 = New-Object System.Data.SqlClient.SqlDataAdapter($cmd2)
$dt2 = New-Object System.Data.DataTable
$adapter2.Fill($dt2) | Out-Null
$dt2 | Format-Table -AutoSize

Write-Host "=== DEFINIÇÃO DA VIEW vw_powerbi_job_repasse ==="
$cmd3 = $conn.CreateCommand()
$cmd3.CommandText = "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_powerbi_job_repasse'))"
$viewDef = $cmd3.ExecuteScalar()
Write-Output $viewDef

$conn.Close()
