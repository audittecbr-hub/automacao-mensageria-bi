$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT 
    'O' AS tipo_origem,
    CAST(A.JOB AS VARCHAR(50)) AS numero_contrato,
    CAST(A.CODIGO_UNIDADE AS VARCHAR(20)) AS unidade_id,
    dbo.Func_JOB_CALCULAR_HONORARIO(A.JOB, 'O') AS honorario
FROM PROJECT_QBERT_JOBS A WITH (NOLOCK)
WHERE A.JOB = '380'

UNION ALL

SELECT 
    'C' AS tipo_origem,
    CAST(C.CctCodigo AS VARCHAR(50)) AS numero_contrato,
    CAST(CASE 
        WHEN C.CctUnidadeFranqCom IS NOT NULL AND C.CctUnidadeFranqCom <> 2153 THEN C.CctUnidadeFranqCom
        WHEN PU.UNIDADE_ID IS NOT NULL THEN PU.UNIDADE_ID
        ELSE ISNULL(C.CctUnidadeFranqCom, C.CctUnidadeFranqOp)
    END AS VARCHAR(20)) AS unidade_id,
    dbo.Func_JOB_CALCULAR_HONORARIO(CAST(C.CctCodigo AS VARCHAR(10)), 'C') AS honorario
FROM PROJECT_CP_CONTRATO C WITH (NOLOCK)
OUTER APPLY (
    SELECT TOP 1 UNIDADE_ID 
    FROM vw_participantes_unidades PU WITH (NOLOCK) 
    WHERE PU.PARTICIPANTE_ID = C.CctCliente
    ORDER BY PU.ModAtivo DESC, PU.VIGENCIA_INICIO DESC
) PU
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
