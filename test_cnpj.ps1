$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
try {
    $conn.Open()
    $cmd = $conn.CreateCommand()
    $cmd.CommandText = @"
SELECT 
    clean_cnpj AS cnpj_cpf,
    CASE 
        WHEN COUNT(DISTINCT UNIDADE_ID) = 0 THEN 'NE'
        WHEN COUNT(DISTINCT UNIDADE_ID) > 1 THEN 'NI'
        ELSE CAST(MAX(UNIDADE_ID) AS VARCHAR(20))
    END AS unidade_id
FROM (
    SELECT 
        U.UNIDADE_ID,
        REPLACE(REPLACE(REPLACE(COALESCE(NULLIF(U.CNPJ_UNIDADE, ''), NULLIF(U.PARTICIPANTE_CPF, ''), NULLIF(P.ParCNPJ, '')), '.', ''), '/', ''), '-', '') AS clean_cnpj
    FROM VW_POWERBI_PARTICIPANTES_UNIDADES U WITH (NOLOCK)
    LEFT JOIN SMART_PARTICIPANTES P WITH (NOLOCK) ON P.ParCodigo = U.PARTICIPANTE_ID
) X
WHERE clean_cnpj IS NOT NULL AND clean_cnpj <> ''
GROUP BY clean_cnpj
"@
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
    $dt = New-Object System.Data.DataTable
    $adapter.Fill($dt) | Out-Null
    Write-Host "Total distinct CNPJs found: " $dt.Rows.Count
    $acs = $dt | Where-Object { $_.cnpj_cpf -like "*65417729000103*" -or $_.cnpj_cpf -like "*65417729000*" }
    $acs | Format-Table -AutoSize | Out-String | Write-Host
} catch {
    Write-Host "Error: " $_.Exception.Message
} finally {
    $conn.Close()
}
