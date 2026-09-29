$connStr = "Provider=MSOLAP;Data Source=localhost:52421;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
try {
    $conn.Open()
    Write-Host "Connected to 52421 successfully!"
    $schema = $conn.GetOleDbSchemaTable([System.Data.OleDb.OleDbSchemaGuid]::Catalogs, $null)
    foreach ($row in $schema.Rows) {
        Write-Host "Catalog: $($row['CATALOG_NAME'])"
    }
    $conn.Close()
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
