# ═══════════════════════════════════════════════════════════════
#  DarkPenBoot Pro — Build do APK via GitHub Actions
#  Uso: .\build_apk.ps1
# ═══════════════════════════════════════════════════════════════
$ErrorActionPreference = "Continue"
$ProjectPath = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
Set-Location $ProjectPath

function Write-Head($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Write-Ok($t)   { Write-Host "[OK] $t" -ForegroundColor Green }
function Write-Warn($t) { Write-Host "[!] $t" -ForegroundColor Yellow }
function Write-Err($t)  { Write-Host "[X] $t" -ForegroundColor Red }

Write-Head "1. Verificando pre-requisitos"

# Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Err "git nao encontrado no PATH."
    exit 1
}
Write-Ok "git: $(git --version)"

# buildozer.spec
if (-not (Test-Path "buildozer.spec")) {
    Write-Err "buildozer.spec nao encontrado."
    exit 1
}
Write-Ok "buildozer.spec encontrado"

# main.py
if (-not (Test-Path "main.py")) {
    Write-Err "main.py nao encontrado (entry point do Buildozer)."
    exit 1
}
Write-Ok "main.py encontrado (entry point)"

# darkpenboot_kivy.py
if (-not (Test-Path "darkpenboot_kivy.py")) {
    Write-Err "darkpenboot_kivy.py nao encontrado."
    exit 1
}
Write-Ok "darkpenboot_kivy.py encontrado"

# Workflow
$wf = ".github\workflows\build.yml"
if (-not (Test-Path $wf)) {
    Write-Warn "Workflow $wf nao encontrado. Procure por outro *.yml em .github\workflows\"
    Get-ChildItem ".github\workflows\" -Filter "*.yml" -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "   -> $($_.Name)"
    }
} else {
    Write-Ok "Workflow: $wf"
}

Write-Head "2. Ajustando buildozer.spec"

# Backup
if (-not (Test-Path "buildozer.spec.bak")) {
    Copy-Item "buildozer.spec" "buildozer.spec.bak"
    Write-Ok "Backup criado: buildozer.spec.bak"
} else {
    Write-Warn "Backup ja existia (nao sobrescrevi)"
}

$spec = Get-Content "buildozer.spec" -Raw -Encoding UTF8

# 2.1 - Garantir source.dir
if ($spec -notmatch '(?m)^source\.dir\s*=') {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nsource.dir = ."
    Write-Ok "source.dir = . adicionado"
} else {
    Write-Ok "source.dir ja configurado"
}

# 2.2 - Garantir include_exts (apenas py, kv, png, jpg, atlas)
if ($spec -match '(?m)^source\.include_exts\s*=(.*)$') {
    $old = $Matches[1].Trim()
    $new = "py,kv,png,jpg,atlas,ttf,json"
    $spec = $spec -replace '(?m)^source\.include_exts\s*=.*$', "source.include_exts = $new"
    Write-Ok "include_exts: '$old' -> '$new'"
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nsource.include_exts = py,kv,png,jpg,atlas,ttf,json"
    Write-Ok "include_exts adicionado"
}

# 2.3 - Excluir desktop, launcher, venvs, git, etc.
$excludes = "DESKTOP,LAUNCHER,LAUNCHER_CONFIG,BUILD,SPECS,LEGACY,FIXES,TOOLS,SCRIPTS,darkpenboot_kivy.py.orig"
$excludeList = @(
    "venv312", "venv312_mobile", "kivy_venv", ".git", ".github",
    "build", "dist", ".buildozer", "__pycache__", "*.pyc",
    "DarkPenBoot_PRO1.py", "DPB_Launcher.py", "analyze_code.py",
    "scan_clean.ps1", "scan_report.txt",
    "run_desktop.ps1", "run_mobile.ps1", "setup_mobile.ps1",
    "docs", "tests", "releases", ".vscode",
    "*.spec.bak", "buildozer.spec.bak",
    "requirements.txt", "requirements-mobile.txt",
    "pyproject.toml", "DarkPenBoot.spec",
    ".launcher_config.json", "launch.json",
    "build.sh", "CHANGELOG.md", "README_BUILD.md"
) -join ","

if ($spec -match '(?m)^source\.exclude_patterns\s*=(.*)$') {
    $old = $Matches[1].Trim()
    $spec = $spec -replace '(?m)^source\.exclude_patterns\s*=.*$', "source.exclude_patterns = $excludeList"
    Write-Ok "exclude_patterns atualizado"
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nsource.exclude_patterns = $excludeList"
    Write-Ok "exclude_patterns adicionado"
}

# 2.4 - Forçar license do Android
if ($spec -notmatch 'android\.accept_sdk_license') {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nandroid.accept_sdk_license = True"
    Write-Ok "android.accept_sdk_license = True adicionado"
}

# 2.5 - Garantir p4a branch develop (resolve a maioria dos erros)
if ($spec -match '(?m)^p4a\.branch\s*=') {
    $spec = $spec -replace '(?m)^p4a\.branch\s*=.*$', "p4a.branch = develop"
    Write-Ok "p4a.branch = develop"
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`np4a.branch = develop"
    Write-Ok "p4a.branch = develop adicionado"
}

# 2.6 - Garantir arquitetura única (arm64-v8a)
if ($spec -match '(?m)^android\.archs\s*=') {
    $spec = $spec -replace '(?m)^android\.archs\s*=.*$', "android.archs = arm64-v8a"
    Write-Ok "android.archs = arm64-v8a"
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nandroid.archs = arm64-v8a"
    Write-Ok "android.archs = arm64-v8a adicionado"
}

# Salva
[System.IO.File]::WriteAllText("$PWD\buildozer.spec", $spec, [System.Text.UTF8Encoding]::new($false))
Write-Ok "buildozer.spec salvo (UTF-8 sem BOM)"

Write-Head "3. Estado do git"
git status --short

Write-Head "4. Commit e push"

$msg = Read-Host "Mensagem do commit (Enter = 'build: gerar APK')"
if ([string]::IsNullOrWhiteSpace($msg)) { $msg = "build: gerar APK" }

git add -A
if ($LASTEXITCODE -ne 0) {
    Write-Err "git add falhou"
    exit 1
}

git commit -m $msg
if ($LASTEXITCODE -ne 0) {
    Write-Warn "git commit retornou $LASTEXITCODE (nada novo? continuando...)"
}

git push
if ($LASTEXITCODE -ne 0) {
    Write-Err "git push falhou. Verifique credenciais."
    exit 1
}
Write-Ok "Push concluido"

Write-Head "5. Proximos passos"
Write-Host ""
Write-Host "1. Aguarde ~15-25 minutos" -ForegroundColor Yellow
Write-Host "2. Abra: https://github.com/Avlis1412/DarkPenBoot-Pro/actions" -ForegroundColor Cyan
Write-Host "3. Clique no build mais recente (Android)" -ForegroundColor Yellow
Write-Host "4. Role ate 'Artifacts' e baixe 'darkpenboot-apk'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Se falhar, abra o log e procure por:" -ForegroundColor Yellow
Write-Host "   - 'ERROR' ou 'FAILED'" -ForegroundColor Gray
Write-Host "   - 'Buildozer failed to execute'" -ForegroundColor Gray
Write-Host "   - 'sdkmanager' ou 'NDK'" -ForegroundColor Gray
Write-Host ""
Write-Ok "Script concluido."
