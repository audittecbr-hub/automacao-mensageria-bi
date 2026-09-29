$port = 62970
$connString = "Provider=MSOLAP;Data Source=localhost:$port;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connString)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT [TABLE_NAME], [MEASURE_NAME], [EXPRESSION] FROM `$SYSTEM.MDSCHEMA_MEASURES"
$adapter = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()

Write-Host "Found $($dt.Rows.Count) measures in MDSCHEMA_MEASURES"

foreach ($row in $dt.Rows) {
    $t = $row["TABLE_NAME"]
    $m = $row["MEASURE_NAME"]
    $expr = $row["EXPRESSION"]
    
    if ($expr -like "*SYNTAXERROR*" -or $expr -like "*\\*") {
        Write-Host "FOUND: [$t].[$m]"
        # write out the lines with error
        $lines = $expr.Split("`n")
        for ($i = 0; $i -lt $lines.Length; $i++) {
            if ($lines[$i] -like "*SYNTAXERROR*" -or $lines[$i] -like "*\\*") {
                Write-Host "  Line $($i+1): $($lines[$i])"
            }
        }
    }
}
