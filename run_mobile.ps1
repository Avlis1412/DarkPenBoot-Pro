# ═══════════════════════════════════════════════════════════════
#  DarkPenBoot MOBILE (Kivy) — Execucao automatica
# ═══════════════════════════════════════════════════════════════
$ErrorActionPreference = "Continue"
$ProjectPath = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
$VenvPath    = Join-Path $ProjectPath "venv312"
$PythonExe   = Join-Path $VenvPath "Scripts\python.exe"
$MobileFile  = Join-Path $ProjectPath "darkpenboot_kivy.py"

Set-Location $ProjectPath

Write-Host ""
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host "  DarkPenBoot MOBILE (Kivy) - Runner" -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta

# ── 1. Verificar venv ──
if (-not (Test-Path $PythonExe)) {
    Write-Host "[ERRO] venv312 nao encontrado em: $VenvPath" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python: $PythonExe" -ForegroundColor Green

# ── 2. Verificar Kivy ──
Write-Host ""
Write-Host "[1/2] Verificando Kivy..." -ForegroundColor Cyan
$kivyVer = & $PythonExe -c "import kivy; print(kivy.__version__)" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Kivy NAO instalado. Instalando (pode demorar ~5 min)..." -ForegroundColor Yellow
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install "kivy[base]"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao instalar Kivy." -ForegroundColor Red
        Write-Host "Dica: use Python 3.11 ou 3.12 (3.14 ainda nao suportado pelo Kivy)." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] Kivy instalado." -ForegroundColor Green
} else {
    Write-Host "[OK] Kivy $kivyVer detectado." -ForegroundColor Green
}

# ── 3. Verificar arquivo mobile ──
if (-not (Test-Path $MobileFile)) {
    Write-Host "[ERRO] Arquivo nao encontrado: $MobileFile" -ForegroundColor Red
    exit 1
}

# ── 4. Executar MOBILE ──
Write-Host ""
Write-Host "===============================================" -ForegroundColor Magenta
Write-Host "  Executando DARKPENBOOT MOBILE (Kivy)" -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta

$env:PYTHONPATH          = $ProjectPath
$env:PYTHONIOENCODING    = "utf-8"
$env:KIVY_NO_ARGS        = "1"
$env:KIVY_NO_CONSOLELOG  = "1"
$env:KIVY_LOG_LEVEL      = "warning"

& $PythonExe $MobileFile
Write-Host "[OK] Mobile finalizado." -ForegroundColor Green
