$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Host "=== PROJECT_QBERT_JOBS PARA 85206 ==="
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM PROJECT_QBERT_JOBS WHERE JOB = '85206'"
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-List

Write-Host "=== TESTE DAS FUNCTIONS PARA 85206 ==="
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = @"
SELECT 
    [dbo].[Func_JOB_CALCULAR_HONORARIO]('85206', 'C') AS Func_Calc_C,
    [dbo].[Func_JOB_CALCULAR_HONORARIO]('85206', 'F') AS Func_Calc_F,
    [dbo].[Func_Job_Calcula_Honorarios]('85206') AS Func_Job_Calc,
    [dbo].[Func_Job_Honorarios]('85206') AS Func_Job_Hon
"@
$adapter2 = New-Object System.Data.SqlClient.SqlDataAdapter($cmd2)
$dt2 = New-Object System.Data.DataTable
$adapter2.Fill($dt2) | Out-Null
$dt2 | Format-Table -AutoSize

Write-Host "=== DEFINIÇÃO DE Func_JOB_CALCULAR_HONORARIO ==="
$cmd3 = $conn.CreateCommand()
$cmd3.CommandText = "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.Func_JOB_CALCULAR_HONORARIO'))"
Write-Output $cmd3.ExecuteScalar()

Write-Host "=== DEFINIÇÃO DE Func_Job_Calcula_Honorarios ==="
$cmd4 = $conn.CreateCommand()
$cmd4.CommandText = "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.Func_Job_Calcula_Honorarios'))"
Write-Output $cmd4.ExecuteScalar()

$conn.Close()
