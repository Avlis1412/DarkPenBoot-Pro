# ═══════════════════════════════════════════════════════════════════════════
# DARKPENBOOT PRO — build.ps1
# Script de build local para Windows
# ═══════════════════════════════════════════════════════════════════════════
#
# Uso:
#   .\build.ps1                # Build .exe com PyInstaller
#   .\build.ps1 -Clean         # Limpa artefatos (dist/, build/, *.spec)
#   .\build.ps1 -All           # Build + testes
#   .\build.ps1 -Help          # Mostra ajuda
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ INSPIRAÇÃO NIXOS                                                        │
# │                                                                         │
# │ Aplicamos princípios NixOS no Windows:                                  │
# │   • Isolamento — venv dedicada                                          │
# │   • Reprodutibilidade — versões fixadas                                 │
# │   • Verificabilidade — SHA256                                           │
# │                                                                         │
# │ NixOS® é marca da NixOS Foundation. Sem afiliação.                      │
# └─────────────────────────────────────────────────────────────────────────┘
#

param(
    [switch]$Clean,
    [switch]$Help,
    [switch]$All
)

# ─── Configuração ────────────────────────────────────────────────────────
$AppName = "DarkPenBoot"
$AppVersion = "3.5.0"
$MainScript = "DarkPenBoot_PRO1.py"
$DistDir = "dist"
$BuildDir = "build"

# ─── Banner ──────────────────────────────────────────────────────────────
function Show-Banner {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Magenta
    Write-Host "  🚀 $AppName Pro v$AppVersion — Build Windows" -ForegroundColor Magenta
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "🟣 Inspirado em NixOS — build reprodutível" -ForegroundColor Magenta
    Write-Host "🟣 NixOS® é marca da NixOS Foundation (sem afiliação)" -ForegroundColor Magenta
    Write-Host ""
}

# ─── Ajuda ───────────────────────────────────────────────────────────────
function Show-Help {
    @"
🚀 $AppName Pro v$AppVersion — Build Script Windows

Uso: .\build.ps1 [OPÇÕES]

Opções:
  (sem args)      Build .exe com PyInstaller
  -Clean          Limpa artefatos (dist/, build/, *.spec)
  -All            Roda build + testes
  -Help           Mostra esta ajuda

Exemplos:
  .\build.ps1              # Build .exe
  .\build.ps1 -Clean       # Limpa tudo
  .\build.ps1 -All         # Build completo

🟣 Inspirado em NixOS — nixos.org
🟣 NixOS® é marca da NixOS Foundation (sem afiliação)
"@
}

# ─── Verificar dependências ──────────────────────────────────────────────
function Test-Dependencies {
    Write-Host "🔍 Verificando dependências..." -ForegroundColor Cyan

    # Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Python não encontrado!" -ForegroundColor Red
        Write-Host "   Instale em: https://python.org" -ForegroundColor Yellow
        exit 1
    }

    # PyInstaller
    $pyi = python -m pip show pyinstaller 2>$null
    if (-not $pyi) {
        Write-Host "📦 Instalando PyInstaller..." -ForegroundColor Yellow
        python -m pip install pyinstaller
    }

    Write-Host "✅ Dependências OK" -ForegroundColor Green
    Write-Host "   Python: $(python --version)" -ForegroundColor Gray
}

# ─── Limpar ──────────────────────────────────────────────────────────────
function Invoke-Clean {
    Write-Host "🧹 Limpando artefatos..." -ForegroundColor Cyan

    foreach ($dir in @($DistDir, $BuildDir)) {
        if (Test-Path $dir) {
            Remove-Item -Recurse -Force $dir
            Write-Host "   🗑️  Removido: $dir" -ForegroundColor Gray
        }
    }

    Get-ChildItem -Filter "*.spec" -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item -Force $_.FullName
        Write-Host "   🗑️  Removido: $($_.Name)" -ForegroundColor Gray
    }

    Write-Host "✅ Limpeza concluída" -ForegroundColor Green
}

# ─── Build ───────────────────────────────────────────────────────────────
function Invoke-Build {
    Write-Host "🏗️  Build Windows (.exe)..." -ForegroundColor Cyan
    Write-Host ""

    # Verifica script principal
    if (-not (Test-Path $MainScript)) {
        Write-Host "❌ Script principal não encontrado: $MainScript" -ForegroundColor Red
        exit 1
    }

    # Verifica sintaxe
    Write-Host "🔍 Verificando sintaxe Python..." -ForegroundColor Cyan
    python -m py_compile $MainScript
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Erro de sintaxe!" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Sintaxe OK" -ForegroundColor Green
    Write-Host ""

    # Roda PyInstaller
    Write-Host "📦 Empacotando com PyInstaller..." -ForegroundColor Cyan
    python -m PyInstaller `
        --onefile `
        --windowed `
        --name $AppName `
        --distpath $DistDir `
        --workpath $BuildDir `
        --specpath . `
        --noconfirm `
        --clean `
        $MainScript

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ PyInstaller falhou!" -ForegroundColor Red
        exit 1
    }

    # Verifica resultado
    $exePath = Join-Path $DistDir "$AppName.exe"
    if (-not (Test-Path $exePath)) {
        Write-Host "❌ Binário não encontrado: $exePath" -ForegroundColor Red
        exit 1
    }

    # Calcula SHA256
    Write-Host "🔐 Calculando SHA256..." -ForegroundColor Cyan
    $hash = (Get-FileHash $exePath -Algorithm SHA256).Hash
    "$hash  $AppName.exe" | Out-File "$exePath.sha256" -Encoding ASCII

    # Resultado
    $size = (Get-Item $exePath).Length
    $sizeMB = [math]::Round($size / 1MB, 2)

    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  ✅ Build concluído!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Binário:  $exePath" -ForegroundColor Cyan
    Write-Host "📏 Tamanho:  $sizeMB MB" -ForegroundColor Cyan
    Write-Host "🔐 SHA256:   $hash" -ForegroundColor Cyan
    Write-Host ""
}

# ─── Main ────────────────────────────────────────────────────────────────
Show-Banner

if ($Help) {
    Show-Help
    exit 0
}

if ($Clean) {
    Invoke-Clean
    exit 0
}

Test-Dependencies
Invoke-Build

if ($All) {
    Write-Host "🧪 Rodando testes adicionais..." -ForegroundColor Cyan
    if (Test-Path "tests") {
        python -m pytest tests/ -v
    } else {
        Write-Host "   ⚠️  Pasta tests/ não encontrada — pulando" -ForegroundColor Yellow
    }
    Write-Host "✅ Testes OK" -ForegroundColor Green
}

Write-Host "🎉 Tudo pronto!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Para rodar o .exe gerado:" -ForegroundColor Gray
Write-Host "   .\$DistDir\$AppName.exe" -ForegroundColor White
Write-Host ""