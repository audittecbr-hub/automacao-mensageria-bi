$connStr = "Server=192.168.2.34;Database=STUDIO_FISCAL;Integrated Security=True;TrustServerCertificate=True;"
$conn = New-Object System.Data.SqlClient.SqlConnection($connStr)
$conn.Open()

# Query all jobs from the newly fixed view
$cmd = $conn.CreateCommand()
$cmd.CommandTimeout = 120
$cmd.CommandText = "SELECT * FROM dbo.vw_powerbi_job_repasse"
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter($cmd)
$dtJobs = New-Object System.Data.DataTable
$adapter.Fill($dtJobs) | Out-Null
$conn.Close()

Write-Output "Jobs in view: $($dtJobs.Rows.Count)"

$csvPath = "c:\Users\cristhofer.maciel.GRUPOSTUDIO\.gemini\antigravity\scratch\automacao-mensageria-bi\vw_jobs_dump.csv"

# Export dtJobs to CSV with UTF8
$dtJobs | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
Write-Output "CSV exported to $csvPath"
