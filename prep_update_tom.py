import json
import subprocess

with open('HTML_Onboarding_Executivo.dax', 'r', encoding='utf-8') as f:
    dax_code = f.read()

# Build TMSL Alter Measure script
# In TMSL, measure expression is inside createOrReplace
tmsl = {
    "createOrReplace": {
        "object": {
            "database": "3015f8a0-2f96-419b-8181-e28a5d3f27f0", # We can get DB name or use AMO
            "table": "vw_powerbi_empresas_Onboarding",
            "measure": "HTML_Onboarding_Executivo"
        },
        "measure": {
            "name": "HTML_Onboarding_Executivo",
            "expression": dax_code
        }
    }
}

# Alternatively, let's use PowerShell with Microsoft.AnalysisServices.Tabular
ps_script = f"""
$port = 57961
$connStr = "Provider=MSOLAP;Data Source=localhost:$port;"
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular") | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect($connStr)
$db = $server.Databases[0]
$table = $db.Model.Tables["vw_powerbi_empresas_Onboarding"]
$measure = $table.Measures["HTML_Onboarding_Executivo"]

$dax = [System.IO.File]::ReadAllText("c:\\Users\\cristhofer.maciel.GRUPOSTUDIO\\.gemini\\antigravity\\scratch\\automacao-mensageria-bi\\HTML_Onboarding_Executivo.dax", [System.Text.Encoding]::UTF8)
$measure.Expression = $dax
$db.Model.SaveChanges()
$server.Disconnect()
Write-Host "SUCCESSFULLY UPDATED MEASURE IN POWER BI VIA TOM!"
"""

with open('update_tom.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("Saved update_tom.ps1")
