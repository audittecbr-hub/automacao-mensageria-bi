$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT TOP 1 * FROM SMART_UNIDADES;
SELECT TOP 1 * FROM VW_POWERBI_PARTICIPANTES_UNIDADES;
"@
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
    $ds = New-Object System.Data.DataSet
    $adapter.Fill($ds) | Out-Null
    foreach ($table in $ds.Tables) {
        $table.Columns | Select-Object ColumnName, DataType | Format-Table -AutoSize | Out-String | Write-Host
    }
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
