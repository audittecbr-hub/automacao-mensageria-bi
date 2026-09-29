import subprocess

ps = """
$adomdDll = "C:\\Program Files\\On-premises data gateway\\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

# Let's check which measure or expression yields 47186526 or 201 rows
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$tabularDll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

foreach ($t in $model.Tables) {
    foreach ($m in $t.Measures) {
        $q = "EVALUATE ROW(`"Val`", [$($m.Name)])"
        try {
            $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
            $r = $cmd.ExecuteReader()
            if ($r.Read()) {
                $val = $r.GetValue(0)
                if ($val -is [double] -or $val -is [decimal]) {
                    if ($val -gt 47000000 -and $val -lt 48000000) {
                        Write-Output "MATCH MEASURE: $($m.Name) => $val"
                    }
                }
            }
            $r.Close()
        } catch {}
    }
}
$conn.Close()
$server.Disconnect()
"""

with open('search_47m.ps1', 'w', encoding='utf-8') as f:
    f.write(ps)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "search_47m.ps1"], capture_output=True, text=True)
print(res.stdout)
