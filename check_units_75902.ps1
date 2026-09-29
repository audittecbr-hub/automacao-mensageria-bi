$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

Write-Output "--- Checking UNIDADE 1660 in vw_powerbi_participantes_unidades ---"
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT * FROM vw_powerbi_participantes_unidades WHERE UNIDADE_ID = 1660"
$r = $cmd.ExecuteReader()
while ($r.Read()) {
    Write-Output ("UNIDADE_ID: " + $r["UNIDADE_ID"] + " | PARTICIPANTE_ID: " + $r["PARTICIPANTE_ID"] + " | UNIDADE_NOME: " + $r["UNIDADE_NOME"] + " | PARTICIPANTE_RAZAO_SOCIAL: " + $r["PARTICIPANTE_RAZAO_SOCIAL"])
}
$r.Close()

Write-Output "`n--- Checking PARTICIPANTE 376 in vw_powerbi_participantes_unidades ---"
$cmd2 = $conn.CreateCommand()
$cmd2.CommandText = "SELECT * FROM vw_powerbi_participantes_unidades WHERE PARTICIPANTE_ID = 376"
$r2 = $cmd2.ExecuteReader()
while ($r2.Read()) {
    Write-Output ("UNIDADE_ID: " + $r2["UNIDADE_ID"] + " | PARTICIPANTE_ID: " + $r2["PARTICIPANTE_ID"])
}
if (!$r2.HasRows) { Write-Output "No rows found for PARTICIPANTE_ID = 376 in vw_powerbi_participantes_unidades" }
$r2.Close()

Write-Output "`n--- Checking PARTICIPANTE 23566 in vw_powerbi_participantes_unidades ---"
$cmd3 = $conn.CreateCommand()
$cmd3.CommandText = "SELECT * FROM vw_powerbi_participantes_unidades WHERE PARTICIPANTE_ID = 23566"
$r3 = $cmd3.ExecuteReader()
while ($r3.Read()) {
    Write-Output ("UNIDADE_ID: " + $r3["UNIDADE_ID"] + " | PARTICIPANTE_ID: " + $r3["PARTICIPANTE_ID"] + " | UNIDADE_NOME: " + $r3["UNIDADE_NOME"])
}
$r3.Close()

$conn.Close()
