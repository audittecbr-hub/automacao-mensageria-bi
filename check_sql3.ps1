$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT PTC.* FROM PROJECT_TIPOS_CONTRATOS PTC WITH (NOLOCK) WHERE PTC.PtcCodigo = 4;
SELECT * FROM SMART_UNIDADES_MODELOS_PERC_PROD WITH (NOLOCK) WHERE SppModCodigo = 10405;
SELECT * FROM SMART_UNIDADES_MODELOS_PERC_FIXO WITH (NOLOCK) WHERE SpfModCodigo = 10405;
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
