# ==============================================================
# Fix Android build - pyjnius version
# ==============================================================
$ErrorActionPreference = "Stop"

$specPath = "buildozer.spec"

if (-not (Test-Path $specPath)) {
    Write-Host "[ERR] buildozer.spec nao encontrado" -ForegroundColor Red
    exit 1
}

# Backup
$ts = (Get-Date).ToString("yyyyMMdd_HHmmss")
Copy-Item $specPath "$specPath.bak_$ts" -Force
Write-Host "[OK] Backup: $specPath.bak_$ts" -ForegroundColor Green

# Le o conteudo
$content = Get-Content $specPath -Raw -Encoding UTF8

# Substitui a linha de requirements
$oldReq = 'requirements = python3,kivy==2.3.0,pyjnius==1.5.0,requests,urllib3,certifi'
$newReq = 'requirements = python3,kivy==2.3.0,pyjnius==1.5.0,requests,urllib3,certifi'

if ($content -match [regex]::Escape($oldReq)) {
    $content = $content.Replace($oldReq, $newReq)
    Write-Host "[OK] requirements atualizado:" -ForegroundColor Green
    Write-Host "     ANTES: $oldReq" -ForegroundColor DarkGray
    Write-Host "     DEPOIS: $newReq" -ForegroundColor Green
} elseif ($content -match 'requirements\s*=.*pyjnius') {
    Write-Host "[INFO] pyjnius ja esta no requirements" -ForegroundColor Cyan
} else {
    # Fallback: regex generica
    $content = $content -replace 'requirements\s*=\s*[^\r\n]+', $newReq
    Write-Host "[OK] requirements atualizado via regex" -ForegroundColor Green
}

# Bump da versao para 3.6.1 (opcional mas recomendado)
$content = $content -replace 'version\s*=\s*3\.5\.0', 'version = 3.6.1'
Write-Host "[OK] version: 3.5.0 -> 3.6.1" -ForegroundColor Green

# Salva
Set-Content -Path $specPath -Value $content -Encoding UTF8 -NoNewline
Write-Host "[OK] $specPath salvo" -ForegroundColor Green

# Mostra a linha final
Write-Host ""
Write-Host "Linha final:" -ForegroundColor Cyan
Select-String "requirements" $specPath | ForEach-Object { Write-Host "  $_" -ForegroundColor White }

# Commit + push
Write-Host ""
Write-Host "Fazendo commit + push..." -ForegroundColor Cyan
git add $specPath
git commit -m "fix(android): fixa pyjnius==1.5.0 e bump version 3.6.1"
git push origin main

Write-Host ""
Write-Host ("=" * 62) -ForegroundColor Green
Write-Host "  OK - Correcao enviada! GitHub Actions vai rebuildar" -ForegroundColor Green
Write-Host ("=" * 62) -ForegroundColor Green