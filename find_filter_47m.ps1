$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's test different filters on DATA_MOV_ANTERIOR and DATA_RT and AREA
$queries = @{
    "Filtro_Hoje" = "EVALUATE ROW('Cnt', COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, [Honorários encontrados] > 0)), 'Sum', CALCULATE([Honorários encontrados]))"
    "Filtro_Mes_Atual" = "EVALUATE ROW('Cnt', COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, [Honorários encontrados] > 0 && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], ""yyyy-MM"") = ""2026-08"")), 'Sum', CALCULATE([Honorários encontrados], FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], ""yyyy-MM"") = ""2026-08""))"
    "Filtro_Mes_07" = "EVALUATE ROW('Cnt', COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, [Honorários encontrados] > 0 && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], ""yyyy-MM"") = ""2026-07"")), 'Sum', CALCULATE([Honorários encontrados], FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], ""yyyy-MM"") = ""2026-07""))"
}

foreach ($k in $queries.Keys) {
    $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($queries[$k], $conn)
    $rdr = $cmd.ExecuteReader()
    if ($rdr.Read()) {
        Write-Output "$k => Cnt: $($rdr.GetValue(0)) | Sum: $($rdr.GetValue(1))"
    }
    $rdr.Close()
}
$conn.Close()
