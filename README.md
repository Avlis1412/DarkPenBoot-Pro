# 🔌 DARKPENBOOT PRO

## Criador de Pendrives Bootáveis Multi-Plataforma

[![Version](https://img.shields.io/badge/version-3.5.0-blue?style=for-the-badge)](https://github.com/Avlis1412/DarkPenBoot-Pro/releases)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow?style=for-the-badge&logo=python)](https://www.python.org)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-purple?style=for-the-badge)
[![Build](https://github.com/Avlis1412/DarkPenBoot-Pro/actions/workflows/build.yml/badge.svg)](https://github.com/Avlis1412/DarkPenBoot-Pro/actions/workflows/build.yml)

Crie pendrives bootáveis de forma simples, rápida e segura.
Suporte a Windows, Linux, macOS, Android e NixOS — tudo em uma ferramenta.

Download • Recursos • Como Usar • NixOS • Build

---

## 📥 Download

| Plataforma | Arquivo | Link |
| :----------: | :-------: | :----: |
| 🪟 Windows | `DarkPenBoot.exe` | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |
| 🐧 Linux | `darkpenboot` (binário) | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |
| 🍏 macOS | `DarkPenBoot` (binário) | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |
| 📱 Android | `darkpenboot-*.apk` | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |

> 🔐 Cada download vem com arquivo `.sha256` para verificação.

### Verificação SHA256

```bash
# Linux/macOS
sha256sum -c darkpenboot.sha256

# Windows PowerShell
$esperado = (Get-Content DarkPenBoot.exe.sha256).Split()[0]
$calculado = (Get-FileHash DarkPenBoot.exe -Algorithm SHA256).Hash
if ($esperado -eq $calculado) { Write-Host "✅ Hash OK" -ForegroundColor Green }
```
