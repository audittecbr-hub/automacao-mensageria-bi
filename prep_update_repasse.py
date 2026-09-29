import subprocess

ps_script = """
[System.Reflection.Assembly]::LoadWithPartialName("Microsoft.AnalysisServices.Tabular") | Out-Null
try {
    $port = 51444
    $server = New-Object Microsoft.AnalysisServices.Tabular.Server
    $server.Connect("localhost:$port")
    $db = $server.Databases[0]
    $table = $db.Model.Tables["medidas_html"]
    $measure = $table.Measures["Painel_Repasses"]
    
    $dax = [System.IO.File]::ReadAllText("c:\\Users\\cristhofer.maciel.GRUPOSTUDIO\\.gemini\\antigravity\\scratch\\automacao-mensageria-bi\\Painel_Repasses_dax.txt", [System.Text.Encoding]::UTF8)
    $measure.Expression = $dax
    $db.Model.SaveChanges()
    $server.Disconnect()
    Write-Host "SUCCESSFULLY_UPDATED_PAINEL_REPASSES"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}
"""

with open('update_repasse_tom.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

print("Saved update_repasse_tom.ps1")
