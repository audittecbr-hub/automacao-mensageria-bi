$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$sql = @"
SELECT
    m.id,
    m.codigo_lancamento_omie,
    CONVERT(VARCHAR(10), m.data_emissao, 103) AS data_emissao,
    CONVERT(VARCHAR(10), m.data_lancamento, 103) AS data_lancamento,
    CONVERT(VARCHAR(10), m.data_vencimento, 103) AS data_vencimento,
    m.bandeira,
    m.cnpj_cpf,
    m.razao_social,
    m.numero_contrato,
    m.descricao_cat,
    m.percentual_categoria,
    m.ccoddep,
    m.percentual_departamento,
    m.descricao_dept,
    m.valor_bruto,
    m.categoria,
    m.situacao,
    m.numero_documento,
    m.numero_documento_fiscal,
    j.JOB AS Job_Encontrado,
    CONVERT(VARCHAR(19), j.DATA_CADASTRO, 120) AS Job_Data_Cadastro,
    j.PERC_HONORARIOS_JOB AS Job_Perc_Honorarios,
    j.UNIDADE_ID AS Job_Unidade_Id,
    j.UNIDADE_NOME AS Job_Unidade_Nome,
    j.PARTICIPANTE_CLIENTE AS Job_Participante_Cliente,
    j.PARTICIPANTE_FRANQUEADO AS Job_Participante_Franqueado,
    j.REDE_DISTRIBUICAO AS Job_Rede_Distribuicao,
    j.REDE_DISTRIBUICAO_OLD AS Job_Rede_Distribuicao_Old
FROM [public metas_bruto] m WITH (NOLOCK)
LEFT JOIN (
    SELECT 
        JOB,
        MAX(DATA_CADASTRO) AS DATA_CADASTRO,
        MAX(PERC_HONORARIOS_JOB) AS PERC_HONORARIOS_JOB,
        MAX(UNIDADE_ID) AS UNIDADE_ID,
        MAX(UNIDADE_NOME) AS UNIDADE_NOME,
        MAX(PARTICIPANTE_CLIENTE) AS PARTICIPANTE_CLIENTE,
        MAX(PARTICIPANTE_FRANQUEADO) AS PARTICIPANTE_FRANQUEADO,
        MAX(REDE_DISTRIBUICAO) AS REDE_DISTRIBUICAO,
        MAX(REDE_DISTRIBUICAO_OLD) AS REDE_DISTRIBUICAO_OLD
    FROM dbo.vw_powerbi_job_repasse WITH (NOLOCK)
    GROUP BY JOB
) j ON j.JOB = m.numero_contrato
WHERE m.data_lancamento >= '2026-08-01'
  AND (
      m.categoria IN ('TAX', 'Corporate')
      OR m.bandeira LIKE '%TAX%'
      OR m.bandeira LIKE '%CORP%'
      OR m.descricao_dept LIKE '%TAX%'
      OR m.descricao_dept LIKE '%CORP%'
      OR m.descricao_dept LIKE '%Repasse%'
      OR m.descricao_dept LIKE '%Franchising%'
  )
ORDER BY m.data_lancamento DESC, m.id DESC
"@

$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 120
$cmd.CommandText = $sql
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()

Write-Output "Total rows retrieved: $($dt.Rows.Count)"

# Convert DataTable to array of hashtables for clean JSON
$rows = @()
foreach ($row in $dt.Rows) {
    $obj = [ordered]@{}
    foreach ($col in $dt.Columns) {
        $val = $row[$col.ColumnName]
        if ($val -eq [DBNull]::Value) {
            $obj[$col.ColumnName] = $null
        } else {
            $obj[$col.ColumnName] = $val
        }
    }
    $rows += $obj
}

$json = ConvertTo-Json -InputObject $rows -Depth 3
$jsonPath = "c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\tax_corp_data.json"
[System.IO.File]::WriteAllText($jsonPath, $json, [System.Text.Encoding]::UTF8)
Write-Output "JSON saved to $jsonPath"
