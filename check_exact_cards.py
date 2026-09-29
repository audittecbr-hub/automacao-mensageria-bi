# Let's extract the exact evaluated string of [Mockup_Honorarios_Matriz] from the model
# and parse the spans to calculate the exact card totals!
import re
import subprocess

ps_script = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$query = "EVALUATE ROW('Mockup', [Mockup_Honorarios_Matriz])"
$cmd = $server.Connection.CreateCommand()
$cmd.CommandText = $query
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetString(0)
    [System.IO.File]::WriteAllText("mockup_eval.html", $html, [System.Text.Encoding]::UTF8)
    Write-Output "SAVED_MOCKUP_EVAL"
}
$server.Disconnect()
"""

with open('get_mockup_eval.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "get_mockup_eval.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(res.stdout.decode('latin1', errors='replace'))

# Now let's parse the spans in mockup_eval.html
with open('mockup_eval.html', 'r', encoding='utf-8') as f:
    html = f.read()

classes = ['dado-enc', 'dado-apres', 'dado-aprov-total', 'dado-nao-aprov', 'dado-perdidos', 'dado-nao-aprovados-real']

print("\n=== VALORES DOS CARDS CALCULADOS NO MOCKUP ===")
for c in classes:
    pattern = rf"<span class='{c}'[^>]*>"
    matches = re.findall(pattern, html)
    total_val = 0.0
    total_val_sr = 0.0
    for m in matches:
        v_match = re.search(r"data-valor='([^']*)'", m)
        vsr_match = re.search(r"data-valor-sr='([^']*)'", m)
        if v_match:
            try:
                total_val += float(v_match.group(1).replace(',', '.'))
            except:
                pass
        if vsr_match:
            try:
                total_val_sr += float(vsr_match.group(1).replace(',', '.'))
            except:
                pass
    print(f"Classe: {c:25} | Com Regra RT: R$ {total_val:15,.2f} | Sem Regra RT: R$ {total_val_sr:15,.2f}")
