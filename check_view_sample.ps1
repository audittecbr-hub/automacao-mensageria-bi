$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

$cmd = $conn.CreateCommand()
$cmd.CommandText = @"
SELECT 
    JOB,
    PERC_HONORARIOS_JOB,
    PERC_HONORARIOS_FRANQUEADO,
    PERC_FRANQUEADO,
    UNIDADE_ID,
    UNIDADE_NOME
FROM dbo.vw_powerbi_job_repasse WITH (NOLOCK)
WHERE JOB IN ('84087-C4', '85265-T', '83389-C1', '87420')
"@
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Host "JOB: $($r['JOB']) | HonJob: $($r['PERC_HONORARIOS_JOB']) | HonFranq: $($r['PERC_HONORARIOS_FRANQUEADO']) | Franq: $($r['PERC_FRANQUEADO']) | Unit: $($r['UNIDADE_ID']) - $($r['UNIDADE_NOME'])"
}
$r.Close()

$conn.Close()
