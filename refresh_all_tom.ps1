
$port = 59771
$connStr = "Provider=MSOLAP;Data Source=localhost:$port;"
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular") | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect($connStr)
$db = $server.Databases[0]

Write-Host "Connected to database: $($db.Name)"
Write-Host "Model tables count: $($db.Model.Tables.Count)"

$sw = [System.Diagnostics.Stopwatch]::StartNew()
Write-Host "Starting Model.RequestRefresh(Full)..."

foreach ($table in $db.Model.Tables) {
    if (-not $table.Name.StartsWith("DateTableTemplate_") -and -not $table.Name.StartsWith("LocalDateTable_")) {
        Write-Host "Refreshing table: $($table.Name)..."
        $table.RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Full)
    }
}

$db.Model.SaveChanges()
$sw.Stop()

Write-Host "ALL TABLES REFRESHED SUCCESSFULLY IN $($sw.ElapsedMilliseconds) ms ($([Math]::Round($sw.ElapsedMilliseconds/1000, 2)) seconds)!"
$server.Disconnect()
