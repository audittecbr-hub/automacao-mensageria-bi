$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "Encontrados", [Honorários encontrados],
    "Apresentados", [Honorários apresentados],
    "Aprovados", [Honorários aprovados],
    "Negociacao", [Honorário negociação],
    "Perdidos", [Honorários perdidos],
    "Nao_Aprovados", [Honorários não aprovados]
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-List | Out-File -FilePath "verified_hon_base.txt" -Encoding UTF8
$conn.Close()
Write-Output "FINISHED_VERIFICATION"
