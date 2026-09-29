$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = @"
SELECT TOP 5
    PARTICIPANTE_ID,
    UNIDADE_ID,
    UNIDADE_NOME,
    PERC_FRANQUEADO
FROM vw_powerbi_participantes_unidades WITH (NOLOCK)
WHERE UNIDADE_ID = 95
"@
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "Part: $($r['PARTICIPANTE_ID']) | Unit: $($r['UNIDADE_ID']) | Name: $($r['UNIDADE_NOME']) | PercFranq: $($r['PERC_FRANQUEADO'])"
}
$r.Close()

$conn.Close()
