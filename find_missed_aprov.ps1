$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
FILTER(
    SELECTCOLUMNS(
        FILTER(
            vw_powerbi_relatorio_aprovacao,
            vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) &&
            [Honorários aprovados] > 0
        ),
        "Job", vw_powerbi_relatorio_aprovacao[JOB],
        "DataRT", vw_powerbi_relatorio_aprovacao[DATA_RT],
        "DataMov", vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR],
        "Val", [Honorários aprovados]
    ),
    ISBLANK([DataMov]) || [DataMov] < DATE(2026, 6, 1) || [DataMov] > DATE(2026, 12, 31)
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
while ($rdr.Read()) {
    Write-Output "Job: $($rdr.GetValue(0)) | DataRT: $($rdr.GetValue(1)) | DataMov: $($rdr.GetValue(2)) | Val: $($rdr.GetValue(3))"
}
$rdr.Close()
$conn.Close()
