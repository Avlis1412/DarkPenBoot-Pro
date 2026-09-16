$spec = @'
[app]
# ─────────────────────────────────────────────────────────────────
# Identidade do App
# ─────────────────────────────────────────────────────────────────
title = DarkPenBoot Pro
package.name = darkpenboot
package.domain = org.avlis1412

# ─────────────────────────────────────────────────────────────────
# Código-fonte
# ─────────────────────────────────────────────────────────────────
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,md,ttf,otf,ico
source.exclude_patterns = tests,*.pyc,__pycache__,.git,.github,build,dist,.venv,venv,env,bin,.buildozer,*.bak_*,*.bak,releases,deploy.*,fix-*.ps1,analyze.ps1,setup-*.ps1,*.spec,*.md

# ─────────────────────────────────────────────────────────────────
# Versão
# ─────────────────────────────────────────────────────────────────
version = 3.6.1

# ─────────────────────────────────────────────────────────────────
# Dependências Python
# python3      → interpretador (obrigatório)
# kivy         → framework UI (versão fixa)
# pyjnius      → ponte Java/Android (p4a injeta automaticamente)
# requests     → HTTP
# urllib3      → backend do requests
# certifi      → certificados SSL
# ─────────────────────────────────────────────────────────────────
requirements = python3,kivy==2.3.0,requests,urllib3,certifi

# ─────────────────────────────────────────────────────────────────
# Interface
# ─────────────────────────────────────────────────────────────────
orientation = portrait
fullscreen = 0

# ─────────────────────────────────────────────────────────────────
# Ícone e Splash
# ─────────────────────────────────────────────────────────────────
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

# ─────────────────────────────────────────────────────────────────
# Permissões Android
# ─────────────────────────────────────────────────────────────────
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,USB_PERMISSION,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# ─────────────────────────────────────────────────────────────────
# SDK/NDK
# ─────────────────────────────────────────────────────────────────
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# ─────────────────────────────────────────────────────────────────
# Arquiteturas
# ─────────────────────────────────────────────────────────────────
android.archs = arm64-v8a, armeabi-v7a

# ─────────────────────────────────────────────────────────────────
# Opções extras
# ─────────────────────────────────────────────────────────────────
android.allow_backup = True
android.wakelock = True
android.entrypoint = org.kivy.android.PythonActivity

# ─────────────────────────────────────────────────────────────────
# python-for-android
# ─────────────────────────────────────────────────────────────────
p4a.branch = develop

# ─────────────────────────────────────────────────────────────────
# Log
# ─────────────────────────────────────────────────────────────────
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
'@

# Salva SEM BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText("$PWD\buildozer.spec", $spec, $utf8NoBom)

Write-Host ""
Write-Host "[OK] buildozer.spec atualizado (sem BOM)" -ForegroundColor Green
Write-Host ""

# Confere
$bytes = [System.IO.File]::ReadAllBytes("buildozer.spec")
Write-Host "Primeiros bytes: $($bytes[0..2] -join ',')  (esperado: 91,97,112)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Linha de requirements:" -ForegroundColor Cyan
Select-String "^requirements" buildozer.spec | ForEach-Object { Write-Host "  $_" }