$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$query = @"
EVALUATE
ROW(
    "HTML_Enc_Len", LEN([HTML_Detalhamento_Encontrados]),
    "HTML_Apr_Len", LEN([HTML_Detalhamento_Apresentados]),
    "HTML_Apv_Len", LEN([HTML_Detalhamento_Aprovados]),
    "HTML_Neg_Len", LEN([HTML_Detalhamento_Negociacao]),
    "HTML_Per_Len", LEN([HTML_Detalhamento_Perdidos]),
    "HTML_NaoApv_Len", LEN([HTML_Detalhamento_Nao_Aprovados])
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$dt | Format-List | Out-File -FilePath "compact_lens.txt" -Encoding UTF8
$conn.Close()
Write-Output "FINISHED_CHECK_LENS"
