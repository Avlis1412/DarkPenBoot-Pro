[app]
p4a.branch = develop
title = DarkPenBoot Pro
package.name = darkpenboot
package.domain = org.avlis1412

source.dir = .
source.include_exts = py,kv,png,jpg,atlas,ttf,json
source.exclude_patterns = venv312,venv312_mobile,kivy_venv,.git,.github,build,dist,.buildozer,__pycache__,*.pyc,DarkPenBoot_PRO1.py,DPB_Launcher.py,analyze_code.py,scan_clean.ps1,scan_report.txt,run_desktop.ps1,run_mobile.ps1,setup_mobile.ps1,deploy.ps1,docs,tests,releases,.vscode,*.spec.bak,buildozer.spec.bak,requirements.txt,requirements-mobile.txt,pyproject.toml,DarkPenBoot.spec,.launcher_config.json,launch.json,build.sh,CHANGELOG.md,README_BUILD.md

version = 3.6.1

requirements = python3,kivy==2.2.1,requests,urllib3,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE,USB_PERMISSION,WAKE_LOCK,FOREGROUND_SERVICE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a

android.allow_backup = True
android.wakelock = True
android.entrypoint = org.kivy.android.PythonActivity


log_level = 1
warn_on_root = 1

[buildozer]
log_level = 1
warn_on_root = 1