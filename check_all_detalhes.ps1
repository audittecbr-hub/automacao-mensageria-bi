$tabularDll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($tabularDll) | Out-Null

$adomdDll = "C:\Program Files\On-premises data gateway\Microsoft.AnalysisServices.AdomdClient.dll"
[System.Reflection.Assembly]::LoadFrom($adomdDll) | Out-Null

$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection("Data Source=localhost:54175")
$conn.Open()

foreach ($table in $model.Tables) {
    foreach ($m in $table.Measures) {
        if ($m.Name.StartsWith("HTML_Detalhamento_")) {
            $query = "EVALUATE ROW(`"Test`", LEN([$($m.Name)]))"
            try {
                $cmd = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdCommand($query, $conn)
                $rdr = $cmd.ExecuteReader()
                if ($rdr.Read()) {
                    Write-Output "OK: $($m.Name) | Length: $($rdr.GetValue(0))"
                }
                $rdr.Close()
            } catch {
                Write-Output "ERROR in $($m.Name): $($_.Exception.Message)"
            }
        }
    }
}

$conn.Close()
$server.Disconnect()
