$ErrorActionPreference = "Stop"
$ProjectPath = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
$VenvName    = "venv312_mobile"
$VenvPath    = Join-Path $ProjectPath $VenvName
$VenvPython  = Join-Path $VenvPath "Scripts\python.exe"

Set-Location $ProjectPath

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Configurando Ambiente Mobile (Kivy)" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "[1/4] Verificando Python 3.12..." -ForegroundColor Yellow
$py312Exists = $false
try {
    $ver = & py -3.12 --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $py312Exists = $true
        Write-Host "[OK] Python 3.12 encontrado: $ver" -ForegroundColor Green
    }
} catch { }

if (-not $py312Exists) {
    Write-Host "[!] Python 3.12 nao encontrado. Instalando via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.12 --exact --scope user --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] Falha ao instalar Python 3.12." -ForegroundColor Red
        Write-Host "Baixe manualmente: https://www.python.org/downloads/release/python-31210/" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] Python 3.12 instalado. Feche e reabra o PowerShell e rode de novo." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "[2/4] Criando ambiente virtual '$VenvName'..." -ForegroundColor Yellow
if (Test-Path $VenvPath) {
    Write-Host "[!] Pasta '$VenvName' ja existe. Removendo..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $VenvPath
}
& py -3.12 -m venv $VenvName
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao criar venv." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Ambiente criado: $VenvPath" -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] Instalando Kivy (pode demorar)..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install "kivy[base]"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao instalar Kivy." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Kivy instalado." -ForegroundColor Green

Write-Host ""
Write-Host "[4/4] Verificando..." -ForegroundColor Yellow
& $VenvPython -c "import kivy; print('Kivy', kivy.__version__)"
Write-Host ""
Write-Host "CONCLUIDO! Interpreter: .\$VenvName\Scripts\python.exe" -ForegroundColor Green
