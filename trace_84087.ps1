$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = @"
SELECT 
    A.JOB,
    A.CODIGO_CLIENTE,
    A.CODIGO_PRODUTO,
    A.CODIGO_UNIDADE,
    A.DATA_RECEBIMENTO,
    A.MODELO_NEGOCIO,
    U.UniNome,
    U.UniRetemImposto
FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
LEFT JOIN SMART_UNIDADES U WITH (NOLOCK) ON U.UniCodigo = A.CODIGO_UNIDADE
WHERE A.JOB = '84087-C4'
"@
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "Job: $($r['JOB']) | Cli: $($r['CODIGO_CLIENTE']) | Prod: $($r['CODIGO_PRODUTO']) | Unit: $($r['CODIGO_UNIDADE']) - $($r['UniNome']) | Model: $($r['MODELO_NEGOCIO']) | DataRec: $($r['DATA_RECEBIMENTO'])"
}
$r.Close()

# Let's check models for unit 95
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = @"
SELECT ModCodigo, ModUnidade, ModModelo, ModTipoContrato, ModAtivo, ModData, ModDataInativo, ModDataTermino
FROM SMART_UNIDADES_MODELOS WITH (NOLOCK)
WHERE ModUnidade = 95
ORDER BY ModAtivo DESC, ModData DESC
"@
$r2 = $cmd2.ExecuteReader()
while ($r2.Read()) {
    Write-Host "ModCodigo: $($r2['ModCodigo']) | ModAtivo: $($r2['ModAtivo']) | ModData: $($r2['ModData']) | Inativo: $($r2['ModDataInativo'])"
}
$r2.Close()

# Let's check products and fixo for unit 95
$cmd3 = $conn.CreateCommand()
$cmd3.CommandText = @"
SELECT SpfModCodigo, SpfPerc, SpfCadData
FROM SMART_UNIDADES_MODELOS_PERC_FIXO WITH (NOLOCK)
WHERE SpfModCodigo IN (SELECT ModCodigo FROM SMART_UNIDADES_MODELOS WHERE ModUnidade = 95)
"@
$r3 = $cmd3.ExecuteReader()
while ($r3.Read()) {
    Write-Host "FIXO: ModCodigo: $($r3['SpfModCodigo']) | SpfPerc: $($r3['SpfPerc'])"
}
$r3.Close()

# Let's check vw_participantes_unidades
$cmd4 = $conn.CreateCommand()
$cmd4.CommandText = @"
SELECT UNIDADE_ID, PERC_FRANQUEADO
FROM vw_participantes_unidades WITH (NOLOCK)
WHERE UNIDADE_ID = 95
"@
$r4 = $cmd4.ExecuteReader()
while ($r4.Read()) {
    Write-Host "PU: UNIDADE_ID: $($r4['UNIDADE_ID']) | PERC_FRANQUEADO: $($r4['PERC_FRANQUEADO'])"
}
$r4.Close()

$conn.Close()
