$daxPath = "c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\Painel_Repasses_dax.txt"
$dax = [System.IO.File]::ReadAllText($daxPath, [System.Text.Encoding]::UTF8)

$dll1 = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Core.dll"
$dll2 = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"

if (Test-Path $dll1) { [System.Reflection.Assembly]::LoadFrom($dll1) | Out-Null }
if (Test-Path $dll2) { [System.Reflection.Assembly]::LoadFrom($dll2) | Out-Null }

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:53635")
Write-Host "Connected to server: $($server.Name)"

$db = $server.Databases[0]
Write-Host "Database: $($db.Name)"

$table = $db.Model.Tables["medidas_html"]
$measure = $table.Measures["Painel_Repasses"]

$measure.Expression = $dax
$db.Model.SaveChanges()
Write-Host "SUCCESS: Painel_Repasses updated successfully in repasse model!"
$server.Disconnect()
