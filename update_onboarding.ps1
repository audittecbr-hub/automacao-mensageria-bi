[System.Reflection.Assembly]::LoadFrom('C:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity-ide\mcp\powerbi-modeling-mcp\Microsoft.AnalysisServices.Tabular.dll') | Out-Null
try {
    $server = New-Object Microsoft.AnalysisServices.Tabular.Server
    $server.Connect('localhost:57961')
    $db = $server.Databases[0]
    $table = $db.Model.Tables['vw_powerbi_empresas_Onboarding']
    $measure = $table.Measures['HTML_Onboarding_Executivo']
    
    $dax = Get-Content 'HTML_Onboarding_Executivo.dax' -Raw -Encoding UTF8
    
    $measure.Expression = $dax
    
    $db.Model.SaveChanges()
    Write-Output 'SUCCESSFULLY_UPDATED_ONBOARDING_MEASURE'
} catch {
    Write-Output "Error: $( $_.Exception.Message )"
    if ($_.Exception.InnerException) {
        Write-Output "Inner: $( $_.Exception.InnerException.Message )"
    }
}
