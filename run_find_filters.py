import subprocess

ps_script = """
$adomdDll = "C:\\Program Files\\On-premises data gateway\\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

$queries = [ordered]@{
    "Mes_Atual_08_com_RT" = 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-08")), "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-08"))'
    "Mes_Atual_08_sem_RT" = 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-08")), "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-08"))'
    "Mes_07_com_RT" = 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-07")), "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-07"))'
    "Mes_07_sem_RT" = 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-07")), "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-07"))'
    "Mes_06_com_RT" = 'EVALUATE ROW("Cnt", COUNTROWS(FILTER(vw_powerbi_relatorio_aprovacao, vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO] > 0 && vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12) && FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-06")), "Sum", CALCULATE(SUM(vw_powerbi_relatorio_aprovacao[HONORARIO_TOTAL_ENCONTRADO]), vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12), FORMAT(vw_powerbi_relatorio_aprovacao[data_mov_anterior], "yyyy-MM") = "2026-06"))'
}

foreach ($k in $queries.Keys) {
    $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($queries[$k], $conn)
    $rdr = $cmd.ExecuteReader()
    if ($rdr.Read()) {
        Write-Output "$k => Cnt: $($rdr.GetValue(0)) | Sum: $($rdr.GetValue(1))"
    }
    $rdr.Close()
}
$conn.Close()
"""

with open('find_filters.ps1', 'w', encoding='utf-8') as f:
    f.write(ps_script)

res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "find_filters.ps1"], capture_output=True, text=True)
print(res.stdout)
