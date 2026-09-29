$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's check what combination gives 201 rows in vw_powerbi_relatorio_aprovacao
$cols = @("Regional", "AREA_ATUAL", "AREA_ANTERIOR", "NOME_TRIBUTO", "MES_BASE", "ANO_BASE")

foreach ($c in $cols) {
    $q = @"
EVALUATE
SUMMARIZECOLUMNS(
    vw_powerbi_relatorio_aprovacao[$c],
    "Cnt", CALCULATE(COUNTROWS(vw_powerbi_relatorio_aprovacao), vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0, vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)),
    "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1), vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31))
)
"@
    try {
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
        $adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
        $dt = New-Object System.Data.DataTable
        $adapter.Fill($dt) | Out-Null
        foreach ($r in $dt.Rows) {
            $cnt = $r["Cnt"]
            $sum = $r["Sum"]
            if ($cnt -eq 201 -or ($sum -gt 47000000 -and $sum -lt 48000000)) {
                Write-Output "MATCH in ${c}: Value=$($r[0]) | Cnt=$cnt | Sum=$sum"
            }
        }
    } catch {
        Write-Output "Error in $c : $_"
    }
}
$conn.Close()
