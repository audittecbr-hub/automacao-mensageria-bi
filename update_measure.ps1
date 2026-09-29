[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.AnalysisServices.Tabular') | Out-Null
try {
     = New-Object Microsoft.AnalysisServices.Tabular.Server
    .Connect('localhost:63722')
     = .Databases[0]
     = .Model.Tables['medidas_html']
     = .Measures['Painel_Repasses']
    
     = Get-Content 'Painel_Repasses_Codigo.txt' -Raw -Encoding UTF8
    
    .Expression = 
    
    .Databases[0].Model.SaveChanges()
    Write-Output 'Success!'
} catch {
    Write-Output "Error: "
    if (.Exception.InnerException) {
        Write-Output "Inner: "
    }
}
