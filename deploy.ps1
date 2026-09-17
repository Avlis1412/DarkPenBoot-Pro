# ═══════════════════════════════════════════════════════════════
#  DarkPenBoot Pro — Build + Git + Monitoramento
#  Uso: .\deploy.ps1
# ═══════════════════════════════════════════════════════════════
$ErrorActionPreference = "Continue"
$ProjectPath = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
$Repo        = "Avlis1412/DarkPenBoot-Pro"
Set-Location $ProjectPath

function Write-Head($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Write-Ok($t)   { Write-Host "[OK] $t" -ForegroundColor Green }
function Write-Warn($t) { Write-Host "[!] $t" -ForegroundColor Yellow }
function Write-Err($t)  { Write-Host "[X] $t" -ForegroundColor Red }
function Ask-Yes($q)    { $r = Read-Host "$q [s/N]"; return ($r -match '^[sSyY]') }

# ═══════════════════════════════════════════════════════════════
Write-Head "1. Limpeza de arquivos temporarios"

$tmpFiles = @(
    "scan_report.txt", "buildozer.spec.bak",
    "analyze_code.py", "fix_bom.py",
    "fix_encoding.py", "fix_build_v5.py"
)
foreach ($f in $tmpFiles) {
    $p = Join-Path $ProjectPath $f
    if (Test-Path $p) {
        Remove-Item $p -Force -ErrorAction SilentlyContinue
        Write-Host "  [DEL] $f" -ForegroundColor DarkGray
    }
}

# Remove __pycache__ e build/dist
Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\venv' } |
    ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }

foreach ($d in @("build", "dist", ".buildozer")) {
    $p = Join-Path $ProjectPath $d
    if (Test-Path $p) {
        Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  [DEL] $d/" -ForegroundColor DarkGray
    }
}
Write-Ok "Limpeza concluida"

# ═══════════════════════════════════════════════════════════════
Write-Head "2. Corrigir buildozer.spec"

if (-not (Test-Path "buildozer.spec")) {
    Write-Err "buildozer.spec nao encontrado!"
    exit 1
}

$spec = Get-Content "buildozer.spec" -Raw -Encoding UTF8

# 2.1 log_level = 1 (evita corte de log)
$spec = $spec -replace '(?m)^log_level\s*=\s*\d+\s*$', 'log_level = 1'
if ($spec -notmatch '(?m)^log_level\s*=') {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nlog_level = 1"
}
Write-Ok "log_level = 1"

# 2.2 source.dir
if ($spec -notmatch '(?m)^source\.dir\s*=') {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nsource.dir = ."
}
Write-Ok "source.dir = ."

# 2.3 include_exts
$spec = $spec -replace '(?m)^source\.include_exts\s*=.*$', 'source.include_exts = py,kv,png,jpg,atlas,ttf,json'

# 2.4 exclude_patterns (so o essencial)
$excludeList = "venv312,venv312_mobile,kivy_venv,.git,.github,build,dist,.buildozer,__pycache__,*.pyc,DarkPenBoot_PRO1.py,DPB_Launcher.py,analyze_code.py,scan_clean.ps1,scan_report.txt,run_desktop.ps1,run_mobile.ps1,setup_mobile.ps1,deploy.ps1,docs,tests,releases,.vscode,*.spec.bak,buildozer.spec.bak,requirements.txt,requirements-mobile.txt,pyproject.toml,DarkPenBoot.spec,.launcher_config.json,launch.json,build.sh,CHANGELOG.md,README_BUILD.md"

if ($spec -match '(?m)^source\.exclude_patterns\s*=') {
    $spec = $spec -replace '(?m)^source\.exclude_patterns\s*=.*$', "source.exclude_patterns = $excludeList"
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nsource.exclude_patterns = $excludeList"
}
Write-Ok "exclude_patterns atualizado"

# 2.5 accept_sdk_license
if ($spec -notmatch 'android\.accept_sdk_license') {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nandroid.accept_sdk_license = True"
}
Write-Ok "android.accept_sdk_license = True"

# 2.6 p4a branch
if ($spec -match '(?m)^p4a\.branch\s*=') {
    $spec = $spec -replace '(?m)^p4a\.branch\s*=.*$', 'p4a.branch = develop'
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`np4a.branch = develop"
}
Write-Ok "p4a.branch = develop"

# 2.7 android archs
if ($spec -match '(?m)^android\.archs\s*=') {
    $spec = $spec -replace '(?m)^android\.archs\s*=.*$', 'android.archs = arm64-v8a'
} else {
    $spec = $spec -replace '(?m)^(\[app\])', "`$1`nandroid.archs = arm64-v8a"
}
Write-Ok "android.archs = arm64-v8a"

[System.IO.File]::WriteAllText("$PWD\buildozer.spec", $spec, [System.Text.UTF8Encoding]::new($false))
Write-Ok "buildozer.spec salvo (UTF-8 sem BOM)"

# ═══════════════════════════════════════════════════════════════
Write-Head "3. Corrigir workflow GitHub Actions"

$wf = ".github\workflows\build.yml"
if (-not (Test-Path $wf)) {
    $candidates = Get-ChildItem ".github\workflows\" -Filter "*.yml" -ErrorAction SilentlyContinue
    if ($candidates) {
        $wf = $candidates[0].FullName
        Write-Warn "Workflow principal: $wf"
    } else {
        Write-Err "Nenhum workflow encontrado em .github\workflows\"
        exit 1
    }
}

$wfContent = Get-Content $wf -Raw -Encoding UTF8

# 3.1 Python 3.11 fixo
$wfContent = $wfContent -replace "python-version:\s*['""]?[\d.]+['""]?", "python-version: '3.11'"
Write-Ok "Python 3.11 fixado"

# 3.2 Adicionar aceitacao automatica de licenses do Android
if ($wfContent -notmatch 'sdkmanager --licenses') {
    $licenseStep = @"

      - name: Accept Android Licenses
        if: matrix.os == 'ubuntu-latest'
        run: |
          mkdir -p `$ANDROID_HOME/cmdline-tools/latest/bin
          yes | `$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses || true
"@
    # Insere antes do passo do Buildozer
    $wfContent = $wfContent -replace '(\s*- name: Build with Buildozer)', "$licenseStep`$1"
    Write-Ok "Step 'Accept Android Licenses' adicionado"
}

# 3.3 Cache v8
$wfContent = $wfContent -replace 'buildozer-v\d+', 'buildozer-v8'
Write-Ok "Cache atualizado para v8"

[System.IO.File]::WriteAllText("$((Resolve-Path $wf).Path)", $wfContent, [System.Text.UTF8Encoding]::new($false))

# ═══════════════════════════════════════════════════════════════
Write-Head "4. Verificar sintaxe Python"

$pyFiles = @("main.py", "darkpenboot_kivy.py")
foreach ($f in $pyFiles) {
    if (Test-Path $f) {
        $result = & ".\venv312_mobile\Scripts\python.exe" -m py_compile $f 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Ok "$f compila OK"
        } else {
            Write-Err "$f tem erro de sintaxe:"
            Write-Host $result -ForegroundColor Red
            if (-not (Ask-Yes "Continuar mesmo assim?")) { exit 1 }
        }
    }
}

# ═══════════════════════════════════════════════════════════════
Write-Head "5. Git status"

git status --short | Out-Host
$changes = git status --short
if (-not $changes) {
    Write-Warn "Nenhuma mudanca para commitar."
    if (Ask-Yes "Forcar novo build mesmo assim?") {
        git commit --allow-empty -m "build: trigger manual"
    } else {
        exit 0
    }
}

# ═══════════════════════════════════════════════════════════════
Write-Head "6. Commit e push"

$defaultMsg = "build: correcoes de buildozer.spec e workflow para Android"
$msg = Read-Host "Mensagem do commit (Enter = '$defaultMsg')"
if ([string]::IsNullOrWhiteSpace($msg)) { $msg = $defaultMsg }

git add -A
git commit -m $msg
if ($LASTEXITCODE -ne 0) {
    Write-Warn "git commit retornou $LASTEXITCODE"
}

Write-Host "Fazendo push para origin/main..." -ForegroundColor Yellow
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Err "Push falhou. Verifique credenciais com: git config --list"
    exit 1
}
Write-Ok "Push concluido"

# ═══════════════════════════════════════════════════════════════
Write-Head "7. Iniciar monitoramento do build"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Warn "gh (GitHub CLI) nao instalado. Instale para monitorar:"
    Write-Host "  winget install GitHub.cli" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Ou abra manualmente:" -ForegroundColor White
    Write-Host "  https://github.com/$Repo/actions" -ForegroundColor Cyan
    exit 0
}

# Aguarda 5 segundos pro GitHub detectar o push
Start-Sleep -Seconds 5

Write-Host "Buscando build em execucao..." -ForegroundColor Yellow
$runs = gh run list --repo $Repo --limit 3 --json databaseId,status,conclusion,name,createdAt | ConvertFrom-Json
$current = $runs | Where-Object { $_.status -in @("in_progress", "queued", "pending") } | Select-Object -First 1

if (-not $current) {
    Write-Warn "Nenhum build em execucao detectado ainda."
    Write-Host "  Aguarde alguns segundos e verifique:" -ForegroundColor Gray
    Write-Host "  https://github.com/$Repo/actions" -ForegroundColor Cyan
    exit 0
}

Write-Ok "Build #$($current.databaseId) iniciado"
Write-Host "  URL: https://github.com/$Repo/actions/runs/$($current.databaseId)" -ForegroundColor Cyan
Write-Host ""

if (Ask-Yes "Monitorar em tempo real? (pode demorar ~20 min)") {
    Write-Host "Pressione Ctrl+C para parar o monitoramento." -ForegroundColor Gray
    gh run watch $current.databaseId --repo $Repo --exit-status
    $exitCode = $LASTEXITCODE

    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Ok "Build SUCESSO! Baixando APK..."
        $artifactsDir = Join-Path $ProjectPath "_artifacts"
        New-Item -ItemType Directory -Path $artifactsDir -Force | Out-Null
        gh run download $current.databaseId --repo $Repo --dir $artifactsDir
        Write-Ok "Artefatos baixados em: $artifactsDir"
        Get-ChildItem $artifactsDir -Recurse -File | ForEach-Object {
            Write-Host "  $($_.FullName)" -ForegroundColor White
        }
    } else {
        Write-Err "Build falhou. Para analisar:"
        Write-Host "  .\analisar_log_ci.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Acompanhe em:" -ForegroundColor White
    Write-Host "  https://github.com/$Repo/actions/runs/$($current.databaseId)" -ForegroundColor Cyan
}

Write-Host ""
Write-Ok "Script concluido."
