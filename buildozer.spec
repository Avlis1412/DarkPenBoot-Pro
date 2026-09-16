[app]
title = DarkPenBoot Pro
package.name = darkpenboot
package.domain = org.avlis1412

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md,spec
source.exclude_patterns = tests,*.pyc,__pycache__,.git,build,dist,.venv,bin,.buildozer,*.bak_*,releases,*.md,deploy.*

version = 3.6.1

requirements = python3,kivy==2.3.0,pyjnius==1.5.0,requests,urllib3,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a

log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1