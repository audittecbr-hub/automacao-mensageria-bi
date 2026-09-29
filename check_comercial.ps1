$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT TOP 25
    C.CctCodigo,
    C.CctCliente,
    C.CctUnidadeFranqCom,
    C.CctUnidadeFranqOp,
    C.CctModeloNegocio,
    PTC.PtcProduto,
    M.ModCodigo,
    ISNULL(P.SppPerc, F.SpfPerc) AS perc_comercial
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
LEFT JOIN PROJECT_TIPOS_CONTRATOS PTC WITH (NOLOCK) ON PTC.PtcCodigo = C.CctTpContrato
LEFT JOIN SMART_UNIDADES_MODELOS M WITH (NOLOCK) ON M.ModUnidade = C.CctUnidadeFranqCom AND M.ModModelo = C.CctModeloNegocio AND M.ModTipoContrato = 1
LEFT JOIN SMART_UNIDADES_MODELOS_PERC_PROD P WITH (NOLOCK) ON P.SppModCodigo = M.ModCodigo AND P.SppProduto = PTC.PtcProduto
LEFT JOIN SMART_UNIDADES_MODELOS_PERC_FIXO F WITH (NOLOCK) ON F.SpfModCodigo = M.ModCodigo
WHERE C.CctTpContrato = 4
ORDER BY C.CctCodigo DESC;
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
