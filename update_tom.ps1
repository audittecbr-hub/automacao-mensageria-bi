
$port = 57961
$connStr = "Provider=MSOLAP;Data Source=localhost:$port;"
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular") | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect($connStr)
$db = $server.Databases[0]
$table = $db.Model.Tables["vw_powerbi_empresas_Onboarding"]
$measure = $table.Measures["HTML_Onboarding_Executivo"]

$dax = [System.IO.File]::ReadAllText("c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\HTML_Onboarding_Executivo.dax", [System.Text.Encoding]::UTF8)
$measure.Expression = $dax
$db.Model.SaveChanges()
$server.Disconnect()
Write-Host "SUCCESSFULLY UPDATED MEASURE IN POWER BI VIA TOM!"
