$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$measuresToTest = @(
    "[Honorarios aprovados em negociacao]",
    "[Honorarios aprovados negociacao iniciais]",
    "[Honorarios aprovados negociacao compensacao]",
    "[Honorarios aprovados negociacao restituicao]",
    "[Honorarios aprovados negociacao ajuizamento]",
    "[Honorarios em negociacao]",
    "[Honorários apresentados]",
    "[Honorários perdidos]",
    "[Honorários não aprovados]",
    "[Honorários aprovados]"
)

foreach ($m in $measuresToTest) {
    try {
        $q = "EVALUATE ROW(`"Val`", $m)"
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
        $rdr = $cmd.ExecuteReader()
        if ($rdr.Read()) {
            Write-Output "OK: $m => $($rdr.GetValue(0))"
        }
        $rdr.Close()
    } catch {
        Write-Output "ERROR on $m : $($_.Exception.Message)"
    }
}
$conn.Close()
