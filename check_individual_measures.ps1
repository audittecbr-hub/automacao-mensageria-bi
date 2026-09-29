$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$measures = @(
    "Honorários encontrados",
    "Honorários apresentados",
    "Honorários aprovados",
    "Honorário negociação",
    "Honorários perdidos",
    "Honorários não aprovados",
    "HTML_Detalhamento_Encontrados",
    "HTML_Detalhamento_Apresentados",
    "HTML_Detalhamento_Aprovados",
    "HTML_Detalhamento_Negociacao",
    "HTML_Detalhamento_Perdidos",
    "HTML_Detalhamento_Nao_Aprovados"
)

foreach ($name in $measures) {
    try {
        $query = "EVALUATE ROW(`"Test`", [$name])"
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
        $rdr = $cmd.ExecuteReader()
        Write-Output "OK: $name"
    } catch {
        Write-Output "ERROR in $name : $($_.Exception.Message)"
    }
}
$conn.Close()
