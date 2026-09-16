[app]
title = DarkPenBoot Pro
package.name = darkpenboot
package.domain = org.avlis1412

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,md,ttf,otf,ico
source.exclude_patterns = tests,*.pyc,__pycache__,.git,.github,build,dist,.venv,venv,env,bin,.buildozer,*.bak_*,*.bak,releases,deploy.*,fix-*.ps1,analyze.ps1,setup-*.ps1,*.spec,*.md

version = 3.6.1

requirements = python3,kivy==2.3.0,requests,urllib3,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,USB_PERMISSION,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.wakelock = True
android.entrypoint = org.kivy.android.PythonActivity

p4a.branch = develop

log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1