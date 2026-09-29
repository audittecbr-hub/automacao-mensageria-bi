$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME LIKE '%PARTICIPANTES%';
SELECT TOP 5 * FROM SMART_UNIDADES WHERE UniNome LIKE '%ACS%';
"@
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
    $ds = New-Object System.Data.DataSet
    $adapter.Fill($ds) | Out-Null
    foreach ($table in $ds.Tables) {
        $table | Format-Table -AutoSize | Out-String | Write-Host
    }
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
