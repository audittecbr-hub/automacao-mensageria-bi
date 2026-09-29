$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT 
    C.CctCodigo,
    C.CctCliente,
    C.CctTpContrato,
    PTC.PtcProduto,
    PU.UNIDADE_ID,
    M.ModCodigo,
    M.ModModelo,
    M.ModUnidade,
    F.SpfPerc
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN PROJECT_TIPOS_CONTRATOS PTC WITH (NOLOCK) ON PTC.PtcCodigo = C.CctTpContrato
LEFT JOIN VW_POWERBI_PARTICIPANTES_UNIDADES PU WITH (NOLOCK) ON PU.PARTICIPANTE_ID = C.CctCliente
LEFT JOIN SMART_UNIDADES_MODELOS M WITH (NOLOCK) ON M.ModUnidade = PU.UNIDADE_ID AND M.ModTipoContrato = 1
LEFT JOIN SMART_UNIDADES_MODELOS_PERC_FIXO F WITH (NOLOCK) ON F.SpfModCodigo = M.ModCodigo
WHERE C.CctCodigo = 380;
"@
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    $adapter.Fill($dt) | Out-Null
    $dt | Format-Table -AutoSize | Out-String | Write-Host
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
