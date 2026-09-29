
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$query = @"

EVALUATE
ROW(
    // Aprovados
    "Aprovados_All", [Honorários aprovados],
    "Aprovados_RT12", CALCULATE([Honorários aprovados], vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    "Aprovados_RT12_and_MovRange", CALCULATE(
        [Honorários aprovados], 
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),

    // Negociação
    "Negociacao_All", [Honorário negociação],
    "Negociacao_RT12", CALCULATE([Honorário negociação], vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    "Negociacao_RT12_and_MovRange", CALCULATE(
        [Honorário negociação], 
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),

    // Perdidos
    "Perdidos_All", [Honorários perdidos],
    "Perdidos_RT12", CALCULATE([Honorários perdidos], vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    "Perdidos_RT12_and_MovRange", CALCULATE(
        [Honorários perdidos], 
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),

    // Não Aprovados
    "NaoAprov_All", [Honorários não aprovados],
    "NaoAprov_RT12", CALCULATE([Honorários não aprovados], vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    "NaoAprov_RT12_and_MovRange", CALCULATE(
        [Honorários não aprovados], 
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),

    // Encontrados
    "Encontrados_All", [Honorários encontrados],
    "Encontrados_RT12", CALCULATE([Honorários encontrados], vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    "Encontrados_RT12_and_MovRange", CALCULATE(
        [Honorários encontrados], 
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    ),

    // Apresentados
    "Apresentados_All", [Honorários apresentados],
    "Apresentados_RT12", CALCULATE([Honorários apresentados], vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12)),
    "Apresentados_RT12_and_MovRange", CALCULATE(
        [Honorários apresentados], 
        vw_powerbi_relatorio_aprovacao[DATA_RT] >= DATE(2026, 6, 12),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] >= DATE(2026, 6, 1),
        vw_powerbi_relatorio_aprovacao[DATA_MOV_ANTERIOR] <= DATE(2026, 12, 31)
    )
)

"@

$cmd = $server.Connection.CreateCommand()
$cmd.CommandText = $query
$rdr = $cmd.ExecuteReader()
$dt = New-Object System.Data.DataTable
$dt.Load($rdr)
$dt | Format-List | Out-File -FilePath "dax_filter_comparison.txt" -Encoding UTF8
$server.Disconnect()
