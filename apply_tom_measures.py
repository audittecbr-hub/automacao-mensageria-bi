import json
import subprocess

with open('updated_html_measures.json', 'r', encoding='utf-8') as f:
    measures = json.load(f)

# Find Microsoft.AnalysisServices.Tabular.dll
ps_find_dll = """
$paths = @(
    "C:\\Program Files\\Microsoft Power BI Desktop\\bin\\Microsoft.AnalysisServices.Tabular.dll",
    "C:\\Program Files\\Microsoft Power BI Desktop RS\\bin\\Microsoft.AnalysisServices.Tabular.dll"
)
foreach ($p in $paths) {
    if (Test-Path $p) { Write-Output $p; exit }
}
$gac = Get-ChildItem -Path "C:\\Windows\\Microsoft.NET\\assembly" -Filter "Microsoft.AnalysisServices.Tabular.dll" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
if ($gac) { Write-Output $gac.FullName; exit }
"""
res = subprocess.run(["powershell", "-Command", ps_find_dll], capture_output=True, text=True)
dll_path = res.stdout.strip().split('\n')[0].strip()
print(f"DLL: {dll_path}")

ps_script = f"""
[System.Reflection.Assembly]::LoadFrom("{dll_path}") | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:57299")
$model = $server.Databases[0].Model

$measuresJson = Get-Content -Raw -Encoding UTF8 "updated_html_measures.json" | ConvertFrom-Json

foreach ($m in $measuresJson) {{
    $table = $model.Tables[$m.tableName]
    if ($table) {{
        $measure = $table.Measures[$m.name]
        if ($measure) {{
            $measure.Expression = $m.expression
            Write-Output "Updated: $($m.name)"
        }} else {{
            Write-Output "Measure not found: $($m.name)"
        }}
    }}
}}

$model.SaveChanges()
Write-Output "SUCCESS: All measures saved to TOM on port 57299"
$server.Disconnect()
"""

with open('apply_measures.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res2 = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "apply_measures.ps1"], capture_output=True, text=True)
print(res2.stdout)
if res2.stderr:
    print(f"Error: {res2.stderr}")
