# ═══════════════════════════════════════════════════════════════
#  Analisador de log do GitHub Actions — DarkPenBoot Pro
#  Baixa o log do último build falho, extrai e procura erros
# ═══════════════════════════════════════════════════════════════
$ErrorActionPreference = "Continue"

$Repo    = "Avlis1412/DarkPenBoot-Pro"
$WorkDir = "C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
$LogsDir = Join-Path $WorkDir "_ci_logs"

Set-Location $WorkDir

function Write-Head($t) { Write-Host ""; Write-Host "=== $t ===" -ForegroundColor Cyan }
function Write-Ok($t)   { Write-Host "[OK] $t" -ForegroundColor Green }
function Write-Warn($t) { Write-Host "[!] $t" -ForegroundColor Yellow }
function Write-Err($t)  { Write-Host "[X] $t" -ForegroundColor Red }

Write-Head "1. Verificando dependencias"
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Warn "gh (GitHub CLI) nao encontrado. Instalando via winget..."
    winget install --id GitHub.cli --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        Write-Err "Instale manualmente: https://cli.github.com/"
        exit 1
    }
    Write-Warn "Feche e reabra o PowerShell, depois rode de novo."
    exit 0
}
Write-Ok "gh: $(gh --version | Select-Object -First 1)"

Write-Head "2. Autenticacao GitHub"
$authStatus = gh auth status 2>&1
if ($authStatus -match "not logged") {
    Write-Warn "Faca login (uma vez so):"
    Write-Host "  gh auth login" -ForegroundColor Yellow
    Write-Host "  Escolha: GitHub.com > HTTPS > Login with web browser" -ForegroundColor Gray
    exit 0
}
Write-Ok "Autenticado"

Write-Head "3. Buscando ultimo build falho"
$runs = gh run list --repo $Repo --limit 10 --json databaseId,conclusion,name,createdAt,headBranch | ConvertFrom-Json
$failRun = $runs | Where-Object { $_.conclusion -eq "failure" } | Select-Object -First 1

if (-not $failRun) {
    Write-Err "Nenhum build falho encontrado."
    Write-Host "Builds recentes:" -ForegroundColor Yellow
    $runs | ForEach-Object {
        Write-Host "  #$($_.databaseId)  $($_.conclusion)  $($_.name)"
    }
    exit 0
}

Write-Ok "Build #$($failRun.databaseId) - $($failRun.name)"
Write-Host "  Branch: $($failRun.headBranch)" -ForegroundColor Gray
Write-Host "  Data:   $($failRun.createdAt)" -ForegroundColor Gray

Write-Head "4. Baixando logs"
if (Test-Path $LogsDir) { Remove-Item $LogsDir -Recurse -Force -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null

gh run view $failRun.databaseId --repo $Repo --log > "$LogsDir\full_log.txt" 2>&1

if (-not (Test-Path "$LogsDir\full_log.txt")) {
    Write-Err "Falha ao baixar logs."
    exit 1
}
$logSize = (Get-Item "$LogsDir\full_log.txt").Length
Write-Ok "Log baixado: $([math]::Round($logSize/1MB, 2)) MB"

Write-Head "5. Procurando erros"

$patterns = @(
    @{ Name = "sdkmanager";    Regex = "Broken pipe|Could not determine java|sdkmanager.*failed|Accept.*licenses" },
    @{ Name = "Python CI";     Regex = "python3\.(13|14)|No module named|ModuleNotFoundError" },
    @{ Name = "p4a";           Regex = "python-for-android.*fail|p4a.*error|p4a.*not found" },
    @{ Name = "NDK / gcc";     Regex = "error:|fatal error|gcc.*failed|clang.*failed|undefined reference" },
    @{ Name = "Buildozer";     Regex = "Buildozer failed|Command failed|exit code 1|exit status 1" },
    @{ Name = "Cython/Kivy";   Regex = "Cython.*fail|kivy.*build.*fail|cythonize" },
    @{ Name = "pip install";   Regex = "pip.*error|Could not find a version|No matching distribution" },
    @{ Name = "Java";          Regex = "JAVA_HOME|java version|javac" }
)

$results = @()
$logContent = Get-Content "$LogsDir\full_log.txt" -Raw

foreach ($p in $patterns) {
    $matches = [regex]::Matches($logContent, $p.Regex, 'IgnoreCase')
    if ($matches.Count -gt 0) {
        $results += [PSCustomObject]@{
            Categoria = $p.Name
            Ocorrencias = $matches.Count
        }
        Write-Host ("  [!] {0,-15} {1} ocorrencia(s)" -f $p.Name, $matches.Count) -ForegroundColor Yellow
    }
}

if ($results.Count -eq 0) {
    Write-Warn "Nenhum padrao de erro conhecido encontrado."
    Write-Host "  O log pode usar formato diferente. Abra manualmente:" -ForegroundColor Gray
    Write-Host "  $LogsDir\full_log.txt" -ForegroundColor Gray
    exit 0
}

Write-Head "6. Extraindo contexto dos erros"

# Pega as primeiras 3 ocorrencias de cada categoria e mostra 5 linhas antes/depois
foreach ($p in $patterns) {
    $matches = [regex]::Matches($logContent, $p.Regex, 'IgnoreCase')
    if ($matches.Count -eq 0) { continue }

    Write-Host ""
    Write-Host "───── $($p.Name) ─────" -ForegroundColor Magenta

    $shown = 0
    foreach ($m in $matches) {
        if ($shown -ge 3) { break }
        $shown++

        $start = [Math]::Max(0, $m.Index - 500)
        $len = [Math]::Min(1200, $logContent.Length - $start)
        $context = $logContent.Substring($start, $len)

        $lines = $context -split "`n"
        Write-Host ""
        Write-Host "  [match #$shown em posicao $($m.Index)]" -ForegroundColor Gray
        foreach ($line in $lines) {
            if ($line -match $p.Regex) {
                Write-Host "  > $line" -ForegroundColor Red
            } else {
                Write-Host "    $line" -ForegroundColor DarkGray
            }
        }
    }
}

Write-Head "7. Resumo final"
Write-Host ""
Write-Host "Log completo em:" -ForegroundColor White
Write-Host "  $LogsDir\full_log.txt" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para abrir:" -ForegroundColor White
Write-Host "  notepad `"$LogsDir\full_log.txt`"" -ForegroundColor Gray
Write-Host ""

# Sugestoes automaticas
$sugestoes = @()
if ($results.Categoria -contains "sdkmanager") {
    $sugestoes += "sdkmanager: adicionar 'android.accept_sdk_license = True' no buildozer.spec"
}
if ($results.Categoria -contains "Python CI") {
    $sugestoes += "Python CI: fixar 'python-version: 3.11' no workflow"
}
if ($results.Categoria -contains "p4a") {
    $sugestoes += "p4a: forcar 'p4a.branch = develop' no buildozer.spec"
}
if ($results.Categoria -contains "NDK / gcc") {
    $sugestoes += "NDK: verificar versao do NDK (25b) e arquitetura arm64-v8a"
}

if ($sugestoes.Count -gt 0) {
    Write-Host "Sugestoes de correcao:" -ForegroundColor Yellow
    foreach ($s in $sugestoes) {
        Write-Host "  - $s" -ForegroundColor White
    }
}

Write-Host ""
Write-Ok "Analise concluida."
