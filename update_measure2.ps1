[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.AnalysisServices.Tabular') | Out-Null
try {
    $server = New-Object Microsoft.AnalysisServices.Tabular.Server
    $server.Connect('localhost:63722')
    $db = $server.Databases[0]
    $table = $db.Model.Tables['medidas_html']
    $measure = $table.Measures['Painel_Repasses']
    
    $dax = Get-Content 'Painel_Repasses_Codigo.txt' -Raw -Encoding UTF8
    
    $measure.Expression = $dax
    
    $db.Model.SaveChanges()
    Write-Output 'Success!'
} catch {
    Write-Output "Error: $( $_.Exception.Message )"
    if ($_.Exception.InnerException) {
        Write-Output "Inner: $( $_.Exception.InnerException.Message )"
    }
}
