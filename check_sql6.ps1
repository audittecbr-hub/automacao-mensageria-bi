$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT * FROM SMART_UNIDADES_MODELOS_PERC_PROD WITH (NOLOCK) WHERE SppModCodigo IN (11147, 11602);
SELECT * FROM SMART_UNIDADES_MODELOS_PERC_FIXO WITH (NOLOCK) WHERE SpfModCodigo IN (11147, 11602);
SELECT UniCodigo, UniNome FROM SMART_UNIDADES WHERE UniCodigo IN (2153, 2613);
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
