$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
SELECTCOLUMNS(
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[JOB] = "88208-FTX" ||
        vw_powerbi_relatorio_aprovacao[JOB] = "88207-FTX" ||
        vw_powerbi_relatorio_aprovacao[JOB] = "88209-FTX"
    ),
    "Job", vw_powerbi_relatorio_aprovacao[JOB],
    "Cli", vw_powerbi_relatorio_aprovacao[NOME],
    "DataRT", vw_powerbi_relatorio_aprovacao[DATA_RT],
    "DataMov", vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR],
    "Iniciais", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS],
    "Comp", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO],
    "Rest", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO],
    "Ajuiz", vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]
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
