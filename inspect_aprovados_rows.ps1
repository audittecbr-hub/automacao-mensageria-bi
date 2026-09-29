$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
TOPN(
    25,
    SELECTCOLUMNS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            (COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0
        ),
        "Job", vw_powerbi_relatorio_aprovacao[JOB],
        "Cliente", vw_powerbi_relatorio_aprovacao[NOME],
        "AreaAnterior", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR],
        "AreaAtual", vw_powerbi_relatorio_aprovacao[AREA_ATUAL],
        "Status", vw_powerbi_relatorio_aprovacao[STATUS],
        "NomeTributo", vw_powerbi_relatorio_aprovacao[NOME_TRIBUTO],
        "DataRT", vw_powerbi_relatorio_aprovacao[DATA_RT],
        "DataMov", vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR],
        "ValIniciais", COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0),
        "ValComp", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO],
        "ValRest", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO],
        "ValAjuiz", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO],
        "ValTotalAprov", COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + 
             vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
    )
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$da = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$da.Fill($dt) | Out-Null

foreach ($r in $dt.Rows) {
    Write-Output "JOB: $($r['Job']) | CLI: $($r['Cliente']) | AREA_ANT: $($r['AreaAnterior']) | AREA_ATUAL: $($r['AreaAtual']) | STATUS: $($r['Status']) | TRIB: $($r['NomeTributo']) | VAL: $($r['ValTotalAprov'])"
}

$conn.Close()
