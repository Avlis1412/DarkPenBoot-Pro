$ProjectPath = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
$PythonExe   = Join-Path $ProjectPath "venv312\Scripts\python.exe"
Set-Location $ProjectPath
Write-Host ""
Write-Host "=== DarkPenBoot Desktop ===" -ForegroundColor Cyan
& $PythonExe "DarkPenBoot_PRO1.py"
