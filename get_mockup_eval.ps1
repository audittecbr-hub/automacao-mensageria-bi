
$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:54175")
$model = $server.Databases[0].Model

$query = "EVALUATE ROW('Mockup', [Mockup_Honorarios_Matriz])"
$cmd = $server.Connection.CreateCommand()
$cmd.CommandText = $query
$rdr = $cmd.ExecuteReader()
if ($rdr.Read()) {
    $html = $rdr.GetString(0)
    [System.IO.File]::WriteAllText("mockup_eval.html", $html, [System.Text.Encoding]::UTF8)
    Write-Output "SAVED_MOCKUP_EVAL"
}
$server.Disconnect()
