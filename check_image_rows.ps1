$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's inspect the exact rows in Image 1:
# Sandro Renato Barboza: 86730-FTX (COMPENSACAO, 14.511,22), (AJUIZAMENTO, 26.824,47)
# Bari Transportes: 87233-RPQ (NEGOCIACAO, 57.440,99)
# SPM Resende: 86146-T (NEGOCIACAO, 48.354,32)
# Fernandes Distrib: 87613-FTX (NEGOCIACAO, 61.178,91)
# Bom Baiano: 87616-FTX (NEGOCIACAO, 78.036,30)
# Fort Luz: 87628-RPQ (NEGOCIACAO, 75.691,19)
# Bomfim: 87724-FTX (NEGOCIACAO, 43.003,39), 87724-PRT (NEGOCIACAO, 23.579,74)
# Shopping das Borrachas: 87259-FTX (NEGOCIACAO, 82.894,61), 87259-FTX (NEGOCIACAO, 30.410,42)
# Lopes & Barcelos: 87997-FTX (NEGOCIACAO, 939.205,97)

# Notice: All of these have AREA_ATUAL in (COMPENSACAO, AJUIZAMENTO, NEGOCIACAO)!
# Wait! In dump_encontrados_fixed.html:
# Row 0 was OPERACAO -> Not in Image 1!
# Row 1 was REUNIAO TECNICA -> Not in Image 1!
# Row 2 was FIM -> Not in Image 1!
# Row 3 was FIM -> Not in Image 1!
# Row 4 was COMPENSACAO -> IN IMAGE 1? Wait, Sandro was row 1 in Image 1!
# Why was Nutriminas (Row 4) not in Image 1? Nutriminas was SD (Regional Sudeste 2)!

# Let's check which Regional or Area or combination was shown!
$q = @"
EVALUATE
SUMMARIZECOLUMNS(
    vw_powerbi_relatorio_aprovacao[Regional],
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[JOB] IN {"86730-FTX", "87233-RPQ", "86146-T", "87613-FTX", "87616-FTX", "87628-RPQ", "87724-FTX", "87724-PRT", "87259-FTX", "87997-FTX"}
    ),
    "Cnt", COUNTROWS(vw_powerbi_relatorio_aprovacao)
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
foreach ($r in $dt.Rows) {
    Write-Output "Reg: $($r[0]) | Cnt: $($r[1])"
}
$conn.Close()
