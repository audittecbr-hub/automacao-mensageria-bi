$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$q = @"
EVALUATE
FILTER(
    SELECTCOLUMNS(
        vw_powerbi_relatorio_aprovacao,
        "Job", vw_powerbi_relatorio_aprovacao[JOB],
        "DataRT", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_RT], "yyyy-MM-dd"),
        "DataMov", FORMAT(vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR], "yyyy-MM-dd"),
        "Val", [Honorários aprovados]
    ),
    [Val] > 0 && [DataRT] >= "2026-06-12"
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$rdr = $cmd.ExecuteReader()
$rows = @()
while ($rdr.Read()) {
    $rows += "$($rdr.GetValue(0))|$($rdr.GetValue(1))|$($rdr.GetValue(2))|$($rdr.GetValue(3))"
}
$rdr.Close()
$conn.Close()

[System.IO.File]::WriteAllLines("db_aprov_rows.txt", $rows)
Write-Output "Saved db_aprov_rows.txt, count: $($rows.Count)"
