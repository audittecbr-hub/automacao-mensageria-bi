$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    Write-Output "Connected successfully to SQL Server!"
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "
        SELECT 
            p.name AS ParameterName,
            t.name AS TypeName,
            p.max_length,
            p.parameter_id
        FROM sys.parameters p
        JOIN sys.objects o ON p.object_id = o.object_id
        JOIN sys.types t ON p.user_type_id = t.user_type_id
        WHERE o.name = 'Func_JOB_CALCULAR_HONORARIO'
        ORDER BY p.parameter_id;
    "
    $r = $cmd.ExecuteReader()
    while ($r.Read()) {
        Write-Output ("Param ID: " + $r['parameter_id'] + " | Name: " + $r['ParameterName'] + " | Type: " + $r['TypeName'])
    }
    $r.Close()

    # Also let's get the function definition
    $cmd2 = $conn.CreateCommand()
    $cmd2.CommandText = "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.Func_JOB_CALCULAR_HONORARIO')) AS def;"
    $def = $cmd2.ExecuteScalar()
    Write-Output "`nFunction Definition:"
    Write-Output $def
} catch {
    Write-Output ("Error: " + $_.Exception.Message)
} finally {
    $conn.Close()
}
