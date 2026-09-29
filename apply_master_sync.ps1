$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$jsonPath = "C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\master_sync_payload.json"
$rawJson = [System.IO.File]::ReadAllText($jsonPath, [System.Text.Encoding]::UTF8)
$measures = ConvertFrom-Json $rawJson

foreach ($item in $measures) {
    $tableName = $item.tableName
    $name = $item.name
    $expr = $item.expression
    
    $table = $model.Tables[$tableName]
    if ($table -eq $null) {
        Write-Warning "Table not found: $tableName"
        continue
    }
    
    $m = $table.Measures[$name]
    if ($m -eq $null) {
        $m = New-Object Microsoft.AnalysisServices.Tabular.Measure
        $m.Name = $name
        $m.Expression = $expr
        $table.Measures.Add($m)
        Write-Output "Created measure: $name in $tableName"
    } else {
        $m.Expression = $expr
        Write-Output "Updated measure: $name in $tableName"
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_MASTER_SYNC_SAVED"
$server.Disconnect()
