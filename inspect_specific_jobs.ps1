$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
SELECTCOLUMNS(
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[JOB] = "87829-PRT" || vw_powerbi_relatorio_aprovacao[JOB] = "88380-PRT"
    ),
    "Job", vw_powerbi_relatorio_aprovacao[JOB],
    "Cli", vw_powerbi_relatorio_aprovacao[NOME],
    "AreaAnt", vw_powerbi_relatorio_aprovacao[AREA_ANTERIOR],
    "AreaAtual", vw_powerbi_relatorio_aprovacao[AREA_ATUAL],
    "DataRT", vw_powerbi_relatorio_aprovacao[DATA_RT],
    "DataMov", vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR],
    "HonIniciais", vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS],
    "UtlzInic", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS],
    "UtlzComp", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO],
    "UtlzRest", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO],
    "UtlzAjuiz", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO],
    "HonTotalAprovado", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APROVADO],
    "TotalAprovado", vw_powerbi_relatorio_aprovacao[TOTAL_APROVADO],
    "HonAtual", vw_powerbi_relatorio_aprovacao[HONORARIOS_ATUAL]
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
while ($rdr.Read()) {
    $vals = @()
    for ($i = 0; $i -lt $rdr.FieldCount; $i++) {
        $vals += "$($rdr.GetName($i)): $($rdr.GetValue($i))"
    }
    Write-Output ($vals -join " | ")
}
$rdr.Close()
$conn.Close()
