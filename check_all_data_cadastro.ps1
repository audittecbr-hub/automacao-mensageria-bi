$dll1 = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Core.dll"
$dll2 = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
$dll3 = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.AdomdClient.dll"

if (Test-Path $dll1) { [System.Reflection.Assembly]::LoadFrom($dll1) | Out-Null }
if (Test-Path $dll2) { [System.Reflection.Assembly]::LoadFrom($dll2) | Out-Null }
if (Test-Path $dll3) { [System.Reflection.Assembly]::LoadFrom($dll3) | Out-Null }

$connStr = "Data Source=localhost:62446;"
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection($connStr)
$conn.Open()

$daxQuery = @"
EVALUATE
VAR vFiltered = 
    FILTER(
        'public metas_bruto',
        'public metas_bruto'[data_lancamento] >= DATE(2026, 8, 1)
        && (
            CONTAINSSTRING(UPPER('public metas_bruto'[bandeira]), "TAX")
            || CONTAINSSTRING(UPPER('public metas_bruto'[bandeira]), "CORP")
        )
    )
VAR vBase = 
    ADDCOLUMNS(
        vFiltered,
        "JobVal", 'public metas_bruto'[numero_contrato],
        "DtCadastroJob",
            VAR curJob = 'public metas_bruto'[numero_contrato]
            RETURN
            CALCULATE(
                MAX('vw_powerbi_job_repasse'[DATA_CADASTRO]),
                FILTER('vw_powerbi_job_repasse', 'vw_powerbi_job_repasse'[JOB] = curJob)
            ),
        "DtCadastroPU",
            VAR curCnpj = 'public metas_bruto'[cnpj_cpf]
            RETURN
            CALCULATE(
                MAX('vw_participantes_unidades'[VIGENCIA_INICIO]),
                FILTER('vw_participantes_unidades', 
                    (NOT ISBLANK('vw_participantes_unidades'[PARTICIPANTE_CPF]) && 'vw_participantes_unidades'[PARTICIPANTE_CPF] = curCnpj) || 
                    (NOT ISBLANK('vw_participantes_unidades'[CNPJ_UNIDADE]) && 'vw_participantes_unidades'[CNPJ_UNIDADE] = curCnpj)
                )
            )
    )
VAR vFinal = 
    ADDCOLUMNS(
        vBase,
        "DtCadastroFinal", COALESCE([DtCadastroJob], [DtCadastroPU])
    )
RETURN
SELECTCOLUMNS(
    vFinal,
    "ID", 'public metas_bruto'[id],
    "CodigoOmie", 'public metas_bruto'[codigo_lancamento_omie],
    "DataLancamento", 'public metas_bruto'[data_lancamento],
    "Bandeira", 'public metas_bruto'[bandeira],
    "CNPJ", 'public metas_bruto'[cnpj_cpf],
    "Cliente", 'public metas_bruto'[razao_social],
    "Categoria", 'public metas_bruto'[descricao_cat],
    "ValorBruto", 'public metas_bruto'[valor_bruto],
    "ContratoJob", 'public metas_bruto'[numero_contrato],
    "DtCadastroJob", [DtCadastroJob],
    "DtCadastroPU", [DtCadastroPU],
    "DtCadastroFinal", [DtCadastroFinal]
)
"@

$cmd = $conn.CreateCommand()
$cmd.CommandText = $daxQuery
$adapter = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()

Write-Output "Total launches analyzed (Tax & Corporate, Ago/Set 2026): $($dt.Rows.Count)"

$comJob = 0
$comJobComData = 0
$comJobSemData = 0
$semJob = 0

foreach ($r in $dt.Rows) {
    $job = [string]$r["[ContratoJob]"]
    $dtCad = $r["[DtCadastroFinal]"]
    if ([string]::IsNullOrWhiteSpace($job)) {
        $semJob++
    } else {
        $comJob++
        if ($dtCad -eq [DBNull]::Value -or [string]::IsNullOrWhiteSpace([string]$dtCad)) {
            $comJobSemData++
            Write-Output "Job sem data cadastro: Job='$job' | Cliente='$($r["[Cliente]"])' | Valor=$($r["[ValorBruto]"])"
        } else {
            $comJobComData++
        }
    }
}

Write-Output "`n=== RESUMO ==="
Write-Output "Lançamentos com Job: $comJob"
Write-Output "Lançamentos com Job e COM Data Cadastro: $comJobComData"
Write-Output "Lançamentos com Job e SEM Data Cadastro: $comJobSemData"
Write-Output "Lançamentos sem Job (Contrato em branco): $semJob"
