$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT 
    M.ModCodigo,
    M.ModUnidade,
    M.ModTipoContrato,
    M.ModModelo,
    M.ModData,
    M.ModDataTermino,
    M.ModDataInativo
FROM SMART_UNIDADES_MODELOS M WITH (NOLOCK)
WHERE M.ModUnidade = 2153
"@
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    $adapter.Fill($dt) | Out-Null
    $dt | Format-Table -AutoSize | Out-String | Write-Host
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
