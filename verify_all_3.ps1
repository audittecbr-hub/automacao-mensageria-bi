$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$measures = @("HTML_Detalhamento_Aprovados", "HTML_Detalhamento_Aprovados_Negociacao", "Mockup_Honorarios_Matriz")

foreach ($m in $measures) {
    try {
        $q = "EVALUATE ROW(`"Html`", [$m])"
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
        $rdr = $cmd.ExecuteReader()
        if ($rdr.Read()) {
            $html = $rdr.GetValue(0)
            [System.IO.File]::WriteAllText("dump_$m.html", $html, [System.Text.Encoding]::UTF8)
            Write-Output "OK: $m dumped successfully (length: $($html.Length))"
        }
        $rdr.Close()
    } catch {
        Write-Output "ERROR on $m : $($_.Exception.Message)"
    }
}
$conn.Close()
