$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$t = $model.Tables["medidas_html"]
$results = @()
foreach ($m in $t.Measures) {
    if ($m.Name -like "HTML_Detalhamento*") {
        $lines = $m.Expression -split "`n"
        $filterLines = @()
        $formatLines = @()
        foreach ($l in $lines) {
            if ($l -like "*FILTER(*" -or $l -like "*CONCATENATEX(*" -or $l -like "*td-valor*") {
                $filterLines += $l.Trim()
            }
        }
        $results += [PSCustomObject]@{
            Measure = $m.Name
            Snippet = ($filterLines -join " || ")
        }
    }
}
$results | Format-List | Out-File -FilePath "all_detalhamentos_summary.txt" -Encoding UTF8
Write-Output "SUMMARY_WRITTEN"
$server.Disconnect()
