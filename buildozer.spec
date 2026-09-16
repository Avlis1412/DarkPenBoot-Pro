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
# pyjnius      → ponte Java/Android (obrigatório para USB, permissões)
# requests     → HTTP
# urllib3      → backend do requests
# certifi      → certificados SSL
# ─────────────────────────────────────────────────────────────────
requirements = python3,kivy==2.3.0,pyjnius==1.5.0,requests,urllib3,certifi

# ─────────────────────────────────────────────────────────────────
# Interface
# ─────────────────────────────────────────────────────────────────
orientation = portrait
fullscreen = 0
# Não usar fullscreen=1 se quiser ver barra de status

# ─────────────────────────────────────────────────────────────────
# Ícone e Splash (descomente quando tiver os arquivos)
# ─────────────────────────────────────────────────────────────────
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

# ─────────────────────────────────────────────────────────────────
# Permissões Android
# INTERNET                → download de ISOs
# WRITE_EXTERNAL_STORAGE  → gravar ISOs e bootáveis
# READ_EXTERNAL_STORAGE   → ler ISOs existentes
# MANAGE_EXTERNAL_STORAGE → gerenciar arquivos (Android 11+)
# USB_PERMISSION          → detectar pendrive OTG ★ CRÍTICO ★
# WAKE_LOCK               → manter CPU acordada durante operações
# FOREGROUND_SERVICE      → rodar em background (Android 8+)
# ACCESS_NETWORK_STATE    → verificar conexão
# ACCESS_WIFI_STATE       → info de rede
# ─────────────────────────────────────────────────────────────────
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,USB_PERMISSION,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# ─────────────────────────────────────────────────────────────────
# SDK/NDK
# android.api = target do Android (33 = Android 13)
# android.minapi = mínimo suportado (21 = Android 5.0)
# android.ndk = versão do NDK (25b é estável)
# android.sdk NÃO é mais usado (depreciado) — removido
# ─────────────────────────────────────────────────────────────────
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# ─────────────────────────────────────────────────────────────────
# Arquiteturas
# arm64-v8a   → celulares modernos (2017+)
# armeabi-v7a → celulares antigos (2013+)
# ─────────────────────────────────────────────────────────────────
android.archs = arm64-v8a, armeabi-v7a

# ─────────────────────────────────────────────────────────────────
# Opções extras do Android
# ─────────────────────────────────────────────────────────────────
android.allow_backup = True
android.wakelock = True
android.entrypoint = org.kivy.android.PythonActivity

# ─────────────────────────────────────────────────────────────────
# python-for-android (versão estável fixa)
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