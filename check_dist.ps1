$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT 
    ISNULL(CAST(CctUnidadeFranqCom AS VARCHAR), 'NULL') AS UnidadeCom,
    ISNULL(CAST(CctUnidadeFranqOp AS VARCHAR), 'NULL') AS UnidadeOp,
    COUNT(*) as Qtd
FROM PROJECT_CP_CONTRATO WITH (NOLOCK)
GROUP BY CctUnidadeFranqCom, CctUnidadeFranqOp
ORDER BY Qtd DESC
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
