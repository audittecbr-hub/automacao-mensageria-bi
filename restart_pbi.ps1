$targetPid = 24300
Stop-Process -Id $targetPid -Force -ErrorAction SilentlyContinue
Write-Host "Process $targetPid stopped."

Start-Sleep -Seconds 2

$pbipPath = "C:\Users\cristhofer.maciel.GRUPOSTUDIO\Downloads\Ranking_Metas_V2.pbip"
Start-Process $pbipPath
Write-Host "Started $pbipPath"
