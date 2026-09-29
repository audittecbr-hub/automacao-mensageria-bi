import json
import re
import subprocess

with open('Mockup_Honorarios_Matriz_Current.dax', 'r', encoding='utf-8') as f:
    code = f.read()

code_norm = code.replace('\r\n', '\n')

detalhes_pattern = re.compile(r'VAR _linha2_detalhes\s*=\s*.*?VAR _linha_nao_aprovados', re.DOTALL)
new_detalhes_clean = """VAR _linha2_detalhes = 
    "<tr class='detalhe-aprovados' style='display:none; background: rgba(255,255,255,0.02);'>" &
        "<td colspan='6' style='padding-left: 40px; font-size:13px !important; font-weight: normal !important; color:var(--text-sec) !important; text-align:left !important; border-left: 3px solid var(--accent); padding-top:14px; padding-bottom:14px;'><div style='display:flex; align-items:center; gap:14px; flex-wrap:wrap;'><span style='color:var(--text-main); font-weight:700; font-size:13px; text-transform:uppercase; letter-spacing:0.5px;'>&#127942; Legenda de Pontuação:</span><span style='background:rgba(255,255,255,0.06); padding:6px 12px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); font-size:13px; color:#fff;'>Honorários Iniciais = <b style='color:var(--accent); font-size:14px;'>4 pts</b></span><span style='background:rgba(255,255,255,0.06); padding:6px 12px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); font-size:13px; color:#fff;'>Honorários Compensação = <b style='color:var(--accent); font-size:14px;'>3 pts</b></span><span style='background:rgba(255,255,255,0.06); padding:6px 12px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); font-size:13px; color:#fff;'>Honorários Restituição = <b style='color:var(--accent); font-size:14px;'>2 pts</b></span><span style='background:rgba(255,255,255,0.06); padding:6px 12px; border-radius:6px; border:1px solid rgba(255,255,255,0.08); font-size:13px; color:#fff;'>Honorários Ajuizamento = <b style='color:var(--accent); font-size:14px;'>1 pt</b></span></div></td>" &
    "</tr>" &
    "<tr class='detalhe-aprovados' style='display:none; background: rgba(255,255,255,0.02);'>" &
        "<td style='padding-left: 40px; font-size:15px; font-weight:600; color:var(--text-main); border-left: 3px solid var(--accent); padding-top:14px; padding-bottom:14px;'><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:16px; color:var(--accent);'>&#128269;</span> Honorários Iniciais</div></td>" &
        "<td id='hi-sul' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hi-sp' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hi-sd' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hi-nn' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hi-total' style='font-size:22px; font-weight:700; font-variant-numeric: tabular-nums; letter-spacing: -0.5px; color:var(--accent);'>R$ 0,00</td>" &
    "</tr>" &
    "<tr class='detalhe-aprovados' style='display:none; background: rgba(255,255,255,0.02);'>" &
        "<td style='padding-left: 40px; font-size:15px; font-weight:600; color:var(--text-main); border-left: 3px solid var(--accent); padding-top:14px; padding-bottom:14px;'><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:16px; color:var(--accent);'>&#128269;</span> Honorários Compensação</div></td>" &
        "<td id='hc-sul' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hc-sp' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hc-sd' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hc-nn' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hc-total' style='font-size:22px; font-weight:700; font-variant-numeric: tabular-nums; letter-spacing: -0.5px; color:var(--accent);'>R$ 0,00</td>" &
    "</tr>" &
    "<tr class='detalhe-aprovados' style='display:none; background: rgba(255,255,255,0.02);'>" &
        "<td style='padding-left: 40px; font-size:15px; font-weight:600; color:var(--text-main); border-left: 3px solid var(--accent); padding-top:14px; padding-bottom:14px;'><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:16px; color:var(--accent);'>&#128269;</span> Honorários Restituição</div></td>" &
        "<td id='hr-sul' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hr-sp' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hr-sd' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hr-nn' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='hr-total' style='font-size:22px; font-weight:700; font-variant-numeric: tabular-nums; letter-spacing: -0.5px; color:var(--accent);'>R$ 0,00</td>" &
    "</tr>" &
    "<tr class='detalhe-aprovados' style='display:none; background: rgba(255,255,255,0.02);'>" &
        "<td style='padding-left: 40px; font-size:15px; font-weight:600; color:var(--text-main); border-left: 3px solid var(--accent); border-bottom-left-radius: 8px; padding-top:14px; padding-bottom:14px;'><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:16px; color:var(--accent);'>&#128269;</span> Honorários Ajuizamento</div></td>" &
        "<td id='ha-sul' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='ha-sp' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='ha-sd' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='ha-nn' style='font-size:16px; font-weight:600; color:var(--text-main); font-variant-numeric: tabular-nums;'>R$ 0,00</td>" &
        "<td id='ha-total' style='font-size:22px; font-weight:700; font-variant-numeric: tabular-nums; letter-spacing: -0.5px; color:var(--accent); border-bottom-right-radius: 8px;'>R$ 0,00</td>" &
    "</tr>\n\nVAR _linha_nao_aprovados"

code_norm = detalhes_pattern.sub(new_detalhes_clean, code_norm)

pts_pattern = re.compile(r'var ptsSul\s*=\s*tSul\s*\*\s*2;.*?var ptsNN\s*=\s*tNN\s*\*\s*2;', re.DOTALL)
new_pts_code = """var ptsSul = (sAp['Regional Sul'] * 4) + (sComp['Regional Sul'] * 3) + (sRetif['Regional Sul'] * 2) + (sAjuiz['Regional Sul'] * 1);
        var ptsSP = (sAp['Regional Sudeste'] * 4) + (sComp['Regional Sudeste'] * 3) + (sRetif['Regional Sudeste'] * 2) + (sAjuiz['Regional Sudeste'] * 1);
        var ptsSD = (sAp['Regional Sudeste 2'] * 4) + (sComp['Regional Sudeste 2'] * 3) + (sRetif['Regional Sudeste 2'] * 2) + (sAjuiz['Regional Sudeste 2'] * 1);
        var ptsNN = (sAp['Regional NNCO'] * 4) + (sComp['Regional NNCO'] * 3) + (sRetif['Regional NNCO'] * 2) + (sAjuiz['Regional NNCO'] * 1);"""

code_norm = pts_pattern.sub(new_pts_code, code_norm)

payload = [
    {
        "tableName": "medidas_html",
        "name": "Mockup_Honorarios_Matriz",
        "expression": code_norm
    }
]

with open('update_mockup_font_payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

ps_apply = """
$dll = "C:\\Program Files\\On-premises data gateway\\FabricIntegrationRuntime\\5.0\\Gateway\\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$json = Get-Content -Raw -Encoding UTF8 "update_mockup_font_payload.json" | ConvertFrom-Json

foreach ($item in $json) {
    $table = $model.Tables[$item.tableName]
    if ($table) {
        $m = $table.Measures[$item.name]
        if ($m) {
            $m.Expression = $item.expression
            Write-Output "Updated measure: $($item.name) in table $($item.tableName)"
        }
    }
}

$model.SaveChanges()
Write-Output "SUCCESS_SAVED"
$server.Disconnect()
"""

with open('apply_font_update.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_apply)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "apply_font_update.ps1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(res.stdout.decode('latin1', errors='replace'))
