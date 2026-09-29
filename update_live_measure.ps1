param(
    [int]$port = 57503
)

[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.AnalysisServices.Tabular') | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:$port")
Write-Host "Connected to server. Database: $($server.Databases[0].Name)"

$db = $server.Databases[0]
$table = $db.Model.Tables['medidas_html']
$measure = $table.Measures['Painel_Repasses']

$jsonPath = "c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\update_repasse_mcp_req.json"
$rawJson = Get-Content -Path $jsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
$newExpr = $rawJson.request.definitions[0].expression

$measure.Expression = $newExpr
$db.Model.SaveChanges()

Write-Host "Measure Painel_Repasses updated and saved successfully in running Power BI Desktop instance!"
$server.Disconnect()
