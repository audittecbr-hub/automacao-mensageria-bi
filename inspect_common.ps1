
$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's inspect the entire list of 201 items if we can find them
# In Image 1, what are the first 15 jobs?
# 86730-FTX (2 rows: 14511.22 and 26824.47)
# 87233-RPQ (57440.99)
# 86146-T (48354.32)
# 87613-FTX (61178.91)
# 87616-FTX (78036.30)
# 87628-RPQ (75691.19)
# 87724-FTX (43003.39)
# 87724-PRT (23579.74)
# 87259-FTX (2 rows: 82894.61 and 30410.42)
# 87997-FTX (939205.97)
# 87671-FTX (101668.65)
# 88038-FTX (73336.24)
# 88038-RPQ (43107.53)

# Let's see what is common to ALL these rows in vw_powerbi_relatorio_aprovacao!
$q = @"
EVALUATE
FILTER(
    vw_powerbi_relatorio_aprovacao,
    vw_powerbi_relatorio_aprovacao[JOB] IN {
        "86730-FTX", "87233-RPQ", "86146-T", "87613-FTX", "87616-FTX", 
        "87628-RPQ", "87724-FTX", "87724-PRT", "87259-FTX", "87997-FTX", 
        "87671-FTX", "88038-FTX", "88038-RPQ"
    } && vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

Write-Output "Matching rows count: $($dt.Rows.Count)"

# Let's inspect column values that are identical across all these rows:
$allSame = @{}
foreach ($col in $dt.Columns) {
    $vals = New-Object System.Collections.Generic.HashSet[string]
    foreach ($row in $dt.Rows) {
        $vals.Add([string]$row[$col.ColumnName]) | Out-Null
    }
    if ($vals.Count -le 3) {
        Write-Output "Col: $($col.ColumnName) => Values: $([string]::Join(', ', $vals))"
    }
}

$conn.Close()
