$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Output "--- Searching 75902 in PROJECT_QBERT_JOBS ---"
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM PROJECT_QBERT_JOBS WHERE JOB LIKE '%75902%'"
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    for ($i=0; $i -lt $r.FieldCount; $i++) {
        Write-Output ($r.GetName($i) + ': ' + $r.GetValue($i))
    }
    Write-Output "-------------------"
}
$r.Close()

Write-Output "`n--- Searching 75902 in PROJECT_CP_CONTRATO ---"
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "SELECT * FROM PROJECT_CP_CONTRATO WHERE CctCodigo LIKE '%75902%'"
$r2 = $cmd2.ExecuteReader()
while ($r2.Read()) {
    for ($i=0; $i -lt $r2.FieldCount; $i++) {
        Write-Output ($r2.GetName($i) + ': ' + $r2.GetValue($i))
    }
    Write-Output "-------------------"
}
$r2.Close()

Write-Output "`n--- Searching 75902 in PROJECT_MOVIMENTO ---"
$cmd3 = $conn.CreateCommand()
$cmd3.CommandText = "
SELECT M.* 
FROM PROJECT_MOVIMENTO M
INNER JOIN PROJECT_QBERT_JOBS J ON J.CODIGO = M.PmvJob
WHERE J.JOB LIKE '%75902%'
"
$r3 = $cmd3.ExecuteReader()
while ($r3.Read()) {
    Write-Output ("PmvJob: " + $r3["PmvJob"] + " | PmvArea: " + $r3["PmvArea"] + " | PmvExcluido: " + $r3["PmvExcluido"] + " | PmvSaidaData: " + $r3["PmvSaidaData"] + " | PmvEntradaData: " + $r3["PmvEntradaData"])
}
$r3.Close()

$conn.Close()
