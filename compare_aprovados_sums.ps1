$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$queries = [System.Collections.Specialized.OrderedDictionary]::new()
$queries.Add("Sum_HONORARIO_TOTAL_APROVADO", 'EVALUATE ROW("Sum", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_APROVADO]))')
$queries.Add("Sum_UTLZ_4_fields", 'EVALUATE ROW("Sum", SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS]) + SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO]) + SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO]) + SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]))')
$queries.Add("Sum_UTLZ_with_coalesce", 'EVALUATE ROW("Sum", SUMX(vw_powerbi_relatorio_aprovacao, COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]))')
$queries.Add("Sum_UTLZ_4_fields_RT_filter", 'EVALUATE ROW("Sum", SUMX(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026,6,12)), vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]))')
$queries.Add("Sum_UTLZ_coalesce_RT_filter", 'EVALUATE ROW("Sum", SUMX(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026,6,12)), COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]))')
$queries.Add("Count_UTLZ_4_fields_RT_filter", 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026,6,12) && (vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0)))')
$queries.Add("Count_UTLZ_coalesce_RT_filter", 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026,6,12) && (COALESCE(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_HONORARIOS_INICIAIS], vw_powerbi_relatorio_aprovacao[HONORARIOS_INICIAIS], 0) + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_COMPENSACAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_RESTITUICAO] + vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_FORMA_UTLZ_AJUIZAMENTO]) > 0)))')

foreach ($k in $queries.Keys) {
    try {
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($queries[$k], $conn)
        $rdr = $cmd.ExecuteReader()
        if ($rdr.Read()) {
            Write-Output "$k => $($rdr.GetValue(0))"
        }
        $rdr.Close()
    } catch {
        Write-Output "$k => ERROR: $($_.Exception.Message)"
    }
}
$conn.Close()
