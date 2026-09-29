$dll = "C:\Program Files\On-premises data gateway\FabricIntegrationRuntime\5.0\Gateway\Microsoft.AnalysisServices.Tabular.dll"
[System.Reflection.Assembly]::LoadFrom($dll) | Out-Null
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("localhost:60593")
$model = $server.Databases[0].Model

$t = $model.Tables["medidas_html"]

foreach ($name in @("HTML_Detalhamento_Iniciais", "HTML_Detalhamento_Restituicao", "HTML_Detalhamento_Aprovados", "HTML_Detalhamento_Perdidos", "HTML_Detalhamento_Nao_Aprovados")) {
    $m = $t.Measures[$name]
    if ($m) {
        Write-Output "=== $name ==="
        Write-Output $m.Expression
    }
}

$server.Disconnect()
