$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's test what produces 512 rows:
# Could it be Power BI visual filter? E.g., is there a filter on the page or visual for Regional, or date, or area?
# Or is CONCATENATEX hitting the string limit?
# Let's check LEN of the CONCATENATEX or number of rows in the visual!

$query = @"
EVALUATE
ROW(
    "Len_Detalhamento", LEN([HTML_Detalhamento_Encontrados])
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
Write-Output "Len: $($dt.Rows[0][0])"

# Let's count how many rows are in the HTML string:
$query2 = 'EVALUATE ROW("HTML", [HTML_Detalhamento_Encontrados])'
$cmd2 = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query2, $conn)
$rdr = $cmd2.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetString(0)
    $count = ([regex]::Matches($html, "class='linha-detalhe'")).Count
    Write-Output "Total rows in HTML string: $count"
    
    # Let's sum data-val in the HTML string
    $matches = [regex]::Matches($html, "data-val='([^']+)'")
    $sum = 0.0
    foreach ($m in $matches) {
        $val = [double]::Parse($m.Groups[1].Value, [System.Globalization.CultureInfo]::InvariantCulture)
        $sum += $val
    }
    Write-Output "Sum data-val in HTML string: $sum"
}

$conn.Close()
