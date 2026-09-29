import subprocess

ps = """
$adomdDll = "C:\\Program Files\\On-premises data gateway\\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$raw = [System.IO.File]::ReadAllText("matriz_perfect.dax", [System.Text.Encoding]::UTF8)
$vars = $raw -split '(?m)^VAR '

Write-Output "Total VARs: $($vars.Count)"

$accum = ""
for ($i = 1; $i -lt $vars.Count; $i++) {
    $v = "VAR " + $vars[$i]
    $varName = $vars[$i].Substring(0, $vars[$i].IndexOf('=' )).Trim()
    $testDax = $accum + "`n" + $v + "`nRETURN " + $varName
    $q = "EVALUATE ROW(`"Test`", " + $testDax + ")"
    try {
        $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($q, $conn)
        $rdr = $cmd.ExecuteReader()
        $rdr.Close()
        # Write-Output "VAR $i ($varName) OK"
        $accum += "`n" + $v
    } catch {
        Write-Output "SYNTAX ERROR AT VAR $i: $varName"
        Write-Output "Error details: $($_.Exception.Message)"
        break
    }
}

$conn.Close()
"""

with open('debug_vars.ps1', 'w', encoding='utf-8') as f:
    f.write(ps)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "debug_vars.ps1"], capture_output=True, text=True)
print(res.stdout)
print(res.stderr)
