
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:60593")
$conn.Open()

$query = @"
EVALUATE
TOPN(
    20,
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APROVADO] > 0
    ),
    vw_powerbi_relatorio_aprovacao[JOB], ASC
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$cols = @("JOB", "NOME", "Regional", "HONORARIO_TOTAL_APROVADO", "HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO", "HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO", "HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO", "HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS", "HONORARIOS_INICIAIS", "HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_MENSAIS")
foreach ($r in $dt.Rows) {
    $line = ""
    foreach ($c in $cols) {
        $val = $r[$c]
        $line += "$c: $val | "
    }
    Write-Output $line
}
$conn.Close()
