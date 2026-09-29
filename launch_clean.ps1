Stop-Process -Id 27272 -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$pbipPath = "C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.pbip"
Start-Process $pbipPath
Write-Host "Launched $pbipPath clean!"
