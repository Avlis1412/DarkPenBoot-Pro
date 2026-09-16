# ===========================================================
# DARKPENBOOT PRO - check.ps1
# Verificacao completa do projeto
# ===========================================================

Write-Host ""
Write-Host "===========================================================" -ForegroundColor Magenta
Write-Host "  DarkPenBoot Pro - Verificacao do Projeto" -ForegroundColor Magenta
Write-Host "===========================================================" -ForegroundColor Magenta
Write-Host ""

$global:ok = 0
$global:fail = 0

function Check-File {
    param([string]$Path, [string]$Description)
    if (Test-Path $Path) {
        $size = (Get-Item $Path).Length
        if ($size -gt 0) {
            Write-Host "  [OK]    $Description ($size bytes)" -ForegroundColor Green
            $global:ok++
        } else {
            Write-Host "  [VAZIO] $Description - arquivo vazio!" -ForegroundColor Yellow
            $global:fail++
        }
    } else {
        Write-Host "  [FALTA] $Description" -ForegroundColor Red
        $global:fail++
    }
}

function Check-Folder {
    param([string]$Path, [string]$Description)
    if (Test-Path $Path -PathType Container) {
        Write-Host "  [OK]    $Description" -ForegroundColor Green
        $global:ok++
    } else {
        Write-Host "  [FALTA] $Description" -ForegroundColor Red
        $global:fail++
    }
}

Write-Host "[1] Arquivos Python" -ForegroundColor Cyan
Check-File "DarkPenBoot_PRO1.py" "App desktop (Tkinter)"
Check-File "darkpenboot_kivy.py" "App mobile (Kivy)"
Write-Host ""

Write-Host "[2] Arquivos de Build" -ForegroundColor Cyan
Check-File "build.ps1" "Build Windows"
Check-File "build.sh" "Build Linux/macOS"
Check-File "buildozer.spec" "Config Android"
Write-Host ""

Write-Host "[3] Arquivos Nix" -ForegroundColor Cyan
Check-File "flake.nix" "Build Nix"
Check-File "shell.nix" "Ambiente dev"
Check-File "nix\android.nix" "Build Android Nix"
Write-Host ""

Write-Host "[4] Documentacao" -ForegroundColor Cyan
Check-File "README.md" "README principal"
Check-File "README_BUILD.md" "Guia de build"
Check-File "CHANGELOG.md" "Historico de versoes"
Check-File "LICENSE" "Licenca MIT"
Check-File "docs\ARQUITETURA.md" "Documentacao tecnica"
Check-File "docs\NIXOS.md" "Filosofia NixOS"
Write-Host ""

Write-Host "[5] Metadata" -ForegroundColor Cyan
Check-File "pyproject.toml" "Metadata Python"
Check-File "requirements.txt" "Dependencias"
Check-File ".gitignore" "Git ignore"
Write-Host ""

Write-Host "[6] CI/CD" -ForegroundColor Cyan
Check-File ".github\workflows\build.yml" "Build automatico"
Check-File ".github\workflows\release.yml" "Release automatica"
Write-Host ""

Write-Host "[7] Testes" -ForegroundColor Cyan
Check-File "tests\__init__.py" "Package init"
Check-File "tests\test_checksums.py" "Testes de hash"
Check-File "tests\test_config.py" "Testes de config"
Check-File "tests\test_download.py" "Testes de download"
Write-Host ""

Write-Host "[8] Estrutura de pastas" -ForegroundColor Cyan
Check-Folder ".github" "Pasta .github"
Check-Folder ".github\workflows" "Pasta workflows"
Check-Folder "docs" "Pasta docs"
Check-Folder "tests" "Pasta tests"
Check-Folder "nix" "Pasta nix"
Write-Host ""

Write-Host "[9] Git" -ForegroundColor Cyan
if (Test-Path ".git") {
    Write-Host "  [OK]    Repositorio Git inicializado" -ForegroundColor Green
    $global:ok++

    $branch = git rev-parse --abbrev-ref HEAD 2>$null
    Write-Host "  [INFO]  Branch atual: $branch" -ForegroundColor Gray

    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host "  [OK]    Remote: $remote" -ForegroundColor Green
        $global:ok++
    } else {
        Write-Host "  [FALTA] Remote origin nao configurado" -ForegroundColor Red
        $global:fail++
    }

    $tag = git describe --tags --abbrev=0 2>$null
    if ($tag) {
        Write-Host "  [OK]    Ultima tag: $tag" -ForegroundColor Green
        $global:ok++
    } else {
        Write-Host "  [INFO]  Nenhuma tag encontrada" -ForegroundColor Gray
    }

    $status = git status --porcelain 2>$null
    if ($status) {
        $count = ($status | Measure-Object).Count
        Write-Host "  [INFO]  $count arquivo(s) nao commitado(s)" -ForegroundColor Yellow
    } else {
        Write-Host "  [OK]    Working tree limpo" -ForegroundColor Green
        $global:ok++
    }
} else {
    Write-Host "  [FALTA] Repositorio Git nao inicializado" -ForegroundColor Red
    $global:fail++
}
Write-Host ""

Write-Host "[10] Ferramentas do sistema" -ForegroundColor Cyan
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pyVer = python --version 2>&1
    Write-Host "  [OK]    Python: $pyVer" -ForegroundColor Green
    $global:ok++
} else {
    Write-Host "  [FALTA] Python nao instalado" -ForegroundColor Red
    $global:fail++
}

if (Get-Command git -ErrorAction SilentlyContinue) {
    $gitVer = git --version 2>&1
    Write-Host "  [OK]    Git: $gitVer" -ForegroundColor Green
    $global:ok++
} else {
    Write-Host "  [FALTA] Git nao instalado" -ForegroundColor Red
    $global:fail++
}

$pyi = python -m pip show pyinstaller 2>$null
if ($pyi) {
    Write-Host "  [OK]    PyInstaller instalado" -ForegroundColor Green
    $global:ok++
} else {
    Write-Host "  [INFO]  PyInstaller nao instalado (sera instalado no build)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "===========================================================" -ForegroundColor Magenta
Write-Host "  RESULTADO" -ForegroundColor Magenta
Write-Host "===========================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "  OK:     $global:ok" -ForegroundColor Green
if ($global:fail -gt 0) {
    Write-Host "  Falhas: $global:fail" -ForegroundColor Red
} else {
    Write-Host "  Falhas: $global:fail" -ForegroundColor Green
}
Write-Host ""

if ($global:fail -eq 0) {
    Write-Host "  [SUCESSO] Tudo OK! Projeto pronto!" -ForegroundColor Green
} elseif ($global:fail -le 2) {
    Write-Host "  [ATENCAO] Falhas menores - verificar acima" -ForegroundColor Yellow
} else {
    Write-Host "  [ERRO] Multiplas falhas - verificar acima" -ForegroundColor Red
}
Write-Host ""

Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "  1. Baixar .exe do GitHub Actions" -ForegroundColor White
Write-Host "  2. Testar localmente" -ForegroundColor White
Write-Host "  3. Criar Release oficial" -ForegroundColor White
Write-Host ""

Write-Host "Links uteis:" -ForegroundColor Cyan
Write-Host "  Actions:  https://github.com/Avlis1412/DarkPenBoot-Pro/actions" -ForegroundColor Gray
Write-Host "  Releases: https://github.com/Avlis1412/DarkPenBoot-Pro/releases" -ForegroundColor Gray
Write-Host ""