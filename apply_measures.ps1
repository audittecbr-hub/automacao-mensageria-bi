
[System.Reflection.Assembly]::LoadFrom("") | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:57299")
$model = $server.Databases[0].Model

$measuresJson = Get-Content -Raw -Encoding UTF8 "updated_html_measures.json" | ConvertFrom-Json

foreach ($m in $measuresJson) {
    $table = $model.Tables[$m.tableName]
    if ($table) {
        $measure = $table.Measures[$m.name]
        if ($measure) {
            $measure.Expression = $m.expression
            Write-Output "Updated: $($m.name)"
        } else {
            Write-Output "Measure not found: $($m.name)"
        }
    }
}

$model.SaveChanges()
Write-Output "SUCCESS: All measures saved to TOM on port 57299"
$server.Disconnect()
