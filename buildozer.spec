[app]

title = DarkPenBoot Pro
package.name = darkpenboot
package.domain = org.avlis1412

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md,spec
source.exclude_patterns = tests,*.pyc,__pycache__,.git,build,dist,.venv,bin,.buildozer

version = 3.5.0

# ─── Dependências Python ─────────────────────────────────────────────
# NOTA: não incluímos pyinstaller (é para desktop)
requirements = python3,kivy==2.3.0,requests,urllib3,certifi

# ─── Configurações Android ───────────────────────────────────────────
orientation = portrait
fullscreen = 0

# ─── Permissões ──────────────────────────────────────────────────────
# INTERNET: para downloads
# WRITE_EXTERNAL_STORAGE: para salvar ISOs em /sdcard
# READ_EXTERNAL_STORAGE: para listar ISOs existentes
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# ─── SDK ─────────────────────────────────────────────────────────────
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

# ─── Arquiteturas ────────────────────────────────────────────────────
android.archs = arm64-v8a, armeabi-v7a

# ─── Ícone (opcional) ────────────────────────────────────────────────
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

# ─── Log ─────────────────────────────────────────────────────────────
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1