$port = 52151

# 1. Update in-memory Tabular Model via TOM / AMO
$assembly = [System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular")
if (-not $assembly) {
    # Try finding Microsoft.AnalysisServices.Tabular.dll
    $dllPaths = Get-ChildItem -Path "C:\Program Files\Microsoft Power BI Desktop", "C:\Users\cristhofer.maciel.GRUPOSTUDIO\AppData\Local\Microsoft\Power BI Desktop" -Filter "Microsoft.AnalysisServices.Tabular.dll" -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName
    if ($dllPaths) {
        [System.Reflection.Assembly]::LoadFrom($dllPaths[0]) | Out-Null
    }
}

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:$port")
$db = $server.Databases[0]
$table = $db.Model.Tables["medidas_html"]
$measure = $table.Measures["Painel_Repasses"]

$daxCode = Get-Content -Path "Painel_Repasses_dax.txt" -Raw -Encoding UTF8
$measure.Expression = $daxCode
$db.Model.SaveChanges()
$server.Disconnect()

Write-Host "Measure Painel_Repasses updated in TOM memory!"

# 2. Update TMDL on disk
$tmdlPath = "C:\Users\cristhofer.maciel.GRUPOSTUDIO\OneDrive\repasse.SemanticModel\definition\tables\medidas_html.tmdl"
if (Test-Path $tmdlPath) {
    $tmdlContent = Get-Content -Path $tmdlPath -Raw -Encoding UTF8
    
    # Format indented DAX for TMDL
    $lines = $daxCode -split "`r?`n"
    $indentedDax = ($lines | ForEach-Object { "`t\t\t\t$_" }) -join "`r`n"
    
    $pattern = "(?s)measure Painel_Repasses =.*?(?=\r?\n\tlineageTag|\r?\n\tannotation|\r?\n\tmeasure|\r?\n\tcolumn|$)"
    $replacement = "measure Painel_Repasses = `r`n" + $indentedDax
    
    $newTmdl = $tmdlContent -replace $pattern, $replacement
    Set-Content -Path $tmdlPath -Value $newTmdl -Encoding UTF8
    Write-Host "medidas_html.tmdl updated on disk!"
}
