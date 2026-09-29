$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT TOP 20
    C.CctCodigo,
    C.CctCodigoAux,
    C.CctCliente,
    C.CctTpContrato,
    C.CctUnidadeFranqCom,
    C.CctUnidadeFranqOp,
    C.CctModeloNegocio,
    C.CctObs,
    C.CctDataCadastro,
    dbo.Func_JOB_CALCULAR_HONORARIO(CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS honorario
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
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
