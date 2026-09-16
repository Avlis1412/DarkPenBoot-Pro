# ==============================================================
# DarkPenBoot Pro - Deploy Completo
# Uso:
#   .\deploy.ps1
#   .\deploy.ps1 -Build
#   .\deploy.ps1 -NoPush
#   .\deploy.ps1 -DryRun
# ==============================================================
param(
    [switch]$Build,
    [switch]$NoPush,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$Version  = "3.6.1"
$Date     = (Get-Date).ToString("yyyy-MM-dd")
$Branch   = "main"
$Remote   = "origin"
$MainPy   = "DarkPenBoot_PRO1.py"
$RepoUrl  = "https://github.com/Avlis1412/DarkPenBoot-Pro"
$ReleasesDir = "releases"

function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Ok($m)  { Write-Host "[OK]   $m" -ForegroundColor Green }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m) { Write-Host "[ERR]  $m" -ForegroundColor Red }
function Head($m){
    Write-Host ""
    Write-Host ("=" * 62)
    Write-Host "  $m"
    Write-Host ("=" * 62)
}

Head "DARKPENBOOT PRO - DEPLOY v$Version"

if (-not (Test-Path $MainPy)) { Err "$MainPy nao encontrado"; exit 1 }
if (-not (Test-Path ".git"))  { Err ".git nao encontrado";     exit 1 }
if (-not (Test-Path $ReleasesDir)) {
    if (-not $DryRun) { New-Item -ItemType Directory -Path $ReleasesDir | Out-Null }
    Info "Criado: $ReleasesDir/"
}

# 1. LIMPEZA
Head "[1/5] LIMPEZA"
$baks = Get-ChildItem -Path . -Filter "*.bak_*" -File -ErrorAction SilentlyContinue
if ($baks.Count -gt 0) {
    if (-not $DryRun) { $baks | Remove-Item -Force }
    Ok "$($baks.Count) backups removidos"
} else { Info "Nenhum backup" }

$temps = @("diag.py","diag2.py","fix_final.py","fix_final_v361.py",
           "fix_tk_methods.py","kivy_patcher_v361.py","patcher_v360.py",
           "patcher_consolidado_v361.py",".launcher_config.json")
$n = 0
foreach ($t in $temps) {
    if (Test-Path $t) { if (-not $DryRun) { Remove-Item $t -Force }; $n++ }
}
if ($n -gt 0) { Ok "$n temporarios removidos" } else { Info "Nenhum temporario" }

# 2. BUILD
$ExeVersioned = "$ReleasesDir\DarkPenBoot_PRO_$Version.exe"
if ($Build) {
    Head "[2/5] BUILD"
    if (-not (python -m pip show pyinstaller 2>$null)) {
        Warn "Instalando PyInstaller..."
        if (-not $DryRun) { python -m pip install --quiet pyinstaller }
    }
    if (Test-Path "build") { if (-not $DryRun) { Remove-Item "build" -Recurse -Force } }
    if (Test-Path "dist")  { if (-not $DryRun) { Remove-Item "dist"  -Recurse -Force } }
    if (Test-Path "DarkPenBoot.spec") {
        Info "Usando DarkPenBoot.spec"
        if (-not $DryRun) { pyinstaller --clean --noconfirm DarkPenBoot.spec | Out-Null }
    } else {
        Info "Build automatico"
        $icon = if (Test-Path "assets/icon.ico") { "--icon=assets/icon.ico" } else { "" }
        if (-not $DryRun) {
            pyinstaller --onefile --windowed `
                --name "DarkPenBoot_PRO_$Version" `
                $icon $MainPy | Out-Null
        }
    }
    if (Test-Path "dist") {
        $exe = Get-ChildItem "dist" -Filter "*.exe" | Select-Object -First 1
        if ($exe) {
            if (-not $DryRun) { Copy-Item $exe.FullName $ExeVersioned -Force }
            $sizeMb = [math]::Round($exe.Length / 1MB, 2)
            Ok "EXE: $ExeVersioned ($sizeMb MB)"
        }
    }
} else {
    Head "[2/5] BUILD - ignorado (use -Build)"
}

# 3. README
Head "[3/5] README"
$releaseFiles = @()
if (Test-Path $ReleasesDir) {
    $releaseFiles = Get-ChildItem $ReleasesDir -Filter "*.exe" | Sort-Object Name -Descending
}

$L = @()
$L += "# DarkPenBoot Pro"
$L += ""
$L += "**Criador Profissional de Pendrives Bootaveis Universais**"
$L += ""
$L += "Windows . Linux . macOS . Android (Termux) . OTG Mobile"
$L += ""
$L += "![Versao](https://img.shields.io/badge/versao-$Version-blue)"
$L += "![Python](https://img.shields.io/badge/python-3.8+-yellow)"
$L += ""
$L += "**Autor:** Adriano Rodrigues da Silva"
$L += "**GitHub:** [@Avlis1412](https://github.com/Avlis1412)"
$L += ""
$L += "---"
$L += ""
$L += "## Novidades v$Version ($Date)"
$L += ""
$L += "### Adicionado"
$L += "- Varredura shell universal: ``_scan_shell_all_platforms()``"
$L += "- Constantes visuais v$Version"
$L += "- Helpers de cor (``_blend_color``, ``_lighten_hex``, ``_darken_hex``)"
$L += ""
$L += "### Modificado"
$L += "- ``refresh_drives()`` - pulso neon + oscilacao do orb"
$L += "- ``_do_identify()`` - fallback shell se API falhar"
$L += "- ``_do_diskpart()`` - revarredura se perder o alvo"
$L += ""
$L += "### Corrigido"
$L += "- ``SyntaxError`` em ``download_with_fallback``"
$L += ""
$L += "---"
$L += ""
$L += "## Executaveis Disponiveis"
$L += ""

if ($releaseFiles.Count -gt 0) {
    $L += "| Versao | Arquivo | Tamanho |"
    $L += "|--------|---------|---------|"
    foreach ($f in $releaseFiles) {
        $mb = [math]::Round($f.Length / 1MB, 2)
        $L += "| **$($f.BaseName)** | ``$($f.Name)`` | $mb MB |"
    }
    $L += ""
    $L += "> Download: [$RepoUrl/tree/$Branch/$ReleasesDir]($RepoUrl/tree/$Branch/$ReleasesDir)"
} else {
    $L += "_Nenhuma versao compilada. Rode ``.\deploy.ps1 -Build``._"
}
$L += ""
$L += "---"
$L += ""
$L += "## Recursos"
$L += ""
$L += "| Recurso | Descricao |"
$L += "|---------|-----------|"
$L += "| Multi-FS | NTFS, FAT32, exFAT, ext4/3/2, JHFS+, APFS |"
$L += "| 7 temas | Matrix, Crimson, Nord, Cyberpunk, Monokai, Light, Soft Dark |"
$L += "| ~35 distros | Debian, Ubuntu, Fedora, Arch, NixOS, etc |"
$L += "| Hashes | SHA256, SHA512, SHA1, MD5, SHA3-256, BLAKE2b |"
$L += "| Downloads | Fallback curl -> wget -> urllib + mirrors |"
$L += "| Recuperacao USB | Chkdsk, MBR rebuild, format FS |"
$L += "| Mobile | Kivy + Buildozer (Android) |"
$L += ""
$L += "---"
$L += ""
$L += "## Como usar"
$L += ""
$L += "### 1. Instalar dependencias"
$L += "``````bash"
$L += "pip install -r requirements.txt"
$L += "``````"
$L += ""
$L += "### 2. Executar"
$L += "``````bash"
$L += "python $MainPy"
$L += "``````"
$L += ""
$L += "### 3. Build e deploy"
$L += "``````powershell"
$L += ".\deploy.ps1 -Build      # compila EXE versionado"
$L += ".\deploy.ps1             # so docs + push"
$L += "``````"
$L += ""

$newReadme = $L -join "`n"
if ($DryRun) {
    Warn "[DRY] README.md seria atualizado ($($L.Count) linhas)"
} else {
    Set-Content -Path "README.md" -Value $newReadme -Encoding UTF8
    Ok "README.md ($($L.Count) linhas)"
}

# 4. COMMIT
Head "[4/5] COMMIT"
if ($DryRun) {
    Warn "[DRY] git add -u; git add README.md deploy.ps1 deploy.py .gitignore"
    if ($Build) { Warn "[DRY] git add -f $ReleasesDir" }
    Warn "[DRY] git commit"
} else {
    git add -u
    foreach ($f in @("README.md","deploy.ps1","deploy.py",".gitignore")) {
        if (Test-Path $f) { git add $f }
    }
    if ($Build -and (Test-Path $ReleasesDir)) {
        git add -f $ReleasesDir
        Info "Force add: $ReleasesDir/"
    }
    $staged = git diff --cached --name-only
    if (-not $staged) {
        Warn "Nada para commitar"
    } else {
        $msg = @(
            "deploy(v$Version): README + build versionado",
            "",
            "- README.md: tabela de versoes",
            "- releases/DarkPenBoot_PRO_$Version.exe",
            "- deploy.ps1: pipeline PowerShell",
            "",
            "Data: $Date"
        ) -join "`n"
        git commit -m $msg | Out-Null
        Ok "Commit realizado"
    }
}

# 5. PUSH
Head "[5/5] PUSH"
if ($NoPush) {
    Info "Push ignorado (-NoPush)"
} elseif ($DryRun) {
    Warn "[DRY] git push $Remote $Branch"
} else {
    git push $Remote $Branch
    if ($LASTEXITCODE -eq 0) { Ok "Push concluido" }
    else { Warn "Push falhou" }
}

Write-Host ""
Write-Host ("=" * 62)
Write-Host "  OK - Deploy v$Version concluido!"
Write-Host ("=" * 62)
Write-Host "  Repositorio: $RepoUrl"

if (Test-Path $ReleasesDir) {
    $rels = Get-ChildItem $ReleasesDir -Filter "*.exe"
    if ($rels.Count -gt 0) {
        Write-Host ""
        Write-Host "  EXEs em releases/:"
        foreach ($r in $rels) {
            $mb = [math]::Round($r.Length / 1MB, 2)
            Write-Host "    - $($r.Name)  ($mb MB)"
        }
    }
}
Write-Host ""
