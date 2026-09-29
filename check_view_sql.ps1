$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = "SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_powerbi_job_repasse'))"
$def = $cmd.ExecuteScalar()
$conn.Close()
Write-Host "View definition length: $($def.Length)"
[System.IO.File]::WriteAllText("c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\current_view_def.sql", $def, [System.Text.Encoding]::UTF8)
Write-Host "Contains CROSS APPLY: $($def.Contains('CROSS APPLY'))"
Write-Host "Contains OUTER APPLY: $($def.Contains('OUTER APPLY'))"
