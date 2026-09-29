$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$query = @"
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.vw_powerbi_job_repasse')) AS ViewDef
"@
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandText = $query
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dt = New-Object System.Data.DataTable
$adapter.Fill($dt) | Out-Null
$conn.Close()
$dt.Rows[0]["ViewDef"] | Out-File -FilePath "c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\vw_def.txt" -Encoding UTF8
Write-Host "View definition written."
