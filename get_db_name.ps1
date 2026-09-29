
$port = 51444
$connStr = "Provider=MSOLAP;Data Source=localhost:$port;Initial Catalog=;"
$conn = New-Object System.Data.OleDb.OleDbConnection($connStr)
$conn.Open()

# Read DB Name
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT [CATALOG_NAME] FROM $SYSTEM.DBSCHEMA_CATALOGS"
$adapter = New-Object System.Data.OleDb.OleDbDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dbName = $dt.Rows[0]["CATALOG_NAME"]
Write-Host "Database Name: $dbName"

$conn.Close()
