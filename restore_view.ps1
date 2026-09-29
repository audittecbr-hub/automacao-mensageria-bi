$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$viewSql = [System.IO.File]::ReadAllText("c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\current_view_def.sql", [System.Text.Encoding]::UTF8)

# Replace CREATE VIEW with ALTER VIEW
$alterSql = $viewSql.Replace("CREATE VIEW [dbo].[vw_powerbi_job_repasse]", "ALTER VIEW [dbo].[vw_powerbi_job_repasse]")

$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 120
$cmd.CommandText = $alterSql
$cmd.ExecuteNonQuery() | Out-Null
$conn.Close()
Write-Host "View vw_powerbi_job_repasse RESTORED to exact original definition on SQL Server!"
