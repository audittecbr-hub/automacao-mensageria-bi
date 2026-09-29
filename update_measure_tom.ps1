$serverName = "localhost:56243"

# Load AMO / TOM assemblies
$amoPath = Get-ChildItem -Path "C:\Program Files\Microsoft Office", "C:\Program Files\Microsoft Power BI Desktop", "C:\Users\cristhofer.maciel.GRUPOSTUDIO\AppData" -Filter "Microsoft.AnalysisServices.Tabular.dll" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($amoPath) {
    [System.Reflection.Assembly]::LoadFrom($amoPath.FullName) | Out-Null
    Write-Host "TOM Assembly carregada: $($amoPath.FullName)"
} else {
    [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular") | Out-Null
}

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("Data Source=$serverName;")

$database = $server.Databases[0]
$model = $database.Model

$table = $model.Tables["medidas_html"]
$measure = $table.Measures["Painel_Repasses"]

$newDax = [System.IO.File]::ReadAllText("c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\updated_painel_repasses.dax", [System.Text.Encoding]::UTF8)

$measure.Expression = $newDax
$model.SaveChanges()
Write-Host "Medida Painel_Repasses atualizada com sucesso no Power BI Desktop!"

$server.Disconnect()
