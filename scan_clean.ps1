# ═══════════════════════════════════════════════════════════════
#  DarkPenBoot Pro — Varredura e Limpeza (v2 - sem aspas aninhadas)
# ═══════════════════════════════════════════════════════════════
$ErrorActionPreference = "Continue"
$ProjectPath = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
Set-Location $ProjectPath
$ReportFile = Join-Path $ProjectPath "scan_report.txt"

function Size-Of($bytes) {
    if ($bytes -ge 1GB) { return ('{0:N2} GB' -f ($bytes / 1GB)) }
    if ($bytes -ge 1MB) { return ('{0:N2} MB' -f ($bytes / 1MB)) }
    if ($bytes -ge 1KB) { return ('{0:N2} KB' -f ($bytes / 1KB)) }
    return ('{0} B' -f $bytes)
}

function Rel-Path($fullPath) {
    return $fullPath.Substring($ProjectPath.Length).TrimStart('\')
}

'DarkPenBoot Pro - Scan Report - ' + (Get-Date) | Out-File $ReportFile -Encoding utf8

# ── 1. ESTRUTURA RAIZ ──
Write-Host ""
Write-Host "=== 1. Estrutura da pasta raiz ===" -ForegroundColor Cyan
$rootItems = Get-ChildItem -Force | Sort-Object PSIsContainer, Name
foreach ($item in $rootItems) {
    if ($item.PSIsContainer) {
        $sum = (Get-ChildItem -Recurse -Force -ErrorAction SilentlyContinue $item.FullName | Measure-Object -Property Length -Sum).Sum
        if (-not $sum) { $sum = 0 }
        Write-Host ('  [DIR]  {0,-32} {1,>10}' -f $item.Name, (Size-Of $sum))
        ('[DIR]  ' + $item.Name + ' - ' + (Size-Of $sum)) | Out-File $ReportFile -Append -Encoding utf8
    } else {
        Write-Host ('  [FILE] {0,-32} {1,>10}' -f $item.Name, (Size-Of $item.Length))
        ('[FILE] ' + $item.Name + ' - ' + (Size-Of $item.Length)) | Out-File $ReportFile -Append -Encoding utf8
    }
}

# ── 2. ARQUIVOS .PY DO PROJETO ──
Write-Host ""
Write-Host "=== 2. Arquivos Python do projeto ===" -ForegroundColor Cyan
$pyFiles = Get-ChildItem -Recurse -File -Filter "*.py" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\(venv312|venv312_mobile|kivy_venv|\.git|__pycache__|build|dist|\.buildozer)\\' }
foreach ($f in $pyFiles) {
    $rel = Rel-Path $f.FullName
    Write-Host ('  {0,-50} {1,>10}' -f $rel, (Size-Of $f.Length))
    ($rel + ' - ' + (Size-Of $f.Length)) | Out-File $ReportFile -Append -Encoding utf8
}

# ── 3. CANDIDATOS À LIMPEZA ──
Write-Host ""
Write-Host "=== 3. Candidatos a limpeza ===" -ForegroundColor Cyan
$toDelete = New-Object System.Collections.ArrayList

# 3a. Cache
foreach ($d in @("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache")) {
    Get-ChildItem -Recurse -Directory -Filter $d -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch '\\venv312' } |
        ForEach-Object { [void]$toDelete.Add($_.FullName) }
}

# 3b. Build do Buildozer
foreach ($d in @("build", "dist", ".buildozer")) {
    $p = Join-Path $ProjectPath $d
    if (Test-Path $p) { [void]$toDelete.Add($p) }
}

# 3c. Venv antigo
$oldVenv = Join-Path $ProjectPath "kivy_venv"
if (Test-Path $oldVenv) { [void]$toDelete.Add($oldVenv) }

# 3d. .pyc soltos
Get-ChildItem -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\venv312' } |
    ForEach-Object { [void]$toDelete.Add($_.FullName) }

# 3e. Scripts temporarios
foreach ($f in @("fix_encoding.py", "fix_bom.py", "fix_build_v5.py", "check.ps1")) {
    $p = Join-Path $ProjectPath $f
    if (Test-Path $p) { [void]$toDelete.Add($p) }
}

# 3f. Arquivos com nomes suspeitos
$suspicious = Get-ChildItem -Force -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '^(h origin|olver erro|Untitled)' }
foreach ($f in $suspicious) { [void]$toDelete.Add($f.FullName) }

# 3g. Nix
foreach ($f in @("flake.nix", "shell.nix")) {
    $p = Join-Path $ProjectPath $f
    if (Test-Path $p) { [void]$toDelete.Add($p) }
}
$nixDir = Join-Path $ProjectPath "nix"
if (Test-Path $nixDir) { [void]$toDelete.Add($nixDir) }

# 3h. .launcher_profiles
$lp = Join-Path $ProjectPath ".launcher_profiles"
if (Test-Path $lp) { [void]$toDelete.Add($lp) }

# 3i. Deploy (opcional)
$deployFiles = New-Object System.Collections.ArrayList
foreach ($f in @("deploy.ps1", "deploy.py", "build.ps1")) {
    $p = Join-Path $ProjectPath $f
    if (Test-Path $p) { [void]$deployFiles.Add($p) }
}

# ── Mostrar ──
Write-Host ""
Write-Host "Itens que serao REMOVIDOS:" -ForegroundColor Yellow
$totalSize = 0
foreach ($p in $toDelete) {
    if (Test-Path $p) {
        $item = Get-Item $p -Force -ErrorAction SilentlyContinue
        if ($item) {
            if ($item.PSIsContainer) {
                $sz = (Get-ChildItem -Recurse -Force -ErrorAction SilentlyContinue $item.FullName | Measure-Object -Property Length -Sum).Sum
                if (-not $sz) { $sz = 0 }
            } else {
                $sz = $item.Length
            }
            $totalSize += $sz
            $rel = Rel-Path $p
            Write-Host ('  - {0,-55} {1,>10}' -f $rel, (Size-Of $sz)) -ForegroundColor Gray
        }
    }
}
Write-Host ""
Write-Host "Scripts de deploy (opcional):" -ForegroundColor Yellow
foreach ($p in $deployFiles) {
    $item = Get-Item $p -Force
    $rel = Rel-Path $p
    Write-Host ('  ? {0,-55} {1,>10}' -f $rel, (Size-Of $item.Length)) -ForegroundColor Yellow
}
Write-Host ""
Write-Host ('Espaco total a liberar: ~' + (Size-Of $totalSize)) -ForegroundColor Yellow

# ── 4. CRITICOS PRESERVADOS ──
Write-Host ""
Write-Host "=== 4. Arquivos CRITICOS (PRESERVADOS) ===" -ForegroundColor Green
$keep = @(
    "buildozer.spec", "main.py", "DarkPenBoot_PRO1.py", "darkpenboot_kivy.py",
    "DPB_Launcher.py", "requirements.txt", "requirements-mobile.txt",
    "LICENSE", "README.md", "README_BUILD.md", "CHANGELOG.md",
    "pyproject.toml", ".gitignore", ".gitattributes",
    "run_desktop.ps1", "run_mobile.ps1", "setup_mobile.ps1", "scan_clean.ps1"
)
foreach ($f in $keep) {
    $p = Join-Path $ProjectPath $f
    if (Test-Path $p) { Write-Host ('  [OK] ' + $f) -ForegroundColor Green }
}
Write-Host '  [OK] .github\workflows\*.yml (Buildozer)' -ForegroundColor Green
Write-Host '  [OK] assets\* (icones APK)' -ForegroundColor Green
Write-Host '  [OK] .vscode\launch.json' -ForegroundColor Green
Write-Host '  [OK] venv312\ + venv312_mobile\ (ambientes)' -ForegroundColor Green

# ── 5. LIMPEZA ──
Write-Host ""
Write-Host "=== 5. Limpeza ===" -ForegroundColor Cyan
$resp = Read-Host ('Remover ' + $toDelete.Count + ' item(ns)? [s/N]')
if ($resp -notmatch '^[sSyY]') {
    Write-Host "Cancelado." -ForegroundColor Yellow
    Write-Host ('Relatorio salvo em: ' + $ReportFile) -ForegroundColor Cyan
    exit 0
}

$respDeploy = Read-Host "Remover tambem deploy.ps1/deploy.py/build.ps1? [s/N]"
if ($respDeploy -match '^[sSyY]') {
    foreach ($p in $deployFiles) { [void]$toDelete.Add($p) }
}

$removed = 0
$freed = 0
foreach ($p in $toDelete) {
    if (-not (Test-Path $p)) { continue }
    try {
        $item = Get-Item $p -Force -ErrorAction SilentlyContinue
        if ($item.PSIsContainer) {
            $sz = (Get-ChildItem -Recurse -Force -ErrorAction SilentlyContinue $item.FullName | Measure-Object -Property Length -Sum).Sum
            if (-not $sz) { $sz = 0 }
            Remove-Item -Recurse -Force $p -ErrorAction Stop
        } else {
            $sz = $item.Length
            Remove-Item -Force $p -ErrorAction Stop
        }
        $removed++
        $freed += $sz
        $rel = Rel-Path $p
        Write-Host ('  [DEL] ' + $rel) -ForegroundColor DarkGray
    } catch {
        Write-Host ('  [ERR] ' + $p + ' - ' + $_) -ForegroundColor Red
    }
}

# ── 6. RESUMO ──
Write-Host ""
Write-Host "=== 6. Resumo ===" -ForegroundColor Cyan
Write-Host ('Itens removidos: ' + $removed) -ForegroundColor Green
Write-Host ('Espaco liberado: ' + (Size-Of $freed)) -ForegroundColor Green
Write-Host ''
Write-Host ('Relatorio: ' + $ReportFile) -ForegroundColor Cyan
Write-Host ''
Write-Host 'Estado final da pasta raiz:' -ForegroundColor Yellow
Get-ChildItem -Force | Sort-Object PSIsContainer, Name | ForEach-Object {
    $t = if ($_.PSIsContainer) { '[DIR] ' } else { '[FILE]' }
    Write-Host ('  ' + $t + ' ' + $_.Name)
}
Write-Host ''
Write-Host 'Projeto limpo. Pronto para o build do APK.' -ForegroundColor Green
