import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")

$query = @"
EVALUATE
TOPN(
    20,
    FILTER(
        vw_powerbi_relatorio_aprovacao,
        vw_powerbi_relatorio_aprovacao[TOTAL_ENCONTRADO] > 0 || vw_powerbi_relatorio_aprovacao[TOTAL_APRESENTADO] > 0
    ),
    vw_powerbi_relatorio_aprovacao[JOB], ASC
)
"@

$cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, (New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:60593")))
$cmd.Connection.Open()
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null

$cols = @("JOB", "NOME", "Regional", "DATA_RT", "AREA_ANTERIOR", "AREA_ATUAL", "TOTAL_ENCONTRADO", "TOTAL_APRESENTADO", "HONORARIO_TOTAL_ENCONTRADO", "HONORARIO_TOTAL_APRESENTADO", "VALOR_ATUAL", "HONORARIOS_ATUAL")
foreach ($r in $dt.Rows) {
    $line = ""
    foreach ($c in $cols) {
        $val = $r[$c]
        $line += "$c: $val | "
    }
    Write-Output $line
}
$cmd.Connection.Close()
$server.Disconnect()
"""

with open('check_cols_diff.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "check_cols_diff.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
text = res.stdout.decode('latin1', errors='replace')
with open('diff_output.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved diff_output.txt")
