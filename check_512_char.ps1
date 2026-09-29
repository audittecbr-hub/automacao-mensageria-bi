$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query2 = 'EVALUATE ROW("HTML", [HTML_Detalhamento_Encontrados])'
$cmd2 = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query2, $conn)
$rdr = $cmd2.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetString(0)
    $matches = [regex]::Matches($html, "<tr class='linha-detalhe'[^>]*>.*?</tr>")
    Write-Output "Total matches: $($matches.Count)"
    if ($matches.Count -ge 512) {
        $m512 = $matches[511]
        $index512 = $m512.Index + $m512.Length
        Write-Output "Character index after 512th row: $index512"
        
        # Let's sum the first 512 rows:
        $sum512 = 0.0
        for ($i = 0; $i -lt 512; $i++) {
            $m = [regex]::Match($matches[$i].Value, "data-val='([^']+)'")
            if ($m.Success) {
                $sum512 += [double]::Parse($m.Groups[1].Value, [System.Globalization.CultureInfo]::InvariantCulture)
            }
        }
        Write-Output "Sum of first 512 rows in HTML: $sum512"
    }
}
$conn.Close()
